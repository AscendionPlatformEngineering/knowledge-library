"""T3.1 tests — index.json output of tools/build_index_json.py.

Run from repo root:
    python3 -m pytest tools/test_build_index_json.py -v

Drives EPIC-3 T3.1. Until tools/build_index_json.py exists, every test is
expected to fail at fixture setup (subprocess.CalledProcessError) — that
failure is the spec for the implementation.

Output contract (locked):
    - Path: dist/knowledge-graph/agent/v1/index.json
    - Top-level keys: schema_version, nodes, edges, lenses
    - schema_version == "1.0"
    - edges renamed from compute_graph_data's "links"
    - sort_keys=True, indent=2, trailing newline, byte-deterministic
"""
import hashlib
import json
import subprocess
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / "dist" / "knowledge-graph" / "agent" / "v1" / "index.json"


def _run_builder():
    subprocess.run(
        ["python3", "tools/build_index_json.py"],
        check=True,
        cwd=REPO_ROOT,
        capture_output=True,
    )


def _rebuild_clean():
    if INDEX_PATH.exists():
        INDEX_PATH.unlink()
    _run_builder()


@pytest.fixture(scope="session")
def built():
    _run_builder()
    return True


@pytest.fixture(scope="session")
def index(built):
    return json.loads(INDEX_PATH.read_text())


def test_index_file_exists(built):
    assert INDEX_PATH.exists()


def test_schema_version(index):
    assert index["schema_version"] == "1.0"


def test_top_level_keys(index):
    assert set(index.keys()) == {"schema_version", "nodes", "edges", "lenses"}


def test_node_counts(index):
    pages = [n for n in index["nodes"] if n["type"] == "page"]
    standards = [n for n in index["nodes"] if n["type"] == "standard"]
    sections = [n for n in index["nodes"] if n["type"] == "section"]
    assert len(pages) == 73
    assert len(standards) == 224
    assert len(sections) == 18
    assert len(index["nodes"]) == 315


def test_edge_count_and_shape(index):
    assert len(index["edges"]) == 620
    node_ids = {n["id"] for n in index["nodes"]}
    edge_kinds = set()
    for edge in index["edges"]:
        assert set(edge.keys()) == {"source", "target", "kind"}
        assert edge["source"] in node_ids
        assert edge["target"] in node_ids
        edge_kinds.add(edge["kind"])
    assert "contains" in edge_kinds
    assert "alignment" in edge_kinds
    assert "related" in edge_kinds


def test_page_node_required_fields(index):
    expected = {"id", "label", "section", "type", "url", "description", "lenses"}
    for node in index["nodes"]:
        if node["type"] != "page":
            continue
        assert set(node.keys()) == expected
        assert isinstance(node["lenses"], list)


def test_standard_node_required_fields(index):
    expected = {"id", "label", "type", "url", "description"}
    for node in index["nodes"]:
        if node["type"] != "standard":
            continue
        assert set(node.keys()) == expected
        assert "lenses" not in node


def test_lenses_definitions(index):
    assert len(index["lenses"]) >= 1
    expected_keys = {"id", "label", "description", "members", "caption_source"}
    for lens in index["lenses"]:
        assert set(lens.keys()) == expected_keys

    debt_ledger = next(l for l in index["lenses"] if l["id"] == "debt-ledger")
    assert debt_ledger["label"] == "Debt Ledger"
    assert len(debt_ledger["members"]) == 8

    expected_members = {
        "nfr/maintainability",
        "nfr/security",
        "nfr/reliability",
        "nfr/usability",
        "compliance/bsp-afasa",
        "compliance/gdpr",
        "compliance/iso27001",
        "compliance/pci-dss",
    }
    assert expected_members.issubset(set(debt_ledger["members"]))
    assert debt_ledger["members"] == sorted(debt_ledger["members"])
    assert debt_ledger["caption_source"] == "nfr/usability"


def test_lens_members_resolve_to_pages(index):
    page_ids = {n["id"] for n in index["nodes"] if n["type"] == "page"}
    for lens in index["lenses"]:
        for member in lens["members"]:
            assert member in page_ids, (
                f"lens {lens['id']!r} member {member!r} not found as page node"
            )


def test_section_nodes_present_in_published_index(index):
    """The published index.json includes 18 section nodes with label and description."""
    section_nodes = [n for n in index["nodes"] if n["type"] == "section"]
    assert len(section_nodes) == 18
    for n in section_nodes:
        assert n["id"] and isinstance(n["id"], str)
        assert n["label"] and isinstance(n["label"], str)
        assert n["description"] and isinstance(n["description"], str)
        # No lenses on sections
        assert "lenses" not in n


def test_byte_deterministic_index_json():
    _rebuild_clean()
    first = INDEX_PATH.read_bytes()
    hash1 = hashlib.sha256(first).hexdigest()

    _rebuild_clean()
    second = INDEX_PATH.read_bytes()
    hash2 = hashlib.sha256(second).hexdigest()

    assert hash1 == hash2
