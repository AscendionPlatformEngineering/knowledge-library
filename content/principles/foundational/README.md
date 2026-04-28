# Foundational Principles

Architecture for systems that need to outlast their original authors, frameworks, and assumptions — the timeless principles that survive every technology shift.

**Section:** `principles/` | **Subsection:** `foundational/`
**Alignment:** SOLID | Clean Architecture | Hexagonal Architecture | TOGAF ADM

---

## What "foundational" actually means

A *trend-driven* system follows the architectural fashion of the moment: today's microservices, yesterday's three-tier ESB, tomorrow's mesh-something-or-other. Each cycle requires a partial rewrite when the fashion shifts. The architecture has no opinion about anything except its current technology stack — and it shows.

A *foundational* system is built on principles that survive technology shifts. The codebase looks recognisable to architects from 1985 *and* 2025: clear module boundaries, explicit dependencies, conceptual integrity, decisions documented and revisited. Frameworks come and go; the design philosophy persists. When the team rewrites the persistence layer in five years, they preserve the principles and replace only the implementation.

The architectural shift is not "we use the latest tools." It is: **we make decisions our successors can defend, change, and extend without rewriting the system.**

---

## Six principles

### 1. Modularity is information hiding, not file separation

Splitting code into files is not modularity. Modularity is hiding design decisions that are likely to change behind interfaces that are stable. The most-cited paper in software engineering — Parnas (1972) — said this fifty years ago. Most codebases still get it wrong: they split by technology layer (controllers, services, repositories) and call themselves modular, while every change still ripples through every layer.

#### Architectural implications

- Module boundaries align with axes of change — what's likely to vary independently — not with technology types.
- Public interfaces expose contracts; internal data structures and algorithms are not visible to callers.
- A change in implementation should not ripple across module boundaries. If it does, the boundary is in the wrong place.
- The cost of crossing a module boundary should be visible in the codebase, not buried in folder hierarchies.

#### Quick test

> Pick a recent change request that turned out to be larger than expected. How many modules did it touch? If the answer is "most of them," your modules are organised by file type, not by what changes together.

#### Reference

David Parnas's [*On the Criteria To Be Used in Decomposing Systems into Modules*](https://en.wikipedia.org/wiki/Information_hiding) (1972) is the foundational text. Robert C. Martin's *Single Responsibility Principle* (the "S" in SOLID) operationalises it for object-oriented systems.

---

### 2. Dependencies flow toward stability, not toward familiarity

The Dependency Inversion Principle says high-level policy should not depend on low-level mechanism — the mechanism should depend on the policy. In practice this means the volatile parts of the system (frameworks, databases, vendor APIs) depend on the stable parts (domain logic, business rules), never the reverse. This is what makes a system survive the inevitable replacement of its frameworks and databases.

#### Architectural implications

- Domain logic has no `import` statements pointing at frameworks, ORMs, or vendor SDKs.
- Inbound and outbound adapters wrap external dependencies; the core knows nothing about HTTP, SQL, or Kafka.
- Replacing the database, message bus, or web framework should not require changes to domain code.
- New developers should be able to read the domain layer and understand the business without knowing the technology stack.

#### Quick test

> Open a domain class at random. Does it import anything from your web framework, your ORM, or a vendor SDK? If yes, the dependency is flowing the wrong way.

#### Reference

Robert C. Martin's [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) (2012) is the canonical statement. Alistair Cockburn's [Hexagonal Architecture (Ports and Adapters)](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)) (2005) is the same idea expressed geometrically. Both rest on Parnas's earlier work.

---

### 3. Conceptual integrity outranks feature completeness

Fred Brooks called conceptual integrity *the most important consideration in system design*. A system that does fewer things consistently is more useful, more learnable, and more maintainable than one that does more things inconsistently. Every feature added in a way that conflicts with the system's design philosophy is a tax paid forever — by users learning special cases, by engineers maintaining exceptions, by future architects untangling the contradiction.

#### Architectural implications

