# Deployment Patterns

Architecture for the moment code reaches users — the patterns for traffic shifting, feature exposure, rollback, and cadence that make production changes safe enough to be frequent, and frequent enough to be safe.

**Section:** `patterns/` | **Subsection:** `deployment/`
**Alignment:** Continuous Delivery | DORA Metrics | Feature Toggles | Trunk-Based Development

---

## What "deployment patterns" actually means

A *deploy-as-event* approach treats deployment as a discrete moment: code is built, code goes to production, code runs. This worked when teams deployed quarterly, when each deploy was a project, and when the architectural decisions all lived inside the source code. It does not work when teams deploy daily — every step in that "discrete moment" must be safe, reversible, observed, and decoupled from end-user impact, and "the moment" stops being a moment and becomes the system's fundamental rhythm.

A *deployment-as-architecture* approach treats how code reaches users as a first-class concern, with its own design surface. Deployment frequency, traffic-shifting strategy, rollback speed, feature-flag granularity, schema-migration coupling — these are not operational details negotiated at release time. They are properties the architecture either has or lacks, and they determine whether the team ships safely fifty times a day or unsafely once a quarter.

The architectural shift is not "we set up CI/CD." It is: **deployment is the moment the architecture's choices become real, and how that moment is engineered determines almost every other property of the system — risk, recovery, cadence, feedback, learning rate.**

---

## Six principles

### 1. Decouple deploy from release

Deploying code (placing it in production where it can run) and releasing a feature (exposing it to users) are different operations performed at different times by different mechanisms. Conflating them — assuming deploy *is* release — forces every deploy into a release window, multiplies risk, and slows the team to whatever the riskiest pending change can tolerate. Decoupling is mechanical: feature flags, dark launches, progressive exposure, environment-based gating. The architectural insight is that they ARE separable, and the cost of separating them is paid once.

#### Architectural implications

- Code reaches production behind flags or gated by user / region / percentage rules.
- A "release" is a configuration change, not a deployment.
- Failed releases roll back via flag flip in seconds, not via redeploy in minutes.
- The set of in-flight features (deployed but not yet released, or partially released) is observable through tooling, not tribal memory.

#### Quick test

> Could you turn off your most recently shipped feature for one specific customer or region without redeploying? If the answer is "no, we'd have to revert the code," you have not separated deploy from release — every release decision is paying full deployment cost.

#### Reference

