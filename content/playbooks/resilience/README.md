# Resilience Playbook

The strategic guide for designing systems that absorb and recover from failure — recognising that the team's failure-mode inventory rather than uptime targets, the layered resilience patterns applied per-tier (timeout, retry, circuit breaker, bulkhead, fallback), the explicit RPO and RTO targets per service rather than blanket assumptions, the chaos engineering practice that surfaces unknown failure modes before they surface themselves, and the recovery rehearsal discipline that proves the system can actually fail back are what determine whether a system is meaningfully resilient or whether it merely lacks evidence of being fragile until the next unlikely event reveals it.

**Section:** `playbooks/` | **Subsection:** `resilience/`
**Alignment:** Release It! (Nygard) | Site Reliability Engineering (Google) | Chaos Engineering (Principles of Chaos) | AWS Well-Architected Reliability Pillar

---

## What "resilience playbook" means — and how it differs from "HA/DR technology" and "incident response runbook"

This page is about the *playbook* — the strategic guide for how the team designs systems for resilience: which failure modes are anticipated and which are accepted, what resilience patterns apply at which layers, what RPO/RTO targets each service commits to, how chaos engineering and game days surface unknown failure modes. The technology of resilience — multi-AZ deployment, replicated databases, automated failover, backup tooling — lives in [`technology/ha-dr`](../../technology/ha-dr) at section level. The procedural document executed *during* an incident — the runbook — lives in [`runbooks/incident`](../../runbooks/incident). Three lanes: this page owns the *upfront design discipline*; `ha-dr` owns the *tech surface*; the incident runbook owns the *during-incident execution*. The same engineering team works across all three at different moments: design-time, technology-choice-time, incident-time.

A *primitive* approach to resilience is to set an uptime target ("99.9%") and trust that the engineering team will achieve it. The target is treated as the answer to the question "are we resilient?" — yes if uptime is measured at or above target, no if below. The framing is wrong because uptime alone hides what happens when failure does occur: how long is recovery, how much data is lost, how does the team know recovery is complete, whether the system gracefully degrades or hard-fails when components are unreachable. The team experiences few incidents because failures are rare, learns little from them when they do occur, and has no calibrated picture of which failure modes the system would survive. The first significant failure surfaces unknowns: a region outage the system isn't designed for, a database failover that doesn't actually work, a dependency cascade nobody anticipated. The uptime target was met for years; the resilience claim was hollow.

A *production* approach to resilience is a *layered design discipline* with failures anticipated explicitly. The *failure-mode inventory* — what failures are anticipated, what failures are accepted, what are the impact characterisations of each — is documented per service and revisited when system topology changes. The *layered resilience patterns* are applied per tier: at the network layer (timeouts on every external call, retries with exponential backoff and jitter, circuit breakers that fail fast when a dependency is unhealthy); at the service layer (bulkheads that contain failure within a domain, rate limiting that protects under load, graceful degradation that returns partial results rather than nothing); at the data layer (replication for availability, backup for recoverability, eventual consistency where appropriate); at the platform layer (multi-AZ for zonal resilience, multi-region for regional, capacity headroom for surge). The *explicit RPO and RTO targets* per service are derived from business requirements (the order-management service can lose at most 1 minute of data and must recover within 5 minutes; the catalog service can lose 1 hour and recover within 30 minutes), not assumed uniformly. The *chaos engineering practice* runs continuously: failure injection in production-like environments to verify resilience patterns work as designed; game days where teams simulate failures to test response. The *recovery rehearsal discipline* runs periodically: backups are restored, failovers are exercised, the team proves the system can actually fail back, not just that it can fail. Each layer has documented standards; failures are anticipated; recovery is demonstrated, not assumed.

