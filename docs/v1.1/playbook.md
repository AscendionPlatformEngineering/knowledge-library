# Knowledge Graph v1.1 — Implementation Playbook

**Companion to:** `knowledge-graph-v1.1.md` (architectural specification)
**Status:** All six open questions signed off — implementation green-lit
**Author:** Drafted for Jeril John Panicker, Platform Engineering, Ascendion
**Target:** v42 of `ascendion.engineering` codebase → v43+ feature ships

---

## 1 — Sign-off summary (locked)

| # | Decision | Implication |
|---|---|---|
| 1 | Embedding model: **`bge-small-en-v1.5`** (384-dim, ~33 MB quantized) | First-load tax 11 MB higher than MiniLM but better quality on technical text. Service Worker caches it forever after first visit. |
| 2 | Chunking: **caption + 6 principles + pitfalls + checklist + references** (10/page) | References chunks indexed despite brevity — they encode "this page cites this standard," useful retrieval signal. Total ~810 chunks at v1.1 scale. |
| 3 | Section-index pages: **third node type** (`section`) — between page and standard in visual weight | Adds ~18 nodes; resolves the v42 "73 vs 172" discrepancy by making library structure visible. |
| 4 | Gold-reference summaries: **`summary_author = "Platform Engineering"`** | Team-owned, not personal. Field tracks ownership for review cycles. |
| 5 | Adjacent suggestions: **top-3, cosine > 0.55** | Below threshold, suppress. Numbers tunable after first build. |
| 6 | HNSW params: **M=16, ef_construction=200, ef_search=50** | Sensible defaults at this scale; revisit after performance characterization. |

---

## 2 — Tooling setup

### 2.1 Workstation prerequisites

Verify before starting any task:

```bash
python3 --version      # need 3.11+
node --version         # need 20+
git --version          # any modern
aws --version          # for S3/CloudFront access — already configured per Mediarmor profile

# Confirm existing dev paths
ls /home/claude/work/restoration/tools/generate.py   # main generator
ls /home/claude/work/restoration/tools/seed_content.py # taxonomy + lenses
```

### 2.2 Python build dependencies

