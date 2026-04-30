# ascendion.engineering — Claude session memory

## Project
Static site generator producing the ascendion.engineering knowledge library.
v42 in production. v1.1 knowledge-graph upgrade in flight.

## Conventions (do not violate without asking)
- 2-color palette: warm neutral #D6D2C8 + terracotta #C96330
- 18-section taxonomy in tools/seed_content.py; do not rename
- 73 substantive pages currently; gen handles stubs separately
- AUTHORING_CONVENTIONS embedded in generate.py docstring — substantive tone, no marketing voice
- Mermaid 10.x for diagrams; one diagram type per page

## Active work
Knowledge Graph v1.1 — see docs/v1.1/playbook.md for EPIC/task breakdown.
Spec at docs/v1.1/spec.md. Director prototype at docs/v1.1/prototype.html.

## Critical files
- tools/generate.py — main generator (~250KB)
- tools/seed_content.py — TAXONOMY, soon-to-be CONCEPT_LENSES, GOLD_REFERENCES
- .github/workflows/deploy.yml — CI

## Sign-offs locked (v1.1) — do not relitigate without explicit approval
1. Embedding model: bge-small-en-v1.5
2. Chunking: 10 chunks/page including references
3. Section-index pages: yes, third node type
4. Gold-reference summary_author: "Platform Engineering"
5. Adjacent suggestions: top-3, cosine > 0.55
6. HNSW: M=16, ef_construction=200, ef_search=50

## Working preferences
- Iterative architectural discussion before code
- Short bash audits to verify state before each major action
- Clean commits with verified outputs
- Substantive tone, no marketing voice

## AWS deployment
- ascendion.engineering is hosted in **Ascendion Corporate** AWS account (852973339602)
- SSO profile: `PowerUserAccess-852973339602` (set up via `aws configure sso`)
- Existing CloudFront distribution and S3 bucket continue from v42 — no infra changes for v1.1
- Mediarmor account ([REDACTED_MALAYSIAN_BANK_ACCOUNT_NUMBER_1]) is a separate context (Balangos, VoForma) — NOT used for ascendion.engineering
