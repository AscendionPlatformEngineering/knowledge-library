# Cloud Security

The discipline of operating cloud workloads securely — recognising that the cloud changes which threats matter, which controls work, and which mistakes are catastrophic. The cloud is not on-premises with someone else's hardware; it is a different security regime with different failure modes.

**Section:** `security/` | **Subsection:** `cloud-security/`
**Alignment:** AWS Shared Responsibility Model | NIST SP 800-207 Zero Trust | CIS Benchmarks | AWS Well-Architected Security Pillar

---

## What "cloud security" actually means

A *transplanted* approach treats cloud security as on-premises security with new logos: firewalls become security groups, datacentre access controls become IAM policies, the perimeter moves from the WAN edge to the VPC edge, and the rest is roughly the same. This intuition produces predictably bad outcomes. The cloud's threat model is genuinely different: misconfiguration of a managed service can expose entire datasets without any code being written; an IAM key in a public repository can grant complete account access in seconds; the rate of change is too high for human review to be the primary control; the attack surface includes every API the cloud provider exposes, every region the account can deploy to, every service the team has not yet learned about.

A *cloud-native* approach to security accepts that the threats, the controls, and the operational cadence are different — and adopts patterns appropriate to the actual environment. The shared responsibility model is treated as a contract: what the provider secures, what the customer must secure, where the boundary sits. Misconfiguration is treated as the largest practical attack surface. IAM is treated with the seriousness due to anything that can deliver god-mode access in one stolen key. Detection requires cloud-aware tooling — CSPM for posture, CIEM for entitlements, CWPP for workloads, CNAPP for the integrated view. Automation is mandatory because the rate of change exceeds human review capacity. Account topology is a security boundary, not a billing convenience.

The architectural shift is not "we moved to the cloud." It is: **cloud security is a different discipline from on-premises security, with different threats, different controls, and different cadence — and treating it as a familiar problem with new vendors produces breaches that the classical security playbook would never have predicted.**

---

## Six principles

### 1. The shared responsibility model is contractual, not advisory

AWS, Azure, and GCP each publish a shared responsibility model that names what they secure and what their customers must secure. The exact line varies by service: for IaaS (raw VMs), the customer secures everything from the OS up; for managed databases, the provider secures the database engine but the customer secures the data, the schema, the access policy, and the network exposure; for SaaS, the customer secures only configuration and access. This boundary is a contract — what the provider commits to (often backed by their certifications: SOC 2, ISO 27001, FedRAMP, IRAP) and what the customer is responsible for (everything else). Most cloud breaches occur in the customer's portion of the model, often because the customer team did not know which portion they owned. The architectural discipline is: name the boundary explicitly for each service in use, ensure the customer-side controls are designed and implemented, and verify them through audit rather than assume them through trust.

#### Architectural implications

- The shared responsibility boundary is documented per service in use — what the provider secures, what the team must secure, what residual risk the team has accepted.
- Provider certifications are read and understood — they constrain which compliance regimes are achievable on which services in which regions.
- Customer-side controls (encryption keys, IAM, network configuration, audit logs, retention policies) are designed deliberately, not inherited as defaults.
- The boundary is reviewed when adopting new services — each new service has its own division of responsibility, and the team's prior understanding may not transfer.

#### Quick test

> Pick a managed service in your cloud architecture. What does the provider secure, what do you secure, and where is that boundary documented? If the team's understanding is "the provider handles the security stuff," the customer-side responsibilities are unowned by definition — and that's where the next breach lives.

#### Reference

