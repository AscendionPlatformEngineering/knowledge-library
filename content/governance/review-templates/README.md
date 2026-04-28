# Review Templates

The templates that structure the recurring artefacts of architecture governance — ADRs, RFCs, design specs, exception requests, post-incident reviews. Each template is an interface contract between the submitter and the reviewer: the submitter promises to address the questions the institution thinks matter; the reviewer commits to evaluating the answers given rather than asking unbounded new questions.

**Section:** `governance/` | **Subsection:** `review-templates/`
**Alignment:** ADR (Michael Nygard) | ADR GitHub Organization | RFC Process (IETF) | TOGAF

---

## What "review templates" actually means

A *template* is a pre-structured document that captures what the institution thinks matters about a class of artefact. The Architecture Decision Record (ADR) template, in its canonical [Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) form, has sections for *Status*, *Context*, *Decision*, and *Consequences* — and that minimal four-section structure encodes a particular theory of architectural decisions: that decisions are made under conditions (Context), that they have specific content (Decision), that they have downstream effects (Consequences), and that they have lifecycle (Status). An institution that adopts the ADR template inherits this theory; an institution that modifies the template (adding *Alternatives Considered*, *Decision Drivers*, *Stakeholders*, *Date*) is making explicit the additional things it thinks matter. The template's section design is the architectural artefact.

The same logic applies to other governance templates. An *RFC* (Request for Comments) template is for proposals — for a class of artefact whose purpose is to invite discussion before commitment, with sections for *Motivation*, *Proposal*, *Open Questions*, and *Discussion*. A *design spec* template is for committed designs with implementation detail — different purpose, different sections. An *exception request* template is for cases where standards don't apply — sections for *Standard*, *Why Excepted*, *Bounded Scope*, *Revisit Conditions*. Each template is shaped to what the institution wants to know about that kind of artefact.

The architectural shift is not "we adopted a template." It is: **the template's section structure encodes what the institution thinks matters about a class of decision; designing or adopting the template is itself an architectural choice that shapes thousands of subsequent decisions, and getting it wrong (sections that don't match what's needed, sections that are missing) compounds across the institution's entire decision history.**

---

## Six principles

### 1. The template's section structure encodes the institution's priorities — and getting it right is itself an architectural choice

Every section in a template is a question the institution is committing to ask of every artefact of that class. Add an *Alternatives Considered* section to the ADR template, and every ADR submitted thereafter must address what alternatives were considered and why they were rejected — the institution has decided that "did you consider alternatives?" is a question worth asking, every time, by default. Add a *Stakeholders* section, and every ADR must name who has a stake in the decision — the institution has decided stakeholder visibility matters. Omit a *Date* field, and the institution has implicitly decided that knowing when a decision was made isn't critical — a decision that often surprises the institution later. The choice of sections is an architectural decision in its own right; the template's design shapes the institution's future thinking at scale.

#### Architectural implications

- Each section in the template has a documented purpose — what question it answers and why the institution thinks that question matters — not just a name.
- The template's section list is reviewed periodically: are there sections that don't earn their keep (people consistently skip them or fill them generically)? Are there missing sections (the same kind of question keeps being asked of new ADRs in review, suggesting it should be a default)?
- The template owner can articulate the theory the template encodes — what kind of decision the template is shaped for, what it deliberately doesn't ask, what's out of scope.
- Changes to the template are decisions made deliberately, not aesthetic edits — adding or removing a section affects every future artefact and (potentially) every past one in retroactive review.

#### Quick test

> Pick the most-used review template in your organisation. For each section, what's the documented purpose, and what would change if it were removed? If the answer for any section is "I'm not sure why it's there," that section is no longer earning its place — and the artefacts using it are filling space rather than addressing the question the section was meant to answer.

#### Reference

