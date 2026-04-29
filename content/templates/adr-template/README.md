# ADR Template

The artefact engineers fill in to record an architectural decision — recognising that the ADR's title precision, status lifecycle, context articulation, decision specificity, consequence enumeration (intended outcomes and accepted trade-offs), and reference anchoring are what determine whether the document accumulates as institutional memory the team can navigate years later or as historical noise that doesn't help anyone.

**Section:** `templates/` | **Subsection:** `adr-template/`
**Alignment:** Documenting Architecture Decisions (Nygard) | MADR — Markdown ADRs | Y Statements (Zalando) | ADR Tools

---

## What "ADR template" means — and how it differs from "ADRs as discipline"

This page is about the *template* — the specific structured document an engineer fills in when recording an architectural decision: what fields the document has, what each field is for, what good content in each field looks like, and how the document evolves through its lifecycle. The discipline of *how ADRs work as governance instruments* — when ADRs are required, who reviews them, how they integrate with the team's decision-making process, what authority they carry — lives in [`governance/`](../../governance) at section level. Same family, different operational concern: this page owns the artefact; governance owns the meta-discipline.

A *primitive* ADR is what gets written when "we should document this decision somewhere": a free-form paragraph in a wiki, an email thread that nobody can find later, a code comment, a Slack message. The decision was made; some record exists; the team that needs to understand the rationale six months later can't, because the record is unstructured, uncategorised, and unfindable. The decision becomes folklore, then gets forgotten, then gets re-litigated when someone proposes the alternative the team had originally rejected for reasons nobody now remembers.

A *production* ADR is a *designed document with structured fields*. Its *title* captures the decision precisely (not "database choice" but "Adopt PostgreSQL with logical replication for the order-management transaction store") so that the title alone is sufficient to retrieve the right ADR years later. Its *status* is tracked through a documented lifecycle: Proposed → Accepted → Deprecated → Superseded; the status is not metadata but a primary field, and lifecycle transitions are themselves recorded with date and reason. Its *context* articulates the forces in play — the constraints, requirements, trade-off space, and current state that made this decision necessary — so a reader years later can understand why the decision was needed at all. Its *decision* states what was chosen in active voice and at sufficient specificity to be verifiable ("we will use X with configuration Y" not "X seems good"). Its *consequences* enumerate both the intended outcomes the decision was supposed to produce and the accepted trade-offs (what becomes harder, what risks were knowingly taken, what alternatives were foreclosed). Its *references* anchor the decision in evidence: what alternatives were evaluated, what was prototyped, what research informed the choice. Each field has a defined purpose; what fills each field is calibrated to that purpose.

The architectural shift is not "we have ADRs." It is: **the ADR is a designed document whose title precision, status lifecycle, context articulation, decision specificity, consequence enumeration, and reference anchoring determine whether the team's accumulated decisions form a navigable institutional memory or an undifferentiated archive of past meetings — and treating ADRs as free-form prose produces a corpus that doesn't help future decisions.**

---

## Six principles

### 1. The title captures the decision precisely — searchable retrieval years later depends on it

The ADR's title is the highest-leverage field in the document. It's what appears in the index, in the search results, in the cross-reference; it's what a reader uses to decide whether to open the document. A title like "Database choice" tells future readers nothing about what was decided or why this ADR is the right one to read. A title like "Adopt PostgreSQL with logical replication for the order-management transaction store" tells future readers (a) what was decided, (b) which subsystem the decision concerns, and (c) what specific configuration was adopted. The architectural discipline is to write titles that are *self-contained statements of the decision* — verb-phrased, specific, and contextualised. The rule is operational: a reader should be able to determine from the title alone whether this is the ADR they're looking for, without opening the document.

#### Architectural implications

- Titles are verb-phrased decisions, not noun-phrased topics: "Adopt event sourcing for order state transitions" rather than "Event sourcing." The title states *what* was decided, not just the topic of decision.
- Titles include the subsystem or scope where context-disambiguation requires it: "Use Redis as session store for web tier" rather than just "Use Redis" — across a multi-system architecture, "Redis" appears many times, and the title must distinguish.
- Titles include the specific choice's distinguishing detail when it matters: "Adopt PostgreSQL with logical replication for the order store" rather than "Adopt PostgreSQL" — the replication choice may itself be a decision worth surfacing in the title.
- Titles avoid hedging language ("Consider", "Evaluate", "Possibly") in Accepted ADRs. Hedging in the title signals the decision wasn't made; if the decision was made, the title states it as such.

