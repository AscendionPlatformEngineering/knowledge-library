# Governance Checklists

The checklists that the people running architectural governance use — distinct from the technical review checklists those people apply to code or systems. The audience is the architect-on-duty, the ARB chair, the principal engineer reviewing an exception; the purpose is to make their work consistent, low-friction, and learn-from-itself across cycles.

**Section:** `governance/` | **Subsection:** `checklists/`
**Alignment:** ADR (Michael Nygard) | TOGAF | ATAM (SEI) | COBIT 2019

---

## What "governance checklists" actually means

A *technical* checklist (architecture review, deployment readiness, security review) lives at the boundary where engineering work meets a quality gate — the reviewer evaluates an artefact against a list of properties, and the artefact passes or fails. Those are covered in [`checklists/architecture`](../../checklists/architecture), [`checklists/deployment`](../../checklists/deployment), and [`checklists/security`](../../checklists/security). They're necessary and well-established; they're not what this page is about.

A *governance* checklist sits one level up: it's the checklist used by the people *running* the technical reviews, not the checklist they apply to the work. The ARB chair has a checklist for opening a meeting (decisions due, exception requests pending, follow-ups from last cycle, declared conflicts of interest). The architect-on-duty has a checklist for handling a fast-track decision (does it need an ADR, does it need a community review, what's the escalation path if the team disagrees?). The audit lead has a checklist for periodic governance audits (which decisions in the last quarter were exceptions, were the exceptions reviewed, what's the trend on lead time?). These checklists are operational discipline for the governance system itself.

The architectural shift is not "we added more checklists." It is: **the governance system itself has operational machinery — meetings, exception reviews, audits, periodic recalibration — and that machinery has checklists that keep it consistent across people, time, and circumstance, separate from the technical-review checklists that govern code and systems.**

---

## Six principles

### 1. Governance checklists serve a different audience than technical checklists — and confusing the two produces both ritual and chaos

A technical checklist's audience is an engineer or reviewer evaluating an artefact: does this design specify failure modes, does this PR have tests, does this deployment have a rollback plan? The reviewer is checking the work. A governance checklist's audience is someone *running* the governance process: the ARB chair preparing an agenda, the architect-on-duty triaging incoming requests, the policy owner running a periodic review of which standards are still relevant. The reviewer is checking *the process*. When organisations conflate the two — putting governance-process items into technical checklists, or vice versa — the technical reviewers end up rubber-stamping process items they don't understand, the process operators end up filling in technical fields they aren't qualified to evaluate, and both sets of checklists lose their integrity. The architectural discipline is to keep audience clear: each checklist names who runs it, when, and what their authority is to act on findings.

#### Architectural implications

- Each governance checklist names its primary audience explicitly: ARB chair, architect-on-duty, policy owner, audit lead, exception reviewer — not "anyone reviewing this."
- Technical-review checklists (architecture, deployment, security) are kept distinct from governance-process checklists in storage, naming, and discoverability — confused mixing produces both kinds of failure.
- The governance checklist's items are about *the process working* (was the right person notified, was the SLA met, was the decision documented), not about *the work being good* (is the design correct, is the code tested) — those questions belong to technical checklists.
- Where governance and technical concerns genuinely overlap (e.g. an architectural exception that requires both process steps and technical risk evaluation), the checklist makes the handoff explicit rather than blending the two.

#### Quick test

> Pick a checklist used in your governance process. Who is the named primary audience, and what's their authority to act on its findings? If the answer is "anyone who reviews," the checklist is doing two jobs and the people using it are doing them with whatever blend of authority they happen to have. The lack of clarity will produce uneven outcomes.

#### Reference

[ATAM — Architecture Tradeoff Analysis Method (SEI)](https://insights.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) — the canonical SEI framework for structured architectural reviews, with explicit role separation between facilitator (process) and evaluators (technical). The role-vs-process distinction is the operational basis for the audience separation this principle requires.

---

### 2. Checklists are living documents — versioned, periodically reviewed, retired when they outlive their usefulness

A governance checklist captures a moment's understanding of how a process should run. The process evolves, the organisation grows, the regulatory environment shifts, the technology stack changes — and the checklist is not automatically updated to match. A checklist that hasn't been reviewed in two years is not a checklist; it's archaeology. Items that no longer apply persist (and produce noise as people answer N/A repeatedly), items that should have been added are missing (and the gaps are filled by individual judgment instead of institutional memory), and the checklist's signal-to-noise ratio decays. The discipline is to treat checklists as living documents: under version control with diffs, with documented owners, on a documented review cadence, with a retirement path for items that no longer earn their place.

#### Architectural implications

- Each governance checklist has a documented owner (a named role, not just "the architecture team") and a documented review cadence (quarterly, semi-annually, on event triggers).
- Checklist changes go through a lightweight change process — proposed change, brief justification, owner approval — with a queryable history.
- Items are dated when added, with periodic review of whether each item still serves its purpose; items that consistently produce N/A or "not applicable" answers are flagged for retirement.
- The checklist's metadata travels with it: version, last reviewed date, owner, applicable scope — visible at the top, not buried in metadata files nobody reads.

#### Quick test

> Pick a governance checklist in your organisation. When was it last reviewed, who is its named owner, and what was the most recent change? If the answers are "we don't track that" or "it's been a while," the checklist is calcifying — and the next governance failure will reveal which items should have been added or removed years ago.

#### Reference

[Architecture Decision Records — Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — the seminal practical reference for treating governance artefacts (decisions, the templates and checklists around them) as living documents with status fields, supersession chains, and temporal lifecycle. The same discipline applied to ADRs applies to the checklists that surround them.

---

### 3. Granularity is the central craft — too generic produces ritual, too specific produces irrelevance

A governance checklist's value lives at a particular granularity. Too coarse — "review the architecture" — is no checklist at all; it just delegates the work to the reviewer's judgment with the appearance of process. Too fine — "verify that field 17 of the proposal template matches paragraph 3 of policy 4.2.1" — produces a checklist that applies to one specific scenario and nothing else, and triggers exception requests for everything outside that scenario. The right level lives in between: items that are specific enough to be testable ("does the proposal cite at least one alternative considered and the reason it was rejected?") but general enough to apply across the cases the checklist covers. Calibration takes iteration; the first version of a checklist is rarely at the right granularity, and the discipline is to refine it as items prove too coarse (consistently produce yes-answers without doing useful filtering) or too fine (consistently produce exception requests).

#### Architectural implications

- Checklist items are testable: a competent reviewer applying the item to the same artefact reaches the same yes/no — different judgments suggest the item is too coarse.
- Items that consistently produce "yes" without distinguishing good and bad cases are candidates for removal — they're filling the page without doing work.
- Items that consistently produce "this doesn't apply" or trigger exceptions are candidates for narrowing or splitting — the checklist is being applied across cases it wasn't designed for.
- The aggregate length of the checklist is itself a signal: a 50-item governance checklist is unlikely to be applied carefully each time; concision is a feature, not a constraint.

#### Quick test

> Pick the governance checklist most frequently applied in your organisation. What proportion of items consistently produce "yes" without distinguishing cases? What proportion produce "not applicable"? If both proportions are high, the checklist's granularity is mismatched — the items that always pass aren't filtering, and the items that don't apply are noise.

#### Reference

[Atul Gawande, *The Checklist Manifesto*](https://atulgawande.com/book/the-checklist-manifesto/) — the canonical practitioner-level treatment of checklist design across high-stakes domains; the granularity principles transfer directly to architectural governance. The book's distinction between "do-confirm" checklists (verify after action) and "read-do" checklists (read each item, then act) is itself an architectural choice that governance teams should make deliberately.

---

### 4. Checklists encode institutional memory — capturing lessons that shouldn't be re-learned

The most expensive way for an institution to learn is to repeat its own mistakes; a governance checklist is one of the cheapest places to capture the lessons of past mistakes so they don't repeat. Item: "verify the proposal addresses cross-region failover" — added after the incident in 2022 where a service was approved without a regional failure plan and went down during a regional outage. Item: "verify the proposal documents data sovereignty assumptions" — added after the regulatory finding that revealed undocumented cross-border data flows. Item: "verify the rollback plan has been tested in staging" — added after the production deployment that couldn't be rolled back because the rollback path had never been exercised. Each item earns its place by representing a category of failure the institution wants to prevent at scale; the checklist becomes the place where institutional memory operates without depending on which individuals remember.

#### Architectural implications

- New items are added to checklists as a routine output of post-incident reviews and audit findings — the checklist is a living capture point, not a historical artefact.
- Each item has a documented origin: a brief note on why it was added (the incident, the audit finding, the regulator question that motivated it) — so future reviewers understand whether to keep or retire the item as context evolves.
- When an item's originating concern is resolved through different means (architectural pattern that prevents the failure mode altogether, automated check that catches it earlier), the item becomes a candidate for removal — the checklist is the layer that catches what other layers don't.
- The checklist's items collectively reflect what the institution has learned the hard way; their combined weight is a meaningful artefact, even if any single item seems pedestrian.

#### Quick test

> Pick three items in your most-used governance checklist. For each, what specific incident, audit finding, or near-miss motivated its addition? If the answer for any of them is "I don't know — it's always been there," the item has lost its origin story and is at risk of being either obsolete (retire it) or undervalued (resurface its origin so the team understands why it earns its place).

#### Reference

[CMU SEI — Architecture Review Method library](https://insights.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) treats lessons-learned integration as a first-class outcome of structured reviews. The conceptual framing of checklists as institutional memory is treated extensively in [Atul Gawande's work](https://atulgawande.com/book/the-checklist-manifesto/) on aviation, surgical, and construction checklists — where the cost of repeated mistakes is a lifetime, not just a quarter.

---

### 5. Different governance moments need different checklists — proposal, exception, post-incident, periodic audit

Lumping all governance work into a single "governance checklist" obscures that the moments are categorically different. A *proposal review* asks: is this decision well-formed, has it considered alternatives, does it match institutional standards? An *exception review* asks: why does this case fall outside standards, what's the bounded scope, when is the exception revisited? A *post-incident review* asks: did the governance process catch this risk, did the right people see it in time, what should change? A *periodic audit* asks: across the last quarter, what did the governance system do, where did it work, where did it not? Each moment has a different audience, a different time horizon, a different action space, and therefore a different checklist. Trying to write one checklist that serves all four produces something that serves none of them well.

#### Architectural implications

- The governance system maintains distinct checklists for distinct moments: proposal review, exception request, post-incident review, periodic audit, role transition, escalation triage — each with its own audience, cadence, and action space.
- Each moment's checklist is owned and reviewed independently — the proposal-review checklist owner is not necessarily the audit-lead checklist owner.
- The checklists cross-reference each other where relevant: an exception review may surface the need for a proposal-review checklist update; a post-incident review may surface the need for new items in either.
- The system's overall health depends on the balance: proposal reviews without periodic audits produce drift; audits without proposals produce theatre; post-incident reviews without exception reviews produce repeated workarounds.

#### Quick test

> List the governance moments in your organisation that have a dedicated checklist. If the list is "the architecture review checklist" or "we just have one general one," the system is treating all moments as the same — and the moments that need different attention are getting whatever the general checklist accidentally covers.

#### Reference

[TOGAF](https://www.opengroup.org/togaf) provides the canonical taxonomy of architectural moments (architecture vision, business architecture, requirements management, governance) — each with distinct deliverables and review questions. The granularity is an enterprise framework's; the principle of moment-specific governance applies at any scale.

---

### 6. The checklist must actually be used — friction reduction and integration are part of the design

A checklist that exists in a wiki nobody opens, with friction higher than the cost of skipping it, will be skipped. The decision the team faces in the moment ("do I open the wiki and apply the checklist, or do I just make the call?") is a friction-vs-value tradeoff, and friction often wins. The architectural response is to design for actual use: integrate the checklist into the workflows where governance moments happen (PR templates, ADR templates, ARB agenda automation), measure whether it's being applied (proposals submitted with template completion, exceptions logged with full reviewer attestation), reduce friction where the friction isn't doing useful work (auto-fill known fields, link to standards rather than restating them), and remove items that consistently aren't used so they don't dilute the items that are. The discipline is honest: a checklist that nobody applies is doing zero governance work, regardless of how thoughtfully it was designed.

#### Architectural implications

- Checklists are integrated into the workflows where governance moments occur — not hosted in a separate documentation site that requires switching context.
- Application rates are measured: proportion of proposals that include completed checklist responses, proportion of exceptions that include full reviewer attestation, time-to-apply for routine reviews — these are governance system health metrics.
- Friction is reduced where it isn't producing value: pre-filled fields, references rather than restated content, structured templates that the checklist auto-validates against.
- Items that are consistently not applied are flagged for review: are they not being applied because reviewers don't see them, because they're hard to evaluate, because they're irrelevant? Each cause has a different remediation.

#### Quick test

> Pick the most consequential governance checklist in your organisation. What proportion of relevant decisions in the last quarter actually had this checklist applied, with reviewer attestation, before the decision shipped? If the answer is "we don't measure that" or "we assume it's most of them," the checklist is operating on faith rather than evidence — and its actual coverage is whatever the workflow produces, which may be a lot less than its nominal coverage.

#### Reference

[Atul Gawande, *The Checklist Manifesto*](https://atulgawande.com/book/the-checklist-manifesto/) treats the integration-into-workflow problem extensively — the surgical checklist's adoption depended on the operating-room workflow integrating the checklist's application, not just on the checklist existing. The architectural lesson transfers directly: governance checklists succeed when they're embedded into the moment of decision, not when they're filed for reference.

---

## Architecture Diagram

The diagram below shows the canonical governance-checklist architecture: distinct checklists for distinct governance moments (proposal review, exception review, post-incident review, periodic audit), each with named owner and review cadence; integration points where checklists live in workflow tools (ADR repos, PR templates, ARB agendas); a usage-telemetry layer measuring application rates; a feedback loop where post-incident reviews surface new items and audits flag obsolete ones.

---

## Common pitfalls when adopting governance-checklist thinking

### ⚠️ The all-purpose checklist

A single "architecture review checklist" is used for everything: proposals, exceptions, audits, post-incidents. It serves none of them well. Some items don't apply to most cases (and reviewers learn to skip them); others apply to specific cases that don't fit (and the checklist gets supplemented with ad-hoc items). The team produces governance theatre rather than governance.

#### What to do instead

Distinct checklists per moment. The proposal-review checklist is short, focused on whether the decision is well-formed. The exception-review checklist is focused on bounded scope and revisit conditions. The post-incident-review checklist is focused on surfacing process improvements. Each is owned, reviewed, and applied at the appropriate cadence.

---

### ⚠️ The checklist that hasn't been touched in years

The checklist captures the team's understanding from three years ago. The technology, regulatory environment, and organisation have changed. Items reference systems that no longer exist; missing items would have caught last quarter's incident. Reviewers know the checklist is stale and apply it ritually rather than substantively.

#### What to do instead

Documented owner, documented review cadence, documented retirement path. Quarterly or semi-annually, the owner reviews the checklist with the recent incident log and audit findings, adds items that earn their place, retires items that don't, dates the change. The checklist is a living document, not a historical artefact.

---

### ⚠️ Checklist items at the wrong granularity

Items are either "review the architecture" (too coarse, no actual filtering) or "verify field 17 matches paragraph 3 of policy 4.2.1" (too fine, applies only to one scenario). The checklist either lets everything through or triggers exceptions for everything that doesn't fit its narrow scope.

#### What to do instead

Items are testable but general. Iteration calibrates the granularity: items that always produce "yes" are too coarse and should be split or removed; items that always produce "not applicable" are too narrow and should be generalised or moved to a more specific checklist.

---

### ⚠️ Checklists divorced from workflow

The checklist lives in a wiki nobody opens. The team is supposed to apply it during reviews. In practice, half the time they don't, and the half that do apply it inconsistently. The checklist is doing zero governance work for most decisions.

#### What to do instead

Checklists integrated into the workflow tools where governance moments happen: PR templates, ADR templates, ARB agenda automation. Application is measured. The checklist meets the team where they're working, not in a separate documentation context.

---

### ⚠️ No telemetry on usage

The team assumes the checklist is being applied. Nobody measures whether it actually is. A post-incident review reveals that the relevant checklist item exists, but nobody applied it on the decision that produced the incident. The discovery comes too late.

#### What to do instead

Application rates are tracked: proportion of decisions in the relevant class that have a completed checklist with reviewer attestation. Low rates trigger investigation: is the checklist hard to find, is the workflow not surfacing it, are reviewers skipping it deliberately? Each cause has a different remediation.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Each governance checklist names its primary audience and the action space they have on findings ‖ Audience is explicit (ARB chair, architect-on-duty, audit lead, exception reviewer), not "anyone reviewing." Authority to act on findings is named. Confused audience produces both ritual and chaos. | ☐ |
| 2 | Each checklist has a named owner and documented review cadence ‖ Living-document discipline. The owner is a role, not "the team." The cadence is documented (quarterly, semi-annually, on event triggers). The metadata travels with the checklist visibly. | ☐ |
| 3 | Checklist items are at the right granularity — testable but general; calibrated iteratively ‖ Items that consistently produce "yes" without filtering are candidates for removal. Items that consistently produce "not applicable" are candidates for narrowing or splitting. The aggregate length is itself a signal. | ☐ |
| 4 | Items capture institutional memory — each has a documented origin (incident, audit finding, regulator question) ‖ Items earn their place by representing a category of failure the institution wants to prevent. The origin note keeps the rationale alive across people and time. | ☐ |
| 5 | Distinct checklists exist for distinct governance moments — proposal, exception, post-incident, periodic audit ‖ Each moment has its own audience, cadence, and action space, and therefore its own checklist. Lumping them into one produces something that serves no moment well. | ☐ |
| 6 | Checklists are integrated into the workflow tools where governance moments occur ‖ Embedded in PR templates, ADR templates, ARB agenda automation. Not hosted in a separate documentation site that requires context switching. The checklist meets the team where they work. | ☐ |
| 7 | Application rates are measured per checklist — completed responses with reviewer attestation, proportion of relevant decisions covered ‖ The system operates on evidence rather than faith. Low application rates trigger investigation of cause, not exhortation. | ☐ |
| 8 | Friction is reduced where it isn't producing value — pre-filled fields, references over restatement, structured templates ‖ The checklist's value is its application; friction higher than the cost of skipping ensures it gets skipped. Reducing friction where the friction isn't earning its place is part of the design. | ☐ |
| 9 | Post-incident reviews and audits surface items for addition or retirement ‖ The checklist is a living capture point. Reviews and audits are the routine source of new items; the same reviews are the source of retirement candidates as items lose relevance. | ☐ |
| 10 | The governance-checklist set is distinct from technical-review checklists in storage, naming, and discoverability ‖ The two sets serve different audiences and purposes. Mixing them produces both kinds of failure: governance items reviewed by people without authority to act on them, technical items evaluated by people without the expertise to judge them. | ☐ |

---

## Related

[`governance/review-templates`](../review-templates) | [`governance/roles`](../roles) | [`governance/scorecards`](../scorecards) | [`checklists/architecture`](../../checklists/architecture) | [`checklists/security`](../../checklists/security) | [`patterns/structural`](../../patterns/structural)

---

## References

1. [ATAM (SEI)](https://insights.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) — *sei.cmu.edu*
2. [ADR — Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — *cognitect.com*
3. [TOGAF](https://www.opengroup.org/togaf) — *opengroup.org*
4. [COBIT 2019 (ISACA)](https://www.isaca.org/resources/cobit) — *isaca.org*
5. [The Checklist Manifesto — Atul Gawande](https://atulgawande.com/book/the-checklist-manifesto/) — *atulgawande.com*
6. [ADR GitHub Organization](https://adr.github.io/) — *adr.github.io*
7. [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) — *aws.amazon.com*
8. [Architecture Advice Process — Andrew Harmel-Law](https://martinfowler.com/articles/scaling-architecture-conversationally.html) — *martinfowler.com*
9. [Apache Project Governance](https://www.apache.org/foundation/how-it-works.html) — *apache.org*
10. [DORA Metrics](https://dora.dev/) — *dora.dev*
