# Maintainability NFRs

The strategic guide for maintainability non-functional requirements — recognising that the team's measurable maintainability targets specified rather than left as adjectives in design documents, the explicit decomposition into modifiability and testability and analysability and reusability rather than treating maintainability as a single dimension, the lean-on-static-analysis-evidence approach that reads metrics from the codebase rather than asking developers how maintainable they feel the system is, the per-module rather than per-system targeting that respects the heterogeneous maintainability profile of every real codebase, the trajectory monitoring that distinguishes accumulating debt from absorbed-then-paid-down debt, and the budget-violation-as-architectural-signal interpretation that treats threshold breaches as work to schedule rather than scores to defend are what determine whether the team's maintainability posture stays calibrated with how much change-velocity the business needs from each module or whether the codebase silently accumulates debt for years before refactor cost becomes catastrophic.

**Section:** `nfr/` | **Subsection:** `maintainability/`
**Alignment:** ISO/IEC 25010 (Software Quality Model) | CISQ Software Quality Standards | SonarSource Maintainability Rating | Continuous Architecture in Practice
---

## What "maintainability NFRs" means — and how it differs from code-quality tooling outputs

A *primitive* approach to maintainability is to install a static-analysis tool, accept whatever default thresholds ship with it, and let the dashboard turn red or green automatically. Six months later, the team has either learned to ignore the dashboard (because the thresholds were calibrated for a different kind of codebase and produce false alarms) or learned to game the dashboard (by suppressing rules that flag the architectural debt the team does not want to confront). After eighteen months, the dashboard reliably reports green while the team's actual change velocity has dropped by half because the *architectural* maintainability of the system has degraded in ways the off-the-shelf rules do not measure.

The *architectural* alternative is to specify maintainability NFRs the same way performance and reliability NFRs are specified: with measurable targets per module, evidence requirements grounded in artefacts, trajectories tracked across releases, and budget violations treated as architectural signal. The static-analysis tool becomes the *instrument* that produces the measurements; the *targets* are the architectural decision about how maintainable each part of the system needs to be, given how much change velocity that part requires. A trade-execution engine that changes once a quarter has different maintainability targets than a customer-onboarding flow that changes weekly. The architectural job is to set those targets per module deliberately rather than accept default thresholds for everything.

This is *not* the same as the [NFR Scorecard](../../scorecards/nfr) — that page is about the *scoring instrument* applied across all NFR categories at programme altitude. This page is about *how maintainability NFRs themselves are specified*, what good targets look like, and how to read the measurements once they are produced. The scorecard is the *meta-instrument*; this page is *one of the dimensions* the scorecard scores.

This is also *not* the same as architectural patterns ([`patterns/`](../../patterns)) — patterns shape the design that is built, while maintainability NFRs measure whether the resulting code stays workable over time. A team can apply excellent patterns and still produce unmaintainable code (when the patterns are misapplied or under-documented). A team can produce maintainable code with mediocre patterns (when the discipline of testing, naming, and modularity is high). Both pieces matter; this page covers the measurement-and-target side.

The architectural signature of well-specified maintainability NFRs is *change-cost predictability*. When the targets are calibrated against actual change velocity needs, a developer estimating a feature against a module can predict implementation cost reasonably well from the maintainability indicators. When the targets are not calibrated, the estimates are wrong by a factor of two to five and the team learns to add slack to every estimate, which corrupts the planning loop further.

## Six principles

### 1. Decompose maintainability into ISO/IEC 25010 sub-characteristics rather than treating it as one dimension
ISO/IEC 25010 decomposes maintainability into modifiability, testability, analysability, reusability, and modularity. Each sub-characteristic has different measurement instruments, different target rationales, and different failure modes. Modifiability is measured by change-cost in person-hours per typical change; testability is measured by test-coverage and test-stability; analysability is measured by the time-to-locate a bug given a symptom report; reusability is measured by re-import frequency across modules; modularity is measured by efferent-coupling and afferent-coupling ratios.

A maintainability target expressed as "the system shall be maintainable" or even "the system shall achieve maintainability rating B" is uninterpretable without specifying which sub-characteristic. The team treats these as one dimension because the off-the-shelf tools produce one composite letter grade; the architectural discipline is to read past the letter grade to the underlying measurements and target each sub-characteristic separately.

