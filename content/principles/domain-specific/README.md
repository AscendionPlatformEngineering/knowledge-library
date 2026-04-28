# Domain-Specific Principles

Architecture for systems where the business domain — its language, rules, and constraints — is treated as a first-class engineering input, not as a backlog of requirements.

**Section:** `principles/` | **Subsection:** `domain-specific/`
**Alignment:** Domain-Driven Design | Conway's Law | TOGAF ADM | BIAN

---

## What "domain-specific" actually means

A *domain-agnostic* system applies generic architectural patterns regardless of business context: REST endpoints over a database, microservices split by technical layer, a "Users" table that captures every actor across every workflow. The patterns work — but they could be deployed to a logistics company, a hospital, or a music streamer with only superficial change. The architecture has no opinion about what the business actually does.

A *domain-specific* system internalises the language, rules, and constraints of the business it serves. Service boundaries match business capabilities. The vocabulary domain experts use appears unchanged in code, schemas, and contracts. Regulatory constraints (HIPAA, PCI-DSS, Basel III, GDPR) are architecturally visible — not buried in implementation. Industry reference models (BIAN for banking, HL7 FHIR for healthcare, ACORD for insurance, eTOM for telco, ISA-95 for manufacturing) inform — but don't dictate — the design.

The architectural shift is not "we modelled the database to match the business." It is: **the way we partition, name, and integrate systems is a direct expression of how the business actually works — and changes when the business does.**

---

## Six principles

### 1. Bounded contexts mirror business capabilities, not technical layers

Partition the system along business capability boundaries. Each bounded context owns its data, language, rules, and lifecycle. Horizontal slicing — UI, service, data — as the primary axis of decomposition produces shared databases, distributed monoliths, and Conway's-Law mismatches between teams and architecture.

#### Architectural implications

- The service catalogue reads like the business capability map, not the technology org chart.
- Each context owns its persistent state — no shared "master" databases across context boundaries.
- Cross-context integration is explicit (events, well-defined APIs), never via shared schemas.
- Context boundaries are versioned and stable; changes within a context don't require coordination across contexts.

#### Quick test

> Could a new product manager open your service catalogue and recognise the business areas they're responsible for? Or do they need an org chart and a translation guide?

#### Reference

