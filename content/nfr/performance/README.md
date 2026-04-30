# Performance NFRs

The strategic guide for performance non-functional requirements — recognising that the team's percentile-based latency targets specified at P50 / P95 / P99 rather than averages that hide tail behaviour, the throughput targets stated at sustained-load conditions rather than peak-burst conditions that mask graceful-degradation failures, the resource-saturation budgets specified per system stage rather than aggregated end-to-end, the explicit articulation of trade-offs between latency and throughput and cost rather than averaging-them-away in a composite performance score, the load-pattern characterisation that distinguishes synchronous user-facing traffic from background-batch traffic, and the budget-violation-as-architectural-signal interpretation that treats threshold breaches as either work to schedule or targets to renegotiate are what determine whether the team's performance posture stays calibrated with what users actually experience or whether the system passes test-environment load tests while users see a degraded production system because the load-test profile never matched the actual production traffic shape.

**Section:** `nfr/` | **Subsection:** `performance/`
**Alignment:** ISO/IEC 25010 (Software Quality Model) | Web Vitals (Google) | Google SRE Workbook | Brendan Gregg Performance Tools
---

## What "performance NFRs" means — and how it differs from observability metrics

A *primitive* approach to performance is to write "the system shall be fast" in a design document, run a load test before launch, see numbers that look reasonable, and ship. After launch, users complain that the system is slow under conditions the load test did not exercise — a particular query pattern, a particular tenant size, a particular time of day. The team adds optimisation patches in response to each complaint. After a year, the codebase is full of localised optimisations whose interactions are unmodelled, the original performance contract is forgotten, and any change to the system risks an unpredicted performance regression because there is no definitive answer to "how fast should this actually be."

The *architectural* alternative is to specify performance as a set of measurable contracts: at this load profile, this percentile of requests must complete within this latency budget, with this resource utilisation ceiling, on this hardware envelope. Each clause of the contract is a measurable target with a measurement instrument and a defined load condition. The targets are reviewed at architectural altitude (does the business need P99 of 200 ms, or is P95 of 500 ms acceptable, given what users do with the system?) and validated by load tests whose profiles match production traffic shape, not synthetic-uniform-traffic profiles.

This is *not* the same as [observability metrics](../../observability/metrics) — those pages cover what to instrument and how to read production telemetry. This page is about what *targets* the metrics should be evaluated against — the contract the system is built to meet. Observability tells you what is happening; performance NFRs tell you whether what is happening matches what was specified.

This is also *not* the same as the [NFR Scorecard](../../scorecards/nfr) — that page is the scoring instrument across all NFR categories at programme altitude. This page is one of the dimensions the scorecard scores, with the discipline-specific guidance on how to specify and validate performance targets.

The architectural signature of well-specified performance NFRs is *production-test alignment*. When the load-test profile actually matches production traffic shape, a load test that passes correlates with production performance that meets target. When the load-test profile is generic — uniform request rates, equal-sized payloads, single tenant, repeating queries — the load test passes routinely but tells you nothing about whether production will hold. Bridging that gap is the architectural work that makes performance NFRs actually predictive.

## Six principles

### 1. Specify percentiles, not averages — and always include the tail
"Average response time shall be under 250 ms" is a near-meaningless target. An average can be dragged down by a fast majority while a slow tail damages user experience for the few users hitting it. P50 (median), P95, and P99 together describe the latency *distribution*; the tail (P99 and beyond) is where most user-experience pain lives in a healthy system. A target without a P99 specification is not actually constraining tail behaviour, which is what users feel.

The discipline is to specify P50 / P95 / P99 explicitly per endpoint or per workflow. The targets at each percentile are different — a search query might have P50 ≤ 50 ms, P95 ≤ 200 ms, P99 ≤ 800 ms — and the relative shape of the distribution is itself an architectural choice. A flat distribution (P50 close to P99) implies high consistency at the cost of some median speed; a steep distribution (P50 fast, P99 much slower) implies fast typical case with occasional slow outliers. Different domains favour different shapes; the explicit spec captures the intent.

