# Retrieval-Augmented Generation

The architectural pattern of grounding a language model's output in a corpus the model didn't memorise — recognising that "we'll just plug in a vector database" is the demo, and the architecture is everything between the user query and the retrieved-and-grounded answer.

**Section:** `ai-native/` | **Subsection:** `rag/`
**Alignment:** RAGAS | OpenAI Function Calling | MTEB Embedding Benchmark | OWASP Top 10 for LLM Applications

---

## What "RAG as architecture" actually means

A *prototype* RAG implementation is the diagram from the workshop: query → embed → vector search → top-K documents → stuffed into prompt → model generates answer. It works for the demo because the demo's queries match the corpus and the model mostly knows what to do. The same architecture in production fails repeatedly: chunks split mid-sentence so retrieval gets fragments without context; pure vector search misses keyword matches that BM25 would have caught; the embedding model that worked at prototype-time is now a vendor lock-in nobody planned for; the model invents facts not present in retrieved context and nobody catches it because the system has no faithfulness check; users ask follow-up questions and the system retrieves on the literal follow-up rather than the conversational intent; quality silently degrades as the corpus grows and chunks once retrieved consistently are now buried in noise.

A *production* RAG architecture treats each of these as a design problem with explicit choices. Chunking is application-specific: different corpora, different chunking strategies. Retrieval is hybrid: dense (semantic) and sparse (keyword) recall combined, with reranking. Embedding model selection is recognised as a long-term commitment (re-embedding a corpus is expensive and disruptive). Citation and provenance are first-class system requirements — not "we hope users trust the model" but "the answer cites which retrieved chunks supported each claim, verifiably." Evaluation is multi-axis: faithfulness (does the answer match the retrieved context?), relevance (does the answer match the question?), recall (was the right context retrieved at all?), each measured on representative inputs.

The architectural shift is not "we added retrieval." It is: **RAG is a multi-stage pipeline where each stage has its own failure modes, its own tunable parameters, its own evaluation requirements — and treating it as a single capability obscures where the actual engineering work lives.**

---

## Six principles

### 1. Chunking strategy is application-specific — there is no universal answer

The dominant question in any RAG implementation is rarely "which vector database" — it's "how do we chunk our corpus?" The chunking strategy determines what units of text get retrieved together. Too small, and retrieved chunks lack context (a sentence without its paragraph). Too large, and chunks contain too much irrelevant content (a whole document for a question about one paragraph). Boundaries matter: chunks split at sentence boundaries differ from chunks split at paragraph boundaries differ from chunks aligned with semantic structure (sections, headings) or with the original document's natural units (slides, bullet points). Overlap matters: zero-overlap chunks miss content that straddles boundaries; high-overlap chunks duplicate content and inflate the index. Hierarchical strategies (chunk for retrieval, expand to parent for generation) often outperform flat strategies. The right strategy is application-specific: technical documentation chunks differently from chat transcripts, which chunk differently from research papers.

#### Architectural implications

- Chunking strategy is a deliberate decision per corpus, with the strategy documented and the rationale recorded — not a default from a library.
- Boundary alignment respects the corpus's natural structure: section headings for technical docs, conversation turns for chat, paragraphs for prose, function/method definitions for code.
- Overlap is calibrated: enough to handle boundary-straddling content without flooding the index with duplicates.
- Hierarchical retrieval (small chunks for matching, larger parent units for generation context) is implemented where document structure supports it.

#### Quick test

> Pick a typical retrieval failure in your RAG system — a query that should have hit but didn't. How does the chunking strategy contribute to the failure, and what would change if chunking were different? If the answer is "we use the default chunker," the strategy is inherited rather than chosen — and the failure mode is the strategy's, not the model's.

#### Reference

