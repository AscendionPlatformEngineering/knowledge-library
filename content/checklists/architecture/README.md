# Architecture Review Checklist

The artefact a reviewer applies to evaluate whether a proposed architecture meets the system's actual non-functional requirements — recognising that architecture review is the moment when capacity, latency, security, resilience, observability, and operability concerns either get surfaced and addressed or get inherited as production problems by future operators.

**Section:** `checklists/` | **Subsection:** `architecture/`
**Alignment:** ATAM (SEI) | AWS Well-Architected Framework | Software Architecture in Practice (Bass et al.) | Release It! (Nygard)

---

## What "architecture review checklist" means — and how it differs from "governance checklists"

This page is about the architecture review checklist as a designed artefact — the specific instrument a reviewer applies during an architecture review to evaluate a proposed design across non-functional dimensions. The discipline of *how checklists work as governance instruments* — their authoring, calibration, retirement, ownership — lives in [`governance/checklists`](../../governance/checklists). That page covers checklists generally as part of governance machinery. This page covers one specific checklist in depth: what dimensions it must cover, what makes its items effective, how to calibrate it against the production failures the team has experienced, and how to apply it without reducing review to ceremonial box-ticking.

A *primitive* architecture review uses no checklist. The reviewer relies on intuition, experience, and whatever they happened to remember to ask about. Reviews that catch the things the reviewer has personally learned to ask about; miss the things the reviewer hasn't encountered before. Different reviewers produce different findings on the same design. The same reviewer produces different findings on different days. The discipline runs on individual judgment, varies with who's available, and is impossible to improve systematically because there's no instrument to refine.

A *production* architecture review checklist is a designed artefact with structural properties. It covers the non-functional dimensions that matter for the system's class — capacity, latency, security, resilience, observability, operability, cost, evolvability — explicitly, with items that surface specific concerns within each dimension. Items are *organised by class of concern* (the request-response architecture has different items than the event-driven one), *tier-aware* (a low-stakes prototype gets a lightweight pass; a payment system gets the full instrument), *calibrated by experience* (items added when production incidents reveal what prior reviews missed), and *integrated with the tooling* the team already uses (the checklist surfaces in the design-document template, the architecture decision record format, the review meeting agenda). The checklist becomes the institutional memory of what to look for during review — applied consistently across reviewers, refined continuously through use.

The architectural shift is not "we have a checklist." It is: **the architecture review checklist is a designed coverage instrument whose dimensions, organisation, tier-awareness, and calibration loop determine whether reviews surface the concerns that future operators will face — and treating the checklist as a static document or as ceremonial box-ticking produces reviews whose value is bounded by the reviewer's individual memory.**

---

## Six principles

### 1. Multi-dimensional coverage — the checklist is comprehensive across the non-functional concerns that determine system viability

The most consequential property of an architecture review checklist is the *dimensions it covers*. A checklist that covers only functional correctness ("does the design solve the problem?") misses everything that determines whether the system survives production: it may solve the problem at small scale but fail at peak; it may meet the latency requirement at P50 but not at P99; it may handle the happy path but not the adversarial one. The architectural discipline is to enumerate the non-functional dimensions that matter for the system's class — *capacity* (will it handle the load?), *latency* (will it meet response-time requirements at the tail?), *security* (does it defend against the threats the system actually faces?), *resilience* (what happens when its dependencies fail?), *observability* (will operators be able to diagnose problems in production?), *operability* (can the system be deployed, configured, scaled, recovered without specialist knowledge?), *cost* (is the operational cost sustainable for the value delivered?), *evolvability* (can the design be modified as requirements change without the modifications becoming the new bottleneck?) — and to have items in the checklist that surface concerns within each. Missing dimensions don't disappear; they reappear in production as incidents the review didn't catch.

#### Architectural implications

- The checklist is structured around documented non-functional dimensions: capacity, latency, security, resilience, observability, operability, cost, evolvability — at minimum.
- Each dimension has multiple items that surface specific concerns: under capacity, items address peak vs steady-state load, growth trajectory, scaling-mechanism limits, resource saturation thresholds.
- Items are written to provoke specific answers, not to prompt general affirmation: "what's the P99 latency at peak load given the design's caching strategy?" rather than "is performance considered?"
- The dimensional coverage is reviewed periodically — new dimensions added as new classes of system enter the portfolio (e.g. AI/ML systems may need *training-data lineage* and *inference cost predictability* as additional dimensions).

