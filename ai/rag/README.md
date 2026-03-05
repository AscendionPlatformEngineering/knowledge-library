# RAG Architecture

> **Section:** `ai/` | **Subsection:** `rag/`  
> **Alignment:** TOGAF ADM | NIST CSF | ISO 27001 | AWS Well-Architected | AI-Native Extensions

---

## Overview

Retrieval-Augmented Generation: chunking strategies, embedding models, vector stores, reranking, and hybrid search.

This document is part of the **AI-Native Architecture** body of knowledge within the Ascendion Architecture Best-Practice Library. It provides comprehensive, practitioner-grade guidance aligned to industry standards and extended for AI-augmented, agentic, and LLM-driven design contexts.

---

## Core Principles

### 1. Retrieval Quality is the Ceiling on Generation Quality

No LLM can generate a correct answer from incorrect or missing context. Invest disproportionately in retrieval quality — chunking strategy, embedding model selection, hybrid search, and reranking — before tuning the generation step.

### 2. Chunk Boundaries Must Respect Semantic Units

A chunk should represent one complete thought: a full step, a complete definition, a whole code block. Chunks that split semantic units at arbitrary token boundaries degrade retrieval quality significantly.

### 3. Evaluate Retrieval and Generation Separately

Conflating retrieval and generation metrics hides root causes. Track Context Recall (retrieval), Answer Faithfulness (no hallucination), and Answer Relevance (addresses the question) as three independent metrics.

### 4. Hybrid Search Over Pure Vector

Combining dense vector search with sparse keyword search (BM25) consistently outperforms either alone. Deploy Reciprocal Rank Fusion to combine ranked results from both methods.

### 5. Metadata Filtering Prevents Stale Answers

Vector similarity does not know that a document was superseded six months ago. Add document date, status, and classification as metadata fields. Apply filters at retrieval time to exclude expired or restricted content.


---

## Implementation Guide

**Step 1: Build the Golden Evaluation Dataset First**

Before ingesting a single document, create 200–500 question-answer pairs from your knowledge base. This dataset is your measurement instrument — all pipeline decisions (chunking, embedding model, retrieval strategy) are evaluated against it.

**Step 2: Design the Ingestion Pipeline**

Source documents → pre-processing (format normalization, table extraction) → chunking (semantic or hierarchical) → embedding → vector store + metadata store. Each stage should be independently replaceable.

**Step 3: Implement and Validate Hybrid Search**

Deploy both dense (vector) and sparse (BM25) search. Measure precision@5 for each independently on your golden dataset. Implement RRF fusion and measure the combined precision. Expect a 15–25% improvement over vector-only.

**Step 4: Add the Reranking Stage**

After hybrid search returns top-20 candidates, deploy a cross-encoder reranker to rescore by true relevance. Evaluate the reranked top-5 against your golden dataset. This is typically the highest single-step quality improvement available.

**Step 5: Instrument the Full Pipeline**

Log every query, retrieved chunks, reranked scores, and generated response. Use an evaluation framework (RAGAS, TruLens, DeepEval) for continuous monitoring. Set quality alerts: if Answer Faithfulness drops below 85%, trigger an investigation.


---

## Governance Checkpoints

| Checkpoint | Owner | Gate Criteria | Status |
|---|---|---|---|
| Golden Dataset Created | AI Engineer | 200+ question-answer pairs covering key use cases | Required |
| Chunking Strategy Validated | AI Architect | Retrieval recall benchmarked on golden dataset per chunking strategy | Required |
| Hybrid Search + Reranking Deployed | AI Engineer | Combined pipeline precision@5 exceeds vector-only baseline by >10% | Required |
| RAGAS Evaluation Pipeline Active | MLOps | Automated RAGAS evaluation running on weekly cadence | Required |
| PII Scrubbing in Ingestion | Security Engineer | PII detection and redaction applied before embedding | Required |


---

## Recommended Patterns

### Hierarchical Chunking

Store documents at multiple granularities: sentence-level chunks for precise retrieval, paragraph-level for context richness. Retrieve fine-grained chunks; inject their parent sections into the context window for completeness.

### HyDE (Hypothetical Document Embeddings)

Generate a hypothetical answer to the query using the LLM, embed the hypothetical answer, then retrieve documents similar to it. Bridges the vocabulary gap between short queries and long documents. Especially effective for technical documentation retrieval.

### Self-RAG

The LLM itself decides at each step whether to retrieve additional context, evaluates the relevance of retrieved documents, and critiques its own answer for faithfulness. More accurate than standard RAG but significantly more expensive in token usage.

### Agentic RAG

A planning agent breaks complex queries into sub-questions, issues targeted retrievals for each, synthesizes intermediate answers, and composes the final response. Handles multi-hop questions that require combining information from multiple documents.


---

## Anti-Patterns to Avoid

### ⚠️ Top-k Without Reranking

Sending the top-k vector similarity results directly to the LLM without reranking. Vector similarity ≠ relevance. A chunk that contains the same words as the query but in a different context will score highly and mislead the LLM. Always rerank.

### ⚠️ Ignoring Metadata Filtering

Retrieving documents by pure semantic similarity without filtering by date, classification, or status. Expired policies, superseded procedures, and restricted documents get surfaced as valid context. Corrupts answer quality and creates compliance risks.

### ⚠️ Naive Fixed-Size Chunking

Splitting documents at fixed token counts (every 512 tokens) without regard for sentence or paragraph boundaries. Breaks semantic units, splits code examples mid-function, and severs numbered lists mid-step. Use semantic chunking libraries (LangChain's SemanticChunker, LlamaIndex's SentenceSplitter).


---

## AI Augmentation Extensions

### Continuous RAG Evaluation Pipeline

An automated pipeline runs the golden evaluation dataset against the production RAG system on a scheduled basis. Context Recall, Answer Faithfulness, and Answer Relevance are tracked over time. Quality regressions trigger alerts and block model/pipeline upgrades.

> **Note:** Expand the golden dataset continuously as new query patterns are observed in production logs. Stale evaluation datasets produce misleading quality signals.

### RAG-Powered Architecture Copilot

This library itself is structured for RAG ingestion. An architecture copilot agent retrieves relevant sections based on architect queries, cites the specific subsection, and generates advice grounded in the documented standards.

> **Note:** The copilot cites sources so architects can verify advice. It does not replace ARB review or human architectural judgment.


---

## Related Sections

[`ai/architecture`](../ai/architecture) | [`ai/monitoring`](../ai/monitoring) | [`data/modeling`](../data/modeling) | [`patterns/data`](../patterns/data) | [`adrs/ai`](../adrs/ai)

---

## References

1. [RAG Survey — Gao et al. 2023](https://arxiv.org/abs/2312.10997) — *arxiv.org*
2. [Advanced RAG Techniques — Llamaindex Blog](https://www.llamaindex.ai/blog) — *llamaindex.ai*
3. [RAGAS: Automated Evaluation — GitHub](https://github.com/explodinggradients/ragas) — *github.com*
4. [Reranking in RAG — Cohere Documentation](https://docs.cohere.com/docs/reranking) — *docs.cohere.com*
5. [AI Engineering — Chip Huyen](https://www.oreilly.com/library/view/ai-engineering/9781098166298/) — *O'Reilly*


---

*Last updated: 2025 | Maintained by: Ascendion Solutions Architecture Practice*  
*Section: `ai/rag/` | Aligned to TOGAF · NIST · ISO 27001 · AWS Well-Architected*