[LlamaIndex — Chunking Strategies](https://docs.llamaindex.ai/en/stable/optimizing/production_rag/) — the canonical practical reference covering size, overlap, and structural-aware chunking. The conceptual framework is broadly consistent across LangChain, LlamaIndex, and custom implementations; the strategies vary, the trade-off framework does not.

---

### 2. Hybrid retrieval beats pure vector retrieval for most production workloads

Dense retrieval (cosine similarity over embeddings) excels at semantic matching: "how do I authenticate?" matching to a document about "OAuth 2.0 authorization flows." Sparse retrieval (BM25 over keyword indexes) excels at exact and rare-term matching: a product code, a function name, a specific error message, a person's name — terms whose embedding similarity is unreliable but whose keyword match is decisive. Real production queries mix both; pure-dense retrieval fails on exact-term queries, pure-sparse retrieval fails on conceptual queries. The architectural answer is hybrid: run both retrievers in parallel, combine results (reciprocal rank fusion is the canonical method, with weighted variants for workload tuning), and rerank the combined set with a cross-encoder for the final ordering. The cost is a slightly more complex retrieval stage; the benefit is recall that pure-dense or pure-sparse alone cannot achieve.

#### Architectural implications

- Both dense and sparse retrievers are implemented; the fusion strategy (reciprocal rank fusion, weighted combination, learned reranking) is documented.
- Reranking with a cross-encoder is in the pipeline for workloads where retrieval quality justifies the additional latency — typically anything user-facing.
- Retrieval-stage observability captures recall@K for each retriever independently and for the fused/reranked output, so the contribution of each stage is visible.
- Special-case handling for high-precision query types (exact codes, identifiers, named entities) routes deliberately — sometimes the right answer is a keyword-only lookup, not a semantic one.

#### Quick test

> Pick a query type your RAG system underperforms on — exact identifiers, rare terms, follow-up questions. What retrieval stage contributes the failure, and what would hybrid retrieval change? If the answer is "we use vector search," the architecture is missing a recall path that the workload likely needs.

#### Reference

[BM25 — Okapi BM25 (Wikipedia)](https://en.wikipedia.org/wiki/Okapi_BM25) for the canonical sparse retrieval algorithm; [ColBERT (Khattab & Zaharia, 2020)](https://arxiv.org/abs/2004.12832) for the late-interaction approach that bridges dense and sparse with a different trade-off. For practical hybrid implementation patterns, [Pinecone](https://www.pinecone.io/) and [Weaviate](https://weaviate.io/) document the fusion strategies their platforms support.

---

### 3. Embedding model choice is a long-term commitment — re-embedding is expensive

The embedding model that turns text into vectors is deceptively low-stakes-feeling at prototype time and a major architectural commitment in production. Once a corpus is embedded with model X, switching to model Y means re-embedding the entire corpus (compute cost, time, operational risk), reindexing the vector store, and validating that retrieval quality has not regressed in unexpected places. For a corpus of millions of documents, this is a multi-day project. For a corpus that's continuously updated, it requires careful migration choreography: dual-write to both indexes during transition, run both retrievers in shadow, validate, cut over. The architectural discipline is to treat the embedding model selection as a long-horizon decision: evaluate options on representative tasks (MTEB benchmarks plus your own held-out set), prefer models with documented stability and clear vendor commitments, and when self-hosting is operationally feasible, do so to remove the vendor-deprecation risk.

#### Architectural implications

- Embedding model selection is evaluated against representative tasks for the workload — not chosen by default from the platform's recommendation.
- Vendor stability is part of the selection criterion: deprecation history, version-stability policy, and the cost of vendor lock-in.
- Self-hosted embedding models are evaluated for workloads where vendor-deprecation risk is significant, and where serving infrastructure is in place.
- Migration paths are documented before they're needed: dual-write, shadow-evaluation, cutover criteria — so when a migration is required, the runbook exists.

#### Quick test

> Pick the embedding model in production. What does it cost to migrate to a different one, what evaluation criteria would justify the migration, and is there a migration runbook? If those answers don't exist, the embedding choice is a soft commitment that becomes hard exactly when you need to change it.

#### Reference

[MTEB — Massive Text Embedding Benchmark](https://huggingface.co/spaces/mteb/leaderboard) — the canonical multi-task benchmark for embedding model comparison, with task-by-task scores that often differ dramatically from aggregate rankings; the architectural lesson is that "best embedding model" is workload-dependent, not absolute.

---

### 4. Citation and provenance are system requirements — not features

When a RAG system answers a question, the answer is grounded in retrieved context — but the user typically can't see that context. The architectural failure mode is silent ungroundedness: the model produces an answer that draws on its prior training rather than on retrieved context, the user assumes the answer is grounded, and there's no way to verify. The architectural fix is citation and provenance as first-class system properties: each claim in the answer references the retrieved chunks that supported it, in a form the user can verify; the system's UI surfaces these citations alongside the answer; the underlying audit trail records which chunks were retrieved, which made it into the final prompt, and which the model used. Faithfulness — does the answer follow from the cited context? — becomes verifiable, and the system's trustworthiness becomes a property the user can check.

#### Architectural implications

- The model is prompted to cite retrieved chunks for each claim, with an output format that makes citations machine-extractable (footnote markers, structured output with claim-source pairs).
- The user-facing surface displays citations alongside answers, with chunk content viewable on click — not hidden behind opaque IDs.
- Faithfulness scoring (does the cited content actually support the claim?) is computed on a sample of outputs and tracked as a quality metric.
- The audit trail records the full retrieval set, the prompt-included subset, and the cited chunks — for debugging, contestability, and post-hoc verification.

#### Quick test

> Pick a recent answer your RAG system produced. Can you trace each claim in the answer to a specific retrieved chunk that supports it? If the answer is "we don't track that," the system has no provenance — and ungroundedness is invisible.

#### Reference

[Anthropic — Claude with Citations](https://docs.claude.com/en/docs/build-with-claude/citations) and [OpenAI — Citations in Responses API](https://platform.openai.com/docs/guides/responses/) — both major platforms now offer first-class citation primitives that operationalise this principle. RAGAS includes faithfulness scoring as one of its primary metrics, treating it as the operational measurement of grounding.

---

### 5. Multi-axis evaluation — recall, faithfulness, answer relevance, answer correctness — each is a different metric

The temptation to evaluate a RAG system on a single quality score collapses too much information. A system can have excellent recall (right context retrieved) but poor faithfulness (model ignores context and confabulates). It can have excellent faithfulness (answer follows from retrieved context) but poor recall (the right context wasn't retrieved). It can have excellent answer relevance (response addresses the question) but poor correctness (the response is wrong). These are independent failure modes that require independent measurement. The canonical multi-axis frameworks (RAGAS being the most operationalised) define metrics for each: context recall, context precision, faithfulness, answer relevance, answer correctness — with each metric scored separately and tracked as its own signal. A regression in faithfulness is a different bug from a regression in recall, with different remediations.

#### Architectural implications

- Evaluation is multi-axis: recall, faithfulness, answer relevance, answer correctness — each scored independently per axis on a representative eval set.
- Regression detection runs per axis: a deployment that improves answer relevance but degrades faithfulness is gated even if the aggregate score improves.
- Different axes have different remediation paths: recall failures suggest chunking or retrieval changes; faithfulness failures suggest prompt or model changes; answer relevance failures suggest query understanding or query rewriting.
- Evaluation methodology (judge models, scoring rubrics, ground-truth construction) is documented per axis and validated against human review on a sample.

#### Quick test

> Pick the most recent change to your RAG system. Which evaluation axes moved (recall, faithfulness, relevance, correctness), in which direction, by how much? If the answer is "the eval score improved," the evaluation is collapsing axes that should be kept separate — and the change may have improved one axis at the cost of another.

#### Reference

[RAGAS — Retrieval-Augmented Generation Assessment](https://docs.ragas.io/) — the canonical multi-axis evaluation framework with operational implementations of each metric. The conceptual contribution (treating recall, faithfulness, relevance, and correctness as independent properties) generalises beyond the specific tooling.

---

### 6. The corpus is part of the system — its quality and freshness are operational concerns

The retrieved corpus is treated as a feature in some architectures and as the system in others. In a RAG architecture, the corpus *is* the system in a meaningful sense — its content directly determines the answers. A stale corpus produces stale answers; an incomplete corpus produces missing answers; a corpus full of contradictions produces inconsistent answers. The architectural discipline is to treat corpus management as operational engineering: ingestion pipelines with documented sources, freshness SLAs (how recent must content be?), quality gates (what content qualifies for the corpus?), version control (what changed when?), and feedback loops (which retrieved chunks were never useful, which were misleading?). Without this, the corpus is a static asset that decays in step with the world it's supposed to describe.

#### Architectural implications

- Ingestion pipelines have documented sources, transformation rules, and freshness SLAs — the corpus is built deliberately, not accumulated by accident.
- Quality gates filter ingested content: deduplication, conflict detection, format normalisation, redaction of sensitive content where required.
- Corpus changes are versioned: which documents were added, removed, or modified, when, and why — a corpus changelog is queryable and auditable.
- Feedback from retrieval-stage observability informs corpus management: chunks that are never retrieved are flagged for review (irrelevant content), chunks that are frequently retrieved but produce low-faithfulness answers are flagged for accuracy review.

#### Quick test

> Pick a document in your corpus. When was it ingested, how fresh is it, and what process would update it if its source changed? If the answer is "we did a one-time import last quarter," the corpus has no operational discipline — and its freshness is whatever the original import captured.

#### Reference

[LlamaIndex — Production RAG](https://docs.llamaindex.ai/en/stable/optimizing/production_rag/) covers ingestion pipeline patterns as part of its production guidance. The broader operational framing of corpus management as engineering discipline (rather than as one-time setup) is treated in detail in [Anthropic Engineering](https://www.anthropic.com/engineering)'s case studies on production RAG deployments.

---

## Architecture Diagram

The diagram below shows a canonical production RAG system: corpus ingestion with quality gates and versioning; chunking aligned to document structure; hybrid retrieval (dense + sparse) with cross-encoder reranking; prompt construction with retrieved context; model generation with citation; faithfulness and recall scoring on the output; user-facing citation surface; feedback loops back to corpus management and evaluation.

---

## Common pitfalls when adopting RAG architecture

### ⚠️ The default chunker

A library's default chunker (fixed-size, character-count-based, no structural awareness) is used because it works. It works well enough on smooth narrative prose and poorly on structured documents (tables, code, hierarchical sections). The retrieval recall is mediocre on the structured content; the team blames the model.

#### What to do instead

Chunking is matched to corpus structure. Technical docs chunk by section. Code chunks by function. Conversations chunk by turn. Tables and structured data are kept intact rather than split across chunks. The chunker is custom or selected for the corpus, not inherited.

---

### ⚠️ Vector-only retrieval

The system uses vector search and nothing else. Exact-term queries (product codes, function names, identifiers) routinely fail. The model's downstream answer is plausible but unhelpful because it had to make do with similar-but-wrong context.

#### What to do instead

Hybrid retrieval. Dense retrieval for semantic match, sparse (BM25) for exact terms, fusion (reciprocal rank fusion) for combination, cross-encoder reranking for final ordering. Or, where workload diversity is small, route by query type: identifier-like queries to exact-match, conceptual queries to semantic.

---

### ⚠️ The unannounced embedding migration

The team upgrades the embedding model in place without re-embedding the corpus. The new model produces embeddings in a different space (or the same space with subtle drift). Retrieval quality degrades silently. Investigation takes weeks; the cause is the in-place model change.

#### What to do instead

Embedding migrations are deliberate: re-embed the corpus, build the new index alongside the old, run both retrievers in shadow mode, compare quality, cut over. Never change the embedding model in place against an existing index.

---

### ⚠️ Citations that don't actually verify

The model is asked to cite sources. It produces citation-shaped strings — chunk IDs, paragraph numbers, section names — that look like citations but don't actually correspond to the content claimed. The user sees citations, assumes grounding, and is misled. The architecture has weaponised the appearance of provenance.

#### What to do instead

Citations are machine-extracted from structured output and verified against the actual retrieved chunks. The UI displays only citations that match real retrieved content. Faithfulness scoring catches mismatches between cited chunks and answer claims.

---

### ⚠️ The evergreen corpus that isn't

The team imported the corpus at launch. They intended to update it. They haven't. Two years later, the corpus describes a product version that's been deprecated, processes that have changed, people who have left, terminology that's evolved. Users complain that "the AI gives outdated information." The model is fine; the corpus is stale.

#### What to do instead

Ingestion pipelines run on a documented cadence. Freshness SLAs are defined per content type. Stale content is detected automatically (by source-system change events, by periodic recrawl, by user feedback) and refreshed. The corpus is operational infrastructure, not a one-time deliverable.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Chunking strategy is documented and matched to the corpus's structural properties ‖ Different corpora chunk differently; the strategy is deliberate, with size, overlap, and boundary-alignment chosen for the actual content. Hierarchical retrieval is used where document structure supports it. | ☐ |
| 2 | Hybrid retrieval (dense + sparse) with reranking is implemented for user-facing workloads ‖ Pure vector retrieval misses exact-term and rare-term queries. Hybrid retrieval with cross-encoder reranking is the production-quality default; pure dense retrieval is the degraded variant. | ☐ |
| 3 | Embedding model selection is evaluated on representative tasks and treated as a long-term commitment ‖ MTEB scores plus held-out task evaluation; vendor stability and migration cost are in scope. The selection is deliberate; the migration runbook exists before it's needed. | ☐ |
| 4 | Citations and provenance are produced, displayed, and verified ‖ The model cites retrieved chunks for claims; the UI displays citations with viewable content; faithfulness scoring verifies citations match retrieved content; audit trails record full retrieval and citation sets. | ☐ |
| 5 | Faithfulness scoring runs continuously on a sample of outputs ‖ Faithfulness — does the answer follow from the retrieved context? — is the operational measurement of grounding. Without it, ungrounded outputs ship undetected. | ☐ |
| 6 | Recall, faithfulness, answer relevance, and answer correctness are scored as independent axes ‖ Multi-axis evaluation. Each axis is its own bug; collapsing to a single score hides regressions in one axis behind improvements in another. Per-axis regression detection gates deployment. | ☐ |
| 7 | Corpus ingestion has documented sources, freshness SLAs, and quality gates ‖ The corpus is operational infrastructure: built deliberately, refreshed on a cadence, gated for quality. Stale corpora produce stale answers regardless of model quality. | ☐ |
| 8 | Corpus changes are versioned with a queryable changelog ‖ Which documents were added, removed, or modified, when, and why. The corpus is auditable; reproducing an old answer requires knowing the corpus version that produced it. | ☐ |
| 9 | Retrieval-stage observability captures recall@K independently per retriever and fused output ‖ The contribution of each stage is visible: where recall fails, where reranking helps, where the system has the right answer in the candidate set but ranks it too low. | ☐ |
| 10 | Feedback from retrieval observability and user signals informs corpus and chunking iteration ‖ The system improves the corpus and the retrieval over time based on observed performance. Frequently-retrieved low-faithfulness chunks are flagged for accuracy review; never-retrieved chunks are flagged for relevance review. | ☐ |

---

## Related

[`technology/databases`](../../technology/databases) | [`ai-native/architecture`](../architecture) | [`ai-native/monitoring`](../monitoring) | [`ai-native/security`](../security) | [`ai-native/ethics`](../ethics) | [`patterns/data`](../../patterns/data)

---

## References

1. [RAGAS](https://docs.ragas.io/) — *ragas.io*
2. [MTEB Embedding Benchmark](https://huggingface.co/spaces/mteb/leaderboard) — *huggingface.co*
3. [BM25 — Okapi BM25 (Wikipedia)](https://en.wikipedia.org/wiki/Okapi_BM25) — *Wikipedia*
4. [ColBERT (Khattab & Zaharia, 2020)](https://arxiv.org/abs/2004.12832) — *arXiv*
5. [HyDE (Gao et al., 2022)](https://arxiv.org/abs/2212.10496) — *arXiv*
6. [Pinecone](https://www.pinecone.io/) — *pinecone.io*
7. [Weaviate](https://weaviate.io/) — *weaviate.io*
8. [Qdrant](https://qdrant.tech/) — *qdrant.tech*
9. [LlamaIndex — Production RAG](https://docs.llamaindex.ai/en/stable/optimizing/production_rag/) — *llamaindex.ai*
10. [FAISS](https://github.com/facebookresearch/faiss) — *github.com*
