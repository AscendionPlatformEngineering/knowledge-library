import hashlib
import re
import subprocess
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
DIST_DIR = REPO_ROOT / "dist"
LLMS_TXT_PATH = DIST_DIR / "llms.txt"
BUILDER = TOOLS_DIR / "build_llms_txt.py"

EXPECTED_AGENT_FILES = [
    "index.json",
    "schema.json",
    "chunks.json",
    "vectors.bin",
    "index.bin",
    "gold_references.json",
]

EXPECTED_ANCHOR_PAGE_IDS = [
    "principles/foundational",
    "principles/cloud-native",
    "system-design/event-driven",
    "nfr/maintainability",
    "compliance/pci-dss",
    "security/authentication-authorization",
    "governance/review-templates",
    "ai-native/monitoring",
    "observability/traces",
    "playbooks/migration",
]


def _run_builder():
    subprocess.run(
        ["python3", str(BUILDER)],
        check=True,
        cwd=REPO_ROOT,
        capture_output=True,
    )


def _rebuild_clean():
    if LLMS_TXT_PATH.exists():
        LLMS_TXT_PATH.unlink()
    _run_builder()


@pytest.fixture(scope="session")
def built():
    _run_builder()
    return True


@pytest.fixture(scope="session")
def content(built):
    return LLMS_TXT_PATH.read_text(encoding="utf-8")


# ─────────────────────────── Tests ──────────────────────────────


def test_file_exists(built):
    assert LLMS_TXT_PATH.exists(), f"{LLMS_TXT_PATH} not produced by builder"
    # Must be at site root (dist/llms.txt), not under knowledge-graph/
    assert LLMS_TXT_PATH.parent == DIST_DIR, (
        f"llms.txt must live at site root ({DIST_DIR}), not nested elsewhere"
    )
    assert "knowledge-graph" not in LLMS_TXT_PATH.parts, (
        "llms.txt must not live under /knowledge-graph/"
    )


def test_starts_with_h1_title(content):
    assert content.startswith("# Ascendion Engineering Knowledge Library"), (
        "llms.txt must open with the H1 title line"
    )


def test_has_blockquote_description(content):
    head = content.splitlines()[:10]
    blockquote_lines = [line for line in head if line.startswith("> ")]
    assert blockquote_lines, "expected at least one blockquote line in first 10 lines"

    head_blob = "\n".join(head)
    counts = ["73", "547", "332"]
    assert any(c in head_blob for c in counts), (
        f"blockquote must mention at least one of the corpus counts {counts}"
    )


def _section_text(content: str, heading_prefix: str) -> str:
    """Return the text of the first section whose heading line starts with heading_prefix."""
    lines = content.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith(heading_prefix):
            start = i
            break
    assert start is not None, f"section starting with {heading_prefix!r} not found"
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end])


def test_has_agent_endpoint_section(content):
    assert "## Agent Endpoint" in content, "missing '## Agent Endpoint' section"
    section = _section_text(content, "## Agent Endpoint")
    for fname in EXPECTED_AGENT_FILES:
        assert fname in section, (
            f"agent file {fname!r} not referenced in Agent Endpoint section"
        )


def test_agent_endpoint_uses_absolute_urls(content):
    section = _section_text(content, "## Agent Endpoint")
    urls = re.findall(r"https?://\S+", section)
    assert urls, "Agent Endpoint section must contain URLs"
    for url in urls:
        # strip trailing markdown punctuation
        url = url.rstrip(").,;>")
        assert url.startswith("https://ascendion.engineering/"), (
            f"non-absolute or off-domain URL in Agent Endpoint: {url!r}"
        )


def test_has_anchor_pages_section(content):
    # Allow heading suffix like "(Human-Rendered)"
    assert re.search(r"^## Anchor Pages\b", content, re.MULTILINE), (
        "missing '## Anchor Pages' section heading"
    )
    section = _section_text(content, "## Anchor Pages")
    urls = re.findall(r"https?://\S+", section)
    blob = " ".join(urls)
    for page_id in EXPECTED_ANCHOR_PAGE_IDS:
        assert page_id in blob, (
            f"anchor page {page_id!r} not present in Anchor Pages section URLs"
        )


def test_anchor_pages_use_absolute_urls(content):
    section = _section_text(content, "## Anchor Pages")
    urls = re.findall(r"https?://\S+", section)
    assert urls, "Anchor Pages section must contain URLs"
    for url in urls:
        url = url.rstrip(").,;>")
        assert url.startswith("https://ascendion.engineering/"), (
            f"non-absolute or off-domain anchor URL: {url!r}"
        )
        assert url.endswith("/"), (
            f"anchor page URL must end with trailing slash: {url!r}"
        )


def test_has_license_section(content):
    assert re.search(r"^## License\b", content, re.MULTILINE), (
        "missing '## License' section heading"
    )


def test_has_trailing_newline(content):
    assert content.endswith("\n"), "llms.txt must end with a trailing newline"


def test_byte_deterministic_llms_txt():
    _rebuild_clean()
    first = hashlib.sha256(LLMS_TXT_PATH.read_bytes()).hexdigest()
    _rebuild_clean()
    second = hashlib.sha256(LLMS_TXT_PATH.read_bytes()).hexdigest()
    assert first == second, (
        f"llms.txt not byte-deterministic across rebuilds: {first} vs {second}"
    )