#### Architectural implications
Specifying tail behaviour creates back-pressure on architectural choices that produce nondeterministic latency: garbage collection pauses, network retries, database lock contention, cache misses to cold storage. Each of these contributes to the tail more than to the median. A system designed for tight tail latency makes different trade-offs (statically allocated structures, request shedding under load, hedged requests, latency-bounded cache strategies) than one designed only for median speed.

#### Quick test
Look at the most recent performance specification document. Does it state P95 and P99 targets explicitly? If only an average or P50 is specified, the spec is not constraining the tail and the team is unprotected against latency outliers in production.

### 2. State the load condition under which targets must hold
Latency targets without load specification are not meaningful. P99 ≤ 200 ms at one request per second is a different requirement than P99 ≤ 200 ms at one thousand requests per second sustained for an hour. The same code may meet the first and miss the second by an order of magnitude. The architectural target must include the load envelope: rate, concurrency, sustain duration, payload distribution.

The discipline is to characterise three load conditions per workload: typical (median production traffic shape), peak (the load expected on the busiest hour of the busiest day), and sustained-stress (peak load held for the duration of a typical traffic spike, measuring whether the system holds rather than degrades). Targets are specified per condition; each condition is exercised in load testing with a profile that matches the production traffic *shape*, not just the magnitude.

#### Architectural implications
Load characterisation requires production traffic analysis. The team that does not measure the actual distribution of request sizes, query shapes, tenant sizes, and time-of-day curves cannot construct realistic load profiles. The instrumentation effort is non-trivial and is often deferred — but it is the gating dependency for performance NFRs that are actually validated rather than rubber-stamped.

#### Quick test
Look at the most recent load test report. Was the load profile derived from production traffic statistics, or was it a synthetic uniform pattern? If synthetic, the load test outcome is decoupled from production performance.

### 3. Decompose end-to-end latency budgets into per-stage budgets
A user-facing request budget of 250 ms typically traverses: network ingress (5–20 ms), authentication (5–10 ms), business logic (50–100 ms), data access (50–150 ms), serialisation and egress (5–10 ms). Each stage has its own budget and its own measurement instrument. Specifying only the end-to-end target leaves no architectural guidance about which stage is allowed to consume what share, which means optimisation efforts are spent on whichever stage happens to be obvious rather than the one that has overrun its budget.

The discipline is to publish the per-stage budget as an architectural artefact alongside the end-to-end target. Each stage's budget is validated independently (component-level tests measure stage latency in isolation); the end-to-end target is validated by integration tests that compose them. When a stage overruns its budget, the architectural decision is clear: optimise that stage, or renegotiate the end-to-end target — not optimise an unrelated stage to compensate.

#### Architectural implications
Per-stage budgets force conversation about ownership and trade-offs. A stage owned by an upstream team may have its budget set elsewhere; this page's team negotiates with that team rather than absorbing the cost silently. Database query budgets may impose schema-design constraints; serialisation budgets may impose payload-shape constraints; each constraint is visible because the budget is.

#### Quick test
Pick a recent performance-relevant feature. Does the design document specify how the latency budget decomposes across stages? If only the end-to-end number is stated, the per-stage trade-offs are implicit and unmanaged.

### 4. Distinguish synchronous user-facing traffic from background batch traffic
The performance regime for synchronous user-facing requests is fundamentally different from the regime for background batch processing. User-facing requests have hard tail-latency targets; batch jobs have throughput targets and soft latency tolerance (measured in seconds or minutes rather than milliseconds). Mixing the two on the same target sheet produces incoherent specifications: a P99 ≤ 200 ms target makes no sense for a nightly ETL job; a throughput target of 10K records/second makes no sense for a single-user-request endpoint.

The discipline is to write performance specifications by traffic class. Synchronous user-facing endpoints get percentile-based latency targets at specified load. Background batch jobs get throughput targets and completion-window targets (the job must finish within X hours). Asynchronous user-facing operations (uploads, generation tasks) get a hybrid: queue-arrival latency target for the synchronous portion, and completion-time target for the asynchronous portion.

