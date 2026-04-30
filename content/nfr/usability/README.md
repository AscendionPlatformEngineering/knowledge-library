# Usability NFRs

The strategic guide for usability non-functional requirements — recognising that the team's accessibility targets specified to WCAG conformance levels rather than left as goodwill statements, the learnability targets defined as time-to-first-success measurements rather than as design intuitions, the error-prevention-and-recovery requirements specified per high-risk action class with measurable confirmation patterns, the cognitive-load budgets specified in fields-per-screen and decisions-per-flow rather than discovered after release, the per-task user-flow targets for completion-rate and time-on-task rather than aggregated UX metrics that hide flow-specific failures, and the budget-violation interpretation that treats accessibility violations and task-completion failures as architectural signal rather than as design preferences are what determine whether the team's product is genuinely usable for the populations it serves or whether the team's internal design intuition diverges from external user behaviour because the requirements never made the gap measurable.

**Section:** `nfr/` | **Subsection:** `usability/`
**Alignment:** ISO/IEC 25010 (Software Quality Model) | WCAG 2.2 (W3C) | Nielsen Norman Group Heuristics | ISO 9241-11 (Ergonomics)
---

## What "usability NFRs" means — and how it differs from UX research and accessibility audits

A *primitive* approach to usability is to design what feels intuitive to the team, run a couple of internal demos, listen to internal feedback, and ship. After release, support tickets reveal that real users hit confusion points the team did not anticipate; analytics show that one critical workflow has a 40% abandon rate that the team had not measured. The team responds with patches against the most-visible issues. After eighteen months, the system has accumulated dozens of localised UX fixes whose interactions are unmodelled, the original design intent is forgotten, and there is no architectural answer to "how usable is this actually, and for whom."

The *architectural* alternative is to specify usability as measurable contracts: per-task completion-rate targets at named user-population segments, accessibility-conformance levels with concrete WCAG criteria, learnability targets as time-to-first-success thresholds for new users, error-prevention requirements per high-risk action, and cognitive-load budgets per screen. Each contract has a measurement instrument (analytics events, user-research sessions, automated accessibility scans, support-ticket categorisation) and a budget threshold. UX research becomes the *validation method* against the contract; accessibility audits become the *coverage check*; neither replaces the architectural decision about what usability the system commits to deliver.

This is *not* the same as the [UI / UX / CX](../../technology/ui-ux-cx) page — that page covers the design patterns and user-experience methodologies. This page covers the *requirements specifications* that those patterns must satisfy. UX answers "how do we design it"; usability NFRs answer "what observable behaviour must it produce."

This is also *not* the same as the [NFR Scorecard](../../scorecards/nfr) — that page is the scoring instrument across all NFR categories. This page is one of the dimensions the scorecard scores, with the discipline-specific guidance on how to specify and validate usability targets.

The architectural signature of well-specified usability NFRs is *user-population-aware design*. When the targets distinguish user populations (new versus expert, sighted versus screen-reader, high-bandwidth versus low-bandwidth, native-language versus translated, mobile versus desktop), the design produces deliberate variations for each population rather than one design optimised for the team's modal user. When the targets are population-blind, the system serves the modal user well and serves edge populations poorly without anyone noticing because the measurements never captured those populations.

## Six principles

### 1. Specify accessibility to WCAG conformance levels, not as a goodwill statement
"The system shall be accessible" is a value statement, not a requirement. WCAG (Web Content Accessibility Guidelines) defines conformance levels A, AA, and AAA, with specific testable criteria for each. AA is the de-facto industry baseline and is required by many regulatory regimes; AAA is achievable for some content but operationally demanding for others. The architectural choice is which level applies to which surface of the system, with rationale tied to user population and regulatory requirement.

The discipline is the explicit conformance specification: this surface meets WCAG 2.2 AA; this admin-only surface meets WCAG 2.2 A (smaller user population, more controlled environment); this regulated surface meets WCAG 2.2 AAA. The conformance criteria are measurable — automated scanning catches a substantial fraction; manual testing with assistive technology covers the rest; user testing with disabled users provides the final validation that the spec produces actual usability.

