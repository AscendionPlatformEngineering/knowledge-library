#!/usr/bin/env python3
"""T3.1 — agent endpoint structural graph builder.

Output: dist/knowledge-graph/agent/v1/index.json (byte-deterministic)

Minimal-bulk contract: nodes + edges + lens definitions, no chunk text,
no embeddings. Consumed by the agent endpoint as the structural map of
the knowledge graph.
"""

import importlib.util
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
CONTENT_DIR = REPO_ROOT / "content"
OUT_PATH = REPO_ROOT / "dist" / "knowledge-graph" / "agent" / "v1" / "index.json"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    seed = _load("seed_content", TOOLS_DIR / "seed_content.py")
    generate = _load("generate", TOOLS_DIR / "generate.py")

    metadata = generate.collect_site_metadata(CONTENT_DIR)
    graph = generate.compute_graph_data(metadata)

    lenses_out = []
    for lens_id in sorted(seed.CONCEPT_LENSES.keys()):
        lens = seed.CONCEPT_LENSES[lens_id]
        lenses_out.append({
            "id": lens_id,
            "label": lens["label"],
            "description": lens["description"],
            "members": sorted(lens["members"]),
            "caption_source": lens["caption_source"],
        })

    output = {
        "schema_version": "1.0",
        "nodes": graph["nodes"],
        "edges": graph["links"],
        "lenses": lenses_out,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(output, f, sort_keys=True, indent=2)
        f.write("\n")

    print(
        f"index.json: {len(output['nodes'])} nodes, "
        f"{len(output['edges'])} edges, "
        f"{len(output['lenses'])} lenses -> "
        f"{OUT_PATH.relative_to(REPO_ROOT)}"
    )


if __name__ == "__main__":
    main()
