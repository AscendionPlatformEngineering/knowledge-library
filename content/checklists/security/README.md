# Security Review Checklist

The artefact that evaluates whether a proposed system defends adequately against the threats it actually faces — recognising that security review is about coverage of the attack surface, alignment with the documented threat model, and calibration by the incidents and findings that prior reviews missed, not about ticking compliance boxes that don't reflect the system's real risks.

**Section:** `checklists/` | **Subsection:** `security/`
**Alignment:** OWASP Application Security Verification Standard | NIST Secure Software Development Framework | STRIDE Threat Model | Threat Modeling Manifesto

---

## What "security review checklist" actually means

A *primitive* security review reads as a compliance pass: a long list of items drawn from a regulatory standard or a generic security framework, marked off by reviewers who often don't know which items apply to this specific system, applied uniformly across systems with very different risk profiles. The output is a record that the review happened — useful for audit, less useful for security. The system that just passed the review may still have unaddressed authentication gaps in its admin console, missing rate limits on its public API, secrets in source-controlled configuration, and an attacker-visible attack surface that the review's items didn't cover. Security-review-as-compliance produces compliance, not security.

A *production* security review checklist is a coverage instrument designed around the system's actual *attack surface* and the team's documented *threat model*. It's organised by what an attacker sees and would attempt — entry points, trust boundaries, sensitive data flows, privileged operations — rather than by control category (a list of "encryption" controls, a list of "authentication" controls, a list of "logging" controls all evaluated independently). Items are drawn from the threat model: each documented threat ("attacker compromises an administrator account," "attacker injects malicious input into the API," "attacker accesses backups") produces items that verify the controls defending against it. *Defense in depth* is the organising principle: each layer of defense (network, application, data, identity, monitoring) is verified independently, so that if one layer is breached the next layer still holds. *Compliance items* are distinguished from *security items*: regulatory requirements that don't necessarily improve security still get checked, but separately, so the team can see what's actually defending the system versus what's satisfying audit. The checklist is calibrated by *actual security incidents and findings* — every breach class, penetration-test finding, and vulnerability disclosure produces candidate revisions, so the next review can't miss what the prior one did.

The architectural shift is not "we have a security checklist." It is: **security review is a coverage instrument calibrated by the system's actual attack surface, threat model, and incident history — and treating it as a compliance pass produces audit records rather than security, while leaving the actual risks the system faces unaddressed.**

---

## Six principles

### 1. Defense in depth as organising principle — each layer verified independently

A security review structured as one flat list of controls produces a binary outcome: either every item passes or some don't, with no visibility into *which layer of defense is weak*. The architectural reality is that real attacks succeed by chaining failures across layers: an attacker exploits a network exposure to reach an unpatched service, exploits an authentication weakness to access an account, exploits an authorisation gap to escalate privilege, exploits inadequate logging to evade detection. A defense that holds at any layer breaks the chain. The architectural discipline is to organise the checklist *by layer*, with items verifying each layer's defenses independently: network/perimeter, application/input validation, identity/authentication, authorisation/access control, data/encryption, monitoring/detection, incident-response readiness. Each layer's items can be evaluated independently; weaknesses in one layer are visible without being masked by strength in another.

#### Architectural implications

- The checklist is structured by defense layer with documented sections: network, application, identity, authorisation, data, monitoring, incident response.
- Each layer has its own items verifying the controls present at that layer, evaluated independently.
- The review's output identifies *which layers are strong and which are weak* — not just an aggregate pass/fail across the whole system.
- Failed items in any layer trigger documented decisions even if other layers are strong; the chain-of-failures attack model means single-layer weaknesses are still exploitable.

#### Quick test

> Pick the most recent security review in your organisation. Was the output organised by defense layer (network strong, application weak, identity strong, etc.), or was it a flat list of pass/fail items? If the latter, the review's coverage is opaque — the team can't tell which layers are doing the work and which are the weakest links the next attacker will target.

#### Reference

