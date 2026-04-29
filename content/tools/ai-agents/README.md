# AI Agents Tooling

The architectural concerns of using AI agents as engineering tools — recognising that agents are a deterministic-uncertain hybrid whose tool-use surface, sandbox boundaries, observability, idempotency, and human-in-the-loop checkpoints determine whether they accelerate engineering work or accumulate as a category of failures the team didn't know how to debug.

**Section:** `tools/` | **Subsection:** `ai-agents/`
**Alignment:** Anthropic Building Effective Agents | ReAct (Yao et al.) | Anthropic Tool Use | Model Context Protocol (MCP)

---

## What "AI agents tooling" means — and how it differs from "AI-native architecture"

This page is about AI agents *as engineering tools* — the agents that engineers run to do development work (plan a refactor, generate boilerplate, modify a config across many files, draft a deploy runbook, scaffold a service). The architectural concerns of *building production systems with AI inside* — RAG, monitoring, ethics, security, edge inference — live in the [`ai-native/`](../../ai-native) section. That section covers AI-as-architecture. This page covers AI-as-tooling: agents the engineering team uses, with their own architectural properties as tools.

A *primitive* approach to AI agents treats them as autocomplete with extra steps: prompt the model, paste the answer into the codebase, hope it's correct. This works for trivial cases (boilerplate generation, one-line refactors) and fails at scale: the agent's tool-use surface isn't constrained, so it can do things the engineer didn't authorise; the agent's actions aren't observable, so debugging "why did it produce this output?" requires reconstructing the conversation; the agent isn't idempotent, so re-running the same task produces different results; high-stakes actions (deploys, data deletion, credential changes) happen without checkpoints. The agent works until it doesn't, and when it doesn't, the team has no debugging surface.

A *production* approach treats agents as designed tools with documented properties. *Tool-use surface* — what tools the agent can invoke (file reads, file writes, shell commands, API calls, deploys) — is enumerated and constrained by privilege; tools the agent doesn't need aren't exposed; tools that are dangerous (rm, deploy, drop database) require human confirmation. *Sandbox boundaries* — what the agent can affect — are explicit (this filesystem path, this network destination, this credential scope). *Observability* — every agent action is logged with reasoning, tool call, parameters, result; the run is reconstructable post-hoc from the trace. *Idempotency and reversibility* — agents can retry, replay, or be re-run safely; destructive actions have rollback paths. *Human-in-the-loop checkpoints* — high-stakes or irreversible actions require explicit confirmation; the agent presents the plan and waits, rather than executing autonomously. The agent becomes a tool the team can trust because they can constrain it, observe it, and recover from its mistakes.

The architectural shift is not "we use Claude/GPT to write code." It is: **AI agents are deterministic-uncertain hybrids whose tool-use surface, sandbox boundaries, observability, idempotency, and human-in-the-loop checkpoints determine whether they're trusted engineering tools or unobserved automation accumulating risk — and treating agents as autocomplete-with-extra-steps produces a category of failures whose debugging surface the team will need to design retroactively.**

---

## Six principles

### 1. Agents are deterministic-uncertain hybrids — review and test patterns differ from deterministic code

A traditional code function is deterministic: same input, same output. A traditional model is deterministic-with-noise: same input, similar output (with sampling variance). An agent is *deterministic-uncertain*: the agent's reasoning loop produces the same KIND of output (plan, tool calls, response) on repeated runs, but the SPECIFIC output varies — the plan may have different steps, the tool calls may be different, the response may be phrased differently or even reach a different conclusion. The architectural implication: review and test patterns that work for deterministic code don't work for agents. Reviewing one agent run and assuming the next will behave identically is wrong; testing by replaying recorded prompts is brittle; mocking the model in tests removes the property being tested. The discipline is to design for the deterministic-uncertain property: review the agent's *contract* (what tools it uses, what guardrails apply, what observability emits) rather than the specific output of one run; test the system with the agent in the loop, not just the agent in isolation; rely on observability of actual runs to detect drift, rather than expecting test suites to catch agent behaviour changes.

#### Architectural implications

