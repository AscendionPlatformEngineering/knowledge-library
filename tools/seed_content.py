#!/usr/bin/env python3
"""
Ascendion Engineering — content seeder

Creates the initial content/<section>/<subsection>/{README.md, diagram.mmd}
tree for the static-site generator. Stubs reproduce the boilerplate template
that is currently deployed, so running generate.py after this produces a site
visually identical to the current state for all stub-seeded pages.

Pages with custom content (e.g. principles/ai-native) are NEVER overwritten:
seed_content.py only writes files that don't already exist.

Usage:
    python tools/seed_content.py
"""

from pathlib import Path
import sys

# ─────────────────────────────────────────────────────────────────────────────
# TAXONOMY — section -> {subsection_slug: pretty_title}
# Mirrors the current site exactly (29 sections, ~130 subsections).
# ─────────────────────────────────────────────────────────────────────────────
TAXONOMY = {
    "adrs": {
        "ai":       "AI / ML Decisions",
        "data":     "Data Architecture Decisions",
        "platform": "Platform Architecture Decisions",
        "security": "Security Architecture Decisions",
    },
    "ai": {
        "architecture": "AI System Architecture",
        "ethics":       "AI Ethics & Responsible AI",
        "monitoring":   "AI Monitoring & Observability",
        "rag":          "Retrieval-Augmented Generation",
        "security":     "AI Security",
    },
    "anti-patterns": {
        "distributed-monolith":   "Distributed Monolith",
        "monolithic-coupling":    "Monolithic Coupling",
        "premature-optimization": "Premature Optimization",
        "shared-db-context":      "Shared Database Anti-Pattern",
    },
    "checklists": {
        "architecture": "Architecture Review Checklist",
        "deployment":   "Deployment Readiness Checklist",
        "security":     "Security Review Checklist",
    },
    "cloud": {
        "architecture":     "Cloud Architecture Patterns",
        "aws":              "AWS Architecture",
        "azure":            "Azure Architecture",
        "containerization": "Containerization & Orchestration",
        "gcp":              "GCP Architecture",
        "iac":              "Infrastructure as Code",
        "oracle":           "Oracle Cloud Architecture",
    },
    "compliance": {
        "bsp-afasa": "BSP & AFASA (Philippine FSI)",
        "gdpr":      "GDPR",
        "iso27001":  "ISO 27001",
        "pci-dss":   "PCI DSS",
    },
    "data": {
        "analytics":   "Analytics Architecture",
        "governance":  "Data Governance",
        "integration": "Data Integration",
        "lineage":     "Data Lineage",
        "mesh":        "Data Mesh",
        "modeling":    "Data Modeling",
    },
    "ddd": {
        "aggregates":   "Aggregates",
        "context-maps": "Context Mapping",
        "events":       "Domain Events",
        "repositories": "Repositories",
    },
    "design": {
        "data":       "Data-Level Design",
        "low-level":  "Low-Level Design",
        "performance":"Performance Design",
        "resilience": "Resilience Design",
        "security":   "Security Design",
    },
    "frameworks": {
        "gartner":  "Gartner Frameworks",
        "internal": "Ascendion Internal Frameworks",
        "nist":     "NIST CSF",
        "togaf":    "TOGAF",
        "zachman":  "Zachman Framework",
    },
    "governance": {
        "checklists":       "Governance Checklists",
        "review-templates": "Review Templates",
        "roles":            "Governance Roles",
        "scorecards":       "Governance Scorecards",
    },
    "infra": {
        "ci-cd":      "CI / CD",
        "monitoring": "Infrastructure Monitoring",
        "network":    "Network Architecture",
        "resilience": "Infrastructure Resilience",
        "security":   "Infrastructure Security",
    },
    "integration": {
        "api":       "API Integration",
        "event":     "Event-Driven Integration",
        "messaging": "Messaging Integration",
        "partners":  "Partner Integration",
        "workflow":  "Workflow Integration",
    },
    "maturity": {
        "guidelines": "Maturity Guidelines",
        "models":     "Maturity Models",
    },
    "nfr": {
        "maintainability": "Maintainability NFRs",
        "performance":     "Performance NFRs",
        "reliability":     "Reliability NFRs",
        "security":        "Security NFRs",
        "usability":       "Usability NFRs",
    },
    "observability": {
        "incident-response": "Incident Response",
        "logs":              "Logging",
        "metrics":           "Metrics",
        "sli-slo":           "SLIs & SLOs",
        "traces":            "Distributed Tracing",
    },
    "patterns": {
        "data":       "Data Patterns",
        "deployment": "Deployment Patterns",
        "integration":"Integration Patterns",
        "security":   "Security Patterns",
        "structural": "Structural Patterns",
    },
    "playbooks": {
        "api-lifecycle": "API Lifecycle",
        "migration":     "Migration Playbook",
        "resilience":    "Resilience Playbook",
    },
    "principles": {
        "ai-native":       "AI-Native Principles",
        "cloud-native":    "Cloud-Native Principles",
        "domain-specific": "Domain-Specific Principles",
        "foundational":    "Foundational Principles",
        "modernization":   "Modernization Principles",
    },
    "roadmaps": {
        "modernization":       "Modernization Roadmap",
        "target-architecture": "Target Architecture Roadmap",
        "tech-evolution":      "Technology Evolution Roadmap",
    },
    "runbooks": {
        "incident":  "Incident Runbook",
        "migration": "Migration Runbook",
        "rollback":  "Rollback Runbook",
    },
    "scorecards": {
        "architecture-review": "Architecture Review Scorecard",
        "nfr":                 "NFR Scorecard",
        "principles":          "Principles Scorecard",
    },
    "security": {
        "appsec":        "Application Security",
        "authentication-authorization":   "Authentication & Authorization",
        "cloud":         "Cloud Security",
        "encryption":    "Encryption",
        "vulnerability": "Vulnerability Management",
    },
    "strategy": {
        "ai-readiness":  "AI Readiness Strategy",
        "modernization": "Modernization Strategy",
        "principles":    "Strategy Principles",
    },
    "system-design": {
        "edge-ai":       "Edge AI Systems",
        "event-driven":  "Event-Driven Systems",
        "ha-dr":         "HA & DR Systems",
        "scalable":      "Scalable Systems",
    },
    "ai-native": {
        "architecture": "AI System Architecture",
        "ethics":       "AI Ethics & Responsible AI",
        "monitoring":   "AI Monitoring & Observability",
        "rag":          "Retrieval-Augmented Generation",
        "security":     "AI Security",
    },
    "tech": {
        # Legacy group — pre-v27 technology stubs. The substantive replacements
        # live under `technology/`. These entries exist so the legacy URLs that
        # were rendered by the old permissive build continue to resolve under
        # the strict build introduced in v29. Retire by removing the entries
        # here AND deleting the corresponding content/tech/<slug>/ directories.
        "ai-ml":       "AI/ML Stack",
        "angular":     "Angular Stack",
        "aws":         "AWS Stack",
        "azure":       "Azure Stack",
        "databases":   "Databases Stack",
        "devops":      "DevOps Stack",
        "gcp":         "GCP Stack",
        "java-spring": "Java/Spring Stack",
    },
    "security": {
        "application-security":         "Application Security",
        "authentication-authorization": "Authentication and Authorization",
        "cloud-security":               "Cloud Security",
        "encryption":                   "Encryption",
        "vulnerability-management":     "Vulnerability Management",
    },
    "technology": {
        "ui-ux-cx":          "UI, UX & CX",
        "api-backend":       "API & Backend Technologies",
        "databases":         "Databases",
        "cloud":             "Cloud",
        "devops":            "DevOps",
        "practice-circles":  "Practice Circles",
        "engagement-models": "Engagement Models",
    },
    "templates": {
        "adr-template":       "ADR Template",
        "review-template":    "Review Template",
        "scorecard-template": "Scorecard Template",
    },
    "tools": {
        "ai-agents":  "AI Agents Tooling",
        "cli":        "CLI Tooling",
        "scripts":    "Scripts & Automation",
        "validators": "Validators",
    },
    "views": {
        "deployment": "Deployment View",
        "logical":    "Logical View",
        "physical":   "Physical View",
        "process":    "Process View",
        "scenario":   "Scenario View",
    },
}

