# Monolithic Coupling

> **Section:** `anti-patterns/` | **Subsection:** `monolithic-coupling/`  
> **Alignment:** TOGAF ADM | NIST CSF | ISO 27001 | AWS Well-Architected | AI-Native Extensions

---

## Overview

Design failures stemming from distributed monoliths: shared state, synchronous chains, and god services.

This document is part of the **Anti-Patterns** body of knowledge within the Ascendion Architecture Best-Practice Library. It provides comprehensive, practitioner-grade guidance aligned to industry standards and extended for AI-augmented, agentic, and LLM-driven design contexts.

---

## Core Principles

### 1. Intentional Design for Monolithic Coupling

Every aspect of monolithic coupling must be deliberately designed, not discovered after deployment. Document design decisions as ADRs with explicit rationale.

### 2. Consistency Across the Portfolio

Apply monolithic coupling practices consistently across all systems. Inconsistent application creates governance blind spots and makes incident investigation unpredictable.

### 3. Alignment to Business Outcomes

Monolithic Coupling practices must demonstrably contribute to business outcomes: reduced downtime, faster delivery, lower operational cost, or improved compliance posture.

### 4. Evidence-Based Quality Assessment

Quality of monolithic coupling implementation must be measurable. Define specific metrics and collect evidence continuously — not only at audit or review time.

### 5. Continuous Evolution

Standards for monolithic coupling evolve as technology and threat landscapes change. Schedule quarterly reviews of applicable standards and update practices accordingly.


---

## Implementation Guide

**Step 1: Current State Assessment**

Document the current state of monolithic coupling practice: what is implemented, what is missing, what is inconsistent across teams. Use the governance/scorecards section for a structured assessment framework.

**Step 2: Gap Analysis Against Standards**

Compare current state against the standards in this section and applicable frameworks (Anti-Patterns — Brown, Malveau, McCormick, Mowbray, Building Microservices — Sam Newman). Prioritize gaps by business impact and remediation effort.

**Step 3: Design the Target State**

Define the target monolithic coupling state: which patterns will be adopted, which anti-patterns eliminated, which governance mechanisms introduced. Express as a time-bound roadmap.

**Step 4: Incremental Implementation**

Implement monolithic coupling improvements incrementally: pilot with one team or system, measure outcomes, refine the approach, then expand. Avoid big-bang transformations.

**Step 5: Validate and Iterate**

Measure the impact of implemented changes against defined success criteria. Incorporate lessons learned into the practice standards. Contribute improvements back to this library.


---

## Governance Checkpoints

| Checkpoint | Owner | Gate Criteria | Status |
|---|---|---|---|
| Current State Documented | Solution Architect | Monolithic Coupling current state assessment completed and reviewed | Required |
| Gap Analysis Reviewed | Architecture Review Board | Gap analysis reviewed and prioritization approved | Required |
| Implementation Plan Approved | Enterprise Architect | Target state and roadmap approved by ARB | Required |
| Quality Metrics Defined | Solution Architect | Measurable success criteria defined for monolithic coupling improvements | Required |


---

## Recommended Patterns

### Reference Architecture Adoption

Start from an established reference architecture for monolithic coupling rather than designing from scratch. Adapt to organizational context rather than rebuilding proven foundations.

### Pattern Library Contribution

When your team solves a recurring monolithic coupling problem with a novel approach, document it as a pattern for the library. This compounds organizational knowledge over time.

### Fitness Function Testing

Encode monolithic coupling standards as automated architectural fitness functions — tests that run in CI/CD and fail builds when standards are violated. This makes governance continuous rather than periodic.


---

## Anti-Patterns to Avoid

### ⚠️ Standards Theater

Documenting monolithic coupling standards in architecture policies that no one reads and no one enforces. Standards without automated validation or governance gates are not operational standards.

### ⚠️ Copy-Paste Architecture

Adopting another organization's monolithic coupling patterns wholesale without adapting to organizational context, team capability, or regulatory environment. Always adapt; never just copy.


---

## AI Augmentation Extensions

### AI-Assisted Standards Review

LLM agents analyze design documents against monolithic coupling standards, generating structured gap reports with cited evidence and suggested remediation approaches.

> **Note:** AI review accelerates governance but does not replace expert architectural judgment. Use as a first-pass filter before human review.

### RAG Integration for Monolithic Coupling

This section is optimized for vector ingestion into an AI-powered architecture assistant. Semantic search enables architects to retrieve relevant monolithic coupling guidance through natural language queries.

> **Note:** Reindex the vector store whenever section content is updated to ensure retrieved guidance reflects current standards.


---

## Related Sections

[`principles/foundational`](../principles/foundational) | [`patterns/structural`](../patterns/structural) | [`governance/review-templates`](../governance/review-templates) | [`adrs/platform`](../adrs/platform)

---

## References

1. [Anti-Patterns — Brown, Malveau, McCormick, Mowbray](https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=Anti-Patterns+%E2%80%94+Brown%2C+Malveau%2C+McCormick%2C+Mowbray) — *IEEE Xplore*
2. [Building Microservices — Sam Newman](https://samnewman.io/books/building_microservices/) — *samnewman.io*
3. [Refactoring — Martin Fowler](https://www.amazon.com/Refactoring-Databases-Evolutionary-Addison-Wesley-Signature/dp/0321774515) — *Amazon*
4. [The Pragmatic Programmer](https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=The+Pragmatic+Programmer) — *IEEE Xplore*
5. [Documenting Software Architectures — Bass, Clements, Kazman](https://www.amazon.com/Documenting-Software-Architectures-Views-Beyond/dp/0321552687) — *Amazon*
6. [Building Evolutionary Architectures — Ford, Parsons, Kua](https://www.oreilly.com/library/view/building-evolutionary-architectures/9781491986356/) — *O'Reilly*


---

*Last updated: 2025 | Maintained by: Ascendion Solutions Architecture Practice*  
*Section: `anti-patterns/monolithic-coupling/` | Aligned to TOGAF · NIST · ISO 27001 · AWS Well-Architected*