- The agent's *contract* is documented separately from its prompt: what tools it has access to, what sandbox bounds it operates in, what guardrails apply, what observability it emits. The contract is what's reviewed, not the prompt itself.
- Review focuses on the contract and the system's response to agent behaviour: are the guardrails sufficient, is the observability complete, are the human-in-the-loop checkpoints in the right places?
- Tests exercise the system *with the agent in the loop* — given representative inputs, does the agent's output cause the system to behave correctly? Mocking the agent removes the property being tested.
- Production observability detects drift: agents whose behaviour changes (because the model was updated, because tools were added, because the prompt evolved) surface their changes in the metrics — error rates on agent-driven tasks, time-to-completion, escalation rates to human review.

#### Quick test

> Pick the most-used agent in your organisation. Is its contract documented separately from its prompt? Are tests written against the system with the agent in the loop, or against the agent in isolation? If the answer is "we test the prompt," the testing is operating on a target whose behaviour will drift, and the next prompt or model update will produce changes the tests don't catch.

#### Reference

[Anthropic Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) treats the deterministic-uncertain property as a primary design concern, with patterns for managing it. [ReAct (Yao et al.)](https://arxiv.org/abs/2210.03629) provides the canonical reasoning-and-acting framework that underpins most modern agent architectures, with the loop structure that makes outputs uncertain even when the contract is fixed.

---

### 2. Tool-use surface is the architectural decision — what the agent can do defines what the agent can do wrong

The most consequential architectural decision in agent design is *which tools the agent can invoke*. An agent with read-only access to a filesystem can summarise code but can't modify it. An agent with shell-execute access can run any command available to its execution context — including destructive ones. An agent with deploy access can ship to production. The tool-use surface is the *capability boundary*: the agent can do anything the surface permits and nothing it doesn't. The architectural discipline is to enumerate the tool surface deliberately, scope each tool to least privilege, document the rationale for each tool the agent has access to, and treat the addition of a new tool as a deliberate architectural change — not an incremental convenience that gets added when an engineer thinks "it would be easier if the agent could just do X."

#### Architectural implications

- The agent's tool-use surface is documented: what tools, what scope per tool (read-only filesystem of /workspace, shell commands within sandbox container, API calls to specific endpoints), what authentication the tools use, what rate limits apply.
- Each tool is scoped to least privilege: a tool for "read code" doesn't include "write code"; a tool for "list files" doesn't include "delete files"; a tool for "query API" doesn't include "POST to API."
- Adding a new tool is treated as an architectural change with review: what does this enable, what does it expose, what guardrails are needed, what observability needs to emit.
- The Model Context Protocol (MCP) standardises tool exposure across models and platforms, making the tool surface portable and reviewable.

#### Quick test

> Pick the agent that has the broadest tool surface in your organisation. Enumerate its tools and the scope of each. Are there tools whose scope is broader than the agent actually needs (full filesystem when only /workspace is needed; full shell when only specific commands are needed)? If yes, the agent is over-privileged — and the next time it does something unexpected, the impact will be bounded by the over-privileged scope rather than by the actual need.

#### Reference

[Anthropic Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) covers tool-use surface design at framework level. [Anthropic Model Context Protocol (MCP)](https://modelcontextprotocol.io/) standardises the tool-exposure layer, making the surface portable and reviewable. [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) and [LangChain Agents](https://python.langchain.com/docs/concepts/agents/) provide alternative tool-exposure frameworks with similar architectural concerns.

---

### 3. Sandbox boundaries and execution privilege are explicit, not assumed

An agent that runs in the engineer's local shell with the engineer's credentials inherits everything the engineer can do — including production access, package installs, network egress, persistent file writes outside the working directory. This is convenient (the engineer can run the agent freely) and dangerous (the agent's mistakes are bounded by the engineer's privilege, which is typically broader than the agent needs). The architectural discipline is to define the agent's *execution sandbox* explicitly: what filesystem paths it can read and write, what network destinations it can reach, what credentials it has access to, what processes it can spawn. The sandbox is enforced at the layer below the agent — by container, by VM, by capability-based isolation, by file permissions — not by the agent's own self-restraint. An agent with self-imposed restraint follows the restraint until it doesn't; an agent with externally-imposed sandbox can't violate the sandbox even if it tries.

#### Architectural implications

- The agent's sandbox is defined at the execution layer (container, VM, sandboxed shell) — not by trusting the agent to honour boundaries.
- Filesystem access is scoped: the agent has a working directory and can read/write within it, with explicit list of paths it can access outside (config files, source code, output directory) and clear deny for everything else.
- Network access is scoped: the agent can reach specified hosts/ports for tool APIs, package indexes if needed, but not arbitrary internet — preventing exfiltration even if the agent's prompt is compromised.
- Credentials are scoped: the agent has access to credentials for specific API endpoints, with appropriate rate limits and audit trails — not to arbitrary credentials in the engineer's environment.

#### Quick test

> Pick an agent your team uses for engineering work. What's its sandbox — what filesystem paths, what network destinations, what credentials, what processes? If the answer is "it runs as me in my shell with everything I can access," the agent's blast radius is the engineer's full privilege, and the next mistake (or prompt injection) compounds with that scope.

#### Reference

The sandbox-boundaries discipline is treated in [Anthropic Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) at architectural level. Container-based agent sandboxes, capability-based execution, and seccomp-style filtering are the operational layers that enforce boundaries; specific implementations vary by platform but the architectural principle is consistent.

---

### 4. Observability for agent runs — every action logged with reasoning, tool call, parameters, result

A traditional code function's behaviour is debugged by reading the code. An agent's behaviour can't be debugged that way: the code is the agent loop, but the *behaviour* is the specific reasoning chain on the specific input, which doesn't survive the run. The architectural discipline is *full-fidelity observability of agent runs*: every reasoning step, every tool call with its parameters, every tool result, every state transition is logged. The trace is reconstructable post-hoc — given the run ID, the engineer can replay what the agent thought, what it did, what happened, and where it went wrong (or right). Without this observability, "why did the agent do X?" is unanswerable; with it, debugging an agent's mistake is similar to debugging any other production incident.

#### Architectural implications

- Every agent run produces a structured trace: the input prompt, the system prompt and tool definitions, each reasoning step with its content, each tool call with its parameters, each tool result, the final output, all timestamped and correlated by run ID.
- The trace is queryable: filtering by user, by agent, by tool, by outcome (success/failure/escalation) — operational analysis of agent behaviour at scale.
- Sensitive content in traces (credentials, PII) is redacted at logging time, following the same security-surface discipline as any other observability data ([`observability/logs`](../../observability/logs)).
- Trace retention matches investigation needs: hot for recent runs (last week), warm for historical (last quarter), with cost matching the access pattern.

#### Quick test

> Pick a recent agent-driven task in your organisation that produced an unexpected result. Can you reconstruct what the agent did, with what reasoning, calling what tools with what parameters? If the answer is "we have the prompt and the output but not the steps in between," the agent's behaviour is opaque — and the next unexpected result will be similarly undebuggable.

#### Reference

The observability discipline for agent runs maps directly to general distributed tracing ([`observability/traces`](../../observability/traces)): each agent reasoning step is a span, tool calls are spans within the agent span, the trace context propagates through tool invocations. Modern agent platforms (LangSmith, Anthropic's tooling, OpenAI's tracing) operationalise this; the architectural discipline applies regardless of platform.

---

### 5. Idempotency and reversibility — agents may retry, replay, or be re-run safely

Agents fail. The model returns an error mid-task, the tool call times out, the engineer cancels the run partway through. The agent's design either tolerates these conditions (re-run produces consistent state; partial completion is detectable; reversal is feasible) or doesn't (re-run produces duplicate state; partial completion leaves the system in inconsistent state; reversal requires manual reconciliation). The architectural discipline is the same idempotency-and-reversibility discipline that applies to any operational tool, but with an extra dimension: agents may *internally* retry — when a tool call fails, the agent's reasoning loop may decide to try again, possibly with different parameters. The agent's tool calls must be idempotent (retrying a write doesn't double-write; retrying a delete doesn't error on already-deleted) for the agent's own retry behaviour to be safe.

#### Architectural implications

- Tools the agent invokes are idempotent: a write specifies the desired final state rather than an incremental change; a delete is a no-op if the target doesn't exist; a create includes an idempotency key.
- The agent's task framing supports re-run: tasks are described as desired outcomes ("ensure config X has value Y") rather than incremental actions ("add line Z to config X"), so re-running produces consistent state.
- Destructive actions have explicit reversal paths: drops have backups, deploys have rollback, file modifications can be undone. The reversibility is documented and exercised before relying on it.
- Partial completion is detectable: an agent that runs for ten steps and gets cancelled at step 7 leaves visible artefacts of what was done (logs, trace, files written) so the engineer can resume or roll back deliberately.

#### Quick test

> Pick a multi-step task you've recently run an agent for. If the agent had been interrupted at step 3 of 5, what would the system look like — recoverable, partially-broken, or in an inconsistent state nobody could clean up without root? If the answer is the latter, the agent's task is operating on the assumption that interruption won't happen, and the next interruption will discover what's actually true.

#### Reference

The idempotency discipline transfers from [`runbooks/migration`](../../runbooks/migration) and [`runbooks/rollback`](../../runbooks/rollback). [Idempotence (Wikipedia)](https://en.wikipedia.org/wiki/Idempotence) covers the formal property; [Anthropic Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) covers the agent-specific implications including internal retry behaviour.

---

### 6. Human-in-the-loop checkpoints — irreversible or high-stakes actions require explicit confirmation

An agent that can autonomously run any action it decides to take is operating without checkpoints. Most actions are fine; the rare action that's irreversible or high-stakes is the one that produces the incident. The architectural discipline is to identify which actions are *irreversible* (rm -rf, drop database, send-email-to-customer, deploy-to-production, delete-account) or *high-stakes* (any action with significant blast radius or regulatory implication) and to require *human confirmation* before execution. The agent presents its plan, the engineer reviews and approves (or rejects, or modifies), and only then does the action proceed. The discipline costs friction (the engineer can't fully delegate; some workflows require active engagement) but pays the friction back in the avoided category of incidents — agents that autonomously executed an action they shouldn't have.

#### Architectural implications

- Actions are classified by reversibility and stakes: routine (autonomous), confirmable (require human approval), restricted (require multi-party approval or are entirely off-limits to the agent).
- The classification is documented per tool: each tool the agent can invoke has its action class stated, with the confirmation requirement enforced at the tool layer, not by trusting the agent to ask.
- Confirmation flows are ergonomic: the agent presents the plan with enough context for the engineer to evaluate, the approve/reject is a clear interaction, and there's an audit trail of who approved what.
- The classification is revisited when the agent's surface or the system changes: an action that was routine in a low-stakes environment may become confirmable when the agent moves to production-touching contexts.

#### Quick test

> Pick the highest-stakes action your agents can perform. Does it require human confirmation, or does the agent perform it autonomously? If autonomous, what's the safeguard against the agent doing it incorrectly — a guardrail in the prompt? If the safeguard is in the prompt, the safeguard is as reliable as the agent's prompt-following, which is not 100%. The next prompt-injection or model-update is one step away from the agent autonomously executing an action it shouldn't.

#### Reference

[Anthropic Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) treats human-in-the-loop checkpoint design as a primary architectural concern, with patterns for when to require confirmation and how to design the confirmation flow ergonomically. The principle generalises beyond agents: any automation whose actions are irreversible benefits from the same checkpoint discipline.

---

## Developer-Agent Collaboration Sequence

The diagram below shows the canonical interaction sequence between developer, agent, tools, and the system the agent operates on: the developer defines the task and provides context; the agent plans and presents the plan for review; on approval the agent executes via tools (each tool call observable in the trace); high-stakes actions trigger explicit human-in-the-loop checkpoints; verification at completion confirms the outcome matches the intent.

---

## Common pitfalls when adopting AI-agent-tooling thinking

### ⚠️ Agents reviewed as if they were deterministic code

The team reviews one agent run, sees it works, ships the integration. The next run behaves differently. The review caught the specific output, not the property the agent has of varying its outputs.

#### What to do instead

Review the agent's contract — tools, sandbox, guardrails, observability, checkpoints — not the specific output of one run. Test the system with the agent in the loop. Rely on production observability to detect drift.

---

### ⚠️ Tool-use surface that grows by convenience

Tools get added when an engineer thinks "it would be easier if the agent could do X." The cumulative tool surface is broader than any single use case requires. The agent's blast radius keeps growing without explicit decisions.

#### What to do instead

Each new tool treated as an architectural change with review. Least-privilege scope per tool. Documented rationale. Tools that aren't actively used get removed.

---

### ⚠️ Agent runs in engineer's shell with full privilege

The agent inherits everything the engineer can do. A mistake or prompt injection has the engineer's full blast radius. The sandbox is "trust the agent to behave."

#### What to do instead

Sandbox enforced at execution layer — container, VM, capability-based isolation. Filesystem, network, credentials all scoped. The sandbox can't be violated by the agent even if it tries.

---

### ⚠️ Agent behaviour is opaque post-run

The agent did something. The output exists. What it did and why isn't reconstructable. Debugging an unexpected result is impossible because the steps that produced it weren't logged.

#### What to do instead

Full-fidelity observability: every reasoning step, every tool call with parameters, every result, all logged with run ID. Trace is queryable post-hoc. Sensitive content redacted. Retention matches investigation needs.

---

### ⚠️ High-stakes actions performed autonomously

The agent can deploy, delete, modify production state, send customer emails — all without human confirmation. The safeguard is "the prompt tells it to be careful." The first prompt-injection or unexpected reasoning chain produces the incident.

#### What to do instead

Action classification: routine (autonomous), confirmable (human approval), restricted (off-limits). Enforcement at the tool layer, not in the prompt. Ergonomic confirmation flows with audit trails.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | The agent's contract is documented separately from its prompt — tools, sandbox, guardrails, observability, checkpoints ‖ Review focuses on the contract, not the specific output of one run. The contract is what's reviewed; the prompt is implementation detail. | ☐ |
| 2 | Tests exercise the system with the agent in the loop, not the agent in isolation ‖ Mocking the agent removes the property being tested. End-to-end tests with representative inputs validate that the system handles the agent's deterministic-uncertain output. | ☐ |
| 3 | The agent's tool-use surface is enumerated with documented rationale and least-privilege scope per tool ‖ Read-only when read-only is sufficient; specific endpoints when general API access isn't needed. Adding a tool is an architectural change with review. | ☐ |
| 4 | Tool exposure follows a standard (MCP, function calling, equivalent) for portability and reviewability ‖ The tool layer is portable across models and platforms. The standard makes the surface visible, auditable, and recomposable. | ☐ |
| 5 | The agent's sandbox is enforced at the execution layer — container, VM, capability isolation — not by the agent's self-restraint ‖ Filesystem, network, credentials all scoped. The sandbox cannot be violated by the agent even if it tries. | ☐ |
| 6 | Every agent run produces a structured trace — reasoning steps, tool calls with parameters, results — queryable by run ID ‖ Behaviour is reconstructable post-hoc. Sensitive content redacted. Retention matches investigation needs. | ☐ |
| 7 | Tools the agent invokes are idempotent — retry-safe, no-op on already-done ‖ The agent's internal retry behaviour is safe. Re-running tasks produces consistent state. Partial completion is detectable. | ☐ |
| 8 | Tasks are framed as desired outcomes, not incremental actions ‖ "Ensure X is in state Y" rather than "do action Z." Re-run produces consistent state. Idempotency is a property of the task framing, not just the tool. | ☐ |
| 9 | Actions are classified by reversibility and stakes — routine, confirmable, restricted ‖ Classification documented per tool. Enforcement at the tool layer. The classification is revisited when surface or context changes. | ☐ |
| 10 | High-stakes or irreversible actions require explicit human-in-the-loop confirmation with audit trail ‖ Agent presents plan; engineer reviews; only on approval does the action execute. The confirmation is in the tool layer, not the prompt. | ☐ |

---

## Related

[`tools/cli`](../cli) | [`tools/scripts`](../scripts) | [`tools/validators`](../validators) | [`ai-native/architecture`](../../ai-native/architecture) | [`ai-native/security`](../../ai-native/security) | [`observability/traces`](../../observability/traces)

---

## References

1. [Anthropic Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — *anthropic.com*
2. [Anthropic Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) — *docs.anthropic.com*
3. [Anthropic Model Context Protocol (MCP)](https://modelcontextprotocol.io/) — *modelcontextprotocol.io*
4. [ReAct (Reasoning and Acting)](https://arxiv.org/abs/2210.03629) — *arxiv.org*
5. [Toolformer (Schick et al.)](https://arxiv.org/abs/2302.04761) — *arxiv.org*
6. [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) — *platform.openai.com*
7. [LangChain Agents](https://python.langchain.com/docs/concepts/agents/) — *python.langchain.com*
8. [Idempotence (Wikipedia)](https://en.wikipedia.org/wiki/Idempotence) — *Wikipedia*
9. [OWASP — AI Security and Privacy Guide](https://owasp.org/www-project-ai-security-and-privacy-guide/) — *owasp.org*
10. [Distributed Systems Observability (Cindy Sridharan)](https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/) — *oreilly.com*
