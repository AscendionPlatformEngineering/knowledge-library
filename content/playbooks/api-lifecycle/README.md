# API Lifecycle

The strategic guide for managing APIs across their full lifecycle — recognising that the team's design discipline before first release, versioning strategy that lets multiple versions coexist, deprecation policy with announced timelines and migration support, consumer migration tooling that makes upgrade tractable, and retirement discipline that actually removes old versions are what determine whether an API becomes long-lived infrastructure that consumers depend on confidently or a perpetually compatible burden whose old versions never die because nobody can afford to break the consumers who never migrated.

**Section:** `playbooks/` | **Subsection:** `api-lifecycle/`
**Alignment:** Stripe API Reference | Microsoft REST API Guidelines | Google API Improvement Proposals (AIP) | RFC 8594 — Sunset HTTP Header

---

## What "API lifecycle playbook" means — and how it differs from "API backend technology"

This page is about the *playbook* — the strategic guide for how the team manages APIs over time, from design through retirement. The technology of building APIs — REST versus GraphQL versus gRPC, framework choices, gateway selection, authentication mechanisms — lives in [`technology/api-backend`](../../technology/api-backend) at section level. Same domain, different operational concern: this page owns the lifecycle discipline; `api-backend` owns the technology surface. A team can use the same technology stack and still produce APIs that are either rigorously lifecycle-managed or perpetually accumulating undeprecated versions; the discipline is orthogonal to the framework.

A *primitive* approach to API lifecycle is to treat the API as a one-time deliverable: ship v1, then ship v2 when changes are needed, leave v1 running because consumers haven't migrated, ship v3 when v2 needs changes, and so on. The team gradually accumulates an undifferentiated set of versions with overlapping but slightly different behaviour, no announced deprecation timeline, no consumer migration support, and no retirement plan. Each version becomes load-bearing in some consumer's integration; removing any of them risks breaking systems the API team can't directly fix. The cost of every future change scales with the number of versions in production, because the change has to be verified across all of them or made compatible with all of them. The team ends up unable to evolve the API at all because the cost of any change has become prohibitive.

A *production* approach to API lifecycle is a *designed discipline across phases*. The *design phase* establishes the contract carefully — what resources exist, what operations apply, what the failure modes are, what backwards compatibility means for this API — *before* first release locks decisions into consumer integrations. The *versioning strategy* documents how breaking changes are handled (major version bump in URL, or media-type negotiation, or header-based version selection), so consumers know what triggers a version change and what coexistence guarantees apply. The *deprecation policy* documents how versions are sunset — minimum support window after deprecation announcement, channels for announcement (Sunset HTTP header, deprecation notice in docs, direct emails to identified consumers), and migration support during the deprecation window. The *consumer migration tooling* makes the upgrade path tractable — schema diff tools that show what changed, codemod or transformation scripts where the change is mechanical, parallel running periods where consumers can compare old and new responses, sandbox environments for testing migration. The *retirement discipline* actually executes — at the announced sunset date, the deprecated version is removed; not as a surprise (the announcement was made N months prior with reminders), but as the predictable execution of the announced policy. Each phase has documented standards; the API moves through them with the team's discipline applied at each.

The architectural shift is not "we have versioned APIs." It is: **the API is a designed long-lived contract whose lifecycle discipline — design care before first release, versioning strategy that lets multiple versions coexist with documented coexistence guarantees, deprecation policy with announced timelines and migration support, consumer migration tooling that makes upgrade tractable, and retirement discipline that actually removes old versions — determines whether the team can continue evolving the API for years or whether the API gradually becomes immobile under the weight of undeprecated old versions, and treating every API change as a "we'll add v2 and keep v1 alive" decision produces a permanent obligation that compounds with every release.**

---

## Six principles

### 1. Design discipline before first release matters more than any later decision

The most expensive moment in an API's lifecycle is the moment of first release. Before first release, the team can change anything: add or remove resources, restructure response shapes, rename fields, change error semantics, alter authentication. After first release, every consumer integration becomes a constraint on what can change without breaking them. An API team that ships v1 quickly to "see what consumers need" then iterates rapidly to refine the contract has already locked in the v1 they shipped — every consumer who integrated against it now expects v1 to keep working. The architectural discipline is to *invest the most rigorous design effort before first release*: review the resource model, verify the operations are CRUD-coherent, check naming consistency, examine error semantics for self-consistency, validate that pagination/filtering/sorting follow uniform conventions, ensure authentication and authorisation models are settled. The cost of careful design before first release is *one careful design exercise*; the cost of getting it wrong after release is *every breaking change you'll ever want to make for the lifetime of the API*.

