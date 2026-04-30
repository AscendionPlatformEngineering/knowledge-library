# Security NFRs

The strategic guide for security non-functional requirements — recognising that the team's threats enumerated explicitly via threat-modelling rather than treating security as a uniform "make it secure" requirement, the controls specified per data classification rather than applied homogeneously across all data, the authentication-and-authorization targets stated as observable requirements (multi-factor enforcement coverage, session-lifetime ceilings, privilege-elevation audit completeness) rather than as adjectives, the audit-trail completeness requirements specified per regulated-action class with retention horizons matched to compliance regime, the secrets-management posture specified with rotation cadences and access-instrumentation rather than left to platform defaults, and the security-budget-violation interpretation that treats every audit failure or threat-model finding as architectural signal rather than as a defect to suppress are what determine whether the team's security posture is calibrated against actual threats facing the system or whether the system passes generic compliance checklists while remaining vulnerable to the specific adversary patterns that target its industry and data.

**Section:** `nfr/` | **Subsection:** `security/`
**Alignment:** ISO/IEC 25010 (Software Quality Model) | OWASP ASVS | OWASP SAMM | NIST Cybersecurity Framework | Google SRE Workbook
---

## What "security NFRs" means — and how it differs from compliance checklists and security architecture

A *primitive* approach to security is to apply a generic checklist (the platform's recommended security configuration, an industry compliance baseline) uniformly across the system, satisfy the audit, and assume the system is secure. After a security incident, the post-mortem reveals that the relevant control was either not on the checklist or was applied with default parameters that were inappropriate for the specific threat. The team adds the missing item to its private checklist and the cycle continues. After eighteen months, the organisation has a thick checklist, several incidents per year, and no architectural confidence that the controls deployed are matched to the threats actually facing the system.

The *architectural* alternative is to specify security as a contract grounded in *which threats* the system commits to defend against, *which data classifications* exist and what controls each demands, and *which observable measurements* validate that the controls are operating. Generic compliance checklists are a coverage check (have we considered the standard control set?) but they are not the contract. The contract is per-system: enumerate the threats, classify the data, specify the controls per classification, instrument validation in production, treat every validation failure as architectural signal.

This is *not* the same as the [security architecture pages](../../security) — those cover the design patterns and platform choices that implement security controls (authentication services, secrets management, network segmentation). This page covers the *requirements specifications* that those patterns must satisfy. Security architecture answers "how do we build it"; security NFRs answer "what must it observably do."

This is also *not* the same as the [NFR Scorecard](../../scorecards/nfr) — that page is the scoring instrument across all NFR categories. This page is one of the dimensions the scorecard scores, with the discipline-specific guidance on how to specify and validate security targets.

The architectural signature of well-specified security NFRs is *threat-traceable defence*. When the threat catalogue, data classification, and control specifications are all explicit and traced to each other, every control in the system points to the threat it mitigates and the data it protects. The auditor and the engineer can both read the trace. When the trace is missing, the system has controls and threats but no documented relationship between them, which means the next decision about adding or removing a control is made without reference to what defence it provides.

## Six principles

### 1. Enumerate threats explicitly via threat-modelling, not implicitly via compliance scope
A generic compliance baseline (PCI-DSS, ISO 27001, SOC 2) tells you which control categories you need; it does not tell you which specific threats you face. Two systems with identical compliance scope can face very different threat profiles depending on data sensitivity, user population, deployment model, and external attack surface. Specifying security requirements only against the compliance baseline produces a system that satisfies audit and is protected against the threat profile the baseline was designed for, which may not be the threat profile you actually face.

The discipline is to perform structured threat-modelling per significant subsystem (STRIDE, attack-tree, kill-chain, or another systematic method), enumerate the threats in writing, and specify defensive controls per threat. The compliance baseline provides coverage; the threat model provides direction. Threats that the team chooses not to defend against are documented as accepted risks, with rationale.

#### Architectural implications
Threat-modelling at architectural altitude shapes design choices: which boundaries need authentication, which paths need rate-limiting, which data classes need encryption-at-rest, which audit trails are mandatory. The threat catalogue is itself an architectural artefact, reviewed when the system's deployment model or external-attack-surface changes substantially.

#### Quick test
Pick a recent significant subsystem. Was a structured threat model produced for it? Did the threat model directly drive the controls implemented? If the answer is "we applied the standard security configuration," the threats facing this subsystem were not reasoned about and the control set is generic.

### 2. Classify data and specify controls per classification, not uniformly
A system handles data of different sensitivities. Customer credentials and payment data are highly sensitive. Customer-profile data is sensitive. Product catalogue and public content are not sensitive. Applying the same controls to all of it is either wasteful (encrypting public content) or under-protective (treating credentials with the same rigour as catalogue data). The discipline is the explicit data-classification scheme — typically four levels: public, internal, confidential, restricted — with controls specified per classification and the schema for each data store documenting the classification of every field.

#### Architectural implications
Classification drives concrete controls. Restricted data must be encrypted at rest with managed keys, encrypted in transit, accessible only via roles with multi-factor authentication, audited per access. Confidential data has slightly relaxed controls. Internal data has minimal controls beyond network-perimeter assumptions. Public data has no security-specific controls. The classification of fields ripples through schema design, query-builder choices, log-redaction rules, and replication topologies. A field whose classification is undocumented gets the most-restrictive default, which is expensive — so classifying fields deliberately is itself architectural work.

#### Quick test
Pick a data table in your most-used data store. For each column, can you state the classification level? If most fields are unclassified, the classification scheme is theoretical and the controls applied are uniform-by-default.

### 3. Specify authentication and authorization targets as observable measurements
"All users must authenticate" is a value statement. "All users must authenticate via OIDC, with MFA enforcement at 100% for confidential-data access and 100% for administrative actions, sessions limited to 8 hours of inactivity with re-authentication for elevation-of-privilege" is a measurable target. The first cannot be validated; the second produces specific instrumentation requirements (auth-event logging, session-lifetime metrics, privilege-elevation tracking) that yield ongoing measurements.

The discipline applies the same observability rigour as performance and reliability NFRs: every authentication-or-authorization rule has a target metric, a measurement instrument, and a budget threshold. MFA enforcement is measured as the fraction of confidential-data access events accompanied by successful MFA validation; the target is 100% with any deviation being an audit alert. Session-lifetime ceiling is measured as the distribution of session ages at access time; the target threshold is enforced at the auth-server level and audited at the application level.

#### Architectural implications
Observable auth targets push back on architecture choices. A system without centralised authentication cannot measure MFA-enforcement consistently; this is itself a security requirement-driven motivation for centralised auth. A system without structured audit logging cannot measure session-lifetime distribution; this drives logging investment. The targets and the architecture support each other: targets without architecture are unverifiable; architecture without targets is unmotivated.

#### Quick test
Look at your authentication NFR specification. Are MFA-enforcement, session-lifetime, and privilege-elevation rules expressed as observable measurements with thresholds? Or are they expressed as adjectives ("strong authentication," "reasonable session length")? If the latter, the rules are unverifiable and probably uneven in practice.

### 4. Specify audit-trail completeness per regulated-action class with retention horizons
Different action classes have different audit requirements. Privileged-administrative actions (role changes, configuration changes, service-account creation) require audit immutably with retention measured in years. Customer-data access has audit requirements driven by regulatory regime: GDPR access-logs, HIPAA access-logs, financial-services regulations all specify retention periods. Routine application logs may be retained for weeks. The audit-trail NFR distinguishes these classes and specifies the retention horizon for each.

The discipline is to inventory regulated-action classes, name the regulatory regime that drives each, specify retention duration per regime, and specify the immutability requirement (write-once-read-many storage, append-only databases, log-shipping to managed audit services). The inventory is reviewed when new regulatory regimes apply or when business operations cross a regulatory threshold (entering a new market, reaching a customer-volume threshold).

#### Architectural implications
Audit-trail requirements drive concrete platform choices: which storage backend is used for which audit class (S3 with object-lock for compliance audit; standard log-shipping for routine application logs), which retention policy is configured per backend, which access controls protect the audit data itself (audit logs are themselves restricted data and require their own controls). The architecture follows the requirement; the requirement is rooted in the regulatory regime.

#### Quick test
For your system, name the regulated-action classes, the regulatory regime driving each, and the specified retention duration. If the answer is "we keep all logs for 90 days," the regulated classes are not differentiated and the retention regime probably does not match the strictest regulation that applies.

### 5. Specify secrets-management posture with rotation cadences and access instrumentation
Secrets — API keys, database passwords, signing keys, encryption keys — are the operational core of security. A static secret embedded in a configuration file violates rotation requirements, makes access audit impossible, and creates a high-impact failure mode at compromise. The architecturally correct position is that all secrets live in a managed secrets-store, are rotated on a defined cadence, are accessed only by named identities with audited access, and never appear in source repositories or build artefacts.

The discipline is the secrets-management NFR specification: which secrets-store is used, what rotation cadence applies per secret class, what access-audit completeness is required, and what static-secret-detection runs in CI. The cadences are driven by threat model (compromise blast-radius) and by regulatory regime (some regimes specify rotation frequency). The access-audit requirement creates an instrumentation pre-requisite — the secrets-store must emit access events that are themselves audit-logged.

#### Architectural implications
Secrets-management drives application-architecture choices: how secrets are injected at runtime (environment variables versus volume mounts versus runtime-fetch), how rotation is propagated to running services (graceful credential refresh versus restart), how compromise is responded to (revocation procedure, audit forensics). The choices have operational cost; the cost is the price of the threat-model coverage.

#### Quick test
List the secret classes in your system and the rotation cadence specified per class. If most secrets are rotated only on incident-response or staff change, the rotation discipline is reactive rather than scheduled, and the threat-model has not driven the cadence.

### 6. Treat every audit finding and threat-model gap as architectural signal
A penetration test finding, an audit observation, a threat-model gap discovered in review — each is information about where the system's control set is incomplete relative to its threat profile. The architectural response is to either (a) close the gap with a control change, (b) accept the residual risk with documented rationale, or (c) revise the threat model if the original assumption was incorrect. All three are valid. The wrong response is to close the finding by suppressing the rule, narrowing the audit scope, or downgrading the severity without addressing the underlying state.

The discipline is the security-finding ledger: every finding has a recorded decision, owner, and trajectory. The aggregate is itself a security-posture signal — finding rates trending up are an architectural alarm even if individual findings are low-severity, because they indicate that the threat catalogue and control set are diverging from the operating reality of the system.

#### Architectural implications
The finding ledger is similar in shape to the maintainability suppression-ledger and the reliability burn-rate review: an explicit aggregate of architectural debt with named-decision discipline. The cross-cutting pattern across all NFR domains is that good NFR practice produces a debt-ledger artefact whose movement is architectural signal.

#### Quick test
Look at the most recent set of security findings. Does each have a recorded decision (close / accept / revise) with owner and date? Or are findings closed silently as developers address them in routine work? If the latter, the trajectory of findings is invisible and the architectural signal is lost.

## Five pitfalls

### ⚠️ Treating compliance baseline as the threat model
A compliance baseline (PCI-DSS, ISO 27001, SOC 2) covers the controls auditors expect; it does not cover the specific threats facing this system. Two systems with identical compliance scope can face different threat profiles. Treating the baseline as the threat model produces a system that passes audit and remains vulnerable to threats outside the baseline scope. The fix is the explicit threat model per significant subsystem, with controls traced to threats and the compliance baseline used only as a coverage check.

### ⚠️ Applying uniform controls across all data classifications
A single control set applied to all data wastes investment on low-sensitivity data and may under-protect high-sensitivity data. The fix is the explicit data-classification scheme with per-classification control specification; field-level classification documented in the schema; default to most-restrictive only for unclassified fields and with that default visible as architectural debt.

### ⚠️ Specifying auth requirements as adjectives instead of observable measurements
"Strong authentication" and "reasonable session length" are not requirements. The fix is observable specifications: MFA-enforcement coverage as a percentage with target threshold; session-lifetime as a distribution with measured ceiling; privilege-elevation as audit-event completeness. Every auth requirement has a metric, an instrument, and a budget.

### ⚠️ Single retention duration applied to all logs without regulated-class differentiation
Retention requirements vary by regulatory regime and action class. A single "90-day retention" applied uniformly under-retains audit data subject to regulations requiring multi-year retention, and over-retains routine logs. The fix is the per-class retention matrix, driven by regulatory regime, validated against the strictest regime that applies.

### ⚠️ Reactive rather than scheduled secrets rotation
If secrets rotate only on staff change or incident response, the rotation cadence is unspecified and the time-window of compromise exposure is whatever the time between incidents happens to be. The fix is the scheduled rotation cadence per secret class, automation that performs the rotation without operational disruption, and audit instrumentation that proves rotation occurred.

## Security NFR specification checklist

| # | Check | Status |
|---|---|---|
| 1 | Threat model exists per significant subsystem with named threats | ☐ |
| 2 | Data classification scheme is published with field-level classification documented | ☐ |
| 3 | Controls are specified per data classification, not uniformly | ☐ |
| 4 | Authentication requirements are expressed as observable measurements with thresholds | ☐ |
| 5 | Authorization rules are testable in CI with audit-event coverage | ☐ |
| 6 | Audit-trail retention matrix exists with regulatory-regime-driven duration per class | ☐ |
| 7 | Audit-trail immutability is configured per audit class | ☐ |
| 8 | Secrets-management posture specifies store, rotation cadence, and access-audit | ☐ |
| 9 | Static-secret-detection runs in CI on source and build artefacts | ☐ |
| 10 | Security-finding ledger records decision (close / accept / revise) per finding | ☐ |

## Related

- [Maintainability NFRs](../maintainability) — sister page on code-health and change-velocity requirements
- [Performance NFRs](../performance) — sister page on latency, throughput, and saturation requirements
- [Reliability NFRs](../reliability) — sister page on availability and graceful-degradation requirements
- [Usability NFRs](../usability) — sister page on user-facing quality requirements
- [NFR Scorecard](../../scorecards/nfr) — the scoring instrument applied across all NFR categories
- [Application Security](../../security/application-security) — patterns for application-layer controls
- [Authentication & Authorization](../../security/authentication-authorization) — patterns for identity and access management
- [Encryption](../../security/encryption) — patterns for data-at-rest and data-in-transit protection
- [Cloud Security](../../security/cloud-security) — patterns for platform-layer controls
- [Vulnerability Management](../../security/vulnerability-management) — operational practice for finding-trajectory
- [Templates: ADR Template](../../templates/adr-template) — how risk-acceptance decisions are recorded

## References

1. [ISO/IEC 25010 (Software Quality Model)](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010) — *iso25000.com*
2. [OWASP Top 10](https://owasp.org/www-project-top-ten/) — *owasp.org*
3. [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) — *owasp.org*
4. [OWASP Software Assurance Maturity Model (SAMM)](https://owaspsamm.org/) — *owaspsamm.org*
5. [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) — *nist.gov*
6. [Google SRE Workbook](https://sre.google/workbook/table-of-contents/) — *sre.google*
7. [AWS Well-Architected Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html) — *aws.amazon.com*
8. [Continuous Architecture in Practice](https://www.oreilly.com/library/view/continuous-architecture-in/9780136523710/) — *oreilly.com*
9. [Quality Attribute Workshop (SEI)](https://insights.sei.cmu.edu/library/quality-attribute-workshop-third-edition-participants-handbook/) — *sei.cmu.edu*
10. [arc42 Architecture Template](https://arc42.org/) — *arc42.org*
