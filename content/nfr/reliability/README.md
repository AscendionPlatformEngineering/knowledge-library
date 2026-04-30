# Reliability NFRs

The strategic guide for reliability non-functional requirements — recognising that the team's availability targets specified as service-level objectives with explicit error budgets rather than aspirational uptime numbers, the failure-mode catalogue that enumerates known ways the system can degrade and the response-pattern committed for each rather than treating failure as an unspecified emergent surprise, the recovery-objective targets stated as RTO and RPO with rationale rather than left as adjectives, the partial-availability and graceful-degradation envelopes that distinguish "fully working" from "core flows working" from "read-only mode" from "down," the explicit articulation of which dependencies are tightly coupled and which are degraded-tolerant rather than treating every dependency as equally critical, and the budget-violation-as-architectural-signal interpretation that treats SLO breaches as work to schedule or targets to renegotiate are what determine whether the team's reliability posture is calibrated against what users actually need from the system or whether the system pursues nine-nines availability for paths users use rarely while routinely failing on the paths users care about most.

**Section:** `nfr/` | **Subsection:** `reliability/`
**Alignment:** ISO/IEC 25010 (Software Quality Model) | Google SRE Book | Google SRE Workbook | AWS Well-Architected Reliability Pillar | DORA Capabilities
---

## What "reliability NFRs" means — and how it differs from observability and incident response

A *primitive* approach to reliability is to publish a "99.9% uptime" commitment in a one-pager, build the system without explicit failure-mode planning, and treat each production incident as an unforeseen surprise. After every incident, the post-mortem reveals that the failure mode was foreseeable in retrospect, the team adds a new monitoring rule, and the practice accumulates ad-hoc countermeasures without a coherent reliability model. After eighteen months, the system has hundreds of monitoring rules and tens of runbooks but no architectural answer to the question "how reliable should this actually be, and which kinds of failure are we explicitly engineered to handle?"

The *architectural* alternative is to treat reliability as a contract specifying *how reliable*, *under what failure conditions*, with *what recovery characteristics*, and *what graceful-degradation envelope*. The contract is a set of measurable targets — service-level objectives, error budgets, recovery-time objectives, recovery-point objectives — paired with a catalogue of failure modes the system is engineered to handle and the response pattern committed for each. The contract makes explicit what the system promises and what it does not. Promises that are not made are not failures of the contract; they are out-of-scope events that the team has decided not to engineer for, and the decision is itself architectural.

This is *not* the same as [observability and incident response](../../observability/incident-response) — those pages cover the operational practices of detecting and responding to live failures. This page is about the *targets* observability instruments measure against, and the *failure modes* incident response runbooks address. Observability tells you what is happening; reliability NFRs tell you whether what is happening matches the contract.

This is also *not* the same as [reliability runbooks](../../runbooks/incident) — runbooks are the response procedures for specific incident types. The reliability NFRs are the architectural decisions about which failure types the system commits to handle gracefully and which it does not, which then drive what runbooks must exist.

The architectural signature of well-specified reliability NFRs is *intentional gracefulness*. When the failure-mode catalogue and degradation envelope are explicit, a particular failure produces a defined system response that users observe as gracefully reduced functionality rather than as an outage. When the catalogue is implicit, the same failure produces an uncontrolled cascade because no one specified what should happen when the dependency is unavailable. The difference is rarely a code-quality issue; it is whether the architectural decision was made and documented.

## Six principles

### 1. Specify availability as service-level objectives with explicit error budgets, not as uptime aspirations
"99.9% uptime" without further specification is meaningless. Uptime over what window? Measured at which boundary (the load balancer, the API endpoint, the user-perceivable result)? Counting which kinds of failure (full outage, slow responses, error responses, partial-feature failure)? An aspirational uptime number does not define a contract; it defines a marketing claim.

The architectural form is the service-level objective: at the named user-facing boundary, this fraction of requests must be successful (defined by the user-facing success criterion) within this latency, measured over this rolling window. The complement of the SLO is the error budget — the volume of failure permitted in the period — which is the operational currency teams spend when they take risk (deploying changes, running game days, running migrations) and conserve when budget is depleted. The error budget makes risk-versus-velocity tradeoffs explicit and quantitative.

