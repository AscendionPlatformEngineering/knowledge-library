# Application Security

The discipline of building applications that are hard to attack, where security is a property of the code, the dependencies, the build, and the runtime — not a layer added afterward by a separate team.

**Section:** `security/` | **Subsection:** `application-security/`
**Alignment:** OWASP Top 10 | OWASP ASVS | SLSA Framework | STRIDE

---

## What "application security" actually means

A *bolt-on* approach treats security as something added after the application is built: a penetration test before launch, a Web Application Firewall in front of the service, a bug bounty programme that finds what shipped. The application itself is built to do its job; security is a separate concern handled by a separate team after the design is frozen. This works for catching the most obvious bugs and produces predictably bad outcomes for everything else — structural weaknesses get baked in, dependencies bring in vulnerabilities the team never reviewed, and the cost of fixing what shipped is many times the cost of designing it differently.

A *built-in* approach treats security as a property of the application — present in the design, the code, the dependency choices, the build pipeline, and the runtime, rather than overlaid on top of them. The design is reviewed against threat models. The code is checked statically for known dangerous patterns. The dependencies are tracked, signed, and scanned. The runtime has telemetry that catches what static analysis missed. Each layer catches what the others cannot, and the cumulative effect is an application that is structurally harder to attack — not because it has been hardened against attack, but because it was built to make attack expensive in the first place.

The architectural shift is not "we do security testing." It is: **security is a property the application has by design — through threat modelling, secure defaults, validated inputs, encoded outputs, vetted dependencies, and complementary scans at every stage — not a check applied to a finished product.**

---

## Six principles

### 1. Security is designed in, not bolted on

Every security control added after design is more expensive than the same control designed in from the start, and many controls cannot be retrofitted at all. Authentication assumed to happen at the edge cannot be added inside services without coordinating every caller. Input validation assumed to happen at one boundary cannot be added at another without the original boundary's validation becoming unreliable. Cryptographic decisions made for one threat model do not survive a change in the model. Designing security in means: threat modelling at the start, security requirements in the requirements document, secure defaults in the code, and reviews at architectural milestones — not at the pre-launch milestone when changing direction is impossible.

#### Architectural implications

- Threat models are produced for each significant feature or service before the code is written, not as a checkbox before launch.
- Security requirements (authentication, authorisation, audit, data classification, residency) are explicit alongside functional requirements, not deduced afterwards.
- Default configurations are secure: TLS on, strict permissions, audit on, least-privilege identity, no secrets in code or images.
- Reviews include security at design, code, and pre-deployment gates — not only at the final pre-launch security gate where finding a problem means delaying release.

#### Quick test

> Pick a recently shipped feature in your application. When was the threat model written, who reviewed it, and what changed in the design as a result? If the threat model was written after the feature shipped (or never), security was bolted on, regardless of what the security testing report says.

#### Reference