# Section-aware "body topic" used inside the boilerplate
SECTION_LABELS = {
    "adrs": "Architecture Governance",
    "ai": "AI-Native Architecture",
    "anti-patterns": "Anti-Patterns",
    "checklists": "Review Checklists",
    "cloud": "Cloud Architecture",
    "compliance": "Compliance & Regulatory Frameworks",
    "data": "Data Architecture",
    "ddd": "Domain-Driven Design",
    "design": "Detailed Design Practices",
    "frameworks": "Industry Frameworks Mapping",
    "governance": "Architecture Governance",
    "infra": "Infrastructure Architecture",
    "integration": "Integration Architecture",
    "maturity": "Architecture Maturity Models",
    "nfr": "Non-Functional Requirements",
    "observability": "Observability",
    "patterns": "Architecture & Design Patterns",
    "playbooks": "Engineering Playbooks",
    "principles": "Architecture Principles",
    "roadmaps": "Architecture Roadmaps",
    "runbooks": "Operational Runbooks",
    "scorecards": "Architecture Scorecards",
    "security": "Security Architecture",
    "strategy": "Architecture Strategy",
    "system-design": "System Design Reference Scenarios",
    "tech": "Technology Stack Best Practices",
    "templates": "Architecture Templates",
    "tools": "Architecture Tooling",
    "views": "Architecture Views",
}

