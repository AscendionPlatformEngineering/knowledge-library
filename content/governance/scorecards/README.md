# Governance Scorecards

The metrics that tell you whether the governance system itself is working — not whether the architecture it produces is good (that's a different question covered elsewhere), but whether the governance system is doing its job: making decisions in reasonable time, catching the issues it should catch, adapting as the organisation evolves, and earning its keep without becoming theatre.

**Section:** `governance/` | **Subsection:** `scorecards/`
**Alignment:** DORA Metrics | COBIT 2019 (ISACA) | TOGAF | AWS Well-Architected Framework

---

## What "governance scorecards" actually means

The term *scorecard* is overloaded across the architecture domain. There are *technical scorecards* — measurements of the architecture's outputs (this service's reliability score, this system's maturity rating, this team's quality posture) — and they're covered in the top-level [`scorecards/`](../../scorecards) section. There are *engineering scorecards* — DORA metrics, deployment frequency, change-failure rate, lead time for changes — and they live in the operational lane. This page is about a third kind: scorecards that measure **the governance system itself**. Is it making decisions fast enough? Are the standards it produces adopted in practice or just on paper? When it grants exceptions, what does the exception rate tell us about the rules? When it approves decisions, are those decisions still considered good a year later?

A *primitive* governance system has no scorecards: leadership has a vague sense of whether things are working, escalations happen when they break loudly, and otherwise the system runs on tradition. A *measured* governance system has scorecards that surface its own health: lead time per decision class, queue depth and trend, exception rate per standard, adoption rate per pattern, retrospective decision quality. The metrics aren't decoration — they're the operational interface that lets the governance system see itself, identify where it's serving the organisation poorly, and adapt deliberately.

The architectural shift is not "we added some metrics." It is: **the governance system has operational properties of its own — responsiveness, accuracy, adoption, durability — and measuring these properties is what distinguishes a governance system that improves over time from one that calcifies and gradually loses legitimacy.**

---

## Six principles

### 1. Process metrics and outcome metrics are both needed — measuring only one produces predictable failure modes

A governance system can be measured on its *process* (how it runs: lead time, queue depth, throughput, completion rate) or on its *outcomes* (what it produces: decision quality, regret rate, exception trend over time). Each axis has its failure mode when used alone. *Process-only* measurement produces a system that's fast, throughput-rich, and may be making bad decisions efficiently — every decision is rapid; nobody asks if the decisions were good. *Outcome-only* measurement produces a system that's deliberative and possibly never decides — every decision is carefully evaluated; the lead time grows until teams give up and route around the system. The two metrics balance each other: process metrics expose responsiveness problems; outcome metrics expose quality problems. A governance scorecard that tracks both, weighted toward outcomes (because outcomes are what ultimately matter) but with process metrics surfaced for tactical management, is the architectural answer.

#### Architectural implications

- The scorecard tracks both process metrics (lead time, queue depth, throughput, completion) and outcome metrics (decision quality on retrospective review, exception rate, regret rate).
- Outcome metrics are weighted more heavily than process metrics in any aggregate health score — fast bad decisions are worse than slow good ones.
- Process and outcome metrics are reviewed together: a deteriorating outcome in the presence of stable process metrics tells a different story (decision quality is degrading despite the system running normally) than a deteriorating outcome in the presence of degraded process metrics (the system is overloaded).
- Both axes feed back into governance system tuning: process problems suggest capacity or routing fixes; outcome problems suggest standards, role, or review-depth fixes.

#### Quick test

> Pick the most consequential decision class your governance system handles. Do you have process metrics for it (lead time, queue depth) and outcome metrics for it (retrospective decision quality, exception rate, regret indicators)? If you have only one axis, the system is being managed half-blind — and the failure mode that surfaces will be on the unmeasured axis.

#### Reference

