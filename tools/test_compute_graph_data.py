"""T1.3 tests — lens annotation on graph page nodes.

Run from repo root:
    python3 -m pytest tools/test_compute_graph_data.py -v

These tests will FAIL until compute_graph_data() is updated to attach a
"lenses" field to page nodes. That failure is intentional — drives T1.3.
"""
import importlib.util
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
CONTENT_DIR = REPO_ROOT / "content"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# Modules are not packaged — load by path so tests work from repo root.
seed = _load("seed_content", TOOLS_DIR / "seed_content.py")
gen = _load("generate", TOOLS_DIR / "generate.py")


def _graph():
    metadata = gen.collect_site_metadata(CONTENT_DIR)
    return gen.compute_graph_data(metadata)


def _nodes_by_id(graph):
    return {n["id"]: n for n in graph["nodes"]}


def test_ledger_pages_have_debt_ledger_lens():
    """Every debt-ledger member page node must carry lenses == ['debt-ledger']."""
    graph = _graph()
    by_id = _nodes_by_id(graph)
    members = seed.CONCEPT_LENSES["debt-ledger"]["members"]

    assert len(members) == 8, (
        f"Expected 8 debt-ledger members, got {len(members)}: {members}"
    )

    for member_id in members:
        node = by_id.get(member_id)
        assert node is not None, (
            f"debt-ledger member '{member_id}' missing from graph nodes — "
            f"page renamed or excluded?"
        )
        assert "lenses" in node, (
            f"page node '{member_id}' missing 'lenses' field. "
            f"compute_graph_data() needs to attach lens annotation. "
            f"Node keys: {sorted(node.keys())}"
        )
        assert node["lenses"] == ["debt-ledger"], (
            f"page node '{member_id}' has lenses={node['lenses']!r}, "
            f"expected ['debt-ledger']."
        )


def test_non_ledger_pages_have_empty_lenses():
    """Substantive pages outside any lens must have lenses == []."""
    graph = _graph()
    by_id = _nodes_by_id(graph)
    sample = [
        "principles/foundational",
        "system-design/scalable",
        "technology/devops",
    ]

    for page_id in sample:
        node = by_id.get(page_id)
        assert node is not None, (
            f"sample page '{page_id}' missing from graph — "
            f"check that it is substantive and registered in TAXONOMY."
        )
        assert node["type"] == "page", (
            f"sample '{page_id}' is type={node['type']!r}, expected 'page'."
        )
        assert "lenses" in node, (
            f"page node '{page_id}' missing 'lenses' field. "
            f"All page nodes must have 'lenses' (empty list if no lens). "
            f"Node keys: {sorted(node.keys())}"
        )
        assert node["lenses"] == [], (
            f"page node '{page_id}' has lenses={node['lenses']!r}, "
            f"expected [] (page is in no declared lens)."
        )


def test_standard_nodes_have_no_lenses_field():
    """Standard (alignment-tag) nodes must NOT carry a lenses field — lenses
    are a page-only concept."""
    graph = _graph()
    standards = [n for n in graph["nodes"] if n["type"] == "standard"]
    assert len(standards) >= 3, (
        f"Expected at least 3 standard nodes, got {len(standards)}."
    )

    for node in standards[:10]:
        assert "lenses" not in node, (
            f"standard node '{node['id']}' unexpectedly has 'lenses' field "
            f"(value={node.get('lenses')!r}). Lenses are page-only."
        )


def test_node_count_unchanged_by_annotation():
    """Graph data shape regression guard.

    The total node count must equal the sum of typed components (pages, standards, sections),
    and total links must equal the sum of typed kinds (alignment, related, contains).
    Catches accidental orphan node types or edge kinds.
    """
    graph = _graph()
    pages = [n for n in graph["nodes"] if n["type"] == "page"]
    standards = [n for n in graph["nodes"] if n["type"] == "standard"]
    sections = [n for n in graph["nodes"] if n["type"] == "section"]
    contains_edges = [e for e in graph["links"] if e["kind"] == "contains"]
    alignment_edges = [e for e in graph["links"] if e["kind"] == "alignment"]
    related_edges = [e for e in graph["links"] if e["kind"] == "related"]

    assert len(pages) == 73, (
        f"page node count drift: got {len(pages)}, expected 73."
    )
    assert len(standards) == 224, (
        f"standard node count drift: got {len(standards)}, expected 224."
    )
    # Total nodes must equal pages + standards + sections (no orphan node types).
    assert len(graph["nodes"]) == len(pages) + len(standards) + len(sections), (
        f"total node count drift: got {len(graph['nodes'])}, "
        f"expected pages({len(pages)}) + standards({len(standards)}) + sections({len(sections)}) "
        f"= {len(pages) + len(standards) + len(sections)}. Possible orphan node type."
    )
    # Total links must equal alignment + related + contains (no orphan edge kinds).
    assert len(graph["links"]) == len(alignment_edges) + len(related_edges) + len(contains_edges), (
        f"total link count drift: got {len(graph['links'])}, "
        f"expected alignment({len(alignment_edges)}) + related({len(related_edges)}) + contains({len(contains_edges)}) "
        f"= {len(alignment_edges) + len(related_edges) + len(contains_edges)}. Possible orphan edge kind."
    )