The architectural shift is not "we have HA infrastructure." It is: **the system is a designed resilient artefact whose failure-mode inventory rather than uptime targets, layered resilience patterns applied per tier, explicit RPO/RTO targets derived from business requirements, chaos engineering practice that surfaces unknown failure modes, and recovery rehearsal that proves recovery actually works determine whether the system is meaningfully resilient or whether resilience is merely an unverified claim — and treating resilience as "we set uptime targets and meet them" produces a system whose first significant failure reveals undesigned-for failure modes, untested recovery paths, and a team that doesn't know what the system actually does when components fail.**

---

## Six principles

### 1. The failure-mode inventory is the load-bearing artefact, not the uptime target

A primitive resilience claim is "we target 99.95% uptime." A production resilience claim is "here are the 24 failure modes we have anticipated, characterised by likelihood and impact, with the resilience pattern that mitigates each documented and verified." The architectural discipline is to *enumerate failures*: dependency failures (databases, caches, queues, external APIs); infrastructure failures (instance, AZ, region, network partition); resource exhaustion (CPU, memory, disk, connection pool, file descriptors, thread pool); coordination failures (clock skew, cache invalidation race, leader election split); load-pattern failures (thundering herd, retry storm, slow consumer back-pressure). For each, the team documents: what triggers it, what its impact is, what resilience pattern is supposed to handle it, how that pattern is verified to actually work. Failures *not* in the inventory are *failures not designed for*; when one occurs, the team learns about a new failure mode and adds it to the inventory. The inventory grows over the system's lifetime; resilience is the inventory's coverage.

#### Architectural implications

- The failure-mode inventory is a versioned, owned document per service. New services start with a baseline inventory drawn from the team's accumulated experience; the inventory is reviewed at major changes (new dependencies, new scale, new traffic patterns).
- Each failure mode has: trigger conditions; impact (which user-facing capability degrades, by how much, for how long); resilience pattern applied; verification mechanism (chaos test, game day, observed past incident).
- Failures discovered in production through incidents are added to the inventory with their incident retrospective as evidence. The inventory becomes the institutional memory of "what we now know fails."
- FMEA (Failure Mode and Effects Analysis) discipline borrowed from reliability engineering: failures rated by severity, occurrence, and detection difficulty; high-priority failures get attention first.

#### Quick test

> Does your most critical service have a documented failure-mode inventory that another engineer could read and understand "here are the failures this system anticipates and how each is handled"? If the answer is "we have an SLO target," the inventory doesn't exist as an artefact; resilience is being measured by aggregate availability rather than designed against specific failure modes.

#### Reference