[AWS Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/) — the canonical articulation; equivalents from [Microsoft (Azure)](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility) and [Google (GCP)](https://cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate) follow similar structures with provider-specific differences in service-level boundaries.

---

### 2. Misconfiguration is the largest cloud attack surface

Across published breach reports — Capital One, Microsoft Power Apps, the persistent S3 bucket leaks of 2017–2024, the SAS-token incidents of 2023 — the recurring pattern is misconfiguration of a managed service, not exploitation of a zero-day. Open S3 buckets, exposed databases without authentication, public-readable storage accounts, overly-permissive IAM policies, security groups with `0.0.0.0/0` left over from debugging — these mistakes are made every week, by every team, on every cloud. The cloud's velocity makes misconfiguration both easier (a single misclick in the console can expose a whole bucket) and more consequential (the misconfigured resource is reachable from the internet within seconds). The architectural response is to treat configuration as code with the same rigour as application code — version-controlled, reviewed, tested, and continuously validated against benchmarks.

#### Architectural implications

- Cloud resources are provisioned via Infrastructure as Code (Terraform, Pulumi, CloudFormation, Bicep) rather than via console clicks; the IaC is the source of truth.
- Configuration is reviewed before merge: human review for non-trivial changes, automated policy checks (OPA, Sentinel, AWS Config Rules) for known-bad patterns.
- Continuous compliance scanning runs against deployed state, with CIS Benchmarks, provider-specific best-practice rules, or organisation-specific policies as the standard.
- Configuration drift (the deployed state diverging from IaC) is detected and remediated as a security concern, not absorbed silently.

#### Quick test

> Pick the most data-sensitive service in your cloud account. Without checking, can you state whether it's publicly accessible, what encryption it uses, who has access, and when those settings were last reviewed? If those answers depend on logging into the console and clicking through screens, the configuration is being trusted rather than verified.

#### Reference

[CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks) — the canonical hardening guides for cloud platforms (AWS, Azure, GCP, Kubernetes), with specific configuration recommendations that are testable and version-controlled. Most CSPM tools encode CIS Benchmarks as their default ruleset.

---

### 3. IAM keys are god mode — and IAM at scale is exponentially more dangerous than on-prem identity

In an on-premises environment, a stolen administrator credential typically grants access to one system or one administrative domain. In a cloud account, a stolen IAM access key with broad permissions grants programmatic access to everything in that account: every database, every storage bucket, every running workload, every secret, every audit log (which can be deleted). The blast radius is qualitatively different. Furthermore, IAM at cloud scale produces tens of thousands of policy statements, hundreds of roles, dozens of cross-account trust relationships — far beyond what any human can review for least privilege. The architectural response is layered: prefer short-lived credentials over long-lived keys, prefer role assumption over key sharing, prefer just-in-time access over standing privilege, and use Cloud Infrastructure Entitlement Management (CIEM) tooling to detect over-privileged identities at scale.

#### Architectural implications

- Long-lived IAM access keys are eliminated where possible — replaced by IAM roles, IAM Roles for Service Accounts (IRSA), Workload Identity Federation, or OIDC-based workload identity for CI/CD.
- Where long-lived credentials are unavoidable, they are stored in dedicated secrets managers, rotated automatically, and never present in code, container images, or environment variables in plaintext.
- Just-in-time access (request, approval, time-bounded grant via tools like AWS IAM Identity Center, Azure PIM, or third-party JIT solutions) is preferred over standing administrative access.
- CIEM tooling continuously analyses effective permissions across identities, detects over-privilege (permissions granted but never used), and produces least-privilege recommendations.

#### Quick test

> Pick the most-privileged identity in your cloud account — the one whose compromise would do the most damage. How is it authenticated, what's its credential rotation cadence, and which permissions has it actually used in the last 90 days? If the answer is a long-lived access key with permissions far beyond what's used, the identity is a credential theft incident waiting to be triggered.

#### Reference

[AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) — the practical reference for least-privilege, short-lived credentials, and federation; the architectural arguments transfer to Azure RBAC and GCP IAM with provider-specific terminology.

---

### 4. Cloud-native threats need cloud-native detection

A traditional SIEM ingesting OS-level logs and network captures is structurally unable to catch most cloud-specific threats. A misconfigured S3 bucket leaving production data exposed for 60 days produces no SIEM-relevant signal — the bucket is operating exactly as configured, the configuration is just wrong. An IAM policy granting wildcard access produces no alert when used. An over-permissioned role being assumed by a compromised identity is an entirely cloud-API event that traditional tooling misses entirely. The cloud-security tooling stack has evolved to address this: CSPM (Cloud Security Posture Management) continuously scans configuration; CIEM (Cloud Infrastructure Entitlement Management) analyses identity entitlements; CWPP (Cloud Workload Protection Platform) protects running workloads; CNAPP (Cloud-Native Application Protection Platform) integrates the previous three with code-scanning and runtime protection. The architectural decision is not whether to adopt cloud-native security tooling — it is which subset, and how integrated.

#### Architectural implications

- CSPM is in place against the cloud accounts in scope, with CIS Benchmarks (or stricter) as the policy baseline; findings are tracked with documented SLAs.
- CIEM (or the equivalent native capability) analyses entitlements across cloud identities; over-privileged identities are flagged and reduced.
- CWPP protects running workloads (containers, VMs, serverless) with runtime detection appropriate to the workload type — not "we run an EDR agent."
- The relationship between cloud-security telemetry and the broader SIEM/SOC is deliberate — cloud-specific events flow into the SOC's incident response process, with the cloud-native tooling providing the cloud-aware enrichment the SIEM cannot.

#### Quick test

> Pick a misconfiguration that would be catastrophic in your environment (e.g., a publicly accessible production database, an IAM role with wildcard permissions). What tool would alert you to it within an hour, and how is that alert routed to the response team? If the answer involves "we'd notice when the breach hit the news," the cloud-security tooling is theoretical rather than operational.

#### Reference

[Gartner — Cloud-Native Application Protection Platforms (CNAPP)](https://www.gartner.com/en/information-technology/glossary/cloud-native-application-protection-platform-cnapp) — the analyst category that has consolidated CSPM, CIEM, and CWPP into integrated platforms; for the underlying components, vendor-neutral documentation and open-source projects (OpenCSPM, ScoutSuite, Prowler) provide hands-on understanding.

---

### 5. Cloud changes faster than humans — automation is mandatory

Cloud environments at production scale see thousands of configuration changes per day across hundreds of services. Manual review of every change is not optional automation — it is structurally impossible. Reviews that depend on a human security engineer reading every Terraform plan miss most changes by definition; reviews that approve everything in a hurry miss the bad ones along with the good. The architectural response is automation at every layer: policy-as-code prevents bad changes before they merge (Open Policy Agent, AWS CloudFormation Guard, Azure Policy, Sentinel); preventive controls block bad outcomes at runtime (Service Control Policies, Permission Boundaries, Azure RBAC denies); detective controls find what made it through; remediation playbooks fix issues automatically where the fix is well-understood. Humans review what the automation flags as significant, not the firehose of routine change.

#### Architectural implications

- Policy-as-code runs in CI/CD against IaC — bad patterns (overly permissive IAM, public storage, unencrypted resources, non-compliant tags) are caught before merge, not after deployment.
- Preventive controls (SCPs at AWS organisation level, Azure subscription policies, GCP organisation policies) block entire classes of bad outcomes regardless of what an individual account team configures.
- Auto-remediation (Lambda functions, Azure Automation runbooks, GCP Cloud Functions) responds to well-understood findings with bounded, audited fixes.
- Human review is reserved for changes that automation flags as ambiguous or significant — the team's review capacity is matched to what genuinely needs review.

#### Quick test

> Pick a class of cloud security finding that should never occur in your environment (e.g., public S3 buckets, IAM users with console access). What prevents it from being introduced via Terraform, what detects it if it appears in deployed state, and what automatically remediates it? If the answer is "we trust people to do the right thing," the control is not automated; humans are the security boundary, and humans tire.

#### Reference

[AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html) — the canonical reference for layered preventive, detective, and corrective automation patterns at AWS organisation scale; equivalents from Azure (Azure Landing Zones) and GCP (Security Foundations Blueprint) provide parallel guidance.

---

### 6. Multi-account topology is a security boundary

A flat single-account topology — production, development, staging, sandbox, and CI/CD all in the same AWS account or Azure subscription — produces a security blast radius that includes all of them. A compromised dev workload, a leaked CI/CD credential, an over-privileged developer's session — any of these can affect production data. The architectural response is to use the cloud's native multi-account topology (AWS Organisations with Organisational Units, Azure subscriptions and management groups, GCP folders and projects) as a security boundary: production isolated from non-production, sensitive workloads in dedicated accounts, central security and audit accounts protected by SCPs, cross-account access deliberate and audited. The topology is not about billing — it is about blast radius.

#### Architectural implications

- Multiple accounts/subscriptions/projects are used to separate environments, workloads of differing sensitivity, and shared services from tenant workloads.
- Service Control Policies (or equivalent) at the organisation level enforce invariants that no individual account can override (no public IAM users, no disabling CloudTrail, no specific high-risk regions).
- Cross-account access is deliberate, audited, and time-bounded where possible — not "developers have console access to production for emergencies."
- Centralised security tooling (audit log aggregation, CSPM, CIEM) operates across accounts via dedicated security accounts, not from within each workload account.

#### Quick test

> Pick a critical workload in your cloud environment. What other workloads share its blast radius — that is, what could a compromise of that workload's account or subscription affect? If the answer is "everything," the topology is providing no isolation, and the next compromise will be larger than it needs to be.

#### Reference

[AWS Organisations and Multi-Account Strategy](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/welcome.html) — the canonical reference for multi-account topology as a security boundary; the [Azure landing zone architecture](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/) and [GCP enterprise foundations blueprint](https://cloud.google.com/architecture/security-foundations) provide the parallel patterns for those clouds.

---

## Architecture Diagram

The diagram below shows a canonical multi-account cloud security topology: separate accounts for security tooling, audit logs, network shared services, and workloads of differing sensitivity; SCPs at the organisation level; CSPM and CIEM operating across accounts via the security account; centralised audit log aggregation; cross-account access mediated by IAM roles with explicit trust relationships.

---

## Common pitfalls when adopting cloud security

### ⚠️ The single root account

Everything lives in one cloud account: production, staging, development, CI/CD, security tooling. The blast radius of any compromise is the entire environment. The cloud provider's multi-account capabilities are unused.

#### What to do instead

Multi-account topology from the beginning, even at small scale. Production isolated from non-production. Security and audit in dedicated accounts. Workload accounts grouped by sensitivity or business unit. The topology is a one-time setup that pays back continuously.

---

### ⚠️ The long-lived access key

A developer or CI/CD system has an IAM access key with broad permissions, used for years, never rotated, possibly still in a Slack message or environment variable somewhere. When the key is eventually leaked or stolen, the cloud account is gone before anyone notices.

#### What to do instead

Long-lived keys are eliminated wherever the cloud provider supports the alternative: IAM roles for EC2/ECS/Lambda, IRSA for Kubernetes, Workload Identity Federation for cross-cloud, OIDC for CI/CD. Where long-lived keys are unavoidable, they are stored in secrets managers, rotated automatically, and audited continuously.

---

### ⚠️ Logs that nobody reads

CloudTrail, Activity Log, and Audit Logs are enabled and producing terabytes per day, stored in a bucket nobody queries. When an incident occurs, the team scrambles to figure out how to query the logs at all, often discovering retention limits, ingestion failures, or schemas that don't match documentation.

#### What to do instead

Log strategy is part of the architecture: what's collected, how it's aggregated, how it's queried, what alerts fire automatically. Detective controls (queries that detect known-bad patterns) are written and tested. The team queries logs routinely, not only during incidents — a query that hasn't been run since deployment will fail when it's needed.

---

### ⚠️ The "we'll do CSPM later"

The architecture is in place; CSPM is on the roadmap; the team will adopt it after the next release. Meanwhile, configuration drift accumulates, misconfigurations introduced under deadline pressure go unreviewed, and the next breach is incubating in plain sight.

#### What to do instead

Posture management is foundational, not a later phase. Even basic CSPM coverage (CIS Benchmarks, provider-native posture services like AWS Security Hub, Azure Defender for Cloud, GCP Security Command Center) catches the most common misconfigurations and is dramatically better than none. Mature posture management evolves over time; starting late is the failure mode.

---

### ⚠️ Trusting console permissions to substitute for governance

The team trusts that "only developers have console access" as the access-control story. In practice, console access is only one path; programmatic access via cached credentials, federated SSO sessions, IAM users, and assumed roles takes other paths. The "only developers" assertion is approximately true for one of the paths and irrelevant for the others.

#### What to do instead

Access governance covers all paths: console, API, CLI, federated SSO, programmatic credentials, cross-account roles. CIEM tooling produces the integrated view that ad-hoc thinking cannot. Policies are enforced at the most preventive layer (SCPs, permission boundaries) rather than relying on detective notice.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | The shared responsibility boundary is documented per service in use ‖ Without this, customer-side responsibilities are unowned by definition. The documented boundary makes the team's actual security responsibilities explicit and auditable. | ☐ |
| 2 | Cloud resources are provisioned via Infrastructure as Code, not console clicks ‖ IaC is the source of truth, version-controlled, reviewable, and testable. Console-driven configuration leaks into production untracked and produces drift that no audit can fully reconstruct. | ☐ |
| 3 | Continuous compliance scanning runs against deployed state with documented baselines ‖ CIS Benchmarks, provider-specific best practices, or organisation-specific policies as the baseline; deviations are tracked as findings, not absorbed as state. | ☐ |
| 4 | Long-lived IAM access keys are eliminated where the provider supports alternatives ‖ Roles, federated identity, OIDC for CI/CD, IRSA for Kubernetes — any of these reduces blast radius dramatically compared to a key in an environment variable. Where keys remain unavoidable, they are short-lived, automatically rotated, and never in code. | ☐ |
| 5 | Just-in-time access is preferred over standing privilege for high-impact operations ‖ Standing admin access is the highest-leverage credential to steal. JIT access (request, approve, time-bounded) raises the cost of compromise materially without harming productivity for the legitimate cases. | ☐ |
| 6 | CIEM tooling continuously analyses effective entitlements across identities ‖ Cloud IAM at scale exceeds human review capacity. CIEM produces the over-privilege findings, used-vs-granted analyses, and least-privilege recommendations that no human can produce manually. | ☐ |
| 7 | CSPM, CWPP, and CIEM coverage is in place — not "on the roadmap" ‖ Cloud-native threats need cloud-native detection. SIEM alone misses configuration drift, entitlement bloat, and runtime cloud-API events that traditional tooling cannot see. | ☐ |
| 8 | Policy-as-code prevents known-bad patterns at CI/CD time, not just at runtime ‖ The cheapest fix is the one that never gets merged. OPA, CloudFormation Guard, Azure Policy, Sentinel — any of these in the CI pipeline catches misconfigurations before they reach the cloud at all. | ☐ |
| 9 | Multi-account/subscription topology separates environments, workloads, and sensitivity ‖ The topology is a security boundary, not a billing convenience. Production isolated from non-production, sensitive workloads in dedicated accounts, security tooling centralised in protected accounts. | ☐ |
| 10 | Audit log aggregation is centralised, queryable, and used routinely — not just during incidents ‖ Logs that nobody reads have no security value. Detective queries are written, tested, and run continuously; incident response uses the same tooling that produced routine reports yesterday. | ☐ |

---

## Related

[`patterns/security`](../../patterns/security) | [`security/authentication-authorization`](../authentication-authorization) | [`security/encryption`](../encryption) | [`security/vulnerability-management`](../vulnerability-management) | [`technology/cloud`](../../technology/cloud) | [`technology/devops`](../../technology/devops)

---

## References

1. [AWS Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/) — *aws.amazon.com*
2. [AWS Well-Architected Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html) — *AWS*
3. [Microsoft — Azure Shared Responsibility](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility) — *learn.microsoft.com*
4. [Google Cloud — Shared Responsibility](https://cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate) — *cloud.google.com*
5. [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks) — *cisecurity.org*
6. [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) — *AWS*
7. [NIST SP 800-207 — Zero Trust Architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final) — *NIST*
8. [CSA Cloud Controls Matrix](https://cloudsecurityalliance.org/research/cloud-controls-matrix) — *cloudsecurityalliance.org*
9. [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html) — *AWS*
10. [AWS Organisations and Multi-Account Strategy](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/welcome.html) — *AWS*
