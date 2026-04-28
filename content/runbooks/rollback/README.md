# Rollback Runbook

The artefact that captures how to undo a change that's already been deployed — recognising that the rollback runbook is what makes forward velocity safe, that an untested rollback plan is no plan at all, and that the design of the rollback path is itself an architectural property of the change being rolled back.

**Section:** `runbooks/` | **Subsection:** `rollback/`
**Alignment:** Continuous Delivery (Humble & Farley) | Blue-Green Deployment (Martin Fowler) | Feature Flags (Martin Fowler) | Spinnaker

---

## What "rollback runbook" actually means

A *primitive* rollback approach is what most teams have until they don't: the deploy went out, something's wrong, somebody senior figures out how to roll back under pressure, the rollback either works or it doesn't, and the team learns whatever lessons it learns from the experience. Each rollback is bespoke; the institutional knowledge about *how* to roll back lives in individual heads; the next rollback under pressure is one resignation away from being attempted from scratch.

A *production* rollback runbook treats rollback as a designed, tested, documented capability — the precondition that makes forward velocity safe. The change being deployed is designed with its rollback path in mind: forward-only changes are recognised as forward-only and treated accordingly (more cautious deploys, more verification, more soak time), while reversible changes have explicit rollback paths that are exercised before the forward path is ever taken in production. Decision criteria for invoking rollback vs. forward-fix are documented and trained on. Modern delivery substrates — feature flags, blue-green deployments, canary releases — are treated as architectural rollback primitives rather than as deployment conveniences. The runbook captures the rollback path for a specific change or a specific class of changes, with executable steps, verification, and explicit handling of state-related concerns (data migrations, schema changes, side effects that can't be undone by reverting code).

The architectural shift is not "we wrote a rollback plan." It is: **rollback is the architectural property of a change that determines whether forward velocity is safe; the runbook is what makes that property operational; an untested rollback path is an aspiration, not a capability — and the difference between the two is paid for in incidents that didn't have to happen.**

---

## Six principles

### 1. Rollback discipline is the precondition of forward velocity — no rollback path means no safe forward path

A team with reliable rollback can deploy aggressively: the cost of deploying a bad change is bounded by detection time plus rollback time, and both can be made small. A team without reliable rollback has to deploy cautiously: every deploy is potentially permanent damage to the system or its data, and the team's natural response is to slow down — more review, more testing, more soak — none of which actually makes the deploys safer, just slower. The architectural insight is that *rollback discipline determines forward velocity*, not the other way around. Investing in reliable rollback paths produces compound returns: faster deploys, more deploys, more learning per unit time, less reliability tax paid in over-cautious release engineering. Treating rollback as an afterthought is treating velocity as an afterthought.

#### Architectural implications

- The rollback path for each class of change is treated as a first-class engineering concern — designed, tested, documented, and maintained as a property of the system, not as an emergency-only workflow.
- Changes that lack a tested rollback path are recognised as accumulating *forward risk* — each such change makes future changes incrementally riskier, because the rollback option is unavailable for them too.
- Investment in rollback infrastructure (feature flag systems, blue-green deployment platforms, schema-migration tooling that supports reversal) is recognised as investment in velocity, not as overhead.
- Lead time and deployment frequency (DORA metrics) are treated as functions of rollback reliability — a team with reliable rollback can sustainably ship faster than one without.

#### Quick test

> Pick the most-changed service in your organisation. What's its tested rollback path, and how long does rollback take from decision to completion? If the answer is "we figure it out when we need to" or "we don't have a tested rollback," the team's deployment caution is paying the rollback risk every time — and the velocity cost is being paid in slower deploys, more cautious changes, and the incidents that happen anyway.

#### Reference

[Continuous Delivery — Humble & Farley](https://www.oreilly.com/library/view/continuous-delivery-reliable/9780321670250/) treats rollback discipline as the architectural foundation of fast, safe delivery. [Accelerate — Forsgren, Humble, Kim](https://itrevolution.com/product/accelerate/) provides the empirical research showing that rollback reliability correlates with deployment frequency and lead time at scale.

---

### 2. The forward-only vs reversible choice is an architectural decision made deliberately

Not every change can be made reversible without significant cost. A schema migration that drops a column is forward-only; once data is gone, it's gone. A code deploy is typically reversible; reverting code is straightforward. A data migration may be reversible if the old data is preserved or forward-only if it's transformed in place. The architectural discipline is to recognise this choice as a *deliberate one* rather than letting it emerge by accident: for each change, the team decides whether to make it forward-only (with the implications: more cautious deploy, more verification, more soak time, no rollback option) or reversible (with the implications: scaffolding to maintain the rollback path, retention of old artefacts, dual-running infrastructure). The wrong default is to treat changes as reversible without designing for it; the team discovers at the moment rollback is needed that the path doesn't exist.

#### Architectural implications

- Each significant change documents its reversibility property explicitly — forward-only or reversible — with reasoning.
- Forward-only changes are deployed with additional caution: more soak time, more verification, more conservative percentage breakpoints during cutover, additional alerting.
- Reversible changes are deployed with the rollback infrastructure (feature flags, blue-green slots, retained old data) maintained until the change has soaked long enough that rollback is no longer expected to be needed.
- The choice is documented in change records (ADRs, deployment plans) so future engineers and operators understand the property of changes they inherit.

#### Quick test

> Pick a recent significant change in your organisation. Was the reversibility property documented as a deliberate architectural choice, or did the team discover it at the moment rollback was contemplated? If the latter, the discovery was made too late — and the cost of that lateness is paid in the rollback that didn't happen the way it should have.

#### Reference

[Database Refactoring — Ambler & Sadalage](https://martinfowler.com/books/refactoringDatabases.html) treats the forward-only-vs-reversible choice explicitly for database changes; the discipline transfers to general system changes. [Continuous Delivery — Humble & Farley](https://www.oreilly.com/library/view/continuous-delivery-reliable/9780321670250/) covers the architectural patterns (blue-green, feature flags, canary) that turn changes from accidentally-forward-only into deliberately-reversible.

---

### 3. The plan that's never tested doesn't work — exercising the rollback path is required, not optional

Rollback plans that exist only on paper fail at the moment they're needed. The plan assumed the old system was still running; it isn't. The plan assumed the old data was still accessible; it's been retention-aged out. The plan referenced a tool that's been deprecated; the team finds out under pressure. The plan worked once for a similar change two years ago; the system has evolved since. The architectural discipline is that the rollback path must be *exercised* — actually performed in non-production at minimum, ideally in production-like conditions, ideally in production itself during low-risk periods. Game days, where the team practices rollback on a deliberately-degraded environment, are the canonical pattern. Practiced rollbacks reveal the gaps in the plan that paper review never finds, and the practice itself builds the muscle memory that responders need when the rollback is real.

#### Architectural implications

- Rollback paths are exercised on a documented cadence — at minimum in non-production for each significant change, ideally in production-like staging, periodically in production during low-risk maintenance windows.
- Game days are scheduled for high-stakes systems: the team practices rolling back from a known good state to a prior state under realistic conditions, with timing measured.
- Rollback timing is measured: from decision to invoke rollback through to completed rollback, what's the wall-clock time? The metric drives rollback-path optimisation — slow rollbacks mean longer impact during real incidents.
- Untested rollback paths are flagged: a change shipped without an exercised rollback is itself a known risk, tracked and remediated.

#### Quick test

> Pick the most consequential change your organisation deployed in the last quarter. Was its rollback path exercised before the change went to production, or only available on paper? If only on paper, the change is shipping with an untested rollback — and the next time rollback is needed, the team will discover what the plan assumed that turned out not to be true.

#### Reference

[Chaos Engineering — Rosenthal et al.](https://www.oreilly.com/library/view/chaos-engineering/9781492043850/) and [Game Days (Google SRE)](https://sre.google/sre-book/testing-reliability/) cover the practitioner-level discipline of exercising failure and recovery paths under controlled conditions, with rollback as a primary use case. [Spinnaker](https://spinnaker.io/) operationalises automated rollback exercises as part of continuous delivery pipelines.

---

### 4. Decision criteria for rollback vs forward-fix are documented and trained on

When something's wrong in production, the team faces a choice: roll back to the prior state, or fix forward (deploy a fix that addresses the issue without reverting the underlying change). The right choice depends on factors: how confident is the team in the fix? How long will the forward fix take vs the rollback? Is the user impact severe enough that minimising current pain (rollback) outweighs avoiding repeat work (forward-fix)? Are there state implications (data already written by the new version) that make rollback complex? Without documented criteria, this decision runs on the most senior person's judgment in the room, which varies by who's in the room, time of day, and how confident they happen to be feeling. The architectural discipline is to document the criteria explicitly — when do we default to rollback, when do we default to forward-fix, what's the override authority — and to train responders on applying them, so the decision in the moment is principled rather than improvised.

#### Architectural implications

- Documented criteria for rollback-vs-forward-fix: severity thresholds where rollback is the default, conditions under which forward-fix may be preferred (small fix, high confidence, low user impact), explicit override authority for non-default choices.
- The criteria are trained on — responders know what the defaults are and what justifies an override before the moment they need to apply them.
- The decision is documented at the time it's made: which path was chosen, what justified the choice, what was the outcome. The record feeds into post-incident learning and criteria refinement.
- Forward-fix is recognised as carrying its own risk — a fix deployed under pressure may itself be wrong. The criteria account for this: forward-fix is the right call when the fix is genuinely simple and high-confidence, not just when rollback is inconvenient.

#### Quick test

> Pick a recent production incident that involved a deploy gone wrong. Was the rollback-vs-forward-fix decision made against documented criteria, or against the senior responder's judgment in the moment? If the latter, the decision quality varies with who's on call — and the same situation produces different outcomes with different responders.

#### Reference

[Google SRE Workbook](https://sre.google/workbook/) covers the rollback-vs-forward-fix decision at practitioner depth, including the documented-criteria discipline. [PagerDuty Incident Response](https://response.pagerduty.com/) treats the decision as a documented runbook concern with explicit criteria and decision authorities.

---

### 5. State considerations — data migrations, schema changes, and side effects complicate rollback

Code is the easy part of rollback: revert the deploy and the code is back to the prior state. State is the hard part. A change that wrote new fields to a database can't be fully undone by reverting code; the new fields persist. A schema migration that altered column types may not be cleanly reversible without data conversion. A change that emitted events to downstream systems can't unsend the events. The architectural discipline is to recognise these state implications during change design — not at rollback time — and to plan for them: backwards-compatible schema changes (columns added not modified or removed), feature flags that gate state-writing behaviour separately from code deploy, idempotent processing on the receiving side of events, dual-write patterns that keep the old store updated until the rollback window has passed. Rollback that ignores state implications produces inconsistent state — the code is back to v1 but the data is at v2 — which is often worse than either coherent state alone.

#### Architectural implications

- State implications of each change are documented before deploy: what state does the change write, can rollback restore the prior state, what scaffolding is needed to make rollback possible.
- Schema changes follow patterns that preserve rollback: additive changes (new columns, new tables) before destructive changes (drop column), with separate deploys; backwards-compatible reads on the new schema; phased deprecation of old schema after soak.
- Feature flags gate state-writing behaviour, so reverting a feature flag stops the new behaviour without requiring a code deploy and without leaving partial state.
- Side effects (events emitted, external API calls) are designed for idempotency on the receiving side, so re-emission after rollback doesn't compound the issue.

#### Quick test

> Pick a recent change in your organisation that wrote new state. Could rollback restore the prior state cleanly, or would rollback leave the system in an inconsistent code-vs-state position? If the latter, rollback for that change is itself a complex operation, and the runbook needs to handle it explicitly.

#### Reference

[Database Refactoring — Ambler & Sadalage](https://martinfowler.com/books/refactoringDatabases.html) is the canonical reference for state-aware change patterns. [Online Schema Migration — gh-ost](https://github.com/github/gh-ost) operationalises the state-preserving schema change pattern at scale.

---

### 6. Modern delivery substrates — feature flags, blue-green, canary — are architectural rollback primitives

A code deploy that has to be physically reverted to roll back is the slow, traditional path. Modern delivery substrates make rollback dramatically faster and lower-risk by design. *Feature flags* let new behaviour be turned off without a code deploy — rollback is a configuration change, takes seconds, no deploy pipeline involved. *Blue-green deployment* keeps the prior version running on a parallel slot — rollback is a load balancer or DNS switch back to the prior slot, takes seconds to minutes. *Canary releases* with automated rollback on bad signals catch problems before full rollout. The architectural discipline is to treat these substrates as rollback primitives rather than as deployment conveniences: the team that's invested in feature flags has rollback for feature-flag-gated changes that takes seconds; the team that's invested in blue-green has rollback for code changes that takes minutes. The investment is the architectural enabler; the rollback runbook describes how to use it.

#### Architectural implications

- Feature flags gate every change that can be feature-flag-gated, with the flag's rollback path documented (which flag to flip, expected behaviour after flip, verification).
- Blue-green deployment is the default deployment pattern for services where the cost of running a parallel slot is justified by the rollback speed it enables.
- Canary releases include automated rollback on bad signals — error rate above threshold, latency degradation, key correctness signal failure — without requiring human decision or intervention.
- The runbook describes the rollback path for each substrate: how to flip a flag, how to switch a blue-green slot, how to override a canary's automated decision.

#### Quick test

> Pick a recent rollback in your organisation. Was it accomplished through a substrate primitive (feature flag flip, blue-green switch, canary auto-rollback), or through a code-revert deploy? If the latter, rollback took minutes-to-hours rather than seconds-to-minutes — and the user impact during the rollback window scaled with that timing.

#### Reference

[Feature Flags — Martin Fowler](https://martinfowler.com/articles/feature-toggles.html) is the canonical reference for feature flags as architectural rollback primitives. [Blue-Green Deployment — Martin Fowler](https://martinfowler.com/bliki/BlueGreenDeployment.html) covers the parallel-slot pattern. [Canary Release — Martin Fowler](https://martinfowler.com/bliki/CanaryRelease.html) covers the progressive-rollout pattern. [Spinnaker](https://spinnaker.io/) and [Argo CD](https://argo-cd.readthedocs.io/) operationalise these patterns at platform level.

---

## Architecture Diagram

The diagram below shows the canonical rollback-runbook architecture: change classification (forward-only vs reversible) determines the deployment pattern; modern delivery substrates (feature flags, blue-green, canary) provide rollback primitives with associated speed and complexity; the rollback runbook captures the executable path for invoking rollback; decision criteria gate rollback-vs-forward-fix; state-aware patterns ensure rollback restores coherent state; rollback exercises validate the path before it's needed in production.

---

## Common pitfalls when adopting rollback-runbook thinking

### ⚠️ Rollback as afterthought

The team designs how to deploy forward, then bolts on a rollback section. At the moment rollback is needed, the bolted-on plan turns out to be infeasible.

#### What to do instead

Rollback path designed as part of the change, not after. Reversibility property documented explicitly. Scaffolding required for rollback (feature flags, blue-green slots, retained data) maintained through the soak window.

---

### ⚠️ Untested rollback path

The plan exists on paper. It's never been exercised. The first time it's invoked, the team discovers what the plan assumed that isn't true.

#### What to do instead

Rollback paths exercised on a documented cadence. Game days for high-stakes systems. Rollback timing measured. Untested paths flagged as risk and remediated.

---

### ⚠️ Decision by senior judgment in the room

When something goes wrong, the rollback-vs-forward-fix decision varies with who's on call. The same situation produces different outcomes with different responders.

#### What to do instead

Documented criteria for the decision. Trained on. Decision documented at the time, with reasoning, feeding into post-incident learning.

---

### ⚠️ State implications discovered at rollback time

The team rolls back the code. The data is in a state the old code doesn't expect. The system is now in inconsistent state — code is v1, data is v2 — and the situation is worse than either coherent state alone.

#### What to do instead

State implications documented at change design time. Backwards-compatible schema changes (additive before destructive). Feature flags gate state-writing behaviour. Side effects designed for idempotency on the receiving side.

---

### ⚠️ Code-revert as the only rollback mechanism

Every rollback requires a deploy. Rollback time is dominated by the deploy pipeline. The user impact window scales with deploy time.

#### What to do instead

Investment in modern delivery substrates: feature flags for seconds-scale rollback, blue-green for minutes-scale rollback, canary with automated rollback on bad signals. The runbook describes how to use each substrate's rollback primitive.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Each significant change documents its reversibility property explicitly — forward-only or reversible — with reasoning ‖ The choice is deliberate, not accidental. Forward-only changes are deployed more cautiously; reversible changes have the scaffolding maintained. | ☐ |
| 2 | Rollback paths are exercised before being needed in production ‖ Game days for high-stakes systems. Non-production exercises for routine changes. Rollback timing measured. The plan that's never tested doesn't work. | ☐ |
| 3 | Documented criteria for rollback-vs-forward-fix decisions ‖ Severity thresholds, override authority, training. Decision quality doesn't vary with who's on call. The decision in the moment is principled, not improvised. | ☐ |
| 4 | Each rollback decision is documented at the time it's made — path chosen, reasoning, outcome ‖ Feeds into post-incident learning. Refines criteria over time. The institutional record of rollback decisions improves the next decision. | ☐ |
| 5 | State implications of each change are documented before deploy ‖ What state does the change write, can rollback restore prior state, what scaffolding is needed. State considerations don't surface at rollback time. | ☐ |
| 6 | Schema changes follow patterns that preserve rollback — additive before destructive, with separate deploys ‖ Add columns before reading them; deprecate columns through stages; never alter or drop in a single change with the read-path change. The schema's rollback path is itself a designed property. | ☐ |
| 7 | Feature flags gate state-writing behaviour and other reversible changes ‖ Rollback is a configuration change, not a deploy. Seconds-scale rollback for flag-gated changes. The flag's rollback path is documented. | ☐ |
| 8 | Modern delivery substrates (blue-green, canary) are the default deployment pattern where their cost is justified ‖ Investment in substrate produces compound returns in rollback speed and reduced impact windows. The substrates are architectural primitives, not deployment conveniences. | ☐ |
| 9 | Canary releases include automated rollback on bad signals ‖ Error rate above threshold, latency degradation, key correctness signal failure — automated rollback without human decision required. Catches problems before full rollout. | ☐ |
| 10 | Lead time, deployment frequency, and change failure rate (DORA metrics) are tracked as functions of rollback reliability ‖ The metrics reveal whether rollback investment is paying compound returns in velocity. Rollback reliability is the architectural enabler of safe forward velocity. | ☐ |

---

## Related

[`runbooks/incident`](../incident) | [`runbooks/migration`](../migration) | [`technology/devops`](../../technology/devops) | [`patterns/data`](../../patterns/data) | [`observability/sli-slo`](../../observability/sli-slo) | [`system-design/scalable`](../../system-design/scalable)

---

## References

1. [Continuous Delivery (Humble & Farley)](https://www.oreilly.com/library/view/continuous-delivery-reliable/9780321670250/) — *oreilly.com*
2. [Feature Flags (Martin Fowler)](https://martinfowler.com/articles/feature-toggles.html) — *martinfowler.com*
3. [Blue-Green Deployment (Martin Fowler)](https://martinfowler.com/bliki/BlueGreenDeployment.html) — *martinfowler.com*
4. [Canary Release (Martin Fowler)](https://martinfowler.com/bliki/CanaryRelease.html) — *martinfowler.com*
5. [Spinnaker — Continuous Delivery Platform](https://spinnaker.io/) — *spinnaker.io*
6. [Argo CD](https://argo-cd.readthedocs.io/) — *argo-cd.readthedocs.io*
7. [Database Refactoring (Ambler & Sadalage)](https://martinfowler.com/books/refactoringDatabases.html) — *martinfowler.com*
8. [Accelerate (Forsgren, Humble, Kim)](https://itrevolution.com/product/accelerate/) — *itrevolution.com*
9. [Chaos Engineering (Rosenthal et al.)](https://www.oreilly.com/library/view/chaos-engineering/9781492043850/) — *oreilly.com*
10. [DORA Metrics](https://dora.dev/) — *dora.dev*