#### Architectural implications
Conformance level drives concrete architectural choices: keyboard-only navigation paths must exist for AA; alternative-text infrastructure for images and media is a content-pipeline requirement; colour contrast ratios constrain the design system; ARIA-attribute correctness is a code-review concern. The conformance level is not a UX-team-only concern; it is a system-wide architectural requirement that ripples through the design system, the component library, the content pipeline, and the QA process.

#### Quick test
For your most-prominent user-facing surface, name the WCAG conformance level specified. If the answer is "we follow WCAG" without a level, the requirement is not specified. If the answer is "AA is our default" without per-surface differentiation, the regulatory variation across surfaces is not addressed.

### 2. Specify learnability as time-to-first-success per user population
A new user is a different beast than an expert user. The learnability target measures how quickly a new user can complete a first meaningful task — an order, a query, a configuration change, depending on the product. The target is "time-to-first-success" measured in seconds or minutes, with the success criterion observable in analytics. Without a learnability target, the design optimises implicitly for whoever the team observes most (often expert internal users), and the new-user experience degrades unmonitored.

The discipline is to specify learnability targets per user-population segment: new external users (expected to complete first task in N minutes without external help); existing returning users (expected to find the changed feature in N seconds); first-time mobile users (within the same population, on the smaller form factor); first-time non-native-language users. Each segment has a target, a measurement instrument, and a budget for variance.

#### Architectural implications
Learnability targets drive design choices that may be invisible to expert users: progressive disclosure rather than immediate full feature exposure, contextual onboarding rather than separated tutorials, in-line help rather than separate documentation, undo-friendly defaults rather than confirm-before-everything. Each of these is a deliberate trade-off; without learnability targets, the architecture defaults to the expert-user-friendly choices and the new-user experience suffers.

#### Quick test
For your most-used workflow, what is the time-to-first-success target for a new external user? If the answer is "we don't measure that," the learnability dimension is unmonitored and probably unequal across populations.

### 3. Specify error prevention and recovery per high-risk action class
Not all actions are equally risky. Deleting a file is high-risk; submitting a search query is low-risk. Sending money is high-risk; viewing a balance is low-risk. The architectural treatment of high-risk actions is fundamentally different: confirmation step, undo window, audit trail, error-recovery path. The treatment is specified per action class, not uniformly applied (which would be either over-protective for low-risk actions or under-protective for high-risk ones).

The discipline is to inventory high-risk actions, specify the confirmation pattern (modal versus inline; with or without typed confirmation), specify the undo window (instant undo versus admin-recoverable versus irreversible), and specify the error-recovery path when the action partially fails. The inventory is reviewed when new high-risk actions are introduced or when business-impact thresholds change.

#### Architectural implications
Error-prevention patterns drive architectural choices: undo windows imply soft-delete data models or transaction-log replay capability; confirmation patterns imply UX-state-machine design that distinguishes intent from execution; error-recovery paths imply idempotent action APIs that can be retried safely after partial failure. The patterns are not just UX choices; they are system-level architectural commitments.

#### Quick test
Pick a high-risk action in your system (deletion, money transfer, configuration change). Is the confirmation pattern specified in the NFR document? Is the undo window stated? Is the error-recovery path documented? If any is missing, the high-risk treatment is implicit and probably inconsistent across the system.

### 4. Specify cognitive-load budgets — fields per screen, decisions per flow
Cognitive load is finite. A form with 30 fields on one screen is fundamentally harder to complete than the same 30 fields decomposed across five screens of six fields each. A workflow with seven decisions per step is harder than one with two decisions per step. These budgets are quantitative and architectural; they shape the screen-flow design. Without explicit budgets, the design defaults to whatever fits on the canvas, which often packs more than users can reasonably process.

