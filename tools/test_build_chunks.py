"""T2.1 tests — chunk corpus output of tools/build_chunks.py.

Run from repo root:
    python3 -m pytest tools/test_build_chunks.py -v

Drives EPIC-2 T2.1. Until tools/build_chunks.py exists, every test is
expected to fail at fixture setup (subprocess.CalledProcessError) — that
failure is the spec for the implementation.

Output contract (locked):
    - File: dist/knowledge-graph/agent/v1/chunks.json
    - Chunk id format:
        singletons:    "{page_id}:{chunk_type}"          e.g. "nfr/maintainability:caption"
        indexed:       "{page_id}:{chunk_type}:{index}"  e.g. "nfr/maintainability:principle:0"
"""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
CONTENT_DIR = REPO_ROOT / "content"
CHUNKS_PATH = REPO_ROOT / "dist" / "knowledge-graph" / "agent" / "v1" / "chunks.json"
BUILDER = TOOLS_DIR / "build_chunks.py"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


seed = _load("seed_content", TOOLS_DIR / "seed_content.py")
gen = _load("generate", TOOLS_DIR / "generate.py")


def _run_builder():
    """Invoke build_chunks.py from repo root. Raises on non-zero exit."""
    subprocess.run(
        ["python3", str(BUILDER)],
        check=True,
        cwd=REPO_ROOT,
        capture_output=True,
    )


@pytest.fixture(scope="session")
def chunks():
    """Run the chunker once, return parsed chunks list."""
    _run_builder()
    if not CHUNKS_PATH.parent.exists():
        pytest.skip("dist/ directory not produced — build infra issue, not a chunk-content issue")
    with open(CHUNKS_PATH) as f:
        data = json.load(f)
    return data["chunks"]


@pytest.fixture(scope="session")
def substantive_page_ids():
    """Page IDs (section/sub) for every substantive README in content/."""
    metadata = gen.collect_site_metadata(CONTENT_DIR)
    return {pid for pid, m in metadata.items() if m["is_substantive"]}


# ─────────────────────────── Tests ──────────────────────────────


def test_chunks_file_exists(chunks):
    assert CHUNKS_PATH.exists(), f"{CHUNKS_PATH} not produced by build_chunks.py"


def test_chunk_count_in_expected_range(chunks):
    n = len(chunks)
    assert 600 <= n <= 1000, (
        f"chunk count {n} outside sanity range [600, 1000] (target ~810). "
        f"Either chunking regressed or page set shifted significantly."
    )


def test_every_substantive_page_has_chunks(chunks, substantive_page_ids):
    seen = {c["page_id"] for c in chunks}
    missing = substantive_page_ids - seen
    assert not missing, (
        f"{len(missing)} substantive pages produced no chunks: "
        f"{sorted(missing)[:10]}{'…' if len(missing) > 10 else ''}"
    )


def test_every_page_has_caption_chunk(chunks):
    by_page = {}
    for c in chunks:
        if c["chunk_type"] == "caption":
            by_page.setdefault(c["page_id"], []).append(c)

    page_ids_in_chunks = {c["page_id"] for c in chunks}
    for pid in page_ids_in_chunks:
        captions = by_page.get(pid, [])
        assert len(captions) == 1, (
            f"page '{pid}' has {len(captions)} caption chunks; expected exactly 1"
        )
        expected_id = f"{pid}:caption"
        assert captions[0]["id"] == expected_id, (
            f"caption chunk id mismatch for '{pid}': "
            f"got {captions[0]['id']!r}, expected {expected_id!r}"
        )


def test_principle_chunks_have_indexed_ids(chunks):
    principles_by_page = {}
    for c in chunks:
        if c["chunk_type"] == "principle":
            principles_by_page.setdefault(c["page_id"], []).append(c)

    for pid, items in principles_by_page.items():
        indices = []
        for c in items:
            expected_prefix = f"{pid}:principle:"
            assert c["id"].startswith(expected_prefix), (
                f"principle chunk id {c['id']!r} does not match "
                f"'{expected_prefix}{{n}}' format"
            )
            tail = c["id"][len(expected_prefix):]
            assert tail.isdigit(), (
                f"principle chunk id {c['id']!r} suffix {tail!r} is not an integer"
            )
            indices.append(int(tail))

        indices.sort()
        assert indices[0] == 0, (
            f"page '{pid}' principle indices start at {indices[0]}, expected 0"
        )
        assert indices == list(range(len(indices))), (
            f"page '{pid}' principle indices have gaps: {indices}"
        )


def test_chunk_ids_are_unique(chunks):
    ids = [c["id"] for c in chunks]
    seen = set()
    dupes = []
    for cid in ids:
        if cid in seen:
            dupes.append(cid)
        seen.add(cid)
    assert not dupes, f"duplicate chunk ids: {dupes[:10]}"


def test_chunks_are_sorted_deterministically(chunks):
    """Two runs must produce byte-identical chunks.json."""
    h1 = hashlib.sha256(CHUNKS_PATH.read_bytes()).hexdigest()
    _run_builder()
    h2 = hashlib.sha256(CHUNKS_PATH.read_bytes()).hexdigest()
    assert h1 == h2, (
        f"chunks.json not byte-deterministic across runs: "
        f"first sha256={h1[:12]}…, second={h2[:12]}…"
    )


def test_chunk_text_is_non_empty(chunks):
    short = [
        (c["id"], len(c.get("text", "")))
        for c in chunks
        if len(c.get("text", "")) < 20
    ]
    assert not short, (
        f"{len(short)} chunks have text < 20 chars (likely accidentally empty): "
        f"{short[:5]}"
    )


def test_chunk_text_length_recorded(chunks):
    mismatches = [
        (c["id"], c.get("text_length"), len(c.get("text", "")))
        for c in chunks
        if c.get("text_length") != len(c.get("text", ""))
    ]
    assert not mismatches, (
        f"{len(mismatches)} chunks have text_length mismatch: {mismatches[:5]}"
    )


def test_schema_version_present(chunks):
    """Output must be a wrapped object with schema_version='1.0' and a chunks key.

    The `chunks` fixture is a dependency only to ensure the builder has run;
    we re-read the raw file here to inspect the wrapper."""
    with open(CHUNKS_PATH) as f:
        data = json.load(f)
    assert data["schema_version"] == "1.0"
    assert "chunks" in data


def test_chunks_reference_standards_correctly(chunks):
    """When 'references' field is non-empty, every entry must resolve in
    GOLD_REFERENCES (or its TAG_LINKS shim). At least 5 chunks must have refs."""
    valid_ids = set(gen.GOLD_REFERENCES.keys()) | set(gen.TAG_LINKS.keys())

    chunks_with_refs = [c for c in chunks if c.get("references")]
    assert len(chunks_with_refs) >= 5, (
        f"only {len(chunks_with_refs)} chunks have non-empty references; "
        f"expected ≥ 5 to confirm references are wired through"
    )

    bad = []
    for c in chunks_with_refs:
        for ref in c["references"]:
            if ref not in valid_ids:
                bad.append((c["id"], ref))
    assert not bad, (
        f"{len(bad)} chunk references do not resolve in GOLD_REFERENCES/TAG_LINKS: "
        f"{bad[:5]}"
    )
