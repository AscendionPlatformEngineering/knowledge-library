#!/usr/bin/env python3
"""T2.2 — embed chunk corpus with BGE and build HNSW index for cosine search.

Inputs:
    dist/knowledge-graph/agent/v1/chunks.json  (from T2.1)

Outputs (byte-deterministic):
    dist/knowledge-graph/agent/v1/vectors.bin
        bytes 0-3:  uint32 LE = num_vectors
        bytes 4-7:  uint32 LE = dims (384)
        bytes 8+:   float32 LE, num_vectors * dims values, L2-normalized
    dist/knowledge-graph/agent/v1/index.bin
        hnswlib HNSW index, space='cosine', dim=384

Locked decisions:
    Embedding model: BAAI/bge-small-en-v1.5
    HNSW: M=16, ef_construction=200, ef_search=50, random_seed=42
    Determinism: set_num_threads(1) before init_index, single seed
"""

import json
import os
import struct
import sys
from pathlib import Path

import numpy as np


REPO_ROOT = Path(__file__).resolve().parent.parent
AGENT_DIR = REPO_ROOT / "dist" / "knowledge-graph" / "agent" / "v1"
CHUNKS_PATH = AGENT_DIR / "chunks.json"
VECTORS_PATH = AGENT_DIR / "vectors.bin"
INDEX_PATH = AGENT_DIR / "index.bin"

MODEL_NAME = "BAAI/bge-small-en-v1.5"
DIMS = 384
HNSW_M = 16
HNSW_EF_CONSTRUCTION = 200
HNSW_EF_SEARCH = 50
HNSW_SEED = 42


def main():
    if not CHUNKS_PATH.exists():
        print(f"ERROR: {CHUNKS_PATH} missing — run tools/build_chunks.py first.", file=sys.stderr)
        sys.exit(1)

    with open(CHUNKS_PATH) as f:
        data = json.load(f)
    chunks = data["chunks"]
    n = len(chunks)
    texts = [c["text"] for c in chunks]

    # Pin thread counts for determinism before any heavy compute.
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
        batch_size=32,
    )
    embeddings = np.ascontiguousarray(embeddings.astype(np.float32))

    assert embeddings.shape == (n, DIMS), (
        f"embedding shape {embeddings.shape}, expected {(n, DIMS)}"
    )

    AGENT_DIR.mkdir(parents=True, exist_ok=True)

    with open(VECTORS_PATH, "wb") as f:
        f.write(struct.pack("<II", n, DIMS))
        f.write(embeddings.tobytes(order="C"))

    import hnswlib

    index = hnswlib.Index(space="cosine", dim=DIMS)
    index.set_num_threads(1)
    index.init_index(
        max_elements=n,
        M=HNSW_M,
        ef_construction=HNSW_EF_CONSTRUCTION,
        random_seed=HNSW_SEED,
    )
    index.set_ef(HNSW_EF_SEARCH)
    index.add_items(embeddings, ids=list(range(n)))
    index.save_index(str(INDEX_PATH))

    print("─" * 60)
    print(
        f"Vectors: {n} encoded into vectors.bin and index.bin built "
        f"(M={HNSW_M}) -> {AGENT_DIR.relative_to(REPO_ROOT)}"
    )


if __name__ == "__main__":
    main()