Eric Evans introduced bounded contexts in *Domain-Driven Design* (2003). Vaughn Vernon's *Implementing Domain-Driven Design* (2013) operationalises them. Martin Fowler's [BoundedContext summary](https://martinfowler.com/bliki/BoundedContext.html) captures the essence in a few hundred words.

---

### 2. Ubiquitous language is enforced in code, contracts, and conversation

The vocabulary domain experts use must appear unchanged in class names, API contracts, database schemas, and team conversations. When code says "Order" and the domain expert says "Booking" with subtly different semantics, bugs accumulate in the gap — slowly at first, then in clusters, then as production incidents.

#### Architectural implications

- API resource names match domain terms, not engineering shorthand.
- Database column names match domain terms, including case and pluralisation where the business uses them.
- ADRs and design docs use the same vocabulary as customer-facing documentation and support tickets.
- Translation layers between "business words" and "engineering words" are a smell — eliminate or formalise as anti-corruption layers (see Principle 6).

#### Quick test

> Pick a random domain term used in your last sprint review. Does it have the same definition in a board meeting, a support ticket, and the codebase?

#### Reference

*Domain-Driven Design* (Evans 2003), Chapter 2 — "Communication and the Use of Language". Sam Newman's *Building Microservices*, 2nd edition (2021), treats ubiquitous language as a precondition for service decomposition.

---

### 3. Industry reference models are accelerators, not constraints

Mature domains have decades-old reference architectures: [BIAN](https://bian.org/) for banking, [HL7 FHIR](https://hl7.org/fhir/) for healthcare, [ACORD](https://www.acord.org/standards-architecture/reference-architecture) for insurance, [TM Forum eTOM](https://www.tmforum.org/oda/) for telco, [ISA-95](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95) for manufacturing. They encode learning that no single organisation could replicate. Use them as starting points; differentiate where business strategy demands it.

#### Architectural implications

- Map your APIs to the relevant reference model where one exists; document deviations explicitly with rationale.
- Don't reinvent baseline service domains the industry has already standardised (customer onboarding, claims processing, order management).
- Treat reference-model alignment as a non-functional requirement when it enables ecosystem integration (open banking, interoperable health records, regulatory reporting).
- Where strategy demands divergence, document why — future engineers and auditors need the rationale.

#### Quick test

> Can you identify which BIAN service domains (or FHIR resources, or ACORD entities) your APIs correspond to? If "none of the above," either your domain is genuinely novel or you're quietly reinventing wheels.

#### Reference

[BIAN Service Landscape](https://bian.org/servicelandscape/) (banking). [HL7 FHIR R5](https://hl7.org/fhir/) (healthcare). [ACORD Reference Architecture](https://www.acord.org/standards-architecture/reference-architecture) (insurance). [TM Forum Open Digital Architecture](https://www.tmforum.org/oda/) (telco).

---

### 4. Regulatory boundaries are architectural boundaries

Domain regulations — data residency, consent, retention, audit trails, encryption-at-rest — define hard architectural constraints. They should be visible in the design, not buried three layers deep in implementation. A compliance officer should be able to trace a regulatory requirement to specific architectural decisions without reading source code.

#### Architectural implications

- Data classification (PII, PHI, PCI, public, internal) is a first-class system attribute, surfaced in service contracts and runtime metadata.
- Data residency is modelled, not assumed. Cross-region flows are explicit and review-gated.
- Audit logging is part of the architecture, not an afterthought patched on by SecOps.
- Consent state is an authoritative domain entity, not a column in a marketing table.

#### Quick test

> Can a compliance officer trace a single regulatory requirement (e.g., "EU PII must not leave the EU") to a specific component, control, and code path in your system in under five minutes?

#### Reference

[GDPR Article 25](https://gdpr-info.eu/art-25-gdpr/) — Data Protection by Design and by Default. [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework). [ISO/IEC 27001](https://en.wikipedia.org/wiki/ISO/IEC_27001).

---

### 5. Domain events are the durable contract between contexts

Cross-context integration through immutable domain events (`OrderPlaced`, `ClaimSubmitted`, `PolicyIssued`, `PaymentSettled`) decouples systems temporally, becomes the historical record, and survives system rewrites. Synchronous calls and shared databases couple contexts in ways that resist evolution and concentrate failure.

#### Architectural implications

- Inter-context communication defaults to events; synchronous calls are the documented exception, not the rule.
- Events are versioned and backward-compatible (additive changes; breaking changes require new event types).
- The event log is treated as a durable architectural asset — retained beyond any single producer or consumer's lifetime.
- Schema evolution and consumer compatibility are explicit governance concerns, not left to "be careful."

#### Quick test

> If you removed a downstream consumer of a service, would the upstream system care or even notice? If yes, you're using calls where you should be using events.

#### Reference

Martin Kleppmann, *[Designing Data-Intensive Applications](https://dataintensive.net/)* (O'Reilly, 2017) — particularly Chapters 11 (Stream Processing) and 12 (The Future of Data Systems). Vaughn Vernon, *Implementing Domain-Driven Design* (2013), Chapter 8 on Domain Events. [Confluent's Event-Driven Architecture course](https://developer.confluent.io/courses/event-driven-architecture/intro/).

---

### 6. Anti-corruption layers protect domain integrity at boundaries

When integrating with legacy systems, vendor APIs, or contexts using different language and models, an anti-corruption layer (ACL) translates external concepts into yours. Without an ACL, foreign concepts leak into the domain core, weakening its coherence over time and embedding vendor specifics into business logic.

#### Architectural implications

- Every external system integration has an explicit translation layer; no direct vendor-model imports into domain logic.
- ACL changes are localised — when a vendor changes their schema, the blast radius is one component.
- The ACL is an architectural artifact owned by the domain team, not the integration team.
- Internal domain concepts never appear in vendor-shaped form (and vice versa) outside the ACL boundary.

#### Quick test

> When a third-party vendor changes their data model, how many files in your codebase need updating? If the answer is more than the ACL's translation surface, the ACL is incomplete or being bypassed.

#### Reference

*Domain-Driven Design* (Evans 2003), Chapter 14 — Strategic Design. [Microsoft Cloud Design Patterns — Anti-Corruption Layer](https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer).

---

## Architecture Diagram

The diagram below shows a domain-specific system organised around DDD strategic design — a strategic core with supporting and generic subdomains, integrated via an event backbone, and protected from external systems by anti-corruption layers.

---

## Common pitfalls when adopting domain-specific thinking

### ⚠️ The CRUD trap

Treating the domain as a thin CRUD layer over a database. Domain models become anaemic, business logic leaks into application services, and the resulting architecture mirrors the database schema rather than the business it serves.

#### What to do instead

Identify the few domain entities with real behaviour — state transitions, invariants, computations — and build rich domain models for them. Reserve CRUD treatment for genuine reference data (currency codes, country lists). Resist the temptation to make every entity a generic resource.

---

### ⚠️ The shared-everything fallacy

One database for all contexts. One canonical "Customer" model used by marketing, fulfillment, and finance. The intent — coherence and reuse — collapses into a coordination tax: every change requires alignment across teams; every release blocks on the slowest dependency; every team carries every other team's compromises.

#### What to do instead

Accept that "Customer" means different things in different contexts. Marketing cares about lifecycle stage and campaign attribution; fulfillment cares about delivery addresses; finance cares about credit terms. Each context defines its own model with the attributes and rules that matter to it. Integrate via events that carry only the relevant slice.

---

### ⚠️ The ubiquitous-language gap

Engineers say "Order"; the domain expert says "Booking" with subtly different rules. The codebase and the business diverge, and bugs accumulate in the translation. Worse, the divergence becomes invisible — engineers stop noticing the mismatch and treat their vocabulary as authoritative.

#### What to do instead

Whenever vocabulary diverges, choose one term and enforce it everywhere — code, schemas, APIs, dashboards, support tools, runbooks. Domain experts should be uncomfortable reading anything other than their own language. The investment in alignment pays back at every cross-team conversation.

---

### ⚠️ The reference-model hostage

Adopting BIAN, FHIR, or ACORD wholesale and treating it as immutable, even where it conflicts with strategic differentiation. Reference models are accelerators for commodity capabilities, not constitutions. Treating them as constraints removes the very strategic flexibility they were meant to enable.

#### What to do instead

Map to the reference model where alignment is cheap and ecosystem-valuable (regulatory reporting, partner integration). Diverge explicitly where strategy demands; document the deviation and the business reason. The reference model is a starting point, not a target architecture.

---

### ⚠️ The Conway's Law surprise

Designing an architecture that doesn't fit the organisation that has to build and operate it. Within months, the implementation drifts toward what the org can actually maintain, and the documented design becomes archaeology. The architects blame the engineers; the engineers blame the architects; both are missing the point.

#### What to do instead

Design with the org structure in mind — or change the org. The "Inverse Conway Manoeuvre" (Skelton & Pais, *[Team Topologies](https://teamtopologies.com/)*) treats team boundaries as architectural decisions, not afterthoughts. If your bounded contexts cross team boundaries, expect coordination cost; if they fragment within a team, expect drift.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Service catalogue matches business capability map (not technology layers) ‖ The service registry should read like a list of business capabilities — Booking, Pricing, Fulfillment — not technology layers like Frontend or Backend. If a new product manager opens it and recognises their domain, you've structured well. If they see "user-service-v2", the boundary is wrong. | ☐ |
| 2 | Each bounded context owns its persistent state — no cross-context schema sharing ‖ No shared databases across contexts. If two services both write to the same `customers` table, they aren't really separate contexts — they're a distributed monolith with extra steps. Each context's data, schema migrations, and access patterns belong to one team. | ☐ |
| 3 | Ubiquitous language audit completed: code, schemas, contracts, docs all use the same domain vocabulary ‖ A domain expert should be able to read your code, schema names, API documentation, and Slack discussions without needing translation. If "Order" means three different things in three places, the language hasn't been disciplined. Bugs accumulate in the gap. | ☐ |
| 4 | Industry reference model (BIAN / FHIR / ACORD / eTOM / ISA-95) mapped where applicable; deviations documented with rationale ‖ These reference models encode decades of cross-industry learning that no single organisation could replicate. Map where ecosystem integration matters — open banking, interoperable health records, regulatory reporting. Document divergences explicitly so future architects know it was a strategic choice, not an oversight. | ☐ |
| 5 | Data classification (PII, PHI, PCI, public) surfaced in service contracts and runtime metadata ‖ A service contract that says "returns User object" tells you nothing about whether that contains PII, PHI, or payment data. Surface classification: tag fields, classify endpoints, make compliance posture readable from architecture diagrams — not buried three layers deep. | ☐ |
| 6 | Regulatory traceability documented: each constraint maps to a specific architectural decision ‖ A compliance officer should be able to point at a regulation ("EU PII can't leave the EU") and follow it to specific architectural decisions in your system. Without traceability, audits become archaeology — and architectural changes risk silent compliance breaks. | ☐ |
| 7 | Cross-context integration uses domain events; synchronous calls are documented exceptions ‖ Synchronous calls between contexts couple them temporally — when one is slow, all are slow; when one is down, all are down. Events decouple temporally and become the historical record, surviving system rewrites and team changes. | ☐ |
| 8 | Event schema versioning and consumer compatibility governance is explicit and enforced ‖ Events live longer than the systems that produced them. Without explicit versioning rules — additive changes only, breaking changes require new event types — every consumer team becomes a hostage to every producer team's deploys, and old events become production landmines. | ☐ |
| 9 | Every external system integration has an explicit anti-corruption layer ‖ When a vendor changes their schema, the blast radius should be one component (the ACL), not your domain core. Without ACLs, vendor concepts leak into business logic and you become hostage to their roadmap — every vendor migration becomes a domain rewrite. | ☐ |
| 10 | Team boundaries align with bounded context boundaries (or this misalignment is consciously managed) ‖ Conway's Law is descriptive, not aspirational — your architecture mirrors your org structure regardless. The question is whether you designed it that way or were surprised by it. Use Team Topologies' Inverse Conway Manoeuvre to align deliberately, or accept the coordination tax. | ☐ |

---

## Related

[`principles/ai-native`](../../principles/ai-native) | [`ddd/context-maps`](../../ddd/context-maps) | [`integration/event`](../../integration/event) | [`patterns/data`](../../patterns/data) | [`frameworks/togaf`](../../frameworks/togaf) | [`governance/review-templates`](../../governance/review-templates)

---

## References

1. [Eric Evans — Domain-Driven Design Reference](https://www.domainlanguage.com/ddd/reference/) — *domainlanguage.com*
2. [Vaughn Vernon — IDDD Samples (companion code to *Implementing Domain-Driven Design*)](https://github.com/VaughnVernon/IDDD_Samples) — *github.com*
3. [Designing Data-Intensive Applications](https://dataintensive.net/) — *dataintensive.net*
4. [Sam Newman — Building Microservices, 2nd ed.](https://samnewman.io/books/building_microservices_2nd_edition/) — *samnewman.io*
5. [Team Topologies](https://teamtopologies.com/) — *teamtopologies.com*
6. [Martin Fowler — Bounded Context](https://martinfowler.com/bliki/BoundedContext.html) — *martinfowler.com*
7. [BIAN Service Landscape](https://bian.org/servicelandscape/) — *bian.org*
8. [HL7 FHIR R5 — Healthcare Interoperability](https://hl7.org/fhir/) — *hl7.org*
9. [Anti-Corruption Layer Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer) — *Microsoft Learn*
10. [GDPR Article 25 — Data Protection by Design and by Default](https://gdpr-info.eu/art-25-gdpr/) — *gdpr-info.eu*