# ─────────────────────────────────────────────────────────────────────────────
# README.md TEMPLATE
# Mirrors the boilerplate that is currently rendered on every article page.
# Topics that warrant real content (e.g. principles/ai-native) bypass this
# template — seed_content.py only writes files that do NOT already exist.
# ─────────────────────────────────────────────────────────────────────────────
README_TEMPLATE = """\
# {title}

{description}

**Section:** `{section}/` | **Subsection:** `{slug}/`
**Alignment:** TOGAF ADM | NIST CSF | ISO 27001 | AWS Well-Architected | AI-Native Extensions

---

## Overview

{description}

This document is part of the **{section_label}** body of knowledge within the Ascendion Architecture Best-Practice Library. It provides comprehensive, practitioner-grade guidance aligned to industry standards and extended for AI-augmented, agentic, and LLM-driven design contexts.

---

## Core Principles

### 1. Intentional Design for {title}

Every aspect of {title_lc} must be deliberately designed, not discovered after deployment. Document design decisions as ADRs with explicit rationale.

### 2. Consistency Across the Portfolio

Apply {title_lc} practices consistently across all systems. Inconsistent application creates governance blind spots and makes incident investigation unpredictable.

### 3. Alignment to Business Outcomes

{title} practices must demonstrably contribute to business outcomes: reduced downtime, faster delivery, lower operational cost, or improved compliance posture.

### 4. Evidence-Based Quality Assessment

Quality of {title_lc} implementation must be measurable. Define specific metrics and collect evidence continuously — not only at audit or review time.

### 5. Continuous Evolution

Standards for {title_lc} evolve as technology and threat landscapes change. Schedule quarterly reviews of applicable standards and update practices accordingly.

---

## Implementation Guide

**Step 1: Current State Assessment**

Document the current state of {title_lc} practice: what is implemented, what is missing, what is inconsistent across teams. Use the governance/scorecards section for a structured assessment framework.

**Step 2: Gap Analysis Against Standards**

Compare current state against the standards in this section and applicable frameworks (TOGAF 9.2 Architecture Governance Framework, COBIT 2019). Prioritize gaps by business impact and remediation effort.

**Step 3: Design the Target State**

Define the target {title_lc} state: which patterns will be adopted, which anti-patterns eliminated, which governance mechanisms introduced. Express as a time-bound roadmap.

**Step 4: Incremental Implementation**

Implement {title_lc} improvements incrementally: pilot with one team or system, measure outcomes, refine the approach, then expand. Avoid big-bang transformations.

**Step 5: Validate and Iterate**

Measure the impact of implemented changes against defined success criteria. Incorporate lessons learned into the practice standards. Contribute improvements back to this library.

---

## Governance Checkpoints

| Checkpoint | Owner | Gate Criteria | Status |
|---|---|---|---|
| Current State Documented | Solution Architect | {title} current state assessment completed and reviewed | Required |
| Gap Analysis Reviewed | Architecture Review Board | Gap analysis reviewed and prioritization approved | Required |
| Implementation Plan Approved | Enterprise Architect | Target state and roadmap approved by ARB | Required |
| Quality Metrics Defined | Solution Architect | Measurable success criteria defined for {title_lc} improvements | Required |

---

## Recommended Patterns

### Reference Architecture Adoption

Start from an established reference architecture for {title_lc} rather than designing from scratch. Adapt to organizational context rather than rebuilding proven foundations.

### Pattern Library Contribution

When your team solves a recurring {title_lc} problem with a novel approach, document it as a pattern for the library. This compounds organizational knowledge over time.

### Fitness Function Testing

Encode {title_lc} standards as automated architectural fitness functions — tests that run in CI/CD and fail builds when standards are violated. This makes governance continuous rather than periodic.

---

## Anti-Patterns to Avoid

### ⚠️ Standards Theater

Documenting {title_lc} standards in architecture policies that no one reads and no one enforces. Standards without automated validation or governance gates are not operational standards.

### ⚠️ Copy-Paste Architecture

Adopting another organization's {title_lc} patterns wholesale without adapting to organizational context, team capability, or regulatory environment. Always adapt; never just copy.

---

## AI Augmentation Extensions

### AI-Assisted Standards Review

LLM agents analyze design documents against {title_lc} standards, generating structured gap reports with cited evidence and suggested remediation approaches.

> **Note:** AI review accelerates governance but does not replace expert architectural judgment. Use as a first-pass filter before human review.

### RAG Integration for {title}

This section is optimized for vector ingestion into an AI-powered architecture assistant. Semantic search enables architects to retrieve relevant {title_lc} guidance through natural language queries.

> **Note:** Reindex the vector store whenever section content is updated to ensure retrieved guidance reflects current standards.

---

## Related Sections

[`principles/foundational`](../principles/foundational) | [`patterns/structural`](../patterns/structural) | [`governance/review-templates`](../governance/review-templates) | [`adrs/platform`](../adrs/platform)

---

## References

1. [TOGAF 9.2 Architecture Governance Framework](https://pubs.opengroup.org/architecture/togaf9-doc/arch/chap44.html) — *opengroup.org*
2. [COBIT 2019](https://www.isaca.org/resources/cobit) — *isaca.org*
3. [ISO/IEC 42010](https://www.iso.org/standard/74393.html) — *iso.org*
4. [IT Governance — Weill & Ross](https://www.amazon.com/Managers-Guide-Information-Security-Controls/dp/0749441127) — *Amazon*
5. [Documenting Software Architectures — Bass, Clements, Kazman](https://www.amazon.com/Documenting-Software-Architectures-Views-Beyond/dp/0321552687) — *Amazon*
6. [Building Evolutionary Architectures — Ford, Parsons, Kua](https://www.oreilly.com/library/view/building-evolutionary-architectures/9781491986356/) — *O'Reilly*

---

*Last updated: 2025 | Maintained by: Ascendion Solutions Architecture Practice*
*Section: `{section}/{slug}/` | Aligned to TOGAF · NIST · ISO 27001 · AWS Well-Architected*
"""

