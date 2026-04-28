# Encryption

The discipline of using cryptography correctly — encrypting what should be encrypted, managing keys with operational rigour, choosing algorithms that survive the next decade, and recognising what encryption does and does not protect against.

**Section:** `security/` | **Subsection:** `encryption/`
**Alignment:** NIST FIPS 140-3 | TLS 1.3 (RFC 8446) | AES (FIPS 197) | NIST Post-Quantum Cryptography

---

## What "encryption" actually means

A *check-the-box* approach to encryption is widespread: TLS is on the front door, the database has "encryption at rest" enabled (typically by the cloud provider with a provider-managed key), backups are encrypted, and the architecture diagram has padlock icons in the right places. The *property* claimed is "data is encrypted." The *property* delivered is often weaker than that — keys are co-located with the data they protect, certificate rotation is manual and overdue, the algorithm in use was strong when it was chosen and is now showing its age, and crucially, "encryption" is being treated as a substitute for access control rather than a complement to it.

A *cryptographic engineering* approach treats encryption as one of several architectural disciplines, each with operational consequences. Data at rest, in transit, and in use each have specific patterns. Key management is recognised as harder than encryption — most cryptographic failures in practice are key-management failures. Algorithm choice is treated as having an expiration date, with crypto agility (the ability to swap algorithms when one ages out) as an architectural property rather than a future migration. Certificate lifecycle is operational discipline backed by automation. And the limits of encryption are clear: encryption hides data from those without keys, but does not validate that those *with* keys should have access at this moment to this data.

The architectural shift is not "we turned on encryption." It is: **cryptography is an operational discipline that requires deliberate architectural attention to keys, algorithms, certificates, and the boundary between what encryption guarantees and what other controls must provide — and pretending that "encryption is on" is the goal produces architectures that meet the compliance question and miss the security one.**

---

## Six principles

### 1. Encrypt by default — at rest, in transit, and in use

The default position in 2026 is that data is encrypted everywhere it lives and everywhere it moves; exceptions require justification rather than the inverse. *At rest*: storage-level encryption (disk, volume, object store, database) using strong symmetric algorithms (AES-256-GCM is the canonical choice). *In transit*: TLS 1.3 on every hop including internal service-to-service, not just at the perimeter. *In use*: emerging confidential-computing approaches (Intel SGX, AMD SEV-SNP, AWS Nitro Enclaves, Azure Confidential Computing) for workloads handling regulated or highly sensitive data. The cost of encryption-by-default has fallen dramatically — modern processors include AES instructions, TLS 1.3 has lower handshake overhead than 1.2, cloud providers offer encryption with provider-managed keys at no incremental cost — but the cost of *not* encrypting by default is paid in the breach where unencrypted data is found accessible to whoever found a way in.

#### Architectural implications

- All data at rest is encrypted with strong symmetric cryptography; "I don't think we need encryption here" is the position requiring explicit justification, not the default.
- All in-transit communication uses TLS 1.3 (or TLS 1.2 minimum where 1.3 is unavailable) with strong cipher suites; cleartext internal traffic is recognised as a vulnerability, not a performance optimisation.
- Mutual TLS (mTLS) is used for service-to-service communication where the threat model warrants it — typically the case for production workloads handling sensitive data.
- Confidential computing is evaluated for workloads handling data whose exposure to the cloud provider's operators is itself a risk (regulated data, sovereign workloads, threat models that include the host).

#### Quick test

> Pick a piece of sensitive data in your system. Trace its path from creation to consumption. At which hops is it in cleartext, and why? If "we trust the network" appears in the answer, that trust is a security boundary that the threat model needs to justify — and most current threat models will not.

#### Reference