#### Architectural implications
Mixing classes on shared infrastructure produces noisy-neighbour effects: a batch job consuming database I/O degrades user-facing query latency. The traffic-class taxonomy in the NFR document drives the isolation architecture: separate connection pools, separate read replicas, separate compute nodes, or scheduled batch windows. The taxonomy is not just for documentation; it informs the platform topology.

#### Quick test
Look at the performance NFR document for any subsystem that handles both user requests and batch processing. Are the targets for the two classes specified separately? If they are aggregated, the document cannot guide isolation architecture.

### 5. Treat resource-saturation budgets as first-class targets, not just outcomes
Latency and throughput are observable from outside the system. Resource saturation (CPU utilisation, memory pressure, connection-pool depth, database lock contention) is observable from inside, and is the leading indicator of performance failure under load increase. A system at 90% CPU with current latency targets met is in a different state than the same system at 50% CPU with the same latency — the first will fail at the next load spike, the second has headroom.

The discipline is to specify resource-saturation ceilings as part of the performance contract. CPU utilisation under steady state ≤ 60%; memory pressure ≤ 70%; connection-pool depth ≤ 50% of maximum; database lock-wait-time as a fraction of total query time ≤ 5%. These ceilings encode the *headroom* the system maintains and turn capacity-planning from reactive (we ran out, scale now) into proactive (we approached the ceiling, plan the next capacity step).

#### Architectural implications
Saturation ceilings drive scaling-event triggers. An autoscaling policy keyed to CPU=60% rather than CPU=90% scales earlier and avoids latency degradation. A connection-pool sized so 50% utilisation is steady-state means the pool is one configuration parameter away from accommodating a 2× traffic spike without code changes. The ceilings shape the operational envelope as much as the latency targets shape the user experience.

#### Quick test
For your performance-critical service, name the resource-saturation ceilings stated in the NFR document. If the answer names only "CPU and memory autoscaling" without specific thresholds, the ceilings are at-best implicit and the operational envelope is not architecturally specified.

### 6. Validate target predictiveness against production observation
A performance NFR document is only as good as the correspondence between its targets and what users actually experience. The validation loop is: production telemetry measures real performance, the measurements are compared to the target sheet, deviations are analysed, and either the system is corrected (the target is what we want, and we are not meeting it) or the targets are corrected (production reveals that the original target was wrong for the actual workload). Without the loop, the targets become a document people read once at design time and never reconcile with reality.

The discipline is to run a target-versus-observation review at a regular cadence — typically tied to the release cycle or quarter — that compares production percentiles, throughput, and saturation to the documented targets, and either schedules remediation or revises the targets with rationale. Revisions are themselves architectural decisions, recorded as ADRs, with the trajectory of target revisions itself a meta-signal: a target that has been relaxed three times is a target the system was probably never going to meet, and the architectural conversation should focus on the design choices that made that target unrealistic.

#### Architectural implications
The validation loop requires production telemetry of a quality that supports percentile reporting. Average response time is not enough; tracing-grade telemetry that captures full distributions per endpoint per traffic class is the dependency. Many teams do not have this; the architectural choice is whether to invest in the telemetry infrastructure (which then unlocks performance NFR validation) or to accept that the targets will remain unvalidated.

#### Quick test
At your last release-readiness review, was a target-versus-observation reconciliation performed? If yes, was at least one target updated based on production findings? If neither happened, the validation loop is not running and the targets are uncorrelated with reality.

## Five pitfalls

### ⚠️ Specifying averages instead of percentiles
The most common performance-NFR failure. An average is dragged down by a fast majority and obscures tail behaviour, which is what users experience as "slow." The fix is the explicit P50 / P95 / P99 specification per workload. A target sheet without P99 is not constraining the tail, which is where production user pain lives.

### ⚠️ Load testing with synthetic uniform traffic profiles
Synthetic load is faster to construct and produces clean numbers, but its results do not predict production performance. Production traffic has heterogeneous payload sizes, query patterns, tenant distributions, and time-of-day shapes; the synthetic profile washes all of these into noise. The fix is production-derived load profiles for at least the critical workloads, with synthetic profiles relegated to lower-tier validation.

