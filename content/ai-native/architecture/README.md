# AI System Architecture

The architectural patterns that distinguish a working AI prototype from a production AI system — recognising that adding a model to an architecture changes the architecture's stability properties, cost profile, and failure modes in ways that don't appear in classical software engineering.

**Section:** `ai-native/` | **Subsection:** `architecture/`
**Alignment:** Anthropic Engineering | OpenAI Function Calling | LangGraph | NIST AI Risk Management Framework

---

## What "AI system architecture" actually means

A *prototype* AI architecture is the diagram from the demo — a model behind an API, a prompt template, a thin orchestration layer, and a working happy path. The prototype answers the question *can this work at all?* and the answer is usually yes, because foundation models are remarkable. The same architecture in production fails in ways the demo never surfaces: latency variance that breaks downstream timeouts, cost that scales nonlinearly with traffic, a stochastic core where the same input produces different outputs, an agent loop that runs forever when no action satisfies the goal, evaluation that nobody runs because writing tests for a probabilistic system is hard.

A *production* AI architecture is one where these failure modes have been designed for explicitly. The serving topology has documented latency and cost characteristics. The agentic loop has bounded steps, guardrails, and a way to fail safely when no plan resolves. The deterministic and stochastic regions of the system are named — what's deterministic stays deterministic, what's stochastic is contained. Prompts are versioned like code, with tests, regression suites, and a deployment cadence. Cost is a non-functional requirement with budgets and alerts. Evaluation is engineering — a continuously running suite of inputs whose outputs are scored, drift-checked, and gated against deployment.

The architectural shift is not "we added a model." It is: **AI introduces a stochastic core with non-trivial latency, cost, and failure properties — and the surrounding architecture must be designed to bound those properties, route around them, and measure them, rather than letting them propagate freely.**

---

## Six principles

### 1. The deterministic and stochastic regions of the system are named — and the boundary is small

Foundation models are stochastic: the same input can produce different outputs, errors are non-discrete (bad answer vs. wrong answer vs. plausible-but-incorrect answer), and the failure mode is rarely "exception thrown." Surrounding code is typically deterministic: same input, same output, errors are discrete, observability is straightforward. Mixing the two without architectural discipline produces a system where deterministic logic must somehow accommodate stochastic outputs, often by adding more stochastic logic — and the unpredictability propagates. The architectural response is to keep the stochastic surface small, routed, and bounded: the model is called once at the boundary, its output is parsed and validated against a schema, retries are bounded, and the rest of the system operates on validated structured data. Calls into the model are expensive and risky; calls out of the model produce schema-conformant deterministic objects that the rest of the system can reason about.

#### Architectural implications