# ─────────────────────────────────────────────────────────────────────────────
# diagram.mmd TEMPLATE
# Mirrors the generic governance-lifecycle diagram on the current site.
# Real per-page diagrams replace this on a case-by-case basis.
# ─────────────────────────────────────────────────────────────────────────────
DIAGRAM_TEMPLATE = """\
flowchart TD
    A([🚀 Start: {title}]) --> B[Assessment & Discovery]

    B --> C{{Current State\\nDocumented?}}
    C -->|No| B
    C -->|Yes| D[Apply Architecture Principles]

    D --> D1[Design for Change]
    D --> D2[Least Privilege]
    D --> D3[Observability First]
    D --> D4[AI Augmentation Readiness]

    D1 & D2 & D3 & D4 --> E[Select Design Patterns]

    E --> F{{NFR Targets\\nDefined?}}
    F -->|No| F1[Define NFRs in nfr/]
    F1 --> F
    F -->|Yes| G[Document ADRs]

    G --> H[Architecture Review Board]

    H --> I{{Security\\nReview Passed?}}
    I -->|No| I1[Revise Design]
    I1 --> H
    I -->|Yes| J{{ARB\\nApproval?}}

    J -->|Rejected| J1[Address Feedback]
    J1 --> H
    J -->|Approved| K[Implementation]

    K --> L[CI/CD Pipeline]
    L --> L1[SAST / DAST Scan]
    L --> L2[Architecture Lint]
    L --> L3[NFR Validation]

    L1 & L2 & L3 --> M{{All Gates\\nPassed?}}
    M -->|No| M1[Fix & Rerun]
    M1 --> L
    M -->|Yes| N[Deploy to Production]

    N --> O[Observability Validation]
    O --> P[Post-Deployment Review]
    P --> Q([✅ Governance Record Closed])

    style A fill:#4f8ef7,color:#fff
    style Q fill:#10b981,color:#fff
    style I1 fill:#fef3c7
    style J1 fill:#fef3c7
    style M1 fill:#fef3c7
"""