#### Architectural implications
SLO-grade specification requires the user-facing success criterion to be observable in real time. "Successful API response" is sufficient when the API is the user; for systems where the user is downstream of several APIs, the SLO must be specified at the boundary the user actually experiences (typically synthetic transactions or real-user monitoring data). The instrumentation pre-requisite is non-trivial; without it, the SLO is a number on a spreadsheet rather than a real-time contract.

#### Quick test
Look at your reliability commitment. Is it expressed as an SLO with named user-facing success criterion, measurement boundary, latency threshold, and rolling window? Or is it an uptime percentage without those qualifiers? If the latter, the spec is not a contract.

### 2. Catalogue failure modes explicitly with committed response patterns
A reliability NFR document should enumerate the failure modes the system is engineered to handle. Network partition between two regions: the system fails over to the surviving region within RTO of N minutes. Primary database unavailable: read-only mode activates within N seconds; writes queue and retry. Third-party payment service unavailable: order placement degrades to confirmation-pending state and retries asynchronously. Cache cluster unavailable: requests fall back to origin with documented latency degradation.

For each failure mode, the document specifies the trigger condition (how the system detects it), the response pattern (what the system does when it detects), the user-observable behaviour (what users see), and the recovery procedure (what runs to restore full operation). Failure modes not in the catalogue are not engineered for, which is itself a decision; users encountering an uncatalogued failure see undefined behaviour, and the post-incident response is to either add the mode to the catalogue or accept that it remains uncatalogued.

#### Architectural implications
The catalogue forces the architectural conversation about which failures are common enough to engineer for. Engineering for every conceivable failure is impossibly expensive; engineering for none is operationally fragile. The catalogue is a deliberate choice within that spectrum. The choice is reviewed when failure-mode evidence accumulates (incidents reveal a mode we did not anticipate; we add it to the catalogue or decide not to).

#### Quick test
Pick a recent production incident. Was the failure mode in your published catalogue? If yes, did the system respond as the catalogue committed? If the mode was not catalogued, was a decision made post-incident either to add it or to leave it out, with rationale? If neither happened, the catalogue is not active and the reliability practice is reactive rather than architected.

### 3. State recovery objectives — RTO and RPO — per workload, not per system
Different workloads have different recovery requirements. A real-time trading system might need RTO ≤ 30 seconds and RPO = 0 (no data loss). A batch reporting system might tolerate RTO ≤ 4 hours and RPO ≤ 24 hours (overnight data acceptable). A static content distribution system might have RTO ≤ 5 minutes and RPO = 0 (content is reproducible from upstream, so loss is recoverable). A single system-wide RTO/RPO is wrong for at least some workloads.

The discipline is to publish per-workload RTO and RPO with rationale tied to business consequence. The recovery-time investment for each workload follows: tighter RTO requires hot standby and automated failover; relaxed RTO permits cold standby and manual procedures, which are an order of magnitude cheaper. Aggregating to a single system RTO either over-invests in workloads that can tolerate slow recovery or under-invests in those that cannot.

#### Architectural implications
RTO and RPO targets drive concrete platform choices: synchronous versus asynchronous replication, hot versus warm versus cold standby, automated versus runbook-driven failover. The cost gradient across these choices is steep. The per-workload matrix prevents the platform from being either over-built (expensive standby for everything) or under-built (single-region hope for things that needed multi-region).

#### Quick test
Ask "what is the RTO for workload X" for three workloads of different criticality. If the answer is the same for all three, the workloads are not differentiated. If the answer is "we don't have one stated for that workload," the spec is incomplete and recovery investment is being made without a target.

### 4. Specify the degradation envelope — what "still working" means at progressive failure levels
A binary up-or-down characterisation of system state is too coarse for systems of any complexity. Real systems have progressive degradation envelopes: fully functional → core flows only → read-only → severely degraded → unavailable. Each envelope corresponds to a different failure scenario and a different user expectation. A user accessing an e-commerce site during a partial outage expects that browsing and reading product detail still work even if checkout has been disabled — this is the read-only envelope being intentional.

The discipline is to specify the envelope levels: which features are guaranteed at "core flows only," which at "read-only," which at "severely degraded." The envelope levels are tied to specific failure modes (cache out → read-only is acceptable; primary database out → core flows only; both out → severely degraded). Users see a stable degradation behaviour during partial failures rather than a chaotic mix of working and broken features.