#### Quick test

> Pick five recent ADRs from your organisation. Reading only the titles, can you determine what each decided? If multiple titles are vague nouns ("Caching", "Authentication", "Logging") rather than specific decisions, the corpus has lost the searchability that titles are supposed to provide — and finding the right ADR among many requires opening each one.

#### Reference

[Documenting Architecture Decisions (Nygard)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) is the seminal articulation of ADR practice; title discipline is treated alongside the other structural elements. [MADR — Markdown ADRs](https://adr.github.io/madr/) provides a standardised template format including title conventions.

---

### 2. Status is tracked through a documented lifecycle — Proposed / Accepted / Deprecated / Superseded

A primitive ADR has no status field — it exists or it doesn't, and the reader has to infer whether the decision is still current. A production ADR carries its status as a *primary field*, with the status drawn from a small documented vocabulary: *Proposed* (the decision is under review and not yet binding); *Accepted* (the decision is binding; the team is implementing or has implemented it); *Deprecated* (the decision is no longer the team's preferred approach but no replacement has been chosen); *Superseded by ADR-NNN* (the decision has been replaced by a specific newer decision; the link is in the status itself). Lifecycle transitions are recorded with date and reason — the document accumulates its own history. The discipline pays compound returns: a reader looking at any ADR can immediately see whether the decision still applies, whether it's been replaced, and what replaced it.

#### Architectural implications

- Status appears prominently at the top of the document, not buried in metadata; it's one of the first things a reader sees.
- The status vocabulary is documented and standardised; teams choose from a small fixed set rather than inventing labels.
- Lifecycle transitions are appended to the document as the ADR moves through states: "Status changed to Accepted on 2024-03-15 by team review" / "Status changed to Superseded by ADR-0042 on 2025-01-08, see that document for the current decision."
- Cross-references between superseded and superseding ADRs are bidirectional: the superseded ADR points forward to its successor; the successor points back to what it replaced.

#### Quick test

> Pick the oldest ADR in your organisation. What's its status, and how was that status established — by an explicit transition with date and reason, or implicitly because the document hasn't been touched in years? If the status isn't explicit, readers can't tell whether the decision still applies, and the corpus stops being a current reference and starts being an archaeological record.

#### Reference