# Per-section short descriptions (one-liner used in the README header)
SHORT_DESC = {
    ("adrs", "ai"):        "Architecture decision records for AI/ML systems including model selection, data, and governance trade-offs.",
    ("adrs", "data"):      "Architecture decision records for data architecture including modelling, integration, and governance.",
    ("adrs", "platform"):  "Architecture decision records for platform-level concerns including runtime, deployment, and integration.",
    ("adrs", "security"):  "Architecture decision records for security-critical decisions including identity, encryption, and segmentation.",

    ("ai", "architecture"):"AI-native system architecture including reference patterns for inference, retrieval, and orchestration.",
    ("ai", "ethics"):      "Responsible-AI principles, fairness, transparency, and human oversight for AI systems.",
    ("ai", "monitoring"):  "Telemetry, evaluation, drift detection, and quality observability for AI systems.",
    ("ai", "rag"):         "Retrieval-Augmented Generation patterns including indexing, hybrid retrieval, and grounding.",
    ("ai", "security"):    "Security architecture for AI: prompt injection, training data protection, model exfiltration, and guardrails.",

    ("anti-patterns", "distributed-monolith"):   "When microservices are coupled at the data or release layer despite service boundaries.",
    ("anti-patterns", "monolithic-coupling"):    "Hidden coupling that prevents independent change in modular systems.",
    ("anti-patterns", "premature-optimization"): "Optimizing performance, scale, or abstraction before the design has been validated.",
    ("anti-patterns", "shared-db-context"):      "Multiple services or domains sharing a database, breaking ownership and lifecycle.",

    ("checklists", "architecture"): "Pre-build architecture review checklist covering principles, NFRs, security, and observability.",
    ("checklists", "deployment"):   "Pre-production deployment checklist covering testing, observability, security, and rollback readiness.",
    ("checklists", "security"):     "Security review checklist for design, code, and deployment phases.",

    ("cloud", "architecture"):     "Cloud-native reference architectures and decision frameworks for AWS, Azure, and GCP.",
    ("cloud", "aws"):               "AWS-specific reference architectures, services, and Well-Architected guidance.",
    ("cloud", "azure"):             "Azure-specific reference architectures, services, and CAF guidance.",
    ("cloud", "containerization"):  "Containerization and orchestration patterns: Docker, Kubernetes, ECS, ACA.",
    ("cloud", "gcp"):               "GCP-specific reference architectures, services, and architecture-framework guidance.",
    ("cloud", "iac"):               "Infrastructure-as-code practices: Terraform, CDK, Bicep, Pulumi, modular composition.",
    ("cloud", "oracle"):            "Oracle Cloud Infrastructure architecture for legacy and enterprise workloads.",

    ("compliance", "bsp-afasa"): "Bangko Sentral ng Pilipinas regulations and AFASA compliance for Philippine financial services.",
    ("compliance", "gdpr"):      "EU General Data Protection Regulation compliance architecture and controls.",
    ("compliance", "iso27001"):  "ISO 27001 information security management system compliance architecture.",
    ("compliance", "pci-dss"):   "PCI DSS compliance architecture for payment card data handling.",

    ("data", "analytics"):   "Analytics platform architecture including warehousing, lakehouse, and BI patterns.",
    ("data", "governance"):  "Data ownership, classification, quality, retention, and stewardship architecture.",
    ("data", "integration"): "Data integration patterns: ETL/ELT, CDC, streaming, and federation.",
    ("data", "lineage"):     "End-to-end data lineage tracking, lineage capture, and impact analysis architecture.",
    ("data", "mesh"):        "Data Mesh architectural principles, data products, and federated governance.",
    ("data", "modeling"):    "Data modelling for transactional, analytical, and event-driven systems.",

    ("ddd", "aggregates"):   "Aggregate root design, transactional consistency boundaries, and invariant protection.",
    ("ddd", "context-maps"): "Context mapping patterns: shared kernel, customer-supplier, conformist, anti-corruption layer.",
    ("ddd", "events"):       "Domain event modelling, event storming, and event-carried state transfer.",
    ("ddd", "repositories"): "Repository patterns, persistence boundaries, and aggregate retrieval.",

    ("design", "data"):        "Data-level design: schema design, indexing strategies, query patterns, and consistency models.",
    ("design", "low-level"):   "Component-level and class-level design including SOLID, Gang-of-Four, and refactoring patterns.",
    ("design", "performance"): "Performance design: caching tiers, async processing, batching, and resource pooling.",
    ("design", "resilience"): "Resilience design: bulkheads, circuit breakers, timeouts, retries, and graceful degradation.",
    ("design", "security"):   "Security-by-design at the component level: input validation, output encoding, secrets handling.",

    ("frameworks", "gartner"):  "Gartner reference frameworks including Pace-Layered, Bimodal IT, and emerging tech radars.",
    ("frameworks", "internal"): "Ascendion-internal architecture frameworks adapted from industry standards for client engagement.",
    ("frameworks", "nist"):     "NIST Cybersecurity Framework, NIST AI RMF, and applied control architectures.",
    ("frameworks", "togaf"):    "TOGAF ADM phases, deliverables, and architecture content framework.",
    ("frameworks", "zachman"):  "Zachman Framework rows and columns applied to enterprise architecture.",

    ("governance", "checklists"):       "Governance gate checklists for architecture, security, and pre-production review.",
    ("governance", "review-templates"): "Review templates for ARB, security review, and design review meetings.",
    ("governance", "roles"):            "RACI for architecture governance: Solution Architect, Enterprise Architect, ARB, CTO.",
    ("governance", "scorecards"):       "Scorecards for measuring architecture quality and governance compliance.",

    ("infra", "ci-cd"):      "CI/CD pipeline architecture including testing stages, artifact management, and deployment strategies.",
    ("infra", "monitoring"): "Infrastructure monitoring architecture including metrics, alerting, and capacity tracking.",
    ("infra", "network"):    "Network architecture including segmentation, ingress/egress, service mesh, and connectivity.",
    ("infra", "resilience"): "Infrastructure resilience including multi-AZ, multi-region, backup, and DR architecture.",
    ("infra", "security"):   "Infrastructure security including network segmentation, IAM, secret management, and key rotation.",

    ("integration", "api"):       "API integration patterns: REST, GraphQL, gRPC, and BFF.",
    ("integration", "event"):     "Event-driven integration patterns: pub/sub, event sourcing, and CDC.",
    ("integration", "messaging"): "Messaging integration patterns: queues, topics, and message broker architecture.",
    ("integration", "partners"):  "External partner integration patterns: B2B, API gateways, and data exchange.",
    ("integration", "workflow"):  "Workflow and orchestration integration: BPM, saga, and stateful workflows.",

    ("maturity", "guidelines"): "Maturity assessment guidelines and how to use maturity models for architecture programs.",
    ("maturity", "models"):     "Maturity models: capability maturity, security maturity, AI maturity, cloud maturity.",

    ("nfr", "maintainability"): "Maintainability NFRs: code health, deployability, observability of internal state.",
    ("nfr", "performance"):     "Performance NFRs: latency, throughput, capacity, and scalability targets.",
    ("nfr", "reliability"):     "Reliability NFRs: availability, durability, fault tolerance, MTTR, MTBF.",
    ("nfr", "security"):        "Security NFRs: confidentiality, integrity, availability, and compliance posture.",
    ("nfr", "usability"):       "Usability NFRs: accessibility, internationalization, and human factors.",

    ("observability", "incident-response"): "Incident response architecture: detection, escalation, war room, and postmortem flows.",
    ("observability", "logs"):              "Logging architecture: structured logs, log aggregation, retention, and correlation.",
    ("observability", "metrics"):           "Metrics architecture: time-series, RED/USE methods, and metric cardinality control.",
    ("observability", "sli-slo"):           "SLI/SLO design, error budgets, and SLO-driven engineering practice.",
    ("observability", "traces"):            "Distributed tracing architecture: instrumentation, sampling, and trace correlation.",

    ("patterns", "data"):        "Data patterns: CQRS, Event Sourcing, Outbox, Data Lake, Lakehouse, Data Mesh.",
    ("patterns", "deployment"): "Deployment patterns: blue-green, canary, rolling, feature flags, immutable infrastructure.",
    ("patterns", "integration"):"Enterprise Integration Patterns: message broker, saga, choreography, orchestration.",
    ("patterns", "security"):   "Security patterns: zero-trust, secrets vault, mTLS, identity federation.",
    ("patterns", "structural"): "Structural patterns: hexagonal, layered, microkernel, event-driven, microservices.",

    ("playbooks", "api-lifecycle"): "End-to-end API lifecycle playbook from design through deprecation.",
    ("playbooks", "migration"):     "Migration playbook for legacy-to-cloud, monolith-to-microservices, and re-platforming.",
    ("playbooks", "resilience"):    "Resilience engineering playbook: chaos engineering, game days, failure injection.",

    ("principles", "ai-native"):       "Principles for systems where AI is a first-class architectural component.",
    ("principles", "domain-specific"): "Domain-specific principles for financial services, government, healthcare, and telco.",
    ("principles", "foundational"):    "Base axioms of sound architecture: separation of concerns, single responsibility, design for failure.",
    ("principles", "modernization"):   "Principles for legacy modernization: strangler fig, decomposition, and incremental migration.",

    ("roadmaps", "modernization"):       "Modernization roadmap framework with phasing, dependencies, and value realization.",
    ("roadmaps", "target-architecture"): "Target architecture roadmap from current state to target state with intermediate milestones.",
    ("roadmaps", "tech-evolution"):      "Technology evolution roadmap including capability uplift and platform investments.",

    ("runbooks", "incident"):  "Incident response runbook including triage, escalation, communication, and recovery procedures.",
    ("runbooks", "migration"): "Migration runbook including pre-migration, migration window, and post-migration verification.",
    ("runbooks", "rollback"):  "Rollback runbook including decision criteria, execution steps, and post-rollback assessment.",

    ("scorecards", "architecture-review"): "Architecture review scorecard covering principles, NFRs, security, and operability.",
    ("scorecards", "nfr"):                 "NFR scorecard for measuring system quality against non-functional targets.",
    ("scorecards", "principles"):          "Architecture principles scorecard for measuring adherence to defined principles.",

    ("security", "appsec"):        "Application security architecture: SAST, DAST, IAST, dependency scanning, runtime protection.",
    ("security", "authentication-authorization"):   "Authentication and authorization architecture: OIDC, OAuth 2.x, RBAC, ABAC, ReBAC.",
    ("security", "cloud"):         "Cloud security architecture: shared responsibility, IAM, key management, network controls.",
    ("security", "encryption"):    "Encryption architecture: at rest, in transit, in use, key management, post-quantum readiness.",
    ("security", "vulnerability"): "Vulnerability management architecture: SCA, SAST, DAST, runtime detection, response.",

    ("strategy", "ai-readiness"):  "AI readiness strategy: data foundations, governance, capability, and adoption framework.",
    ("strategy", "modernization"): "Modernization strategy: portfolio assessment, migration patterns, and value framework.",
    ("strategy", "principles"):    "Strategic architecture principles guiding multi-year platform and capability decisions.",

    ("system-design", "edge-ai"):      "Edge AI system design including model deployment, sync patterns, and offline operation.",
    ("system-design", "event-driven"): "Event-driven system design including event sourcing, CQRS, and stream processing.",
    ("system-design", "ha-dr"):        "High-availability and disaster-recovery system design across regions and providers.",
    ("system-design", "scalable"):     "Scalable system design including horizontal scaling, sharding, and partitioning strategies.",

    ("security", "application-security"):         "Secure-by-design application engineering: OWASP, dependency supply chain, validation, and threat modeling.",
    ("security", "authentication-authorization"): "Identity systems: AuthN vs AuthZ, federation (OIDC/SAML/OAuth), policy decision points, MFA, and identity governance.",
    ("security", "cloud-security"):               "Cloud-native security: shared responsibility, IAM at scale, CSPM/CIEM/CWPP/CNAPP, and account topology.",
    ("security", "encryption"):                   "Cryptographic engineering: data at rest/transit/in-use, key management, crypto agility, and certificate lifecycle.",
    ("security", "vulnerability-management"):     "Vulnerability lifecycle: discovery, prioritization, remediation workflows, and patch hygiene.",

    ("ai-native", "architecture"): "AI system architecture: serving topology, agentic state machines, deterministic-stochastic boundary, and inference cost shaping.",
    ("ai-native", "ethics"):       "Responsible AI engineering: fairness measurement, interpretability, human oversight, model and system cards, and risk-tier compliance.",
    ("ai-native", "monitoring"):   "AI-specific observability: drift detection, hallucination signal, output quality scoring, token economics, and feedback loops.",
    ("ai-native", "rag"):          "Retrieval-Augmented Generation as architecture: chunking, hybrid retrieval, embedding choice, citation provenance, and multi-axis evaluation.",
    ("ai-native", "security"):     "AI threat surface: prompt injection, training-data poisoning, model extraction, jailbreaks, and agent capability boundaries.",

    ("technology", "ui-ux-cx"):          "Frontend frameworks (React, Angular, Vue), UX laws, and customer-experience architecture.",
    ("technology", "api-backend"):       "Backend stacks (Java/Spring, Node.js, Python) and API design and delivery patterns.",
    ("technology", "databases"):         "Database choices across SQL, NoSQL, document, key-value, graph, time-series, and vector.",
    ("technology", "cloud"):             "Cloud platforms (AWS, Azure, GCP) and 12-factor cloud-native architecture patterns.",
    ("technology", "devops"):            "DevOps and SRE excellence: pipelines, IaC, GitOps, observability, and security.",
    ("technology", "practice-circles"):  "Specialized practice circles for platform, enterprise integration, COTS, and legacy modernization.",
    ("technology", "engagement-models"): "Strategic delivery frameworks: staffing, managed capacity, managed services, and AI-native delivery.",

    ("tech", "ai-ml"):       "AI/ML technology stack including training, serving, and feature store technologies.",
    ("tech", "angular"):     "Angular front-end stack including state management, routing, and testing patterns.",
    ("tech", "aws"):         "AWS technology stack: compute, storage, networking, data, and AI services.",
    ("tech", "azure"):       "Azure technology stack: compute, storage, networking, data, and AI services.",
    ("tech", "databases"):   "Database technology choices: relational, document, key-value, graph, time-series, vector.",
    ("tech", "devops"):      "DevOps tooling stack: CI/CD, IaC, GitOps, observability, and security.",
    ("tech", "gcp"):         "GCP technology stack: compute, storage, networking, data, and AI services.",
    ("tech", "java-spring"): "Java and Spring stack: Spring Boot, Spring Cloud, reactive Spring, and testing.",

    ("templates", "adr-template"):       "Standard ADR template covering context, decision, alternatives, and consequences.",
    ("templates", "review-template"):    "Standard architecture review template for ARB and design review meetings.",
    ("templates", "scorecard-template"): "Scorecard template for architecture quality and governance scoring.",

    ("tools", "ai-agents"):  "AI-agent tooling: agent frameworks, tool libraries, and integration patterns.",
    ("tools", "cli"):        "CLI tooling for architects: scaffolders, validators, and diagram generators.",
    ("tools", "scripts"):    "Operational scripts for architecture as code: linting, migrating, scaffolding.",
    ("tools", "validators"): "Architecture validators: schema, dependency, NFR, and policy validators.",

    ("views", "deployment"): "4+1 Deployment View: physical deployment topology and operational concerns.",
    ("views", "logical"):    "4+1 Logical View: conceptual decomposition of the system's functionality.",
    ("views", "physical"):   "4+1 Physical View: hardware and infrastructure topology.",
    ("views", "process"):    "4+1 Process View: runtime concurrency, processes, and threads.",
    ("views", "scenario"):   "4+1 Scenario View: use-case scenarios linking the four primary views.",
}