#### Architectural implications
Different sub-characteristics will have different priorities per module. A trade-execution engine prioritises analysability (because production debugging time is critical) and testability (because test investment is high) over reusability (because the engine has no peer modules). A shared utility library prioritises reusability and modularity. The targets per sub-characteristic per module become a small matrix; aggregating it into a single number throws away the architectural decision.

#### Quick test
For three randomly chosen modules in your codebase, name the maintainability sub-characteristic that matters most for that module. If the answer is "all of them equally" for all three, the targets are not differentiated and the practice is treating maintainability as a scalar.

### 2. Express targets as observable measurements with thresholds, not as adjectives
"The codebase shall be readable" is a wish, not a requirement. "Cyclomatic complexity shall be ≤10 for 95% of functions; ≤15 for 99%" is a requirement. "The system shall be testable" is a wish; "Lines of test code shall be ≥80% of lines of production code; statement coverage on the critical-path module shall be ≥85%" is a requirement.

The discipline is the same as for performance NFRs: every maintainability target must be a measurable threshold on an instrument that runs in CI and produces a number. The threshold breach is a CI signal that the budget has been exceeded, not a subjective complaint. The target without measurability is a value statement masquerading as an engineering requirement.

#### Architectural implications
Choosing the measurement instrument is itself an architectural decision. Cyclomatic complexity is one measurement; cognitive complexity (a Sonar variant) is a different measurement; both are imperfect proxies for analysability. The team commits to one instrument family per sub-characteristic, accepts that the instrument has known limitations, and uses the trajectory of measurements over time as the operating signal. Switching instruments invalidates the historical trend line.

#### Quick test
Pick the most-recently-written maintainability requirement in your design documentation. Does it specify a numerical threshold, the measurement instrument, and the scope of measurement? If any of the three is missing, the requirement is not observable.

### 3. Set targets per module, not per system
Every real codebase has heterogeneous maintainability profiles. The customer-onboarding module changes weekly and needs aggressive maintainability targets so it stays workable. The legacy fraud-rules engine changes once a quarter and tolerates higher complexity because the change cost is paid rarely. The shared logging library is touched by everyone and needs the most disciplined targets of all because every quality compromise is multiplied across consumers. A single system-wide target is necessarily wrong for at least some modules — too strict for the ones that change rarely (wasting investment) or too loose for the ones that change weekly (accumulating velocity-killing debt).

The discipline is to publish the per-module target matrix as an architectural artefact, with rationale. The matrix is reviewed when the change-velocity profile of a module changes — which usually happens at major-feature boundaries — and otherwise stays stable for trajectory readability.

#### Architectural implications
The per-module matrix is itself a maintainable artefact. Adding a new module includes adding a row to the matrix with named target levels and rationale. Modules without an explicit row inherit a documented default. The matrix lives in the repo, is reviewed at PR time, and is the input to the CI-level threshold gates per module.

#### Quick test
For your codebase, ask "what is the maintainability target for module X?" If the answer is "the same as everywhere else, we have one rule for the codebase," the team has not differentiated. If the answer is "we don't actually have a stated target for that module," the team is not specifying maintainability NFRs at all and the dashboard is doing the work that the architectural decision should have done.

### 4. Read trajectory across releases, not absolute level on the latest commit
A module at complexity-90 today after a feature delivery may be in a healthier state than a module that has held complexity-50 for four years. The first is moving but recently absorbed a feature; the second has plateaued at a level that is mediocre and stable. The trajectory information dominates the absolute-level information.

Effective maintainability programmes report trajectory per module per sub-characteristic, with annotations for known events that explain step-changes (a refactor sprint, a major feature, a deprecation). Reading the trajectory line tells the architectural story: this module is degrading, that one is improving, that one is stable; the degrading ones need investigation; the stable ones might warrant target re-calibration.

#### Architectural implications
Trajectory reading requires the measurement to be stable across commits. A measurement that produces noise as large as the signal it is trying to track cannot be trended. This puts pressure back on Principle 2 (observable, measurable thresholds): noisy measurements that fluctuate ±10% cycle-to-cycle on stable code are diagnostic of an instrument problem, not of a code-quality problem.

