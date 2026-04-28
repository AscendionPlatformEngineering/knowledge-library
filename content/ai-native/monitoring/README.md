# AI Monitoring & Observability

The signals that tell you whether an AI system is working — recognising that classical observability (latency, error rate, throughput) is necessary but radically insufficient, because AI systems can be perfectly fast, perfectly available, and producing wrong answers all day long.

**Section:** `ai-native/` | **Subsection:** `monitoring/`
**Alignment:** OpenTelemetry GenAI Conventions | NIST AI Risk Management Framework | RAGAS

---

## What "AI observability" actually means

A *classical* observability stack — Prometheus metrics, distributed traces, structured logs — answers the questions: is the service up, how fast is it, what's the error rate, what's the throughput? These are necessary for any production system, AI or otherwise. A perfectly classical-observable AI system can be 100% available, sub-100ms latency, zero error rate, and producing nonsense — and the dashboard will be all green. The classical signals are necessary; the observability surface they cover is no longer the whole observability surface.

An *AI-specific* observability stack adds signals the classical stack cannot produce: drift indicators (the input distribution has shifted from what the model was trained or evaluated on), output quality scores (the model's outputs are scored against rubrics, reference answers, or by judge models), hallucination rate (where verifiable, the proportion of outputs that contain factual errors), feedback signals (user-level signals that the output was useful or not — explicit ratings, implicit downstream behaviour), token economics (per-request cost, cost per outcome, cost trends), and end-to-end inference traces (the full path from prompt to output, including retrievals, tool calls, and intermediate model invocations). The classical stack tells you whether the system is responding; the AI stack tells you whether it's responding *correctly*. Both are required.

The architectural shift is not "we added some dashboards." It is: **AI systems have failure modes that classical observability cannot detect — silent quality degradation, drift, hallucination — and the observability stack must be expanded to include AI-specific signals before any of those failure modes become incidents.**

---

## Six principles

### 1. Quality, not just availability — output quality is the central signal

A traditional service has two primary signals: is it up, and is it fast? An AI service has a third primary signal: is its output good? "Good" is workload-specific — for a summarisation system it's faithfulness and informativeness; for a classification system it's correctness and calibration; for a code-generation system it's compilation, correctness, and style; for a RAG system it's faithfulness to retrieved context and answer relevance. Whatever "good" means in context, it must be *measured continuously* — not only during evaluation, not only on held-out test sets, but in production, on real traffic, with results visible on the same dashboards that show latency. Without continuous quality measurement, the system can degrade silently for weeks before users complain enough to surface the problem.

#### Architectural implications

- "Output quality" is defined per AI surface with measurable metrics — faithfulness, relevance, correctness, calibration — appropriate to what the workload produces.
- Quality is measured continuously on production traffic, not only on held-out evaluation sets — a sample of production outputs is scored automatically (rules, judge models) and tracked over time.
- Quality dashboards exist alongside latency and error-rate dashboards; SLOs include quality thresholds, not only availability and latency thresholds.
- Quality regressions trigger alerts and incident response — a sustained drop in output quality is treated with the same urgency as a sustained increase in error rate.

#### Quick test

> Pick the most-used AI feature in your system. What's its current output quality score, what was it a week ago, and what would alert if it degraded? If those numbers don't exist, quality is invisible — and the system can degrade without anyone noticing until users complain.

#### Reference

[OpenTelemetry — GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — the canonical reference for instrumenting AI systems with quality-relevant attributes (model name, prompt tokens, completion tokens, evaluation scores) in a vendor-neutral way.

---

### 2. Drift detection is necessary because the world doesn't stay still

Foundation models are trained on data with a cutoff. Fine-tuned models are trained on data the team curated at a moment in time. RAG systems retrieve from corpora that grow, change, and become stale. Production traffic evolves: new query patterns, new domains, new vocabulary, new edge cases. Drift — the divergence between what the system was designed for and what it now sees — is not a question of *whether* but of *when and how much*. Drift detection in AI systems takes multiple forms: input distribution drift (the questions are different now), output distribution drift (the model's outputs have shifted), feedback drift (users are responding differently), corpus drift (in RAG, the underlying documents have changed). Each requires its own monitoring; collectively, they are how the system notices that its environment has changed before that change becomes a quality problem.

#### Architectural implications

- Input distribution monitoring tracks features of incoming requests (query length, topic distribution, language, complexity) against a baseline and alerts on significant divergence.
- Output distribution monitoring tracks features of model outputs (length, refusal rate, structure conformance, judge-scored quality) against a baseline.
- For RAG systems, corpus drift is monitored — newly added documents, removed documents, and changes in retrieval patterns over time.
- Drift thresholds are calibrated to the workload — too tight produces noise, too loose lets drift accumulate; calibration is reviewed periodically as the system matures.

#### Quick test

> Compare your AI system's input distribution today to its input distribution six months ago. What shifted, and how would you know? If the only way to compare is to manually pull samples from each period and look at them, drift is being noticed retrospectively at best, not detected.

#### Reference

[Evidently AI](https://www.evidentlyai.com/) — the canonical open-source library for ML drift detection across input, output, and prediction distributions; the conceptual framework (data drift, concept drift, prediction drift) transfers to LLM systems with appropriate adaptation.

---

### 3. Hallucination is a measurable signal — for the workloads where it can be measured

Foundation models produce confident, fluent, plausible outputs that are sometimes wrong. The hallucination rate — the proportion of outputs containing factual errors — is workload-dependent: for closed-book question-answering, hallucination is the dominant quality concern; for RAG systems, it manifests as outputs unfaithful to retrieved context; for code generation, it appears as references to non-existent functions, libraries, or APIs; for tool use, it shows up as fabricated tool arguments. Where hallucination is measurable — by checking outputs against retrieval context, against verified knowledge bases, against compilation/execution, against ground truth — that measurement is a critical observability signal. Where it is not directly measurable, proxies (refusal rate, citation density, calibrated uncertainty, judge-model assessment) approximate it. Either way, the system's hallucination tendency is observable, and the architectural discipline is to observe it.

#### Architectural implications

- For RAG systems, faithfulness scoring (output supported by retrieved context) is computed on a sample of production outputs and tracked as a primary metric.
- For tool-use systems, hallucinated tool calls (calls to non-existent tools, fabricated arguments) are detected at the boundary and recorded as a quality failure.
- For code-generation systems, compilation and basic execution checks on a sample of outputs serve as ground-truth signal for hallucination rate.
- Where direct measurement is unavailable, proxies are used deliberately and documented as proxies — not as ground truth.

#### Quick test

> Pick the workload in your system most affected by hallucination. What's the current hallucination rate, how is it measured, and what would a 2x increase look like on your dashboards? If the answer is "we don't have a number," the failure mode is not being monitored — and the next hallucination incident will surface in customer complaints.

#### Reference

[RAGAS](https://docs.ragas.io/) — the canonical multi-metric framework for RAG evaluation that includes faithfulness scoring as one of its primary axes, providing operational measurement of hallucination in retrieval-grounded systems.

---

### 4. Token economics are an observability signal, not just a cost concern

Per-request token usage tells you more than just the bill. Sudden increases in input tokens may indicate that the prompt template has changed, that a retrieval system is returning more context than before, or that user queries have grown longer in ways worth investigating. Sudden increases in output tokens may indicate that the model is generating more verbose responses (often a quality concern, not just a cost one) or that the system is in an unbounded loop. The cost per outcome (cost per resolved issue, cost per useful answer, cost per closed task) is a far better metric than cost per call, because it accounts for the work the system is actually doing rather than just its mechanical activity. Treating token telemetry as observability — alongside the cost concern — surfaces architectural problems that classical observability misses.

#### Architectural implications

- Token usage is recorded per request: input tokens, output tokens, cached tokens, model identifier — not aggregated to monthly totals after the fact.
- Token-per-request distributions are monitored: sudden increases in median or tail tokens are alerts, not just budget concerns.
- Cost-per-outcome metrics are computed where outcomes can be defined (cost per resolved support ticket, cost per accepted code suggestion, cost per validated answer) — this is the metric that connects spend to value.
- Token economics dashboards sit alongside latency and quality dashboards, not in a finance-only spreadsheet.

#### Quick test

> Pick your highest-volume AI feature. What's its current cost per resolved outcome (not per call), how has that trended over the past month, and what would alert you if it doubled? If "cost per outcome" is undefined, the system's economic efficiency is invisible to engineering.

#### Reference

[Helicone](https://www.helicone.ai/) and [Langfuse](https://langfuse.com/) — production-oriented LLM observability platforms that treat token usage and cost as first-class observability signals, alongside latency and quality.

---

### 5. End-to-end inference tracing — across retrievals, tool calls, model hops, and post-processing

A single user-visible AI interaction often involves a half-dozen or more underlying operations: a query is embedded, a vector store is queried, candidate documents are reranked, a prompt is constructed, a model is called, the output is parsed, a tool is invoked based on the output, the tool's result feeds back into another model call, and so on. When something goes wrong — slow response, wrong answer, exception, refusal — the team needs to see the entire chain of operations to diagnose where. Distributed tracing, adapted for AI workloads with operation types (retrieve, embed, generate, tool-call, parse) and AI-specific attributes (model, tokens, scores), is the architectural primitive for this. Without it, debugging an AI system reduces to pulling logs from each component and reconstructing the chain mentally — which scales poorly and produces biased reconstructions.

#### Architectural implications

- Distributed tracing is enabled across all AI operations, with spans for each significant step (embed, retrieve, rerank, generate, tool call, parse, validate).
- Spans carry AI-specific attributes: model name and version, prompt tokens, completion tokens, retrieval scores, tool names, evaluation scores — not only the classical span attributes.
- Traces are sampled at a rate that captures interesting events (errors, slow tails, low-quality outputs) more aggressively than uninteresting routine traffic.
- Traces are linked to the audit log, the cost telemetry, and the quality scoring — one operation produces signal across all observability surfaces.

#### Quick test

> Pick a recent slow or low-quality AI interaction in your system. Can you produce, in seconds, the full trace of operations that produced it — embedding, retrieval, model call, tool calls, post-processing — with their durations and intermediate outputs? If the answer involves correlating logs across components manually, the system is not traced and debugging is bottlenecked.

#### Reference

[OpenTelemetry — Distributed Tracing](https://opentelemetry.io/docs/concepts/signals/traces/) provides the underlying tracing primitive; [GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) extends it with AI-specific attributes; [Arize Phoenix](https://phoenix.arize.com/) and [LangSmith](https://docs.smith.langchain.com/) provide developer-friendly trace UIs purpose-built for LLM workloads.

---

### 6. Feedback loops — turning user signals into evaluation data

The most valuable signal an AI system can collect is also the most-overlooked: user feedback on individual outputs. Explicit feedback (thumbs up/down, ratings, corrections) and implicit feedback (did the user accept the suggestion, did they revise it, did they retry, did they abandon) carry information that no automated metric can produce. Capturing this feedback, attaching it to the corresponding output and trace, aggregating it over time, and feeding it back into both monitoring (which outputs were problematic) and evaluation (extending the eval set with real cases) is the architectural pattern that closes the loop between deployed behaviour and engineering improvement. Without this, the team improves the system based on guesses about what's wrong; with this, they improve based on evidence.

#### Architectural implications

- Explicit feedback (rating, correction, confirmation) is captured at the point of interaction with low friction — buttons or shortcuts inline with the output.
- Implicit feedback (user behaviour after seeing the output: accepted, revised, retried, abandoned) is captured where the workload allows — instrumentation built into the consuming surface.
- Feedback is attached to the trace and audit log of the original output, producing rich training/evaluation data.
- A subset of feedback-tagged outputs is reviewed regularly and added to the evaluation set, growing the eval distribution toward production reality over time.

#### Quick test

> Pick the AI feature in your system with the highest volume. What proportion of interactions has feedback attached, how is that feedback used, and how has the eval set grown from feedback over the past quarter? If feedback is captured and not used, or used only at aggregate level without per-output review, the loop is open.

#### Reference

[LangSmith](https://docs.smith.langchain.com/) and [Arize Phoenix](https://phoenix.arize.com/) — both treat feedback collection as a first-class capability with linkage to traces and evaluation. The architectural framing of feedback loops as data flywheels is treated extensively in [Anthropic Engineering](https://www.anthropic.com/engineering) and OpenAI's production deployment guides.

---

## Architecture Diagram

The diagram below shows a canonical AI observability stack: classical signals (latency, errors, throughput) running alongside AI-specific signals (quality scores, drift indicators, hallucination rate, token economics); end-to-end tracing across embeddings, retrievals, model calls, tools, and post-processing; feedback collection at the user surface; an evaluation pipeline that ingests both production samples and feedback to produce eval-set extensions and gate deployments.

---

## Common pitfalls when adopting AI observability

### ⚠️ The all-green dashboard

The classical dashboard shows 100% availability, 80ms p95, 0% errors. The team is satisfied. Meanwhile, a prompt change three weeks ago has caused output quality to silently degrade by 25%. Users have noticed but customer support is the only feedback channel; engineering is unaware until escalation reaches them.

#### What to do instead

Quality dashboards next to availability dashboards. Quality SLOs alongside latency SLOs. Output sampling and scoring runs continuously in production. The system's actual usefulness is monitored alongside its mechanical responsiveness.

---

### ⚠️ Drift detection that nobody calibrated

A drift detector is deployed with default sensitivity. It alerts daily on noise, the team mutes the alerts, the alerts continue firing in the muted state. Six months later, real drift occurs, the alert fires, nobody sees it, the drift causes a quality incident.

#### What to do instead

Drift thresholds are calibrated to the workload — accepting some noise to catch the meaningful signals, or accepting some delay to reduce noise. Calibration is reviewed periodically. Muted alerts are an audit-trail bug, not a normal operating condition.

---

### ⚠️ Sampling traces by outcome, not by interest

100% of successful traces are sampled and stored. 100% of error traces are sampled. The store is full of routine successes that nobody investigates; the interesting cases (slow tails, low-quality outputs, partial failures) are buried in the noise.

#### What to do instead

Tail-based sampling: keep all errors, all slow tails (above p95 latency), all low-quality outputs (below quality threshold), and a small representative sample of routine traffic for baseline. The store optimises for what's worth investigating, not for what's most common.

---

### ⚠️ Cost as a finance concern, not an engineering signal

Token costs aggregate to a monthly bill the finance team queries. Engineering doesn't see per-request cost in the dashboards alongside latency. When a cost regression occurs (prompt change, retrieval expansion, longer outputs), it's noticed in the finance review weeks later, not in the deploy-time dashboards.

#### What to do instead

Token usage and cost are first-class engineering observability signals on the same dashboards as latency. Cost regressions on deployment are detected in canary phase, not in monthly review. Cost-per-outcome is the engineering-friendly metric that connects spend to value.

---

### ⚠️ Feedback collected and stored, never used

The system has a thumbs-up/down on every output. The data flows into a table that nobody queries. The team improves the system based on intuition rather than the evidence sitting in their database.

#### What to do instead

Feedback is the seed for eval-set growth: tagged outputs are reviewed, validated, and migrated into the eval set on a regular cadence. Feedback informs prioritisation: which features are users dissatisfied with, which prompts produce frequent corrections, which model versions have higher negative-feedback rates.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Output quality is defined and measured continuously on production traffic, not only on held-out evaluation sets ‖ Quality scores run as continuous signals; quality SLOs are defined; quality regressions trigger alerts and incident response same as availability regressions. | ☐ |
| 2 | Input, output, and (where relevant) corpus drift detection is in place with calibrated thresholds ‖ Distribution monitoring is in place for inputs, outputs, and the underlying corpus where applicable. Thresholds are calibrated to balance noise and signal; calibration is reviewed periodically. | ☐ |
| 3 | Hallucination signal is captured per workload — directly where measurable, via proxies where not ‖ Faithfulness for RAG, compilation/execution checks for code, fabrication detection for tool calls. Where direct measurement isn't available, proxies (refusal rate, citation density, calibrated uncertainty, judge scores) are used deliberately. | ☐ |
| 4 | Token usage is observed per request — input, output, cached, model — not aggregated to monthly cost only ‖ Token economics are first-class observability, surfaced on engineering dashboards alongside latency. Sudden distributional shifts in tokens are alerts, not month-end discoveries. | ☐ |
| 5 | Cost-per-outcome metrics are defined for workloads where outcomes can be measured ‖ Cost per resolved ticket, cost per accepted code suggestion, cost per validated answer — the metric that connects spend to value, and that surfaces architectural inefficiency that cost-per-call misses. | ☐ |
| 6 | End-to-end tracing covers all AI operations with appropriate AI-specific attributes ‖ Spans for embed, retrieve, rerank, generate, tool-call, parse, validate; attributes for model, tokens, scores. Distributed tracing across the full chain is the primitive that makes AI debugging tractable. | ☐ |
| 7 | Trace sampling is tail-based: keep errors, slow tails, low-quality outputs, plus a baseline sample ‖ Optimise the trace store for what's worth investigating, not for what's most common. The interesting cases are kept in full; routine traffic is sampled for baseline only. | ☐ |
| 8 | Explicit and implicit user feedback is captured at the point of interaction and attached to the trace ‖ Feedback closes the loop between deployed behaviour and engineering improvement. Tagged outputs are linked to the original trace, audit log, and cost record — full context. | ☐ |
| 9 | A subset of feedback-tagged outputs is reviewed regularly and migrated into the eval set ‖ Evaluation grows toward production reality over time. Without this discipline, the eval set captures the system the team built originally; with it, the eval set captures the system in production today. | ☐ |
| 10 | Quality dashboards sit alongside availability dashboards; AI-specific SLOs are defined alongside classical SLOs ‖ The signals the team operates on include both. A system that's 100% available and producing wrong answers is broken; the dashboards reflect that, not just the mechanical signals. | ☐ |

---

## Related

[`technology/devops`](../../technology/devops) | [`ai-native/architecture`](../architecture) | [`ai-native/rag`](../rag) | [`ai-native/security`](../security) | [`ai-native/ethics`](../ethics) | [`patterns/data`](../../patterns/data)

---

## References

1. [OpenTelemetry — GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — *opentelemetry.io*
2. [OpenTelemetry — Distributed Tracing](https://opentelemetry.io/docs/concepts/signals/traces/) — *opentelemetry.io*
3. [Evidently AI](https://www.evidentlyai.com/) — *evidentlyai.com*
4. [Arize Phoenix](https://phoenix.arize.com/) — *arize.com*
5. [LangSmith](https://docs.smith.langchain.com/) — *smith.langchain.com*
6. [Helicone](https://www.helicone.ai/) — *helicone.ai*
7. [Langfuse](https://langfuse.com/) — *langfuse.com*
8. [RAGAS](https://docs.ragas.io/) — *ragas.io*
9. [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — *NIST*
10. [Anthropic Engineering](https://www.anthropic.com/engineering) — *anthropic.com*