def main():
    repo_root = Path(__file__).resolve().parent.parent
    content = repo_root / "content"
    content.mkdir(exist_ok=True)

    created_readme, created_diagram, skipped = 0, 0, 0

    for section, subs in TAXONOMY.items():
        section_label = SECTION_LABELS.get(section, section.title())

        for slug, title in subs.items():
            sub_dir = content / section / slug
            sub_dir.mkdir(parents=True, exist_ok=True)

            description = SHORT_DESC.get((section, slug),
                                         f"{title} — practitioner guidance.")

            readme_path = sub_dir / "README.md"
            if not readme_path.exists():
                readme_path.write_text(
                    README_TEMPLATE.format(
                        title=title,
                        title_lc=title.lower(),
                        description=description,
                        section=section,
                        slug=slug,
                        section_label=section_label,
                    ),
                    encoding="utf-8",
                )
                created_readme += 1
            else:
                skipped += 1

            diagram_path = sub_dir / "diagram.mmd"
            if not diagram_path.exists():
                diagram_path.write_text(
                    DIAGRAM_TEMPLATE.format(title=title),
                    encoding="utf-8",
                )
                created_diagram += 1

    print(f"\n── Seed complete ─────────────────────────────────────────")
    print(f"  READMEs created:  {created_readme}")
    print(f"  diagrams created: {created_diagram}")
    print(f"  skipped (already existed): {skipped}")
    print(f"\nNext: run `python tools/generate.py` to build the site.\n")


if __name__ == "__main__":
    main()
