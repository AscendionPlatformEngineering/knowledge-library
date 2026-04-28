# Migration Runbook

The artefact that turns a multi-week, multi-team, often-irreversible system change into an executable, gated, rollback-aware project — recognising that migrations are where the architectural complexity of the old and new systems collide, and where the runbook's structure determines whether the migration ships cleanly or accumulates as the next quarter's tech debt.

**Section:** `runbooks/` | **Subsection:** `migration/`
**Alignment:** Database Refactoring (Ambler & Sadalage) | Strangler Fig Pattern (Martin Fowler) | Continuous Delivery (Humble & Farley) | Online Schema Migration (gh-ost)

---

## What "migration runbook" actually means

A *primitive* migration is the kind that gets attempted on a Friday afternoon: the team has a new system that's "ready," they flip a DNS record or a feature flag, traffic goes to the new system, and either everything's fine (lucky) or something's wrong and the team spends the weekend rolling back, reconciling state, and apologising to users. Migrations done this way work occasionally; they fail expensively when they fail; the organisation's appetite for migrations diminishes after each failure until even necessary migrations are postponed indefinitely.

A *production* migration runbook treats the same problem as a designed, multi-phase project. The migration has phases: *preparation* (the new system is built, tested, deployed alongside the old, with no production traffic yet); *dual-running* (both systems handle real traffic, often with the new system shadowed against the old to validate correctness); *progressive cutover* (traffic is shifted from old to new in measured increments — 1%, 5%, 25%, 50%, 100% — with verification gates between increments); *cleanup* (the old system is decommissioned; the migration's temporary scaffolding is removed). Each phase has documented entry criteria, executable steps, verification criteria, and exit criteria. Each phase is *gated*: you don't proceed to the next phase until the current phase's verifications pass, and every phase is *reversible* until the cleanup phase commits to one-way decommission. The runbook is what turns this multi-week multi-team coordination problem into a tractable, executable artefact.

The architectural shift is not "we wrote a migration plan." It is: **migrations are multi-phase projects where reversibility, gating, verification, and decommissioning are first-class concerns — and the runbook's structure determines whether each migration ships predictably or fails the way Friday-afternoon migrations fail.**

---

## Six principles

### 1. Migrations are projects with phase structure — preparation, dual-running, progressive cutover, cleanup

A migration runbook that's structured as a single-shot script ("run this command on Friday at 8 PM") fails the way single-shot migrations fail: there's no opportunity to discover problems before they hit production, no opportunity to roll back without coordinated emergency response, and no scaffolding for handling the inevitable surprises. A migration runbook structured as a multi-phase project has, by design, opportunities to detect and address problems at each phase boundary — and the boundaries are where the project's overall risk is concentrated. *Preparation* validates that the new system can do the work in isolation. *Dual-running* validates that the new system produces the same outputs the old does on real traffic. *Progressive cutover* validates that the new system works under increasing load with the old system as a fallback. *Cleanup* finalises the migration by removing the old system and the scaffolding. Each phase is its own runbook segment with its own verification.

#### Architectural implications

- The runbook is structured as a multi-phase document with documented entry criteria, steps, verification, and exit criteria per phase — not a single script.
- Phases are calendar-aware: each phase has a documented expected duration (preparation may take weeks; dual-running typically days; progressive cutover hours; cleanup days), and the runbook is built to accommodate the timeline rather than force everything into a single execution window.
- Each phase's verification is documented and enforced — proceeding to the next phase requires the current phase's verifications passing, not just the team's collective sense that things look fine.
- The phases align with what the system actually requires; phases that don't apply (e.g. a system with no historical state may not need dual-running) are explicitly documented as not applicable, with reasoning.

#### Quick test

> Pick a recent or planned migration in your organisation. Is the runbook structured as a phased project with explicit phase boundaries, or as a single-shot script with optional rollback? If single-shot, the migration is one surprise away from emergency response — and the surprises that don't surface until production are the most expensive ones.

#### Reference

[Database Refactoring — Ambler & Sadalage](https://martinfowler.com/books/refactoringDatabases.html) is the canonical reference for phased database migrations; the discipline (deprecate, transition, remove) maps directly to migration-runbook phase structure. [Continuous Delivery — Humble & Farley](https://www.oreilly.com/library/view/continuous-delivery-reliable/9780321670250/) covers the multi-phase migration pattern at the system level.

---

### 2. Reversibility planning — design the rollback path before designing the forward path

The most consequential architectural property of a migration is whether it's *reversible* and *up to which point*. A migration that's reversible at every phase up until cleanup is dramatically lower-risk than one that becomes irreversible at the first traffic shift. Reversibility is not free: it requires designing the new system to coexist with the old (dual-write, shadow-read), maintaining the old system through the dual-running phase, having tested rollback paths before the forward path is exercised. The architectural discipline is to design the rollback path *first* — establish what reversibility means at each phase, what's required to maintain it, when it's deliberately given up — and only then design the forward execution. Migrations that design the forward path first and the rollback path as an afterthought routinely discover, at the worst possible time, that the rollback they thought they had isn't actually feasible.

#### Architectural implications

- Each phase of the migration runbook documents its reversibility property: fully reversible (rollback to prior phase is possible without data loss), partially reversible (rollback possible with documented data loss or reconciliation), irreversible (this phase commits the migration; rollback would require fresh restoration from backup).
- The transition to an irreversible phase is itself a documented decision point — not a step that's quietly crossed without acknowledgment.
- The scaffolding required for reversibility (dual-write infrastructure, shadow-read pipelines, old-system retention) is documented and maintained through the phases that need it; it's removed only after cleanup is committed.
- Rollback paths are *exercised* — actually performed in non-production at minimum, ideally in production-like conditions — before the forward path is taken in production. An untested rollback is no rollback (see [`runbooks/rollback`](../rollback)).

#### Quick test

> Pick a migration in your organisation that's currently in progress. At each phase, is rollback feasible? Have the rollback paths been exercised? If the answer is "we'll figure it out if we need to," the migration is operating with rollback as an aspiration — and the next thing that goes wrong will reveal whether the aspiration matches reality.

#### Reference

[Database Refactoring — Ambler & Sadalage](https://martinfowler.com/books/refactoringDatabases.html) treats reversibility as a primary architectural concern in multi-phase database migrations. [Online Schema Migration — gh-ost](https://github.com/github/gh-ost) is a canonical tool that operationalises reversibility for the specific case of MySQL schema migrations; the architectural patterns generalise.

---

### 3. Progressive cutover — small percentage shifts with verification at each step

A migration that shifts 100% of traffic from the old system to the new in a single moment has no opportunity to discover a problem before all users see it. A migration that shifts traffic progressively — 1%, 5%, 25%, 50%, 100% — exposes problems at each percentage point with a small subset of users, lets the team verify that the new system handles increasing load, and provides a natural rollback point at each step. The architectural pattern is to choose percentage breakpoints based on the system's traffic profile and the team's confidence in the new system, with verification gates between breakpoints. The discipline takes more execution time (a 100% cutover that could happen in a moment becomes a multi-hour or multi-day progression) but pays the time back in dramatically lower risk and the ability to detect problems early.

#### Architectural implications

- Cutover is staged with documented percentage breakpoints (canonical defaults: 1%, 5%, 25%, 50%, 100%; tuned per migration to the system's risk and traffic profile).
- Each breakpoint has documented verification: the new system's error rate, latency distribution, and key correctness signals are within tolerance compared to the old system on the same traffic.
- Soak time at each breakpoint is documented — the team waits long enough at each percentage for problems that take time to surface (memory leaks, periodic batch jobs, scheduled work) to actually surface.
- The progression can pause or reverse at any breakpoint — pausing if the new system is borderline, reversing if it's failing — with explicit decision criteria for each.

#### Quick test

> Pick a migration in your organisation. Did or does it use progressive cutover with documented breakpoints and verification at each, or is it (will it be) a single-shot cutover? If single-shot, the team is committing to discovering all problems with the entire user base as the test population.

#### Reference

[Canary Release — Martin Fowler](https://martinfowler.com/bliki/CanaryRelease.html) treats progressive cutover at the deployment level; the same discipline applies to migrations. [Continuous Delivery — Humble & Farley](https://www.oreilly.com/library/view/continuous-delivery-reliable/9780321670250/) covers the canary and percentage-rollout patterns as primary release-engineering disciplines that transfer to migration runbooks.

---

### 4. Verification gates between phases — proceed only on signals, not on schedule

The instinct to ship on schedule produces failed migrations. A team committed to "ship by end of quarter" can find itself proceeding to the next migration phase before the current phase's verification passes, on the rationale that they're behind schedule. The architectural discipline is the *verification gate*: the move from one phase to the next is conditional on the current phase's documented verifications passing — error rates within tolerance, correctness signals matching, performance signals acceptable, no unaddressed user reports. If the verifications don't pass, the migration doesn't proceed; the team either stays in the current phase to address the underlying issue or rolls back. Schedule pressure tries to override gates; the runbook's discipline is to make the gate criteria explicit, documented, and enforced — not advisory thresholds that experienced engineers can wave away.

#### Architectural implications

- Each phase boundary has a documented verification gate with specific, measurable criteria (error rate below X, latency P99 below Y, correctness mismatch rate below Z, no unaddressed user reports of class W).
- Gate criteria are determined before the phase is executed, not negotiated during execution under schedule pressure.
- Failed gates produce a documented decision: stay in current phase to address (with timeline), or roll back to prior phase (with reasoning). Proceed-anyway is not a default option.
- Soak time before evaluating gate criteria is documented and enforced — gates evaluated too quickly miss problems that take time to manifest.

#### Quick test

> Pick the most consequential migration your organisation has done in the last year. At each phase boundary, were verification gates documented and enforced? Or did the migration proceed based on team confidence and schedule? If the latter, the migration's success was correlated with luck; the next migration with similar discipline is one bad-luck draw away from a different outcome.

#### Reference

[Continuous Delivery — Humble & Farley](https://www.oreilly.com/library/view/continuous-delivery-reliable/9780321670250/) treats deployment gates as a first-class engineering discipline; the same principle applies to migration phase boundaries. [Accelerate — Forsgren, Humble, Kim](https://itrevolution.com/product/accelerate/) operationalises verification gates as part of the engineering performance research.

---

### 5. Multi-team coordination is part of the runbook, not extracted from it

A migration that touches more than one team's systems requires coordination: the team running the migration depends on signals from teams operating downstream services, on cooperation from teams whose systems read or write the migrating data, on availability of subject-matter experts during cutover windows. A runbook that handles only the technical steps and leaves coordination to be figured out separately produces predictable failure modes: the wrong people are paged at the wrong time; signals from dependent teams are missing or late; the cutover window happens during a dependent team's maintenance window. The architectural discipline is to make coordination part of the runbook itself: who needs to be notified at each phase, who needs to confirm readiness, who needs to be available during cutover, what's the communication channel and cadence. The runbook becomes the coordination artefact as well as the technical one.

#### Architectural implications

- Each phase identifies the teams involved with named roles: who owns the migration, who's consulted, who needs to be informed, who needs to be on call during specific windows.
- Notifications and status updates are baked into the runbook as steps: "Notify team X 24 hours before phase 3 starts" is a step, not an undocumented social practice.
- Communication channels and cadences are documented per phase: dual-running may use weekly syncs; progressive cutover may use real-time chat; cleanup may use periodic written status.
- Dependencies on other teams' systems are explicit: "Phase 3 cannot proceed until team Y has shipped feature Z" is a documented gate, not an implicit assumption.

#### Quick test

> Pick a recent migration that involved multiple teams. Was the coordination part of the runbook (named roles, notification steps, dependency gates), or was it figured out separately and inconsistently? If the latter, the migration's coordination ran on individual relationships and tribal knowledge — and the next migration depending on different individuals is a different coordination outcome away.

#### Reference

[Team Topologies — Skelton & Pais](https://teamtopologies.com/) covers cross-team coordination patterns in detail; the explicit-coordination discipline transfers from organisational architecture to migration-runbook design. [The Phoenix Project — Kim et al.](https://itrevolution.com/product/the-phoenix-project/) treats coordination failures as a primary cause of migration project failures, with the architectural response being explicit coordination structure.

---

### 6. Cleanup and decommission are migration phases — the migration isn't done until the old system is removed

A common pattern: the new system is in production, traffic is at 100%, the team declares the migration "done," and moves on to the next thing. The old system is still running. A year later, the old system is still running — nobody decommissioned it because it wasn't urgent, and now decommissioning it is harder because nobody remembers exactly what depends on it. Two systems are now in operation, with the cost paid in infrastructure, ongoing maintenance, and the cognitive load of every engineer who has to understand both. The architectural discipline is to treat *cleanup* as part of the migration, with its own runbook phase: the old system is fully decommissioned (instances terminated, data retained per retention policy then deleted, monitoring removed, runbooks deprecated), the migration's temporary scaffolding is removed (dual-write code paths, shadow-read pipelines, feature flags), and the migration is declared done only when nothing of the old system or its scaffolding remains in production.

#### Architectural implications

- The runbook includes an explicit cleanup phase with documented steps: terminate old-system instances, remove or archive data per retention policy, decommission monitoring and alerting, deprecate old runbooks, remove dual-write and shadow-read scaffolding, remove migration-specific feature flags.
- The cleanup phase is gated like any other: it doesn't start until the new system has been at 100% for a documented soak period (typically weeks); it has verification that nothing is still using the old system before decommission.
- The migration is "done" when cleanup is complete — not when traffic reaches 100%. Status communication reflects this: "100% traffic on new system; 60 days into soak period; cleanup phase scheduled for next quarter."
- Old systems that aren't cleaned up are tracked: a list of systems-still-running-after-migration is itself an architectural debt artefact, prioritised for cleanup.

#### Quick test

> Pick a migration your organisation completed within the last two years. Has the old system been fully decommissioned, including all its scaffolding (dual-write paths, shadow-read pipelines, migration feature flags)? If the answer is "the old system is still there in some form," the migration was declared done before cleanup, and the architectural cost is being paid every quarter since.

#### Reference

[Strangler Fig Pattern — Martin Fowler](https://martinfowler.com/bliki/StranglerFigApplication.html) treats migration as a process that includes the eventual removal of the old system; the pattern's name refers specifically to the strangler vine that grows around a host tree until the host is gone. [Decommissioning Patterns — Lewis](https://martinfowler.com/articles/distributed-objects-microservices.html) treats decommissioning as a first-class phase of the migration, with explicit gates and verification.

---

## Architecture Diagram

The diagram below shows the canonical migration-runbook architecture: phased project structure (preparation → dual-running → progressive cutover → cleanup) with verification gates between phases; reversibility properties tracked per phase; coordination structure with named roles and notification steps; rollback paths from any reversible phase; cleanup phase as part of the migration, not an afterthought.

---

## Common pitfalls when adopting migration-runbook thinking

### ⚠️ Single-shot Friday-night migration

The migration is structured as a single script. It runs once. Either it works (lucky) or it doesn't (everyone loses a weekend). No verification gates; no progressive cutover; rollback is hopeful.

#### What to do instead

Multi-phase project structure with verification gates. Preparation, dual-running, progressive cutover, cleanup. Each phase reversible until cleanup. The runbook accommodates the timeline rather than forcing everything into one window.

---

### ⚠️ Forward path designed before rollback path

The team designs how to migrate forward, then bolts on a rollback section. At the moment rollback is needed, the bolted-on plan turns out to be infeasible.

#### What to do instead

Rollback path designed first. Reversibility properties documented per phase. Scaffolding required for reversibility (dual-write, shadow-read, old-system retention) maintained through the phases that need it. Rollback paths exercised before forward path is taken in production.

---

### ⚠️ 100% cutover in a single moment

Traffic shifts from old to new instantly. Problems are discovered with the entire user base as the test population.

#### What to do instead

Progressive cutover with documented percentage breakpoints (1%, 5%, 25%, 50%, 100%). Verification at each breakpoint. Soak time for problems that take time to manifest. Pause or reverse at any breakpoint based on signals.

---

### ⚠️ Schedule pressure overrides verification gates

The team is behind schedule. The verification at the current phase boundary is borderline. The decision is to proceed anyway. The next phase exposes the underlying issue that the verification was meant to catch.

#### What to do instead

Gate criteria determined before phase execution. Failed gates produce documented decisions: stay-and-address or roll-back. Proceed-anyway is not a default option. Schedule pressure is treated as a signal to revisit timeline or scope, not to wave gates aside.

---

### ⚠️ Migration "done" when traffic reaches 100%

The new system is at 100%. The migration is declared done. The old system is still running a year later, with its scaffolding intact.

#### What to do instead

Cleanup is a phase of the migration, not an afterthought. The migration is "done" when cleanup is complete — old system decommissioned, scaffolding removed, monitoring deprecated. Status reflects the actual state.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | The runbook is structured as a multi-phase project with documented entry criteria, steps, verification, and exit criteria per phase ‖ Not a single-shot script. Phases align with what the system requires; phases not applicable are explicitly documented. | ☐ |
| 2 | Each phase documents its reversibility property — fully, partially, or irreversible ‖ The transition to irreversibility is itself a documented decision point. Scaffolding for reversibility is maintained through phases that need it. | ☐ |
| 3 | Rollback paths are exercised before forward paths are taken in production ‖ An untested rollback is no rollback. Game days, staging exercises, or production-like rehearsal validate that the rollback is actually feasible. | ☐ |
| 4 | Cutover is staged with documented percentage breakpoints and verification at each ‖ 1%, 5%, 25%, 50%, 100% (tuned per migration). Each breakpoint has documented verification and soak time. The progression can pause or reverse based on signals. | ☐ |
| 5 | Verification gates have specific, measurable criteria determined before phase execution ‖ Error rate below X, correctness mismatch below Y, no unaddressed user reports. The criteria are not negotiated during execution under schedule pressure. | ☐ |
| 6 | Failed gates produce documented decisions — stay-and-address or roll-back, not proceed-anyway ‖ Proceed-anyway is not a default option. Schedule pressure is treated as a signal to revisit, not to wave gates aside. | ☐ |
| 7 | Multi-team coordination is part of the runbook — named roles, notification steps, dependency gates ‖ Coordination is not figured out separately. The runbook is the coordination artefact as well as the technical one. | ☐ |
| 8 | Communication channels and cadences are documented per phase ‖ Dual-running may use weekly syncs; progressive cutover may use real-time chat. The cadence matches the phase's tempo. | ☐ |
| 9 | Cleanup is an explicit phase with documented steps — decommission, scaffolding removal, monitoring deprecation ‖ Cleanup is gated like any other phase. The migration is "done" when cleanup is complete, not when traffic reaches 100%. | ☐ |
| 10 | Migrations whose cleanup hasn't completed are tracked as architectural debt ‖ A list of systems-still-running-after-migration is itself a debt artefact, prioritised for cleanup. The cost of two-systems-running is recognised, not hidden. | ☐ |

---

## Related

[`runbooks/incident`](../incident) | [`runbooks/rollback`](../rollback) | [`technology/devops`](../../technology/devops) | [`patterns/data`](../../patterns/data) | [`system-design/scalable`](../../system-design/scalable) | [`observability/sli-slo`](../../observability/sli-slo)

---

## References

1. [Database Refactoring (Ambler & Sadalage)](https://martinfowler.com/books/refactoringDatabases.html) — *martinfowler.com*
2. [Strangler Fig Pattern (Martin Fowler)](https://martinfowler.com/bliki/StranglerFigApplication.html) — *martinfowler.com*
3. [Continuous Delivery (Humble & Farley)](https://www.oreilly.com/library/view/continuous-delivery-reliable/9780321670250/) — *oreilly.com*
4. [Online Schema Migration (gh-ost)](https://github.com/github/gh-ost) — *github.com*
5. [Canary Release (Martin Fowler)](https://martinfowler.com/bliki/CanaryRelease.html) — *martinfowler.com*
6. [Accelerate (Forsgren, Humble, Kim)](https://itrevolution.com/product/accelerate/) — *itrevolution.com*
7. [Team Topologies](https://teamtopologies.com/) — *teamtopologies.com*
8. [The Phoenix Project (Kim et al.)](https://itrevolution.com/product/the-phoenix-project/) — *itrevolution.com*
9. [Feature Flags (Martin Fowler)](https://martinfowler.com/articles/feature-toggles.html) — *martinfowler.com*
10. [Decommissioning Patterns (Lewis)](https://martinfowler.com/articles/distributed-objects-microservices.html) — *martinfowler.com*
