# Migration Playbook

The strategic guide for executing migrations from one architecture to another — recognising that the team's choice between strangler-fig incrementalism and big-bang cutover, the abstraction layer that lets old and new coexist during transition, the data migration discipline that keeps both systems consistent during overlap, the cutover design that makes traffic shift safe and reversible, and the decommissioning execution that actually removes the legacy system are what determine whether a migration finishes as planned or stretches indefinitely with two systems running in parallel forever because nobody can afford the risk of fully cutting over to one or fully removing the other.

**Section:** `playbooks/` | **Subsection:** `migration/`
**Alignment:** Strangler Fig Pattern (Fowler) | Branch by Abstraction (Fowler) | Working Effectively with Legacy Code (Feathers) | AWS Migration Strategies — 7 Rs

---

## What "migration playbook" means — and how it differs from "migration runbook"

This page is about the *playbook* — the strategic guide for how the team plans and executes migrations as a class of engineering work: which migration strategies exist, when each is appropriate, how to choose between them, what disciplines apply to phases, how to design for reversibility. The *runbook* — the step-by-step procedural document that engineers execute during a specific migration event, with rollback steps and validation gates — lives in [`runbooks/migration`](../../runbooks/migration) at section level. Same domain, different operational concern: this page owns the strategic discipline; the runbook owns the procedural execution. A team running a specific migration applies the playbook's choices and the runbook's procedures together; they are complementary artefacts at different abstraction levels.

A *primitive* approach to migration is to plan a big-bang cutover: design the new system separately; build it to feature parity; cut over on a chosen date; remove the old system afterward. The plan looks clean on paper and fails systematically in practice. The new system is built without the operational lessons of the old (the production load patterns, the edge cases, the integrations whose existence nobody documented). The cutover date keeps slipping because feature parity is harder to verify than to claim. When the cutover happens, problems surface that weren't caught in pre-cutover testing because production traffic has properties that test traffic doesn't. Rollback is impossible because the rollback path was a slide on the plan, not a tested procedure. The team ends up running both systems in parallel "temporarily" until the parallel period becomes the new permanent state, and the migration is declared complete with the old system still running because nobody can take the risk of removing it.

A *production* approach to migration is a *staged discipline* with reversibility built in at every phase. The *strategy choice* — strangler fig versus big bang versus parallel run versus blue-green — is made deliberately based on the system's risk profile, the migration's blast radius, and the team's ability to validate behaviour before committing. The *abstraction layer* is introduced before any migration work begins: callers go through an interface that can route to either old or new implementation, which lets the team migrate one slice at a time without coordinating breaking changes across consumers. The *data migration discipline* keeps both systems consistent during the overlap period: writes go to both (dual-write), or one is the source of truth and the other follows (replication), or a backfill is performed at cutover with verified equality. The *cutover design* makes traffic shift safe (canary then progressive rollout, with rollback gates at each step) and *reversible* (the rollback path is tested before the cutover, not improvised during incident). The *decommissioning execution* actually removes the legacy system: the routes are removed, the code is deleted, the infrastructure is destroyed. Each phase has documented standards; the migration moves through them with rollback paths verified at each.

The architectural shift is not "we have a migration plan." It is: **the migration is a designed staged transition whose strategy choice (strangler / big bang / parallel run / blue-green), abstraction layer for old-new coexistence, data migration discipline for overlap consistency, cutover design for safe and reversible traffic shift, and decommissioning execution that actually removes the legacy system determine whether the migration finishes within plan or becomes a permanent parallel-run state — and treating migration as "build new, cut over, remove old" produces a plan that fails at the cutover, leaving the team running two systems forever because the rollback path was never built and the decommissioning never had a credible execution date.**

---

## Six principles

### 1. The migration strategy is chosen deliberately based on risk profile, not by default