- The boundary between stochastic (model calls) and deterministic (orchestration, parsing, business logic) is explicit in the code — not a convention, an architectural rule.
- Model outputs are parsed and validated against a schema before downstream code consumes them — JSON schemas, Pydantic models, Zod schemas, structured-output APIs (OpenAI's `response_format`, Anthropic's tool use, gemini's structured output).
- Retry and fallback logic at the boundary catches schema-conformance failures, content-policy refusals, and timeout — without these, a stochastic transient failure becomes a system-wide incident.
- The deterministic region of the system can be tested as classical software; the stochastic region needs evaluation as a separate discipline (see principle 6).

#### Quick test

> Pick a model call in your system. What happens if the model returns text that doesn't parse as the expected structure? If the answer is "the downstream code crashes" or "we don't know," the boundary between deterministic and stochastic is not architectural — it's incidental, and the failure mode is one bad output away.

#### Reference

[OpenAI — Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) and [Anthropic — Tool Use](https://docs.claude.com/en/docs/build-with-claude/tool-use) — the canonical references for constraining model output to a schema, which is the practical mechanism for narrowing the stochastic surface.

---

### 2. Serving topology is an architectural decision with cost, latency, and dependency consequences

Where a model runs is rarely a neutral choice. *API-hosted* foundation models (OpenAI, Anthropic, Google, Bedrock) trade per-token cost for zero infrastructure and the latest capabilities; the constraint is rate limits, vendor availability, and the inability to fine-tune the foundation. *Self-hosted* open-weight models (Llama, Mistral, Qwen, DeepSeek, on vLLM/TensorRT-LLM/Ray Serve) trade infrastructure work for cost predictability, data residency, and customisation; the constraint is GPU capacity, latency tail, and the operational burden. *Edge-deployed* models (smaller variants on-device or in CDN) trade capability for offline operation and latency floor; the constraint is model size and update cadence. *Hybrid* topologies route different workloads to different tiers based on sensitivity, latency budget, or cost. The architectural mistake is to default — picking the first option that works in the prototype and inheriting whatever consequences come — rather than choosing deliberately based on the workload's actual characteristics.

#### Architectural implications

- The serving choice for each AI surface in the system is documented with the trade-off: cost, latency, dependency risk, data-residency posture, and capability requirement.
- Workloads with mixed requirements (some sensitive, some not; some interactive, some batch) use multiple serving tiers with explicit routing — not a single tier as a compromise.
- API-hosted dependencies are treated as critical third-party services with monitoring, fallback, and SLAs; self-hosted infrastructure is treated as production infrastructure with capacity planning and runbooks.
- Inference cost is modelled per request (tokens-in × input-cost + tokens-out × output-cost) and aggregated to monthly budgets — without this, AI cost surprises arrive in the bill, not in the architecture.

#### Quick test

> Pick the most-used AI feature in your system. What's the per-request cost, the p95 latency, and the dependency risk profile of its serving tier? If those numbers don't exist, the serving topology is a default rather than a decision.

#### Reference

[vLLM](https://docs.vllm.ai/) for self-hosted serving with continuous batching; [Ray Serve](https://docs.ray.io/en/latest/serve/index.html) for the broader serving framework. For the architectural framing of cost and latency as design properties, [Anthropic Engineering](https://www.anthropic.com/engineering) publishes practical guidance on production deployment trade-offs.

---

### 3. Agentic systems need bounded loops, capability boundaries, and explicit failure modes

An agent — a system that uses a model to choose actions in pursuit of a goal — is an architectural primitive with properties classical orchestration does not have. A traditional workflow has a fixed graph; an agent has a graph the model decides at runtime. A traditional workflow halts on error; an agent reasons about errors and may loop forever trying alternative paths. A traditional workflow's actions are constrained by what's wired up; an agent's actions are constrained only by the tools its given access to. The ReAct pattern (Reason-Act-Observe) and its descendants in LangGraph, AutoGen, OpenAI's Assistants, and Anthropic's tool use describe the loop, but using the loop in production means designing its bounds: maximum steps, capability scope, escalation when no plan succeeds, audit of every action. Without these bounds, the agent is an open-ended process whose runtime cost, action history, and final state are all under the model's control rather than the system's.

#### Architectural implications

- Maximum agent loop steps are bounded — beyond N iterations, the loop halts with a documented escalation, not silent failure or runaway cost.
- Each tool the agent can call has documented preconditions, effects, and reversibility; destructive actions (deletes, financial moves, irreversible state changes) require additional confirmation or are simply outside agent scope.
- Every agent action is logged with the prompt that produced it, the tool called, the inputs supplied, the result observed — an audit trail at the action level, not just at the request level.
- Failure modes are designed for: tool failure, content-policy refusal, infinite-loop detection, budget exhaustion — each has a defined response that doesn't depend on the agent recovering.

#### Quick test

> Pick the most autonomous agentic workflow in your system. What's the maximum number of steps it can take before halting, and what happens at step N+1? If the answer is "we haven't measured" or "it just keeps trying," the loop is unbounded — and the failure mode is a runaway cost or a corrupted state, not a clean halt.

#### Reference

[ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) — the canonical reference for the reason-act-observe loop. [LangGraph](https://langchain-ai.github.io/langgraph/) provides a graph-based framing of agent state machines that makes the bounded-loop discipline explicit.

---

### 4. Prompts are code — versioned, tested, reviewed, deployed

A prompt is the executable specification of a model's behaviour for a given task. Treating it as a string in a config file produces the same outcome as treating SQL queries as strings in a config file: silent breakage on changes nobody reviewed, no test coverage, no rollback path, no idea which version is in production. The discipline is to treat prompts as source code: under version control, with test coverage (a regression suite of inputs whose expected behaviours are checked), peer-reviewed before merge, deployed in stages, and monitored after release. Prompt engineering frameworks (DSPy, LangChain's PromptTemplates, the structured prompt patterns in Anthropic's documentation) provide the technical scaffolding; the discipline is the engineering practice around them.

#### Architectural implications

- Prompts live in version control with the application code or in a dedicated prompt-management system; not in databases, environment variables, or admin UIs without revision control.
- A regression suite of representative inputs runs against every prompt change — outputs are scored automatically (against rubrics, against reference outputs, by another model judging quality) and changes that regress are blocked.
- Prompts are deployed in stages with canary or shadow traffic when the change is significant, not flipped atomically across all production traffic.
- The prompt and the model version that produced an output are recorded with the output — without this, debugging "why did the system answer this way?" requires reconstructing state that's already gone.

#### Quick test

> Pick a production prompt in your system. Where is it stored, what tests run against it, and which version of the model is it tied to? If the prompt is a string in a config table edited by anyone with write access, the system has no source-of-truth for its own behaviour.

#### Reference

[Anthropic — Prompt Engineering](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview) and [DSPy](https://dspy.ai/) — the former for the engineering practice, the latter for the framework that treats prompts as compiled artefacts with declarative inputs and optimised modules.

---

### 5. Inference cost is a non-functional requirement with budgets, alerts, and architectural levers

A user interaction with a foundation model costs money — not abstractly, but per request, with the total visible on the monthly bill. At small scale this is a curiosity; at production scale it becomes the dominant cost line item, often exceeding compute and storage combined. The architectural levers are well-understood: model selection (smaller model for easier tasks, larger only when needed), context shaping (smaller prompts, summarisation, retrieval scoping), caching (semantic cache on prompts, KV cache on tokens), batch sizing for throughput, fine-tuning to reduce required context for repeated tasks. The discipline is to treat inference cost as a non-functional requirement — with a budget, monitored continuously, alerted on threshold, and revisited when patterns change — not as something noticed in the next finance review.

#### Architectural implications

- Per-request cost is computed and logged with every model call; aggregate cost is observable in real time, not at month-end reconciliation.
- Budget alerts fire before they hurt: warning at 70% of monthly budget, critical at 90%, with documented response actions (rate-limit, escalate, throttle non-essential features).
- Architectural levers are deliberately chosen: a routing layer that sends easy queries to small models and hard queries to large ones; semantic caching on prompts that recur; context shaping that strips redundant content before sending.
- Cost is reviewed alongside latency and quality as the AI service's NFRs — not as an after-the-fact concern.

#### Quick test

> Pick the highest-volume AI feature in your system. What's its monthly cost, what's the cost per user interaction, and what's the architectural lever you'd pull if cost doubled tomorrow? If those answers don't exist, cost is a discovered fact, not a managed property.

#### Reference

[OpenAI — Pricing](https://openai.com/api/pricing/) and [Anthropic — Pricing](https://www.anthropic.com/pricing) are the unit-cost references; the architectural framing of inference cost as an NFR is treated in detail in [Anthropic Engineering](https://www.anthropic.com/engineering)'s production deployment guides and in [OpenAI's cookbook](https://cookbook.openai.com/) on production patterns.

---

### 6. Evaluation is engineering — a continuous discipline, not a launch milestone

Classical software has tests: deterministic inputs, expected outputs, automated assertions. AI systems have evaluations: representative inputs, scored outputs, distributional assessments. The two are different in kind. A test is a binary pass/fail on a specific case; an evaluation is a measurement of behaviour across a population of cases, with statistical comparison between versions. Evaluations are the only honest way to answer the question *did this change make the system better or worse?* — without them, "the new prompt seems good" is the team's evidence base. The discipline is to build the evaluation suite alongside the system: representative inputs (the held-out set), scoring rubrics (deterministic where possible, model-graded where not), regression detection (is this version worse than the prior one?), and gating (is this change safe to deploy?).

#### Architectural implications

- An evaluation suite exists, runs continuously, and is treated as engineering infrastructure — not a one-time deliverable.
- Held-out inputs are representative of production traffic, refreshed periodically, and protected from contamination (not used in prompt iteration loops without care).
- Output scoring uses multiple methods: deterministic rules where possible (regex, structured comparison), model-graded scoring where not (with the judge model documented and validated), human review on a sample for ground truth.
- Regression detection compares versions on the suite and gates deployment — a change that worsens any critical metric beyond a threshold is blocked, not approved with "we'll watch it."

#### Quick test

> Pick a recent change to a prompt or model in your system. What evaluation suite ran against it, what metrics moved, and what threshold gated the deployment? If the answer is "we tried it on a few examples and it looked good," the change is being deployed on vibes — and the next regression will surface in production rather than in the eval.

#### Reference

[Anthropic — Evals](https://docs.claude.com/en/docs/test-and-evaluate) and [OpenAI — Evals](https://platform.openai.com/docs/guides/evals) — the canonical practical references. For RAG-specific evaluation, [RAGAS](https://docs.ragas.io/) provides a multi-metric framework that exemplifies the multi-axis evaluation discipline this principle requires.

---

## Architecture Diagram

The diagram below shows a canonical production AI system: the deterministic-stochastic boundary made explicit; serving topology with a mix of API-hosted and self-hosted models; an agentic state machine with bounded loops and tool boundaries; a prompt management layer with versioning; a continuous evaluation pipeline gating deployments; cost telemetry feeding budgets.

---

## Common pitfalls when adopting AI architecture thinking

### ⚠️ The unbounded agent

An agent loop is deployed without step limits because "it should converge." It doesn't always converge. A pathological input causes it to loop indefinitely, calling tools, accruing cost, and never producing output. The first sign is the cost alert at 3 AM.

#### What to do instead

Maximum step count on every agent loop. Documented escalation when the limit is hit (return partial result with status, alert humans, log full trace). Budget caps per request, not just per month. The default for an agentic system is *bounded*, with unbounded as the explicit configuration choice.

---

### ⚠️ Prompts as untracked configuration

Prompts live in a database table edited by anyone with admin access. A change last Tuesday is regressing quality this week. Reproducing the bug requires figuring out what the prompt was at the time the bug occurred, but the table doesn't track history. The system has lost its own source-of-truth.

#### What to do instead

Prompts in version control alongside the code that uses them, or in a dedicated prompt-management system with full history, diffs, and rollback. Every model output records the prompt version and model version that produced it. Reverting a regression is a one-line change with a deploy, not an archaeology project.

---

### ⚠️ Cost surprise

The team uses the largest model for everything because "it's the best." The bill at month-end is several times what was projected. Investigation reveals 90% of traffic was easy queries that a smaller, cheaper model would have handled at the same quality.

#### What to do instead

Routing layer that sends queries to the smallest model that handles them well, with the larger model reserved for queries the small one routes up. Continuous cost monitoring per feature, with alerts. Periodic A/B tests on whether the larger model's quality improvement justifies its cost on a specific workload.

---

### ⚠️ The eval set that doesn't represent production

The evaluation set was built during prototyping with cases the team hand-picked. Production traffic looks different — different domains, different lengths, different mix. The eval scores are great; production quality is mediocre. The eval set has measured a system that resembles the prototype, not the deployed one.

#### What to do instead

Eval set is constructed from representative production traffic (sampled and reviewed for safety/PII), refreshed periodically as traffic patterns shift, and explicitly guarded from contamination. The eval set's representativeness is itself a property to monitor — if production drift exceeds the eval set's coverage, the eval set needs updating.

---

### ⚠️ Stochasticity propagating into deterministic logic

The model returns text. Downstream code parses it loosely, accepting near-misses. When the model's output drifts (different phrasing, different structure), the parser silently accepts wrong values. The system continues to operate, producing wrong outputs, and the failure is invisible until users complain.

#### What to do instead

Strict schema validation at the model boundary. Model output that doesn't conform to the schema is treated as an error — retry, fallback, or fail loudly. The downstream code consumes only validated structured data, not "whatever the parser could extract." The boundary is sharp, by design.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | The boundary between deterministic and stochastic code is explicit; model outputs are schema-validated before downstream consumption ‖ The stochastic surface is small, routed, and bounded. Downstream code reasons about validated structured data, not about whatever text the model produced. Schema validation failures retry or fall back deliberately. | ☐ |
| 2 | Serving topology is documented per AI surface — cost, latency, dependency risk, data residency ‖ The choice of API-hosted, self-hosted, edge, or hybrid is deliberate, with named trade-offs. Multiple tiers route by workload characteristics, not by which option appeared first in the prototype. | ☐ |
| 3 | Agent loops are bounded — maximum steps, tool capability scope, audit trail per action ‖ The default is bounded, with unbounded as explicit configuration. Tools have documented preconditions and reversibility; destructive actions have additional confirmation. Every action is logged at the action level. | ☐ |
| 4 | Prompts are version-controlled with regression test coverage and staged deployment ‖ Prompts are source code: stored in version control, peer-reviewed, regression-tested against representative inputs, deployed in stages. Every output records the prompt version and model version that produced it. | ☐ |
| 5 | Inference cost is treated as a non-functional requirement with per-request logging, budgets, and alerts ‖ Per-request cost is observable in real time. Budget alerts fire before incidents. Architectural levers (routing, caching, context shaping) are exercised based on observed patterns, not as one-time optimisations. | ☐ |
| 6 | Routing across model sizes is implemented where workload diversity justifies it ‖ Easy queries go to small/cheap models; hard queries escalate to large/expensive ones. The routing layer is observable and tuneable; A/B tests evaluate whether quality differences justify cost differences on the actual traffic. | ☐ |
| 7 | A continuous evaluation suite gates prompt and model changes ‖ Eval set is representative of production. Scoring uses multiple methods. Regression detection is automated. Changes that regress critical metrics are blocked at deployment, not approved with "we'll watch it." | ☐ |
| 8 | Caching strategies (semantic cache, KV cache, response cache) are deliberate where the workload supports them ‖ Caching reduces cost and latency where queries recur; the cache layer is observable and tuneable. Cache hits and their consequences (stale data, leaked context) are monitored. | ☐ |
| 9 | Documented failure modes for stochastic-core failures: model unavailable, content-policy refusal, schema-conformance failure, rate limit ‖ Each failure mode has a defined response that doesn't depend on the model recovering. Fallbacks (smaller model, cached response, deterministic alternative, graceful degradation) are tested before production needs them. | ☐ |
| 10 | The AI service has SLOs distinct from classical service SLOs — including quality, hallucination rate, and cost-per-interaction ‖ Latency and availability alone do not capture AI-system health. Quality scores, refusal rates, drift indicators, and cost per interaction are tracked alongside the classical signals. | ☐ |

---

## Related

[`principles/ai-native`](../../principles/ai-native) | [`ai-native/monitoring`](../monitoring) | [`ai-native/rag`](../rag) | [`ai-native/security`](../security) | [`ai-native/ethics`](../ethics) | [`system-design/edge-ai`](../../system-design/edge-ai)

---

## References

1. [Anthropic Engineering](https://www.anthropic.com/engineering) — *anthropic.com*
2. [OpenAI — Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) — *platform.openai.com*
3. [Anthropic — Tool Use](https://docs.claude.com/en/docs/build-with-claude/tool-use) — *docs.claude.com*
4. [ReAct: Synergizing Reasoning and Acting (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) — *arXiv*
5. [LangGraph](https://langchain-ai.github.io/langgraph/) — *langchain-ai.github.io*
6. [vLLM](https://docs.vllm.ai/) — *docs.vllm.ai*
7. [Ray Serve](https://docs.ray.io/en/latest/serve/index.html) — *ray.io*
8. [DSPy](https://dspy.ai/) — *dspy.ai*
9. [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — *NIST*
10. [Anthropic — Prompt Engineering](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview) — *docs.claude.com*