[Release It! (Nygard)](https://pragprog.com/titles/mnee2/release-it-second-edition/) treats failure-mode enumeration and pattern-per-failure as the foundational discipline of resilient systems. [FMEA — Failure Mode and Effects Analysis](https://en.wikipedia.org/wiki/Failure_mode_and_effects_analysis) brings the systematic enumeration discipline from reliability engineering.

---

### 2. Resilience patterns are applied per layer — timeouts, retries, circuit breakers, bulkheads, fallbacks

Resilience is not a single property; it's a *stack of patterns* applied at different layers, each handling a specific failure class. *Timeouts* prevent a slow dependency from holding resources indefinitely (every external call has a timeout; the timeout is shorter than upstream timeouts so failures propagate with bounded delay). *Retries with exponential backoff and jitter* handle transient failures without amplifying load on the failing dependency. *Circuit breakers* fail fast when a dependency is unhealthy, avoiding repeated calls to a known-broken system; they include the half-open probing logic to detect recovery. *Bulkheads* (named after ship compartments) contain failure within a domain — a runaway request from tenant A doesn't exhaust resources for tenant B because they have separate resource pools. *Rate limiting* protects the service from being overwhelmed by load surges that would otherwise consume all capacity. *Graceful degradation* returns reduced functionality (cached data, default values, partial results) rather than failure when a dependency is unavailable. *Fallback* provides an alternative path when the primary path fails (a stale read from cache, a backup data source, a queued retry for later). The architectural discipline is to *apply the patterns deliberately*, not just because frameworks provide them but because each pattern handles a specific failure class identified in the inventory.

#### Architectural implications

- Each external call (network, database, cache, queue, file system) has a timeout configured. The timeout is set deliberately based on what the caller can wait, not left at a framework default.
- Retry policies are tuned per dependency: which errors are retried (transient yes, business errors no), how many attempts, what backoff policy, what jitter strategy. Retry storms are prevented by jitter.
- Circuit breakers are deployed for dependencies whose failure should not propagate as repeated calls. Half-open state is part of the configuration. Circuit-breaker state is exposed as a metric.
- Bulkhead boundaries are designed: which workloads share which thread pools / connection pools / memory regions; what isolation the bulkhead provides. Bulkheads are tested by overloading one tenant and verifying others are unaffected.

#### Quick test

> Pick the most-trafficked external dependency in your system. Does the call have a timeout, a retry policy with backoff and jitter, a circuit breaker? Do you know what happens if that dependency is fully unavailable — does the system gracefully degrade, return cached data, queue for retry, or hard-fail? If you don't know, the resilience patterns aren't applied at the layer that matters; the failure mode "this dependency is unavailable" isn't designed for.

#### Reference

[Release It! (Nygard)](https://pragprog.com/titles/mnee2/release-it-second-edition/) catalogues the resilience patterns and the failure modes they handle. [Resilience4j](https://resilience4j.readme.io/) and [Polly — .NET resilience library](https://www.thepollyproject.org/) implement the canonical pattern set as composable libraries.

---

### 3. RPO and RTO targets are derived from business requirements per service, not assumed uniformly

A primitive resilience target is "five nines availability for everything." A production resilience target is *per-service* and *derived from business requirements*: the *Recovery Point Objective* (RPO) is how much data the business can afford to lose (1 second for payment transactions; 1 hour for analytics aggregations; 24 hours for backup data); the *Recovery Time Objective* (RTO) is how long the service can be down (30 seconds for the payment path; 30 minutes for the order-history view; hours for non-customer-facing tools). The targets are derived from business impact analysis: what does each minute of downtime cost; what does data loss imply for customers, regulators, business operations; what is the business actually willing to pay (in infrastructure, in operational complexity) to achieve different targets. The architectural discipline is to *vary the targets across services* — uniform targets either over-engineer low-criticality services or under-protect high-criticality ones. Each service's target informs its resilience design: the payment service may run multi-region active-active because RTO of 30 seconds requires it; the analytics service may run single-region with backups because RTO of hours allows it.

#### Architectural implications

- Each service has documented RPO and RTO targets, derived from business impact analysis (not engineering preference). The targets are reviewed when business requirements change.
- The targets *drive* the resilience design: RPO of seconds requires synchronous replication; RPO of hours allows asynchronous backup. RTO of seconds requires automated failover; RTO of hours allows manual recovery.
- The cost of meeting the targets is *part of the target's documentation*: tighter targets cost more in infrastructure, complexity, and operational discipline. The business sees the trade-off explicitly.
- Targets are verified through recovery rehearsal: backup restoration timed; failover drilled; the achieved RPO/RTO compared to the documented target. Drift is surfaced.

#### Quick test

> Pick three services in your organisation. Can you find documented RPO and RTO targets for each, with the business-impact rationale? Are the targets different (because the services have different criticality) or uniform (because no per-service analysis was done)? If uniform, the targets aren't business-derived; they're engineering convenience, and they either over-protect or under-protect every service.

#### Reference

[AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html) treats RPO/RTO derivation from business requirements as a design-time discipline. [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) covers SLO derivation from user-perceived reliability requirements at depth.

---

### 4. Chaos engineering surfaces unknown failure modes before they surface themselves

A primitive belief is that the test suite verifies resilience. Tests verify *what was thought of* — they're a check on the failures the team anticipated. *Chaos engineering* — deliberately injecting failures into production-like or production environments — surfaces failure modes the team *didn't* anticipate. The discipline includes: *failure injection* (kill instances, partition networks, inject latency, fill disks, exhaust connection pools, throttle CPU); *steady-state hypothesis* (what observable property should hold during the failure injection — error rate stays below threshold, latency stays within bound, no data loss); *blast-radius control* (start in non-production; expand to small production slice; expand to wider scope only after lower-blast-radius experiments show resilience). Game days are *coordinated chaos engineering with people* — teams simulate failures, the response is exercised, the surfaced gaps become the priority list. The architectural discipline is to *make chaos engineering routine*, not heroic — the experiments run continuously; the failure modes they discover go into the inventory; the patterns that fail under injection become the engineering priority.

#### Architectural implications

- Chaos experiments are versioned, reviewed, and run on a cadence: weekly low-blast-radius experiments; monthly broader scope; quarterly game days. The cadence is documented.
- Each experiment has a steady-state hypothesis stated before the experiment runs: what property should hold; what would falsify it. The hypothesis is the experiment's outcome criterion.
- Blast radius is explicit: which traffic, which services, which environments. The experiment can be aborted and reverted at any moment if observed impact exceeds the planned blast radius.
- Surfaced failure modes go into the failure-mode inventory; the resilience patterns that didn't hold get prioritised for fixing. The chaos engineering practice produces a pipeline of resilience improvements.

#### Quick test

> Does your team run chaos experiments on a known cadence, or has it been "we should set that up sometime"? If the latter, chaos engineering isn't part of the resilience discipline; the only failures that get surfaced are the ones that occur naturally, which is a slower and more painful learning process.

#### Reference

[Chaos Engineering](https://principlesofchaos.org/) (Principles of Chaos) is the canonical articulation of the discipline. [Game Days (Google SRE)](https://sre.google/sre-book/testing-reliability/) describes the coordinated team exercise discipline.

---

### 5. Recovery is rehearsed, not assumed — backups restored, failovers exercised

The hardest discipline in resilience is *proving the recovery actually works*. Backups taken nightly that have never been restored are a Schrödinger's cat — they may or may not be restorable; the team finds out when they need them. Failover paths designed in architecture documents that have never been exercised similarly may or may not work. The architectural discipline is to *rehearse recovery on a cadence*: backups are restored to a test environment and verified for completeness; database failovers are triggered and the recovery time measured; multi-region failover is exercised and the regional cutover validated. The rehearsals find the gaps: the backup script silently skipping certain tables, the failover that takes 10x the assumed duration, the dependency that doesn't replicate to the secondary region. Each gap is a resilience defect repaired before it becomes an incident.

#### Architectural implications

- Recovery rehearsal cadence is documented per service: backup restoration verified weekly or monthly; failover drilled quarterly; multi-region cutover annually for services that claim regional resilience.
- The rehearsal generates evidence: the timed recovery, the post-recovery validation that data is intact and the service is operational, the lessons captured. The evidence is published — the team can point to "our last backup restoration completed at 14:32 elapsed with full data integrity."
- Gaps surfaced during rehearsal become priority work: missed tables in backup scope, dependencies not in failover plan, runbook steps that don't match current system state.
- Production-like environments are essential for rehearsal: the rehearsal needs to be representative enough that lessons transfer to production. Toy environments produce toy lessons.

#### Quick test

> When was the last time you successfully restored a backup of your most critical database to a working state and verified the data was intact? When was the last time you exercised the regional failover for a service that claims to be regionally resilient? If the answer to either is "I'm not sure" or "we did it once at the design phase," the recovery isn't being rehearsed; the team is trusting that recovery works without evidence.

#### Reference

[AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html) treats recovery rehearsal as a primary practice. [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) covers the discipline in the testing-for-reliability chapter.

---

### 6. Graceful degradation is designed — partial functionality is better than total failure

A primitive system either works or doesn't: when a dependency fails, the system fails. A production system *degrades gracefully*: when a dependency fails, the system continues to operate with reduced functionality. The architectural discipline is to *design degradation deliberately*: which features depend on which dependencies; what happens when each dependency is unavailable; what the user sees when degraded; what the system continues to do that's useful even without the dependency. A search service whose recommendation backend is unavailable can return search results without recommendations rather than failing entirely. A product page whose review service is unavailable can show the product without reviews rather than 500-erroring. A checkout flow whose recommendation service is unavailable can complete checkout without upsells rather than blocking the order. Each degradation is a design decision: what reduced state the system enters, what's communicated to the user, when full functionality is restored.

#### Architectural implications

- Each user-facing capability has a documented dependency map: which dependencies are required (failure means the capability fails) versus which are enhancing (failure means the capability degrades but works).
- The degradation strategies are designed: cached data when the live source is down; default values when personalisation is unavailable; partial results when some sources fail; queued retry when fast path fails. Each strategy is implemented and tested.
- The user-facing communication is designed: when the system is degraded, what does the user see? "Reviews are temporarily unavailable" is better than a generic 500. "Checkout completed but order tracking will appear shortly" is better than blocking checkout.
- The recovery to full functionality is automatic and observable: when the dependency returns, the system stops degrading; metrics surface the moment of return.

#### Quick test

> Pick the most-traffic-receiving page in your system. Enumerate the dependencies it calls. For each, what happens when that dependency is unavailable — does the page return reduced functionality or fail entirely? If most dependencies cause page failure, graceful degradation isn't part of the design; the system is operating in all-or-nothing mode.

#### Reference

[Release It! (Nygard)](https://pragprog.com/titles/mnee2/release-it-second-edition/) treats graceful degradation as a primary resilience pattern. [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) covers degradation design in the chapter on handling overload.

---

## Common pitfalls when adopting resilience playbook thinking

### ⚠️ Resilience claimed via uptime target — no failure-mode enumeration

The team commits to "99.9% uptime" without enumerating which failure modes are designed for. The first significant failure surfaces an undesigned-for failure mode; the uptime claim was hollow.

#### What to do instead

Failure-mode inventory per service: enumerated failures with trigger conditions, impact, resilience pattern, and verification. The inventory is the resilience claim, not the aggregate uptime number.

---

### ⚠️ Resilience patterns applied via framework defaults — not deliberately

Timeouts default to 30 seconds because the framework default is 30 seconds. Retries happen because the SDK retries by default. Circuit breakers don't exist because nobody added them. The patterns aren't applied to specific failure modes; they happen accidentally where the framework provides them and not at all where it doesn't.

#### What to do instead

Each external call has timeout, retry, circuit-breaker policies set deliberately based on the failure mode they're protecting against. Bulkheads designed at workload boundaries. Rate limiting protects under surge. Graceful degradation paths designed.

---

### ⚠️ Uniform RPO/RTO targets across all services

Every service is targeted at "five nines" or "1 minute RTO" without per-service business impact analysis. The result is over-engineering of low-criticality services and under-protection of high-criticality ones, with no rationale either way.

#### What to do instead

Per-service RPO/RTO derived from business impact analysis. Targets vary across services because services have different criticality. The targets drive the resilience design (synchronous replication for tight RPO, asynchronous backup for loose).

---

### ⚠️ Chaos engineering is "we should set that up sometime"

The team relies on the test suite for resilience verification. The test suite checks anticipated failures; chaos engineering would surface unanticipated ones. The latter never gets prioritised.

#### What to do instead

Chaos experiments on a documented cadence (weekly small, monthly broader, quarterly game day). Each experiment has a steady-state hypothesis. Surfaced failures go into the inventory; failed patterns become priority work.

---

### ⚠️ Recovery never rehearsed — backups untested, failovers undrilled

Backups run nightly; nobody has restored one. Failover is documented in architecture; nobody has triggered it. When a real incident requires recovery, the team discovers the gaps.

#### What to do instead

Recovery rehearsal on documented cadence. Backups restored and verified. Failovers triggered and timed. Multi-region cutovers exercised. Gaps repaired before they're needed.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Failure-mode inventory exists per critical service ‖ Enumerated failures with trigger conditions, impact, resilience pattern applied, verification mechanism. The inventory is reviewed at major changes and grows from incident retrospectives. | ☐ |
| 2 | Resilience patterns applied at each layer deliberately ‖ Timeouts on every external call, set to caller-acceptable values. Retries with backoff and jitter. Circuit breakers for dependencies whose failure shouldn't propagate. Bulkheads at workload boundaries. Rate limiting under surge. | ☐ |
| 3 | RPO and RTO targets documented per service from business impact analysis ‖ Targets vary across services because criticality varies. The cost of meeting tighter targets is part of the documentation. The targets drive the resilience design. | ☐ |
| 4 | Targets are verified through periodic measurement ‖ Recovery rehearsals time the achieved RPO/RTO. The achieved values compared to documented targets. Drift surfaces; the targets or the implementation are revised. | ☐ |
| 5 | Chaos engineering practice runs on a documented cadence ‖ Weekly low-blast-radius experiments; monthly broader; quarterly game days. Each experiment has a steady-state hypothesis. Blast radius explicit and revertible. | ☐ |
| 6 | Surfaced failure modes from chaos enter the inventory ‖ Each chaos-discovered failure becomes a documented entry in the failure-mode inventory. The pattern that didn't hold becomes prioritised engineering work. | ☐ |
| 7 | Backup restoration is verified, not assumed ‖ Restored to a test environment on a documented cadence. The restoration is timed; data integrity verified. Gaps in backup scope (skipped tables, missed dependencies) repaired. | ☐ |
| 8 | Failover paths are exercised, not just designed ‖ Database failovers triggered. Multi-region cutovers drilled for services that claim regional resilience. The runbooks tested under realistic conditions; gaps surfaced and fixed. | ☐ |
| 9 | Graceful degradation designed per user-facing capability ‖ Dependency map: required vs enhancing dependencies for each capability. Degradation strategies designed (cached data, default values, partial results). User-facing communication designed for degraded states. | ☐ |
| 10 | The resilience design itself is a versioned, owned artefact ‖ The failure-mode inventory, RPO/RTO targets, chaos experiment cadence, recovery rehearsal cadence are documented per service. The artefact has an owner and a revision history. Resilience is auditable. | ☐ |

---

## Related

[`playbooks/api-lifecycle`](../api-lifecycle) | [`playbooks/migration`](../migration) | [`technology/ha-dr`](../../technology/ha-dr) | [`runbooks/incident`](../../runbooks/incident) | [`observability/sli-slo`](../../observability/sli-slo)

---

## References

1. [Release It! (Nygard)](https://pragprog.com/titles/mnee2/release-it-second-edition/) — *pragprog.com*
2. [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) — *sre.google*
3. [Chaos Engineering](https://principlesofchaos.org/) — *principlesofchaos.org*
4. [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html) — *docs.aws.amazon.com*
5. [Resilience4j](https://resilience4j.readme.io/) — *resilience4j.readme.io*
6. [Polly — .NET resilience library](https://www.thepollyproject.org/) — *thepollyproject.org*
7. [Circuit Breaker (Fowler)](https://martinfowler.com/bliki/CircuitBreaker.html) — *martinfowler.com*
8. [Bulkhead Pattern (Microsoft)](https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead) — *learn.microsoft.com*
9. [FMEA — Failure Mode and Effects Analysis](https://en.wikipedia.org/wiki/Failure_mode_and_effects_analysis) — *en.wikipedia.org*
10. [Game Days (Google SRE)](https://sre.google/sre-book/testing-reliability/) — *sre.google*
