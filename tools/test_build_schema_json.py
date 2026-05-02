import copy
import hashlib
import json
import subprocess
from pathlib import Path

import jsonschema
import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
AGENT_DIR = REPO_ROOT / "dist" / "knowledge-graph" / "agent" / "v1"
INDEX_PATH = AGENT_DIR / "index.json"
SCHEMA_PATH = AGENT_DIR / "schema.json"
INDEX_BUILDER = TOOLS_DIR / "build_index_json.py"
SCHEMA_BUILDER = TOOLS_DIR / "build_schema_json.py"


def _run_builder(builder_path):
    subprocess.run(
        ["python3", str(builder_path)],
        check=True,
        cwd=REPO_ROOT,
        capture_output=True,
    )


def _rebuild_clean():
    """Delete schema.json and rebuild — used by determinism test."""
    if SCHEMA_PATH.exists():
        SCHEMA_PATH.unlink()
    _run_builder(SCHEMA_BUILDER)


@pytest.fixture(scope="session")
def built():
    """Run both builders so index.json AND schema.json exist."""
    _run_builder(INDEX_BUILDER)
    _run_builder(SCHEMA_BUILDER)
    return True


@pytest.fixture(scope="session")
def schema(built):
    return json.loads(SCHEMA_PATH.read_text())


@pytest.fixture(scope="session")
def index(built):
    return json.loads(INDEX_PATH.read_text())


# ─────────────────────────── Tests ──────────────────────────────


def test_schema_file_exists(built):
    assert SCHEMA_PATH.exists(), f"{SCHEMA_PATH} not produced by build_schema_json.py"


def test_schema_is_valid_json_schema_2020_12(schema):
    jsonschema.Draft202012Validator.check_schema(schema)


def test_schema_has_required_metadata(schema):
    assert schema["$id"] == "https://ascendion.engineering/knowledge-graph/agent/v1/schema.json"
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"


def test_current_index_json_validates(schema, index):
    jsonschema.validate(instance=index, schema=schema)


def test_index_missing_schema_version_is_rejected(schema, index):
    bad = copy.deepcopy(index)
    del bad["schema_version"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=bad, schema=schema)


def test_page_node_with_extra_field_is_rejected(schema, index):
    bad = copy.deepcopy(index)
    first_page = next(n for n in bad["nodes"] if n["type"] == "page")
    first_page["rogue_field"] = "x"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=bad, schema=schema)


def test_edge_with_invalid_kind_is_rejected(schema, index):
    bad = copy.deepcopy(index)
    bad["edges"][0]["kind"] = "bogus"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=bad, schema=schema)


def test_schema_accepts_section_node(schema):
    """Schema validates a minimal section node."""
    valid_doc = {
        "schema_version": "1.0",
        "nodes": [
            {
                "id": "compliance",
                "type": "section",
                "label": "Compliance & Regulatory Frameworks",
                "description": "Mapping regulatory requirements to architecture...",
            }
        ],
        "edges": [],
        "lenses": [],
    }
    jsonschema.validate(instance=valid_doc, schema=schema)


def test_schema_accepts_contains_edge(schema):
    """Schema validates an edge with kind 'contains'."""
    valid_doc = {
        "schema_version": "1.0",
        "nodes": [
            {
                "id": "compliance",
                "type": "section",
                "label": "Compliance",
                "description": "x",
            },
            {
                "id": "compliance/pci-dss",
                "type": "page",
                "label": "PCI DSS",
                "section": "compliance",
                "url": "/compliance/pci-dss/",
                "description": "x",
                "lenses": [],
            },
        ],
        "edges": [
            {
                "source": "compliance",
                "target": "compliance/pci-dss",
                "kind": "contains",
            }
        ],
        "lenses": [],
    }
    jsonschema.validate(instance=valid_doc, schema=schema)


def test_byte_deterministic_schema_json():
    _rebuild_clean()
    first = hashlib.sha256(SCHEMA_PATH.read_bytes()).hexdigest()
    _rebuild_clean()
    second = hashlib.sha256(SCHEMA_PATH.read_bytes()).hexdigest()
    assert first == second, "schema.json bytes differ across rebuilds"