def test_all_lens_members_resolve_to_real_pages():
    """Every member of every lens must appear as a page node — catches drift
    when a page is renamed without updating CONCEPT_LENSES."""
    graph = _graph()
    by_id = _nodes_by_id(graph)

    for lens_id, lens in seed.CONCEPT_LENSES.items():
        for member_id in lens["members"]:
            node = by_id.get(member_id)
            assert node is not None, (
                f"CONCEPT_LENSES['{lens_id}'] member '{member_id}' has no "
                f"matching page node in the graph. Page may have been "
                f"renamed, destubbed, or removed without updating "
                f"seed_content.CONCEPT_LENSES."
            )
            assert node["type"] == "page", (
                f"lens member '{member_id}' resolved to type "
                f"{node['type']!r}, expected 'page'."
            )


# ─────────────────────── T4.1 — section nodes + contains edges ─────────────────────


@pytest.fixture(scope="module")
def graph():
    """Module-scoped graph build — reused across the T4.1 tests below."""
    return _graph()


def test_section_nodes_count_is_eighteen(graph):
    """Exactly 18 section nodes — one per substantive section."""
    section_nodes = [n for n in graph["nodes"] if n["type"] == "section"]
    assert len(section_nodes) == 18, (
        f"Expected 18 sections, got {len(section_nodes)}"
    )


def test_section_node_ids_match_expected_set(graph):
    """The 18 section IDs are exactly the substantive sections."""
    EXPECTED = {
        "ai-native", "checklists", "compliance", "governance", "maturity",
        "nfr", "observability", "patterns", "playbooks", "principles",
        "runbooks", "scorecards", "security", "strategy", "system-design",
        "technology", "templates", "tools",
    }
    section_ids = {n["id"] for n in graph["nodes"] if n["type"] == "section"}
    assert section_ids == EXPECTED


def test_no_section_node_for_stub_only_sections(graph):
    """The 13 stub-only sections must NOT have section nodes."""
    EXCLUDED = {
        "adrs", "ai", "anti-patterns", "cloud", "data", "ddd", "design",
        "frameworks", "infra", "integration", "roadmaps", "tech", "views",
    }
    section_ids = {n["id"] for n in graph["nodes"] if n["type"] == "section"}
    overlap = section_ids & EXCLUDED
    assert not overlap, f"Stub-only sections leaked into graph: {overlap}"


def test_each_section_has_required_fields(graph):
    """Section nodes have exactly: id, type, label, description. No extras, no lenses."""
    REQUIRED = {"id", "type", "label", "description"}
    for n in graph["nodes"]:
        if n["type"] == "section":
            assert set(n.keys()) == REQUIRED, (
                f"Section {n['id']!r} fields = {set(n.keys())}, "
                f"expected exactly {REQUIRED}"
            )
            assert isinstance(n["label"], str) and n["label"], (
                f"empty label on {n['id']}"
            )
            assert isinstance(n["description"], str) and n["description"], (
                f"empty description on {n['id']}"
            )


def test_contains_edges_count_equals_substantive_page_count(graph):
    """Exactly 73 contains-edges — one per substantive page."""
    contains_edges = [e for e in graph["links"] if e["kind"] == "contains"]
    assert len(contains_edges) == 73, (
        f"Expected 73 contains-edges, got {len(contains_edges)}"
    )


def test_contains_edges_source_is_section_target_is_page(graph):
    """Every contains-edge: source is a section, target is a page. Never reversed."""
    section_ids = {n["id"] for n in graph["nodes"] if n["type"] == "section"}
    page_ids = {n["id"] for n in graph["nodes"] if n["type"] == "page"}
    for e in graph["links"]:
        if e["kind"] == "contains":
            assert e["source"] in section_ids, (
                f"contains-edge source {e['source']!r} is not a section"
            )
            assert e["target"] in page_ids, (
                f"contains-edge target {e['target']!r} is not a page"
            )
            # Page must belong to the section by ID prefix (regression guard).
            assert e["target"].startswith(e["source"] + "/"), (
                f"page {e['target']!r} does not belong to section {e['source']!r}"
            )


def test_existing_page_node_shape_unchanged(graph):
    """Regression guard: page nodes keep their pre-T4.1 field set.

    EPIC-3 published index.json with a specific page-node field set. Adding
    section nodes must not add or remove fields on page nodes."""
    EXPECTED_PAGE_FIELDS = {
        "id", "label", "section", "type", "url", "description", "lenses",
    }
    page_nodes = [n for n in graph["nodes"] if n["type"] == "page"]
    assert len(page_nodes) == 73, (
        f"page count drift: expected 73, got {len(page_nodes)}"
    )
    for n in page_nodes:
        assert set(n.keys()) == EXPECTED_PAGE_FIELDS, (
            f"page {n['id']!r} fields = {set(n.keys())}, "
            f"expected exactly {EXPECTED_PAGE_FIELDS}"
        )