[NIST SP 800-207 Zero Trust](https://csrc.nist.gov/publications/detail/sp/800-207/final) treats defense in depth as an organising principle for modern security architecture. [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) provides a layered structure for application security verification that maps directly to checklist organisation.

---

### 2. Coverage by attack surface — what an attacker sees, not what control category it falls under

A common pattern: the security checklist is structured by control category — "all encryption items here, all authentication items there, all logging items in another section." Each category gets reviewed independently. The result: the *attack surface* — what an attacker actually sees and probes — isn't a coherent unit of review. The public API endpoints that an attacker would attempt are evaluated piecewise across multiple categories, with no item asking "have we evaluated each public endpoint as an attack-surface unit?" The architectural discipline is to organise coverage *by attack surface*: every public-facing surface (API endpoints, web UI, mobile API, admin console, email/notification ingress, file upload paths, third-party integration callbacks) has documented items verifying it as a unit. The review walks the attacker's view of the system, not the defender's catalog of controls.

#### Architectural implications

- The checklist enumerates the attack surfaces the system exposes: public APIs (each major endpoint or family), admin consoles, web/mobile UI, ingress paths (file upload, email, webhooks), trust boundaries with third-party services.
- Each attack surface has its own items covering authentication, authorisation, input validation, rate limiting, monitoring, and incident-response readiness for that specific surface.
- The review walks each attack surface as a coherent unit, in addition to (not instead of) layer-organised review.
- Surfaces that emerge mid-review (the admin console nobody mentioned in the design doc) are added to the surface enumeration rather than skipped because they weren't on the original list.

#### Quick test

> Pick the most-attacked surface in your organisation (probably the public API). Walk the security checklist's coverage of that surface. Are there items asking about authentication, authorisation, rate limiting, input validation, monitoring, and IR readiness for that specific surface? If the items are scattered across control-category sections without per-surface assembly, the review never evaluates the surface the way the attacker does.

#### Reference

[OWASP Top 10](https://owasp.org/www-project-top-ten/) is structured around the most common attack-surface vulnerabilities. [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/) treats attack-surface enumeration as a primary discipline. [STRIDE Threat Model](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats) provides the canonical attacker-perspective categorisation that maps to attack-surface review.

---

### 3. Threat model alignment — items map to documented threats, not generic best practices

A security checklist drawn from a generic standard catches the threats the standard's authors anticipated. It doesn't catch the threats *this specific system actually faces* — the threat model that's specific to the system's users, data, integrations, and adversaries. The architectural discipline is to maintain a documented threat model (typically using STRIDE, attack trees, or LINDDUN frameworks) and to ensure each item in the checklist *maps to a documented threat*. An item that doesn't map to any threat may be inherited cargo-cult requirement; a threat that doesn't have any items defending against it is a coverage gap. The checklist becomes the operational expression of the threat model, applied at review time.

#### Architectural implications

- A documented threat model exists for the system, identifying the actors, assets, attack vectors, and threats relevant to it.
- Each item in the checklist maps to a documented threat (or to a layer-level concern that addresses a class of threats).
- Items without threat-model mapping are flagged for review: are they catching a real threat that the threat model missed, or are they cargo cult that should be removed?
- Threats without item coverage are also flagged: an attack vector documented in the threat model that no item verifies is a coverage gap that the next attacker may find.

#### Quick test

> Pick five items in your security checklist. For each, what specific threat does it defend against (drawn from the system's threat model)? If items can't be mapped to documented threats, they're either catching threats the threat model missed (revise the threat model) or cargo cult (consider removal). Either way, the alignment isn't there.

#### Reference

[Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/) treats threat-model-aligned security work as the foundational discipline. [STRIDE Threat Model](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats) provides the canonical threat categorisation. [NIST Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf) operationalises threat-model-aligned security review at framework level.

---

### 4. Compliance items distinguished from security items — the same checklist serves different purposes

Compliance and security overlap but aren't the same. Some compliance items genuinely improve security (encrypting sensitive data at rest defends against backup-compromise threats and satisfies regulatory requirements). Some compliance items are largely audit-driven and don't materially change the security posture (specific log retention periods that satisfy regulations but don't deter real attackers). Some security items aren't required by any regulation but materially defend against real threats (rate limiting on the public API). A checklist that conflates these produces two failure modes: items that satisfy compliance but don't defend produce false security confidence; security items that aren't compliance-required get deprioritised in audit-driven environments. The architectural discipline is to *distinguish*: each item is tagged as compliance-required, security-driven, or both. The team can see what's actually defending the system, what's satisfying audit, and where investment is needed.

#### Architectural implications

- Each item carries tags identifying its purpose: compliance (which regulation), security (which threat), or both.
- The review output reports compliance coverage and security coverage separately; the team sees both views.
- Compliance-only items that don't materially improve security are still applied (regulations are non-optional) but recognised as audit work, not security work.
- Security-only items not required by regulation are prioritised on their security value, not on audit pressure.

#### Quick test

> Pick five items in your security checklist. For each, is it primarily compliance-driven, security-driven, or both? If the team can't distinguish, the checklist is conflating the purposes — and either compliance items are creating false security confidence or security items are being deprioritised because they don't show up on the audit.

#### Reference

[NIST Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf) explicitly separates security practices from compliance reporting. [OWASP Software Assurance Maturity Model (SAMM)](https://owaspsamm.org/) provides a maturity model that distinguishes security capability from compliance posture.

---

### 5. Tier-aware depth — the same checklist scales from minor changes to major systems

Applying the full security checklist to every change is over-burden — the team that has to do a comprehensive threat-model review for a typo fix learns to bypass the review. Applying a lightweight subset to every change is under-coverage — major systems that warrant deep review get the same depth as trivial changes. The architectural discipline is *tier-aware depth*: documented tiers (typically 3-4: routine, moderate, significant, critical) with criteria based on what the change touches (does it modify authentication? does it expose new attack surface? does it handle new sensitive data?). Each tier has documented expected coverage (which items are required, which are optional, which are skipped). High-tier changes get the full instrument; low-tier changes get the focused subset that catches the concerns at that scale. Tier assignment is itself a documented decision.

#### Architectural implications

- The checklist defines tiers (routine / moderate / significant / critical) with documented criteria — based on what the change touches: new attack surface, modified authentication or authorisation, new sensitive data handling, new third-party integration, etc.
- Each tier has documented expected coverage: which items are required, which are optional, which are skipped at that tier.
- Tier assignment for each review is documented at the start: "this change is being reviewed at tier 3 because it adds a new public API endpoint that handles personal data."
- Tier escalation mid-review is possible: a change that started at tier 2 and revealed unexpected security implications escalates to tier 3 and applies the additional items.

#### Quick test

> Pick the last five security reviews in your organisation. Were the tiers documented at the start, and did the items applied match the tier? If all five used the same depth regardless of stakes, the checklist isn't tier-aware — and either over-burdens routine changes or under-serves significant ones.

#### Reference

[OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) operationalises tiered security verification (Levels 1, 2, 3) with explicit criteria for each level. [NIST Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf) covers tier-aware security practices at framework level.

---

### 6. Calibration by incidents and pen-test findings — what got missed becomes the next item

A security checklist authored once and never revised becomes increasingly disconnected from the threats the system actually faces. New attack techniques emerge; the system's architecture evolves; new third-party integrations introduce new threats. The architectural discipline is to treat the checklist as a *living artefact calibrated by security findings*: every security incident, penetration-test finding, and vulnerability disclosure produces candidate revisions. The post-incident review or post-pen-test review asks "would the existing checklist have caught this?" If yes, the review process failed to apply it; if no, the checklist itself failed to cover this attack vector and an item gets added. Over time, the checklist accumulates the institutional learning of what *actual attackers* have found in this system — and the next review catches what previous reviews missed.

#### Architectural implications

- Every security incident, penetration-test finding, and vulnerability disclosure includes the question "would the security checklist have caught this?"
- Findings produce a queue of candidate checklist revisions, prioritised by frequency of similar findings and severity.
- Revisions are versioned and reviewed; what's added, why, which finding motivated it, reviewed by someone other than the author before merging.
- The checklist's items reflect the team's actual security history — items present because incidents and findings demonstrated they were needed, not because a generic standard recommended them.

#### Quick test

> Pick the most consequential security finding in your organisation in the last year (a real incident, a pen-test finding, or a coordinated disclosure). Was a candidate checklist revision proposed? If yes, was it incorporated? If the answer is "we discussed it but didn't update the checklist," the calibration loop is broken — and the next review will miss what this finding showed.

#### Reference

[OWASP Software Assurance Maturity Model (SAMM)](https://owaspsamm.org/) treats security-finding feedback into review processes as a primary maturity property. [SLSA Framework](https://slsa.dev/) operationalises the calibration loop for supply-chain security specifically, with similar architecture for general security review.

---

## Architecture Diagram

The diagram below shows the canonical security-review-checklist architecture: defense-in-depth layer organisation (network / application / identity / authorisation / data / monitoring / IR); attack-surface enumeration walking the attacker's view; threat-model alignment mapping items to documented threats; compliance-vs-security tagging; tier-aware depth with documented criteria; calibration loop where incidents, pen-test findings, and disclosures produce candidate revisions.

---

## Common pitfalls when adopting security-review-checklist thinking

### ⚠️ Compliance-style flat checklist

A long list of items drawn from a regulatory standard, marked off uniformly. Output is an audit record. The system passes the review and still has unaddressed real-world gaps.

#### What to do instead

Coverage organised by defense layer and attack surface. Items mapped to threats from the system's documented threat model. The review's output identifies which layers and surfaces are strong and which are weak.

---

### ⚠️ Items by control category, not attack surface

Encryption section, authentication section, logging section — each evaluated independently. The attack surface is never reviewed as a coherent unit; piecewise coverage misses surface-specific risks.

#### What to do instead

Per-attack-surface coverage in addition to layer-organised review. Each public endpoint, admin console, ingress path, third-party integration is evaluated as a coherent unit covering authentication, authorisation, input validation, rate limiting, monitoring, IR readiness for that surface.

---

### ⚠️ Generic items disconnected from threat model

The checklist items are drawn from a generic standard. They don't map to threats the system actually faces. Threats in the threat model don't have items defending against them.

#### What to do instead

Each item maps to a documented threat. Threats without item coverage are flagged as gaps. Items without threat mapping are reviewed — catching real threats the threat model missed, or cargo cult that should be removed.

---

### ⚠️ Compliance and security conflated

The checklist mixes compliance-required items with security-driven items. Items that satisfy regulations but don't materially defend produce false security confidence; security items not required by regulations get deprioritised.

#### What to do instead

Items tagged: compliance-required (which regulation), security-driven (which threat), or both. Review output reports compliance coverage and security coverage separately. The team sees what's defending the system versus what's satisfying audit.

---

### ⚠️ Static checklist disconnected from incidents and findings

The checklist was authored two years ago. Three pen-test findings since then surfaced gaps that items would have caught — if they had been added. The findings never produced revisions.

#### What to do instead

Calibration loop. Every security finding asks "would the checklist have caught this?" Findings feed candidate revisions. Versioned, reviewed updates. The checklist accumulates the team's actual security history.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | The checklist is structured by defense layer with documented sections — network, application, identity, authorisation, data, monitoring, IR ‖ Each layer evaluated independently. The review identifies which layers are strong and which are weak. Single-layer weaknesses are visible. | ☐ |
| 2 | The checklist enumerates attack surfaces the system exposes, with per-surface coverage ‖ Public APIs (each major endpoint family), admin consoles, UI, ingress paths, third-party integrations. Each surface evaluated as a coherent unit. The review walks the attacker's view. | ☐ |
| 3 | Each item maps to a documented threat from the system's threat model ‖ Items without threat mapping are flagged. Threats without item coverage are flagged. The checklist is the operational expression of the threat model. | ☐ |
| 4 | Items are tagged as compliance-required, security-driven, or both ‖ The review output reports compliance and security coverage separately. The team sees what's defending versus what's satisfying audit. Investment can be prioritised correctly. | ☐ |
| 5 | The checklist defines tiers with documented criteria for tier assignment ‖ Routine / moderate / significant / critical. Criteria based on what the change touches: new attack surface, modified auth, new sensitive data, etc. Each tier has documented expected coverage. | ☐ |
| 6 | Tier assignment for each review is documented at the start ‖ "This change is at tier 3 because it adds a new public API endpoint handling personal data." Tier escalation mid-review is documented. The review's depth matches the change's stakes. | ☐ |
| 7 | Items demand specific evidence — concrete configurations, audit-log queries, threat-model entries — not affirmation ‖ "What's the rate-limit configuration for endpoint X, and how is it monitored?" rather than "is rate limiting considered?" The review demands specifics. | ☐ |
| 8 | Every security incident asks "would the checklist have caught this?" with revision queue feed ‖ Calibration loop. Findings produce candidate revisions. Versioned and reviewed updates. The checklist accumulates the team's actual security history. | ☐ |
| 9 | Penetration-test findings and vulnerability disclosures feed the same calibration loop ‖ Not just incidents — pen tests and disclosures often surface gaps before incidents would. Their findings drive revisions with the same rigour. | ☐ |
| 10 | The checklist is integrated with code-review, design-review, and pre-deploy gates ‖ Surfaces in PR templates, design docs, deploy tickets. Authors confront items as they design and ship; reviewers reference items as they evaluate. The checklist embeds in the workflow. | ☐ |

---

## Related

[`checklists/architecture`](../architecture) | [`checklists/deployment`](../deployment) | [`security/application-security`](../../security/application-security) | [`security/authentication-authorization`](../../security/authentication-authorization) | [`security/encryption`](../../security/encryption) | [`security/vulnerability-management`](../../security/vulnerability-management)

---

## References

1. [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) — *owasp.org*
2. [OWASP Top 10](https://owasp.org/www-project-top-ten/) — *owasp.org*
3. [NIST Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf) — *csrc.nist.gov*
4. [STRIDE Threat Model](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats) — *learn.microsoft.com*
5. [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/) — *threatmodelingmanifesto.org*
6. [OWASP Software Assurance Maturity Model (SAMM)](https://owaspsamm.org/) — *owaspsamm.org*
7. [NIST SP 800-207 Zero Trust](https://csrc.nist.gov/publications/detail/sp/800-207/final) — *csrc.nist.gov*
8. [SLSA Framework](https://slsa.dev/) — *slsa.dev*
9. [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks) — *cisecurity.org*
10. [CSA Cloud Controls Matrix](https://cloudsecurityalliance.org/research/cloud-controls-matrix) — *cloudsecurityalliance.org*
