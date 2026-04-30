"""T2.2 tests — vector index output of tools/build_vector_index.py.

Run from repo root:
    python3 -m pytest tools/test_build_vector_index.py -v

Drives EPIC-2 T2.2. Until tools/build_vector_index.py exists, every test is
expected to fail at fixture setup (subprocess.CalledProcessError) — that
failure is the spec for the implementation.

Output contract (locked):
    - dist/knowledge-graph/agent/v1/vectors.bin
        bytes 0-3:  uint32 LE = num_vectors (724)
        bytes 4-7:  uint32 LE = dims (384)
        bytes 8+:   float32 LE, num_vectors × dims values, L2-normalized
        total size: 8 + 724 * 384 * 4 = 1,112,072 bytes
    - dist/knowledge-graph/agent/v1/index.bin
        hnswlib index, space='cosine', dim=384
        labels = chunk index in chunks.json order
        M=16, ef_construction=200, ef_search=50, random_seed=42
"""
import hashlib
import json
import struct
import subprocess
from pathlib import Path

import numpy as np
import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
AGENT_DIR = REPO_ROOT / "dist" / "knowledge-graph" / "agent" / "v1"
CHUNKS_PATH = AGENT_DIR / "chunks.json"
VECTORS_PATH = AGENT_DIR / "vectors.bin"
INDEX_PATH = AGENT_DIR / "index.bin"
BUILDER = TOOLS_DIR / "build_vector_index.py"

NUM_VECTORS = 724
DIMS = 384
HEADER_SIZE = 8
EXPECTED_VECTORS_BYTES = HEADER_SIZE + NUM_VECTORS * DIMS * 4  # 1_112_072
BGE_MODEL_NAME = "BAAI/bge-small-en-v1.5"


def _run_builder():
    """Invoke build_vector_index.py from repo root. Raises on non-zero exit."""
    subprocess.run(
        ["python3", str(BUILDER)],
        check=True,
        cwd=REPO_ROOT,
        capture_output=True,
    )


def _rebuild_clean():
    """Delete outputs and rebuild — used by determinism tests."""
    for p in (VECTORS_PATH, INDEX_PATH):
        if p.exists():
            p.unlink()
    _run_builder()


@pytest.fixture(scope="session")
def built():
    """Run the builder once for the session. Tests 2-8 reuse artifacts."""
    _run_builder()
    if not AGENT_DIR.exists():
        pytest.skip("agent/v1 dir not produced — infra issue, not content issue")
    return True


@pytest.fixture(scope="session")
def chunks(built):
    with open(CHUNKS_PATH) as f:
        return json.load(f)["chunks"]


@pytest.fixture(scope="session")
def vectors(built):
    """Parsed (num, dim, float32 grid) from vectors.bin."""
    raw = VECTORS_PATH.read_bytes()
    num = struct.unpack("<I", raw[0:4])[0]
    dim = struct.unpack("<I", raw[4:8])[0]
    grid = np.frombuffer(raw[HEADER_SIZE:], dtype="<f4").reshape(num, dim)
    return num, dim, grid


@pytest.fixture(scope="session")
def bge_model(built):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(BGE_MODEL_NAME)


@pytest.fixture(scope="session")
def hnsw_index(built):
    import hnswlib
    idx = hnswlib.Index(space="cosine", dim=DIMS)
    idx.load_index(str(INDEX_PATH))
    idx.set_ef(50)
    return idx


# ─────────────────────────── Tests ──────────────────────────────


def test_vectors_file_exists(built):
    assert VECTORS_PATH.exists(), f"{VECTORS_PATH} not produced by build_vector_index.py"


def test_index_file_exists(built):
    assert INDEX_PATH.exists(), f"{INDEX_PATH} not produced by build_vector_index.py"


def test_vectors_header_correct(built):
    raw = VECTORS_PATH.read_bytes()[:HEADER_SIZE]
    num = struct.unpack("<I", raw[0:4])[0]
    dim = struct.unpack("<I", raw[4:8])[0]
    assert num == NUM_VECTORS, f"header num_vectors {num}, expected {NUM_VECTORS}"
    assert dim == DIMS, f"header dims {dim}, expected {DIMS}"


def test_vectors_total_size(built):
    size = VECTORS_PATH.stat().st_size
    assert size == EXPECTED_VECTORS_BYTES, (
        f"vectors.bin size {size}, expected {EXPECTED_VECTORS_BYTES} "
        f"(8 header + {NUM_VECTORS} * {DIMS} * 4)"
    )


def test_vectors_are_normalized(vectors):
    num, dim, grid = vectors
    rng = np.random.default_rng(42)
    sample_idx = rng.choice(num, size=50, replace=False)
    norms = np.linalg.norm(grid[sample_idx], axis=1)
    deviations = np.abs(norms - 1.0)
    worst = float(deviations.max())
    assert worst < 1e-4, (
        f"L2 norm deviates from 1.0 by {worst} on sampled vectors; "
        f"BGE embeddings must be normalized"
    )


def test_index_loads_and_queries(hnsw_index, bge_model, chunks):
    query = "what is the debt ledger pattern?"
    qvec = bge_model.encode([query], normalize_embeddings=True)
    labels, _ = hnsw_index.knn_query(qvec, k=5)
    top_labels = labels[0].tolist()
    top_page_ids = [chunks[i]["page_id"] for i in top_labels]
    hit = any(
        pid.startswith("nfr/maintainability") or pid.startswith("compliance/")
        for pid in top_page_ids
    )
    assert hit, (
        f"semantic search for {query!r} returned no nfr/maintainability or "
        f"compliance/* page in top-5; got {top_page_ids}"
    )


def test_known_chunk_self_match(hnsw_index, bge_model, chunks):
    target_id = "nfr/maintainability:caption"
    target = next((c for c in chunks if c["id"] == target_id), None)
    assert target is not None, f"chunk {target_id!r} missing from chunks.json"
    target_idx = chunks.index(target)

    qvec = bge_model.encode([target["text"]], normalize_embeddings=True)
    labels, distances = hnsw_index.knn_query(qvec, k=1)
    top_label = int(labels[0][0])
    top_distance = float(distances[0][0])
    similarity = 1.0 - top_distance

    assert top_label == target_idx, (
        f"self-match failed: top-1 label {top_label} (chunk {chunks[top_label]['id']!r}), "
        f"expected {target_idx} ({target_id!r})"
    )
    assert similarity > 0.95, (
        f"self-match cosine similarity {similarity:.4f} below 0.95"
    )


def test_byte_deterministic_vectors():
    _rebuild_clean()
    h1 = hashlib.sha256(VECTORS_PATH.read_bytes()).hexdigest()
    _rebuild_clean()
    h2 = hashlib.sha256(VECTORS_PATH.read_bytes()).hexdigest()
    assert h1 == h2, f"vectors.bin not byte-deterministic: {h1} vs {h2}"


def test_byte_deterministic_index():
    _rebuild_clean()
    h1 = hashlib.sha256(INDEX_PATH.read_bytes()).hexdigest()
    _rebuild_clean()
    h2 = hashlib.sha256(INDEX_PATH.read_bytes()).hexdigest()
    assert h1 == h2, f"index.bin not byte-deterministic: {h1} vs {h2}"