[ADR Tools (npryce)](https://github.com/npryce/adr-tools) operationalises lifecycle management at command-line level, with `adr supersede` as a primary operation. [MADR — Markdown ADRs](https://adr.github.io/madr/) provides the canonical status vocabulary used across most ADR practice.

---

### 3. Context articulates the forces in play — what made this decision necessary

The decision section says *what* was chosen; the context section says *why the decision was needed at all*. A reader years later approaching the ADR has lost the surrounding situation: the constraints that applied at the time, the requirements that drove the choice, the trade-off space the team was navigating, the state of the system that made this decision relevant. Without context, the decision looks arbitrary — and the temptation is to second-guess it ("why didn't they just use X?") because the considerations that ruled X out are no longer visible. The architectural discipline is to write context that *captures the forces*: requirements, constraints, current state, alternatives considered, and the trade-off space those alternatives spanned. Context isn't autobiography; it's the situational frame that makes the decision intelligible to a reader who wasn't there.

#### Architectural implications

- Context describes the *requirements* the decision had to meet (functional and non-functional: throughput targets, consistency guarantees, operational constraints).
- Context describes the *constraints* in play (existing systems that had to integrate, regulatory requirements, team capability, time budget, cost envelope).
- Context describes the *current state* — what existed before the decision, what wasn't working, what motivated change.
- Context describes the *alternatives considered* and the trade-off space across them: not "we chose X" but "X, Y, and Z were the candidates; X traded A for B, Y traded B for C, Z required capability we don't have."

#### Quick test

> Pick a recent ADR in your organisation. Reading only its context section, can you understand why this decision was needed? Could you defend the chosen option against an alternative without already knowing the answer? If the context reads as a narrative of what was done rather than as a frame for the decision, the document is documentation but not reasoning — and a future reader will have to reconstruct the reasoning themselves.

#### Reference

[Y Statements (Zalando)](https://medium.com/olzzio/y-statements-10eb07b5a177) treats context articulation as a primary discipline, with the canonical "In the context of \[scope\], facing \[concern\], we decided for \[option\] and against \[alternatives\] to achieve \[quality\], accepting \[downside\]." [Building Evolutionary Architectures (Ford et al.)](https://www.oreilly.com/library/view/building-evolutionary-architectures/9781491986356/) covers context-driven architectural decision-making at framework level.

---

### 4. The decision states what was chosen in active voice and at sufficient specificity to be verifiable

A decision sentence that reads "X seems like the right approach" or "we should consider X" hasn't actually decided anything — it's still ruminating. A decision sentence that reads "We will use X" with sufficient specifics is a decision a future reader can verify against the system: did the team actually use X? Did they configure it as stated? The architectural discipline is *active voice and verifiable specificity*: "We will" / "We are adopting" / "We have chosen" rather than "It would be good to" / "The team should consider"; specifics that name the actual technology, the actual configuration, the actual scope ("for new microservices in the orders bounded context, effective on the next release") rather than gestures at intent ("we'll use modern messaging").

#### Architectural implications

- The decision section opens with an active-voice statement: "We will adopt X for Y, configured as Z, applying to scope W, effective from V."
- Specificity is calibrated to the decision's stakes: a decision about the database for one service can be more specific than a decision about a general technology direction; both should be specific enough to be verifiable.
- Effective dates and scope boundaries are explicit: "for new services" / "for services touching personal data" / "across the entire fleet by Q3" — so a future reader knows what was actually committed.
- Hedging language ("possibly", "consider", "evaluate", "perhaps") in the decision section is a signal that the decision wasn't actually made; the document should be in Proposed status rather than Accepted, or the decision should be sharpened.

#### Quick test

> Pick a recent Accepted ADR. Quote its decision sentence. Is it active voice? Is it specific enough that you could verify whether the system follows the decision? If the answer is "we decided to consider adopting X" or similar hedging, the document is not yet binding — and what's been recorded is a discussion, not a decision.

#### Reference

[Documenting Architecture Decisions (Nygard)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) treats the active-voice discipline as central to ADR practice. [Y Statements (Zalando)](https://medium.com/olzzio/y-statements-10eb07b5a177) makes the active-voice requirement explicit in its template grammar.

---

### 5. Consequences enumerate both intended outcomes and accepted trade-offs

A decision section that lists only the benefits is incomplete — it elides the costs the team accepted in making the choice. A consequences section that says only "this will improve performance" hides the trade-offs the future reader might inherit. The architectural discipline is to enumerate *both sides*: the *intended outcomes* the decision was made to produce (what becomes possible, what's fixed, what improves) AND the *accepted trade-offs* (what becomes harder, what alternatives were foreclosed, what risks were knowingly taken, what costs the team is paying for the chosen approach). Future readers benefit doubly: they see why the decision was good, and they see what it cost — which is the information they need to know whether the trade-offs the original team accepted still apply.

#### Architectural implications

- The consequences section is structured into Intended Outcomes (what the decision aims to achieve) and Accepted Trade-offs (what the decision costs).
- Trade-offs are explicit and named, not euphemistic: "we are accepting eventual consistency at this boundary; reads-after-writes from outside the bounded context may return stale data for up to 5 seconds" rather than "some operational complexity."
- Risks knowingly taken are acknowledged: "This couples our roadmap to Vendor X's release cycle" / "This requires the team to develop expertise we don't currently have, with a 6-month ramp."
- Forecasted operational implications are noted: monitoring requirements, runbook updates, on-call training implications, cost-envelope changes.

#### Quick test

> Pick a recent ADR. Are the consequences both-sided — intended benefits AND accepted trade-offs — or only the benefits? If only the benefits are listed, the document is selling the decision rather than recording it. The next time the team revisits this ADR (because something the trade-offs implied has now become a problem), the trade-offs will have to be reconstructed from memory.

#### Reference

[Y Statements (Zalando)](https://medium.com/olzzio/y-statements-10eb07b5a177) explicitly requires both-sided consequence statements ("achieving \[quality\], accepting \[downside\]") in its grammar. [Building Evolutionary Architectures (Ford et al.)](https://www.oreilly.com/library/view/building-evolutionary-architectures/9781491986356/) treats trade-off acknowledgement as central to architectural discipline.

---

### 6. References anchor the decision in evidence — alternatives evaluated, prototypes built, research consulted

A decision presented without supporting references is a decision presented as opinion. A decision anchored in references — links to the alternatives that were evaluated, the prototype results that informed the choice, the research papers or vendor documentation consulted, the prior ADRs whose decisions this builds on — is a decision presented as the conclusion of an investigation. The architectural discipline is *reference anchoring*: every ADR ends with explicit links to (a) the alternatives that were considered (with brief notes on why each was rejected); (b) any prototyping or benchmarking results that informed the choice; (c) the canonical sources for the chosen approach (vendor docs, research papers, established practice references); (d) related prior ADRs and the cross-references between them. The references make the ADR's reasoning *checkable* — a future reader can re-examine the evidence and decide whether the original conclusion still holds.

#### Architectural implications

- The references section lists alternatives considered with one-line summaries of why each was rejected — not just "we considered X, Y, Z" but "X (rejected: doesn't support Q), Y (rejected: violates constraint R), Z (rejected: too expensive)."
- Prototyping results are linked: the spike branch, the benchmark spreadsheet, the proof-of-concept repository — so the empirical evidence that informed the decision is recoverable.
- Canonical sources for the chosen approach are linked: vendor documentation, research papers, established-practice references (e.g., the relevant pages of [Building Evolutionary Architectures (Ford et al.)](https://www.oreilly.com/library/view/building-evolutionary-architectures/9781491986356/)).
- Related prior ADRs are cross-referenced bidirectionally: this ADR builds on / supersedes / depends on / contradicts other ADRs; those other ADRs are updated to point back to this one.

#### Quick test

> Pick a recent ADR. Does its references section list the alternatives considered (with rejection reasons), prototyping results, canonical sources, and related ADRs? If references are sparse or absent, the decision is presented without its supporting evidence — and a future reader has to take the chosen conclusion on the original team's authority rather than examining the evidence themselves.

#### Reference

[ADR Examples (joelparkerhenderson)](https://github.com/joelparkerhenderson/architecture-decision-record) is a curated collection of ADR examples; reference-anchoring discipline varies across them, with the highest-quality examples following the discipline above. [Diátaxis Documentation Framework](https://diataxis.fr/) provides the broader documentation philosophy that underpins reference-anchoring (technical documents are checkable artefacts, not authoritative pronouncements).

---

## ADR Lifecycle States

The diagram below shows the canonical ADR lifecycle as a state machine: a Proposed ADR is under review and not yet binding; transitions to Accepted when the team commits to the decision; may transition to Deprecated when the team no longer prefers the approach but no replacement is identified; transitions to Superseded by a specific newer ADR when a replacement is chosen. Each transition records date and reason; the document accumulates its own history.

---

## Common pitfalls when adopting ADR-template thinking

### ⚠️ Vague titles that don't disambiguate

Titles like "Caching" or "Database choice" tell future readers nothing about what was decided. Searching the corpus produces ambiguous results; opening each ADR to find the right one is the only way.

#### What to do instead

Verb-phrased decisions, specific to the subsystem, with distinguishing detail. The title alone should be sufficient to determine if this is the ADR the reader needs.

---

### ⚠️ No status field — current/historical/superseded indistinguishable

A reader encounters an old ADR. Is it still binding? Was it replaced? Was the decision quietly walked back? The document doesn't say.

#### What to do instead

Status as a primary field with a documented vocabulary (Proposed / Accepted / Deprecated / Superseded). Lifecycle transitions recorded with date and reason. Bidirectional cross-references between superseded and superseding ADRs.

---

### ⚠️ Missing context — the decision looks arbitrary

The ADR records what was decided but not why the decision was needed. Future readers second-guess the choice because the considerations that ruled out alternatives aren't visible.

#### What to do instead

Context section captures requirements, constraints, current state, and the trade-off space of alternatives. The decision is intelligible to a reader who wasn't in the original discussion.

---

### ⚠️ Hedging decision sentences that don't actually decide

"It would be good to use X" / "We should consider X" / "The team is evaluating X." The decision section reads like discussion, not commitment. The status says Accepted, but nothing was actually decided.

#### What to do instead

Active voice and verifiable specificity. "We will use X with configuration Y, applying to scope Z, effective from V." If hedging language is necessary, the ADR should be in Proposed status, not Accepted.

---

### ⚠️ One-sided consequences — only the benefits

The consequences section lists what the decision will achieve. The trade-offs the team accepted aren't documented. When the trade-offs surface later as problems, the team has to reconstruct what was knowingly accepted versus what was overlooked.

#### What to do instead

Two-sided consequences: Intended Outcomes and Accepted Trade-offs. Trade-offs explicit and named; risks knowingly taken acknowledged; operational implications forecasted.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Titles are verb-phrased decisions specific enough to disambiguate the ADR from others ‖ "Adopt X with Y for Z" rather than "X" or "Database choice." A reader can determine from the title alone whether this is the ADR they need. | ☐ |
| 2 | Status is a primary field at the top of the document, drawn from a documented vocabulary ‖ Proposed / Accepted / Deprecated / Superseded by ADR-NNN. Status is visible immediately, not buried in metadata. | ☐ |
| 3 | Lifecycle transitions are recorded with date and reason, accumulated in the document over time ‖ Each status change appends to the document's history. The ADR's full lifecycle is visible without external state. | ☐ |
| 4 | Superseded and superseding ADRs cross-reference bidirectionally ‖ Superseded ADRs link forward to their successors; successors link back to what they replaced. The corpus is navigable by following these links. | ☐ |
| 5 | Context articulates requirements, constraints, current state, and the trade-off space of alternatives ‖ A reader who wasn't in the original discussion can understand why the decision was needed and what considerations applied. | ☐ |
| 6 | Decision section uses active voice and verifiable specificity ‖ "We will adopt X with Y, applying to Z, effective from V." Specifics are calibrated to the decision's stakes. Hedging language signals the decision isn't yet made. | ☐ |
| 7 | Consequences are two-sided — Intended Outcomes and Accepted Trade-offs ‖ Trade-offs explicit and named, not euphemistic. Risks knowingly taken acknowledged. Operational implications forecasted. | ☐ |
| 8 | References list alternatives considered with rejection reasons ‖ Not "we considered X, Y, Z" but per-alternative rejection rationale. Future readers can re-examine why alternatives were ruled out. | ☐ |
| 9 | References anchor the decision in evidence — prototyping results, canonical sources, related ADRs ‖ Spike branches, benchmark results, vendor documentation, research papers. The decision's evidence base is recoverable. | ☐ |
| 10 | The ADR template is a documented standard the team uses for all decisions, not a once-off format ‖ The template is itself an ADR or governance artefact. New ADRs follow the same structure. The corpus is consistent across time and authors. | ☐ |

---

## Related

[`templates/review-template`](../review-template) | [`templates/scorecard-template`](../scorecard-template) | [`governance/ownership`](../../governance/ownership) | [`governance/review-templates`](../../governance/review-templates) | [`patterns/event-driven`](../../patterns/event-driven)

---

## References

1. [Documenting Architecture Decisions (Nygard)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — *cognitect.com*
2. [MADR — Markdown ADRs](https://adr.github.io/madr/) — *adr.github.io*
3. [ADR Tools (npryce)](https://github.com/npryce/adr-tools) — *github.com*
4. [ADR Examples (joelparkerhenderson)](https://github.com/joelparkerhenderson/architecture-decision-record) — *github.com*
5. [Y Statements (Zalando)](https://medium.com/olzzio/y-statements-10eb07b5a177) — *medium.com*
6. [ADR — Spotify Engineering](https://engineering.atspotify.com/2020/04/when-should-i-write-an-architecture-decision-record/) — *engineering.atspotify.com*
7. [ADR Manager — adr.github.io](https://adr.github.io/) — *adr.github.io*
8. [Building Evolutionary Architectures (Ford et al.)](https://www.oreilly.com/library/view/building-evolutionary-architectures/9781491986356/) — *oreilly.com*
9. [ThoughtWorks Tech Radar](https://www.thoughtworks.com/radar) — *thoughtworks.com*
10. [Diátaxis Documentation Framework](https://diataxis.fr/) — *diataxis.fr*
