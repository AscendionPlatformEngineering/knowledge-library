# Cloud-Native Principles

Architecture for systems that take advantage of what cloud platforms actually provide — elastic scaling, declarative orchestration, runtime observability, supply-chain integrity — rather than running on the cloud the same way they would have run in a data centre.

**Section:** `principles/` | **Subsection:** `cloud-native/`
**Alignment:** Twelve-Factor App | CNCF Cloud Native | Site Reliability Engineering | SLSA

---

## What "cloud-native" actually means

A *cloud-portable* application is one that runs anywhere by avoiding everything cloud-specific. The architecture is lowest-common-denominator: a stateful process on a VM, indifferent to whether it sits in a data centre or a managed kubelet. The cloud doesn't really do anything for it.

A *cloud-native* application is designed to take advantage of what the cloud actually provides: managed backing services, elastic scaling, declarative orchestration, runtime observability, supply-chain integrity. It cannot run as a single process with local state because it is not supposed to. The properties of the cloud — reliability, scalability, security at runtime — are architectural commitments, not features bolted on.

The [Twelve-Factor App](https://12factor.net/) (Heroku, 2011) was the precursor: a set of app-design principles for the early PaaS era — codebase, dependencies, config, processes, port binding, logs as streams. Cloud-native still rests on those principles, but the umbrella is much larger:

- **Twelve-Factor** answers: *how should I structure an application so it is portable and operationally sane?*
- **Cloud-native** answers: *how should I build and run software so that the platform, the operations, and the supply chain are part of the architecture?*

A useful mental model:

- **Twelve-Factor** = application design principles
- **Cloud-native** = application + runtime + operations + platform principles

Twelve-Factor stays relevant — every cloud-native app should pass it. But cloud-native also covers Kubernetes, service meshes, autoscaling, supply-chain security, and the discipline of distributed-systems operations — concerns Twelve-Factor never fully addressed because they did not yet exist as engineering practices.

The architectural shift is: **the platform owns infrastructure concerns; the application owns capability. Together, with operations as a first-class engineering discipline, they deliver outcomes the application alone never could.**

---

## Six principles

### 1. Application state lives in backing services; processes are ephemeral

Cloud infrastructure is elastic and disposable: instances start, stop, drain, terminate, get evicted, get rescheduled, fail. Applications that hold state in memory or on local disk lose data when the container dies and cannot scale horizontally because each replica holds different state. The cloud-native shape is the opposite: every persistent thing lives in a named backing service (database, cache, object store, message broker), and the application processes are interchangeable.

#### Architectural implications

- All persistent state lives in backing services. Local disk is treated as scratch space; nothing important is written to it.
- Backing services are connected via URL/credentials drawn from configuration — they can be swapped without code changes.
- Sessions are external (Redis, JWT, signed cookies) so any pod can serve any user.
- Replicas are interchangeable. If you can't kill any single pod without users noticing more than a brief reconnect, the application has illicit state.

#### Quick test

> Roll a die. Kill that-numbered replica without warning. If anything other than a brief reconnect happens — if you lose work-in-progress, log a customer out, or leave an order half-written — the application is holding state it should not be.

#### Reference

[Twelve-Factor App, factor #6 (Processes)](https://12factor.net/processes) and [#4 (Backing services)](https://12factor.net/backing-services). The ephemerality contract is what makes elastic scaling possible at all.

---

### 2. Configuration is environment, not binary

Cloud-native applications move between environments constantly: dev, staging, prod, canary, multiple regional clones, blue/green pairs. The same image must run in each — what differs is configuration: connection strings, feature flags, region, scale, secrets. If those differences live in the binary, every environment requires a rebuild. If they live in the environment, the image becomes the immutable artifact and the operating environment becomes the customisation layer.

#### Architectural implications

- No environment-specific values are baked into the binary or container image.
- Configuration flows in from environment variables, mounted ConfigMaps, mounted Secrets, and platform service discovery.
- The same image that ran in dev is the image that runs in prod — promotion is a label change, not a rebuild.
- Secrets are managed by the platform (Kubernetes Secrets, AWS Secrets Manager, HashiCorp Vault), never committed to source.

#### Quick test

> Can you deploy the same container image into a brand-new region with only configuration changes — no rebuild, no patch, no recompile? If the answer is no, configuration has leaked into the binary and the architecture is no longer environment-agnostic.

#### Reference

[Twelve-Factor App, factor #3 (Config)](https://12factor.net/config). Cloud-native extends this with declarative configuration objects (ConfigMaps, Secrets) that the platform mounts at runtime.

---

### 3. The platform owns infrastructure; the application owns capability

This is the largest delta between Twelve-Factor and cloud-native thinking. Twelve-Factor was designed for the early PaaS era when the platform was simple and the application carried most of the operational burden. Cloud-native inverts this: the platform — Kubernetes, service mesh, ingress controllers, autoscalers, operators — does the operational heavy lifting. Applications publish their requirements declaratively and the platform satisfies them. Applications stop trying to manage their own load balancers, TLS rotation, service discovery, or pod placement; the platform does it better and more uniformly than each application could.

#### Architectural implications

- Applications do not manage their own load balancers, TLS termination, service discovery, or rate limiting — the platform does.
- Health, readiness, and startup probes are how the application communicates fitness to the platform. They are first-class architectural concerns.
- Applications publish their needs declaratively (resource requests, network policies, scaling thresholds, traffic policies); the platform reconciles them.
- "Deploy" means "give the platform a manifest" — not "run scripts on servers" or "SSH in and restart something".

#### Quick test

> Can a brand-new engineer describe what your platform does for you on a single page — autoscaling rules, traffic shaping, secret mounting, health-check semantics? If the answer is "the platform team handles it" without further detail, the platform has become a black box and the application team cannot reason about its own runtime.

#### Reference

[Kubernetes Documentation — Concepts](https://kubernetes.io/docs/concepts/) and the [CNCF Cloud Native Definition](https://github.com/cncf/toc/blob/main/DEFINITION.md). The platform as the architectural substrate is the defining cloud-native commitment.

---

### 4. Failure is the default; resilience is the design

Cloud infrastructure has many more failure modes than monolithic on-prem deployments. Network partitions, transient timeouts, AZ-level events, pod evictions, slow neighbours, regional capacity limits — these are not exceptional, they are routine. Applications that assume reliable calls and instant responses break under load, often in ways that propagate across the entire system. Cloud-native applications assume failure as the default and design retries, timeouts, circuit breakers, idempotency, and graceful degradation explicitly.

#### Architectural implications

- Every external call has an explicit timeout, retry policy with exponential backoff, and circuit breaker.
- State-changing operations are idempotent — retries cannot duplicate orders, double-charge customers, or send the same notification twice.
- Each dependency has a documented graceful-degradation path: what does the app do when this service is slow, down, or returning errors?
- Chaos experiments run continuously in production-like environments, not as a quarterly drill.

#### Quick test

> Block the application's connection to its primary database for thirty seconds in a non-production environment. Does the system fail loudly with clear errors and recover cleanly? Or does it cascade — slow, then timeout, then crash, then take its callers down? If the answer is "we've never tried that," resilience hasn't been verified.

#### Reference

[The Reactive Manifesto](https://www.reactivemanifesto.org/) names the underlying properties (responsive, resilient, elastic, message-driven). [Site Reliability Engineering (Google)](https://sre.google/sre-book/table-of-contents/) provides the operational practices.

---

### 5. Observability is a property of the system, not an addition to it

A cloud-native system has many small moving parts — pods, services, queues, caches, sidecars, controllers. When something goes wrong, the engineer cannot reproduce the issue locally and cannot debug from a single log file. The system must emit enough structured signal that any incident can be reconstructed from telemetry alone. That requires three things designed in from the start, not bolted on after an outage: structured logs, metrics, and distributed traces. SLOs (service-level objectives) drive what to alert on so the team is woken only by what actually matters to users.

#### Architectural implications

- Every service emits structured logs (typically JSON), metrics (Prometheus or equivalent), and distributed traces with propagated context across all service boundaries.
- Trace context (request IDs, span IDs) flows through every internal call, every backing-service call, every async hand-off.
- SLOs are defined for every user-facing capability, with error budgets that explicitly govern release pace.
- Dashboards, runbooks, and alert rules are part of the deliverable for every service — not a follow-up ticket after launch.

#### Quick test

> Pick a recent incident. Could it have been diagnosed entirely from telemetry, or did the team have to add logging, redeploy, and reproduce? If observability had to be retrofitted to debug, it wasn't a property of the system — it was an absence.

#### Reference

[OpenTelemetry Documentation](https://opentelemetry.io/docs/) provides the modern instrumentation standard. [Observability (software systems)](https://en.wikipedia.org/wiki/Observability_(software)) covers the conceptual underpinnings.

---

### 6. Build artefacts are immutable; the supply chain is architecture

The container image is the unit of deployment. It is built once and deployed many times; it is never modified after build. Everything that goes into the image — base layers, dependencies, build tooling — is part of the runtime architecture and part of the security and reliability surface. A vulnerability in a base layer is a vulnerability in production. A compromised dependency is a compromised system. Cloud-native applications treat the supply chain itself as something that must be designed, signed, and verified, not just consumed.

#### Architectural implications

- Container images are built once; promotion across environments is a tag change, never a rebuild.
- Every image has a Software Bill of Materials (SBOM) recording every dependency and base layer.
- Images are signed at build; signatures are verified at admission. Unsigned images cannot deploy.
- Base images are pinned, scanned regularly, and rebuilt on a schedule — not "whenever we remember".

#### Quick test

> Take a production container image at random. Can you produce its SBOM, verify its signature, and trace every layer back to a known build pipeline within fifteen minutes? If not, the supply chain is not architecture — it is opaque cargo.

#### Reference

[SLSA — Supply-chain Levels for Software Artifacts](https://slsa.dev/) is the industry-standard framework for build-pipeline integrity. The [CNCF Cloud Native Landscape](https://landscape.cncf.io/) catalogues the tools that operationalise it.

---

## Architecture Diagram

The diagram below shows the canonical cloud-native runtime: stateless application pods sit on a managed platform that handles ingress, service mesh, and autoscaling; backing services hold all persistent state; configuration and secrets are mounted at runtime; signed container images flow in from the supply chain; and observability telemetry flows out continuously to drive SLO measurement.

---

## Common pitfalls when adopting cloud-native thinking

### ⚠️ Dressing up a monolith with sidecars

Putting an unchanged monolith into a container, deploying it on Kubernetes, and declaring the system "cloud-native". The deployment platform is modern but the architecture isn't — there's no real benefit beyond a different bill from a different vendor.

#### What to do instead

Cloud-native is an architectural commitment, not a hosting choice. The application must be redesigned for ephemerality, statelessness, and resilience. Migrating without redesigning is just lift-and-shift wearing a different name.

---

### ⚠️ Twelve-Factor as a checklist

Treating Twelve-Factor as a compliance exercise: each factor checked off in code review, no further thought given. Apps "comply" while still holding session state in memory, mutating their config at runtime, or relying on a specific working directory.

#### What to do instead

Twelve-Factor is the floor, not the ceiling. Each factor exists to enable a specific cloud-native property — disposability, statelessness, environment portability. Verify the property holds, not just the textual rule.

---

### ⚠️ The pet container

Treating containers as long-lived servers with names and personalities. Operations involve SSH-ing into containers, patching configuration in place, restarting services manually, debugging from container-local logs. The cloud has become a more expensive data centre.

#### What to do instead

Containers are cattle. State changes happen by deploying a new image, not by mutating a running one. If a container needs to be SSH'd into to be diagnosed, observability is missing — fix the observability, don't normalise the SSH.

---

### ⚠️ Observability reduced to logging

Calling unstructured `printf`s "observability" because they show up in a log aggregator. No metrics with cardinality, no distributed traces, no SLOs — just text people grep through during incidents.

#### What to do instead

Observability is three pillars (logs, metrics, traces) bound by trace context, with SLOs as the alerting layer. Each pillar answers a different question; logs alone cannot diagnose distributed-systems behaviour. Invest in all three from the first service onward — retrofitting is far more expensive than instrumenting from the start.

---

### ⚠️ The platform as a black box

Adopting Kubernetes, a service mesh, or a managed orchestrator without understanding what they do. When something breaks, the application team cannot reason about scheduling, retries, mTLS, or admission control because no one on the team understands the platform's semantics. Outages become magic.

#### What to do instead

The platform is part of the architecture. Application engineers don't need to be platform builders, but they do need to understand the platform's contracts: how scheduling works, what mesh retries look like, what autoscaling reacts to, what admission policies are enforced. A platform whose behaviour can't be predicted by application teams is an outage waiting to happen.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Every service runs as a stateless process; all state lives in named backing services ‖ Roll a die and kill that-numbered replica. If anything more dramatic than a brief reconnect happens, the application is holding state it should not be. Statelessness is the property that makes elasticity possible — without it, scaling out only multiplies the problem. | ☐ |
| 2 | Every configuration value comes from the environment, never from the binary ‖ Search the codebase for hard-coded URLs, region names, environment-specific paths, or feature flags compiled into the build. Each one is a deployment that requires a rebuild. The same image must promote from dev to prod by tag alone. | ☐ |
| 3 | The same container image is promoted across every environment without rebuild ‖ Promotion across dev / staging / prod is a tag change, not a different artefact. If each environment has its own build pipeline, environment-specific drift is inevitable and "works in staging" stops meaning anything. | ☐ |
| 4 | Liveness, readiness, and startup probes are implemented and tested ‖ The platform decides when to send traffic to a pod, when to restart it, and when to consider startup complete. Without proper probes, the platform makes those decisions wrong, and the application gets traffic before it is ready or marked unhealthy when it is fine. | ☐ |
| 5 | Every external call has an explicit timeout, retry policy, and circuit breaker ‖ Distributed-system calls fail. Cascading failures happen when slow callees turn into queue backups in their callers, which turn into queue backups in their callers' callers. Timeouts and circuit breakers stop this cascade — explicit, not default. | ☐ |
| 6 | State-changing operations are idempotent so retries are safe ‖ Without idempotency, retry-on-error becomes duplicate-orders, double-charges, or repeated notifications. Idempotency keys, deduplication windows, and PUT-vs-POST semantics make retries the safe default rather than the dangerous one. | ☐ |
| 7 | Structured logs, metrics, and distributed traces are emitted for every request ‖ Three pillars, all three required. Logs alone cannot diagnose distributed behaviour. Metrics alone cannot debug a specific request. Traces alone cannot show patterns. The combination — bound by trace context — is what makes a cloud-native system debuggable. | ☐ |
| 8 | Service-level objectives are defined for every user-facing capability and tracked over time ‖ SLOs convert "is the service healthy" from an opinion into a measurement. They define what to alert on (so the team is paged for what users actually care about) and govern release pace through error budgets (when budget is spent, slow down). | ☐ |
| 9 | Container images are scanned, signed, and admitted only by policy ‖ Vulnerability scanning catches known CVEs in dependencies. Image signing prevents unsigned or tampered artefacts from running. Admission policies enforce both at the cluster boundary. Without these, the supply chain is an opaque attack surface. | ☐ |
| 10 | The application team can describe, on a single page, what the platform does for them ‖ The platform — autoscaling rules, mesh retries, traffic shaping, secret mounting, admission policies — is part of the architecture every application team relies on. If the team can't articulate the platform's contracts, outages will be inexplicable when they happen. | ☐ |

---

## Related

[`principles/foundational`](../../principles/foundational) | [`principles/modernization`](../../principles/modernization) | [`principles/domain-specific`](../../principles/domain-specific) | [`principles/ai-native`](../../principles/ai-native) | [`patterns/distributed`](../../patterns/distributed) | [`nfr/reliability`](../../nfr/reliability)

---

## References

1. [The Twelve-Factor App](https://12factor.net/) — *12factor.net*
2. [CNCF Cloud Native Definition](https://github.com/cncf/toc/blob/main/DEFINITION.md) — *GitHub / CNCF*
3. [Kubernetes Documentation — Concepts](https://kubernetes.io/docs/concepts/) — *kubernetes.io*
4. [CNCF Cloud Native Landscape](https://landscape.cncf.io/) — *landscape.cncf.io*
5. [Site Reliability Engineering (Google)](https://sre.google/sre-book/table-of-contents/) — *sre.google*
6. [OpenTelemetry Documentation](https://opentelemetry.io/docs/) — *opentelemetry.io*
7. [The Reactive Manifesto](https://www.reactivemanifesto.org/) — *reactivemanifesto.org*
8. [SLSA — Supply-chain Levels for Software Artifacts](https://slsa.dev/) — *slsa.dev*
9. [Observability (software systems)](https://en.wikipedia.org/wiki/Observability_(software)) — *Wikipedia*
10. [Service Mesh — What is Istio?](https://istio.io/latest/docs/concepts/what-is-istio/) — *istio.io*
