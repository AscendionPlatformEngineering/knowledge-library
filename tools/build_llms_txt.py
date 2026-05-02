#!/usr/bin/env python3
"""T3.4 — llms.txt discovery manifest builder.

Output: dist/llms.txt (byte-deterministic)

Plain-markdown manifest at the site root for AI-agent discovery.
Reads live counts from the agent endpoint artifacts; anchor-page and
agent-file lists are constants.
"""

import json
import sys
from pathlib import Path


SITE_BASE_URL = "https://ascendion.engineering"
AGENT_PATH = "/knowledge-graph/agent/v1"

ANCHOR_PAGES = [
    ("principles/foundational", "Foundational Principles", "Core architectural principles for production systems."),
    ("principles/cloud-native", "Cloud-Native Principles", "Twelve-Factor and beyond: principles for cloud-resident services."),
    ("system-design/event-driven", "Event-Driven Systems", "When event-driven architecture is the right call, and when it is overengineering."),
    ("nfr/maintainability", "Maintainability NFRs", "Decomposing maintainability into measurable sub-characteristics; anchor of the debt-ledger lens."),
    ("compliance/pci-dss", "PCI DSS", "Architectural patterns for reducing cardholder-data-environment scope."),
    ("security/authentication-authorization", "Authentication and Authorization", "Distinguishing identity (authn) from access (authz); failure modes when conflated."),
    ("governance/review-templates", "Review Templates", "When to use ADRs vs RFCs vs inline comments — choosing the right governance artifact."),
    ("ai-native/monitoring", "AI Monitoring and Observability", "Production observability for ML systems beyond classical SRE metrics."),
    ("observability/traces", "Distributed Tracing", "Tracing patterns and common pitfalls in production deployments."),
    ("playbooks/migration", "Migration Playbook", "Operational guidance for system migrations and modernization."),
]

AGENT_FILES = [
    ("index.json", "Graph Structure", "JSON with page nodes, standard nodes, edges, and lens definitions. Schema-validated. ~144 KB."),
    ("schema.json", "JSON Schema", "JSON Schema 2020-12 contract for index.json. Strict (additionalProperties: false). ~3.5 KB."),
    ("chunks.json", "Chunks", "Semantic chunks across all substantive pages. Chunk types: caption, principle, pitfalls, checklist, references. ~1.7 MB."),
    ("vectors.bin", "Embedding Vectors", "BAAI/bge-small-en-v1.5 384-dim L2-normalized embeddings; 8-byte header followed by flat float32 grid. ~1.1 MB."),
    ("index.bin", "HNSW Index", "Cosine-similarity HNSW index over the vectors (M=16, ef_construction=200, seed=42). ~1.2 MB."),
    ("gold_references.json", "Gold References", "External citations with license, organization, and verification metadata. ~115 KB."),
]


def main():
    repo_root = Path(__file__).resolve().parent.parent
    index_path = repo_root / "dist" / "knowledge-graph" / "agent" / "v1" / "index.json"
    gold_refs_path = repo_root / "dist" / "knowledge-graph" / "agent" / "v1" / "gold_references.json"
    out_path = repo_root / "dist" / "llms.txt"

    missing = [p for p in (index_path, gold_refs_path) if not p.exists()]
    if missing:
        for p in missing:
            print(f"error: required artifact missing: {p.relative_to(repo_root)}", file=sys.stderr)
        print(
            "run tools/build_index_json.py and tools/build_gold_references_json.py first",
            file=sys.stderr,
        )
        sys.exit(1)

    index = json.loads(index_path.read_text(encoding="utf-8"))
    page_count = sum(1 for n in index["nodes"] if n["type"] == "page")
    edge_count = len(index["edges"])
    lens_count = len(index["lenses"])

    refs = json.loads(gold_refs_path.read_text(encoding="utf-8"))
    ref_count = len(refs["references"])

    lens_word = "lens" if lens_count == 1 else "lenses"

    lines = []
    lines.append("# Ascendion Engineering Knowledge Library")
    lines.append("")
    lines.append(
        f"> Production engineering knowledge graph for the Ascendion Platform "
        f"Engineering practice. {page_count} substantive pages, {edge_count} edges "
        f"between concepts, {ref_count} gold-tier external references, and "
        f"{lens_count} cross-cutting {lens_word}. Designed for both human readers "
        f"(rendered HTML) and AI agents (structured JSON plus binary vector embeddings)."
    )
    lines.append("")
    lines.append("## Agent Endpoint")
    lines.append("")
    lines.append(f"Machine-readable artifacts under `{AGENT_PATH}/`:")
    lines.append("")
    for filename, title, description in AGENT_FILES:
        url = f"{SITE_BASE_URL}{AGENT_PATH}/{filename}"
        lines.append(f"- [{title}]({url}): {description}")
    lines.append("")
    lines.append("## Anchor Pages (Human-Rendered)")
    lines.append("")
    lines.append("Curated entry points for navigating the library:")
    lines.append("")
    for page_id, label, description in ANCHOR_PAGES:
        url = f"{SITE_BASE_URL}/{page_id}/"
        lines.append(f"- [{label}]({url}) — {description}")
    lines.append("")
    lines.append("## License & Provenance")
    lines.append("")
    lines.append(
        "Content authored by the Ascendion Platform Engineering practice circle. "
        "The library is continuously deployed from the `feature/knowledge-graph-v1.1` "
        "integration branch."
    )
    lines.append("")
    lines.append(
        "The knowledge graph schema and corpus are versioned. "
        "Current schema_version: `1.0`."
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(
        f"llms.txt: {len(lines)} lines, {out_path.stat().st_size} bytes -> "
        f"{out_path.relative_to(repo_root)}"
    )


if __name__ == "__main__":
    main()