#### Architectural implications

- API design review is a structured exercise before v1 release: resource model, operations, naming, error semantics, pagination and filtering, authentication, idempotency. Each is reviewed against documented conventions.
- "Ship to learn" is correct *in private alpha or controlled beta* (small set of design partners, expectations of breaking changes). It is *wrong* in public v1 release (where consumer integrations become binding constraints).
- The team distinguishes between design decisions made *before* first release (cheap to revise) and after (expensive to revise). The latter trigger the versioning discipline; the former are absorbed in normal iteration.
- Design conventions are documented at the organisation level, not invented per API. Stripe, Microsoft, and Google all maintain published API design guides; teams reference one as their convention rather than inventing a new convention each time.

#### Quick test

> Pick the most recently shipped public API in your organisation. Was there a structured pre-release design review against documented conventions, or did the API ship when the implementation was working? If the latter, the design decisions in v1 are now binding constraints — every flaw found later requires a versioning decision rather than a refactor.

#### Reference

[Stripe API Reference](https://stripe.com/docs/api) is the canonical example of API design discipline — uniformity of resource models, error semantics, pagination, and idempotency keys is rigorously maintained across the surface. [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines) and [Google API Improvement Proposals (AIP)](https://google.aip.dev/) are the published conventions Microsoft and Google teams reference at design time.

---

### 2. The versioning strategy is documented and chosen deliberately, not accidental

A primitive API has version-by-accident: when the team needs to make a breaking change, someone proposes adding `v2` to the URL, the team agrees, and `/v2/...` endpoints appear with no documented rule for what triggered the version change, what coexistence guarantees apply between v1 and v2, or how consumers know which to use. A production API has a *deliberate, documented versioning strategy* established before first release: which mechanism (URL path versioning, media-type negotiation, custom header, query parameter), what triggers a new version (any breaking change, only when accumulated changes warrant it, on a schedule), what coexistence is guaranteed (v1 receives no new features but stays bug-fixed during deprecation window, or v1 is frozen entirely), and how consumers migrate. The strategy is *part of the API's published documentation*, not implicit team convention. Each major release follows the documented rules; the discipline pays compound returns because consumers know what to expect from any version change.

#### Architectural implications

- One versioning mechanism is chosen and applied consistently. Mixed strategies (URL versioning for some endpoints, media-type for others) create confusion and break tooling that assumes one mechanism.
- The trigger for a new major version is documented: any breaking change, or a curated set of breaking changes accumulated over time, or a scheduled cadence. The team can answer "why did v3 happen now?" from the documented rule.
- Coexistence guarantees between versions are explicit: v1 still works, receives security patches, but does not receive new features and may receive bug fixes only at reduced priority. The guarantees are part of the published policy, not negotiated per-consumer.
- Semantic versioning principles apply at the API surface even when the version number is a single integer: a breaking change forces a new major version; backwards-compatible additions stay in the current major version.

#### Quick test

> Look at how a recent major version increment was decided in your organisation. Can you find a documented rule explaining what triggered it (a specific breaking change, or accumulated changes warranting a version bump)? Or did "we should call this v2" emerge from a meeting? If the latter, the versioning strategy is implicit, and consumers can't predict when versions will appear or what changes between them.

#### Reference

[Semantic Versioning 2.0](https://semver.org/) is the canonical articulation of versioning discipline. [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines) and [Stripe API Reference](https://stripe.com/docs/api) document their respective versioning strategies as part of the public API contract.

---

### 3. Multiple versions coexist with documented guarantees, not as accumulating debt

When v2 ships, v1 doesn't disappear — consumers integrated against v1 keep working until they migrate. The discipline of *multi-version coexistence* is to make this period *bounded, supported, and documented* rather than perpetual and accidental. During coexistence: v1 continues to operate with documented guarantees (security patches yes, new features no, behaviour stable); v2 is the recommended version with active development; consumers can compare v1 and v2 responses to understand what's changing; a deprecation timeline for v1 is published. The architectural test is: *can you point to the policy document that says how long v1 is supported and what happens when?* If the answer is "we'll keep v1 running as long as anyone uses it", coexistence has degraded into accumulation, and v1 is a permanent obligation. If the answer is "v1 is supported for 18 months from v2 GA, with security patches only for the last 6 months, and removal at 18 months", coexistence is a managed phase with a defined endpoint.

#### Architectural implications

- Each version's support level is explicitly classified: full support (the current version), maintenance (security and high-severity bug fixes only), deprecated (the deprecation timeline is announced; no fixes except critical security), retired (removed from production).
- The API gateway or routing layer enforces the version classification: deprecated versions return Sunset headers; retired versions return 410 Gone with migration documentation.
- Internal teams maintaining the API have a documented multi-version testing matrix: changes are verified against all supported versions, not just the current one. The number of supported versions is explicitly bounded so the matrix doesn't grow indefinitely.
- A consumer can determine which version they are calling and what its support level is from API responses (deprecation headers, version info endpoint). The mechanism is part of the API contract.

#### Quick test

> Inspect a current API response in your organisation. Is the version embedded somewhere in the response or headers? Can you tell from a response whether the version is fully supported, in maintenance, or deprecated? If version classification isn't visible in API responses, consumers can't tell when they need to migrate, and migration becomes a surprise rather than a managed phase.

#### Reference

[RFC 8594 — Sunset HTTP Header](https://www.rfc-editor.org/rfc/rfc8594) standardises the mechanism for communicating deprecation timelines through API responses. [Stripe API Reference](https://stripe.com/docs/api) maintains documented version-by-version coexistence with explicit support classifications.

---

### 4. The deprecation policy is announced, with timelines and migration support — not negotiated case by case

A primitive deprecation is "we'd like to remove v1; please migrate when you can." A production deprecation is the *predictable execution of an announced policy*: deprecation date is announced (typically alongside a new major version's GA); minimum support window is documented (12-24 months is common for public APIs; shorter for internal APIs); the announcement is published through multiple channels (Sunset HTTP header on every response, deprecation notice in API documentation, direct emails to identified consumers, blog post, status page); migration documentation is published alongside the announcement (what changed, why, how to migrate, what tooling is available). At the announced sunset date, the deprecated version is removed. The discipline is *predictability*: consumers can plan migration because the timeline was announced; the API team can execute removal because the announcement was made and renewed; the cost of removing the old version was set when v2 shipped, not negotiated per-consumer at sunset time.

#### Architectural implications

- The deprecation timeline is part of the API's published lifecycle policy: minimum N months from announcement to removal; reminders sent at announced milestones (T-12 months, T-6 months, T-3 months, T-1 month).
- The Sunset header is set on every response from a deprecated version, with the planned removal timestamp. The mechanism is automatic, not relying on consumers to read documentation.
- Migration support is documented and available during the deprecation window: schema-diff tooling, sample migration code, parallel-run sandboxes where consumers can compare v1 and v2 responses, support channel for migration questions.
- Identified consumers (those whose integrations the API team can enumerate, typically via API key or OAuth client) receive direct outreach. Anonymous traffic relies on header-based notice and public documentation.

#### Quick test

> If you needed to deprecate the v1 of your most-trafficked API today, what would you do, and how soon could you actually remove v1? If the answer is "we'd send an email and hope they migrate" or "we couldn't actually remove v1 ever," the deprecation policy doesn't exist as a deployable artefact — it exists only as good intentions.

#### Reference

[RFC 8594 — Sunset HTTP Header](https://www.rfc-editor.org/rfc/rfc8594) defines the standard header for communicating deprecation timelines. [Google API Improvement Proposals (AIP)](https://google.aip.dev/) document Google's deprecation discipline in the AIP-180 series.

---

### 5. Consumer migration tooling makes the upgrade path tractable — not just possible

A primitive upgrade story is "v2 is available; please update your client." A production upgrade story is a *toolkit* that makes the migration achievable for the consumer engineering team in measured effort. The toolkit includes: *schema diff tooling* (what changed structurally between v1 and v2 — added fields, removed fields, renamed fields, type changes); *migration code or codemods* where the change is mechanical (a script that transforms a v1 request payload to a v2 payload, or a wrapper library that calls v2 with v1 semantics); *parallel-run sandboxes* where consumers can call both v1 and v2 with the same request and compare responses to understand the change empirically; *worked examples* showing typical integration patterns updated from v1 to v2; *test fixtures* showing v1 and v2 responses side by side. The architectural discipline is to recognise that the migration is consumer-engineering work that the API team partly enables; the better the tooling, the cheaper the migration, and the more consumers actually do migrate before the deprecation deadline.

#### Architectural implications

- Schema diff tooling is generated automatically from the API specification (OpenAPI, Protocol Buffers, GraphQL SDL). Consumers can ask "what changed?" and get a structured answer, not prose summary.
- Where the change is mechanical (renamed field, restructured response shape with deterministic mapping), a migration script or codemod is published. The API team takes on the toil of writing it once instead of every consumer writing the equivalent.
- A parallel-run mode is supported on the API gateway: the same request is routed to both v1 and v2; the response compared; differences logged for the consumer to inspect. This lets consumers verify migration empirically.
- Identified consumers receive personalised migration support: the API team can see which v1 endpoints they call and offer specific migration guidance. The discipline scales with the number of high-value integrations.

#### Quick test

> Take the last major version increment you shipped. What did you publish to help consumers migrate — beyond the changelog and "please update"? If the answer is "the changelog and please update," consumer migration is being treated as the consumer's problem, and the deprecation timeline will collide with consumers who couldn't justify the migration effort.

#### Reference

[Stripe API Reference](https://stripe.com/docs/api) maintains migration guides and version-comparison tooling as part of the public API surface. [API Stylebook](https://apistylebook.com/) catalogues migration tooling patterns from major API providers.

---

### 6. Retirement actually executes — versions are removed at the announced sunset, not perpetually extended

The hardest discipline in API lifecycle is *actually removing the deprecated version at the announced sunset date*. The temptation to extend — "let's give them another quarter" — is constant: a major consumer hasn't migrated; the migration is harder than expected; an internal political ally requested an extension. Each extension renders the next sunset date less credible: if you extended once, you'll extend again, and consumers learn to ignore the sunset announcements. The architectural discipline is *credibility through execution*: the announced sunset date is treated as the binding commitment; extensions are rare, public, and explicit (with documented reasons and a new committed date). When the sunset arrives, the deprecated version returns 410 Gone with migration documentation in the response body; the routes are removed; the underlying code is removed in a subsequent cleanup. Future deprecation announcements are credible because past ones were executed.

#### Architectural implications

- Sunset is a calendar-driven, automated removal: the gateway or routing layer is configured to disable the deprecated routes at the announced timestamp, not relying on a manual "let's flip the switch" moment.
- Extensions are *exceptional and documented*: when an extension does happen, the new sunset date is publicly announced with the reason, and the extension period is explicitly capped (no rolling extensions).
- The 410 Gone response includes a Link header to the migration documentation and a structured error body identifying the API version that was removed and the recommended replacement. Consumers hitting the removed endpoint receive immediately actionable information.
- Post-sunset retirement is followed by *codebase removal*: the deprecated version's implementation is deleted from source control after a brief grace period, so the engineering surface stops carrying multi-version complexity.

#### Quick test

> Look at your most recently deprecated API version. Has it actually been removed at the announced sunset date, or is it still serving traffic past the announcement? If the latter, the retirement discipline has decayed, and future deprecation announcements will be discounted by consumers who learned the announcement isn't binding.

#### Reference

[RFC 8594 — Sunset HTTP Header](https://www.rfc-editor.org/rfc/rfc8594) treats sunset as a binding commitment; the header value is the planned removal date. [Google API Improvement Proposals (AIP)](https://google.aip.dev/) document the Google deprecation lifecycle including post-sunset retirement.

---

## Common pitfalls when adopting API lifecycle thinking

### ⚠️ Shipping v1 to "see what consumers need" then iterating

The first release happens before the design is settled, on the assumption that early consumers will surface what's needed. Once consumers integrate, the half-formed v1 becomes a binding constraint, and every subsequent refinement requires a breaking change.

#### What to do instead

Pre-release design review against documented conventions. Use private alpha or controlled beta with explicit "expect breaking changes" expectations, then release publicly only after the contract is settled. The cost of careful design before release is bounded; the cost of correcting v1 after release is unbounded.

---

### ⚠️ Versioning by accident — no documented strategy

Each major version increment happens through ad-hoc team discussion ("let's call this v2") without a documented rule for what triggers a version change or what coexistence guarantees apply. Consumers can't predict when versions will appear.

#### What to do instead

Documented versioning strategy chosen before first release: which mechanism (URL path, header, media type), what triggers a new version, what coexistence guarantees between versions. Strategy is part of the published API documentation.

---

### ⚠️ Coexistence becomes accumulation — no announced removal date

v1 keeps running because some consumers haven't migrated. v2 ships. v3 ships. The team now maintains three versions indefinitely. Every change has to be considered against all three; the cost of evolution scales with version count.

#### What to do instead

Each version has an announced classification (full support / maintenance / deprecated / retired) and a documented sunset date once deprecated. The number of simultaneously supported versions is explicitly bounded (typically 2 — current and previous, with previous in deprecation window).

---

### ⚠️ Deprecation as soft request — "please migrate when you can"

The deprecation announcement is a polite suggestion with no timeline, no Sunset header on responses, and no actual removal date. Consumers don't migrate because there's no deadline; the API team can't remove v1 because there's no committed sunset.

#### What to do instead

Deprecation is the start of an announced timeline (minimum N months from announcement to removal). Sunset HTTP header is set on every response from the deprecated version. Direct outreach to identified consumers. Migration documentation published alongside the announcement.

---

### ⚠️ Sunset extensions become routine — credibility erodes

The first sunset date arrives; a major consumer hasn't migrated; the team extends the date by a quarter. The extension repeats. Consumers learn that sunset announcements are negotiable, and future ones are discounted.

#### What to do instead

Sunset is a binding commitment executed on the announced date. Extensions are exceptional, public, and explicitly capped (one extension only, with a new firm date). The 410 Gone response is the default at the sunset moment.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Pre-release design review is structured against documented conventions ‖ Resource model, operations, naming, error semantics, pagination, authentication all reviewed before v1 release. The team uses a published convention set (Stripe, Microsoft REST, Google AIP) rather than inventing per-API. | ☐ |
| 2 | Versioning strategy is documented and consistent across the API surface ‖ One mechanism (URL path / header / media type) is chosen and applied uniformly. The trigger for a new major version is documented. Strategy is part of public API documentation. | ☐ |
| 3 | Multi-version coexistence has explicit support classifications ‖ Each version is classified (full support / maintenance / deprecated / retired). Internal multi-version testing matrix exists and is bounded. The number of simultaneously supported major versions is explicitly capped. | ☐ |
| 4 | Version classification is visible in API responses ‖ Sunset HTTP header on deprecated versions; deprecation notices in documentation; consumers can determine which version they are calling and its support level from response data. | ☐ |
| 5 | Deprecation policy is published with timelines ‖ Minimum N months from announcement to removal documented in lifecycle policy. Reminder schedule documented (T-12, T-6, T-3, T-1 months). Direct outreach to identified consumers part of the policy. | ☐ |
| 6 | Migration tooling makes upgrade tractable ‖ Schema diff tooling, migration scripts where mechanical, parallel-run sandboxes for empirical comparison, worked examples updating typical integration patterns. The migration is supported, not just possible. | ☐ |
| 7 | Sunset dates are treated as binding commitments ‖ Extensions are rare, public, and capped. Routes are disabled automatically at the announced timestamp. Post-sunset 410 Gone responses include migration documentation. | ☐ |
| 8 | Codebase removal follows retirement ‖ Deprecated version's implementation is deleted from source control after a brief grace period. Engineering surface stops carrying multi-version complexity. The retirement is fully executed, not just routed away. | ☐ |
| 9 | Identified consumers receive personalised migration support ‖ Team can see which deprecated endpoints each consumer calls. Direct outreach during deprecation window. High-value integrations receive dedicated migration assistance. | ☐ |
| 10 | The lifecycle policy itself is a versioned, owned artefact ‖ The policy document has an owner, a revision history, and is referenced from the API documentation. Changes to the policy are themselves announced (a meta-deprecation discipline). | ☐ |

---

## Related

[`playbooks/migration`](../migration) | [`playbooks/resilience`](../resilience) | [`technology/api-backend`](../../technology/api-backend) | [`templates/adr-template`](../../templates/adr-template) | [`governance/decisions`](../../governance/decisions)

---

## References

1. [Stripe API Reference](https://stripe.com/docs/api) — *stripe.com*
2. [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines) — *github.com*
3. [Google API Improvement Proposals (AIP)](https://google.aip.dev/) — *google.aip.dev*
4. [Semantic Versioning 2.0](https://semver.org/) — *semver.org*
5. [RFC 8594 — Sunset HTTP Header](https://www.rfc-editor.org/rfc/rfc8594) — *rfc-editor.org*
6. [API Stylebook](https://apistylebook.com/) — *apistylebook.com*
7. [OpenAPI Specification](https://www.openapis.org/) — *openapis.org*
8. [AsyncAPI](https://www.asyncapi.com/) — *asyncapi.com*
9. [Building Evolutionary Architectures (Ford et al.)](https://www.oreilly.com/library/view/building-evolutionary-architectures/9781491986356/) — *oreilly.com*
10. [ThoughtWorks Tech Radar](https://www.thoughtworks.com/radar) — *thoughtworks.com*
