# Deployment Readiness Checklist

The artefact that determines whether a change is ready to ship — recognising that deployment readiness is a gate (proceed / defer / rollback), not a document, and that the checklist's items are calibrated by the specific production failure modes the team has actually experienced rather than by generic best practices that don't reflect the system's real risks.

**Section:** `checklists/` | **Subsection:** `deployment/`
**Alignment:** Continuous Delivery (Humble & Farley) | 12-Factor App | DORA Metrics | Release It! (Nygard)

---

## What "deployment readiness checklist" actually means

A *primitive* deployment readiness check is "the tests are green and someone approved the PR." This catches some classes of regression but misses many: the change passes tests but introduces an unmonitored failure mode, the change is correct but its rollback path was never exercised, the change is fine in isolation but interacts badly with another change shipping the same day, the change relies on configuration that exists in staging but not in production. Deployment-readiness-as-test-pass is a coverage instrument that reflects what the test suite catches, not what production actually requires.

A *production* deployment readiness checklist treats readiness as a *gate* with three stages. *Pre-deploy verification* — what must be true *before* deploy initiates: rollback path exists and is exercised, monitoring exists for the new behaviour, runbooks exist for the new failure modes, dependent teams have been notified, capacity has been validated for the new load. *Deploy-time monitoring expectations* — what signals must be tracked *during* deploy: error rate, latency, key business metrics, downstream signals, with documented thresholds for pause-or-rollback. *Post-deploy verification* — what must be true *after* deploy completes for the change to be declared shipped: signals returned to baseline, soak time elapsed, no unaddressed user reports, the change actually does what it was supposed to do (not just that it deployed without error). Each stage has documented items demanding specific evidence; failed items produce documented decisions, not "we'll address it later."

The architectural shift is not "we have a deploy checklist." It is: **deployment readiness is a three-stage gate (pre / during / post) calibrated by the team's actual production failures, with each gate's items demanding specific evidence and each failed gate producing a documented decision — and treating readiness as test-pass-equivalent or as nice-to-haves produces deploys that fail the way the team's last several deploys failed.**

---

## Six principles

### 1. Readiness is a gate, not a document — the checklist exists to determine ship / defer / rollback

The most consequential property of a deployment readiness checklist is whether its outcome *matters*. A checklist that produces a list of items the team marks off and then ships regardless is a document — useful as a record, not as a gate. A checklist that produces a *decision* — proceed with deploy, defer until items are addressed, rollback if the deploy is in progress — is a gate. The architectural discipline is to make the gate explicit and binding: the checklist is the input to a documented decision; failed items mean the decision is not "proceed." The decision authority is documented (typically a deploy lead, on-call engineer, or service owner); the override authority for proceeding despite failed items is documented and used rarely; the override is itself documented when it happens, with reasoning, so calibration can examine whether the override was justified.

#### Architectural implications

- The checklist's outcome is a documented decision (proceed / defer / rollback), not a list of marks.
- Decision authority is explicit: who decides, based on what items, with what override path.
- Failed items produce documented decisions: which items failed, what the decision was (defer / proceed-with-override / rollback), what justified the choice.
- Overrides are tracked across deploys: a pattern of overrides on a specific item is a calibration signal — either the item's threshold is too strict (revise), or the team is taking risks the checklist meant to prevent (training/process issue).

#### Quick test

> Pick the most recent deploy in your organisation that had a non-trivial change. What did the readiness checklist produce — a list of marks, or a documented decision? If the answer is "we marked items and shipped," the checklist is documentation, not a gate — and the items that don't quite pass are being rationalised through rather than triggering the decision the checklist exists to support.

#### Reference