#### Quick test

> Pick the most recent architecture review in your organisation. List the non-functional dimensions the checklist explicitly covered. Did capacity have items distinct from latency? Did resilience cover failure modes of dependencies, not just of the system itself? Did observability ask what operators would do to diagnose a specific class of failure? If any dimension was implicit, the review's coverage was implicit too — and the gaps will surface in production.

#### Reference

[ATAM — SEI](https://www.sei.cmu.edu/our-work/projects/display.cfm?customel_datapageid_4050=21859) is the canonical architecture-evaluation method, with multi-dimensional coverage as its central organising principle. [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) operationalises a six-pillar dimensional model (operational excellence, security, reliability, performance efficiency, cost optimization, sustainability) that's directly applicable to checklist design across cloud and non-cloud architectures.

---

### 2. Items by class of concern — request-response, event-driven, and ML systems each need their own dimensions

A single uniform checklist applied to every architecture catches the dimensions that matter for some classes and misses the dimensions that matter for others. A request-response system needs items about latency at P99, retry behaviour, idempotency of mutating operations, circuit-breaker configuration. An event-driven system needs items about message ordering guarantees, exactly-once vs at-least-once semantics, dead-letter handling, consumer-lag thresholds. An ML system needs items about training-data lineage, inference cost predictability, model-drift detection, fallback behaviour when predictions are unavailable. The architectural discipline is to recognise that the dimensions that matter depend on the system's class, and to provide *per-class items* — either as separate checklist sections, separate checklists per class, or a base checklist with class-specific extension items. Forcing all systems through the same items either over-burdens simple ones with irrelevant questions or under-serves complex ones with shallow coverage.

#### Architectural implications

- The checklist is organised by class of concern with shared items (those applicable to all systems) and class-specific items (those applicable only to specific classes).
- The classes are documented: request-response, event-driven, batch processing, streaming, ML inference, ML training, edge/IoT, etc. — with criteria for assigning a system to a class (a system can be in multiple classes).
- The class-specific items are authored by people with operational experience of the class — the items reflect what actually goes wrong in production for that class, not generic concerns.
- New classes are added as the portfolio evolves; class-specific items are revised as operational experience accumulates.

#### Quick test

> Pick three systems in your portfolio with different classes (request-response API, event-stream processor, ML inference service). Do they all use the same checklist with the same items, or do they use class-specific extensions? If the same checklist is applied uniformly, the simpler systems are over-burdened and the complex ones are under-served — and the dimensions specific to each class are catching less than they could.

#### Reference

[Software Architecture in Practice — Bass et al.](https://www.oreilly.com/library/view/software-architecture-in/9780136885979/) treats architecture quality attributes as varying by system class, with the implication that evaluation methods (and checklists) need class-specific dimensions. [Production-Ready Microservices — Fowler](https://www.oreilly.com/library/view/production-ready-microservices/9781491965962/) provides a class-specific checklist for microservice architecture; the framing transfers to per-class checklist design generally.

---

### 3. Tier-aware depth — different stakes deserve different review depths

Applying the full architecture review checklist to a low-stakes prototype is over-burden — the prototype's reviewer spends hours on items that don't apply, the prototype's author resents the friction, and the checklist becomes a target for evasion rather than for use. Applying a lightweight checklist to a payment-processing system is under-coverage — the system that can't afford to fail gets the same review depth as the system that can. The architectural discipline is *tier-aware depth*: the checklist has documented tiers (typically 3-4: low-stakes, medium-stakes, high-stakes, critical) with explicit criteria for tier assignment, and each tier has documented expected coverage (which items are required, which are optional, which are skipped). High-stakes systems get the comprehensive instrument; low-stakes systems get the focused subset that catches the concerns that matter at that scale. Tier assignment is itself a decision documented in the review, not assumed.

#### Architectural implications

- The checklist defines tiers (low-stakes, medium-stakes, high-stakes, critical or equivalent) with documented criteria — typically based on user impact, revenue impact, regulatory exposure, blast radius of failure.
- Each tier has documented expected coverage: which items are required at each tier, which are skipped, which are optional with reviewer discretion.
- Tier assignment for each review is documented at the start: "this design is being reviewed at tier 3 (high-stakes) because it touches the payment flow and a failure has direct customer impact."
- Tier changes mid-review are possible but documented: a review that started at tier 2 and discovered the design has more risk than initially thought escalates to tier 3 and applies the corresponding additional items.

#### Quick test

> Pick the last five architecture reviews in your organisation. Were their tiers documented at the start, and did the items applied match the tier? If all five reviews used the same depth regardless of stakes, the checklist isn't tier-aware — and either over-burdens the simple cases, under-serves the complex ones, or both.

#### Reference

[AWS Well-Architected Framework — Lens Concept](https://docs.aws.amazon.com/wellarchitected/latest/userguide/lenses.html) operationalises a similar tier-and-class-aware approach, where different lenses apply different depths to different system classes. The conceptual framing of tier-aware review depth is treated in [Software Architecture in Practice — Bass et al.](https://www.oreilly.com/library/view/software-architecture-in/9780136885979/) as part of evaluation-method scaling.

---

### 4. Items are calibrated by production experience — what was missed becomes the next item

A checklist authored once and never revised becomes increasingly disconnected from the production reality it's supposed to surface concerns about. Systems evolve; failure modes change; new classes of incident emerge that the checklist's authors didn't anticipate. The architectural discipline is to treat the checklist as a *living artefact calibrated by production experience*: every production incident — particularly those that surfaced concerns the architecture review *should have* caught — produces a candidate revision to the checklist. The post-incident review asks "would the existing checklist have surfaced this concern?" If yes, the review process failed to apply it; if no, the checklist itself failed to cover this dimension and an item gets added. Over time, the checklist accumulates the institutional learning of what production has taught the team to look for — and the team's reviews get incrementally better at catching what they previously missed.

#### Architectural implications

- Every production incident's post-mortem includes the question "would the architecture review checklist have surfaced this concern?"
- Findings produce a queue of candidate checklist revisions, prioritised by frequency of similar incidents and severity.
- Revisions are versioned and reviewed — the change is documented (what's added, why, which incident motivated it), and reviewed by someone other than the author before merging.
- Periodic checklist review (typically quarterly) examines items that *haven't* been triggered in a long time — they may still be valuable (catching infrequent but important concerns), or may be obsolete (catching concerns that no longer apply to the current portfolio).

#### Quick test

> Pick the most consequential production incident in your organisation in the last year. Was a candidate checklist revision proposed as part of its post-mortem? If yes, was it incorporated? If the answer is "we discussed it but didn't update the checklist," the calibration loop is broken — and the next incident in the same class will surface the same gap that the existing review didn't catch.

#### Reference

[Etsy — How to Conduct a Postmortem (Allspaw)](https://www.etsy.com/codeascraft/blameless-postmortems) treats post-incident learning generally; the same discipline applied to checklist calibration produces continuously-improving review instruments. [The Checklist Manifesto — Atul Gawande](https://atulgawande.com/book/the-checklist-manifesto/) covers the calibration-through-use principle for high-stakes checklists in domains where missed items have catastrophic consequences.

---

### 5. Items provoke specific answers, not generic affirmation — the difference between coverage and box-ticking

An item that reads "is observability addressed?" produces a yes from any reviewer willing to wave through any answer. An item that reads "what's the runbook URL for the alert that fires when the queue depth exceeds threshold X, and has the runbook been exercised?" produces either a specific answer (with concrete URL and exercise date) or a documented gap. The difference is whether the item *provokes coverage* or *prompts ceremonial affirmation*. The architectural discipline is to write items that demand specific, evidence-bearing answers — "what's the P99 latency under peak load?" not "is performance considered?"; "what's the on-call runbook for this alert?" not "is the system observable?"; "what's the rollback path and when was it last exercised?" not "is rollback addressed?" Items that can be passed by handwaving leave the same gaps that having no checklist leaves; items that demand specifics produce coverage that's actually visible.

#### Architectural implications

- Items are written to demand specific evidence — concrete numbers, URLs, dates, names — rather than affirmation of consideration.
- The reviewer's role is to evaluate whether the answer is satisfactory, not to confirm that an answer was given.
- Items that consistently get handwave answers are flagged for revision — either the item is too vague (rewrite for specifics) or the reviewers aren't applying it rigorously (training/process issue).
- The "specific answer" expectation is documented in the checklist's introduction, so authors know what's expected and reviewers know what to demand.

#### Quick test

> Pick five items from your architecture review checklist. For each, what's the typical answer? If the answers are mostly "yes" or "considered," the items are prompting affirmation rather than coverage. If the answers are concrete (numbers, URLs, names, dates), the items are doing the work the checklist exists to do.

#### Reference

[The Checklist Manifesto — Atul Gawande](https://atulgawande.com/book/the-checklist-manifesto/) treats the read-do (read each step, then act) versus do-confirm (act, then verify) distinction; specific-answer items are read-do checklists where the "do" is producing the evidence, not just confirming consideration. [Code Review Best Practices — Google](https://google.github.io/eng-practices/review/) covers the same principle for code review specifically — the distinction between approval-as-courtesy and approval-as-evaluation.

---

### 6. Discoverability and tooling integration — the checklist surfaces where designs are reviewed

A checklist stored on a wiki that nobody opens during reviews is operationally equivalent to no checklist. Discoverability is the architectural property that determines whether the careful authoring work pays off in practice. The discipline has several layers. *Design-document template integration* — the architecture decision record (ADR) or design-document template includes the checklist as a section, so authors confront the items as they write the design rather than discovering them in review. *Review-tooling integration* — the checklist surfaces in the review meeting agenda, the pull request template, the design-review ticket, wherever review happens — so reviewers don't have to look up the checklist separately. *Outcome tracking* — the checklist's items are tracked across reviews, so missed items, common gaps, and item-level effectiveness are visible to the team that owns the checklist. The discipline is to recognise that the checklist isn't a document — it's an integrated tool embedded in the review workflow, surfacing where designs are evaluated and tracking what the reviews actually catch.

#### Architectural implications

- Design-document and ADR templates include the checklist as a section the author fills in, with each item answered explicitly — not appended at review time.
- Review-tooling surfaces the checklist as part of the review workflow: the PR template, the design-review ticket, the meeting agenda — wherever review happens.
- Item-level outcomes are tracked: which items found gaps, which items were waived, which items were applied without producing findings — over time, across reviews.
- Stable discovery paths: the checklist URL doesn't change with reorganisation; broken links are treated as regressions, not normal decay.

#### Quick test

> Pick the most-trafficked design-review surface in your organisation (PR template, design ticket, ADR). Does the architecture review checklist surface there as part of the workflow, or do reviewers need to look it up separately? If separately, the checklist's adoption is gated on reviewer initiative — and the reviews that don't reference it produce coverage that doesn't include what the checklist exists to catch.

#### Reference

[Pull Request Review Patterns — Martin Fowler](https://martinfowler.com/articles/ship-show-ask.html) covers the integration of review instruments into the workflow; the same architectural discipline applies to checklists generally. [Code Review Best Practices — Google](https://google.github.io/eng-practices/review/) operationalises the "checklist embedded in workflow" pattern at practitioner depth.

---

## Architecture Diagram

The diagram below shows the canonical architecture-review-checklist architecture: dimensional coverage organised by non-functional concern (capacity, latency, security, resilience, observability, operability, cost, evolvability); class-specific item extensions for different system types; tier-aware depth with documented criteria; calibration loop where production incidents produce candidate revisions; tooling integration surfacing the checklist in design templates and review workflows; outcome tracking that informs the calibration loop.

---

## Common pitfalls when adopting architecture-review-checklist thinking

### ⚠️ Generic items prompting affirmation

Items read "is performance considered?" Every review produces a "yes." The checklist's coverage is theatrical; the actual concerns are missed at the same rate as having no checklist.

#### What to do instead

Items written to demand specific evidence — concrete numbers, URLs, dates, names. The reviewer's role is to evaluate whether the answer is satisfactory, not to confirm an answer was given. Items that consistently get handwave answers are flagged for revision.

---

### ⚠️ One-size-fits-all checklist

Same items for every system, regardless of class. Request-response items applied to ML systems; ML items applied to batch jobs. Either the simple systems are over-burdened or the complex ones are under-served.

#### What to do instead

Items by class of concern. Shared items applicable to all systems; class-specific items for request-response, event-driven, ML inference, etc. Class assignment is documented per review.

---

### ⚠️ Same depth regardless of stakes

The full checklist is applied to every review, including low-stakes prototypes. Or a lightweight subset is applied to every review, including critical systems.

#### What to do instead

Tier-aware depth. Documented tiers with criteria; each tier has documented expected coverage. Tier assignment per review documented. High-stakes get the full instrument; low-stakes get the focused subset.

---

### ⚠️ Static checklist disconnected from production experience

The checklist was authored two years ago. Three production incidents since then surfaced concerns that the checklist would have been able to catch — if it had had the relevant items. The items never got added.

#### What to do instead

Calibration loop. Every post-mortem asks "would the checklist have caught this?" Findings feed candidate revisions. Versioned, reviewed updates. The checklist accumulates institutional learning continuously.

---

### ⚠️ Checklist on a wiki nobody opens

The checklist exists. It lives on a wiki. Reviewers don't navigate to it during reviews. The careful authoring work pays zero dividends.

#### What to do instead

Tooling integration. Checklist embedded in design-document templates, PR templates, review tickets, meeting agendas. Stable URLs. Item-level outcome tracking visible to the team that owns the checklist.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | The checklist covers documented non-functional dimensions — capacity, latency, security, resilience, observability, operability, cost, evolvability — at minimum ‖ Multi-dimensional coverage. Each dimension has multiple items surfacing specific concerns. Missing dimensions reappear as production incidents. | ☐ |
| 2 | Items are written to demand specific evidence — concrete numbers, URLs, dates, names — not generic affirmation ‖ The difference between coverage and box-ticking. Items that demand specifics produce visible coverage; items that prompt affirmation leave the same gaps that having no checklist leaves. | ☐ |
| 3 | Items are organised by class of concern — shared base items plus class-specific extensions ‖ Request-response systems have items distinct from event-driven systems and ML systems. Class assignment per review is documented. Class-specific items reflect operational experience of the class. | ☐ |
| 4 | The checklist defines tiers with documented criteria for tier assignment ‖ Low-stakes, medium-stakes, high-stakes, critical (or equivalent). Criteria based on user impact, revenue impact, regulatory exposure, blast radius. Each tier has documented expected coverage. | ☐ |
| 5 | Tier assignment for each review is documented at the start ‖ "This design is being reviewed at tier 3 because..." Tier changes mid-review are documented. The review's depth matches the system's stakes. | ☐ |
| 6 | Every post-mortem asks "would the checklist have caught this concern?" ‖ Calibration loop. Findings feed candidate revisions to a queue. Revisions versioned, reviewed, and merged. The checklist accumulates institutional learning over time. | ☐ |
| 7 | Periodic checklist review examines items that haven't been triggered ‖ Items still valuable (catching infrequent but important concerns) versus obsolete (no longer applicable). The checklist stays focused on what's relevant. | ☐ |
| 8 | The checklist is integrated with design-document templates and ADR formats ‖ Authors confront items as they write the design, not as they receive review feedback. The checklist becomes part of design authoring, not just review evaluation. | ☐ |
| 9 | The checklist surfaces in review tooling — PR templates, review tickets, meeting agendas ‖ Reviewers don't look up the checklist separately. The instrument is embedded in the workflow where review happens. | ☐ |
| 10 | Item-level outcomes are tracked across reviews ‖ Which items found gaps, which were waived, which were applied without findings. The team that owns the checklist sees its operational effectiveness over time and refines accordingly. | ☐ |

---

## Related

[`checklists/deployment`](../deployment) | [`checklists/security`](../security) | [`governance/checklists`](../../governance/checklists) | [`governance/review-templates`](../../governance/review-templates) | [`patterns/structural`](../../patterns/structural) | [`system-design/scalable`](../../system-design/scalable)

---

## References

1. [ATAM (Architecture Tradeoff Analysis Method)](https://www.sei.cmu.edu/our-work/projects/display.cfm?customel_datapageid_4050=21859) — *sei.cmu.edu*
2. [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) — *aws.amazon.com*
3. [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/) — *learn.microsoft.com*
4. [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework) — *cloud.google.com*
5. [Software Architecture in Practice (Bass et al.)](https://www.oreilly.com/library/view/software-architecture-in/9780136885979/) — *oreilly.com*
6. [Production-Ready Microservices (Fowler)](https://www.oreilly.com/library/view/production-ready-microservices/9781491965962/) — *oreilly.com*
7. [Release It! (Nygard)](https://pragprog.com/titles/mnee2/release-it-second-edition/) — *pragprog.com*
8. [The Checklist Manifesto — Atul Gawande](https://atulgawande.com/book/the-checklist-manifesto/) — *atulgawande.com*
9. [Code Review Best Practices (Google)](https://google.github.io/eng-practices/review/) — *google.github.io*
10. [Pull Request Review Patterns](https://martinfowler.com/articles/ship-show-ask.html) — *martinfowler.com*
