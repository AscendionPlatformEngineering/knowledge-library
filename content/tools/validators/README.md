# Validators

The architecture of validators as gates that produce pass/fail outcomes on inputs — recognising that validator design (multi-layer coverage from schema through semantic and policy, placement at appropriate stages, actionable failure messages, evolution as the system evolves, and false-positive discipline) is what determines whether validators function as trusted gates or as ceremonial checks the team learns to bypass.

**Section:** `tools/` | **Subsection:** `validators/`
**Alignment:** JSON Schema | OpenAPI | Open Policy Agent (OPA) | Pact (contract testing)

---

## What "validators" actually means — and how they differ from checklists

This page is about validators as *machine-applied gates*. A validator takes input — a JSON document, a code change, a configuration file, an HTTP request, a deployment manifest — and produces a binary outcome: *pass* (the input meets the validator's criteria) or *fail* (the input doesn't, with a specific reason). The discipline of *human-applied* review instruments — the architecture-review checklist, the deployment-readiness checklist, the security-review checklist — lives in [`checklists/`](../../checklists). Checklists are applied by humans during deliberate review work; validators are applied by machines as automatic gates. Same family (gating instruments), different operational mode.

A *primitive* validator is what gets added when "we keep getting bad input": a single regex check, a hardcoded length validation, a presence-of-required-field check. It catches the specific cases that motivated it and misses everything else. Worse, primitive validators frequently produce *unhelpful failure messages*: "Validation failed" or "Invalid input" — telling the consumer that something is wrong but not what or how to fix it. The result is validators that exist but don't help: consumers learn to rely on guess-and-check rather than on the validator's signal, the validator becomes ceremonial, and eventually it gets bypassed for "edge cases" that proliferate.

A *production* validator architecture treats validation as a *layered, multi-stage discipline*. *Schema validation* — does the input have the expected structure (required fields present, types correct, format constraints met)? *Semantic validation* — does the input make sense given the system's domain rules (this field's value is in the allowed range, this combination of fields is consistent, this reference resolves to a real thing)? *Policy validation* — does the input comply with operational policies (security constraints, regulatory requirements, organisational standards)? *Contract validation* — at boundaries between systems, does the input match the agreed-upon contract (API specification, message schema, interface definition)? Each layer is independent, each can be implemented and updated separately, and each contributes to the overall coverage.

Beyond layering, validators are *placed at appropriate stages*: pre-commit (linters, formatters, schema checks before code is shared); CI (semantic checks, contract tests, security scans before merge); deploy (configuration validators, dependency checks before production); runtime (request validation, response validation as production traffic flows). Each stage has different latency budgets and different failure costs. Failed validation is *actionable*: error messages explain what's wrong, where (file, line, field), and how to fix it. The validator is *trusted* because it doesn't produce false positives that erode confidence; consumers respect its signal because the signal is reliable.

The architectural shift is not "we have validators." It is: **validators are machine-applied gates whose layered coverage, stage placement, message actionability, evolution discipline, and false-positive rate determine whether they function as trusted gates that prevent bad inputs from reaching production or as ceremonial checks the team learns to bypass — and the difference compounds in the incidents that bypassed validation didn't catch.**

---

## Six principles

### 1. Validators are gates with pass/fail outcomes — not advice, not warnings, not soft signals