[Martin Fowler, Feature Toggles](https://martinfowler.com/articles/feature-toggles.html). Note that he distinguishes four toggle categories — release, experiment, ops, permission — each with different lifecycle expectations.

---

### 2. Canary deployments are statistical experiments, not just gradual rollouts

A canary that gets 1% of traffic but is never compared to baseline metrics is a slow rollout, not a canary. The pattern requires automated comparison of error rates, latency, and business metrics between the canary version and the baseline version, with predefined abort criteria and a decision authority. Without these, the only thing the gradual rollout achieves is making failures slower to detect — small blast radius for longer is not the same as small blast radius caught early.

#### Architectural implications

- Every canary stage has predefined abort criteria measured automatically.
- Comparison metrics are SLI-level (errors, latency, throughput) plus business-level (signups, transactions, conversions).
- The decision to advance, hold, or abort is automated wherever possible; humans intervene only where statistical signal isn't yet sufficient.
- Aborted canaries result in automatic rollback to the baseline version, with no human intervention required beyond approval of the abort itself.

#### Quick test

> Pick the most recent canary deployment your team ran. What were the success criteria, and were they evaluated automatically? If the answer is "no errors in the dashboard," that's not statistical comparison — that's wishful checking, dressed in canary clothes.

#### Reference

[Google SRE Book, Release Engineering](https://sre.google/sre-book/release-engineering/). The release-engineering chapter sets out the operational discipline; the broader book extends it through canary analysis and abort handling.

---

### 3. Rollback is the architecture; recovery is the discipline

Every deployment must be reversible. If rollback requires a "rollback project" — coordinating database restoration, cache invalidation, queue replay across teams — there is no rollback, only delayed disaster. The architecture's design decisions determine whether rollback is a button press or a multi-day operation. Rollback speed should match (or beat) deployment speed; if it's slower, the deployment cadence is too aggressive for what the architecture can recover from.

#### Architectural implications

- Every deployment leaves the previous version warm and ready to receive traffic again.
- Schema changes are designed for compatibility with both N-1 and N versions throughout the deployment window.
- Stateful side effects (queue messages, cache writes, file outputs) are versioned or idempotent so the previous version can resume cleanly.
- Rollback procedures are tested before the deployment that might need them — exercised regularly enough that the team trusts them under pressure.

#### Quick test

> If your most recent deployment had to be rolled back right now — not in an hour, right now — what would happen? If the answer is "we'd need to schedule the rollback," the architecture has not made rollback a first-class capability, and every deploy is taking on unmanaged risk.

#### Reference

[Jez Humble & David Farley, Continuous Delivery](https://continuousdelivery.com/). The discussion of rollback runs through the entire book; it is treated as a property of the deployment architecture rather than an emergency procedure.

---

### 4. Blue-green is about state, not code

The code side of blue-green is straightforward: run two complete environments, switch traffic between them. The hard problem is everything that has STATE: the database schema both versions must understand, the cached entries both produce, the in-flight messages on the queue, the file storage both reference. Most blue-green failures are state failures, not deployment failures. Pretending otherwise — focusing on the load-balancer flip while glossing over the database migration — is the most common form of theatre in the pattern's name.

#### Architectural implications

- Schema changes are forward-compatible with N-1 and N simultaneously through the cutover window; breaking changes are deferred or staged through deprecation.
- Cached data is keyed in a way that doesn't poison the other environment when both produce entries during overlap.
- Long-running operations (background jobs, async workflows) are designed to survive a version switch mid-flight or are drained before cutover.
- The cost of running the second environment full-size is paid for, in budget and in operational attention; the half-size shadow is a different pattern with different guarantees.

#### Quick test

> In a blue-green cutover, what happens to a transaction that started on blue and completes on green? If you don't have a clear answer, the pattern is being practiced on the easy parts only — and the failure mode you'll discover later is the one nobody planned for.

#### Reference

[Martin Fowler, Blue-Green Deployment](https://martinfowler.com/bliki/BlueGreenDeployment.html). The original article is short; the practical depth comes from operating the pattern on systems with real state.

---

### 5. Deployment cadence is an architectural property

Teams that deploy fifty times a day and teams that deploy once a quarter are running fundamentally different architectures, regardless of how similar the source code looks. Cadence is a forcing function. Daily deploys require small changes, fast tests, automated rollback, decoupled release, and granular observability. Quarterly deploys require none of those, which is why they don't have them, which is why they can only deploy quarterly. The lock-in works in both directions, and breaking out of low-cadence requires fixing the architecture, not adding willpower.

#### Architectural implications

- Deployment frequency is a measured, tracked metric — not a feeling, not a slide goal, not an aspiration.
- The team commits to operational practices (test automation, observability, on-call discipline) that match the cadence.
- "We can't deploy more often" is an architectural statement; the response is to identify exactly what would have to change before that ceases to be true.
- Rare deploys mean each deploy is a high-risk event handled with ceremony; frequent deploys mean each is low-risk and routine — and the difference is engineered, not cultural.

#### Quick test

> What is your team's deployment frequency this week? If you don't have a number — measured, not estimated — cadence is not currently an engineered property, and the team is shipping at whatever rate the system tolerates rather than the rate it could.

#### Reference

[DORA Research Program](https://dora.dev/). Deployment Frequency is one of the four key metrics; the relationship between cadence and the other three (lead time, change failure rate, MTTR) is the central finding of the research.

---

### 6. Deployment topology is part of the application

Where the application runs (regions, availability zones, edge locations), how it's reached (load balancers, service mesh, CDN), and how versions coexist (single-version, blue-green, canary, A/B) is not an operational detail discovered at deploy time. It is architecture, owned alongside the code, versioned alongside the code, reviewed alongside the code. Infrastructure-as-code is the mechanism; treating deployment topology as part of the application — not a hand-off to a different team in a different repository — is the principle.

#### Architectural implications

- Deployment configuration (Terraform, Kubernetes manifests, mesh policies) lives in the application repository or its sibling, not in a separate "infra" repo nobody from the app team touches.
- The choice of deployment pattern (rolling, blue-green, canary) for each service is a documented decision with rationale.
- Topology changes (region addition, mesh policy update, autoscaling rule) follow the same review and rollout discipline as code changes.
- "What does production look like" is something a team member can answer instantly from the repository, not by SSH-ing into a running system or asking a different team.

#### Quick test

> Pick your most recent deployment. Was the topology configuration in the same review as the code change, or in a separate ticket handled by another team in another repository? If separate, the topology is operationally owned, not architecturally owned — and the gap is where most deployment incidents live.

#### Reference

[OpenGitOps Principles](https://opengitops.dev/) sets out the modern statement of declarative, versioned topology. [Trunk-Based Development](https://trunkbaseddevelopment.com/) describes the development practice that makes high-cadence deployment topology workable.

---

## Architecture Diagram

The diagram below shows a canonical canary deployment architecture: the developer ships a change, CI produces an immutable artifact, two versions of the application coexist in production behind a traffic router, observability captures user-facing signals, and a decision layer (automated where possible) shifts traffic forward or rolls it back based on metric comparison.

---

## Common pitfalls when adopting deployment-pattern thinking

### ⚠️ The Friday-deploy taboo

"We don't deploy on Fridays" is presented as wisdom but is usually the symptom of fragile architecture. Teams that can't deploy safely on Friday can't safely deploy on Tuesday either — Tuesday simply has a five-day buffer before the weekend exposes whatever failed.

#### What to do instead

Treat the inability to deploy on Friday as a signal. The architecture lacks one or more of: fast rollback, observability, automated abort, decoupled release, schema-migration safety. Fix those, and Friday deploys become routine. The goal is to deploy whenever a change is ready, not to schedule risk around the calendar.

---

### ⚠️ Permanent feature flags

Feature flags introduced for a launch and never removed. After eighteen months, the flag system has more configuration paths than the application has user-facing features. Every code path is now conditional on flag state, every test must consider every combination, and the flag system itself has become the most fragile part of the architecture.

#### What to do instead

Every feature flag has an owner and a removal date at creation time. Lifecycle types matter: release flags die after rollout; experiment flags die at conclusion; permission flags persist (and should be a different mechanism). When a flag's purpose has expired, removing it is a P1 follow-up, not a backlog item that ages quietly into permanence.

---

### ⚠️ Canary without metrics

Gradual rollout with no automated comparison to baseline. The canary stage is just a delay, the dashboard is glanced at by whoever has time, and "looks fine" is the abort criterion. The pattern's name is being practiced; the pattern's value is not.

#### What to do instead

Define the success criteria before the canary starts. Baseline metrics come from the previous stable version; comparison is automated; abort is automatic when criteria fail. The human role is exception handling, not primary monitoring.

---

### ⚠️ Rollback by re-deploying old code

Pretending you have rollback when you only have a longer redeploy. "Rolling back" by triggering a build of the previous commit takes ten minutes — the same ten minutes the original deploy took. During those ten minutes, the failed version is serving traffic. This is not rollback; it is delay with a recovery label.

#### What to do instead

Rollback shifts traffic; redeploy rebuilds and re-routes. Keep the previous version warm and addressable until the new version has soaked. The rollback action should be a routing change measured in seconds, not a build measured in minutes.

---

### ⚠️ Schema migration coupled to code deploy

The single biggest reason "Friday deploys are scary" — every deploy includes a schema change that may or may not be reversible. Code rollback is fast; schema rollback is "we need to discuss this in the morning." So schema couples to code, which couples to risk, which couples to scheduling, which becomes the quarterly deploy nobody enjoys.

#### What to do instead

Schema migrations and code deploys are independently deployable, in either order. Migrations are forward-compatible with both N-1 and N application versions; rollback of code does not require rollback of schema. The two halves of the change are separate deployments with their own observation windows.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Every deployment has a documented rollback procedure tested in production-like environment ‖ Rollback is a tested capability or it is not a capability. Documented procedures that have never been exercised are fiction the team will read for the first time during an incident, when fiction is the worst thing to be reading. | ☐ |
| 2 | Feature flags are tracked with owners and removal dates ‖ Without ownership and lifecycle, flags accumulate forever. The flag inventory should be queryable; flags past their removal date should appear in someone's queue, not buried in code that nobody reads. | ☐ |
| 3 | Canary deployments compare metrics against baseline automatically ‖ Manual dashboard checking is not canary analysis. Automated comparison with predefined criteria is what makes a canary a statistical experiment rather than a slow rollout in disguise. | ☐ |
| 4 | Schema migrations and code deploys are independently deployable ‖ Coupled migrations make every deploy slower, riskier, and harder to roll back. The decoupling cost is paid once; the coupling cost is paid every deploy, forever, in compound interest. | ☐ |
| 5 | Deployment topology is described in code reviewed alongside the application ‖ Topology in a separate operational repository owned by another team is not architecture, it is hand-off. The application team should be able to read the topology in their main code review, not file a ticket to learn what production looks like. | ☐ |
| 6 | Deployment frequency is a measured metric, not a feeling ‖ The DORA finding is that frequency correlates with everything else worth measuring. If frequency isn't tracked, the team has no objective view of whether the deployment architecture is improving or degrading over time. | ☐ |
| 7 | Dark launches and shadow traffic are available for high-risk changes ‖ For critical paths (payments, identity, search, anything regulated), validating against production load before exposing users is the difference between catching issues in shadow and catching them in incident reviews. | ☐ |
| 8 | Time-from-merge-to-production is bounded and trackable ‖ DORA's lead-time-for-changes metric. Long lead times mean batched changes; batched changes mean each deploy carries multiple risks; multiple risks mean rare deploys; rare deploys mean even longer lead times. The cycle reinforces itself in either direction. | ☐ |
| 9 | Failed deployments revert automatically without human intervention beyond approval ‖ Automation eliminates the panic decision during incidents. The team's role becomes deciding whether the auto-rollback was correct, not deciding under stress whether to roll back at all. | ☐ |
| 10 | The deployment system itself is on its own deployment pipeline ‖ Manual changes to the deploy pipeline, the CI system, the secret store — each is a category of change that can break the recovery path. Treating the deployment infrastructure as code with the same discipline closes that loophole before it becomes the incident. | ☐ |

---

## Related

[`principles/cloud-native`](../../principles/cloud-native) | [`principles/foundational`](../../principles/foundational) | [`principles/modernization`](../../principles/modernization) | [`patterns/data`](../data) | [`patterns/integration`](../integration) | [`anti-patterns/distributed-monolith`](../../anti-patterns/distributed-monolith)

---

## References

1. [Jez Humble & David Farley — Continuous Delivery](https://continuousdelivery.com/) — *continuousdelivery.com*
2. [Martin Fowler — Feature Toggles](https://martinfowler.com/articles/feature-toggles.html) — *martinfowler.com*
3. [Martin Fowler — Blue-Green Deployment](https://martinfowler.com/bliki/BlueGreenDeployment.html) — *martinfowler.com*
4. [Martin Fowler — Canary Release](https://martinfowler.com/bliki/CanaryRelease.html) — *martinfowler.com*
5. [DORA Research Program](https://dora.dev/) — *dora.dev*
6. [Trunk-Based Development](https://trunkbaseddevelopment.com/) — *trunkbaseddevelopment.com*
7. [Google SRE Book — Release Engineering](https://sre.google/sre-book/release-engineering/) — *sre.google*
8. [Continuous Deployment](https://en.wikipedia.org/wiki/Continuous_deployment) — *Wikipedia*
9. [Feature Toggle](https://en.wikipedia.org/wiki/Feature_toggle) — *Wikipedia*
10. [OpenGitOps Principles](https://opengitops.dev/) — *opengitops.dev*
