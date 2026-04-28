# Authentication and Authorization

The discipline of knowing *who* is making a request and *whether* they should be allowed to make it — two distinct problems that are repeatedly conflated, and whose conflation is responsible for a substantial fraction of the access-control bugs in production applications.

**Section:** `security/` | **Subsection:** `authentication-authorization/`
**Alignment:** OAuth 2.0 | OpenID Connect | SAML 2.0 | NIST SP 800-207 Zero Trust

---

## What "AuthN and AuthZ" actually means

A *combined* approach treats authentication and authorisation as a single concern: a user logs in, the application receives a token saying "this user is logged in," and access decisions are scattered throughout the code wherever they happen to be needed. The login flow is one problem; whether a particular user can perform a particular action on a particular resource is a thousand small problems, each handled independently. The architecture has identity but does not have access control as a coherent property — it has many small access-control judgements made in many places, each with its own assumptions about what the token contains and what the user can do.

A *separated* approach treats authentication and authorisation as two distinct disciplines. *Authentication* is establishing identity — verifying that the entity making a request is who they claim to be, with appropriate strength for the action being attempted. *Authorisation* is making access decisions — answering, for each request, whether *this principal* may perform *this action* on *this resource* in *this context*. The two have different lifecycles (authentication is occasional, authorisation is on every request), different protocols (federation for the first, policy for the second), and different failure modes. Treating them separately produces architectures where identity flows from a federated source, access decisions are centralised in a policy decision point, and the rest of the application asks "may this principal do this thing?" rather than computing the answer.

The architectural shift is not "we use OAuth." It is: **identity is established once via federation, access is decided per request via centralised policy, the session is protected as the most-attacked surface in the system, and the lifecycle of who-has-what is governed continuously — not "we set up auth at the beginning of the project."**

---

## Six principles

### 1. AuthN is *who*; AuthZ is *what* — different problems with different patterns

The most common architectural error in access control is conflating these. Authentication asks: is this entity who they claim to be? It happens once (or once per session) and produces an identity. Authorisation asks: should this identity be allowed to do this thing right now? It happens on every request, against every resource, in every context. The protocols differ — OIDC and SAML for authentication, RBAC and ABAC and ReBAC for authorisation. The architectural placement differs — authentication at the perimeter or via federation, authorisation as close as possible to the resource being protected. The cadence differs — authentication is expensive and infrequent, authorisation is cheap and constant. Building a single system that does both, deeply coupled, produces a brittle blob that resists the kind of change both disciplines require.

#### Architectural implications

- The application's entry points consume authenticated identity (a verified principal) and pass it to authorisation logic — not authentication credentials that authorisation logic re-verifies.
- Authorisation logic operates on identity, action, resource, and context — not on raw credentials, session tokens, or implementation details of the authentication mechanism.
- Failure modes are distinct: authentication failures (unknown user, bad credentials, expired session) and authorisation failures (known user, not permitted) produce different responses, different telemetry, and different remediation.
- Changes to authentication (adding MFA, switching IdPs, adopting passkeys) should not require changes to authorisation logic, and vice versa — the separation is what makes both evolvable.

#### Quick test

> Pick a recently added access check in your application. Is the check expressed in terms of *identity, action, resource, context* — or is it expressed in terms of session attributes, cookies, or token fields? If it's the latter, authorisation logic is reaching into authentication mechanism, and the two are coupled in ways that will resist change.

#### Reference

