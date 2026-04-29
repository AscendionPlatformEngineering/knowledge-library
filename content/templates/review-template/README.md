# Review Template

The artefact a review produces — recognising that the template's scope statement, severity-classified findings, actionable per-finding messages, documented decisions with named authority, captured reviewer-author dialogue, and outcome-traceability to system change are what determine whether the review document is a binding decision artefact or a record of meetings that didn't actually resolve anything.

**Section:** `templates/` | **Subsection:** `review-template/`
**Alignment:** ATAM (Architecture Tradeoff Analysis Method) | ARID (Active Reviews for Intermediate Designs) | Google Engineering Practices | C4 Model

---

## What "review template" means — and how it differs from "reviews as discipline"

This page is about the *review document template* — the specific structured artefact that captures the result of an architecture review, design review, or other formal evaluation. The discipline of *how reviews work as governance instruments* — when reviews are required, who reviews, what authority reviews carry, how reviews integrate with the team's decision flow — lives in [`governance/review-templates`](../../governance/review-templates) and the broader governance section. Same family, different operational concern: this page owns the document; governance owns the meta-discipline.

A *primitive* review document is what gets produced when "we should write up the review somewhere": meeting notes that capture some of the discussion, a list of issues raised that may or may not be ranked by importance, an implicit decision communicated by the absence of objection. The reviewer's concerns get partially captured; the author's responses get partially captured; the decision to proceed or revise is implicit; the relationship between the review and the system changes that followed is unrecoverable. Six months later, when someone asks "why did we accept that approach despite the security concern raised in review?" — the review document doesn't say.

A *production* review document is a *designed artefact with structured fields*. Its *scope statement* at the top defines what's being reviewed, against what criteria, at what depth — so the reader can calibrate what the review covered and what it didn't. Its *findings* are classified by *severity* with a documented vocabulary (blocker / significant / minor / observation) and explicit criteria for each tier — so future readers can distinguish concerns the reviewer flagged as must-address from concerns flagged as nice-to-address. Each finding is *actionable*: what the issue is, where it occurs (specific reference into the system or design), and what to do about it — not vague concerns but specific issues with specific resolution paths. The *decision* is documented with named decision authority and rationale: proceed / proceed-with-changes / defer / reject; who decided; why. The *reviewer-author dialogue* is captured — not just the findings, but the back-and-forth that produced the decision, including objections raised, counterarguments, and resolutions reached. The *outcome traceability* links the review to specific system changes: what got fixed (with PR links), what was deferred to follow-up (with ticket links), what was accepted as-is (with explicit acknowledgement and rationale).

The architectural shift is not "we have review documents." It is: **the review document is a designed artefact whose scope statement, severity-classified findings, actionable findings, decisions with named authority, dialogue capture, and outcome traceability determine whether the review's work survives the review meeting or evaporates into folklore — and treating the document as meeting notes produces a corpus where the team's accumulated review judgment can't be recovered when needed.**

---

## Six principles

### 1. Scope statement at the top — what's being reviewed, against what criteria, at what depth