### ⚠️ Treating performance as one composite score
A single performance score aggregating latency / throughput / saturation has the same problem as a single maintainability score: it is uninterpretable when it changes because the contributing inputs are decoupled. The fix is to keep latency, throughput, and saturation as separate dimensions in the target sheet and report them separately.

### ⚠️ Optimising whichever stage is obvious rather than the one over budget
Without per-stage latency budgets, optimisation effort gravitates to whichever stage is most visible (usually application code), not whichever stage is over its budget (which may be database access or network ingress). The result is application code that is increasingly optimised against parts of the system that were not the bottleneck. The fix is the per-stage budget published as an architectural artefact and validated by stage-isolated component tests.

### ⚠️ Letting saturation creep without ceilings
A system running at 85% CPU under typical load has no headroom for spikes. Without an explicit ceiling, saturation creeps upward with each release as features are added, until the next traffic spike causes a cascade of latency failures. The fix is the explicit saturation ceiling as a first-class target; scaling events are triggered when the ceiling is approached, not when latency has already degraded.

## Performance NFR specification checklist

| # | Check | Status |
|---|---|---|
| 1 | Latency targets are specified at P50, P95, and P99 per workload | ☐ |
| 2 | Each target states the load condition (rate, concurrency, sustain duration) | ☐ |
| 3 | End-to-end latency budgets decompose into per-stage budgets | ☐ |
| 4 | Synchronous and batch traffic classes have distinct target sheets | ☐ |
| 5 | Resource-saturation ceilings are specified (CPU, memory, pool depth) | ☐ |
| 6 | Load-test profiles are derived from production traffic statistics | ☐ |
| 7 | Production telemetry supports percentile reporting per workload | ☐ |
| 8 | Target-versus-observation reconciliation runs at release cadence | ☐ |
| 9 | Target revisions are recorded as ADRs with rationale | ☐ |
| 10 | Saturation-ceiling-approach triggers scaling events before latency degrades | ☐ |

## Related

- [Maintainability NFRs](../maintainability) — sister page on code-health and change-velocity requirements
- [Reliability NFRs](../reliability) — sister page on availability and graceful-degradation requirements
- [Security NFRs](../security) — sister page on confidentiality, integrity, and authentication requirements
- [Usability NFRs](../usability) — sister page on user-facing quality requirements
- [NFR Scorecard](../../scorecards/nfr) — the scoring instrument applied across all NFR categories
- [Observability: SLI / SLO](../../observability/sli-slo) — the production telemetry that validates these targets
- [Observability: Metrics](../../observability/metrics) — the instrument that produces the percentile measurements
- [Templates: ADR Template](../../templates/adr-template) — how target revisions are recorded as decisions

## References

1. [ISO/IEC 25010 (Software Quality Model)](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010) — *iso25000.com*
2. [Web Vitals (Google)](https://web.dev/articles/vitals) — *web.dev*
3. [Google SRE Workbook — SLOs](https://sre.google/workbook/implementing-slos/) — *sre.google*
4. [The Four Golden Signals (Google SRE)](https://sre.google/sre-book/monitoring-distributed-systems/) — *sre.google*
5. [Brendan Gregg Performance Tools](https://www.brendangregg.com/perf.html) — *brendangregg.com*
6. [Multi-Window Multi-Burn-Rate Alerts (Google SRE)](https://sre.google/workbook/alerting-on-slos/) — *sre.google*
7. [Continuous Architecture in Practice](https://www.oreilly.com/library/view/continuous-architecture-in/9780136523710/) — *oreilly.com*
8. [Quality Attribute Workshop (SEI)](https://insights.sei.cmu.edu/library/quality-attribute-workshop-third-edition-participants-handbook/) — *sei.cmu.edu*
9. [arc42 Architecture Template](https://arc42.org/) — *arc42.org*
10. [DORA Capabilities Catalog](https://dora.dev/capabilities/) — *dora.dev*