#### Quick test
Look at the most recent maintainability report. Does it show a trajectory line per module across at least the last six releases? If only the latest measurement is shown, the team cannot distinguish absorbed debt from accumulating debt.

### 5. Treat budget violations as architectural signal, not as defects to suppress
A maintainability budget breach — a function whose cyclomatic complexity exceeded the threshold, a module whose coupling ratio drifted past the limit — is not a defect that needs to be removed by tweaking the rule. It is information: the codebase has accumulated a measurable amount of debt at a known location, and the architectural choice is whether to (a) schedule the refactor now, (b) accept the debt and adjust the target with rationale, or (c) suppress the rule for that location with a documented exception. All three are valid choices; choosing (d) silently bumping the rule's threshold to make the warning go away is the architecturally wrong response because it removes the signal without addressing the underlying state.

The discipline is to treat every threshold breach as a small architectural decision with a recorded outcome. Suppressions are documented with rationale and reviewed at module-level reviews; threshold adjustments are documented in the per-module matrix; refactor schedules become part of the next-cycle plan. The aggregate of these decisions becomes the architectural debt ledger, which is itself a key maintainability artefact.

#### Architectural implications
The CI tooling must distinguish "new violation" (introduced this PR) from "existing violation" (pre-existing baseline) and treat them differently. New violations block merges by default; existing violations are tracked in the debt ledger but do not block routine work. This separation prevents the common dysfunction where a tightening rule generates 200 instant violations and the team responds by suppressing the rule entirely.

#### Quick test
Look at your most recent set of maintainability suppressions. Does each suppression have a recorded rationale and a review date? If they are anonymous suppressions added during normal development, the architectural debt ledger is not being kept.

### 6. Calibrate targets against change-velocity needs, not against industry best-practice averages
Industry-published maintainability thresholds (Sonar's default ratings, McCabe's original cyclomatic complexity threshold of 10) are useful starting points, not architectural targets. The right target for your module depends on how much change velocity the business needs from that module, which is a local question with no industry default. A trading engine that updates strategies daily needs much tighter modifiability targets than a once-a-quarter regulatory reporting module, even if both are written in the same language by the same team.

The discipline is to calibrate the per-module target matrix against the actual change-frequency-and-criticality profile of each module, then validate the calibration by checking whether change-cost estimates against well-targeted modules are coming in close to actuals. Over multiple cycles, the targets should become predictive: a module hitting its targets should be producing accurate change estimates, and a module drifting past its targets should be producing increasing estimate-vs-actual variance.

#### Architectural implications
This calibration cycle requires the team to actually track change-cost estimate-vs-actual variance per module, which most teams do not. The instrumentation pays off in two ways: it produces the calibration evidence for maintainability targets, and it produces planning-accuracy evidence for the engineering practice as a whole. The two outcomes are inseparable; treating maintainability targets as decoupled from change-cost predictability removes the validation loop and turns the targets into wishes.

#### Quick test
For a module that is consistently meeting its maintainability targets, look at the last five feature estimates against that module. Were the actuals within ±25% of the estimates? If yes, the targets are predictive. If not, the targets and the estimates are decoupled and one of them is not calibrated to reality.

## Five pitfalls

### ⚠️ Treating maintainability as a single composite letter grade
The off-the-shelf tools produce a composite — Sonar's maintainability rating A through E, the maintainability index — that aggregates across cyclomatic complexity, lines-of-code, comments, and several other inputs. The composite has the advantage of producing one number; it has the disadvantage of being uninterpretable when it changes, because a movement from B to C could be from any of half a dozen contributing inputs. The fix is to read the underlying sub-characteristic measurements and target them individually, using the composite (if at all) only as a coarse coverage check.

### ⚠️ Adopting industry-default thresholds without calibrating to change-velocity needs
Cyclomatic complexity 10 is Sonar's default; it is also McCabe's 1976 suggestion based on a small empirical study. Neither was derived from your business's change-velocity profile. Modules that need weekly change deserve tighter targets; modules that change once a quarter can tolerate higher complexity. Adopting the default for everything wastes investment on the rare-change modules and under-invests in the high-velocity modules. The fix is the per-module target matrix calibrated against actual change-velocity needs.