A review document without a scope statement leaves the reader (and especially the reader who wasn't in the review meeting) unable to calibrate what the review actually covered. Was this a security review or a general architecture review? Did the reviewer evaluate operability? Did the reviewer have access to the runtime configuration, or only to the design document? The architectural discipline is to open the document with an explicit *scope statement* that addresses three dimensions: *what's being reviewed* (the system / design / change / specific subsystem), *against what criteria* (which dimensions: architecture, security, operability, scalability, cost — typically with a checklist or framework name), and *at what depth* (design-document review only, code review with a sample of files, architecture deep-dive with the team, runtime evaluation in a staging environment). Without scope, the absence of findings doesn't tell readers whether the topic was clean or whether it wasn't examined.

#### Architectural implications

- The scope section names the artefact under review (with version or reference) — design doc URL, repo SHA, system version, architecture revision.
- The criteria are explicit: which dimensions were evaluated, with reference to the framework or checklist used (e.g., AWS Well-Architected, [`checklists/architecture`](../../checklists/architecture), team-specific standards).
- The depth of review is documented: design review of provided documents only / code review of files X, Y, Z / runtime evaluation in environment W / full deep-dive with author present.
- Out-of-scope dimensions are explicitly noted: "this review did not evaluate cost or operational readiness — those are subjects of separate reviews."

#### Quick test

> Pick a recent review document in your organisation. Reading only its scope section, can you tell what was reviewed, against what criteria, at what depth? If the scope is implicit ("review of the new payment service") rather than explicit (system + version + criteria + depth), the document leaves future readers unable to interpret what the review's silence on a topic actually means.

#### Reference

[ATAM — Architecture Tradeoff Analysis Method](https://insights.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method-atam-eight-years-of-experience/) treats scope-explicit review as a primary discipline; the canonical ATAM evaluation begins with documented scope. [ARID — Active Reviews for Intermediate Designs](https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=6276) similarly opens with explicit scoping.

---

### 2. Findings classified by severity with documented criteria — blocker / significant / minor / observation

A finding marked simply "issue" tells the reader nothing about how seriously to take it. The author confronted with a list of unranked findings either treats them all as urgent (over-respond) or treats them all as minor (under-respond); without ranking, the reviewer's calibration is lost. The architectural discipline is *severity classification* with a documented vocabulary and explicit criteria. *Blocker*: the finding must be addressed before the change proceeds; the change should not ship until resolved. *Significant*: the finding should be addressed; ignoring it incurs material risk; the change can proceed only if the team explicitly accepts the risk with rationale. *Minor*: the finding should be addressed but isn't urgent; the change can proceed and the finding becomes follow-up work. *Observation*: the finding is informational; no action required. Each tier's criteria are documented at the team or organisation level; reviewers calibrate against the same scale; readers can interpret the severity without re-litigating each finding.

#### Architectural implications

- The severity vocabulary is documented at organisation level (typically 4 tiers): blocker / significant / minor / observation. Some organisations use 3 tiers or a numeric scale; the principle is consistency across reviews.
- Each tier has criteria documented: a blocker is a finding meeting criteria X (e.g., security vulnerability, data-correctness risk, regulatory non-compliance); a significant finding meets criteria Y; etc.
- Findings are tagged with severity in the document, prominently and consistently — ideally formatted such that all blockers can be visually located at a glance.
- Severity is calibrated against the criteria, not against the reviewer's mood; a pattern of blockers turning into "well, we can ship anyway" is a calibration signal that the criteria are too strict or that decision authority is not respecting the severity classification.

#### Quick test

> Pick a recent review document. Are findings classified by severity, with the severity vocabulary documented? If findings are unranked or ranked subjectively, the document is forcing every reader to re-evaluate each finding — and the calibration the reviewer applied is being lost in transmission.

#### Reference

[Google Engineering Practices Documentation](https://google.github.io/eng-practices/) covers severity-classified review at code-review level; the discipline transfers to architecture review. [ATAM — Architecture Tradeoff Analysis Method](https://insights.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method-atam-eight-years-of-experience/) operationalises severity classification through risk-themed analysis.

---

### 3. Each finding is actionable — what's wrong, where, what to do about it

A finding stated as "concerns about scalability" tells the author that the reviewer is concerned but not what specifically to address. The author's response is to either ask the reviewer for more detail (scheduling cost) or guess and re-submit (rework cost). The architectural discipline is to write findings with three explicit elements: *what's wrong* (the specific issue, in language the author can act on), *where* (specific reference into the artefact under review — design section number, code file, configuration line, architecture component), *what to do about it* (the proposed resolution, even if the resolution is "evaluate alternatives X and Y"). The discipline pays compound returns: actionable findings get fixed; vague findings don't, and re-surface in the next review.

#### Architectural implications

- Each finding has the three-element structure: issue, location, recommendation. Templates that enforce this structure (per-finding fields rather than free-form prose) help reviewers maintain the discipline.
- The "where" is specific enough that the author can locate the issue without re-reading the full artefact: design document section reference, code file and line, architecture component name, configuration key.
- The "what to do" is the reviewer's recommended resolution, not necessarily the only path; it gives the author a starting point. If the reviewer doesn't have a recommendation, the finding might be better expressed as a question rather than a finding.
- For complex findings spanning multiple locations, the finding is decomposed into multiple specific findings rather than one diffuse one.

#### Quick test

> Pick a recent review document. Pick three findings. For each, are the issue, location, and recommendation all explicit? If findings are vague ("scalability concerns") or have no recommendation ("fix this somehow"), the author is forced to interpret the finding before they can act on it — and interpretation costs that compound across many findings.

#### Reference

[Google Engineering Practices Documentation](https://google.github.io/eng-practices/) treats actionable feedback as a primary code-review discipline; the discipline transfers to architecture review at framework level.

---

### 4. Decisions documented with named authority and rationale

A review meeting that ends with "the team will think about it" or "we'll see how it goes" hasn't actually decided anything. The author leaves the meeting unsure what was agreed; future readers can't tell what was decided versus what was discussed. The architectural discipline is *explicit decision documentation*: each review concludes with one of a small set of documented decisions — *proceed* (the change ships as proposed), *proceed with changes* (the change ships after specific findings are addressed; the changes are listed), *defer* (the change is paused until specific conditions are met; the conditions are listed), *reject* (the change is not adopted; the reason is documented). The decision is attributed to a named decision authority — the architect, the reviewer, the team lead, the architecture review board — depending on the team's governance. The rationale is captured: why this decision was reached, particularly when it goes against any reviewer's recommendation.

#### Architectural implications

- The decision section is a primary part of the document, not buried in conclusion prose. The decision vocabulary is small and documented (proceed / proceed-with-changes / defer / reject).
- Decision authority is named: who decided, with what authority. For team decisions, the team is named; for individual decisions, the individual is named.
- Rationale is documented: why the decision was reached. This is especially important when decisions go against severe findings (proceeding despite a blocker is a documented and audited choice, not an oversight).
- For "proceed with changes," the required changes are listed explicitly; the decision references them, and the outcome traceability section later confirms each was addressed.

#### Quick test

> Pick a recent review document. What was the decision, who decided, and what was the rationale? If any of these is implicit ("the team felt it was probably fine"), the document hasn't recorded a decision — and future readers can't tell whether the change was authorised or whether nothing was actually agreed.

#### Reference

[ATAM — Architecture Tradeoff Analysis Method](https://insights.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method-atam-eight-years-of-experience/) treats decision documentation as central to architectural review. The same discipline applies to lighter-weight design reviews.

---

### 5. Reviewer-author dialogue is captured — not just findings but the back-and-forth that produced the decision

A review document that captures only the findings and the final decision misses an important layer: the *dialogue* between reviewer and author that often produced the resolution. The reviewer raised a concern; the author responded with context or a counter-proposal; the reviewer either accepted the response or refined the concern; eventually a resolution was reached. The resolution alone tells the reader *what* was decided; the dialogue tells them *why*. Future readers facing similar concerns benefit enormously from seeing how the original reasoning unfolded — including responses that were considered and rejected. The architectural discipline is to capture this dialogue alongside the findings, either as threaded comments on each finding or as a discussion section that walks through the major exchanges.

#### Architectural implications

- Per-finding fields include a "dialogue" or "discussion" thread that captures author responses, reviewer follow-ups, and the eventual resolution.
- The dialogue is captured at sufficient depth to be useful but not so much that it overwhelms the findings — typically a few exchanges per finding rather than full meeting transcripts.
- Substantive dissent is preserved: if a reviewer raised a concern that the team decided not to address, the concern and the rationale for not addressing it are both visible. Future readers see what was knowingly accepted.
- Tooling supports the dialogue (PR-style comment threads, document review systems with inline comments) — though the principle is the dialogue itself, not any particular tool.

#### Quick test

> Pick a recent review document. Was substantive disagreement captured (a finding the author disputed), or only the findings the author accepted? If disagreement isn't visible, the document is showing the consensus output but hiding the reasoning that produced it — and future readers can't tell what was knowingly accepted versus what was overlooked.

#### Reference

[Google Engineering Practices Documentation](https://google.github.io/eng-practices/) treats reviewer-author dialogue capture as central to code review; the principles extend to architecture review.

---

### 6. Outcome traceability — what got fixed, what was deferred, what was accepted as-is

A review document that ends with "decision: proceed with changes" but never confirms whether the changes were actually made is incomplete. Six months later, the team that needs to know whether the security finding from review actually got addressed has no way to tell — the review says it was supposed to be addressed; the system either was or wasn't changed; the linkage is missing. The architectural discipline is *outcome traceability*: each finding's resolution is linked to specific system changes (PR URLs, commit hashes, deploy records) for things that were fixed; ticket links for things that were deferred to follow-up work; explicit "accepted as-is" annotations for findings that the team decided not to act on, with the rationale recorded. Outcome traceability turns the review document into a binding contract whose fulfilment is auditable.

#### Architectural implications

- Each finding has a resolution status: Fixed (with link to PR / commit / deploy), Deferred (with link to ticket / issue), Accepted-as-is (with rationale).
- The traceability is closed-loop: when the deferred ticket is eventually completed, the review document is updated (or the ticket links back to the review document so the linkage is recoverable).
- For "proceed with changes" decisions, the document confirms each required change was made before the change was considered complete.
- Reviews with persistently un-closed deferrals are surfaced through governance: a backlog of deferred review findings older than N months is a calibration signal that follow-up isn't happening.

#### Quick test

> Pick a review from six months ago in your organisation. Walk its findings: for each, can you tell whether it was fixed, deferred, or accepted as-is? If the linkage is missing, the review's recommendations didn't have a closing mechanism — and the team that depended on those recommendations being addressed has no way to verify they were.

#### Reference

The outcome-traceability discipline transfers from code-review practice ([Google Engineering Practices Documentation](https://google.github.io/eng-practices/)) to architecture review. [Backstage — Software Catalog](https://backstage.io/docs/features/software-catalog/) and similar tools operationalise traceability between review documents and the system changes they produced.

---

## Review Document Structure

The diagram below shows the canonical structure of a review document as a class diagram: a Review aggregates Scope, Findings (each with Severity, Location, and Recommendation), Dialogue threads, a Decision (with named authority and rationale), and Outcome traceability links to system changes. The document is a structured artefact whose fields determine whether the review's work survives the meeting.

---

## Common pitfalls when adopting review-template thinking

### ⚠️ Implicit scope — readers can't calibrate what was covered

The review document doesn't say what was reviewed, against what criteria, at what depth. The absence of findings on a topic could mean it was examined and found clean, or it could mean it wasn't examined at all.

#### What to do instead

Explicit scope statement at the top: artefact under review with version, criteria evaluated (with framework reference), depth of review. Out-of-scope dimensions explicitly noted.

---

### ⚠️ Unranked findings — calibration lost

Findings are listed without severity classification. The author treats all findings as equally urgent (over-respond) or equally minor (under-respond). The reviewer's calibration is lost.

#### What to do instead

Severity vocabulary documented at organisation level (blocker / significant / minor / observation). Each tier has criteria. Findings tagged with severity, formatted for visual distinction.

---

### ⚠️ Vague findings without recommendation

"Scalability concerns" / "consider security implications" / "could be cleaner." The author doesn't know what specifically to address or what good would look like.

#### What to do instead

Each finding has three elements: what's wrong, where (specific reference), what to do (recommended resolution). If no recommendation exists, express as a question rather than a finding.

---

### ⚠️ Implicit decision — no clear outcome

The review meeting ended with discussion but no documented conclusion. Future readers can't tell what was actually decided.

#### What to do instead

Documented decision from a small vocabulary (proceed / proceed-with-changes / defer / reject), attributed to named authority, with rationale. For "proceed with changes," required changes are listed explicitly.

---

### ⚠️ No outcome traceability — recommendations dangle

The review said the change should ship after addressing finding X. Did it? The document doesn't say; the system either was or wasn't changed; the linkage between recommendation and outcome is missing.

#### What to do instead

Each finding's resolution linked to system changes (PR, commit, deploy) for fixes; ticket links for deferrals; explicit "accepted as-is" with rationale for findings the team decided not to act on. The review becomes an auditable contract.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Scope statement at the top names artefact (with version), criteria evaluated, and depth of review ‖ Out-of-scope dimensions explicitly noted. The reader can calibrate what the review covered without inference. | ☐ |
| 2 | Findings classified by severity drawn from a documented organisational vocabulary ‖ Blocker / significant / minor / observation, with documented criteria per tier. Reviewers calibrate against the same scale. | ☐ |
| 3 | Each finding has three elements: what's wrong, where (specific reference), what to do ‖ Specifics rather than vague concerns. The author can act on the finding without interpretation cost. | ☐ |
| 4 | Findings are formatted for visual distinction by severity ‖ All blockers can be visually located at a glance. The document's structure surfaces the most important findings first. | ☐ |
| 5 | Decision drawn from documented vocabulary — proceed / proceed-with-changes / defer / reject ‖ Each option's meaning is documented at organisation level. The decision is binary, not a discussion summary. | ☐ |
| 6 | Decision authority is named — who decided, with what authority ‖ Team / individual / review board, depending on governance. The decision can be attributed and audited. | ☐ |
| 7 | Decision rationale is documented, especially when going against severe findings ‖ Proceeding despite a blocker is a documented choice, not an oversight. The rationale is recoverable for future readers. | ☐ |
| 8 | Reviewer-author dialogue is captured per finding, including substantive disagreement ‖ The reasoning behind the decision is visible. Future readers see what was knowingly accepted versus what was overlooked. | ☐ |
| 9 | Each finding has resolution status — Fixed (with PR link), Deferred (ticket link), Accepted-as-is (rationale) ‖ Outcome traceability is closed-loop. The review becomes an auditable contract. | ☐ |
| 10 | The review template is a documented standard the team uses for all reviews ‖ The template is governance-controlled; new reviews follow the same structure. The corpus is consistent across time and reviewers. | ☐ |

---

## Related

[`templates/adr-template`](../adr-template) | [`templates/scorecard-template`](../scorecard-template) | [`governance/review-templates`](../../governance/review-templates) | [`governance/roles`](../../governance/roles) | [`checklists/architecture`](../../checklists/architecture)

---

## References

1. [ATAM — Architecture Tradeoff Analysis Method](https://insights.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method-atam-eight-years-of-experience/) — *insights.sei.cmu.edu*
2. [ARID — Active Reviews for Intermediate Designs](https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=6276) — *resources.sei.cmu.edu*
3. [Google Engineering Practices Documentation](https://google.github.io/eng-practices/) — *google.github.io*
4. [C4 Model — Architecture Reviews](https://c4model.com/) — *c4model.com*
5. [Google SRE Workbook — Production Readiness Reviews](https://sre.google/workbook/evolving-sre-engagement-model/) — *sre.google*
6. [AWS Well-Architected Tool](https://aws.amazon.com/well-architected-tool/) — *aws.amazon.com*
7. [Microsoft Engineering Fundamentals Playbook](https://microsoft.github.io/code-with-engineering-playbook/) — *microsoft.github.io*
8. [Backstage — Software Catalog](https://backstage.io/docs/features/software-catalog/) — *backstage.io*
9. [Building Evolutionary Architectures (Ford et al.)](https://www.oreilly.com/library/view/building-evolutionary-architectures/9781491986356/) — *oreilly.com*
10. [Diátaxis Documentation Framework](https://diataxis.fr/) — *diataxis.fr*