#### Architectural implications
The envelope drives architectural choices about feature-flag boundaries, dependency-isolation patterns, and synchronous-versus-asynchronous communication. A feature flag that disables non-essential features under degraded mode is the operational instrument of the envelope. Bulkheads that isolate non-essential dependencies prevent their failure from affecting essential flows. The envelope without these architectural patterns is theoretical; the patterns without the envelope are unfocused.

#### Quick test
For a representative dependency failure (cache cluster out), what does your system do? Is the response specified in the NFR document? If "the system goes down because the cache is unavailable" is the implicit response, the dependency is tightly coupled and the degradation envelope is not designed.

### 5. Distinguish tightly-coupled from degraded-tolerant dependencies
Every dependency is on a spectrum from "if it fails, we fail" (tightly coupled) to "if it fails, we degrade gracefully" (degraded-tolerant). The architectural choice for each dependency is which side of the spectrum it sits on, and the choice has cost: degraded-tolerance requires bulkheads, fallbacks, queuing, and circuit-breaking, all of which are engineering work. Tight coupling is the cheap default; engineers do not make tight coupling happen, they fail to engineer the alternative.

The discipline is to inventory dependencies and declare each one's coupling treatment. The trading-engine inventory: market-data feed (tightly coupled — without it, no trading), risk-checking service (tightly coupled — without it, no order acceptance), audit-log service (degraded-tolerant — buffer locally and replay), notification service (degraded-tolerant — best-effort), product-catalogue cache (degraded-tolerant — fall back to authoritative store with latency penalty). The inventory is itself an artefact, reviewed when dependencies change.

#### Architectural implications
The coupling treatment of each dependency directly determines the system's blast radius from its failure. A tightly coupled dependency means the system's availability is bounded by that dependency's availability; you cannot exceed it. A degraded-tolerant dependency means the system can be more available than the dependency. The math: a system tightly coupled to three dependencies each at 99.9% availability has at-best 99.7% availability (1 - 3 × 0.001). Awareness of this math drives the architectural choice of which dependencies to harden.

#### Quick test
For your highest-traffic service, name the tightly coupled dependencies and the degraded-tolerant ones. If the answer is "all of them are tightly coupled" without that being a deliberate choice, the architecture has not differentiated and the system's availability is the floor of the worst dependency's availability.

### 6. Treat error-budget burn rate as architectural signal, not as performance shame
When an error budget is being consumed faster than the rolling window replenishes it, the architectural conversation is: why? Is the system absorbing more change than usual (legitimate burn from feature delivery)? Is a specific failure mode escalating in frequency (signal that the catalogue needs a new entry or an existing entry needs hardening)? Is the SLO target itself wrong for the actual workload (signal that the target needs revision rather than the system needs hardening)? All three are valid responses; the wrong response is to treat budget burn as performance shame and rush patches without understanding the cause.

The discipline is the burn-rate review: when burn-rate exceeds threshold, an architectural review examines the failure-mode trajectory and either schedules hardening work, revises the SLO with rationale, or decides the burn is within acceptable risk envelope. The decision is recorded; the burn-rate trajectory across reviews becomes the meta-signal — burn that is rising without being explained is the architectural-debt-in-reliability indicator.

#### Architectural implications
The burn-rate review needs cross-functional participation: reliability engineering for the failure-mode trajectory, product for the user-impact assessment, engineering for the hardening cost estimate. Without that triad, the review degrades to one-side conversations and the decisions become biased. The review cadence (typically weekly or biweekly during active burn, less frequent in healthy state) and the explicit decision categories (harden / revise / accept) are the architectural instruments.

#### Quick test
At your last burn-rate review, was a recorded decision made (harden / revise / accept), with rationale and a named owner? If burn is being tracked but no decision-record exists, the review is observation without action and the budget is decoupled from architectural change.

## Five pitfalls

### ⚠️ Specifying uptime as an aspirational percentage without SLO grounding
"99.9% uptime" without measurement-boundary, success-criterion, and rolling-window specification is marketing language, not a contract. It cannot be validated; it cannot be budgeted. The fix is the SLO formulation: at this measurement boundary, this fraction of requests must succeed (by named criterion) within this latency, measured over this window.