The most consequential property of a validator is whether its output *binds*. A validator that produces "warnings" the team can ignore, or "advice" the team can override, or "soft signals" with no enforcement isn't a gate — it's a hint. Hints are useful; gates are different. The architectural distinction is *what the validator's output forces*: pass means the input proceeds; fail means the input doesn't. Failed validation halts the pipeline, blocks the merge, rejects the request, refuses the deploy. The discipline pays the friction cost (consumers can't ship past a failed validator) and pays the friction back in the bad inputs that don't reach production. A validator whose output can be ignored is a validator the team will eventually ignore — and the failures it was meant to prevent will surface in production rather than at the gate.

#### Architectural implications

- Each validator's output is binding: pass allows the input to proceed; fail halts it. The decision is binary; there's no "validator advised against this but the team chose to proceed" path that doesn't require explicit override.
- Override paths exist for specific, exceptional cases — a documented mechanism with audit trail (who overrode, when, why, with what authority) — but are not the default mode of operating around the validator.
- A pattern of overrides on a specific validator is a calibration signal: either the validator is producing false positives (revise) or the team is taking risks the validator was meant to prevent (training/process issue, or the validator was mis-calibrated).
- Validators that produce "warnings" rather than gates are recognised as hints; they're useful but separate from the gate layer.

#### Quick test

> Pick the most-used validator in your organisation. What does failure mean — does it block the merge / deploy / request, or does it produce a warning the team can ignore? If the latter, the validator is a hint, not a gate — and the failures it would catch will eventually surface in production.

#### Reference

[OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) treats validation as gating discipline at framework level. [Open Policy Agent (OPA)](https://www.openpolicyagent.org/docs/latest/policy-language/) operationalises policy validation as binding gates with documented override paths.

---

### 2. Multi-layer validation — schema, semantic, policy, contract are independent concerns

A validator that conflates layers fails predictably. A validator that checks "the field `age` is present and is an integer" handles schema validation but misses semantic validation (`age = -5` passes schema but is semantically nonsense) and policy validation (`age = 200` passes both but violates business policy that ages must be plausible). A validator that mixes all three together becomes complex, slow to evolve, and hard to debug when it fails in unexpected ways. The architectural discipline is *layered validation* with each layer independent: *schema* (structure, types, required fields, format constraints) using a schema language ([JSON Schema](https://json-schema.org/), [Protobuf](https://protobuf.dev/), [Pydantic](https://docs.pydantic.dev/), [OpenAPI](https://www.openapis.org/)); *semantic* (domain rules: ranges, consistency, reference resolution) in code closer to the domain; *policy* (organisational/regulatory rules) in a policy engine ([OPA Rego](https://www.openpolicyagent.org/docs/latest/policy-language/), [Conftest](https://www.conftest.dev/)); *contract* (cross-system agreements) using contract testing ([Pact](https://pact.io/)) or schema validation against a published API spec. Each layer can be implemented, evolved, and debugged independently.

#### Architectural implications

- Schema validation is implemented in a schema language with first-class tooling (auto-generated validators, IDE support, documentation generation) — not in hand-written if-statements.
- Semantic validation lives in domain code, called after schema validation passes — the domain code can assume the structure is valid and focus on domain-specific rules.
- Policy validation lives in a policy engine separate from application code — policies can be authored, reviewed, and updated by people other than application engineers (security team, compliance team).
- Contract validation lives at boundaries between systems with the contract as the artefact — published API specs, contract tests, message schemas. Both sides of the boundary validate against the same contract.

#### Quick test

> Pick a critical input path in your organisation (an API endpoint, a config file, a deployment manifest). What's its schema validator, what's its semantic validator, what's its policy validator? If the answer is "we have one validator that checks everything," the layering is conflated — and changes to any layer require touching all layers.

#### Reference

[JSON Schema](https://json-schema.org/) is the canonical schema language for JSON; [OpenAPI](https://www.openapis.org/) extends it for HTTP API contracts; [Protobuf](https://protobuf.dev/) provides schema for binary protocols. [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) operationalises policy validation with a dedicated policy language. [Pact](https://pact.io/) operationalises consumer-driven contract testing.

---

### 3. Validator placement matches stage — pre-commit, CI, deploy, runtime have different budgets and costs

A validator that takes 30 seconds is fine in CI (where many checks run in parallel) and prohibitive at runtime (where it adds latency to every request). A validator that requires production credentials can't run pre-commit (where it would mean every developer has those credentials). A validator that catches data-shape issues belongs at the boundary where the data enters the system, not deep inside business logic. The architectural discipline is *stage-appropriate placement*: each validator runs at the earliest stage where it has the inputs it needs and where its latency cost is acceptable. *Pre-commit*: linters, formatters, fast schema checks (sub-second budget, runs on developer's machine). *CI*: semantic checks, contract tests, security scans (minutes-budget, runs on shared infrastructure). *Deploy*: configuration validators, dependency checks, infrastructure-as-code policy checks (deploy-window budget). *Runtime*: request validation, response validation, rate-limit enforcement (sub-millisecond budget, runs in production). Validators at the wrong stage are either too slow (runtime validator with CI-scale work) or too late (runtime validator catching what should have been caught pre-commit).

#### Architectural implications

- Each validator is placed at the earliest stage where it has its inputs and where its latency cost is acceptable.
- Pre-commit validators are fast (sub-second), runnable by developers, and don't require production credentials or external services.
- CI validators have minutes-scale budgets and can run heavier checks: full schema validation, contract tests, security scans, integration tests.
- Deploy validators run during the deploy gate ([`checklists/deployment`](../../checklists/deployment)): infrastructure policy checks, configuration validators, dependency vulnerability scans.
- Runtime validators are sub-millisecond, validate every request against the published API contract, and reject malformed inputs before they reach business logic.

#### Quick test

> Pick the slowest validator in your CI pipeline. What does it check, and could the same check run pre-commit? If yes, the validator is placed too late — every PR pays the CI latency for a check that could have run on the developer's machine before the PR was opened.

#### Reference

[12-Factor App](https://12factor.net/) (Factor V: Build, Release, Run) covers the stage separation that validators map to. [Conftest](https://www.conftest.dev/) operationalises policy validation at deploy time for infrastructure-as-code. [OpenAPI](https://www.openapis.org/) and [Schemathesis](https://schemathesis.readthedocs.io/) provide runtime validation against published API contracts.

---

### 4. Failure messages are actionable — what's wrong, where, how to fix it

A validator that fails with "Validation failed" tells the consumer that something is wrong without saying what. The consumer's response is to read the source, reverse-engineer what was expected, guess at the fix, and try again. Multiple iterations later, the consumer either gets it right or gives up. The architectural discipline is *actionable failure messages*: every failed validation produces a message that includes (1) *what's wrong* — the specific rule that was violated, in language a consumer can understand; (2) *where* — file path, line number, field name, request element — so the consumer can locate the offending input; (3) *how to fix it* — the expected format/value/structure, with examples where possible. The discipline pays compound returns: validators with actionable messages are trusted because consumers can act on them; validators with cryptic messages are bypassed because acting on them is too costly.

#### Architectural implications

- Every failure message includes the rule that was violated, expressed in terms the consumer can understand (not the validator's internal vocabulary).
- The failure includes location: file/line for static inputs, field path for structured inputs, request identifier for runtime inputs.
- Where possible, the message includes the expected format/value/structure as part of the error: "expected `age` to be an integer between 0 and 120, got `'old'`" rather than "type error."
- For complex validations (policy violations, semantic failures), the message links to documentation explaining the rule, why it exists, and how to comply.

#### Quick test

> Pick a recent validation failure in your organisation. Did the failure message tell the consumer (a) what's wrong, (b) where, and (c) how to fix it? If any of those are missing, the consumer paid a discovery cost on top of the fix cost — and the next consumer hitting the same failure pays the same cost again.

#### Reference

[Pydantic](https://docs.pydantic.dev/) is a canonical example of actionable validation messages in the Python ecosystem; its error messages include field paths, expected types, and observed values. The principle generalises across validation frameworks: actionable messages are a UX feature that compounds with use.

---

### 5. Validators evolve as the system evolves — schemas change, rules change, calibration follows

A schema authored two years ago doesn't necessarily reflect the current system. New fields have been added to the data, new policies have been adopted by the organisation, new constraints have emerged from the domain. A validator that doesn't evolve with the system either rejects valid inputs (false positives, eroding trust) or accepts invalid inputs (false negatives, the failures the validator was supposed to prevent). The architectural discipline is to treat validators as *living artefacts*: schemas have versions, evolution paths, and migration strategies; semantic rules are reviewed when domain rules change; policies are updated as organisational standards evolve; contracts are renegotiated when consumer-producer agreements change. The validator's evolution discipline matches the system's evolution rate — fast-evolving systems need validators that can be updated without ceremony; stable systems can have more deliberate validator evolution.

#### Architectural implications

- Schemas are versioned; consumers can specify which schema version they're using; producers maintain compatibility across version transitions until consumers migrate.
- Semantic and policy rules have documented owners and review cadences; rules are reviewed when domain or organisational changes warrant.
- Validator changes are tested against representative input corpora (recorded production traffic, golden examples, edge-case collections) before deploy — to catch regressions where a schema update suddenly rejects previously-valid input.
- The evolution path for breaking changes is documented: deprecation period, dual-validation period (both old and new accepted), removal of old validator. Consumers have time to migrate.

#### Quick test

> Pick a validator your organisation has used for over a year. When was it last revised, and what motivated the revision? If the answer is "we don't track that — it's been the same since it was written," the validator is operating on the assumption that the system hasn't changed. Either it's accepting input it shouldn't or rejecting input it should accept; in either case, the cost is being paid.

#### Reference

The schema-evolution discipline is treated in [Protobuf — Protocol Buffers](https://protobuf.dev/) (with explicit field-numbering and reserved-field rules to support evolution), [JSON Schema](https://json-schema.org/) (with `$id` versioning), and [OpenAPI](https://www.openapis.org/) (with API versioning patterns). The operational discipline transfers across schema languages.

---

### 6. False positives erode trust — validators that flag valid input get bypassed

The most insidious validator failure mode is the *false positive*: the validator rejects an input that's actually valid. A few false positives are tolerable; a steady rate of false positives erodes trust until consumers stop respecting the validator's output. They learn to override on every failure (because failures are usually false positives anyway), they bypass the validator for "exceptional cases" (which proliferate), or they reroute around the validator entirely. By the time a real defect hits the validator, the team's response is to override that too. The architectural discipline is to treat false positives as *defects* in the validator: every false positive triggers investigation (was the rule too strict? was the input class not anticipated? is the validator buggy?) and revision. The goal is a validator with a near-zero false-positive rate, even at the cost of accepting some false negatives — because trust is the resource the validator depends on, and false positives consume it faster than false negatives reveal themselves.

#### Architectural implications

- False positives are tracked: each override of a failed validation is recorded with reason; patterns of overrides are analysed for false-positive rate per validator.
- High false-positive rates trigger validator revision: refining the rule to be less strict, adding exception handling for the input class, fixing bugs in the validator implementation.
- The trade-off between false positives and false negatives is acknowledged: a near-zero-false-positive validator may have higher false-negative rate than an ideal validator; the trade-off is deliberate, not accidental.
- Validators with persistently high false-positive rates that can't be reduced are candidates for retirement: a validator that wrongly rejects 30% of valid inputs is doing more harm than good.

#### Quick test

> Pick the most-overridden validator in your organisation. What's its false-positive rate — how often do overrides indicate the validation was wrong rather than that the team chose to ship despite a real flag? If false positives are common and uninvestigated, the validator's trust is being eroded — and the team's habit of overriding on this validator transfers to others.

#### Reference

The false-positive discipline transfers from broader software-defect discipline; the same principle applies to alerting in observability (false-positive alerts erode trust) and to test suites (flaky tests are worse than failing tests because they erode trust in the suite). The architectural framing of "trust is the resource validators depend on" is treated implicitly in [Continuous Delivery — Humble & Farley](https://www.oreilly.com/library/view/continuous-delivery-reliable/9780321670250/) for build-pipeline gates.

---

## Multi-Stage Validation Pipeline

The diagram below shows the canonical placement of validators across the development-to-runtime pipeline: pre-commit (fast schema checks, linters, formatters), CI (semantic checks, contract tests, security scans), deploy (configuration validators, infrastructure policy checks), runtime (request/response validation, rate-limit enforcement). Each stage has its own latency budget and failure cost; validators are placed at the earliest stage where their inputs are available and their cost is acceptable.

---

## Common pitfalls when adopting validator thinking

### ⚠️ Validators that produce warnings instead of binding gates

Failures produce warnings the team can ignore. The team learns to ignore them. Bad inputs reach production despite the validator existing.

#### What to do instead

Binding gates: pass allows progress, fail halts. Override paths exist for documented exceptional cases with audit trail, but aren't the default mode. Patterns of overrides trigger calibration review.

---

### ⚠️ Conflated layers — schema, semantic, policy all in one validator

Hand-written if-statements check structure, business rules, and policy together. Changes to any layer require touching all layers. Failures in the conflated validator are hard to debug.

#### What to do instead

Layered validation: schema in a schema language (JSON Schema, Protobuf, Pydantic); semantic in domain code; policy in a policy engine (OPA); contract at boundaries (Pact, OpenAPI). Each layer independent.

---

### ⚠️ Validator at the wrong stage

A schema check that should run pre-commit runs in CI (slow feedback). A request validator that should run at runtime runs at startup (catches startup-time inputs but not request-time). The placement doesn't match the stage's properties.

#### What to do instead

Stage-appropriate placement: each validator runs at the earliest stage where its inputs are available and its latency is acceptable. Pre-commit fast and developer-machine-runnable; CI minutes-scale; runtime sub-millisecond.

---

### ⚠️ "Validation failed" messages

The validator rejects input but doesn't say what's wrong, where, or how to fix. The consumer guesses, iterates, eventually succeeds or gives up.

#### What to do instead

Actionable messages with three elements: what (the specific rule violated), where (file/line/field/request identifier), how to fix (expected format/value, with examples). For complex rules, link to documentation.

---

### ⚠️ Static validator disconnected from system evolution

The validator was written two years ago. The system has evolved. The validator now either rejects valid inputs (eroding trust) or accepts invalid ones (failing its purpose).

#### What to do instead

Validators as living artefacts: versioned schemas, documented owners and review cadences, evolution paths for breaking changes, testing against representative input corpora before deploy.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Validators produce binding pass/fail outcomes — fail halts the pipeline ‖ Override paths exist for exceptional cases with audit trail; not the default. Patterns of overrides trigger calibration review. | ☐ |
| 2 | Validation is layered — schema, semantic, policy, contract — each implemented independently ‖ Schema in a schema language; semantic in domain code; policy in a policy engine; contract at boundaries. Layers can be evolved separately. | ☐ |
| 3 | Schema validation uses a schema language with first-class tooling ‖ JSON Schema, Protobuf, Pydantic, OpenAPI — auto-generated validators, IDE support, documentation generation. Not hand-written if-statements. | ☐ |
| 4 | Policy validation lives in a policy engine separate from application code ‖ OPA, Conftest, equivalent. Policies authored by security/compliance teams; reviewed and updated separately from application code. | ☐ |
| 5 | Contract validation lives at boundaries with the contract as the artefact ‖ Both sides of the boundary validate against the same contract (OpenAPI spec, Pact contract, Protobuf schema). The contract is shared, versioned, and tested. | ☐ |
| 6 | Each validator is placed at the earliest stage where its inputs are available and latency is acceptable ‖ Pre-commit fast and local; CI minutes-scale; deploy at the deploy gate; runtime sub-millisecond. Misplaced validators are too slow or too late. | ☐ |
| 7 | Failure messages include what's wrong, where, and how to fix it ‖ The rule violated (in consumer-friendly language), location (file/line/field), expected format/value with examples. Links to documentation for complex rules. | ☐ |
| 8 | Schemas are versioned with documented evolution paths for breaking changes ‖ Deprecation period, dual-validation phase, removal of old. Consumers have time to migrate. The validator's evolution discipline matches the system's. | ☐ |
| 9 | Validator changes are tested against representative input corpora before deploy ‖ Recorded production traffic, golden examples, edge-case collections. Catches regressions where a schema update rejects previously-valid input. | ☐ |
| 10 | False positives are tracked and treated as defects ‖ Each override recorded with reason; patterns analysed; high false-positive rates trigger revision. Trust is the resource validators depend on; false positives consume it faster than false negatives reveal themselves. | ☐ |

---

## Related

[`tools/ai-agents`](../ai-agents) | [`tools/cli`](../cli) | [`tools/scripts`](../scripts) | [`checklists/security`](../../checklists/security) | [`security/application-security`](../../security/application-security) | [`technology/devops`](../../technology/devops)

---

## References

1. [JSON Schema](https://json-schema.org/) — *json-schema.org*
2. [OpenAPI Specification](https://www.openapis.org/) — *openapis.org*
3. [Protobuf — Protocol Buffers](https://protobuf.dev/) — *protobuf.dev*
4. [Pydantic — Python Validation](https://docs.pydantic.dev/) — *docs.pydantic.dev*
5. [Open Policy Agent (OPA) Rego](https://www.openpolicyagent.org/docs/latest/policy-language/) — *openpolicyagent.org*
6. [Conftest — Policy Testing](https://www.conftest.dev/) — *conftest.dev*
7. [Pact — Contract Testing](https://pact.io/) — *pact.io*
8. [Schemathesis — API Testing](https://schemathesis.readthedocs.io/) — *schemathesis.readthedocs.io*
9. [ESLint — JavaScript Linter](https://eslint.org/) — *eslint.org*
10. [ruff — Python Linter](https://docs.astral.sh/ruff/) — *docs.astral.sh*