The discipline is to specify per-screen budgets (fields per screen, primary actions per screen, decisions per screen) and per-flow budgets (total screens for routine task, total decisions across the flow). The budgets are reviewed when new flows are introduced; budget violations are tracked in the design-review process the same way performance budget violations are tracked in code review.

#### Architectural implications
Cognitive-load budgets push back on stakeholder pressure to add fields and options. A new field added to a checkout form has a quantifiable cognitive cost; if the screen is already at budget, the new field forces either a flow split or an existing field's removal. The budget makes the trade-off explicit and architectural rather than a designer-versus-stakeholder negotiation lost case-by-case.

#### Quick test
For a representative form in your system, count the fields and the decisions per screen. Compare to your specified budget. If you have no specified budget, the cognitive-load posture is implicit and whatever-it-happens-to-be.

### 5. Specify per-task completion-rate and time-on-task targets, not aggregate UX metrics
Aggregate UX metrics (NPS, CSAT, SUS scores) are useful for trend monitoring but are too coarse to drive specific design changes. They average across all tasks; they cannot distinguish whether the dissatisfaction comes from one critical workflow that has a 40% abandon rate or from a uniformly mediocre experience across all flows. Per-task completion-rate and time-on-task targets are specific enough to drive specific architectural responses.

The discipline is to inventory the user tasks the system supports, specify a completion-rate target per task (typically 90%+ for routine tasks, lower acceptable for first-time tasks), and specify a time-on-task target with rationale tied to user-experience research. Tasks falling below target are diagnosed individually — which step of the flow is losing users — and addressed with specific design changes. The aggregate UX metrics are kept for trend monitoring but the per-task targets drive the architectural decisions.

#### Architectural implications
Per-task targets require analytics instrumentation that captures task-flow events: started, step-by-step progressed, completed, abandoned-at-step-N. Without that instrumentation, the targets cannot be measured and the practice degrades to designer intuition. The instrumentation cost is the price of architectural usability validation.

#### Quick test
For your top three user tasks, name the completion-rate target and the most recent measurement. If the targets do not exist, or the measurements have not been taken, the per-task discipline is not running.

### 6. Treat accessibility violations and task-completion failures as architectural signal
An accessibility audit finding, a per-task completion-rate dip, a support-ticket pattern indicating UX confusion — each is information about where the system's usability does not match its targets. The architectural response mirrors the other NFR domains: close the gap with a design change, accept the residual with documented rationale, or revise the target if the original was not appropriate for the population. The trajectory of findings and decisions is itself the meta-signal — accessibility findings rising or completion rates declining are architectural alarms even when individual instances are low-severity.

The discipline is the usability-finding ledger: every finding has decision (close / accept / revise), owner, and trajectory. The aggregate is a usability-posture signal that is read at architectural altitude rather than at design-team-only altitude.

#### Architectural implications
Same shape as the security-finding ledger and the maintainability suppression ledger and the reliability burn-rate review. The cross-cutting NFR pattern: every well-run NFR domain produces a debt-ledger artefact whose movement is architectural signal.

#### Quick test
Look at the most recent set of accessibility findings or task-completion-rate dips. Does each have a recorded decision (close / accept / revise) with owner and date? Or are findings closed silently as designers address them in routine work? If the latter, the trajectory signal is lost.

## Five pitfalls

### ⚠️ Specifying accessibility as goodwill rather than WCAG conformance level
"We are committed to accessibility" without WCAG level commitment is unverifiable. The fix is the per-surface conformance specification (WCAG 2.2 AA as default, with rationale-driven differentiation per surface) and the validation regime that combines automated scanning, manual assistive-technology testing, and user testing with disabled users.

### ⚠️ Optimising for the team's modal user without measuring edge populations
The team's internal demo audience is unrepresentative of the user population. Optimising for the modal user the team observes most produces a system that serves that user well and serves edge populations poorly. The fix is per-population learnability and completion-rate targets, instrumented across analytics segments.