[NIST SP 800-162 — Guide to Attribute Based Access Control (ABAC)](https://csrc.nist.gov/publications/detail/sp/800-162/final) — the foundational treatment of authorisation as a separate discipline, with attributes (identity, environment, resource) as the inputs and access decisions as the output, distinct from the credential verification that produced the identity.

---

### 2. Identity is federated by default

Building your own identity system in 2026 is an architectural mistake. Federation protocols — OpenID Connect for users, SAML for enterprise SSO, OAuth 2.0 for delegated access — are mature, widely supported, and offload the hardest parts (credential storage, MFA, password recovery, account compromise detection) to identity providers whose entire business is doing those parts well. The remaining justification for "we'll build our own" is rarely technical — it's usually inertia, NIH bias, or a misunderstanding of what federation actually costs. The correct default is to integrate with an identity provider (a dedicated IdP like Auth0, Okta, Azure AD, AWS Cognito, or an internal IdP for an organisation that operates one) and consume identity claims from it. The application's job is to verify the claims and act on them, not to manage credentials.

#### Architectural implications

- The application accepts identity from a federated source via OIDC, SAML, or equivalent — it does not store or manage user passwords directly.
- Token verification (signature, issuer, audience, expiration) is performed at the edge or in middleware; authorisation logic consumes verified identity, not raw tokens.
- The IdP relationship has documented operational concerns: rotation of signing keys, handling of provider outages, claim mapping when the provider's schema changes.
- Multiple IdPs are accommodated for federation across organisations (B2B SSO, customer SSO, internal SSO) — the application doesn't assume a single identity authority.

#### Quick test

> Pick the authentication entry point in your application. Where are credentials verified, and what happens when the verifying system is unavailable? If credentials are verified inside the application against a database the application controls, it has chosen to operate its own identity system — and inherits all the responsibilities that come with one.

#### Reference

[OpenID Connect](https://openid.net/connect/) and [OAuth 2.0](https://oauth.net/2/) — the canonical specifications for federated authentication and delegated authorisation. For enterprise contexts, [SAML 2.0](https://en.wikipedia.org/wiki/SAML_2.0) remains widely deployed and worth understanding even when newer protocols are preferred for new work.

---

### 3. Access decisions belong at a Policy Decision Point — not scattered through code

The pattern of `if (user.role === 'admin')` checks scattered throughout the codebase is the access-control equivalent of input sanitisation scattered through application code: it produces inconsistencies, hard-to-audit behaviour, and bugs that hide in the gaps between checks. The alternative is a Policy Decision Point — a single component, library, or service — that answers the question: "may *principal P* perform *action A* on *resource R* in *context C*?" The application calls the PDP wherever an access decision is needed; the PDP encodes policy centrally; the policy is auditable, testable, and changeable without hunting through application code. The PDP can be a library (in-process), a sidecar (Open Policy Agent), a managed service (AWS IAM, Cedar policy engine), or a custom component — what matters is that there is *one place* the access policy lives.

#### Architectural implications

- Access decisions in the application are calls to the PDP, not direct examinations of identity attributes; the PDP is the only component that understands the policy.
- Policies are written in a declarative language (Rego, Cedar, custom DSL) — testable independently, version-controlled like code, and reviewable by both engineering and security.
- The policy distinguishes coarse-grained access (can this principal use this service at all?) from fine-grained access (can this principal modify this specific record?) — both are within scope.
- Audit logs record both the access request and the PDP's decision (with reasoning), producing an evidence trail for compliance and incident response.

#### Quick test

> Pick a non-trivial access rule in your application — something more nuanced than "is the user an admin?" Where is that rule expressed, and how do you change it? If the rule lives in application code interleaved with business logic, the policy is implicit, untestable, and dispersed; changing it requires hunting and praying.

#### Reference

[Open Policy Agent](https://www.openpolicyagent.org/) — the canonical open-source PDP, with a declarative policy language (Rego), a library/sidecar/server deployment model, and broad ecosystem support. The architectural pattern (decouple policy from application code) predates OPA but OPA made it operational at production scale.

---

### 4. The session is the most-attacked surface in the system

Once a user is authenticated, the session token they carry effectively *is* their identity for the lifetime of the session. Steal the session token, become the user. Every attack that doesn't bother breaking the password instead targets the session: session fixation (attacker plants a known token), session hijacking (attacker steals a live token), CSRF (attacker uses a victim's session indirectly), token replay (attacker reuses an old token before it expires). The architectural response is a layered set of session protections: cryptographically strong tokens, short-lived access tokens with refresh, transport security (TLS only, Secure flag, HttpOnly, SameSite), CSRF protection (double-submit, SameSite=Lax/Strict, custom header verification), token binding to context (TLS channel, optionally device or location), and clear logout semantics that revoke server-side state. None of this is novel; what's novel is treating session security as architecturally significant rather than as an implementation detail.

#### Architectural implications

- Session tokens are cryptographically strong (sufficient entropy, bound to a verified identity, signed if structured) — not predictable, sequential, or guessable.
- Access tokens are short-lived (minutes to hours); refresh tokens, when used, are bound to clients and revocable; long-lived bearer tokens are reserved for service-to-service contexts with appropriate compensating controls.
- Cookie attributes are set correctly: `Secure`, `HttpOnly`, `SameSite=Lax` or `SameSite=Strict` as appropriate to the cross-site behaviour the application requires.
- CSRF protection is in place for state-changing requests — through SameSite, double-submit tokens, custom headers, or origin checks — chosen deliberately for the application's architecture.
- Logout, password change, and detected compromise all revoke server-side session state — not "remove the cookie and hope."

#### Quick test

> Pick the session implementation in your application. What is the token lifetime, what makes it cryptographically strong, and what happens server-side when a user clicks "log out"? If the token is long-lived, predictable, or logout is "delete the cookie client-side," the session is the system's weakest link, regardless of how strong the authentication is.

#### Reference

[OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) — the practical reference covering token strength, lifetime, transport, CSRF, and logout — each treated as a distinct control with documented failure modes.

---

### 5. MFA is the single highest-leverage control in identity security

Across multiple large-scale studies (Microsoft, Google, Cisco), multi-factor authentication blocks somewhere around 99% of account-compromise attempts. No other identity control has this combination of low cost, broad applicability, and large impact. The architectural decision is not whether to support MFA — modern federation protocols make it cheap to add — but whether to *require* MFA for sensitive actions, *all* user accounts, *administrative* access, *every* internet-exposed login. The maturing answer in 2026 is: yes, by default, with phishing-resistant factors (passkeys, FIDO2) preferred over phishing-vulnerable ones (SMS, time-based codes), and step-up MFA for elevated actions even within authenticated sessions.

#### Architectural implications

- MFA is required for all administrative and privileged access — without exception, including break-glass accounts which use stronger factors and stricter audit.
- Phishing-resistant factors (passkeys/WebAuthn, FIDO2 hardware tokens) are the preferred second factor; SMS and TOTP are fallback options recognised as weaker.
- Step-up authentication is implemented for sensitive actions (financial transactions, permission changes, data export) — the user re-authenticates within the session before the action proceeds.
- Recovery flows for lost factors are designed deliberately: weak recovery undermines strong MFA, strong recovery preserves the security guarantee.

#### Quick test

> Pick the highest-privilege account in your system. What factors are required to authenticate it, and what is the recovery process if those factors are lost? If the recovery process is weaker than the primary authentication, the recovery process is the actual security boundary.

#### Reference

[FIDO Alliance — FIDO2 / WebAuthn](https://fidoalliance.org/fido2/) — the canonical reference for phishing-resistant authentication. For the broader case for MFA's effectiveness, [Microsoft's research on identity attack mitigation](https://www.microsoft.com/en-us/security/blog/2019/08/20/one-simple-action-you-can-take-to-prevent-99-9-percent-of-account-attacks/) documents the empirical 99.9% blocked-attack figure that has held up across multiple replications.

---

### 6. Identity governance is a lifecycle, not a project

People join the organisation, change roles, take on temporary responsibilities, leave. Each transition implies an identity action: provision access at hire, adjust at role change, deprovision at departure. Without automation, these actions happen manually — sometimes — and access accumulates over years. The senior engineer who joined as a junior contractor, became a contractor lead, became a permanent employee, became a team lead, became a manager — that person's account often retains every permission ever granted, including permissions the original role required and the current role doesn't. This *standing access creep* is one of the most-exploited weaknesses in mature systems, because every long-tenured account has more access than any current attacker would receive newly. Joiner-Mover-Leaver automation is the discipline; without it, the organisation has identity hygiene that depends on individual managers remembering to file access removal tickets.

#### Architectural implications

- Joiner-Mover-Leaver workflows are automated: HR or IdP events trigger access provisioning, adjustment, and deprovisioning without manual ticketing.
- Access reviews are recurring — quarterly or annual — with managers attesting to their reports' access; expired or unused permissions are revoked.
- Just-in-time access (request, approval, time-bounded grant) is preferred over standing access for high-privilege actions; the standing access list is reviewed and minimised.
- Service-account identity is governed with the same rigour as human identity — service accounts that exist forever with permissions nobody remembers are equally dangerous, and often less monitored.

#### Quick test

> Pick a long-tenured employee in your organisation. Without asking them, can you produce the list of all access they currently have? When was that list last reviewed against their current role? If the answer is "we'd need to query several systems and we haven't reviewed it," the organisation has standing-access creep that an attacker who compromises the account would inherit in full.

#### Reference

[NIST SP 800-63 — Digital Identity Guidelines](https://pages.nist.gov/800-63-3/) — the broader framework for identity assurance levels, lifecycle management, and the operational discipline that translates principle into running systems.

---

## Architecture Diagram

The diagram below shows a canonical AuthN/AuthZ topology: a federated identity provider issues OIDC tokens after authenticating users (with MFA enforced); the application verifies tokens at the edge; access decisions are delegated to a Policy Decision Point that consumes the verified identity, the requested action, and the resource; an Identity Governance system manages provisioning, deprovisioning, and access reviews across the lifecycle.

---

## Common pitfalls when adopting AuthN/AuthZ thinking

### ⚠️ The role explosion

RBAC starts simple — Admin, User, Guest — and over years grows to hundreds of roles, each with subtle differences, each created when someone needed access that didn't fit existing roles. Eventually the role taxonomy is incomprehensible, role assignment is guesswork, and the principle of least privilege is unenforceable.

#### What to do instead

When roles proliferate beyond comprehension, attribute-based access control (ABAC) or relationship-based access control (ReBAC) is usually the right answer — granting access based on attributes of the principal and resource, or relationships between them, rather than role names. The transition is non-trivial; the alternative is a role taxonomy nobody understands.

---

### ⚠️ Authorisation in the front-end

The UI hides menu items and disables buttons based on the user's role. The back-end accepts whatever request arrives without revalidating. An attacker who edits the UI or calls the API directly bypasses the authorisation entirely.

#### What to do instead

Authorisation is a back-end concern, enforced on every request the back-end receives. The front-end may *additionally* hide UI elements for usability, but the back-end never trusts the front-end's enforcement. Front-end enforcement is presentation, not security.

---

### ⚠️ The unbounded session

A session token, once issued, is valid until the user explicitly logs out — which they rarely do. A user who logs in from a public computer and walks away has left a session active that the next person can use. Long-lived tokens stolen via XSS or device compromise remain valid until manually revoked, often weeks later.

#### What to do instead

Sessions have explicit lifetimes. Idle timeouts (revoke after inactivity) and absolute timeouts (revoke after a maximum lifetime regardless of activity) are both in place. Re-authentication is required for sensitive actions. Revocation propagates server-side — a logout actually invalidates the session, not merely deletes the cookie.

---

### ⚠️ The exception that becomes the rule

A break-glass admin account is created for emergency access; over time, "emergencies" become routine, and the account is used regularly without the audit and approval that emergencies originally required. The principle of least privilege has been replaced by convenience.

#### What to do instead

Break-glass access has stricter controls (stronger MFA, time-bounded, multi-person approval, audited) than routine access. Each use is reviewed; routine use is recognised as policy drift and addressed by adjusting the regular permissions structure, not by normalising emergency access.

---

### ⚠️ Identity sprawl

The organisation has Active Directory, Okta, Auth0, Cognito, several SCIM endpoints, and three different SSO configurations across products. Identity is "federated" in the sense that everything talks to something, but no one has a coherent picture of who has access to what across the system as a whole.

#### What to do instead

A single source of truth for identity exists, even when multiple systems consume it. Provisioning and deprovisioning flow from that source. Access reviews can answer "what does *this person* have access to across everything?" — and the answer comes from one query, not from collation across systems.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Authentication and authorisation are architecturally separated — different protocols, different placement, different evolution paths ‖ The two disciplines have different cadences, failure modes, and change patterns. Coupling them produces a single brittle blob; separating them lets each evolve independently and makes the access-control story comprehensible. | ☐ |
| 2 | Identity is consumed from a federated provider via OIDC, SAML, or equivalent ‖ The application is not in the password-management business. Federation offloads credential storage, MFA, and account-compromise detection to providers whose entire business is doing those well. | ☐ |
| 3 | Access decisions are made at a Policy Decision Point — not scattered through application code ‖ Policy is centralised, declarative, testable, and version-controlled. Application code calls the PDP; the PDP returns allow or deny; the policy is auditable as a single artefact. | ☐ |
| 4 | Session tokens are short-lived, cryptographically strong, and revocable server-side ‖ Sessions are the most-attacked surface. Short lifetimes limit blast radius; cryptographic strength resists guessing; server-side revocation makes logout actually log out. | ☐ |
| 5 | Cookie attributes (Secure, HttpOnly, SameSite) and CSRF protection are correct for the application's cross-site behaviour ‖ Defaults are not always right; the application's actual cross-origin requests determine the correct settings. SameSite=Lax/Strict, Secure on TLS, HttpOnly to resist XSS theft, CSRF tokens or origin checks for state-changing requests. | ☐ |
| 6 | MFA is required for all administrative and privileged access ‖ The single highest-leverage control. Phishing-resistant factors (passkeys, FIDO2) preferred over phishing-vulnerable ones (SMS, TOTP). Recovery flows are at least as strong as the primary authentication. | ☐ |
| 7 | Step-up authentication is implemented for sensitive actions within authenticated sessions ‖ Not every action within a session deserves the same level of trust. Sensitive operations (financial transactions, permission changes, data export) re-prompt for authentication, raising the bar specifically for high-impact actions. | ☐ |
| 8 | Joiner-Mover-Leaver workflows are automated, triggered by HR or IdP events ‖ Manual provisioning produces standing-access creep over time. Automated lifecycle workflows produce identity hygiene as a property of the system, not as a result of individual manager diligence. | ☐ |
| 9 | Access reviews are recurring, with managers attesting to their reports' access ‖ Without periodic review, access only grows. Reviews force the question — "does this person still need this?" — that ad-hoc reasoning never asks. | ☐ |
| 10 | Authorisation decisions are logged with reasoning — not only allow/deny outcome but the policy that produced it ‖ Audit logs that record only outcomes are insufficient for incident response, compliance, or debugging. Logging the policy and the inputs that produced the decision turns audit logs into useful evidence. | ☐ |

---

## Related

[`patterns/security`](../../patterns/security) | [`security/application-security`](../application-security) | [`security/cloud-security`](../cloud-security) | [`security/encryption`](../encryption) | [`patterns/integration`](../../patterns/integration) | [`technology/cloud`](../../technology/cloud)

---

## References

1. [OpenID Connect](https://openid.net/connect/) — *openid.net*
2. [OAuth 2.0](https://oauth.net/2/) — *oauth.net*
3. [SAML 2.0 (Wikipedia)](https://en.wikipedia.org/wiki/SAML_2.0) — *Wikipedia*
4. [Open Policy Agent](https://www.openpolicyagent.org/) — *openpolicyagent.org*
5. [FIDO Alliance — FIDO2 / WebAuthn](https://fidoalliance.org/fido2/) — *fidoalliance.org*
6. [NIST SP 800-63 — Digital Identity Guidelines](https://pages.nist.gov/800-63-3/) — *NIST*
7. [NIST SP 800-162 — ABAC Guide](https://csrc.nist.gov/publications/detail/sp/800-162/final) — *NIST*
8. [NIST SP 800-207 — Zero Trust Architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final) — *NIST*
9. [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) — *owasp.org*
10. [JWT — Introduction](https://jwt.io/introduction) — *jwt.io*