[OWASP Software Assurance Maturity Model (SAMM)](https://owaspsamm.org/) — the canonical maturity framework that names design-time security activities (threat assessment, secure architecture, security requirements) as distinct disciplines that mature independently rather than as a single late-stage gate.

---

### 2. The OWASP Top 10 is a curriculum, not a checklist

The OWASP Top 10 lists categories of application-security failure — broken access control, cryptographic failures, injection, insecure design, security misconfiguration, and so on. Treating each entry as a single bug to fix and check off misses the point. These are not bugs; they are *categories*, and they appear at the top of the list because they recur across applications, decades, and technologies due to structural weaknesses in how the work is done. Broken access control isn't one bug — it's a thousand-bug pattern that comes from authorisation logic scattered through code. Cryptographic failures aren't one bug — they're the predictable result of letting application teams choose algorithms and manage keys. Reading the Top 10 as a curriculum means asking: *what structural property of our development would prevent this entire category from arising in our applications?*

#### Architectural implications

- Each OWASP category is mapped to a structural mitigation — not a list of tests, but a design choice that makes the category architecturally unlikely.
- The application's most attacked surfaces (authentication, authorisation, deserialisation, file uploads, integrations) get architectural attention proportionate to their risk.
- Recurring vulnerability classes in the team's history are treated as evidence of structural weakness — not as individual bugs that can be fixed in isolation.
- Security training for engineers focuses on understanding categories and their structural mitigations, not on memorising specific exploits.

#### Quick test

> Pick the OWASP Top 10 category that has produced the most bugs in your application's history. What changed structurally to make that category less likely after each bug? If the answer is "we fixed the bug" each time, the team is treating the category as a recurring tax instead of as a structural problem to design out.

#### Reference

[OWASP Top 10 — Application Security Risks](https://owasp.org/www-project-top-ten/) — read alongside the underlying [Common Weakness Enumeration (CWE)](https://cwe.mitre.org/) catalogue, which provides the deeper taxonomy of weakness types that produce the recurring categories.

---

### 3. Dependencies are a supply chain, and supply chains have security

Modern applications are mostly other people's code. A typical Node.js or Python service has hundreds to thousands of transitive dependencies — code from authors the team has never met, running in the same process, with the same access. Log4Shell, the *xz utils* backdoor, *event-stream*, *colors.js*, *ua-parser-js* — each demonstrated the same lesson: a dependency you never reviewed can compromise an application you carefully reviewed. The architectural response is to treat dependencies as a supply chain that requires its own controls: an inventory of what's depended on (SBOM), provenance for each artefact (signing, build attestations), continuous scanning for known vulnerabilities, and a process for responding when something is found. None of this is novel; what's novel is treating the supply chain as part of the application's security boundary rather than as someone else's problem.

#### Architectural implications

- Software Bill of Materials (SBOM) is generated for every build and stored alongside the artefact — not "we'll generate one if asked".
- Dependency provenance is verified through artefact signing (Sigstore, in-toto attestations) and supply-chain frameworks (SLSA levels) appropriate to the workload's sensitivity.
- Vulnerability scanning of dependencies happens continuously — at commit, at build, in registries, and in production — not as a one-off audit.
- A documented process exists for responding to a critical dependency disclosure — who's notified, how the team triages, what the SLA is — exercised before the next zero-day arrives.

#### Quick test

> Pick a critical dependency in your application — the one that, if compromised, would compromise the most. Who is its current maintainer, when was the last release, when was the last security audit, and how is its provenance verified? If those answers don't exist, the supply-chain security of that dependency rests on hope.

#### Reference

[SLSA — Supply-chain Levels for Software Artefacts](https://slsa.dev/) — the framework that names increasing levels of supply-chain integrity (build provenance, hermetic builds, two-party review) as a maturity ladder; [Sigstore](https://www.sigstore.dev/) and [CycloneDX](https://cyclonedx.org/) are the practical tooling that makes those levels operational.

---

### 4. Input validation is a perimeter; output encoding is a contract

Two distinct disciplines, repeatedly conflated, with different failure modes. Input validation rejects data that doesn't belong: malformed structure, out-of-range values, prohibited content, wrong type. It happens at the earliest point data enters trust — the application's perimeter. Output encoding ensures data is rendered safely in whatever destination it reaches: HTML-escape for browser context, parameterised queries for SQL context, shell-escape for command context, attribute-encode for XML/SVG context. It happens at the boundary between the application and the destination. The reason both are necessary: input validation cannot anticipate every destination context, and output encoding cannot remediate inputs that should never have been accepted at all. Conflating them — "we validate inputs so we don't need to encode outputs," "we encode outputs so we don't need to validate inputs" — produces injection vulnerabilities in production, which is what most of the OWASP Top 10's injection category amounts to.

#### Architectural implications

- Input validation happens at the perimeter (API boundary, form submission, message queue ingress) — not deep inside business logic where the perimeter has already been crossed.
- Output encoding is context-specific and applied at the rendering boundary — by the templating engine, query builder, command executor, or ORM that knows the destination grammar.
- Parameterised queries are mandatory for any SQL — string concatenation with user data is treated as a critical bug, not as an acceptable shortcut.
- Allow-lists (what is permitted) are preferred over deny-lists (what is forbidden) for input validation, because deny-lists fail to anticipate the next encoding the attacker will use.

#### Quick test

> Pick a user-input field in your application that flows to a SQL query, an HTML page, and a shell command (this is more common than it sounds). For each destination, what encoding or parameterisation is applied at the boundary? If the answer is "we sanitised the input once," the application has a single point of failure across three different injection categories.

#### Reference

[OWASP Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html) — the practical reference for context-specific output encoding, with each major destination grammar (SQL, HTML, OS command, LDAP, XPath) treated as a distinct encoding problem.

---

### 5. SAST, DAST, IAST, and runtime protection are complementary, not redundant

Each tool sees the application from a different angle and finds bugs the others cannot. SAST (Static Application Security Testing) reads source code without running it — it finds dangerous patterns (hard-coded secrets, dangerous function calls, taint flows) that are visible in static text but cannot find bugs that depend on configuration, deployment, or runtime state. DAST (Dynamic Application Security Testing) probes a running application from outside — it finds deployment and configuration bugs (open admin endpoints, missing security headers, weak authentication flows) but cannot see inside the code. IAST (Interactive Application Security Testing) instruments the running application — it sees both code and runtime, and finds bugs in the interaction that SAST and DAST each miss. Runtime protection (RASP, WAF) catches what made it past everything else and limits the blast radius. Pretending one replaces the others — usually because of cost or operational simplicity — is the most common reason production applications still ship with bugs that any of the four would have caught.

#### Architectural implications

- SAST runs on every commit, with rules tuned to the team's languages and frameworks; false positives are managed (suppressed with justification, not ignored), and findings are treated as bugs.
- DAST runs against every staging deployment with realistic configuration, exercising actual authentication and exercising the full surface — not only the unauthenticated endpoints.
- IAST or its functional equivalent (instrumentation, SCA inside the running app) is in place where the bug categories it uniquely catches matter to the workload.
- Runtime protection (WAF rules, RASP if appropriate) is configured deliberately — not "default rules from the vendor" but tuned to the application's actual risk profile.

#### Quick test

> Pick a recent application security finding that reached production. Which of the four — SAST, DAST, IAST, runtime protection — should have caught it, and why didn't it? If the answer is "we don't run that one," the gap is structural, not the result of bad luck.

#### Reference

[OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/) — the framework that names verification activities at each level (testing, scanning, review) with explicit recognition that no single tool covers the whole standard.

---

### 6. Threat modelling is a forcing function for clarity

The act of writing down what an attacker might want, how they might try to get it, and what would stop them — this exercise produces clarity that ad-hoc thinking cannot. STRIDE (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege) gives a structured way to ask the question. Attack trees give a structured way to decompose the answer. The output is not a comprehensive enumeration of every possible attack — it is a shared understanding of where the design is strong, where it is weak, and where the team has explicitly accepted risk. Without a threat model, security work is reactive: respond to the bugs that surface. With a threat model, security work is proactive: design for the threats the model predicts, and use the model to spot when reality has diverged from what was assumed.

#### Architectural implications

- Threat models are documented artefacts, kept current as the design evolves, and reviewed at major milestones — not napkin sketches that get lost after the meeting.
- The model names the attacker (insider, external attacker, compromised dependency, malicious tenant) as well as the assets and the controls — without an attacker, "threat model" becomes a list of nice-to-have features.
- Risks accepted explicitly (we know this is a weakness, the cost of mitigation exceeds the residual risk) are named in the model as accepted risks — not silently absorbed and forgotten.
- The model is used during incident response: when something happens, the question is "did the model predict this, and if not, what does the model need to change?" — turning every incident into a forcing function for the model itself.

#### Quick test

> Pick the most recent significant feature in your application. Where is the threat model for it, when was it last updated, and what risks does it explicitly accept? If those questions cannot be answered, the team is operating on the security threats they have already encountered, not on the threats the design implies.

#### Reference

[Microsoft — STRIDE Threat Modelling](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats) — the foundational treatment of structured threat modelling that introduced STRIDE; for deeper application practice, [Adam Shostack's *Threat Modelling: Designing for Security*](https://shostack.org/books/threat-modeling-book) is the canonical book-length treatment.

---

## Architecture Diagram

The diagram below shows a canonical secure-by-design application pipeline: design-time threat modelling feeds into the architecture; code is reviewed by SAST at commit; dependencies are tracked via SBOM and signed via Sigstore; running applications are probed by DAST and instrumented by IAST; runtime protection (WAF) sits at the edge; findings from every stage flow into a single triage backlog with documented SLAs.

---

## Common pitfalls when adopting application security

### ⚠️ Treating security as the security team's problem

The application team builds; the security team scans before launch and produces a list. The list arrives too late to influence design, often too late to influence release, and the team learns nothing about why the bugs exist. The cycle repeats with the next release.

#### What to do instead

Application security is the application team's responsibility, with the security team providing tooling, expertise, and second opinions — not gatekeeping. Threat modelling, code review, dependency hygiene, and remediation are part of the engineering work, not external to it.

---

### ⚠️ The unmaintained dependency

A critical library was added years ago, the original author has stopped maintaining it, and the team has not noticed. When a vulnerability is disclosed, no patch is forthcoming, and the team discovers the problem at the worst possible time.

#### What to do instead

Dependency hygiene includes tracking maintenance status — last release date, maintainer activity, alternative libraries — not only known CVEs. Unmaintained dependencies are migrated proactively, before the disclosure that forces the migration in a hurry.

---

### ⚠️ Sanitisation as a single chokepoint

A single "sanitise input" function is called everywhere user data is handled, then output is rendered without further encoding because "the input was already sanitised." The function cannot anticipate every destination context, and the bug is found when an attacker exercises a context that was missed.

#### What to do instead

Validate inputs at the perimeter for what they should be; encode outputs at the boundary for the destination context. The two are complementary disciplines, not interchangeable, and both must be present.

---

### ⚠️ Tool fatigue

Five overlapping security scanners are running, producing thousands of findings, with no one able to triage them. The team learns to ignore the dashboards, and real findings drown in the noise.

#### What to do instead

Tools are tuned for signal-to-noise. False positives are suppressed with documented justifications, not ignored silently. The triage process is owned, has SLAs, and feeds back into tool tuning when noise patterns are identified. Fewer well-tuned tools beat more noisy ones.

---

### ⚠️ Threat models as decoration

A threat model was produced at project kickoff and never touched again. The application has evolved substantially since; the model describes a system that no longer exists; nobody refers to it during design or incident response. The artefact exists but provides no protection.

#### What to do instead

Threat models are living documents — updated when the architecture changes, referenced when designing new features, used during incident response. The model that gets referenced is the model that gets maintained; the unreferenced model is decoration regardless of how good it was at creation.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Threat models are produced before significant features are built and updated as designs evolve ‖ Threat modelling at design time is dramatically cheaper than threat-finding after launch. The threat model is a living artefact, referenced during design and incident response — not a one-time deliverable for the launch checklist. | ☐ |
| 2 | Security requirements are explicit alongside functional requirements ‖ Authentication, authorisation, audit, data classification, residency, and threat-model-derived requirements are written down with the same rigour as functional ones. Without this, security requirements get deduced inconsistently by whoever happens to be implementing the feature. | ☐ |
| 3 | Default configurations are secure — TLS on, strict permissions, audit on, least-privilege ‖ The default state of any new component is the secure state. Insecure configurations require explicit justification and approval. The opposite (insecure default, secure on request) produces production deployments that drift toward whatever was easiest. | ☐ |
| 4 | Each OWASP Top 10 category is mapped to a structural mitigation, not a list of tests ‖ The recurring categories of failure are addressed at the design level — centralised authorisation, standardised cryptographic libraries, parameterised query layers — not as a series of bug fixes that resemble each other. | ☐ |
| 5 | Software Bill of Materials is generated for every build and stored alongside the artefact ‖ The SBOM is the source of truth for what's actually in the application; without it, dependency-vulnerability response degrades to guesswork. The SBOM is generated automatically and queryable, not produced manually on request. | ☐ |
| 6 | Dependency vulnerability scanning runs continuously — at commit, build, registry, and runtime ‖ Vulnerabilities are disclosed continuously; scanning continuously is the only way to catch the disclosure before exploitation. Single-point-in-time scanning leaves windows that adversaries find. | ☐ |
| 7 | Input validation happens at the perimeter; output encoding happens at the destination boundary ‖ Two complementary disciplines applied at the right layers, not conflated into a single chokepoint. Allow-lists preferred over deny-lists; parameterisation preferred over escaping where the destination supports it. | ☐ |
| 8 | SAST, DAST, and runtime instrumentation each run with tuned signal-to-noise ‖ Each finds bug categories the others miss. Tools are configured for actual languages, frameworks, and risk profile; false positives are managed; findings are tracked as bugs with documented severity. | ☐ |
| 9 | A documented response process exists for critical dependency disclosures ‖ Who's notified, how the team triages, what the SLA is — exercised before the next zero-day, not invented during one. The process names the people, channels, and decision authority. | ☐ |
| 10 | Security findings flow into a single triage backlog with documented SLAs by severity ‖ A finding without an owner and an SLA is decoration. Triage produces accept-risk, defer, or fix decisions with reasoning recorded; aged findings are escalated; backlog age is a metric. | ☐ |

---

## Related

[`patterns/security`](../../patterns/security) | [`security/authentication-authorization`](../authentication-authorization) | [`security/encryption`](../encryption) | [`security/vulnerability-management`](../vulnerability-management) | [`security/cloud-security`](../cloud-security) | [`technology/devops`](../../technology/devops)

---

## References

1. [OWASP Top 10](https://owasp.org/www-project-top-ten/) — *owasp.org*
2. [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/) — *owasp.org*
3. [OWASP Software Assurance Maturity Model (SAMM)](https://owaspsamm.org/) — *owaspsamm.org*
4. [SLSA — Supply-chain Levels for Software Artefacts](https://slsa.dev/) — *slsa.dev*
5. [Sigstore](https://www.sigstore.dev/) — *sigstore.dev*
6. [CycloneDX SBOM Standard](https://cyclonedx.org/) — *cyclonedx.org*
7. [Common Weakness Enumeration (CWE)](https://cwe.mitre.org/) — *cwe.mitre.org*
8. [Microsoft — STRIDE Threat Modelling](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats) — *learn.microsoft.com*
9. [OWASP Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html) — *owasp.org*
10. [NIST SP 800-218 — Secure Software Development Framework](https://csrc.nist.gov/publications/detail/sp/800-218/final) — *csrc.nist.gov*
