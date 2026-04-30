#!/usr/bin/env python3
"""T2.1 — chunk every substantive README into the corpus consumed by
embedding/HNSW build.

Output: dist/knowledge-graph/agent/v1/chunks.json  (byte-deterministic)

Chunk types (per docs/v1.1/spec.md):
    caption     — first substantive paragraph (one per page, singleton)
    principle   — each numbered principle under "## ... principles" (indexed)
    pitfalls    — "## ... pitfalls" section (singleton, optional)
    checklist   — "## ... checklist" section (singleton, optional)
    references  — "## References" section (singleton, optional)

Chunk id:
    "{page_id}:{chunk_type}"            for singletons
    "{page_id}:{chunk_type}:{index}"    for indexed (principle)
"""

import importlib.util
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
CONTENT_DIR = REPO_ROOT / "content"
OUTPUT_PATH = REPO_ROOT / "dist" / "knowledge-graph" / "agent" / "v1" / "chunks.json"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


seed = _load("seed_content", TOOLS_DIR / "seed_content.py")
gen = _load("generate", TOOLS_DIR / "generate.py")


# Reference keys sorted longest-first so substring matching is stable across
# overlapping labels (e.g. "AWS Well-Architected" before "AWS").
_REFERENCE_KEYS = sorted(
    set(gen.GOLD_REFERENCES.keys()) | set(gen.TAG_LINKS.keys()),
    key=lambda k: (-len(k), k),
)


def _find_h1_index(lines):
    for i, ln in enumerate(lines):
        if ln.startswith("# ") and not ln.startswith("## "):
            return i
    return None


def _extract_caption(text):
    """First substantive paragraph between H1 and the metadata block.

    Skips blank lines, **Section:** / **Alignment:** metadata, and the
    horizontal rule. Stops at the first H2 or the metadata line, whichever
    comes first."""
    lines = text.splitlines()
    h1 = _find_h1_index(lines)
    if h1 is None:
        return ""
    paragraph = []
    for ln in lines[h1 + 1:]:
        s = ln.strip()
        if not s:
            if paragraph:
                break
            continue
        if s.startswith("##"):
            break
        if (
            s.startswith("**Section:**")
            or s.startswith("**Subsection:**")
            or s.startswith("**Alignment:**")
            or s.startswith("---")
        ):
            if paragraph:
                break
            continue
        paragraph.append(s)
    return " ".join(paragraph).strip()


def _split_h2_sections(text):
    """Yield (heading, body) for each top-level ## section, in document order."""
    heading = None
    buf = []
    for line in text.splitlines():
        if line.startswith("## ") and not line.startswith("### "):
            if heading is not None:
                yield heading, "\n".join(buf).strip()
            heading = line[3:].strip()
            buf = []
        else:
            if heading is not None:
                buf.append(line)
    if heading is not None:
        yield heading, "\n".join(buf).strip()


def _split_principles(body):
    """Split a principles section body on '### ' subheadings."""
    chunks = []
    current = None
    for line in body.splitlines():
        if line.startswith("### "):
            if current is not None:
                chunks.append("\n".join(current).strip())
            current = [line]
        else:
            if current is not None:
                current.append(line)
    if current is not None:
        chunks.append("\n".join(current).strip())
    return [c for c in chunks if c]


def _detect_references(text):
    """Return sorted GOLD_REFERENCES keys whose label appears in the chunk text."""
    found = set()
    for key in _REFERENCE_KEYS:
        if key in text:
            found.add(key)
    return sorted(found)


_PRINCIPLES_RE = re.compile(r"principles?$", re.IGNORECASE)
_PITFALLS_RE = re.compile(r"pitfall", re.IGNORECASE)
_CHECKLIST_RE = re.compile(r"checklist", re.IGNORECASE)
_REFERENCES_RE = re.compile(r"^references$", re.IGNORECASE)


def _classify_h2(heading):
    """Map an H2 heading to one of {principle, pitfalls, checklist,
    references} or None for unhandled sections."""
    h = heading.strip().rstrip(":")
    if _REFERENCES_RE.search(h):
        return "references"
    if _PITFALLS_RE.search(h):
        return "pitfalls"
    if _CHECKLIST_RE.search(h):
        return "checklist"
    if _PRINCIPLES_RE.search(h):
        return "principle"
    return None


def _make_chunk(page_id, chunk_type, chunk_index, text, is_indexed):
    if is_indexed:
        cid = f"{page_id}:{chunk_type}:{chunk_index}"
    else:
        cid = f"{page_id}:{chunk_type}"
    return {
        "id": cid,
        "page_id": page_id,
        "chunk_type": chunk_type,
        "chunk_index": chunk_index,
        "text": text,
        "text_length": len(text),
        "references": _detect_references(text),
    }


def chunk_page(page_id, text):
    """Produce all chunks for a single page README. Returns list of chunk dicts.

    Singleton chunk types (pitfalls/checklist/references) collapse multiple
    matching H2 sections on the same page into one chunk so chunk ids stay
    unique. Principles flatten across any number of matching H2 sections into
    a single contiguously-indexed sequence."""
    chunks = []

    caption_text = _extract_caption(text)
    if caption_text:
        chunks.append(_make_chunk(page_id, "caption", 0, caption_text, False))

    principles = []
    singleton_parts = {"pitfalls": [], "checklist": [], "references": []}

    for heading, body in _split_h2_sections(text):
        if not body:
            continue
        kind = _classify_h2(heading)
        if kind is None:
            continue
        if kind == "principle":
            principles.extend(_split_principles(body))
        else:
            singleton_parts[kind].append(f"## {heading}\n\n{body}")

    for idx, principle_text in enumerate(principles):
        chunks.append(
            _make_chunk(page_id, "principle", idx, principle_text, True)
        )

    for kind in ("pitfalls", "checklist", "references"):
        parts = singleton_parts[kind]
        if parts:
            chunks.append(
                _make_chunk(page_id, kind, 0, "\n\n".join(parts), False)
            )

    return chunks


def build():
    metadata = gen.collect_site_metadata(CONTENT_DIR)
    all_chunks = []
    page_count = 0
    for page_id in sorted(metadata):
        m = metadata[page_id]
        if not m["is_substantive"]:
            continue
        readme = CONTENT_DIR / m["section"] / m["subsection"] / "README.md"
        text = readme.read_text(encoding="utf-8")
        page_chunks = chunk_page(page_id, text)
        if page_chunks:
            page_count += 1
            all_chunks.extend(page_chunks)

    all_chunks.sort(key=lambda c: c["id"])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"schema_version": "1.0", "chunks": all_chunks}
    OUTPUT_PATH.write_text(
        json.dumps(payload, sort_keys=True, indent=2),
        encoding="utf-8",
    )
    print(
        f"── Chunked: {len(all_chunks)} chunks across {page_count} pages "
        f"→ {OUTPUT_PATH.relative_to(REPO_ROOT)}"
    )


if __name__ == "__main__":
    build()
