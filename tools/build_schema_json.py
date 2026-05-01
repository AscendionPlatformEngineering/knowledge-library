#!/usr/bin/env python3
"""T3.2 — agent endpoint JSON Schema builder.

Output: dist/knowledge-graph/agent/v1/schema.json (byte-deterministic)

JSON Schema 2020-12 contract describing the shape of index.json.
Schema is a literal Python dict — no data computation, no graph reading.
"""

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = REPO_ROOT / "dist" / "knowledge-graph" / "agent" / "v1" / "schema.json"


def build_schema():
    return {
        "$id": "https://ascendion.engineering/knowledge-graph/agent/v1/schema.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Ascendion Knowledge Library v1.1 — Agent Endpoint Index Schema",
        "description": "Structural graph contract for the v1.1 agent endpoint.",
        "type": "object",
        "additionalProperties": False,
        "required": ["schema_version", "nodes", "edges", "lenses"],
        "properties": {
            "schema_version": {"const": "1.0"},
            "nodes": {
                "type": "array",
                "items": {"$ref": "#/$defs/node"},
            },
            "edges": {
                "type": "array",
                "items": {"$ref": "#/$defs/edge"},
            },
            "lenses": {
                "type": "array",
                "items": {"$ref": "#/$defs/lens"},
            },
        },
        "$defs": {
            "node": {
                "oneOf": [
                    {"$ref": "#/$defs/page_node"},
                    {"$ref": "#/$defs/standard_node"},
                ],
            },
            "page_node": {
                "type": "object",
                "additionalProperties": False,
                "required": ["id", "label", "section", "type", "url", "description", "lenses"],
                "properties": {
                    "id":          {"type": "string", "minLength": 1},
                    "label":       {"type": "string", "minLength": 1},
                    "section":     {"type": "string", "minLength": 1},
                    "type":        {"const": "page"},
                    "url":         {"type": "string", "minLength": 1},
                    "description": {"type": "string"},
                    "lenses":      {"type": "array", "items": {"type": "string"}},
                },
            },
            "standard_node": {
                "type": "object",
                "additionalProperties": False,
                "required": ["id", "label", "type", "url", "description"],
                "properties": {
                    "id":          {"type": "string", "minLength": 1},
                    "label":       {"type": "string", "minLength": 1},
                    "type":        {"const": "standard"},
                    "url":         {"type": "string"},
                    "description": {"type": "string"},
                },
            },
            "edge": {
                "type": "object",
                "additionalProperties": False,
                "required": ["source", "target", "kind"],
                "properties": {
                    "source": {"type": "string", "minLength": 1},
                    "target": {"type": "string", "minLength": 1},
                    "kind":   {"enum": ["alignment", "related"]},
                },
            },
            "lens": {
                "type": "object",
                "additionalProperties": False,
                "required": ["id", "label", "description", "members", "caption_source"],
                "properties": {
                    "id":             {"type": "string", "minLength": 1},
                    "label":          {"type": "string", "minLength": 1},
                    "description":    {"type": "string"},
                    "members":        {"type": "array", "items": {"type": "string"}},
                    "caption_source": {"type": "string", "minLength": 1},
                },
            },
        },
    }


def main():
    schema = build_schema()

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(schema, f, sort_keys=True, indent=2)
        f.write("\n")

    print(
        f"schema.json: JSON Schema 2020-12, additionalProperties strict -> "
        f"{OUT_PATH.relative_to(REPO_ROOT)}"
    )


if __name__ == "__main__":
    main()