### ⚠️ Suppressing rules to silence dashboards rather than addressing the underlying state
The fastest way to make a maintainability dashboard turn green is to suppress the rules generating the most warnings. The dashboard turns green; the underlying state does not change; the next person reading the codebase finds the same legibility problems unmarked. The fix is the documented-suppression discipline: every suppression has rationale and a review date, suppression rate is itself a metric in the maintainability report, and growth in suppression count triggers architectural review.

### ⚠️ Reporting current state without trajectory
Current-state-only reporting cannot distinguish a module that just absorbed a major feature (and will refactor next sprint) from a module that has been at its current level for three years (and is plateaued). The two states have opposite architectural significance. The fix is to publish the trajectory line as the primary view, with current state as a derived secondary number — exactly the same fix as for [maturity assessments](../../maturity/guidelines).

### ⚠️ Decoupling maintainability targets from change-cost estimate variance
The validation loop for maintainability targets is whether modules meeting their targets produce accurate change-cost estimates. If that loop is not running — if change-cost estimate variance is not tracked per module — then the targets cannot be calibrated against the thing they are supposed to predict. The targets become a parallel governance ritual decoupled from the planning practice they should be feeding. The fix is to instrument estimate-vs-actual variance and use it as the calibration signal for the target matrix.

## Maintainability NFR specification checklist

| # | Check | Status |
|---|---|---|
| 1 | Maintainability is decomposed into ISO/IEC 25010 sub-characteristics in design docs | ☐ |
| 2 | Targets are expressed as numerical thresholds on named measurement instruments | ☐ |
| 3 | The per-module target matrix exists with named rationale per row | ☐ |
| 4 | Default targets are documented for modules without an explicit row | ☐ |
| 5 | CI distinguishes "new violation" from "existing violation" and treats them differently | ☐ |
| 6 | Trajectory data exists for at least six prior releases per module | ☐ |
| 7 | Suppressions carry recorded rationale and review dates | ☐ |
| 8 | Suppression-count growth is monitored as its own metric | ☐ |
| 9 | Change-cost estimate variance is tracked per module | ☐ |
| 10 | Targets are recalibrated when change-velocity profile of a module shifts | ☐ |

## Related

- [Performance NFRs](../performance) — sister page on latency and throughput requirements
- [Reliability NFRs](../reliability) — sister page on availability and graceful-degradation requirements
- [Security NFRs](../security) — sister page on confidentiality, integrity, and authentication requirements
- [Usability NFRs](../usability) — sister page on user-facing quality requirements
- [NFR Scorecard](../../scorecards/nfr) — the scoring instrument applied across all NFR categories
- [Principles: Foundational](../../principles/foundational) — the architectural principles applied to design
- [Maturity Guidelines](../../maturity/guidelines) — methodology that frames how trajectory reading works
- [Templates: ADR Template](../../templates/adr-template) — how target choices are recorded as decisions

## References

1. [ISO/IEC 25010 (Software Quality Model)](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010) — *iso25000.com*
2. [CISQ Software Quality Standards](https://www.it-cisq.org/standards/) — *it-cisq.org*
3. [Continuous Architecture in Practice](https://www.oreilly.com/library/view/continuous-architecture-in/9780136523710/) — *oreilly.com*
4. [Capability Maturity Model Integration (CMMI)](https://en.wikipedia.org/wiki/Capability_Maturity_Model_Integration) — *en.wikipedia.org*
5. [arc42 Architecture Template](https://arc42.org/) — *arc42.org*
6. [Quality Attribute Workshop (SEI)](https://insights.sei.cmu.edu/library/quality-attribute-workshop-third-edition-participants-handbook/) — *sei.cmu.edu*
7. [DORA Capabilities Catalog](https://dora.dev/capabilities/) — *dora.dev*
8. [Architecture Tradeoff Analysis Method (Wikipedia)](https://en.wikipedia.org/wiki/Architecture_tradeoff_analysis_method) — *en.wikipedia.org*
9. [TOGAF (overview)](https://en.wikipedia.org/wiki/The_Open_Group_Architecture_Framework) — *en.wikipedia.org*
10. [Architecture Decision Records (ADR community)](https://adr.github.io/) — *adr.github.io*