### ⚠️ Uniform error-prevention treatment instead of per-action-class specification
Applying confirmation modals to every action — including low-risk ones — produces UX fatigue that erodes the protective value of confirmations on high-risk actions. Conversely, applying no confirmations to high-risk actions creates avoidable destructive errors. The fix is the explicit action-risk inventory with per-class confirmation, undo, and error-recovery specifications.

### ⚠️ Letting cognitive load creep without budgets
Without explicit fields-per-screen or decisions-per-flow budgets, every stakeholder request to add a field or an option chips away at usability with no visible cost. After a year of accumulated additions, forms become unmanageable. The fix is the explicit cognitive-load budget reviewed in design review the same way performance budgets are reviewed in code review.

### ⚠️ Aggregate UX metrics replacing per-task measurement
NPS or CSAT alone is too coarse to drive specific design changes. A 4.0/5 score does not tell you which task is failing. The fix is per-task completion-rate and time-on-task with named instruments, retaining aggregate metrics only for trend monitoring at portfolio level.

## Usability NFR specification checklist

| # | Check | Status |
|---|---|---|
| 1 | WCAG conformance level is specified per user-facing surface | ☐ |
| 2 | Accessibility validation combines automated scan, manual AT testing, user testing | ☐ |
| 3 | Learnability targets exist per user-population segment | ☐ |
| 4 | Time-to-first-success is measured for new external users | ☐ |
| 5 | High-risk actions have specified confirmation, undo, and error-recovery patterns | ☐ |
| 6 | Cognitive-load budgets are specified per screen and per flow | ☐ |
| 7 | Per-task completion-rate and time-on-task targets exist | ☐ |
| 8 | Analytics instrumentation captures task-flow events for per-task measurement | ☐ |
| 9 | Population segments are tracked separately (mobile/desktop, language, AT users) | ☐ |
| 10 | Usability-finding ledger records decision (close / accept / revise) per finding | ☐ |

## Related

- [Maintainability NFRs](../maintainability) — sister page on code-health and change-velocity requirements
- [Performance NFRs](../performance) — sister page on latency, throughput, and saturation requirements
- [Reliability NFRs](../reliability) — sister page on availability and graceful-degradation requirements
- [Security NFRs](../security) — sister page on confidentiality, integrity, and authentication requirements
- [NFR Scorecard](../../scorecards/nfr) — the scoring instrument applied across all NFR categories
- [UI / UX / CX](../../technology/ui-ux-cx) — design patterns and user-experience methodologies
- [Templates: Review Template](../../templates/review-template) — review document containing usability validation
- [Templates: ADR Template](../../templates/adr-template) — how usability target choices are recorded as decisions

## References

1. [ISO/IEC 25010 (Software Quality Model)](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010) — *iso25000.com*
2. [WCAG](https://www.w3.org/WAI/standards-guidelines/wcag/) — *w3.org*
3. [Web Vitals (Google)](https://web.dev/articles/vitals) — *web.dev*
4. [Continuous Architecture in Practice](https://www.oreilly.com/library/view/continuous-architecture-in/9780136523710/) — *oreilly.com*
5. [Quality Attribute Workshop (SEI)](https://insights.sei.cmu.edu/library/quality-attribute-workshop-third-edition-participants-handbook/) — *sei.cmu.edu*
6. [arc42 Architecture Template](https://arc42.org/) — *arc42.org*
7. [Architecture Decision Records (ADR community)](https://adr.github.io/) — *adr.github.io*
8. [Capability Maturity Model Integration (CMMI)](https://en.wikipedia.org/wiki/Capability_Maturity_Model_Integration) — *en.wikipedia.org*
9. [DORA Capabilities Catalog](https://dora.dev/capabilities/) — *dora.dev*
10. [TOGAF (overview)](https://en.wikipedia.org/wiki/The_Open_Group_Architecture_Framework) — *en.wikipedia.org*