Add to a new `tools/requirements-build.txt` (kept separate from generator's runtime):

```
sentence-transformers==2.7.0
hnswlib==0.8.0
numpy==1.26.4
jsonschema==4.21.1
```

Install once, locally:

```bash
pip install --break-system-packages -r tools/requirements-build.txt
```

CI installs the same file (see EPIC-2, T2.3).

### 2.3 Browser-side dependencies

Loaded from CDN with SRI hashes — no `npm install` on the frontend, matching v42's no-build posture:

| Library | CDN | Used by |
|---|---|---|
| D3 v7 | `cdn.jsdelivr.net/npm/d3@7` | Already loaded; reuse. |
| `@xenova/transformers` | `cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2` | EPIC-7 |
| `hnswlib-wasm` | `cdn.jsdelivr.net/npm/hnswlib-wasm@0.8.2` | EPIC-7 |

Get SRI hashes once:

```bash
# Run for each library, paste integrity attribute into the <script> tag in generate.py
curl -s https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2/dist/transformers.min.js | openssl dgst -sha384 -binary | openssl base64 -A
```

### 2.4 Claude tooling install

**Claude Code** (assumed already installed). Verify:

```bash
claude --version
```

**Ralph Loop** plugin:

```bash
claude plugin marketplace add anthropic-ralph-loop
claude plugin install ralph-loop@anthropic-ralph-loop
# Verify
claude /ralph-loop --help
```

**Caveman** plugin:

```bash
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
# Verify
claude /caveman lite     # try lite first to gauge fit
```

**Claude Design** is the web UI at `claude.ai/design` — no install required. Bookmark.

### 2.5 Repo bootstrapping

One-time setup on the existing repo:

```bash
cd /home/claude/work/restoration
git checkout -b feature/knowledge-graph-v1.1
git push -u origin feature/knowledge-graph-v1.1

# Create CLAUDE.md if not present (Claude Code session memory)
cat > CLAUDE.md <<'EOF'
# ascendion.engineering — Claude session memory

## Project
Static site generator producing the ascendion.engineering knowledge library.
v42 in production. v1.1 knowledge-graph upgrade in flight.

## Conventions
- 2-color palette: warm neutral #D6D2C8 + terracotta #C96330
- 18-section taxonomy in tools/seed_content.py; do not rename
- 73 substantive pages currently; gen handles stubs separately
- AUTHORING_CONVENTIONS embedded in generate.py docstring — substantive tone, no marketing voice
- Mermaid 10.x for diagrams; one diagram type per page

## Active work
See knowledge-graph-v1.1-implementation.md (this playbook).

## Critical files
- tools/generate.py — main generator (~250KB)
- tools/seed_content.py — TAXONOMY, CONCEPT_LENSES, GOLD_REFERENCES
- .github/workflows/deploy.yml — CI

## Sign-offs locked (v1.1)
1. Embedding model: bge-small-en-v1.5
2. Chunking: 10 chunks/page including references
3. Section-index pages: yes, third node type
4. Gold-reference author: "Platform Engineering"
5. Adjacent suggestions: top-3, cosine > 0.55
6. HNSW: M=16, ef_construction=200, ef_search=50
EOF

# Compress the CLAUDE.md for cheaper session starts (after a few sessions if it grows)
# claude /caveman:compress CLAUDE.md
# CLAUDE.original.md will be created as your editable backup

git add CLAUDE.md
git commit -m "chore(memory): bootstrap CLAUDE.md for v1.1 work"
```

---

## 3 — Tool routing — which tool for which task

The four tools have different sweet spots. Routing them properly avoids the trap of using the heaviest tool for every task.

| Tool | Best for | Avoid for |
|---|---|---|
| **Claude Code** (default) | Greenfield modules (`build_vector_index.py`), cross-file refactors (TAG_LINKS → GOLD_REFERENCES), test scaffolding, deep analysis & exploration. | Repetitive tasks that need many iterations until a test passes — those want Ralph Loop. |
| **Ralph Loop** | Tasks with a *binary verification step*: schema validates, regression tests pass, link verifier reports zero failures, JSON parses. The completion-promise pattern needs an automated check. | Design iteration, prose authoring, exploratory work. No way to write a verifying check for "the side panel feels right." |
| **Claude Design** | Side-panel layouts, lens dropdown styling, search results UI, mobile drawer animation. Anything with a visual artifact that benefits from rapid iteration on screens. | Backend logic, build scripts, schema authoring. Wrong instrument. |
| **Caveman** | Code generation sessions where you want terse output, commits (`/caveman-commit`), code reviews (`/caveman-review`). | Spec edits, architectural reasoning, anything where prose nuance carries signal. Caveman compresses *output*, not *thinking* — but in long analysis sessions, terser output sometimes loses justifications you'd want preserved. |

**Two specific recommendations:**

- **Ralph Loop completion-promise convention.** Every Ralph-Loop-driven task in this playbook has a `Ralph completion promise:` line. Use that exact string. If a task lacks one, do not run it under Ralph Loop — switch to plain Claude Code.
- **Caveman scope.** Run `/caveman lite` for code-generation epics (2, 3, 4, 7, 9, 10). Switch to normal mode for spec/design/review epics (1, 5, 6, 8). `lite` keeps grammar; `full` and `ultra` trade clarity for compression and aren't worth it on a multi-week project.

---

## 4 — EPIC overview

Ten epics, ordered by dependency. Each epic is independently shippable; the graph remains functional throughout.

```
                  EPIC-1 Foundations
                  (registry + lenses)
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
      EPIC-2 Build Pipeline   EPIC-4 Visual Hierarchy
      (chunks + vectors)      + Section Nodes
            │                       │
            ▼                       │
      EPIC-3 Agent Endpoint         │
            │                       │
            └───────────┬───────────┘
                        ▼
                  EPIC-5 Side Panel Workspace
                  (the click-doesn't-navigate change)
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
      EPIC-6 Concept Lens UI   EPIC-7 Semantic Search
            │                       │
            └───────────┬───────────┘
                        ▼
                  EPIC-8 Adjacent Suggestions
                        │
                        ▼
                  EPIC-9 Service Worker / Offline
                        │
                        ▼
                  EPIC-10 Mobile Layout & Polish
```

Effort sizing (rough): S = ½ day, M = 1–2 days, L = 3–5 days. Total v1.1 lands around 25–35 working days at one developer's pace.

---

## 5 — EPIC details

### EPIC-1 — Foundations

Refactor existing data shapes into the v1.1 schema before anything else changes. This is the load-bearing refactor — it touches files everything else depends on.

| Field | Value |
|---|---|
| Effort | M (1–2 days) |
| Tools | Claude Code (refactor + tests). Caveman normal mode — schema is too important to terse. |
| Depends on | Nothing |
| Unblocks | EPIC-2, EPIC-3, EPIC-4 |
| Branch | `feature/kg-v1.1/foundations` |

#### Task T1.1 — Refactor `TAG_LINKS` → `GOLD_REFERENCES`

Replace the flat dict at `tools/generate.py:3097` with the structured registry from spec §4.2.

**Subtasks:**
1. Define new `GOLD_REFERENCES` dict-of-dicts in `generate.py` with schema: `{id, label, url, organization, license, last_verified, summary, summary_author, summary_date}`.
2. Migrate all 332 existing `TAG_LINKS` entries — `summary_author = "Platform Engineering"`, `summary_date = build date`, `last_verified = build date`. Leave `summary` empty string for entries that don't have one yet (a follow-up task fills these in).
3. Update every reference site in `generate.py` — link verifier (line ~3540), alignment edge builder, knowledge-graph generator. Use Claude Code's "find all usages" then refactor systematically.
4. Add a deprecation shim: `TAG_LINKS = {k: v["url"] for k, v in GOLD_REFERENCES.items()}` so any unforeseen call site still works during transition. Remove the shim in EPIC-3 once the refactor is verified.

**Acceptance criteria:**
- [ ] `GOLD_REFERENCES` exists with all 332 entries from former `TAG_LINKS`.
- [ ] Every entry has all 9 fields populated (empty `summary` allowed for v1.1, tracked separately).
- [ ] `python tools/generate.py` runs without `KeyError` and produces byte-identical `dist/` HTML for v42 content (regression check; run `diff -r dist_before/ dist_after/` and expect no differences in HTML pages).
- [ ] HTTPS link verifier still passes.
- [ ] No new pyflakes/ruff warnings introduced.

**Tool routing:** Claude Code with one careful prompt. Do not use Ralph Loop — refactor success isn't binary-verifiable until the regression-diff step.

#### Task T1.2 — Declare `CONCEPT_LENSES` in `seed_content.py`

Add a new top-level dict alongside `TAXONOMY` and `SHORT_DESC`.

**Subtasks:**
1. Add `CONCEPT_LENSES` dict per spec §5.3, with `debt-ledger` as first instance and the eight authored member page IDs.
2. Add a validator function: at module load, assert every `members` page ID resolves to a substantive page in `TAXONOMY`. Fail loudly if a page is renamed/removed without updating lenses.
3. Add caption-source resolution: read the canonical pull-quote sentence from `content/<caption_source>/README.md` at build time and inject into lens metadata.

**Acceptance criteria:**
- [ ] `CONCEPT_LENSES["debt-ledger"]["members"]` contains exactly: `["nfr/maintainability", "nfr/security", "nfr/reliability", "nfr/usability", "compliance/bsp-afasa", "compliance/gdpr", "compliance/iso27001", "compliance/pci-dss"]`.
- [ ] Validator raises `ValueError` if any member ID is not in `TAXONOMY`.
- [ ] `caption_source = "nfr/usability"` resolves to the cross-cutting sentence already authored on that page.
- [ ] Module-import side effects do not slow the generator's startup by more than 50 ms.

**Tool routing:** Claude Code, single session.

#### Task T1.3 — Annotate page nodes with lens membership

Modify `compute_graph_data()` at `generate.py:3835` to add `lenses: List[str]` to each page node.

**Subtasks:**
1. Build `lens_index = defaultdict(list)` once at function start: `lens_id` → `[page_ids]`.
2. In the page-node-creation loop, set `node["lenses"] = lens_index.get(reverse_lookup, [])`.
3. Add a unit test in a new `tools/test_compute_graph_data.py`: assert that the eight ledger pages each have `["debt-ledger"]` in their `lenses` field, and a non-ledger page has `[]`.

**Acceptance criteria:**
- [ ] All 8 debt-ledger pages have `lenses == ["debt-ledger"]` in graph output.
- [ ] All non-ledger substantive pages have `lenses == []`.
- [ ] Unit test passes: `python -m pytest tools/test_compute_graph_data.py`.
- [ ] Graph JSON byte size grows by less than 5 KB.

**Ralph completion promise:** `LENS-ANNOTATION-VERIFIED`
**Tool routing:** Ralph Loop is appropriate here — completion is binary (tests pass).

```
claude /ralph-loop "Implement T1.3: annotate page nodes with lens membership in compute_graph_data. Tests at tools/test_compute_graph_data.py must pass. Output 'LENS-ANNOTATION-VERIFIED' when green." --max-iterations 8 --completion-promise "LENS-ANNOTATION-VERIFIED"
```

---

### EPIC-2 — Build pipeline (chunks + vector index)

Generate the chunk corpus and HNSW index at build time. Pure backend work; no UI changes.

| Field | Value |
|---|---|
| Effort | L (3–5 days) |
| Tools | Claude Code (modules), Ralph Loop (vector index against unit test), Caveman lite |
| Depends on | EPIC-1 |
| Unblocks | EPIC-3, EPIC-7, EPIC-8 |
| Branch | `feature/kg-v1.1/build-pipeline` |

#### Task T2.1 — Implement `chunk_page()` and `build_chunk_corpus()`

Parse each substantive README into typed chunks per spec §4.2.

**Subtasks:**
1. Add `chunk_page(page_id, metadata, readme_text) -> List[Chunk]` to `generate.py`. Reuse existing parsers (`extract_title_desc`, etc.) — do not re-author markdown parsing.
2. Implement chunk-kind detection: regex on `### N.` for principles, `## ⚠️ Pitfalls` heading + bullets for pitfalls, `☐` glyph blocks for checklist, `## References` heading for references.
3. Each chunk's `text` field is plain-text-stripped (no markdown syntax in the embedding-input text).
4. Add `build_chunk_corpus(metadata) -> List[Chunk]` walking all substantive pages.
5. Stable chunk IDs: `<page_id>#<kind>` for singletons (`caption`, `pitfalls`, `checklist`, `references`); `<page_id>#principle_N` for the 6 principles.
6. Add unit test: assert chunk count for 5 representative pages matches expected (caption=1, principles=6, pitfalls=1, checklist=1, references=1 — total 10 each).

**Acceptance criteria:**
- [ ] `build_chunk_corpus` returns ~810 chunks at v42 scale (73 pages × ~10 chunks, allowing for pages with missing sections — log a warning if a substantive page yields fewer than 8 chunks).
- [ ] Each chunk has a unique `id`; duplicates raise.
- [ ] Each chunk's `text` is plain-text only (no markdown punctuation noise).
- [ ] Unit tests pass for the 5 representative pages.

**Tool routing:** Claude Code. The parser logic needs careful reading of authored pages; not a fit for Ralph Loop.

#### Task T2.2 — Build `tools/build_vector_index.py`

New CLI script. Run after `chunks.json` is generated.

**Subtasks:**
1. Read `chunks.json`, instantiate `SentenceTransformer("BAAI/bge-small-en-v1.5")`.
2. Encode all chunk texts with `normalize_embeddings=True` (cosine space).
3. Build HNSW index with `space="cosine", dim=384, M=16, ef_construction=200`. Add all embeddings.
4. Save with `index.save_index(out_path)`.
5. Also output `chunks_meta.json` (just `id` + `embedding_idx` mapping) — keep separate from the larger `chunks.json` to allow agents to fetch metadata without text.
6. Print build stats: chunk count, encoding time, index size, total elapsed.

**Acceptance criteria:**
- [ ] Script accepts `--chunks <path> --out <path>` arguments.
- [ ] Output `vector.bin` is < 2 MB at v1.1 scale.
- [ ] `python -c "import hnswlib; idx = hnswlib.Index(space='cosine', dim=384); idx.load_index('vector.bin'); print(idx.get_current_count())"` prints the chunk count and exits 0.
- [ ] Encoding completes in < 90s on a CI runner (M=16 with batch encoding is fast at this scale).
- [ ] Build is deterministic: running twice with the same chunks input produces byte-identical output (set torch seed and `model.eval()`).

**Ralph completion promise:** `VECTOR-INDEX-VERIFIED`
**Tool routing:** Ralph Loop fits — completion is binary (load round-trips).

#### Task T2.3 — CI integration

Add a build step in `.github/workflows/deploy.yml`.

**Subtasks:**
1. Add a step after `seed_content.py` runs and before S3 sync.
2. Cache pip installs and the BGE model weights (`actions/cache@v4` with key `bge-small-en-v1.5`) — saves ~80s per run after first.
3. Run `python tools/build_vector_index.py --chunks dist/knowledge-graph/agent/v1/chunks.json --out dist/knowledge-graph/agent/v1/vector.bin`.
4. Fail the build if `vector.bin` is missing or chunk count diverges from `chunks.json` length.

**Acceptance criteria:**
- [ ] CI run produces `dist/knowledge-graph/agent/v1/vector.bin` on every push.
- [ ] CI runtime increase < 2 minutes after cache warm-up.
- [ ] `vector.bin` is uploaded to S3 alongside other artifacts and content-hashed in URL.
- [ ] CI fails loudly with a clear message if encoding fails (do not silently produce empty index).

**Tool routing:** Claude Code.

#### Task T2.4 — Validation harness

A small script that proves the index does what we expect.

**Subtasks:**
1. New file `tools/validate_vector_index.py` that loads the index and runs 5 canonical queries (e.g., "audit findings consistent across regimes", "burn rate review", "encryption key rotation", "service level objective", "compensating control").
2. For each query, assert the top-3 results include at least one expected page ID (hand-picked). The expectation acts as a regression sentinel — if BGE drift or chunking regression breaks retrieval, this catches it.
3. Run as part of CI alongside the build step.

**Acceptance criteria:**
- [ ] All 5 canonical queries return expected pages in top-3.
- [ ] Script exits non-zero if any query fails.
- [ ] CI runs validation immediately after index build.

**Tool routing:** Claude Code (small, careful test authoring).

---

### EPIC-3 — Agent endpoint

Publish the machine-readable contract.

| Field | Value |
|---|---|
| Effort | M (1–2 days) |
| Tools | Claude Code (writers + schema), Ralph Loop (schema validates), Caveman lite |
| Depends on | EPIC-1, EPIC-2 |
| Unblocks | EPIC-7 (browser fetches via same endpoints) |
| Branch | `feature/kg-v1.1/agent-endpoint` |

#### Task T3.1 — Implement `gen_agent_endpoint()`

Write `index.json`, `gold_references.json`, `chunks.json` to `dist/knowledge-graph/agent/v1/`.

**Subtasks:**
1. Add `gen_agent_endpoint(graph_data, lenses, refs, chunks, out_root)` to `generate.py`.
2. `index.json` shape: `{schema_version, generated_at, node_count, edge_count, lenses, nodes, edges}` — no chunk text, no embeddings (those go in separate files).
3. `gold_references.json` shape: list of full GoldReference records.
4. `chunks.json` shape: list of Chunk records (with text, without embeddings).
5. All files written with `ensure_ascii=False, indent=2` for human readability; CI gzips at S3 upload.

**Acceptance criteria:**
- [ ] All three files produced under `dist/knowledge-graph/agent/v1/`.
- [ ] `index.json` total size < 250 KB; `chunks.json` < 800 KB; `gold_references.json` < 100 KB.
- [ ] `jq '.lenses[0].member_pages | length' dist/knowledge-graph/agent/v1/index.json` returns `8`.
- [ ] `jq '.nodes | map(select(.type == "page")) | length' index.json` returns 73.

**Tool routing:** Claude Code.

#### Task T3.2 — Author `schema.json`

JSON Schema document describing `index.json`. The contract.

**Subtasks:**
1. Author Draft 2020-12 schema covering all object shapes from spec §4.1–4.2.
2. Add semantic constraints: `type` enum, `kind` enum, `id` pattern (`^[a-z0-9-]+/[a-z0-9-]+$` for page IDs).
3. Validate `index.json` against `schema.json` in CI using `jsonschema` Python library.

**Acceptance criteria:**
- [ ] `python -m jsonschema -i dist/knowledge-graph/agent/v1/index.json dist/knowledge-graph/agent/v1/schema.json` exits 0.
- [ ] Schema rejects synthetic invalid index (e.g., a node with `type: "frog"`) with a clear error message.
- [ ] `schema.json` is < 15 KB.

**Ralph completion promise:** `SCHEMA-VALIDATES`
**Tool routing:** Ralph Loop fits.

#### Task T3.3 — Generate `dist/llms.txt`

Discovery file at site root.

**Subtasks:**
1. Add `gen_llms_txt(out_root)` writing the content from spec §8.2.
2. Include current production URL (`https://ascendion.engineering`).
3. Reference each agent endpoint and the schema.

**Acceptance criteria:**
- [ ] `dist/llms.txt` exists, < 2 KB, plain text.
- [ ] All four URLs in the file resolve (verified by HTTPS link verifier).

**Tool routing:** Claude Code (trivial).

#### Task T3.4 — Content-hashed URLs

Cache invalidation via filename, not query string.

**Subtasks:**
1. After all agent files are written, compute SHA-256 (first 8 hex chars) and rename to `index-<hash>.json`, `chunks-<hash>.json`, `gold_references-<hash>.json`, `vector-<hash>.bin`.
2. Write a small `dist/knowledge-graph/agent/v1/manifest.json` mapping logical names to hashed filenames.
3. Update `llms.txt` and the in-page JS loader (EPIC-7) to fetch `manifest.json` first, then resolve hashed URLs.
4. CloudFront is configured with `cache-control: public, max-age=31536000, immutable` for hashed assets — set this header in the existing S3 sync step.

**Acceptance criteria:**
- [ ] `manifest.json` exists with `{index, chunks, gold_references, vector}` keys mapping to hashed filenames.
- [ ] Two consecutive identical builds produce identical hashes (deterministic input → deterministic hash).
- [ ] Changing any chunk text causes corresponding hash to change.
- [ ] Old hashed files remain accessible at S3 for ~30 days (CloudFront serves stale-on-error during deploy windows).

**Tool routing:** Claude Code.

---

### EPIC-4 — Visual hierarchy + section nodes

Pure rendering work in `gen_knowledge_graph_page()`. The graph stops drowning the page network.

| Field | Value |
|---|---|
| Effort | S (½ day) — biggest perceptual win per LOC in the entire v1.1 |
| Tools | Claude Design (preview iteration), Claude Code (apply changes) |
| Depends on | EPIC-1 |
| Unblocks | EPIC-5 (panel design depends on stable graph visuals) |
| Branch | `feature/kg-v1.1/visual-hierarchy` |

#### Task T4.1 — Add `section` node type

Add 18 section-index pages as a third node kind.

**Subtasks:**
1. In `compute_graph_data`, after page nodes, iterate `TAXONOMY` and emit one `type: "section"` node per registered section. Position is computed from member-page centroid at build time (or left to D3 force at run time).
2. Add edges: `kind: "contains"` from each section node to each member page. New edge kind alongside `alignment` and `related`.
3. Document the `contains` kind in `schema.json` (EPIC-3 already published — bump `schema_version` to `1.1` if you reach this in the same release window, or leave for v1.2).

**Acceptance criteria:**
- [ ] Graph includes exactly 18 section nodes (one per `TAXONOMY` key).
- [ ] Each section node has `contains` edges to its substantive member pages only (stubs excluded).
- [ ] Total edge count grows by ~73 (one per substantive page).

**Tool routing:** Claude Code.

#### Task T4.2 — Demote standards to halo

Change CSS in `gen_knowledge_graph_page` to make standards visually quieter.

**Subtasks:**
1. Standard nodes: radius halved (rect 8×8 instead of 16×16), fill-opacity 0.4, label hidden until hover.
2. Standard nodes excluded from default search hits (this implements the front half of EPIC-7's filter, no harm).
3. Section nodes: medium weight — radius 11 (between page's 9 and standards' historical equivalent), fill `var(--ink-2)`, label always visible but smaller font.

**Acceptance criteria:**
- [ ] Visual diff against v42: page network is the visible backbone, standards form a halo.
- [ ] Hover on standard reveals label.
- [ ] Section nodes visible but not dominant.
- [ ] Mobile: standards remain accessible (no hover) — show labels at zoom > 1.5x.

**Tool routing:** Claude Design — iterate on the rendered preview, paste final CSS into `generate.py`. Faster than coding-blind in Claude Code.

#### Task T4.3 — Section node click behavior (preview)

When clicked, section node opens a panel listing its member pages. Stub for EPIC-5 — final polish lives there.

**Subtasks:**
1. Add stub click handler that logs the section ID to console.
2. Add a temporary `<title>` SVG attribute showing the section name on hover (until full panel arrives).

**Acceptance criteria:**
- [ ] Click event registers; console log shows section ID.
- [ ] Title hover works.

**Tool routing:** Claude Code.

---

### EPIC-5 — Side-panel workspace

The single most important behavior change in v1.1: clicking a node opens a panel; the page does not navigate.

| Field | Value |
|---|---|
| Effort | L (3–5 days) — main UX work of v1.1 |
| Tools | Claude Design (panel layouts + states), Claude Code (logic + integration) |
| Depends on | EPIC-1, EPIC-4 |
| Unblocks | EPIC-6, EPIC-7, EPIC-8 |
| Branch | `feature/kg-v1.1/side-panel` |

#### Task T5.1 — Panel shell and layout

The structural change to `gen_knowledge_graph_page`'s HTML output.

**Subtasks:**
1. Restructure main body: graph canvas takes ~70% width, panel takes ~30% (min 380 px, max 480 px on desktop).
2. Empty state: italic serif copy explaining the workspace model.
3. Panel scroll behavior: `overflow-y: auto`, fixed header within panel showing breadcrumb + close-X.
4. Mobile: panel becomes bottom drawer with handle to drag up (CSS `transform` + JS touch listener).

**Acceptance criteria:**
- [ ] Desktop layout: 2-column grid responds correctly down to 900 px.
- [ ] Mobile (≤ 900 px): drawer behavior, handle visible, drag-up works on touch devices.
- [ ] Empty state matches the copy spec from §7.7.
- [ ] No CLS (cumulative layout shift) when panel content swaps.

**Tool routing:** Claude Design — iterate panel states (empty, loading, page, standard, section, search results) as visual screens. Then port to generate.py.

#### Task T5.2 — Click-opens-panel wiring

Replace the v42 `window.location.href = ...` behavior with `selectNode(id)`.

**Subtasks:**
1. Add `selectNode(id)` JS function that dispatches to `renderPagePanel`, `renderStandardPanel`, or `renderSectionPanel` based on node `type`.
2. Visual feedback: clicked node gets `class="selected"` (ink-color border, slightly larger).
3. Panel scroll-to-top on every node change.
4. URL state: optionally update `window.location.hash` to `#node=<id>` so back/forward works (don't full-navigate; just hash). Listen to `hashchange` to support deep links.

**Acceptance criteria:**
- [ ] Clicking any node opens the corresponding panel; URL path stays at `/knowledge-graph/`.
- [ ] Browser back button works after multi-hop navigation within the graph.
- [ ] Deep link `…/knowledge-graph/#node=compliance/gdpr` opens with GDPR pre-selected.
- [ ] `Esc` key clears selection (returns to empty state).

**Tool routing:** Claude Code.

#### Task T5.3 — Page detail rendering

The full page panel: breadcrumb, title, description, lens badge, related, gold refs, "Open page →" CTA.

**Subtasks:**
1. Author `renderPagePanel(id)` JS function pulling data from `index.json` (already loaded at page init).
2. Lens badge: render only if page has lenses; one badge per lens.
3. Related list: existing `kind: "related"` edges, render as clickable items that call `selectNode(target_id)`.
4. Gold-references section: filter `gold_references.json` for refs whose `id` matches the page's alignment edges. Each ref shows label, organization, license, summary, verified date.
5. "Open page →" button: links to `/<page_id>/index.html` — this is the only navigation away.

**Acceptance criteria:**
- [ ] Panel renders correctly for all 73 substantive pages (smoke test: open each programmatically, no JS errors).
- [ ] Lens badge appears for the 8 ledger pages, absent for others.
- [ ] Related list items are clickable and navigate within the graph (no page reload).
- [ ] "Open page →" navigates to the canonical page URL.

**Tool routing:** Claude Design (visual iteration on info density), then Claude Code (data wiring).

#### Task T5.4 — Standard detail rendering

Smaller panel for diamond nodes.

**Subtasks:**
1. `renderStandardPanel(id)` reads from `gold_references.json`.
2. Show: organization, license, last_verified, summary, summary_author, "Open source ↗" external link.
3. Also show: "Pages aligning with this standard" — list of substantive pages with an alignment edge to this standard. Click → page panel.

**Acceptance criteria:**
- [ ] All 224 standards render correctly.
- [ ] External link opens in new tab with `noopener noreferrer`.
- [ ] Aligning-pages list is sorted alphabetically by section then page.

**Tool routing:** Claude Code.

#### Task T5.5 — Section detail rendering

The third node type's panel.

**Subtasks:**
1. `renderSectionPanel(id)` shows: section name, brief description (from `SHORT_DESC`), list of member subsection pages.
2. Each member page shown as a row with title and 1-line description.
3. Click → page panel.

**Acceptance criteria:**
- [ ] Each of the 18 sections renders correctly.
- [ ] Member pages are listed in canonical order (matches `TAXONOMY` dict order).
- [ ] Stubs are excluded from the listing.

**Tool routing:** Claude Code.

#### Task T5.6 — Mobile drawer

Polish the mobile panel into a proper drawer.

**Subtasks:**
1. Drawer states: peek (60 px showing handle + title), open (60% viewport height), full (95%).
2. Touch drag updates `transform: translateY()` in real time; release snaps to nearest state.
3. Tapping graph canvas while drawer is open dismisses to `peek`.
4. Backdrop dim at `open`/`full` states (≤ 30% opacity).

**Acceptance criteria:**
- [ ] On a real phone (or DevTools touch emulation), drawer responds smoothly to drag — 60 fps target.
- [ ] All three drawer states are reachable.
- [ ] Tapping outside closes drawer to peek.
- [ ] No JS errors on resize between portrait/landscape.

**Tool routing:** Claude Design for the interaction spec, Claude Code for the touch event handling.

---

### EPIC-6 — Concept lens UI

Wire the `CONCEPT_LENSES` data through to the user.

| Field | Value |
|---|---|
| Effort | S (½ day) |
| Tools | Claude Code (data + JS), Claude Design (selector styling) |
| Depends on | EPIC-1, EPIC-4, EPIC-5 |
| Unblocks | — |
| Branch | `feature/kg-v1.1/lens-ui` |

#### Task T6.1 — Lens selector dropdown

Top-bar control.

**Subtasks:**
1. Render `<select>` populated from `index.json`'s `lenses` array; first option is "All".
2. Selector positioned in toolbar, left of any future demo controls.
3. Default state: "All", no highlights.

**Acceptance criteria:**
- [ ] Selector lists "All" + every lens declared in `CONCEPT_LENSES`.
- [ ] Future lenses appear automatically without UI code changes.
- [ ] Keyboard navigation works (`Tab`, `Arrow`, `Enter`).

**Tool routing:** Claude Design + Claude Code.

#### Task T6.2 — Highlight-and-dim activation

When a lens is selected, member nodes light up; everything else dims to 10% opacity.

**Subtasks:**
1. JS function `applyLens(lens_id)`: builds member set, toggles `class="lit"` and `class="dimmed"` on nodes.
2. Edges: thicker terracotta stroke for edges between two lens members; dimmed for everything else.
3. Transition smoothly (~400 ms CSS opacity).

**Acceptance criteria:**
- [ ] Selecting "Debt Ledger" highlights exactly 8 pages.
- [ ] Selecting "All" returns to default state.
- [ ] Transition feels deliberate, not jumpy.
- [ ] Search results (EPIC-7) and lens activation interact correctly: search overrides lens highlight; clearing search restores lens.

**Tool routing:** Claude Code.

#### Task T6.3 — Lens caption banner

Above the graph canvas, a thin banner shows the lens caption when one is active.

**Subtasks:**
1. Caption text from `CONCEPT_LENSES[id]["description"]` injected at page render.
2. Show/hide banner on lens selection.
3. Caption styling: italic serif, terracotta left border, ~14 px font.

**Acceptance criteria:**
- [ ] Selecting Debt Ledger shows the cross-cutting-pattern caption above the graph.
- [ ] Selecting "All" hides the banner.
- [ ] Banner does not cause layout shift when toggled.

**Tool routing:** Claude Design.

---

### EPIC-7 — Semantic search frontend

The browser-side embedding + kNN. The technically deepest epic.

| Field | Value |
|---|---|
| Effort | L (3–5 days) |
| Tools | Claude Code (integration), Ralph Loop (perf budget verification), Caveman lite |
| Depends on | EPIC-2, EPIC-3, EPIC-5 |
| Unblocks | EPIC-8 |
| Branch | `feature/kg-v1.1/semantic-search` |

#### Task T7.1 — Integrate Transformers.js

Browser-side embedding generation.

**Subtasks:**
1. Add `<script>` tag for `@xenova/transformers@2.17.2` with SRI hash.
2. Lazy-load: do not call `pipeline()` until first user query. First-query latency budget: 5 s including model download (Service Worker EPIC-9 makes subsequent visits instant).
3. Show loading state in panel: "Loading semantic search engine (33 MB, one-time)…" with progress bar driven by `transformers.js`'s progress callback.
4. Cache model in IndexedDB via Transformers.js's built-in `useBrowserCache` option.

**Acceptance criteria:**
- [ ] First search after fresh load: model downloads, searches succeed within 8 s on a representative 4G connection.
- [ ] Second search same session: < 200 ms.
- [ ] Second visit (cache populated): first search < 500 ms.
- [ ] No JS errors if user navigates away during model load.

**Tool routing:** Claude Code.

#### Task T7.2 — Integrate hnswlib-wasm

Browser-side vector search.

**Subtasks:**
1. Load `vector.bin` via `fetch()` then pass `ArrayBuffer` to hnswlib-wasm's `loadIndex()`.
2. Set `ef_search = 50` per spec §1, sign-off #6.
3. On query: `index.searchKnn(queryEmbedding, k=20)` → indices into chunks array.
4. Resolve chunk indices to chunk objects (full text + page_id).

**Acceptance criteria:**
- [ ] `vector.bin` loads in < 1 s on representative connection.
- [ ] Search returns 20 chunks in < 50 ms after warmup.
- [ ] No memory leaks across 100 sequential searches (use Chrome DevTools Memory profiler).

**Tool routing:** Claude Code.

#### Task T7.3 — Wire search input → kNN → highlight

The end-to-end flow from input to UI.

**Subtasks:**
1. Search input: 300 ms debounce on keystroke.
2. Empty input: clear all highlights and panel state.
3. Non-empty: embed → kNN → group results by `page_id` → top-N pages light up.
4. Side panel: show ranked chunk snippets with parent page title and page-relative position. Click snippet → page panel scrolled to that section.
5. Search results visually distinct from lens highlights (slightly thicker border on lit nodes).

**Acceptance criteria:**
- [ ] Typing "audit findings" highlights all 8 ledger pages.
- [ ] Typing "encryption key rotation" highlights `security/encryption` and `compliance/pci-dss` (or similar).
- [ ] Clearing the input restores graph to default (or to active lens if one is selected).
- [ ] Search box and lens selector compose correctly: search wins.

**Ralph completion promise:** `SEARCH-FLOW-VERIFIED`
**Tool routing:** Ralph Loop fits — completion criterion is a small set of canonical query → expected pages assertions.

#### Task T7.4 — Performance characterization

Measure and document.

**Subtasks:**
1. Add a hidden `?perf=1` query string mode that logs per-step timings to console.
2. Run on 3 reference devices: dev laptop, mid-range Android (Pixel 6 / Galaxy A series), low-end Android (4 GB RAM device).
3. Document p50 / p95 timings in `docs/v1.1-performance.md` (new file).
4. If p95 first-search > 8 s on low-end device, file an issue and consider quantization (deferred to v1.2).

**Acceptance criteria:**
- [ ] Performance doc exists with timings table.
- [ ] All p95 timings under documented budgets, OR a documented exception with mitigation plan.

**Tool routing:** Claude Code.

---

### EPIC-8 — Adjacent suggestions

Surface semantic neighbors *not* connected by curated edges.

| Field | Value |
|---|---|
| Effort | M (1–2 days) |
| Tools | Claude Code, Ralph Loop (precomputation tests), Caveman lite |
| Depends on | EPIC-2, EPIC-7 |
| Unblocks | — |
| Branch | `feature/kg-v1.1/adjacent-suggestions` |

#### Task T8.1 — Build-time computation of top-3 neighbors

Pre-compute at build time, not at runtime.

**Subtasks:**
1. New function `compute_adjacent_suggestions(chunks, embeddings)` in build pipeline.
2. For each substantive page, take its `caption` chunk's embedding; kNN against all other pages' caption chunks.
3. Filter: cosine > 0.55, exclude pages already linked by `related` edge, exclude pages in same lens (those are surfaced separately as "Lens siblings").
4. Take top 3 remaining.
5. Output: extend each page node with `suggestions: [{page_id, similarity}]`.

**Acceptance criteria:**
- [ ] Suggestions computed for all 73 pages.
- [ ] Pages with no suggestions above threshold get `suggestions: []` (don't fabricate).
- [ ] Suggestion target is never the source page itself.
- [ ] Suggestion target is never in the source page's `related` list.
- [ ] Build adds < 30 s to CI runtime.

**Ralph completion promise:** `SUGGESTIONS-COMPUTED`
**Tool routing:** Ralph Loop fits.

#### Task T8.2 — Surface in side panel

UI integration.

**Subtasks:**
1. New panel section "Adjacent suggestions · semantic" between "Authored relations" and "Gold references".
2. Each item: page title, similarity score (e.g., "0.71"), explanatory note: "shares vocabulary, not explicitly linked."
3. Click → page panel.
4. If page has zero suggestions, omit the section entirely (not "(none)" placeholder).

**Acceptance criteria:**
- [ ] Section appears for ~80% of pages (those with suggestions above threshold).
- [ ] Similarity score formatted to 2 decimals.
- [ ] Suggestion items are visually distinct from authored relations (different terracotta accent).

**Tool routing:** Claude Design (treatment), Claude Code (wiring).

---

### EPIC-9 — Service Worker / offline

Make the library function without network after first visit.

| Field | Value |
|---|---|
| Effort | M (1–2 days) |
| Tools | Claude Code, Ralph Loop (offline test scenarios) |
| Depends on | EPIC-3, EPIC-7 |
| Unblocks | EPIC-10 |
| Branch | `feature/kg-v1.1/service-worker` |

#### Task T9.1 — Service Worker scaffold

A new file `src/sw.js`, registered from the knowledge-graph page only (scope-limited).

**Subtasks:**
1. Service Worker version constant `KG_CACHE_V1`.
2. `install` event: pre-cache shell HTML + critical CSS + D3 + manifest.json.
3. `fetch` event: cache-first for hashed assets, stale-while-revalidate for HTML, network-first for `manifest.json` (must always check for updates).
4. `activate` event: delete old caches.

**Acceptance criteria:**
- [ ] Service Worker registers without console errors.
- [ ] DevTools Application tab shows cache populated after first visit.
- [ ] Subsequent visits with network throttled to "Offline" still load `/knowledge-graph/` and function.

**Tool routing:** Claude Code.

#### Task T9.2 — Cache strategy for embedding model

The 33 MB BGE model is the largest single asset.

**Subtasks:**
1. Transformers.js caches in IndexedDB by default; verify this is happening.
2. Service Worker does NOT also cache the model (avoids double-storage).
3. Document this division in `src/sw.js` comments.

**Acceptance criteria:**
- [ ] First visit: model downloads, IndexedDB shows ~33 MB usage.
- [ ] Second visit offline: model loads from IndexedDB; search works.
- [ ] No double-storage in Service Worker cache (Storage tab shows expected size).

**Tool routing:** Claude Code.

#### Task T9.3 — Update strategy

When new content ships, users must get it without manual cache clear.

**Subtasks:**
1. `manifest.json` is fetched network-first; new hashed asset URLs trigger fresh downloads.
2. SW posts `message` to all clients on activation, optionally showing a non-modal "New library content available, refresh to load" toast.
3. Old cached files retained for ~30 days then evicted.

**Acceptance criteria:**
- [ ] Deploying a content change → user reload → new content visible without DevTools cache clear.
- [ ] Toast appears on update, dismissable.
- [ ] No infinite refresh loops if SW activation fails.

**Tool routing:** Claude Code.

#### Task T9.4 — Offline UX

What happens when the user is offline AND has not pre-cached?

**Subtasks:**
1. `/knowledge-graph/` — falls back to cached version (works).
2. Other library pages — show offline page with link back to `/knowledge-graph/`.
3. Loading state if user opens browser offline mid-load: show a clear "Offline — using cached library" indicator.

**Acceptance criteria:**
- [ ] Offline cold start: pages load from cache without error.
- [ ] Offline indicator visible.
- [ ] Search still works offline (model + index already cached).

**Ralph completion promise:** `OFFLINE-VERIFIED`
**Tool routing:** Ralph Loop fits — completion is a scripted Playwright test that throttles to offline and verifies search works.

---

### EPIC-10 — Mobile layout & polish

Final polish + mobile-specific layout precomputation.

| Field | Value |
|---|---|
| Effort | M (1–2 days) |
| Tools | Claude Design (mobile review), Claude Code (precomputation script) |
| Depends on | EPIC-9 |
| Unblocks | — |
| Branch | `feature/kg-v1.1/mobile-polish` |

#### Task T10.1 — Build-time precomputed layout

For mobile, run D3 force simulation in CI with deterministic seed; ship coordinates.

**Subtasks:**
1. New `tools/precompute_layout.py` using `networkx` or a small custom force implementation; deterministic seed `42`.
2. Tick simulation 300 iterations or until alpha < 0.001.
3. Output coordinates merged into `index.json` as `nodes[i].layout = {x, y}`.
4. Frontend on mobile: skip force simulation, use precomputed coords directly. Drag still works (overrides coord temporarily).
5. Desktop: continues to use live simulation for the rearrange affordance.

**Acceptance criteria:**
- [ ] Mobile graph appears stable on first paint — no settling animation.
- [ ] Desktop graph behaves as today.
- [ ] Two consecutive precompute runs produce identical coordinates.

**Tool routing:** Claude Code.

#### Task T10.2 — Touch interactions

Mobile-specific gesture polish.

**Subtasks:**
1. Pinch-zoom on graph canvas (D3 zoom already supports this; verify).
2. Two-finger pan.
3. Tap-and-hold a node → tooltip preview before opening panel.
4. Suppress hover-only states on touch devices (CSS `@media (hover: hover)`).

**Acceptance criteria:**
- [ ] Pinch-zoom works on real device.
- [ ] Two-finger pan works.
- [ ] No hover-state flicker on touch devices.

**Tool routing:** Claude Design + Claude Code.

#### Task T10.3 — Visual QA pass

Final review across breakpoints and themes.

**Subtasks:**
1. Test viewports: 360, 414, 768, 1024, 1440, 1920 px wide.
2. Test print stylesheet (panel content prints cleanly; graph rasterizes acceptably).
3. Run Lighthouse on `/knowledge-graph/`: Performance, Accessibility, Best Practices, SEO.

**Acceptance criteria:**
- [ ] No horizontal scroll at any tested viewport.
- [ ] Lighthouse Accessibility ≥ 95.
- [ ] Lighthouse Performance ≥ 80 on mobile, ≥ 95 on desktop.
- [ ] Lighthouse Best Practices ≥ 95.

**Tool routing:** Claude Design (review), then targeted Claude Code fixes.

---

## 6 — Cross-cutting acceptance criteria

These apply to v1.1 as a whole, not to a single epic. Verify in a final integration pass before merge.

- [ ] **Payload budget.** Total `dist/knowledge-graph/agent/v1/` payload ≤ 2.6 MB (1.6 MB vector index + 0.7 MB chunks + 0.2 MB index + 0.1 MB refs/manifest/schema). Soft target was 2 MB; overage flagged in Risk-1.
- [ ] **First-load tax.** Total first-load assets (HTML + CSS + JS + D3 + Transformers.js + hnswlib-wasm + manifest) ≤ 250 KB; embedding model (33 MB) is lazy-loaded on first query.
- [ ] **Click-doesn't-navigate.** Clicking any non-section page node opens the side panel; URL path stays at `/knowledge-graph/` (hash may change).
- [ ] **Lens correctness.** Selecting "Debt Ledger" highlights exactly the 8 authored member pages; no false positives, no false negatives.
- [ ] **Search latency.** After warmup, semantic search completes in ≤ 500 ms p95 on the dev laptop reference device.
- [ ] **Standards demoted.** Standards render at half-radius and 0.4 fill-opacity by default; labels appear only on hover.
- [ ] **Offline.** With network disabled in DevTools, `/knowledge-graph/` loads, semantic search works, all 73 pages are openable in the panel.
- [ ] **Agent contract.** `curl https://ascendion.engineering/knowledge-graph/agent/v1/index.json` returns valid JSON parseable against `schema.json` (`python -m jsonschema -i index.json schema.json` exits 0).
- [ ] **Discoverability.** `https://ascendion.engineering/llms.txt` resolves and lists agent endpoints.
- [ ] **No external republication.** Repository search confirms no scraped article body text from any third-party blog/standard exists in `content/` or `dist/`.
- [ ] **Accessibility.** Keyboard navigation works for: search input, lens selector, all interactive elements in the side panel. Skip-to-graph link present. Lighthouse a11y score ≥ 95.
- [ ] **CI green.** All existing checks plus the new ones pass: schema validation, vector index round-trip, canonical-query regression, link verifier.

---

## 7 — Risks & mitigations

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Payload exceeds 2 MB soft target with float32 embeddings + references chunks. Realistic landing: ~2.5 MB. | Confirmed | Low — CDN cost negligible; first-load tax dominated by 33 MB model. | Accept overage in v1.1. v1.2 trigger: int8 quantization (~4× shrink) if mobile first-load complaints surface. |
| R2 | BGE model 33 MB first-load is heavy on FSI client devices behind throttled networks. | Medium | Medium — first-time experience may feel slow. | Service Worker caches on first visit; first-load loading state with progress; consider preload on `/about` page so model is warm before user reaches `/knowledge-graph/`. |
| R3 | hnswlib-wasm has limited maintenance velocity; could break on a future Chrome update. | Low | High — vector search would stop. | Pin version. Track upstream issues. Fallback: pure-JS kNN over normalized vectors works at 800-vector scale (~10ms brute force). |
| R4 | Transformers.js model output could drift between versions, breaking the canonical-query regression test. | Low | Medium | Pin Transformers.js version. Update regression expected-results when intentionally upgrading. |
| R5 | Section-index pages added to graph (sign-off #3) increase node count by ~25%; force simulation may settle slower on mobile. | Low | Low | EPIC-10 precomputed layout for mobile sidesteps this entirely. |
| R6 | `CONCEPT_LENSES` validator failing at module load (e.g., a member page renamed without updating lens) blocks all CI builds. | Medium | Medium | Validator error message must include the orphaned page ID and the lens that references it, so the fix is one-line. |
| R7 | Caveman compression on a code-generation session swallows nuance Claude needed to express; subtle bugs ship. | Low | Medium | Use `lite`, not `full`/`ultra`. Run normal-mode review (`/caveman` off) before merging any Claude-Code-authored PR. |
| R8 | Ralph Loop iterates indefinitely on a task whose completion-promise is too ambitious. | Medium | Low — `--max-iterations` caps it. | Always set `--max-iterations 8` (default cap in this playbook) and review work after halt. |

---

## 8 — Suggested execution sequence

Two-week sprint cadence, three sprints to ship. Adjust to actual capacity.

### Sprint 1 — Foundations + build pipeline (2 weeks)

| Day | Focus | Tools |
|---|---|---|
| 1 | EPIC-1 T1.1 (TAG_LINKS refactor) | Claude Code |
| 2 | EPIC-1 T1.2 + T1.3 | Claude Code + Ralph Loop |
| 3–4 | EPIC-2 T2.1 (chunking) | Claude Code + caveman lite |
| 5 | EPIC-2 T2.2 (vector index) | Ralph Loop |
| 6 | EPIC-2 T2.3 + T2.4 (CI + validation) | Claude Code |
| 7 | EPIC-3 T3.1–T3.4 (agent endpoint) | Claude Code + Ralph Loop |
| 8 | Sprint 1 review + merge | — |
| 9–10 | Buffer / catch-up | — |

End of Sprint 1: build pipeline produces the agent endpoint; nothing user-facing has changed yet.

### Sprint 2 — User-facing UX (2 weeks)

| Day | Focus | Tools |
|---|---|---|
| 1 | EPIC-4 T4.1–T4.3 (visual hierarchy + section nodes) | Claude Design + Claude Code |
| 2–4 | EPIC-5 T5.1–T5.3 (panel shell, click wiring, page detail) | Claude Design + Claude Code |
| 5 | EPIC-5 T5.4–T5.5 (standard + section panels) | Claude Code |
| 6 | EPIC-5 T5.6 (mobile drawer) | Claude Design + Claude Code |
| 7 | EPIC-6 T6.1–T6.3 (lens UI) | Claude Design + Claude Code |
| 8 | Sprint 2 review + merge | — |
| 9–10 | Buffer / catch-up | — |

End of Sprint 2: graph is now a workspace. Side panel works. Lenses work. No semantic search yet.

### Sprint 3 — Search + offline + polish (2 weeks)

| Day | Focus | Tools |
|---|---|---|
| 1–3 | EPIC-7 T7.1–T7.4 (semantic search) | Claude Code + Ralph Loop |
| 4 | EPIC-8 T8.1–T8.2 (adjacent suggestions) | Claude Code + Ralph Loop |
| 5–6 | EPIC-9 T9.1–T9.4 (Service Worker / offline) | Claude Code + Ralph Loop |
| 7 | EPIC-10 T10.1–T10.3 (mobile + visual QA) | Claude Design + Claude Code |
| 8 | Cross-cutting acceptance pass | All |
| 9 | Sprint 3 review + final merge to main | — |
| 10 | Production deploy + monitor | — |

End of Sprint 3: v1.1 in production.

---

## 9 — Quick-reference cards

### 9.1 Ralph Loop completion-promise registry

Copy-paste-able prompts for the binary-verifiable tasks:

```bash
# T1.3 — Lens annotation
claude /ralph-loop \
  "Implement T1.3 from knowledge-graph-v1.1-implementation.md. \
   Tests in tools/test_compute_graph_data.py must pass. \
   Output 'LENS-ANNOTATION-VERIFIED' when green." \
  --max-iterations 8 --completion-promise "LENS-ANNOTATION-VERIFIED"

# T2.2 — Vector index
claude /ralph-loop \
  "Implement T2.2: tools/build_vector_index.py. \
   Verify by loading the produced vector.bin and asserting count matches chunks.json. \
   Output 'VECTOR-INDEX-VERIFIED' when round-trip succeeds." \
  --max-iterations 8 --completion-promise "VECTOR-INDEX-VERIFIED"

# T3.2 — Schema validation
claude /ralph-loop \
  "Implement T3.2: write schema.json that validates index.json. \
   Verify with python -m jsonschema. \
   Output 'SCHEMA-VALIDATES' when green." \
  --max-iterations 6 --completion-promise "SCHEMA-VALIDATES"

# T7.3 — Search flow
claude /ralph-loop \
  "Implement T7.3: end-to-end search wiring. \
   Verify canonical queries return expected pages. \
   Output 'SEARCH-FLOW-VERIFIED'." \
  --max-iterations 10 --completion-promise "SEARCH-FLOW-VERIFIED"

# T8.1 — Adjacent suggestions
claude /ralph-loop \
  "Implement T8.1: build-time adjacent-suggestion computation. \
   Verify exclusions and threshold. \
   Output 'SUGGESTIONS-COMPUTED'." \
  --max-iterations 6 --completion-promise "SUGGESTIONS-COMPUTED"

# T9.4 — Offline verified
claude /ralph-loop \
  "Implement T9.4: offline UX. \
   Verify with Playwright offline test. \
   Output 'OFFLINE-VERIFIED'." \
  --max-iterations 8 --completion-promise "OFFLINE-VERIFIED"
```

### 9.2 Caveman usage

```bash
# Start a code-gen session in lite mode
claude /caveman lite

# Compress repo memory (one-time, when CLAUDE.md grows past ~1k lines)
claude /caveman:compress CLAUDE.md
# After this, CLAUDE.original.md is your editable backup; CLAUDE.md is what Claude reads

# Generate a terse commit
claude /caveman-commit

# One-line PR review
claude /caveman-review

# Switch off when doing analysis or spec work
claude /caveman off
```

### 9.3 Branch + commit conventions

- One feature branch per epic: `feature/kg-v1.1/<epic-slug>`.
- Conventional commits: `feat(kg): T2.2 vector index`, `refactor(kg): TAG_LINKS → GOLD_REFERENCES`, etc.
- PR title: `[v1.1] EPIC-N: <name>` — link to this playbook section in description.
- Each PR closes its epic's tracking issue.
- Squash-merge to keep main history clean.

### 9.4 Files affected at a glance

| Path | Touched in |
|---|---|
| `tools/generate.py` | EPIC-1, 2, 3, 4, 5, 6, 7, 8, 10 |
| `tools/seed_content.py` | EPIC-1 |
| `tools/build_vector_index.py` | EPIC-2 (new file) |
| `tools/validate_vector_index.py` | EPIC-2 (new file) |
| `tools/precompute_layout.py` | EPIC-10 (new file) |
| `tools/test_*.py` | EPIC-1, 2, 3, 7, 8 (new files) |
| `tools/requirements-build.txt` | EPIC-2 (new file) |
| `.github/workflows/deploy.yml` | EPIC-2, 3 |
| `src/sw.js` | EPIC-9 (new file) |
| `dist/llms.txt` | EPIC-3 (build output) |
| `dist/knowledge-graph/agent/v1/*` | EPIC-2, 3, 8, 10 (build output) |
| `docs/v1.1-performance.md` | EPIC-7 (new file) |

### 9.5 What NOT to build (deferred — see spec §11)

If you find yourself reaching for any of these during v1.1, stop and confirm with the architecture call:

- Cloud LLM synthesis (Bedrock proxy)
- On-device LLM (WebLLM, Phi-3, Llama)
- External corpus scraping (Netflix/Stripe/Uber blogs, Stack Overflow, ISO/IEEE standards body text)
- TOON-format storage (use JSON for v1.1; reconsider if v1.2 LLM synthesis lands)
- 29-topic ontology refactor (preserve existing 18-section taxonomy)
- Authority scoring of external sources
- PR-reviewable graph diff workflow (v44+ separate refactor)

---

*End of implementation playbook. Open the spec (`knowledge-graph-v1.1.md`) for architectural rationale; open this file (`knowledge-graph-v1.1-implementation.md`) for what to do next.*