- The system has a stated design philosophy, written down, that drives decisions.
- New features are evaluated against the philosophy, not just against acceptance criteria.
- Saying "no" to a feature that conflicts with the design is a respected architectural act, not a political failure.
- When the philosophy must change, the change is deliberate, documented, and propagated — not absorbed silently as inconsistency.

#### Quick test

> Could a senior engineer who has never seen the system predict, with reasonable accuracy, how a new feature should behave by reading the existing code? If not, the conceptual integrity has eroded — even if every individual feature works.

#### Reference

Fred Brooks, *The Mythical Man-Month* (1975), Chapter 4: ["Aristocracy, Democracy, and System Design"](https://en.wikipedia.org/wiki/The_Mythical_Man-Month). Brooks argued that conceptual integrity requires architectural authority, not just process — a position still under debate.

---

### 4. Make the implicit explicit; assumptions are hidden bugs

Every undocumented assumption is a future bug looking for an excuse. The classes you don't name, the invariants you don't enforce, the contracts you don't write down — these become the source of incidents the on-call engineer can't reproduce. Foundational architectures surface assumptions in code, not in tribal knowledge.

#### Architectural implications

- Domain concepts that exist only in conversation are promoted to first-class objects in the code.
- Invariants ("an order must have at least one line item") are enforced at the boundary that owns the concept, not scattered as defensive checks.
- API contracts describe pre-conditions, post-conditions, and failure modes — not just request/response shapes.
- Ownership of every persistent piece of state is documented. "Who owns this row" should never require a Slack search.

#### Quick test

> Pick three production incidents from the last quarter. How many of them involved an assumption that was true in someone's head but not enforced anywhere in the system? That count is your implicit-assumption budget being spent.

#### Reference

Eric Evans, *Domain-Driven Design* (2003), Chapter 9 — "Making Implicit Concepts Explicit". The Pythonic principle "explicit is better than implicit" ([PEP 20 — The Zen of Python](https://peps.python.org/pep-0020/)) is the same principle in different vocabulary.

---

### 5. Architecture is the cost of change — optimise for reversibility

The purpose of architecture is not to be correct on day one; it is to be cheap to change on every day after. Decisions that are easy to reverse can afford to be made quickly with limited information. Decisions that are hard to reverse deserve the time and care of a major investment. Treating all decisions identically — either all rushed or all over-deliberated — wastes the team's most expensive resource: judgement.

#### Architectural implications

- Architectural decisions are classified by reversibility before commitment. Two-way doors get fast paths; one-way doors get review.
- Hard-to-reverse choices (data models, API contracts, security boundaries) get explicit ADRs and broader review.
- The architecture is treated as evolvable: fitness functions, reversible migrations, and feature flags are first-class tools.
- "We can fix it later" is a hypothesis to be tested, not an excuse to defer the decision.

#### Quick test

> Look at the last five major architectural decisions. Were they classified by reversibility before commitment? Or were they all treated as either trivial or terrifying — with nothing in between?

#### Reference

The "two-way doors" framing comes from Jeff Bezos's 1997 shareholder letter. Operationalised in Neal Ford, Rebecca Parsons, and Patrick Kua's [*Building Evolutionary Architectures*](https://www.thoughtworks.com/insights/blog/microservices/evolutionary-architecture) (Thoughtworks, 2017) — which introduces architectural fitness functions as the verification mechanism. Michael Nygard's [Documenting Architecture Decisions](https://adr.github.io/) is the canonical pattern for capturing the decisions themselves.

---

### 6. Boring technology is a feature; novelty is a tax

Every novel technology in the stack is an "innovation token" spent. Tokens are scarce. They should be spent on what actually differentiates the business — not on the database, message bus, or deployment system. Boring technology is well-understood, has long-tail debugging support, has stable hiring pipelines, and has predictable failure modes. These are competitive advantages, not concessions.

#### Architectural implications

- Adding a new technology requires explicit justification: what does it enable that the existing stack cannot?
- The "default boring" tech list (Postgres, the dominant cloud, your existing language) is the path of least resistance.
- Operational maturity (debugging, observability, on-call playbooks) is a first-class selection criterion.
- Resume-driven development is recognised as a real failure mode and challenged in design review.

#### Quick test

> Count the distinct database engines, message brokers, and language runtimes in your production system. For each one beyond the first, can a current engineer name the failure modes, replication semantics, and the on-call playbook? If not, you have technology you don't actually own.

#### Reference

Dan McKinley's [*Choose Boring Technology*](https://boringtechnology.club/) (2015) introduced the innovation-tokens framing. The principle has older roots in Frederick Brooks's "no silver bullet" essay (1986) and in Linus Torvalds's repeated insistence that boring infrastructure is what makes interesting software possible.

---

## Architecture Diagram

The diagram below shows the canonical foundational structure: dependencies flow from the volatile periphery (frameworks, vendors) inward toward the stable core (domain logic), with adapters mediating at every boundary and architectural governance gating decisions.

---

## Common pitfalls when adopting foundational thinking

### ⚠️ The premature abstraction trap

Building abstractions before understanding the second use case. The first use case is not data; the second is. Abstractions designed from a single example are usually wrong, expensive to undo, and lock in assumptions that don't generalise. The cost of a missing abstraction is small; the cost of the wrong abstraction is large.

#### What to do instead

Wait for the second concrete use case before extracting an abstraction. Use copy-paste once, even if it feels uncomfortable; the duplication makes the right abstraction visible. Sandi Metz's rule of thumb: "duplication is far cheaper than the wrong abstraction."

---

### ⚠️ The Big Ball of Mud accident

Letting "we'll fix it later" become the architecture. Every shortcut taken under deadline pressure compounds; eventually the architecture is whatever the deadlines allowed. The team didn't choose the design — they accepted it through inattention.

#### What to do instead

Architecture is decided continuously, not in big-bang reviews. Allocate explicit refactoring capacity (Google's "20% rule for engineering health" or equivalent). Make the cost of architectural shortcuts visible — in dashboards, in retros, in the on-call burden — so the trade-off is conscious.

---

### ⚠️ The framework-of-the-month

Treating frameworks as architecture. When the framework changes (and it will), the team rebuilds the system from scratch because the architecture lived inside the framework's choices, not above them. The codebase becomes a record of what was popular when each module was written.

#### What to do instead

Frameworks are tools, not foundations. The domain layer should not import the framework. New frameworks should be adopted as adapters, not as architecture. When a framework reaches end-of-life, the rewrite should touch the adapter layer only, not the core.

---

### ⚠️ The cargo-cult patterns

Applying GoF, microservices, or CQRS patterns mechanically because they appeared in a talk, without the context that made them appropriate. Patterns are answers to specific problems; without the problem, the pattern is just complexity.

#### What to do instead

Before adopting a pattern, articulate the problem it solves in your context. If you can't, you don't need the pattern yet. When in doubt, prefer the simpler structure; you can refactor toward a pattern when the need is concrete.

---

### ⚠️ The decision amnesia

Important architectural choices made and forgotten — with no record of why. Six months later, a new engineer "fixes" a careful trade-off that was made deliberately, and the system regresses. The cost is not the original decision; it's the repeated relearning.

#### What to do instead

Capture decisions in ADRs at the moment they're made, with context, options considered, and rationale. Revisit ADRs when the context changes. The cost of an ADR is fifteen minutes; the cost of relitigating decisions for years is thousands of engineering hours.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Module boundaries align with axes of change (what varies together stays together) ‖ Open your codebase tree. Are the top-level folders named by what changes (Booking, Pricing, Identity) or by what it's made of (Controllers, Services, Repositories)? The first decomposition makes change cheap; the second makes change expensive everywhere at once. | ☐ |
| 2 | Dependencies flow toward stability — domain layer has no framework imports ‖ Search the domain layer for imports of your web framework, ORM, or vendor SDKs. Each one is a coupling between business logic and replaceable infrastructure. The domain should not know what HTTP is. | ☐ |
| 3 | Public interfaces define contracts; implementation details are not exposed ‖ Pick a public class. Read its public methods. Could a caller use it without knowing the internal data structures, the database schema, or the algorithm? If not, the abstraction has leaked and changes propagate further than they should. | ☐ |
| 4 | The system has a stated, written design philosophy that drives decisions ‖ A design philosophy is what's true regardless of the feature being built — "we prefer composition," "we never call cross-context databases directly," "we surface invariants in types." Without a written philosophy, every team member invents their own and the system fragments. | ☐ |
| 5 | Architectural decisions are documented in ADRs at the moment they're made ‖ ADRs capture context, options considered, and the rationale for the choice. They cost fifteen minutes when fresh. They save weeks when a future engineer would otherwise relitigate the decision blind, six months later, on the wrong evidence. | ☐ |
| 6 | Decisions are classified by reversibility before commitment ‖ Two-way doors (the API name, the cache key format) can be made fast and revisited. One-way doors (the data model, the security boundary, the public contract) deserve broader review. Treating both alike either burns time on trivia or rushes the irreversible. | ☐ |
| 7 | Every novel technology is justified against an explicit "boring default" ‖ Postgres works. The dominant cloud works. Your existing language works. A new technology should answer "what does this enable that the boring default cannot?" If the honest answer is "nothing critical," it's an innovation token spent on the wrong thing. | ☐ |
| 8 | Code structure matches the conceptual model — no architectural drift ‖ Walk a business workflow from request to response. Does the path through the code match how a domain expert would describe it? If the code path zigzags through unrelated layers, the conceptual model and the code have diverged — and the next change will be harder than the last. | ☐ |
| 9 | Architectural fitness functions or tests guard the boundaries ‖ Fitness functions are automated checks that prevent architectural erosion: "domain layer must not import infrastructure," "no cross-context database access," "p99 latency stays under 200ms." Without them, every architectural rule is enforced by goodwill — which doesn't survive deadlines. | ☐ |
| 10 | The architecture has been challenged by someone other than its authors in the last six months ‖ Architectures rot when only their authors review them. Schedule external review — a senior engineer from another team, an architect from another practice, an alumni who knows the domain. Fresh eyes catch the assumptions you can no longer see. | ☐ |

---

## Related

[`principles/ai-native`](../../principles/ai-native) | [`principles/domain-specific`](../../principles/domain-specific) | [`principles/modernization`](../../principles/modernization) | [`frameworks/togaf`](../../frameworks/togaf) | [`governance/review-templates`](../../governance/review-templates) | [`anti-patterns/distributed-monolith`](../../anti-patterns/distributed-monolith)

---

## References

1. [David Parnas — Information Hiding](https://en.wikipedia.org/wiki/Information_hiding) — *Wikipedia*
2. [Fred Brooks — The Mythical Man-Month](https://en.wikipedia.org/wiki/The_Mythical_Man-Month) — *Wikipedia*
3. [Robert C. Martin — The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) — *cleancoder.com*
4. [Alistair Cockburn — Hexagonal Architecture (Ports and Adapters)](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)) — *Wikipedia*
5. [Martin Fowler — Patterns of Enterprise Application Architecture Catalog](https://martinfowler.com/eaaCatalog/) — *martinfowler.com*
6. [Gang of Four — Design Patterns](https://en.wikipedia.org/wiki/Design_Patterns) — *Wikipedia*
7. [Dan McKinley — Choose Boring Technology](https://boringtechnology.club/) — *boringtechnology.club*
8. [Ford, Parsons, Kua — Building Evolutionary Architectures](https://www.thoughtworks.com/insights/blog/microservices/evolutionary-architecture) — *Thoughtworks Insights*
9. [Architecture Decision Records (ADRs)](https://adr.github.io/) — *adr.github.io*
10. [Gregor Hohpe — The Architect Elevator](https://architectelevator.com/) — *architectelevator.com*