[Continuous Delivery — Humble & Farley](https://www.oreilly.com/library/view/continuous-delivery-reliable/9780321670250/) treats deployment gates as a primary engineering discipline. [DORA Metrics — change failure rate](https://dora.dev/) operationalises the failed-deploy outcome as a tracked metric, providing the calibration signal that the checklist's gate is or isn't doing its job.

---

### 2. Three-stage structure — pre-deploy, deploy-time, and post-deploy verification have different concerns

A common pattern: the readiness checklist is one undifferentiated list applied at deploy time. Items that should have been verified weeks before the deploy ("does a runbook exist for the new failure modes?") are confirmed at the moment the deploy is starting, when the answer is "we'll write one later." Items that should be monitored during deploy ("is error rate within tolerance?") are not a checklist item but a watchful-eye-of-on-call-engineer concern. Items that should be verified after deploy ("did the change actually do what it was supposed to do?") are forgotten once the deploy completes without error. The architectural discipline is to recognise that *readiness has three stages* with different concerns: *pre-deploy* verifies preconditions; *deploy-time* verifies in-flight signals against documented thresholds; *post-deploy* verifies outcomes. Each stage's items have different timing, different decision criteria, and different remediation paths.

#### Architectural implications

- The checklist is structured in three sections: pre-deploy, deploy-time, post-deploy — with documented items in each.
- Pre-deploy items are verified in the days or hours before deploy, not at the moment deploy initiates; the checklist's pre-deploy section is part of deploy planning, not deploy execution.
- Deploy-time items have documented thresholds for pause-or-rollback decisions during the deploy itself; they're not "watch the dashboard" but "if error rate exceeds X for Y minutes, pause and decide."
- Post-deploy items have documented soak time before the deploy can be declared complete; "deployed without error" is not the same as "deploy verified successful."

#### Quick test

> Pick the most recent deploy of a non-trivial change. What was verified before deploy initiated, during deploy, and after deploy completed? If the verification was concentrated at deploy time only, the pre-deploy work is being skipped (rollback paths untested, runbooks missing) and the post-deploy verification is happening implicitly through "no incident reported."

#### Reference

[Release It! — Nygard](https://pragprog.com/titles/mnee2/release-it-second-edition/) covers the multi-stage readiness discipline at practitioner depth. [Production-Ready Microservices — Fowler](https://www.oreilly.com/library/view/production-ready-microservices/9781491965962/) provides a multi-stage readiness model for microservice deployments.

---

### 3. Pre-deploy items verify preconditions — rollback exercised, monitoring exists, runbooks exist, capacity validated

The pre-deploy stage is where most readiness work actually happens. The team that's ready to deploy a change has — *before* the deploy initiates — exercised the rollback path (in non-production at minimum), confirmed that monitoring exists for the new behaviour and the new failure modes the change introduces, written or updated runbooks for incidents the change might cause, notified dependent teams whose systems read or write data the change affects, and validated that capacity exists for the new load profile the change implies. A team that arrives at deploy time without these preconditions verified can either deploy anyway (and discover the gaps post-deploy when an incident reveals them) or defer the deploy (and pay the schedule cost of skipped pre-deploy work). The architectural discipline is to make the pre-deploy items explicit and to verify them as part of deploy planning, not as checkbox-marking at deploy time.

#### Architectural implications

- The pre-deploy section enumerates the preconditions that must be true: rollback path exercised, monitoring exists for new behaviour and new failure modes, runbooks exist for new failure modes, dependent teams notified, capacity validated for new load profile, configuration verified in production-like environment.
- Each item demands specific evidence: "rollback exercised on date X with timing Y" rather than "rollback path exists."
- Failed pre-deploy items produce a documented decision before deploy starts — typically "defer until addressed," not "proceed and figure it out."
- The pre-deploy section is part of deploy planning surfaces — design-doc readiness section, deploy-ticket template — not just a separate checklist applied at deploy time.

#### Quick test

> Pick a recent deploy that caused a production incident. Walk through the pre-deploy items: was rollback exercised before deploy? Did monitoring exist for the failure mode that triggered the incident? Did a runbook exist? If any of these were "no," the pre-deploy gate would have caught the gap if the gate had been applied — and the incident is the cost of skipping that work.

#### Reference

[Continuous Delivery — Humble & Farley](https://www.oreilly.com/library/view/continuous-delivery-reliable/9780321670250/) covers pre-deploy preconditions as primary deployment discipline. [Google SRE Workbook — Production-Readiness Reviews](https://sre.google/workbook/) operationalises the pre-deploy checklist pattern at practitioner depth.

---

### 4. Deploy-time items have explicit thresholds for pause-or-rollback decisions

During the deploy itself, the team's job is to monitor in-flight signals and decide whether to continue, pause, or rollback. Without explicit thresholds, this decision runs on the operator's instinct: "the error rate looks elevated but maybe it's just noise; let's see what happens." The architectural discipline is to make the thresholds explicit *before* the deploy starts: "if error rate exceeds X for Y minutes during deploy, pause; if it exceeds X for 2Y minutes, rollback." "If P99 latency increases by more than 50% over baseline for Y minutes, pause." "If a key business metric (orders/sec, signups/sec) drops by more than X% from baseline, rollback regardless of error rate." With thresholds defined ahead of time, the deploy-time decision is mechanical — apply the threshold to the signal, take the documented action — not a judgment call under pressure with the deploy in progress.

#### Architectural implications

- Each deploy-time item has a documented threshold: error rate above X, latency P99 above Y, key business metric below Z — with windows for sustained breach (transient spikes don't count).
- The thresholds determine documented actions: pause-and-investigate, pause-and-decide, immediate-rollback — depending on severity and duration.
- Threshold values are determined ahead of the deploy, based on the system's normal behaviour and the change's expected impact, not negotiated during the deploy.
- Automated alerts on threshold breaches reduce the cognitive load of the deploy operator — the system surfaces breach, the operator applies the documented decision.

#### Quick test

> Pick the most recent deploy of a non-trivial change. What were the pause-and-rollback thresholds during deploy, and where are they documented? If the answer is "we watch the dashboard and use judgment," the deploy-time gate is operating on instinct — and the operator who's tired or distracted will miss what an alerted threshold would catch.

#### Reference

[Spinnaker — Continuous Delivery Platform](https://spinnaker.io/) operationalises threshold-based deploy-time decisions as automated canary-analysis. [Argo CD](https://argo-cd.readthedocs.io/) provides similar threshold-driven deploy-time controls. The conceptual framing is treated in [Continuous Delivery — Humble & Farley](https://www.oreilly.com/library/view/continuous-delivery-reliable/9780321670250/).

---

### 5. Post-deploy verification has documented soak time and outcome verification — "deployed without error" isn't done

A deploy that completes without immediate error isn't necessarily a successful deploy. The change may have introduced a memory leak that takes hours to manifest. It may have a race condition that only surfaces under specific traffic patterns. It may not actually do what it was supposed to do — it deployed, but the new behaviour isn't working. The architectural discipline is to verify the deploy *over time*: a documented soak period during which the deploy is monitored against deploy-time thresholds at lower vigilance; outcome verification that the change does what it was supposed to do (a metric the team can check, a user-facing surface that should now behave differently, a signal that the new code path is being exercised); explicit declaration that the deploy is complete only when both the soak elapses without breach and the outcome is verified. Until both are true, the deploy is in flight and rollback remains an option.

#### Architectural implications

- The post-deploy section documents the soak period (typically 30 minutes to several hours, depending on change risk) and the deploy-time thresholds that continue to apply during soak.
- Outcome verification items document what the change was supposed to do and how to verify it: "the new endpoint is receiving traffic at expected rate," "the new field is being populated in records being written," "the new metric is being emitted."
- Until the soak elapses without breach AND outcome verification passes, the deploy is "in flight" — rollback is available, full vigilance applies.
- The transition from "in flight" to "complete" is a documented decision, not implicit; the team explicitly declares the deploy successful, which is the trigger for cleaning up rollback scaffolding (if applicable).

#### Quick test

> Pick the most recent deploy in your organisation. When was it declared complete, and what verified that it was actually doing what it was supposed to do? If the answer is "after the deploy ran and nobody complained," the deploy was declared complete on the absence of bad news rather than the presence of good — and changes that silently fail are being shipped as successes.

#### Reference

[Release It! — Nygard](https://pragprog.com/titles/mnee2/release-it-second-edition/) treats post-deploy verification as a primary engineering discipline. [Google SRE Workbook — Canary Analysis](https://sre.google/workbook/) covers the soak-and-verify pattern with concrete examples.

---

### 6. Items are calibrated by the team's actual production failure modes — generic checklists miss the specific risks

A deployment readiness checklist drawn from generic best practices catches the deploys that fail in generic ways. It doesn't catch the deploys that fail in *the team's specific ways* — the failure modes that recur in this system because of its architecture, dependencies, traffic profile, or history. The architectural discipline is *calibration by actual production failure modes*: every deploy-related production incident produces a candidate revision to the checklist. The post-incident review asks "would the existing checklist have caught this?" If yes, the deploy gate failed to apply it; if no, the checklist itself failed to cover this failure mode and an item gets added. Over time, the checklist accumulates the team's institutional learning about *its specific risks* — and the same failure mode that caused last quarter's incident is unlikely to cause next quarter's.

#### Architectural implications

- Every deploy-related production incident's post-mortem includes the question "would the deploy readiness checklist have caught this?"
- Findings produce a queue of candidate checklist revisions, prioritised by frequency of similar incidents and severity.
- Revisions are versioned and reviewed — what's added, why, which incident motivated it; reviewed by someone other than the author before merging.
- The checklist's items reflect the system's specific risks (e.g. items about Kafka consumer-lag thresholds for systems using Kafka, items about connection pool sizing for systems with database hot paths) — not just generic best practices that don't reflect operational reality.

#### Quick test

> Pick the most consequential deploy-related incident in your organisation in the last year. Was a candidate checklist revision proposed as part of its post-mortem? If yes, was it incorporated? If the answer is "we discussed it but didn't update the checklist," the calibration loop is broken — and the next deploy in the same risk class will surface the same gap.

#### Reference

[Etsy — How to Conduct a Postmortem (Allspaw)](https://www.etsy.com/codeascraft/blameless-postmortems) treats post-incident learning generally; the same discipline applied to deploy-checklist calibration produces continuously-improving readiness gates. [Accelerate — Forsgren, Humble, Kim](https://itrevolution.com/product/accelerate/) provides empirical research showing that deploy-readiness calibration correlates with engineering performance metrics.

---

## Architecture Diagram

The diagram below shows the canonical deployment-readiness-checklist architecture: the three-stage gate structure (pre-deploy preconditions, deploy-time thresholds, post-deploy verification), with explicit decisions at each stage; the calibration loop where deploy-related incidents produce candidate revisions; CI/CD pipeline integration where the checklist surfaces in deploy tickets, change requests, and the deploy tooling itself.

---

## Common pitfalls when adopting deployment-readiness-checklist thinking

### ⚠️ Checklist as document, not gate

Items are marked, the deploy proceeds regardless. Failed items don't trigger decisions. The checklist is a record, not a binding instrument.

#### What to do instead

Outcome of the checklist is a documented decision (proceed / defer / rollback). Decision authority and override authority are explicit. Overrides are tracked and reviewed.

---

### ⚠️ Single-stage checklist applied at deploy time

Items that should have been verified weeks ago are confirmed at the moment of deploy. Items that should monitor in-flight signals aren't on the checklist. Items that should verify outcomes after deploy are forgotten.

#### What to do instead

Three-stage structure: pre-deploy preconditions, deploy-time thresholds, post-deploy verification. Each stage has its own items, timing, and decision criteria.

---

### ⚠️ Deploy-time thresholds set by judgment in the moment

The on-call operator watches the dashboard and decides what looks bad. Thresholds aren't documented. Decision quality varies with who's watching.

#### What to do instead

Documented thresholds before deploy: error rate, latency, key business metrics — with windows for sustained breach and documented actions per threshold. Automated alerts on breach. The decision is mechanical, not a judgment call.

---

### ⚠️ Deploy declared complete on "no immediate error"

The deploy ran. Nothing exploded in the next five minutes. The deploy is declared done. Memory leaks, race conditions, and silently-failing changes ship as successes.

#### What to do instead

Documented soak period with continued vigilance. Outcome verification that the change does what it was supposed to do. Deploy is "in flight" until both soak and outcome pass; then explicitly declared complete.

---

### ⚠️ Generic checklist disconnected from team's actual failures

The checklist was drawn from a blog post about deploy best practices. It doesn't include items about the failure modes the team has actually experienced. The same deploy-related incidents recur.

#### What to do instead

Calibration by actual production failure modes. Every deploy-related incident's post-mortem produces a candidate revision. Items reflect the system's specific risks, not just generic best practices.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | The checklist's outcome is a documented decision (proceed / defer / rollback), not a list of marks ‖ Decision authority and override authority are explicit. Failed items produce documented decisions. Overrides are tracked across deploys. | ☐ |
| 2 | The checklist is structured in three stages: pre-deploy, deploy-time, post-deploy ‖ Each stage has documented items with appropriate timing, decision criteria, and remediation paths. | ☐ |
| 3 | Pre-deploy items verify preconditions with specific evidence ‖ Rollback exercised (date, timing), monitoring exists for new behaviour and failure modes, runbooks exist, dependent teams notified, capacity validated. Items demand specifics, not affirmation. | ☐ |
| 4 | Pre-deploy section is part of deploy planning surfaces, not just a separate checklist at deploy time ‖ Deploy-doc, deploy-ticket templates include pre-deploy items. Authors confront items before deploy execution. | ☐ |
| 5 | Each deploy-time item has a documented threshold with windows for sustained breach ‖ Error rate above X, latency P99 above Y, key business metric below Z. Transient spikes don't trigger; sustained breach does. | ☐ |
| 6 | Threshold breaches determine documented actions — pause-and-investigate, pause-and-decide, immediate-rollback ‖ The deploy-time decision is mechanical, not a judgment call. Automated alerts surface breach; operator applies documented decision. | ☐ |
| 7 | Post-deploy section documents soak period with continued vigilance ‖ Soak duration matches change risk (typically 30 min to several hours). Deploy-time thresholds continue to apply during soak. | ☐ |
| 8 | Outcome verification items confirm the change does what it was supposed to do ‖ Specific signals: new endpoint receives traffic, new field populated, new metric emitted. "Deployed without error" is not "deploy verified successful." | ☐ |
| 9 | Deploy completion is a documented decision based on both soak elapsing and outcome passing ‖ The transition from "in flight" to "complete" is explicit, not implicit. Triggers cleanup of rollback scaffolding. | ☐ |
| 10 | Every deploy-related production incident's post-mortem asks "would the checklist have caught this?" ‖ Calibration loop. Findings feed candidate revisions. Versioned and reviewed updates. The checklist accumulates institutional learning over time. | ☐ |

---

## Related

[`checklists/architecture`](../architecture) | [`checklists/security`](../security) | [`runbooks/rollback`](../../runbooks/rollback) | [`runbooks/migration`](../../runbooks/migration) | [`technology/devops`](../../technology/devops) | [`observability/sli-slo`](../../observability/sli-slo)

---

## References

1. [Continuous Delivery (Humble & Farley)](https://www.oreilly.com/library/view/continuous-delivery-reliable/9780321670250/) — *oreilly.com*
2. [12-Factor App](https://12factor.net/) — *12factor.net*
3. [DORA Metrics](https://dora.dev/) — *dora.dev*
4. [Release It! (Nygard)](https://pragprog.com/titles/mnee2/release-it-second-edition/) — *pragprog.com*
5. [Spinnaker — Continuous Delivery Platform](https://spinnaker.io/) — *spinnaker.io*
6. [Argo CD](https://argo-cd.readthedocs.io/) — *argo-cd.readthedocs.io*
7. [Production-Ready Microservices (Fowler)](https://www.oreilly.com/library/view/production-ready-microservices/9781491965962/) — *oreilly.com*
8. [Accelerate (Forsgren, Humble, Kim)](https://itrevolution.com/product/accelerate/) — *itrevolution.com*
9. [Google SRE Workbook](https://sre.google/workbook/table-of-contents/) — *sre.google*
10. [Etsy — How to Conduct a Postmortem](https://www.etsy.com/codeascraft/blameless-postmortems) — *etsy.com*