### ⚠️ Treating failure as an unspecified surprise rather than a catalogued response pattern
Without a failure-mode catalogue, every production incident is treated as a novel emergency. The team accumulates ad-hoc countermeasures without a coherent reliability model. The fix is the explicit failure-mode catalogue with committed response patterns; new failure types either get added to the catalogue with a decision or get explicitly excluded.

### ⚠️ Single system-wide RTO/RPO ignoring workload heterogeneity
Different workloads have different recovery requirements. A trading engine and a reporting system should not have the same RTO. A single number wastes investment on workloads that can tolerate slow recovery and under-invests in those that cannot. The fix is the per-workload RTO/RPO matrix with rationale tied to business consequence.

### ⚠️ Binary up-or-down state instead of progressive degradation envelope
Real systems degrade in stages. A binary characterisation is too coarse to describe what the system does under partial failure, which means the architectural design cannot deliberately produce graceful degradation. The fix is the explicit envelope levels (fully functional → core flows → read-only → severely degraded) with feature-flag and bulkhead architecture supporting each level.

### ⚠️ Treating all dependencies as tightly coupled without choosing
Tight coupling is the default; degraded-tolerance is engineered. Without an explicit coupling inventory, the system's availability is bounded by the worst dependency's availability, often without the team realising it. The fix is the dependency-coupling inventory: each dependency declared as tightly coupled or degraded-tolerant, with the engineering work for tolerance present where declared.

## Reliability NFR specification checklist

| # | Check | Status |
|---|---|---|
| 1 | Availability is specified as SLO with measurement boundary, criterion, latency, and window | ☐ |
| 2 | Error budget is published with named consumption rules | ☐ |
| 3 | Failure-mode catalogue exists with response pattern per mode | ☐ |
| 4 | RTO and RPO are specified per workload with rationale | ☐ |
| 5 | Degradation envelope levels are documented with per-level feature scope | ☐ |
| 6 | Dependency-coupling inventory declares each dependency tightly-coupled or tolerant | ☐ |
| 7 | Engineering for degraded-tolerance is present where declared (bulkheads, fallbacks) | ☐ |
| 8 | SLO measurement infrastructure runs in production at the named boundary | ☐ |
| 9 | Burn-rate review cadence is established with cross-functional participation | ☐ |
| 10 | Burn-rate review decisions (harden / revise / accept) are recorded with rationale | ☐ |

## Related

- [Maintainability NFRs](../maintainability) — sister page on code-health and change-velocity requirements
- [Performance NFRs](../performance) — sister page on latency, throughput, and saturation requirements
- [Security NFRs](../security) — sister page on confidentiality, integrity, and authentication requirements
- [Usability NFRs](../usability) — sister page on user-facing quality requirements
- [NFR Scorecard](../../scorecards/nfr) — the scoring instrument applied across all NFR categories
- [Observability: SLI / SLO](../../observability/sli-slo) — instrumentation that measures against these targets
- [Observability: Incident Response](../../observability/incident-response) — operational practice during failure
- [Runbooks: Incident](../../runbooks/incident) — response procedures for specific failure types
- [Runbooks: Rollback](../../runbooks/rollback) — recovery procedures triggered by RTO/RPO targets
- [Patterns: HA / DR](../../system-design/ha-dr) — architectural patterns supporting reliability targets

## References

1. [ISO/IEC 25010 (Software Quality Model)](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010) — *iso25000.com*
2. [Google SRE Book](https://sre.google/sre-book/table-of-contents/) — *sre.google*
3. [Google SRE Workbook](https://sre.google/workbook/table-of-contents/) — *sre.google*
4. [Google SRE Workbook — SLOs](https://sre.google/workbook/implementing-slos/) — *sre.google*
5. [Error Budget Policy (Google SRE)](https://sre.google/workbook/error-budget-policy/) — *sre.google*
6. [The Four Golden Signals (Google SRE)](https://sre.google/sre-book/monitoring-distributed-systems/) — *sre.google*
7. [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html) — *aws.amazon.com*
8. [DORA Capabilities Catalog](https://dora.dev/capabilities/) — *dora.dev*
9. [Game Days (Google SRE)](https://sre.google/sre-book/testing-reliability/) — *sre.google*
10. [Continuous Architecture in Practice](https://www.oreilly.com/library/view/continuous-architecture-in/9780136523710/) — *oreilly.com*
