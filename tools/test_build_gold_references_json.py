"""T3.3 tests — gold_references.json output of tools/build_gold_references_json.py.

Run from repo root:
    python3 -m pytest tools/test_build_gold_references_json.py -v

Drives EPIC-3 T3.3. Until tools/build_gold_references_json.py exists, every
test is expected to fail at fixture setup (subprocess.CalledProcessError) —
that failure is the spec for the implementation.

Output contract (locked):
    - Path: dist/knowledge-graph/agent/v1/gold_references.json
    - Top-level keys: schema_version, references
    - schema_version == "1.0"
    - 332 reference objects, sorted by id (alphabetical)
    - Each reference has exactly 9 string fields:
        id, label, url, organization, license, last_verified,
        summary, summary_author, summary_date
    - sort_keys=True, indent=2, trailing newline, byte-deterministic
"""
import copy
import hashlib
import json
import subprocess
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
AGENT_DIR = REPO_ROOT / "dist" / "knowledge-graph" / "agent" / "v1"
OUTPUT_PATH = AGENT_DIR / "gold_references.json"
BUILDER = TOOLS_DIR / "build_gold_references_json.py"


REQUIRED_FIELDS = {
    "id",
    "label",
    "url",
    "organization",
    "license",
    "last_verified",
    "summary",
    "summary_author",
    "summary_date",
}


def _run_builder():
    subprocess.run(
        ["python3", str(BUILDER)],
        check=True,
        cwd=REPO_ROOT,
        capture_output=True,
    )


def _rebuild_clean():
    if OUTPUT_PATH.exists():
        OUTPUT_PATH.unlink()
    _run_builder()


@pytest.fixture(scope="session")
def built():
    _run_builder()
    return True


@pytest.fixture(scope="session")
def output(built):
    return json.loads(OUTPUT_PATH.read_text())


# ─────────────────────────── Tests ──────────────────────────────


def test_file_exists(built):
    assert OUTPUT_PATH.exists(), f"{OUTPUT_PATH} not produced by builder"


def test_schema_version(output):
    assert output["schema_version"] == "1.0"


def test_top_level_keys(output):
    assert set(output.keys()) == {"schema_version", "references"}


def test_reference_count(output):
    assert len(output["references"]) == 332


def test_every_reference_has_required_fields(output):
    for ref in output["references"]:
        assert set(ref.keys()) == REQUIRED_FIELDS, (
            f"reference {ref.get('id')!r} has fields {set(ref.keys())}, "
            f"expected {REQUIRED_FIELDS}"
        )


def test_all_field_values_are_strings(output):
    for ref in output["references"]:
        for field, value in ref.items():
            assert isinstance(value, str), (
                f"reference {ref.get('id')!r} field {field!r} is "
                f"{type(value).__name__}, expected str"
            )


def test_references_sorted_by_id(output):
    ids = [ref["id"] for ref in output["references"]]
    assert ids == sorted(ids), "references must be sorted alphabetically by id"


def test_byte_deterministic_gold_references_json():
    _rebuild_clean()
    first = hashlib.sha256(OUTPUT_PATH.read_bytes()).hexdigest()
    _rebuild_clean()
    second = hashlib.sha256(OUTPUT_PATH.read_bytes()).hexdigest()
    assert first == second, "gold_references.json bytes differ across rebuilds"