[TLS 1.3 (RFC 8446)](https://datatracker.ietf.org/doc/html/rfc8446) — the canonical specification for the modern in-transit encryption protocol. For at-rest encryption, [AES (FIPS 197)](https://csrc.nist.gov/publications/detail/fips/197/final) remains the algorithmic foundation; the engineering question is not whether to use AES but how the keys are managed (see principle 2).

---

### 2. Key management is harder than encryption

AES is a solved problem. The implementations are vetted, the algorithm has held up against decades of cryptanalysis, and using it correctly is well-documented. The genuinely hard problem in cryptographic engineering is *key management*: where keys live, who has access to them, how they rotate, how they recover from compromise, how they are derived from one another, and how the chain of custody is maintained from generation through retirement. Most cryptographic failures in practice are not algorithmic — they are keys leaked into version control, keys with permissions broader than needed, keys never rotated, keys with no clear retirement path, keys generated by predictable random number generators, keys hard-coded into container images. The architectural response is to treat key management as a first-class discipline with its own infrastructure (KMS, HSM), its own operational runbooks (rotation, rekeying, recovery), and its own audit trail.

#### Architectural implications

- Keys live in dedicated key management infrastructure — cloud KMS (AWS KMS, Azure Key Vault, GCP KMS) for typical sensitivity, HSM (hardware security module) for higher-sensitivity workloads or compliance regimes that require it.
- Envelope encryption (data encrypted with a data key; the data key encrypted with a key-encryption key) is the standard pattern at scale — limits the exposure of the master key and enables efficient rotation.
- Keys have documented rotation cadences appropriate to their sensitivity; rotation is automated where possible and tested where not.
- Key recovery procedures (what happens if a master key is lost, compromised, or destroyed) are documented, rehearsed, and known to the team that would execute them under pressure.

#### Quick test

> Pick the master key for the most sensitive data in your system. Where does it live, who can access it, when was it last rotated, and what is the recovery procedure if it were destroyed today? If the answers depend on tribal knowledge, the key management is a single point of failure dressed up as security.

#### Reference

[NIST SP 800-57 — Recommendation for Key Management](https://csrc.nist.gov/projects/key-management/key-management-guidelines) — the foundational reference that treats key lifecycle (generation, distribution, storage, rotation, destruction) as a discipline distinct from the cryptographic algorithms the keys are used with.

---

### 3. Algorithms have expiration dates — crypto agility is an architectural property

Cryptographic algorithms are not eternal. SHA-1 was strong in 1995, deprecated by 2017, broken by 2020. MD5 was strong in 1992, broken by 2004, still in use in 2026 in places it should have been removed by 2010. RSA-1024 was strong in 2000, retired by 2010. Looking forward: practical quantum computers will break RSA and elliptic-curve cryptography (the algorithms behind most current public-key crypto) when they arrive at sufficient scale; "harvest now, decrypt later" attacks make data captured today vulnerable years before quantum computers actually exist. NIST's post-quantum cryptography programme has standardised replacements (CRYSTALS-Kyber for key encapsulation, CRYSTALS-Dilithium for signatures); migration will take years. The architectural response is *crypto agility* — designing systems where algorithms are configuration, not concrete, so the migration when it comes is a configuration change rather than a refactor.

#### Architectural implications

- Algorithm choices are abstracted from the application — code asks for "encrypt" / "sign" / "hash"; the cryptographic library provides the algorithm; the algorithm is configurable.
- Algorithm versioning is built in: new data uses the new algorithm, old data remains decryptable with the old algorithm during transition, eventual re-encryption is a planned process not an emergency.
- The team tracks the cryptographic news: deprecation announcements, broken algorithms, post-quantum readiness — at a cadence that produces deliberate migration rather than reactive scrambling.
- Post-quantum cryptography migration is on the architectural roadmap, not an item to consider when quantum computers arrive — the data being captured today is the data that will be vulnerable tomorrow.

#### Quick test

> Pick a cryptographic algorithm in use in your system today. If it were deprecated next year, how would you migrate to its replacement? If the answer involves changing application code, recompiling, and redeploying every service, the architecture is not crypto-agile and the next algorithmic crisis will be expensive.

#### Reference

[NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography) — the canonical reference for the upcoming algorithmic transition. The CRYSTALS-Kyber and CRYSTALS-Dilithium standards are now finalised; migration timelines vary by sensitivity but the work has begun in earnest.

---

### 4. Don't roll your own crypto — use vetted libraries

The temptation to implement cryptographic primitives yourself is the warning sign that you should not. Cryptographic implementations are subtle in ways that are not visible from algorithm specifications: timing attacks (where the time taken to perform an operation leaks information about the key), padding-oracle attacks (where an error message reveals whether decryption succeeded), IV reuse (where reusing an initialisation vector with the same key destroys the security guarantee), nonce-reuse vulnerabilities, side-channel attacks. Vetted libraries — OpenSSL/BoringSSL, libsodium, Tink, Bouncy Castle — have had decades of scrutiny and dedicated security work. Custom implementations, even of well-understood algorithms, have not. The architectural rule is unambiguous: use vetted libraries; if a library doesn't provide what you need, the answer is almost always to choose differently or use a library that does, not to write the primitive yourself.

#### Architectural implications

- Cryptographic primitives (encryption, signing, hashing, key derivation, random number generation) come from vetted libraries — never implemented bespoke.
- High-level cryptographic APIs (libsodium's crypto_secretbox, Tink's StreamingAEAD, Web Crypto API) are preferred over low-level primitives where they exist — they remove categories of misuse that low-level APIs allow.
- Random numbers used for cryptography come from the operating system's secure RNG (`/dev/urandom`, `getrandom()`, `CryptGenRandom`, language wrappers like `secrets.token_bytes`) — never from `Math.random()`, `rand()`, or other non-cryptographic sources.
- The team's cryptographic code is reviewed by someone with cryptographic background — not because review catches everything, but because it catches the most common misuse patterns.

#### Quick test

> Pick the cryptographic operations in your codebase. Are they all calls to a vetted library, or is there custom code that performs encryption, hashing, or key derivation? If custom cryptographic code exists, it is a vulnerability with high probability — the question is when, not if, the bug surfaces.

#### Reference

[libsodium documentation](https://doc.libsodium.org/) and [Google's Tink](https://developers.google.com/tink) — both are explicitly designed to be misuse-resistant, providing high-level APIs where the wrong choice is hard to make. For broader background, the [Cryptographic Right Answers](https://gist.github.com/tqbf/be58d2d39690c3b366ad) discussion from cryptographic engineers documents which primitives to use for which purposes.

---

### 5. Certificate lifecycle is operational discipline backed by automation

Every TLS-protected service has certificates. Every certificate has an expiry date. Manual certificate management at scale is a guaranteed source of outages — Microsoft, Equifax, LinkedIn, and many others have had major incidents caused by expired certificates. The architectural response is automation: ACME (RFC 8555) for issuance and renewal, services like Let's Encrypt or AWS Certificate Manager or cloud-native tooling like cert-manager for Kubernetes, monitoring of certificate expiry as a first-class operational signal, and Certificate Transparency monitoring for unauthorised issuance. The principle is straightforward: any process that depends on a human remembering to do something before a deadline will eventually fail; certificate lifecycle is exactly such a process, and the failure mode is a major outage.

#### Architectural implications

- Certificate issuance and renewal are automated via ACME or equivalent — humans set up the automation; the automation handles the operational reality.
- Certificate expiry is monitored with alerts at multiple thresholds (90 days, 30 days, 7 days remaining) routed to the responsible team — not a single alert at expiry-time minus a day.
- Certificate Transparency logs are monitored for issuance against the organisation's domains — unauthorised issuance is an early indicator of compromise.
- Internal PKI (for mTLS, internal service certificates, VPN certificates) is automated with the same rigour as public-facing certificates — internal expiry causes outages too.

#### Quick test

> Pick a certificate in your environment. When does it expire, who's responsible for renewing it, and what process renews it? If the answer involves a calendar reminder and a person who'll do it manually, the next expiry-driven outage is incubating.

#### Reference

[Let's Encrypt](https://letsencrypt.org/) and the [ACME protocol (RFC 8555)](https://datatracker.ietf.org/doc/html/rfc8555) — the canonical references for automated certificate issuance. [Certificate Transparency](https://certificate.transparency.dev/) is the complementary discipline for monitoring what certificates exist for the domains you care about.

---

### 6. Encryption hides data; it does not validate access

This principle is the most-violated in practice and the most-consequential when it is. Encryption ensures that data cannot be read by parties without the appropriate key. It does not ensure that the parties *with* the key are the ones who should have access at this moment to this particular piece of data. A database where every row is encrypted, with the application holding the decryption key, is encrypted to anyone who steals the disk — and unencrypted to anyone who steals the application's credentials or compromises the application's process. "Encryption at rest" provides protection against a specific threat model (physical disk theft, backup tape loss) and provides effectively no protection against the threat models that actually matter in cloud environments (compromised IAM credentials, application-level access). Encryption is necessary; it is rarely sufficient.

#### Architectural implications

- Encryption is layered with access control: who can request a decrypt operation, on which data, in which context, is governed by IAM and audit — not by possession of the data alone.
- Customer-managed keys (CMKs) where the cloud provider's operational access to the key is itself a threat in scope; provider-managed keys where it is not — the choice is deliberate.
- Audit logs of decrypt operations exist and are reviewed — encryption that does not log who decrypted what is encryption-without-accountability.
- The threat model names what encryption protects against and what it does not — disk theft, backup loss, network sniffing on one side; application compromise, credential theft, insider access on the other — and other controls address the threats encryption does not.

#### Quick test

> Pick "encryption at rest" in your most sensitive system. What threats does it protect against, and what threats does it not? If the answer is "it makes the data secure," the architecture is conflating encryption with access control — and the next breach will exploit the gap that conflation hides.

#### Reference

[NIST SP 800-111 — Storage Encryption Technologies](https://csrc.nist.gov/publications/detail/sp/800-111/final) — the practical reference that explicitly names which threats storage encryption addresses and which it does not, framing encryption as one component of a defence-in-depth strategy rather than as a complete control.

---

## Architecture Diagram

The diagram below shows a canonical cryptographic architecture: data is encrypted in transit with TLS 1.3 (mTLS for service-to-service); at rest with AES-256-GCM via envelope encryption; keys live in KMS/HSM with documented lifecycle; certificates are issued and renewed automatically via ACME; decrypt operations are logged and reviewable; the boundary between what encryption protects and what access control protects is named explicitly.

---

## Common pitfalls when adopting encryption thinking

### ⚠️ The illusion of "encryption at rest"

Storage-level encryption is enabled with provider-managed keys. The team checks the compliance box and considers data protected. In reality, anyone with cloud credentials that can read the storage object also has the key (transparently) — the encryption protects against disk theft and almost nothing else.

#### What to do instead

Match the encryption to the threat model. Provider-managed keys for low-sensitivity data; customer-managed keys (CMK) for sensitive data where provider access is itself a threat; client-side encryption for data where the cloud provider should never see plaintext. The choice is deliberate, not the default.

---

### ⚠️ Keys in the wrong places

Database connection strings with credentials in environment variables. AWS access keys in container images. SSH keys checked into Git. The team has good encryption *of* data but no discipline about the keys *to* the data — and the keys are easier to steal than the encrypted data.

#### What to do instead

Secrets management infrastructure (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager) for credentials. Key management infrastructure (KMS, HSM) for cryptographic keys. Secrets and keys never appear in code, config files, environment variables in plaintext, container images, or version control.

---

### ⚠️ The expired certificate outage

A certificate expires unexpectedly because the renewal process required a person who has since left the team, or a domain whose ownership has shifted, or a tool that has fallen out of use. Production goes down, the team scrambles, and the lesson learned is "we should automate that."

#### What to do instead

Automate certificate lifecycle from the beginning. ACME-based renewal where supported; cloud-managed certificates (ACM, Azure App Service Certificates, GCP-managed) where the cloud provider handles it; monitoring of expiry across all certificates the organisation depends on; alerts long before expiry — not the day of.

---

### ⚠️ "We use AES" without specifying mode

The team announces that data is encrypted with AES. They do not specify the mode (CBC, GCM, CTR), the key size, the IV strategy, or the integrity protection. AES-CBC without HMAC is malleable; AES-ECB leaks structure; AES-GCM with reused IVs catastrophically fails. "AES" alone tells you nothing about whether the encryption is secure.

#### What to do instead

Specify the full cryptographic construction: AES-256-GCM with random IVs, plus authenticated encryption with associated data (AEAD) — or use a high-level library (libsodium's crypto_secretbox, Tink) that makes these choices correctly without requiring the application team to re-make them.

---

### ⚠️ Treating encryption as a substitute for access control

The architecture's response to "make this data more secure" is "encrypt it more." Encryption is added in layers, but access controls — who can decrypt, when, with which audit — remain weak. The encrypted data is just as accessible to legitimate users as before, and to any attacker who reaches the legitimate user's permissions.

#### What to do instead

Encryption protects against specific threats; access control, audit, and detection protect against others. The threat model names which threats are addressed by which control. "Encrypt more" is not the answer to most security problems beyond the ones encryption was already addressing.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | All data at rest is encrypted with strong symmetric cryptography ‖ Encryption-by-default; "we don't need it here" requires explicit justification. The default position is that data is encrypted, with the encryption matched to the threat model the data faces. | ☐ |
| 2 | All in-transit communication uses TLS 1.3 (or 1.2 minimum) with strong cipher suites ‖ TLS at the perimeter is necessary but insufficient; service-to-service traffic in a modern threat model is also in-transit, also untrusted, and also requires TLS — often mTLS. | ☐ |
| 3 | Keys live in dedicated key-management infrastructure (KMS or HSM) ‖ Keys in environment variables, config files, or code are credentials, not keys — and they leak. KMS/HSM provides the operational primitives (rotation, audit, access control) that ad-hoc storage cannot. | ☐ |
| 4 | Envelope encryption is used at scale, not naïve direct encryption with a master key ‖ Master keys protect data keys; data keys protect data. The pattern limits master-key exposure, enables rotation without re-encrypting everything, and matches what KMS systems are designed to support. | ☐ |
| 5 | Cryptographic primitives come from vetted libraries — never implemented bespoke ‖ Custom cryptography is high-probability buggy. Vetted libraries (OpenSSL, libsodium, Tink, Bouncy Castle) have decades of scrutiny; bespoke implementations have not, and the misuse modes are subtle in ways that don't show up in functional testing. | ☐ |
| 6 | Algorithm choices are abstracted from application code — agility is built in ‖ Algorithms have expiration dates. Crypto agility (configurable algorithms, versioned data, planned migration) makes the inevitable algorithmic transitions a configuration change rather than an application rewrite. | ☐ |
| 7 | Certificate issuance, renewal, and monitoring are automated ‖ Manual certificate management at scale is an outage waiting to happen. ACME, cloud-managed certificates, and expiry monitoring at multiple thresholds turn certificate lifecycle into automation rather than vigilance. | ☐ |
| 8 | Decrypt operations are logged with sufficient detail for audit and detection ‖ Encryption without accountability is half a control. Audit logs of who decrypted what, when, and from where are what turn encryption into a real control rather than a compliance checkbox. | ☐ |
| 9 | The threat model names what encryption protects against and what it does not ‖ Encryption is necessary but rarely sufficient. Naming the threats it does and does not address forces the architecture to address the others through different controls — access management, audit, detection. | ☐ |
| 10 | Post-quantum cryptography migration is on the architectural roadmap ‖ Practical quantum computers are uncertain in date but certain in trajectory. "Harvest now, decrypt later" makes the data being captured today the data that will be vulnerable tomorrow. The migration takes years; starting now is starting in time. | ☐ |

---

## Related

[`patterns/security`](../../patterns/security) | [`security/application-security`](../application-security) | [`security/authentication-authorization`](../authentication-authorization) | [`security/cloud-security`](../cloud-security) | [`security/vulnerability-management`](../vulnerability-management) | [`patterns/data`](../../patterns/data)

---

## References

1. [TLS 1.3 (RFC 8446)](https://datatracker.ietf.org/doc/html/rfc8446) — *IETF*
2. [AES — FIPS 197](https://csrc.nist.gov/publications/detail/fips/197/final) — *NIST*
3. [NIST FIPS 140-3 — Cryptographic Module Validation](https://csrc.nist.gov/publications/detail/fips/140/3/final) — *NIST*
4. [NIST SP 800-57 — Key Management Recommendation](https://csrc.nist.gov/projects/key-management/key-management-guidelines) — *NIST*
5. [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography) — *NIST*
6. [Let's Encrypt](https://letsencrypt.org/) — *letsencrypt.org*
7. [ACME Protocol (RFC 8555)](https://datatracker.ietf.org/doc/html/rfc8555) — *IETF*
8. [Certificate Transparency](https://certificate.transparency.dev/) — *certificate.transparency.dev*
9. [libsodium](https://doc.libsodium.org/) — *doc.libsodium.org*
10. [Google Tink](https://developers.google.com/tink) — *developers.google.com*
