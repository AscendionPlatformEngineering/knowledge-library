# AI-Native Principles

Architecture for systems where AI is a first-class component — not a bolted-on feature.

**Section:** `principles/` | **Subsection:** `ai-native/`
**Alignment:** TOGAF ADM | NIST AI RMF | ISO/IEC 42001 | AWS Well-Architected ML Lens

---

## What "AI-native" actually means

An *AI-augmented* system adds an AI feature to an otherwise traditional architecture: a chatbot stitched onto a CRM, a "summarize" button next to a document viewer, a classifier sitting in front of an inbox. The underlying system would still function if the AI feature were removed.

An *AI-native* system treats model behaviour as part of the system's contract. The architecture accepts that outputs are stochastic, reasoning is part of the request path, and evaluation is continuous rather than periodic. Stochastic means involving chance or probability, with its primary synonyms being random, probabilistic, aleatory, chance-based, and unpredictable. It describes processes that are not deterministic, often characterized by variability, uncertainty, or a random sequence of events. The model, prompt, retrieval index, and evaluation harness are first-class architectural artifacts with their own lifecycles — governed with the same rigour as code and infrastructure.

The architectural shift is not "we use AI somewhere." It is: **what we build now has stochastic components in its critical path, and the architecture must be honest about that.**

---

## Six principles

### 1. Stochasticity is a contract, not an exception

Models do not return the same output twice. The architecture must accept this rather than fight it. Don't assert single outputs; assert distributions, invariants, or bounds.

#### Architectural implications

- Caching keys must include enough context to avoid false hits, but not so much that hit rates collapse.
- Idempotency keys for AI-mediated operations need explicit semantics — replaying the same request should not re-roll the model.
- Retry semantics must distinguish "transient failure" (network, rate limit) from "model gave a different answer" (not retryable in the same sense).
- Public API contracts should describe what the system *commits to*, not what the model happens to return today.

#### Quick test

> If your test suite asserts `assertEqual(actual, "the dog ran")`, you are not architecting for stochasticity.

#### Reference

Anthropic's research on Constitutional AI ([Bai et al., 2022](https://arxiv.org/abs/2212.08073)) and OpenAI's work on calibrated sampling demonstrate why deterministic-output thinking fails for autoregressive models. The architectural pattern of asserting on distributions and invariants is codified in the **NIST AI RMF** Measure 2.7 (test, evaluate, validate).

---

### 2. Evals are tests, and tests are evals

Traditional unit tests cannot catch hallucination, refusal, drift, or prompt injection. Eval pipelines must run continuously — not at release time, but on every change to a prompt, retrieval index, model, or downstream tool definition.

#### Architectural implications

- Eval harness is a first-class CI/CD component with its own SLAs and on-call.
- Eval datasets are versioned artifacts with provenance, not test fixtures buried in a repo.
- Quality gates block deployments based on eval thresholds, not just unit-test pass rates.
- Production traffic feeds back into eval datasets through an explicit, governed loop.

#### Quick test

> If a prompt change ships to production without an eval signal, you do not have AI-native quality engineering.

#### Reference

Stanford's HELM benchmark ([Liang et al., 2022](https://arxiv.org/abs/2211.09110)) establishes that LLM behaviour cannot be characterized by a single test; it requires multi-dimensional, continuously-updated evaluation. The **AWS Well-Architected ML Lens** REL-3 codifies this as continuous quality monitoring rather than point-in-time validation.

---

### 3. Confidence and abstention are valid outputs

A system that always answers, even when it doesn't know, is a system that confidently lies. The architecture must make space for low-confidence paths: human handoff, fallback responses, or explicit "I don't have enough context to answer."

#### Architectural implications

- Every AI-mediated response carries a confidence signal — even if internal.
- Abstention paths are designed in advance, not retrofitted after the first incident.
- Human-in-the-loop handoff is a normal flow, not an emergency backup.
- The product surface accommodates uncertainty: "I'm not sure, here's what I'd check next" is a feature, not a defect.