[ADR — Michael Nygard's seminal post](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — the canonical reference for the four-section ADR structure (Status, Context, Decision, Consequences) with its underlying theory of architectural decisions. [ADR GitHub Organization](https://adr.github.io/) catalogues the variants and provides templates that institutions can fork, modify, and adopt — making the template-as-architectural-choice discipline explicit.

---

### 2. ADR templates and RFC templates serve different purposes — distinguish committed decisions from in-progress proposals

A common confusion: institutions adopt one template (often the ADR template) and use it for everything, including proposals that haven't yet been decided. The result is a Status field that's stuck at "Proposed" for months on what's effectively a discussion document, with the ADR's structure (Decision, Consequences) prematurely shaped before the discussion has resolved. Conversely, institutions that adopt an RFC template and use it for committed decisions end up with a Discussion section that's empty because the discussion already happened, and a Proposal section that reads as a Decision section in tone but lacks the committed-decision rigour. Distinguishing the two — separate templates for separate purposes — produces clearer artefacts in both cases. ADRs capture decisions: status, context, decision, consequences, with a clear lifecycle. RFCs capture proposals open for discussion: motivation, proposal, alternatives, open questions, discussion. The two converge over time (an RFC that's accepted becomes an ADR; an ADR that's superseded references the RFC that replaced it), but their templates encode different stages of decision-making.

#### Architectural implications

- The institution maintains separate templates for proposals (RFC-style) and decisions (ADR-style), with documented criteria for which template applies in which situation.
- The lifecycle relationship between RFCs and ADRs is documented: an RFC that's accepted produces an ADR; an ADR that's superseded by a new direction may reference the RFC that proposed the new direction.
- Status fields differ between the two: RFC statuses (draft, in-review, accepted, rejected) reflect discussion lifecycle; ADR statuses (proposed, accepted, deprecated, superseded) reflect decision lifecycle.
- The two templates link bidirectionally where relevant: each ADR can reference the RFC(s) that informed it; each accepted RFC can reference the ADR(s) it produced.

#### Quick test

> Pick three artefacts in your organisation's decision repository. For each, is it a proposal (still open for discussion) or a decision (committed)? Does its template structure match its purpose? If proposals and decisions are intermixed under one template, the conflation is producing artefacts that serve neither purpose well.

#### Reference

[Architecture Decision Records — Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) for the ADR pattern; [RFC Process (IETF)](https://www.ietf.org/standards/rfcs/) for the canonical RFC pattern at internet-engineering scale. The Rust language project's [RFC repository](https://github.com/rust-lang/rfcs) and the [Python PEP process](https://peps.python.org/) are well-documented practitioner-scale examples of RFC templates designed for proposals open for community discussion before commitment.

---

### 3. Templates evolve — too rigid produces noncompliance, too loose produces chaos

A template that doesn't change for years calcifies in two directions: the institution's priorities have shifted but the template hasn't, so submitters fill in sections that no longer matter and skip the consideration of things that now do. A template that changes constantly produces cognitive overhead and inconsistency — submitters never know which version applies, reviewers can't compare across versions, the artefact archive becomes a museum of template variants. The discipline is to evolve the template deliberately, on a documented cadence, with versioning that lets old artefacts be read in their original template's terms while new artefacts use the current template. Too rigid produces noncompliance (people stop using the template and just write free-form documents because the template doesn't fit); too loose produces chaos (everyone improvises, comparison and audit become impossible).

#### Architectural implications

- The template has a version field; every artefact records which template version produced it; the template's version history is queryable.
- Template changes are themselves decisions — they go through a lightweight ADR or RFC process, with documented motivation and review.
- Old artefacts produced under prior template versions remain readable in their original form; "compatibility" with new fields is optional rather than required (don't retroactively fill in 2018 ADRs with sections added in 2024).
- A template that's calcified (no change in 18+ months despite organisational evolution) is a flag for review; a template that's churning (3+ versions in a quarter) is a flag for stability concerns.

#### Quick test

> Pick your organisation's primary review template. What's its version number, when was the last change, and what was the change's documented motivation? If there's no version, no motivation, or no change in years despite organisational change, the template is on a path toward either noncompliance (people work around it) or chaos (people improvise). Both are losses of governance integrity.

#### Reference

[Architecture Decision Records GitHub Organization](https://adr.github.io/) treats template evolution as a first-class concern, with multiple template variants (Nygard, MADR, Y-Statement) representing different evolutionary outcomes from the same starting point. [Spotify's engineering culture posts](https://engineering.atspotify.com/) document template evolution at scale, including the trade-offs between template stability and adaptation to new contexts.

---

### 4. Metadata is as important as content — status, dates, owners, and supersession

The free-form prose sections of a template (Context, Decision, Consequences) get most of the attention; the metadata fields (Status, Date, Owner, Superseded By) often get treated as decoration. They aren't. The metadata is what makes the artefact archive *operational* rather than purely *informational*. Without a reliable Status field, you can't answer "which decisions are currently in force?" — a question audit, compliance, and onboarding all need to answer. Without Date, you can't answer "what was our policy on X as of June 2023?" — a question incident investigation needs to answer. Without Owner, you can't answer "who do I ask about this decision?" — a question every new engineer asks. Without Superseded By chains, you can't answer "what's the current decision on X?" when the original ADR was replaced — and the institution's history becomes a tangle. Metadata is the operational interface to the artefact archive.

#### Architectural implications

- Metadata fields are at the top of the template, prominently visible — not buried in a header that gets skipped.
- Status field uses a closed vocabulary (Proposed, Accepted, Deprecated, Superseded) — not free text — so queries across the archive return reliable results.
- Date fields capture both creation and last review (an ADR from 2019 may still be in force, but reviewers should know it hasn't been re-examined in five years).
- Supersession is a typed link, not a prose mention — the archive tooling can render the supersession chain and surface the current decision automatically.

#### Quick test

> Pick the question "what's our current policy on multi-region failover?" and try to answer it from your organisation's decision archive. Can you find the current decision in under 30 seconds, with confidence it hasn't been superseded? If the search requires reading prose to figure out which version is current, the metadata isn't doing operational work — and the archive is informational at best.

#### Reference

[ADR GitHub Organization](https://adr.github.io/) treats metadata (status, supersession links) as required template structure; the [MADR (Markdown ADR) variant](https://adr.github.io/madr/) extends the metadata further with explicit Decision Drivers and Considered Options fields. The discipline of typed metadata as operational interface is treated extensively in [Architecture Advice Process — Andrew Harmel-Law](https://martinfowler.com/articles/scaling-architecture-conversationally.html).

---

### 5. Templates support discovery if and only if they're designed for it

An institution with hundreds or thousands of ADRs, RFCs, and design specs accumulated over years has built an asset — but the asset is only valuable if the artefacts can be found when needed. Discovery requires three properties of the template: structured fields that can be indexed (closed-vocabulary status, owner, scope tags); searchable content (markdown is friendlier than custom binary formats; consistent section names enable searches like "find all ADRs whose Consequences section mentions latency"); and link integrity (cross-references that the archive's tooling can follow, including supersession chains and related-ADR links). A template that produces unsearchable artefacts (PDFs locked behind a documentation portal, free-form prose with inconsistent section names, broken cross-reference chains) builds a write-only archive — content goes in and is never effectively retrieved.

#### Architectural implications

- Template format is markdown or a similar text-based format that's grep-friendly, version-controllable, and searchable across modern tooling.
- Closed-vocabulary fields (status, scope tags, decision class) are indexed for query — "show me all accepted ADRs in the data-architecture scope" is a one-line query.
- Cross-reference links use stable identifiers (ADR numbers, slugs, URIs) that survive renames and reorganisation.
- The archive's tooling can render the corpus as both individual artefacts and as aggregated views (timeline, by-scope, by-owner, supersession graph).

#### Quick test

> Pick a current question your team is investigating. Try to find every relevant decision in your organisation's archive on that question, in under five minutes. If the search returns false negatives (relevant decisions you know exist but didn't surface) or false positives (irrelevant matches that drown the real ones), the archive's discoverability is broken — and the institutional knowledge is effectively unavailable to the people who need it.

#### Reference

[adr-tools](https://github.com/npryce/adr-tools) and [log4brains](https://github.com/thomvaill/log4brains) — practitioner tooling that operationalises the discoverability principles for ADR archives. The architectural framing of the decision archive as a queryable institutional asset (rather than a documentation dump) is treated in detail in [ThoughtWorks Technology Radar](https://www.thoughtworks.com/radar) commentary on architecture decision records.

---

### 6. The template is an interface contract between submitter and reviewer

When a submitter fills in a template and submits it for review, an implicit contract is in play: the submitter promises to address the questions the template asks (what's the context, what's the decision, what are the consequences, what alternatives were considered?), and the reviewer commits to evaluating the submission on those questions rather than asking unbounded new ones. The contract makes review tractable — reviewers don't ambush submitters with unrelated concerns, and submitters know what they need to address. When the contract breaks down — reviewers consistently demand things outside the template, submitters consistently leave template sections blank — the review process becomes adversarial. The architectural discipline is to treat the template as the contract: if reviewers consistently demand a question that's not in the template, that question should become a template section; if a template section is consistently left blank or filled trivially, it may not be a question the institution actually values.

#### Architectural implications

- The template is the agreed scope of review questions; reviewers raise out-of-scope concerns through a separate "discussion" thread or as proposed template additions, not as blockers on the current artefact.
- Template sections that are consistently left blank or filled trivially are flagged for review: are they not understood by submitters, are they not actually valued, do they belong in a different template?
- Reviewer questions that consistently come up outside the template are flagged as candidates for new sections — the template evolves toward what the institution actually wants to know.
- The contract is bidirectional: submitters owe addressing the template's questions; reviewers owe staying within the template's scope (or proposing extensions transparently).

#### Quick test

> Pick a recent review in your organisation. Did the reviewers' questions all map to template sections, or did they raise concerns outside the template? Were any template sections left blank or filled trivially? If both happened, the template-as-contract is breaking down — and the review process is operating on individual judgments rather than institutional commitments.

#### Reference

[Architecture Advice Process — Andrew Harmel-Law](https://martinfowler.com/articles/scaling-architecture-conversationally.html) treats the submitter-reviewer relationship explicitly as a contractual one, with the template (and the advice-seeking process around it) as the architectural artefact that scales decision-making across organisations. The same discipline applied to GitHub PR templates is treated in operational detail across many open-source project governance models.

---

## Architecture Diagram

The diagram below shows the canonical review-template architecture: distinct templates for distinct artefact classes (ADR, RFC, design spec, exception request, post-incident review), each with structured metadata and content sections; the lifecycle relationship between RFCs (proposals) and ADRs (decisions); the archive layer with versioned templates and queryable metadata; the review surface where submitters and reviewers operate against the template-as-contract.

---

## Common pitfalls when adopting review-template thinking

### ⚠️ The one-template-for-everything

The institution adopts the ADR template and uses it for proposals, exception requests, design specs, and incident reviews. The artefacts produced are uniformly mediocre: proposals end up with premature Decision sections; specs end up with thin Consequences sections (because consequences for a spec aren't the same as for a decision); exceptions end up with awkward Status fields. The template was designed for one purpose and is being asked to serve five.

#### What to do instead

Distinct templates for distinct artefact classes, each shaped to the questions the institution thinks matter for that class. Documented criteria for which template applies in which situation. The lifecycle relationships between templates (RFC → ADR, post-incident → ADR update) are explicit.

---

### ⚠️ The template that hasn't changed in five years

The template captured the institution's understanding from 2019. The organisation has grown 5x, the technology stack has changed, the regulatory environment has shifted. Submitters fill in sections that no longer reflect priorities; reviewers consistently raise questions outside the template. The template is doing 2019's governance for 2024's organisation.

#### What to do instead

Template evolution is itself a documented decision process, on a documented cadence. The template has a version field; every artefact records which version produced it. Changes are deliberate, motivated, and reviewed.

---

### ⚠️ Metadata as decoration

The template has Status, Date, Owner, and Supersession fields, but they're optional, free-text, and frequently left blank or inconsistently filled. The archive is technically organised but operationally unsearchable: "what's our current decision on X?" requires reading prose to determine which version is current.

#### What to do instead

Metadata fields are required, prominent, and use closed vocabularies. Status, Date, Owner, and Supersession are typed and indexed. The archive's tooling can answer operational questions — current decisions, decisions by scope, supersession chains — without prose interpretation.

---

### ⚠️ Templates trapped in PDF

The institution hosts review templates as PDFs in a documentation portal. The artefacts produced are PDFs. Search across the archive doesn't work; cross-references are static text; version control is "save as v2_final_FINAL.pdf." The decision archive is write-only — content goes in, retrieval is broken.

#### What to do instead

Markdown or similar text-based formats; storage in version control; structured fields rendered by the archive's tooling. Search, cross-reference, and aggregation queries are all first-class. The archive becomes a queryable institutional asset rather than a write-only repository.

---

### ⚠️ Reviewers ambushing submitters

A submitter fills in the template and submits for review. Reviewers raise concerns outside the template's scope, demanding the submitter address considerations that weren't in the template they used. The submitter, having no way to know what was actually expected, ends up rewriting iteratively against an unbounded review surface. Trust between submitters and reviewers erodes.

#### What to do instead

The template is the agreed scope of review questions. Out-of-scope concerns are raised separately (as discussion threads, or as proposed template additions), not as blockers on the current artefact. Reviewer questions that consistently come up outside the template are candidates for new sections, surfaced through the template's evolution process.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Each section in the template has a documented purpose explaining what question it answers and why the institution values it ‖ Section design is an architectural choice. Sections without documented purpose drift toward irrelevance; the template's theory becomes opaque to its users. | ☐ |
| 2 | Distinct templates exist for distinct artefact classes — ADR, RFC, design spec, exception request, post-incident review ‖ Each artefact class has its own purpose, its own questions, its own lifecycle. One-template-for-everything produces artefacts that serve no class well. | ☐ |
| 3 | The lifecycle relationships between templates are documented and operational ‖ RFC → ADR (proposal becomes decision), ADR → ADR (supersession), post-incident → ADR update. Bidirectional links where relevant. | ☐ |
| 4 | Templates have a version field; every artefact records the template version that produced it ‖ Versioning enables both retrospective reading (this 2019 ADR was written under that version's conventions) and forward evolution without retroactive churn. | ☐ |
| 5 | Template changes are deliberate, motivated, and reviewed ‖ Template evolution is itself a decision process. Changes go through a lightweight ADR or RFC. Calcified or churning templates are flags for review. | ☐ |
| 6 | Metadata fields are required, prominent, and use closed vocabularies ‖ Status (Proposed/Accepted/Deprecated/Superseded), Date (created and last reviewed), Owner (named role), Supersession (typed link). The metadata is the operational interface to the archive. | ☐ |
| 7 | Templates are stored in text-based formats in version control with grep-friendly section names ‖ Markdown over PDF, version control over file shares, consistent section names over free-form structure. The archive is a queryable institutional asset. | ☐ |
| 8 | Cross-references use stable identifiers that survive renames and reorganisation ‖ ADR numbers, slugs, URIs. Broken cross-references degrade the archive's value over time; stable identifiers preserve it. | ☐ |
| 9 | The template is treated as a contract between submitter and reviewer ‖ Submitters address the template's questions; reviewers stay within the template's scope. Out-of-scope concerns are raised separately, not as blockers. The contract makes review tractable. | ☐ |
| 10 | Sections consistently left blank are flagged for review; reviewer questions consistently outside the template are candidates for new sections ‖ The template evolves toward what the institution actually values, surfaced through usage patterns rather than design-time guesses. | ☐ |

---

## Related

[`governance/checklists`](../checklists) | [`governance/roles`](../roles) | [`governance/scorecards`](../scorecards) | [`adrs`](../../adrs) | [`templates`](../../templates) | [`patterns/structural`](../../patterns/structural)

---

## References

1. [ADR — Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — *cognitect.com*
2. [ADR GitHub Organization](https://adr.github.io/) — *adr.github.io*
3. [RFC Process (IETF)](https://www.ietf.org/standards/rfcs/) — *ietf.org*
4. [TOGAF](https://www.opengroup.org/togaf) — *opengroup.org*
5. [Architecture Advice Process — Andrew Harmel-Law](https://martinfowler.com/articles/scaling-architecture-conversationally.html) — *martinfowler.com*
6. [ThoughtWorks Technology Radar](https://www.thoughtworks.com/radar) — *thoughtworks.com*
7. [The Checklist Manifesto — Atul Gawande](https://atulgawande.com/book/the-checklist-manifesto/) — *atulgawande.com*
8. [Apache Project Governance](https://www.apache.org/foundation/how-it-works.html) — *apache.org*
9. [Spotify Engineering Culture](https://engineering.atspotify.com/) — *atspotify.com*
10. [Kubernetes Governance](https://kubernetes.io/community/) — *kubernetes.io*