There is no single right migration strategy; there are several patterns, each with different risk-reversibility-cost trade-offs. *Strangler fig* (gradually replace pieces of the old system behind a routing layer until nothing of the old remains) is the lowest-risk strategy and the longest-running; it works when the system can be sliced into independently-migratable pieces. *Branch by abstraction* (introduce an abstraction over both old and new implementations; switch the abstraction's binding) is similar but applied at the code level rather than the system level. *Big-bang cutover* (build new in parallel, switch over on a date, decommission old) is appropriate only when the new system can be validated comprehensively before cutover and the cost of running two systems in parallel for an extended period is prohibitive. *Parallel run* (run both systems with the same input; compare outputs; declare new ready when outputs match) is high-cost during the parallel period but produces strong evidence of behavioural equivalence. *Blue-green* (deploy new alongside old; switch traffic; ability to switch back) is appropriate when the systems are stateless or when state synchronisation is solved. The architectural discipline is to *choose deliberately*, documenting which strategy was selected and why, rather than defaulting to "build new and cut over" because that's the most familiar pattern.

#### Architectural implications

- The migration's strategic decision document records: which pattern was chosen; what alternatives were considered; what trade-offs were accepted (more risk for less time, or more time for less risk); what reversibility guarantees the choice provides.
- The strategy is matched to the system's properties: stateless services migrate easily under blue-green; stateful systems with database changes need a strangler approach with dual-write; legacy systems too tangled to slice may need branch-by-abstraction at the code level.
- The cost of the parallel period is *part of the strategy choice*: strangler fig is months-to-years of dual operation; big-bang is hours; parallel run is weeks or months. The team commits to the cost when choosing.
- The strategy can be revised if mid-migration evidence shows the original choice was wrong, but revision is a documented decision, not silent drift.

#### Quick test

> Pick the most recent migration your organisation completed (or attempted). Was there a documented strategy decision (which pattern, why, what alternatives were ruled out, what trade-offs were accepted)? Or did the migration default to "build new and cut over"? If the latter, the strategy choice was implicit, and the team didn't deliberately decide what risks they were taking on.

#### Reference

[Strangler Fig Pattern (Fowler)](https://martinfowler.com/bliki/StranglerFigApplication.html) is the canonical articulation of incremental replacement. [AWS Migration Strategies — 7 Rs](https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-strategies/migration-strategies.html) catalogues the strategy options for cloud migration specifically.

---

### 2. An abstraction layer is introduced before migration work begins — old and new coexist behind it

The most expensive way to migrate is to change every caller of the old system simultaneously when cutting over to the new. The cost scales with the number of integrations, and any caller missed becomes a late-discovered defect. The architectural discipline is to *introduce an abstraction layer first*: callers go through an interface; the interface can route to either the old implementation or the new; the migration becomes "change which implementation the abstraction is bound to," not "change every caller." The abstraction may be at the code level (branch by abstraction: introduce a wrapping interface around the old implementation; build the new implementation against the same interface; switch the binding) or at the system level (a routing layer or proxy that can direct calls to old or new based on configuration). Either way, the migration becomes *one switch*, applied behind the abstraction, instead of *many coordinated changes* across consumer code.

#### Architectural implications

- The abstraction is introduced *before* any migration work begins. The first PR of the migration is the abstraction, not the new implementation.
- The abstraction has the new system's intended interface, not the old system's interface. This forces design clarity about what the new contract should be, without committing to a specific implementation.
- The routing decision behind the abstraction is configurable at runtime when possible: a feature flag, a percentage rollout, a per-tenant or per-user routing rule. The team can shift traffic gradually rather than as one binary cutover.
- After migration completes, the abstraction may itself be removed (if it was introduced solely for migration) or retained (if it provides ongoing architectural value). The decision is explicit, not accidental.

#### Quick test

> If you started a migration tomorrow, what would the first PR be? If the answer is "the new implementation," the abstraction layer wasn't planned, and the cutover will require coordinated changes across every caller. If the answer is "an abstraction over the existing implementation that the new implementation will also implement," the migration is set up for incremental cutover.

#### Reference

[Branch by Abstraction (Fowler)](https://martinfowler.com/bliki/BranchByAbstraction.html) describes the code-level abstraction pattern. [Strangler Fig Pattern (Fowler)](https://martinfowler.com/bliki/StranglerFigApplication.html) describes the system-level routing pattern.

---

### 3. Data migration discipline keeps both systems consistent during overlap

In any migration where the old and new systems share state or both serve writes during the overlap period, *data consistency is the load-bearing problem*. Possible disciplines: *dual-write* (every write goes to both old and new; reads can come from either; behaviour must be designed so partial failures don't desync), *replication* (one is source of truth; the other follows via replication; reads from the replica may be slightly stale), *backfill at cutover* (read traffic stays on old; new is populated from a one-time export at cutover; cutover requires a brief read-only window or a delta replay), *event sourcing* (both systems consume the same event stream and project it into their respective models). Each has different consistency-cost-complexity trade-offs. The architectural discipline is to *choose explicitly* and to *test the consistency mechanism* before relying on it; the cost of discovering during cutover that dual-write was occasionally dropping records is an unrecoverable production incident.

#### Architectural implications

- The data migration discipline is documented before migration begins: which mechanism, what consistency guarantees apply during overlap, what staleness or skew is acceptable, how consistency is verified.
- Verification is automated: a reconciliation job runs continuously during overlap, comparing key counts and content between systems, alerting on any drift. The team finds inconsistencies before consumers do.
- Schema migration tooling is part of the data discipline: tools like Liquibase or Flyway version schema changes; expand-then-contract schema patterns let old code keep working while new schema is added (expand), then old schema is removed only after the migration is complete (contract).
- The cutover moment for data is designed: which system is source of truth before, during, and after; how reads are routed; what's backfilled at the moment of cutover; how the new source of truth proves itself before old is read-only.

#### Quick test

> If you're partway through a migration and need to know whether the old and new systems have the same data right now, can you check? If the answer is "we'd have to write a one-off comparison script," continuous reconciliation isn't part of the discipline, and you're trusting that dual-write or replication has been working without verification.

#### Reference

[Refactoring Databases](https://databaserefactoring.com/) (Ambler & Sadalage) covers schema migration patterns including expand-then-contract. [Liquibase](https://www.liquibase.org/) and [Flyway Database Migrations](https://flywaydb.org/) are the canonical schema migration tools.

---

### 4. Cutover is staged and reversible — canary, progressive rollout, tested rollback

A primitive cutover is a single switch flipped at a planned time: traffic moves from old to new at moment T. A production cutover is a *staged progression* with reversibility verified at each stage: a canary slice (1-5% of traffic) routed to new while old serves the rest; metrics compared (error rates, latency, business signals); proceed-or-rollback decision at the gate; progressive widening (10%, 25%, 50%, 75%, 100%) with the same gate at each step; full cutover only after metrics confirm new is performing equivalently. The *rollback path* is tested before the cutover begins — the team has demonstrated they can shift traffic back from new to old in measured time, with no data loss, no consumer impact. The cutover plan documents what triggers rollback (specific error rate threshold, latency degradation, business metric drop, manual decision), who has authority to call rollback, and how the rollback is executed. The discipline is *evidence-based progression*: each step generates data; the data informs the next step; the rollback path is the safety net that makes the staging acceptable.

#### Architectural implications

- The cutover plan documents the percentage stages, the gate metrics at each, the proceed-or-rollback thresholds, and the time intervals between stages (giving each stage long enough to surface issues).
- Rollback rehearsal happens *before* the cutover begins: the team executes a full reverse migration on a test environment or low-traffic slice and verifies the rollback path produces a working state. The rollback isn't first executed under stress.
- Metrics monitored during cutover are pre-defined and aligned with what could go wrong: error rates, latency p50/p95/p99, business metrics (orders per minute, payment success rate), and any system-specific health signals.
- Authority for rollback is designated: who can call it, who must be informed. The decision is fast and unambiguous so that hesitation doesn't extend the impact.

#### Quick test

> If your cutover went wrong at the 50% stage, how would you roll back, and how long would the rollback take? If the answer is "we'd need to figure that out at the time," the rollback path hasn't been designed, and the cutover is irreversible at the moment a problem surfaces.

#### Reference

[Strangler Fig Pattern (Fowler)](https://martinfowler.com/bliki/StranglerFigApplication.html) treats progressive cutover as the natural mode of incremental replacement. The [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) book describes canary deployment discipline at depth in the release engineering chapter.

---

### 5. Legacy code surfaces are characterised before being touched — tests as load-bearing artefact

The migration's hardest problem is often *understanding what the legacy system actually does*. The documented behaviour and the actual behaviour have drifted apart over years; edge cases survive because they handle real production cases nobody remembers; subtle invariants exist that nobody can articulate but which the system depends on. A primitive migration assumes the documented behaviour and rebuilds against it; production then reveals the gaps. A production migration *characterises the legacy behaviour empirically before reimplementing it*: characterisation tests pin the actual current behaviour (golden master tests for outputs given inputs); production traffic samples are recorded and replayed against the new implementation to confirm equivalence; integration patterns are enumerated by tracing actual production traffic. The tests become the authoritative spec — they document what the legacy system does, even when the documentation doesn't.

#### Architectural implications

- Characterisation tests are written against the legacy system *before* the new implementation is built, not as a parallel exercise. The tests anchor the migration's correctness criterion.
- Production traffic capture and replay is part of migration tooling: a representative sample of real requests is recorded; the new implementation is run against the same inputs; outputs are compared. Equivalence (or documented intentional divergence) is the criterion for cutover readiness.
- Edge cases discovered during characterisation become explicit: each one documented with its trigger condition, expected behaviour, and whether the new system preserves or intentionally changes the behaviour. The migration becomes a documented audit of legacy behaviour, not a guess.
- Legacy code that resists characterisation (because it has hidden side effects, non-deterministic behaviour, or external dependencies) is flagged early; either the legacy is refactored to be characterisable first, or the migration's risk is accepted explicitly.

#### Quick test

> Pick a recent migration. Were characterisation tests written against the legacy system before the new implementation was built? Or did the team rebuild against the documented behaviour and discover the differences in production? If the latter, the migration's correctness criterion was the documentation, which is by definition incomplete for any long-lived system.

#### Reference

[Working Effectively with Legacy Code (Feathers)](https://www.oreilly.com/library/view/working-effectively-with/0131177052/) is the canonical articulation of characterisation testing as a discipline for legacy systems. [Branch by Abstraction (Fowler)](https://martinfowler.com/bliki/BranchByAbstraction.html) describes how the abstraction layer enables side-by-side characterisation and verification.

---

### 6. Decommissioning is the migration's success criterion — old system actually removed

The hardest discipline in migration is *actually removing the old system after cutover*. The temptation to leave it running "just in case" is constant: the new system has been running for weeks but a low-priority code path hasn't been observed; a senior stakeholder isn't ready to declare migration complete; nobody owns the decommissioning work because it doesn't ship features. Each retained week of the old system's operation has costs (infrastructure, security patching, on-call coverage, mental overhead) and risks (the old system continues to drift while the new is the active codebase, making any future fallback increasingly impractical). The architectural discipline is to *plan decommissioning as a deliverable* with a date, an owner, and explicit completion criteria: traffic is fully on new for N consecutive weeks with no rollbacks; routes to old are removed; old infrastructure is destroyed; old code is deleted from source control. After decommissioning, the migration is closed, documented, and the team's attention released.

#### Architectural implications

- Decommissioning is a planned phase with a date and owner, not a cleanup activity that happens when convenient. The team commits to the date when planning the migration.
- Completion criteria are specific: N consecutive weeks of cutover-only operation; no observed traffic to deprecated routes; no rollbacks during the watch period; sign-off from named stakeholders.
- Removal is staged: routes disabled first (so any unexpected traffic produces a visible error rather than serving from old); after a watch period, code deleted; infrastructure destroyed last.
- Post-decommissioning retrospective documents what was removed, what was retained from the migration (the abstraction may stay, monitoring may stay, the migration's lessons stay), and what the engineering surface looks like after.

#### Quick test

> Pick the most recent migration in your organisation that was declared "complete." Has the legacy system actually been removed — code deleted from repo, infrastructure destroyed, routes returning 404? Or is it still running because removing it never became urgent? If the latter, the migration isn't actually complete; the parallel-run period has become the new permanent state.

#### Reference

[Strangler Fig Pattern (Fowler)](https://martinfowler.com/bliki/StranglerFigApplication.html) treats the eventual *strangling* (full decommissioning of the original) as the strategy's defining property. The [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) book treats decommissioning as a first-class lifecycle phase requiring its own discipline.

---

## Common pitfalls when adopting migration playbook thinking

### ⚠️ Defaulting to big-bang cutover because it's the most familiar pattern

The team plans the migration as "build new in parallel, cut over on a date, remove old afterward" without considering whether the system's risk profile actually fits the strategy. Big-bang carries the highest risk and offers the least reversibility.

#### What to do instead

Strategy choice as a deliberate decision: which pattern (strangler / branch-by-abstraction / parallel run / blue-green / big-bang), what alternatives were considered, what trade-offs were accepted. The decision is documented and reviewable.

---

### ⚠️ Migration work begins without an abstraction layer

The new implementation is built first; cutover requires coordinated changes across every caller. Any caller missed becomes a late-discovered defect. The cost of cutover scales with integration count.

#### What to do instead

The first PR of the migration is the abstraction layer. Callers go through an interface that can route to old or new. The migration becomes "change which implementation the abstraction is bound to," not "change every caller."

---

### ⚠️ Data consistency assumed during overlap, not verified

Dual-write or replication is set up; the team trusts it works without continuous verification. Drift accumulates silently. The discrepancy is discovered when consumers report problems or at the cutover moment.

#### What to do instead

Continuous reconciliation runs during overlap: counts and content compared between systems; alerts fire on drift. Consistency is verified, not assumed. Schema changes use expand-then-contract patterns so neither system is broken at any moment.

---

### ⚠️ Cutover as one switch — no canary, no rollback rehearsal

Traffic moves from old to new at a single moment. If problems surface, rollback is improvised. The cutover plan didn't budget time for staged progression or rollback verification.

#### What to do instead

Staged cutover (canary 1-5%, then 10%, 25%, 50%, 75%, 100%) with metric gates at each stage. Rollback path tested before cutover begins. Authority for rollback designated. Time between stages long enough to surface issues.

---

### ⚠️ Decommissioning never happens — old system runs forever

After cutover, the old system is left running "just in case." Weeks become months become permanent. The migration is declared "complete" while the legacy is still operating. Every future fallback to old becomes increasingly impractical because the old has drifted from the new.

#### What to do instead

Decommissioning planned as a deliverable with date, owner, and completion criteria. Staged removal (routes first, code next, infrastructure last). Post-decommissioning retrospective. The migration is closed only when the legacy is actually gone.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Migration strategy choice is documented with alternatives considered ‖ Which pattern (strangler / branch-by-abstraction / parallel run / blue-green / big-bang) and why this one over the alternatives. Trade-offs accepted are explicit. The choice is reviewable. | ☐ |
| 2 | Abstraction layer introduced before migration work begins ‖ First PR of migration is the abstraction; callers go through an interface; new implementation builds against the same interface. The migration becomes one switch behind the abstraction, not coordinated changes across consumers. | ☐ |
| 3 | Data migration discipline documented and tested before relied on ‖ Mechanism (dual-write / replication / backfill / event sourcing) chosen explicitly. Consistency guarantees during overlap stated. Reconciliation jobs run continuously verifying systems agree. | ☐ |
| 4 | Schema changes use expand-then-contract patterns ‖ New schema added before old code is changed (expand); old code switches to new schema; old schema removed only after migration completes (contract). Neither system is broken at any moment. | ☐ |
| 5 | Legacy behaviour characterised before reimplementation ‖ Characterisation tests pin actual current behaviour. Production traffic captured and replayed against new implementation. Edge cases enumerated and either preserved or intentionally changed with documentation. | ☐ |
| 6 | Cutover is staged with metric gates and time between stages ‖ Canary then progressive rollout (1%, 10%, 25%, 50%, 75%, 100%) with proceed-or-rollback gates at each stage. Time intervals long enough to surface issues. Stages documented in the cutover plan. | ☐ |
| 7 | Rollback path tested before cutover begins ‖ Reverse migration executed on test environment or low-traffic slice. Rollback time measured. Authority for rollback designated; trigger conditions documented. The rollback is exercised, not improvised. | ☐ |
| 8 | Decommissioning planned as a deliverable with date and owner ‖ Completion criteria specific (N consecutive cutover-only weeks, no rollbacks, named sign-off). Removal staged (routes, code, infrastructure). The decommissioning is committed to, not left to convenience. | ☐ |
| 9 | Post-cutover monitoring continues for the watch period ‖ The new system is observed at full traffic for the documented watch period before decommissioning starts. Issues during the watch trigger investigation, possible rollback, or extension before removal. | ☐ |
| 10 | Migration retrospective documents lessons and surface state ‖ What worked, what didn't, what's retained from the migration (abstraction, monitoring, lessons), what the engineering surface looks like after. The migration is closed as an accountable deliverable, not a vague success. | ☐ |

---

## Related

[`playbooks/api-lifecycle`](../api-lifecycle) | [`playbooks/resilience`](../resilience) | [`runbooks/migration`](../../runbooks/migration) | [`runbooks/rollback`](../../runbooks/rollback) | [`patterns/event-driven`](../../patterns/event-driven)

---

## References

1. [Strangler Fig Pattern (Fowler)](https://martinfowler.com/bliki/StranglerFigApplication.html) — *martinfowler.com*
2. [Branch by Abstraction (Fowler)](https://martinfowler.com/bliki/BranchByAbstraction.html) — *martinfowler.com*
3. [Working Effectively with Legacy Code (Feathers)](https://www.oreilly.com/library/view/working-effectively-with/0131177052/) — *oreilly.com*
4. [AWS Migration Strategies — 7 Rs](https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-strategies/migration-strategies.html) — *docs.aws.amazon.com*
5. [Refactoring Databases](https://databaserefactoring.com/) — *databaserefactoring.com*
6. [Liquibase](https://www.liquibase.org/) — *liquibase.org*
7. [Flyway Database Migrations](https://flywaydb.org/) — *flywaydb.org*
8. [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) — *sre.google*
9. [Building Evolutionary Architectures (Ford et al.)](https://www.oreilly.com/library/view/building-evolutionary-architectures/9781491986356/) — *oreilly.com*
10. [Documenting Architecture Decisions (Nygard)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — *cognitect.com*