#### Quick test

> If your system has no path that ends in "I don't know," it is engineered to be confidently wrong.

#### Reference

Calibration research by [Hendrycks & Gimpel (2017)](https://arxiv.org/abs/1610.02136) and the selective-prediction work of [Kamath et al. (2020)](https://arxiv.org/abs/2006.09462) show that abstention paths measurably improve real-world reliability over force-an-answer designs. **NIST AI RMF** Govern 3.2 explicitly requires documented abstention and escalation paths for high-stakes decisions.

---

### 4. Prompts are code; retrieval indexes are databases

Prompts and retrieval indexes shape model behaviour as directly as application code shapes traditional system behaviour. Treat them with the same operational rigour.

#### Architectural implications

- Prompts live in version control and go through code review.
- Prompt changes are deployments, with eval gates and rollback paths.
- Prompt registries (with metadata: owner, version, eval scores) replace ad-hoc prompt strings in config files.
- Indexes have schemas, migration paths, and freshness SLAs.
- Reindexing is a planned operation with capacity, cost, and quality implications.
- Embedding-model changes are treated as breaking changes — old vectors are not compatible with new models.

#### Quick test

> If "we tweaked the prompt" is not a deployment event in your change-management system, your prompts are not architected.

#### Reference

The "promptware" pattern is documented in [Lilian Weng's prompt engineering survey](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) and operationalized in **AWS Bedrock Prompt Management** as well as the **OpenAI Cookbook** patterns for versioned prompts. Treating retrieval indexes as databases is articulated in the [Pinecone production-RAG guide](https://www.pinecone.io/learn/series/rag/) and Anthropic's [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) post.

---

### 5. Token economics shape the architecture

The cloud-native cost model breaks at the inference layer. Token cost scales with input length, retrieval breadth, model size, and request rate in ways CPU/memory pricing did not. Caching, prompt compression, and model tiering are not optimizations — they're foundational architectural decisions.

#### Architectural implications

- Model tiering is the default: small models for routing, classification, and high-volume tasks; large models reserved for complex reasoning.
- Caching is designed in from day one: prompt-level, retrieval-level, and full-response caching, each with explicit invalidation semantics.
- Cost telemetry is a first-class observability signal alongside latency and error rate.
- Architectural reviews include a token budget per request type, with alerts on budget breaches.

#### Quick test

> If you cannot answer "what does this AI feature cost per 1,000 requests?", you have not architected for token economics.

#### Reference

The token-economics framing is laid out in the **AWS Well-Architected ML Lens — Cost Optimization** pillar and in [a16z's "16 changes to the way enterprises are building and buying generative AI"](https://a16z.com/generative-ai-enterprise-2024/). Model tiering and caching as foundational decisions are documented in the [OpenAI Cookbook caching patterns](https://cookbook.openai.com) and **Anthropic's prompt caching** technical guide.

---

### 6. AI failure modes are structurally distinct

Prompt injection, training-data leak, jailbreaking, model drift, and capability regression. The threat model differs meaningfully from traditional services. Security architecture for AI is its own discipline — treating it as "regular AppSec plus content filtering" is insufficient.

#### Architectural implications

- Threat-model AI surfaces specifically: untrusted input → model → tools/data is a different attack chain than untrusted input → application logic.
- Guardrails (input filtering, output classification, tool-use restriction) are architectural components, not just middleware.
- Capability boundaries — what the AI is allowed to do, what it must escalate, what it must refuse — are explicit in the design, not emergent from the prompt.
- Drift monitoring runs continuously; capability regression on a model upgrade is treated as a P1 risk.

#### Quick test

> If your AI security review reads like a web AppSec checklist with "and check the prompt" appended, the threat model has not been redone.

#### Reference

The **OWASP Top 10 for LLM Applications** and **MITRE ATLAS** (Adversarial Threat Landscape for AI Systems) provide the canonical AI threat taxonomy. **NIST AI RMF** Govern 4.1 and Manage 4.1 require explicit AI-specific threat modelling, distinct from generic AppSec. Prompt injection as a distinct attack class is detailed in [Greshake et al., 2023](https://arxiv.org/abs/2302.12173).

---

## Architecture Diagram

The diagram below shows the architectural concerns of an AI-native system as distinct layers — Reasoning, Knowledge, and Trust — each with its own ownership, lifecycle, and failure modes.

---

## Common pitfalls when adopting AI-native thinking

### ⚠️ The chatbot trap

Declaring a system AI-native because it has a chat interface, while the architecture underneath is unchanged from the pre-AI era. The chat surface is the visible part; AI-native is about the contract underneath.

#### What to do instead

Audit the system below the chat surface. If the persistence layer, evaluation harness, prompt versioning, and abstention paths are unchanged from the pre-AI design, the chat is decoration. AI-native means the architecture itself accounts for stochastic behaviour — not that there's a chat box on the homepage.

---

### ⚠️ The eval gap

Strong testing infrastructure for traditional features and "we'll know if it's bad" for AI features. This invariably means: production users discover the bad outputs first, and you find out in support tickets.

#### What to do instead

Stand up an eval harness on the same critical-infrastructure footing as your CI/CD. Versioned datasets, automated runs on every prompt or model change, regression alerts. The signal that catches a bad model upgrade should be a dashboard, not a customer email.

---

### ⚠️ The prompt-in-config anti-pattern

Burying critical model behaviour in YAML files outside any review process. A prompt that determines what your system tells customers should be reviewed at least as carefully as the function that returns the price.

#### What to do instead

Move prompts into a registry with version control, ownership metadata, and CI-gated changes. Every prompt change becomes a deployable artifact with eval scores attached. **AWS Bedrock Prompt Management** and Anthropic's prompt-versioning patterns codify this approach.

---

### ⚠️ The deterministic API illusion

Designing public APIs that promise consistent outputs over a stochastic system. This works until it doesn't, and the failure is loud — a customer notices that the same request returns different answers and loses trust in the entire product.

#### What to do instead

Design the API contract around what the system *commits to* — schema, freshness, confidence range, abstention conditions — rather than what the model happens to say. If the consumer needs determinism, that's a caching decision, not an API claim.

---

### ⚠️ Evaluating only at release time

Treating evals as a pre-launch milestone rather than a continuous signal. By the time your monthly eval review catches the regression, you have already shipped weeks of degraded quality.

#### What to do instead

Run evals on every prompt change, every retrieval-index update, every model-version bump, every tool-definition change. Production traffic feeds back into eval datasets through a governed loop. Continuous evaluation is to AI-native what continuous integration was to web architecture.

---

## Adoption checklist

Use this checklist when reviewing whether a system is genuinely AI-native or merely AI-augmented.

| # | Criterion | |
|---|---|---|
| 1 | "Good output" is specified in measurable, evaluable terms — not just sample outputs that look fine. ‖ "Looks fine" doesn't survive edge cases or model upgrades. Define success as measurable properties: factual accuracy on a benchmark, refusal rates on out-of-scope queries, token-bounded responses, schema compliance. If you can't write a CI test that fails when output regresses, you don't have a contract — you have a vibe. | ☐ |
| 2 | Every AI-mediated operation has a defined low-confidence path: abstention, fallback, or human handoff. ‖ When the model is uncertain, what happens? Without a defined path, the system silently produces confidently wrong answers. Build the abstention path first: "I don't know" beats hallucination; deterministic fallback beats both. Human handoff is the highest-stakes safety net — design it before you need it. | ☐ |
| 3 | Prompt changes go through review and eval gates before reaching production. ‖ Prompts are code. A four-word change can flip behaviour across thousands of edge cases. Treat prompts like database migrations: versioned, reviewed, tested against a regression suite, deployed through the same pipelines as application code. Free-text edits in production is how teams break things invisibly. | ☐ |
| 4 | Retrieval index has a schema, freshness SLA, and migration playbook. ‖ The retrieval index is a database with stochastic queries on top. It needs schema discipline (what shape of chunks?), freshness guarantees (how stale before retrieval is wrong?), and migration plans (changing embedding models is a re-index, not a config flip). Treat it like a Postgres replica, not a folder of PDFs. | ☐ |
| 5 | Per-request token budget is defined, monitored, and alerted on. ‖ Tokens are CPU cycles you pay for in real money. Without per-request budgets, a single prompt-injection or recursive tool call can drain a quarterly budget overnight. Define the ceiling, monitor consumption distributions, alert on tail spikes. Cost is now an architectural concern, not a finance one. | ☐ |
| 6 | AI surface is specifically threat-modelled (not just standard AppSec). ‖ Prompt injection, jailbreaks, training-data poisoning, model exfiltration, RAG context corruption — these don't appear in a standard OWASP review. Run a threat model with OWASP Top 10 for LLMs and MITRE ATLAS as references. If your AI security review reads like a web AppSec checklist with "and check the prompt" appended, the threat model hasn't been redone. | ☐ |
| 7 | Eval pipelines run on every prompt / index / model / tool change. ‖ Evals are the AI equivalent of unit tests. They run automatically on every change: new prompt version, re-indexed corpus, upgraded model, modified tool. Without continuous eval, regressions appear in production as user complaints. With it, regressions appear in CI as failed builds — like every other engineering discipline. | ☐ |
| 8 | Public API contracts describe what the system commits to, not what the model happens to return. ‖ An API that returns "whatever the model said" has no contract. Public contracts describe shape (schema), bounds (length, latency, cost), and behavioural invariants (refusal of out-of-scope queries) — properties the system enforces regardless of what the underlying model does. The model is an implementation detail. | ☐ |
| 9 | Model tiering (small for routing, large for reasoning) is implemented or explicitly deferred. ‖ Using a frontier model for every operation is the AI equivalent of running a Postgres query for every cache lookup — it works, expensively. Tier the models: small for classification and routing, large for actual reasoning. If you've chosen not to tier (early stage, simple use case), document why so future engineers don't repeat the analysis. | ☐ |
| 10 | The system has a defined response to capability regression on a model upgrade. ‖ Model upgrades silently break some use cases — capabilities that worked at v3 may regress at v4. Without a defined response (rollback path, eval gate, gradual rollout), you discover regressions by reading customer complaints. Treat model upgrades like database migrations: gated by tests, reversible, monitored. | ☐ |

A system that scores below 7/10 here is AI-augmented, not AI-native. That is sometimes the right choice — but it should be a deliberate one.

---

## Related

[`patterns/data`](../../patterns/data) | [`ai/architecture`](../../ai/architecture) | [`ai/security`](../../ai/security) | [`ai/monitoring`](../../ai/monitoring) | [`nfr/reliability`](../../nfr/reliability) | [`security/authentication-authorization`](../../security/authentication-authorization)

---

## References

1. [NIST AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/itl/ai-risk-management-framework) — *nist.gov*
2. [ISO/IEC 42001:2023 — AI Management System (Microsoft compliance overview)](https://learn.microsoft.com/en-us/compliance/regulatory/offering-iso-42001) — *Microsoft Learn*
3. [AWS Well-Architected Machine Learning Lens](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html) — *aws.amazon.com*
4. [Designing Machine Learning Systems — Chip Huyen's notes](https://huyenchip.com/2022/06/03/mlops-stack.html) — *huyenchip.com*
5. [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — *owasp.org*
6. [Anthropic — Engineering Reliable LLM Applications](https://www.anthropic.com/engineering) — *anthropic.com*