[DORA Metrics](https://dora.dev/) — the canonical engineering performance framework that explicitly balances process metrics (deployment frequency, lead time for changes) with outcome metrics (change failure rate, time to restore service). The same balanced-scorecard discipline applied to the engineering process applies to the governance process — and getting the balance right is a measurable architectural choice.

---

### 2. Lead time and queue depth are the governance system's responsiveness signals

A governance system that's slow to decide is, in practice, a governance system that gets bypassed. Teams that need a decision and can't wait will either (a) ship without the decision and document the architectural choice as a fait accompli, (b) escalate around the system to whoever will give them an answer faster, or (c) reduce the scope of what they ask for so they don't trigger the slow-review path. All three failure modes are common, and all three reduce the governance system's actual coverage well below its nominal coverage. *Lead time* per decision class — submission to decision, in clock days — and *queue depth* — how many open decisions are awaiting review at any moment — are the canonical responsiveness metrics. The architectural discipline is to measure both, define SLAs per decision class (routine in days, cross-cutting in weeks, high-stakes in months), monitor against the SLAs, and act when the metrics deteriorate — by adding reviewers, promoting decision authority downward, or reducing the review-depth requirement for classes where the depth isn't earning its keep.

#### Architectural implications

- Lead time is measured per decision class, with target SLAs documented (routine: ≤ 5 working days; cross-cutting: ≤ 3 weeks; high-stakes: ≤ 6 weeks — adjust to organisational scale).
- Queue depth is monitored continuously: how many decisions are open at each tier, how long has each been open, what's the trend.
- Lead-time degradation triggers review of the role structure (capacity issue?), the workflow (workflow friction issue?), or the decision class (does this class need the review depth it's getting?).
- Teams have visibility into where their decisions sit in the queue — surprise delays are worse than known delays.

#### Quick test

> Pick a decision your team submitted in the last quarter. From the moment of submission to the moment of decision, how many clock days passed? Was that within the documented SLA for that decision class, or longer? If there's no SLA, or no measurement, lead time is operating on tradition — and the next "we shipped without waiting" decision will reveal the cost.

#### Reference

[DORA Metrics — Lead Time for Changes](https://dora.dev/quickcheck/) treats lead time as a primary engineering performance metric; the conceptual framing (lead time as the gap between intent and outcome, with shorter lead times correlated with better engineering performance) transfers directly to architectural decisions. [Architecture Advice Process — Andrew Harmel-Law](https://martinfowler.com/articles/scaling-architecture-conversationally.html) frames lead time as a primary architectural-governance concern at scale.

---

### 3. Exception rate is a signal about rule quality — not just about compliance

When the governance system grants an exception, it's saying "the standard or pattern doesn't fit this case, but we'll allow the deviation." A small exception rate is healthy — no rule covers every case, and exceptions are how the system handles legitimate edge cases. A *high* exception rate per standard is a different signal: the standard itself doesn't fit the cases the organisation actually faces. If 40% of teams that consult standard X end up requesting exceptions, the standard is wrong, ambiguous, or too narrow — and the architectural response is not "tighten exception review" but "reconsider the standard." The governance scorecard that tracks exception rates per standard surfaces this signal; the scorecard that aggregates exceptions to a single number obscures it. The distinction matters because the corrective actions differ: aggregate-level monitoring suggests stricter enforcement; per-standard monitoring suggests revising specific standards that are mismatched to reality.

#### Architectural implications

- Exception rate is measured per standard or pattern — not aggregated to a single organisational number that obscures which standards are fitting and which aren't.
- High exception rates per specific standards trigger review of the standard: is it ambiguous, too narrow, outdated, or genuinely a case where exceptions are the right answer because the standard's domain is heterogeneous?
- The remedy varies: revise the standard, split it into multiple standards covering distinct cases, retire the standard if its exception rate suggests it no longer applies.
- Exception trend per standard is also tracked: a previously-stable rate that's rising is a signal the organisation has changed in ways the standard hasn't kept up with.

#### Quick test

> Pick three standards in your organisation. For each, what's the current exception rate, what's the trend over the last year, and what does the rate tell you about the standard's fit? If you can't answer because exceptions aren't tracked per standard, the rule-quality signal is invisible — and standards that don't fit are being enforced through exception review rather than being repaired.

#### Reference

[COBIT 2019 (ISACA)](https://www.isaca.org/resources/cobit) treats exception management as a first-class governance process with measurement at the per-control level — making the rule-quality-vs-compliance distinction operational. The conceptual framing applies broadly: exceptions are a measurement of the rule, not just of compliance with it.

---

### 4. Adoption rate vs. paper compliance — the gap is the actual operating reality

A standard exists. Teams are required to follow it. They sign off that they have followed it. But "following the standard" can mean genuinely adopting the pattern, or it can mean checking a box during architectural review while the actual implementation diverges. *Adoption* is what the system actually does; *paper compliance* is what the team attests to. The gap between the two is the governance system's most consequential blind spot — the standards exist, the reviews happen, the scorecards say "compliant," and the actual systems are operating differently. The architectural response is to instrument adoption directly where possible: code-level checks (linting, static analysis, infrastructure-as-code policies), runtime checks (telemetry confirming patterns are being applied), and periodic audits (sampling deployed systems against the patterns they claim to follow). Where direct measurement isn't feasible, sampled audit becomes the proxy — but the discipline of distinguishing adoption from compliance remains the architectural point.

#### Architectural implications

- For standards where adoption can be measured automatically (code patterns, infrastructure configurations, deployment shapes), automated checks run continuously and feed adoption metrics into the scorecard.
- Where automation isn't feasible, sampled audits substitute — selecting a representative sample of deployed systems, evaluating against the standard, and producing an adoption-rate estimate.
- Paper-compliance metrics (proportion of reviews that signed off as compliant) are tracked alongside adoption metrics — the gap between the two is itself a measured signal.
- Persistent gaps trigger investigation: are reviewers approving things that shouldn't be approved, are submitters describing systems differently from how they're built, is the standard interpretable in ways the system designers and reviewers disagree about?

#### Quick test

> Pick a standard your organisation enforces. What proportion of teams attest to compliance with it (paper compliance), and what proportion of deployed systems actually exhibit the pattern (adoption)? If those numbers can't be produced or are obviously different, the gap is your governance system's actual operating reality — and the standard is doing less work than the scorecard suggests.

#### Reference

[AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) treats adoption measurement as a first-class concern in its Tool, with automated and manual evaluation paths producing adoption signals that surface gaps between attestation and reality. The architectural framing of "adoption vs. compliance" generalises beyond AWS-specific tooling.

---

### 5. Decision quality is measurable — retrospectively, on a sample, by people who weren't the deciders

The hardest governance metric to produce honestly is *decision quality*: were the decisions the system approved actually good, in retrospect? The challenge is that the deciders are biased reviewers of their own decisions — they tend to remember the supporting evidence and discount the warning signs. The architectural response is to evaluate decision quality through a separate retrospective process: a sample of decisions from N quarters ago is reviewed by people who weren't the original deciders, against criteria documented in advance (was the context accurate, were the alternatives considered fairly, did the consequences predicted come to pass, did unforeseen consequences emerge that the original review should have surfaced?). The results feed into the scorecard as decision-quality metrics, with the sampling and review process documented to make the measurement honest. This is harder than process metrics — it requires judgment, takes time, and produces uncomfortable findings — but it's the metric that ultimately tells the institution whether its governance system is doing the work it's supposed to do.

#### Architectural implications

- A sample of decisions from a prior period (quarter, half-year) is reviewed by independent reviewers who weren't on the original deciding body.
- Review criteria are documented in advance: context accuracy, alternatives consideration, consequence prediction, unforeseen consequences, contestability, supersession or persistence in light of new information.
- Results feed into the governance scorecard with appropriate aggregation — not naming-and-shaming individuals but surfacing patterns (this decision class is consistently underestimating consequences, this team's submissions are consistently incomplete, this reviewer pattern produces consistently good outcomes).
- The retrospective process is itself reviewed periodically — the criteria evolve, the sampling improves, the reviewers rotate — to keep the measurement honest.

#### Quick test

> Pick a decision your governance system approved 18–24 months ago. Has anyone retrospectively evaluated whether the decision was good — by criteria documented in advance, by reviewers who weren't on the original body? If no, the institution has no honest measurement of whether its governance system produces good decisions, and the system's legitimacy rests on confidence rather than evidence.

#### Reference

[ATAM (SEI)](https://insights.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) treats post-decision review as a structured discipline; the retrospective evaluation method generalises beyond the immediate ATAM context. [TOGAF](https://www.opengroup.org/togaf)'s governance framework includes Architecture Compliance Review processes that operationalise retrospective evaluation at enterprise scale.

---

### 6. Scorecard cadence is itself a calibration — too frequent produces noise, too rare produces drift

A governance scorecard reviewed too frequently — weekly, daily — produces noise. Lead time bounces around routinely; exception rates swing with the latest few decisions; the noise drowns the signal, and the team learns to ignore the metrics. A governance scorecard reviewed too rarely — annually, ad-hoc — misses signals that would have warranted action months earlier; metrics drift slowly into bad regions and the institution adapts gradually without noticing the system's degraded state. The right cadence is in between, and it's calibrated to the metric: lead time and queue depth tolerate weekly review (the noise is meaningful, the signal is operational); exception rate and decision quality benefit from monthly or quarterly cadence (the signal needs aggregation to emerge from noise); adoption rate often deserves quarterly review with sampled audit interspersed. The architectural discipline is to set cadence per metric, document it, and resist the temptation to either obsess (over-frequent) or neglect (under-frequent) — both fail differently, both fail predictably.

#### Architectural implications

- Each metric in the scorecard has a documented review cadence, calibrated to the metric's signal-to-noise characteristics.
- High-frequency operational metrics (lead time, queue depth) are reviewed weekly with monthly aggregation; lower-frequency strategic metrics (decision quality, adoption rate) are reviewed quarterly with annual deep-dives.
- The scorecard's overall review cadence is also documented: monthly tactical review focused on operational metrics, quarterly review covering all metrics, annual review including methodology and metric set.
- The scorecard set itself is reviewed periodically — adding metrics that earn their place, retiring metrics that don't surface useful signal, recalibrating cadences as patterns become clearer.

#### Quick test

> Pick the governance scorecard your organisation uses. What's the review cadence per metric? When was the most recent review of the scorecard's own composition (which metrics are included, which retired, which added)? If the cadence isn't documented or the scorecard hasn't been reviewed for composition in years, the measurement system is operating on inertia — and either drowning in noise or missing slow drift.

#### Reference

[COBIT 2019 — Performance Management Framework](https://www.isaca.org/resources/cobit) operationalises cadence-per-metric as part of its governance framework, with explicit annual / quarterly / monthly cadences for different metric classes. [DORA Metrics](https://dora.dev/) treats cadence as a calibration question: the framework's metrics are reviewed with cadence appropriate to their signal characteristics, not on a single uniform schedule.

---

## Architecture Diagram

The diagram below shows the canonical governance-scorecard architecture: process metrics (lead time, queue depth) and outcome metrics (exception rate, decision quality, adoption rate) as parallel measurement streams; data sources feeding each stream (decision-system telemetry for process, retrospective review for decision quality, automated and sampled audit for adoption); cadence layer applying review-frequency calibration; alerts and triggers feeding back into governance role, checklist, and template adjustments.

---

## Common pitfalls when adopting governance-scorecard thinking

### ⚠️ Single-axis measurement

The institution measures only process metrics: lead time is great, throughput is high. The system feels efficient. Decision quality has been degrading slowly for two years; nobody is measuring it. The system is fast and producing bad decisions; the scorecard says everything is fine.

#### What to do instead

Both process and outcome metrics, weighted toward outcomes. Fast bad decisions are worse than slow good ones; the scorecard's weighting reflects this.

---

### ⚠️ Aggregate exception rate as the only signal

The institution tracks "total exception count" or "exception rate" as a single number. The number is acceptable. Beneath the aggregate, three specific standards account for 80% of exceptions — they don't fit the cases the organisation faces. The aggregate hides the per-standard signal that would have prompted standard revision two years ago.

#### What to do instead

Per-standard exception rate. High rates per specific standards trigger review of those standards, not stricter exception enforcement. The remedy is to fix the rule, not to punish deviations from a misfit rule.

---

### ⚠️ Adoption equals paper compliance

The scorecard reports 95% compliance. The compliance metric measures reviewer attestation. Audits would reveal that actual adoption is closer to 60%. The scorecard is producing a number that's optimistic by design — it measures what's claimed, not what's deployed.

#### What to do instead

Distinguish paper compliance from actual adoption. Where automated measurement is feasible (code-level checks, infrastructure-as-code policies, runtime telemetry), instrument it. Where not, sampled audits produce adoption estimates. The gap between attestation and adoption is itself a measured signal.

---

### ⚠️ Decision quality reviewed by the deciders

The team that approved the decision is the team that retrospectively reviews whether the decision was good. They report the decision was good. Bias is structural; the review is theatre.

#### What to do instead

Retrospective review by independent reviewers — people who weren't on the original deciding body. Criteria documented in advance, sampling rule explicit, results aggregated to surface patterns rather than name individuals. The review is honest because it's structured to be.

---

### ⚠️ Cadence either weekly noise or annual drift

The scorecard is reviewed weekly. Half the metrics swing with the latest few decisions; the team learns to ignore them. Or — the scorecard is reviewed annually. By the time the team sees the metrics, drift has been accumulating for nine months; corrective action is months late.

#### What to do instead

Cadence calibrated per metric. Operational metrics weekly with monthly aggregation; strategic metrics quarterly with annual deep-dive. The scorecard composition is itself reviewed annually — metrics added that earn their place, retired that don't.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Both process metrics and outcome metrics are tracked, with outcome metrics weighted more heavily ‖ Process metrics expose responsiveness; outcome metrics expose quality. Single-axis measurement produces predictable failure on the unmeasured axis. The weighting reflects that outcomes ultimately matter more than throughput. | ☐ |
| 2 | Lead time per decision class is measured against documented SLAs ‖ The governance system's responsiveness is operationalised. SLAs differ by class (routine in days, cross-cutting in weeks, high-stakes in months). Missed SLAs trigger structural review, not exhortation. | ☐ |
| 3 | Queue depth is monitored continuously with visibility to submitting teams ‖ Decisions in flight, time-in-queue per item, trend over time. Surprise delays are worse than known delays; visibility is the precondition for honest expectation-setting. | ☐ |
| 4 | Exception rate is measured per standard, not aggregated to a single number ‖ Per-standard rate surfaces the rule-quality signal that aggregates obscure. High exception rate per a specific standard is a signal the standard needs revision, not stricter enforcement. | ☐ |
| 5 | Adoption rate is measured directly where possible — automated checks, runtime telemetry, sampled audits ‖ Adoption is what the system actually does; compliance is what teams attest to. The gap between the two is the governance system's actual operating reality. | ☐ |
| 6 | Decision quality is reviewed retrospectively by independent reviewers, against criteria documented in advance ‖ The deciders are biased reviewers of their own decisions. Retrospective review by independent reviewers, with structured criteria, is the architectural discipline that produces honest decision-quality measurement. | ☐ |
| 7 | Each metric has a documented review cadence calibrated to its signal-to-noise characteristics ‖ Cadence is itself a calibration. Operational metrics weekly with monthly aggregation; strategic metrics quarterly. The cadence resists both noise (over-frequent) and drift (under-frequent). | ☐ |
| 8 | The scorecard set is itself reviewed periodically — adding earning metrics, retiring underperforming ones ‖ The measurement system evolves. Metrics that don't surface useful signal are retired; new metrics are added when they earn their place. The scorecard is a living artefact, not a fixed dashboard. | ☐ |
| 9 | Metric deterioration triggers structural review — capacity, role, standards, or workflow adjustment ‖ Bad metrics are diagnostic, not punitive. Lead-time degradation triggers role structure review; exception rate per standard triggers standard review; decision quality degradation triggers review-depth or eval review. | ☐ |
| 10 | The scorecard surfaces patterns rather than naming individuals ‖ The measurement system is honest because it's structured to surface aggregate patterns (this decision class consistently underestimates consequences, this standard has rising exception rate) rather than to apportion blame. The signal is institutional, not personal. | ☐ |

---

## Related

[`governance/checklists`](../checklists) | [`governance/review-templates`](../review-templates) | [`governance/roles`](../roles) | [`scorecards`](../../scorecards) | [`maturity`](../../maturity) | [`patterns/structural`](../../patterns/structural)

---

## References

1. [DORA Metrics](https://dora.dev/) — *dora.dev*
2. [COBIT 2019 (ISACA)](https://www.isaca.org/resources/cobit) — *isaca.org*
3. [TOGAF](https://www.opengroup.org/togaf) — *opengroup.org*
4. [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) — *aws.amazon.com*
5. [ATAM (SEI)](https://insights.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) — *sei.cmu.edu*
6. [Architecture Advice Process — Andrew Harmel-Law](https://martinfowler.com/articles/scaling-architecture-conversationally.html) — *martinfowler.com*
7. [ADR — Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — *cognitect.com*
8. [The Checklist Manifesto — Atul Gawande](https://atulgawande.com/book/the-checklist-manifesto/) — *atulgawande.com*
9. [ThoughtWorks Technology Radar](https://www.thoughtworks.com/radar) — *thoughtworks.com*
10. [Apache Project Governance](https://www.apache.org/foundation/how-it-works.html) — *apache.org*
