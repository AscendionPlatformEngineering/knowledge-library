# Governance Roles

Who has the authority to decide, who must be consulted, who is informed, and who is accountable when a class of architectural decision is made — recognising that "the architects decide" is rarely a complete answer, that authority and accountability must match, and that the role architecture of the governance system is itself a designable property of how the organisation functions at scale.

**Section:** `governance/` | **Subsection:** `roles/`
**Alignment:** RACI Matrix | Architecture Advice Process (Andrew Harmel-Law) | Team Topologies | Apache Project Governance

---

## What "governance roles" actually means

A *small organisation* can govern by proximity: the senior engineer or the founder makes architectural decisions, everyone knows it, the role is implicit in the org chart, and it works. The role structure exists but isn't articulated because it doesn't need to be. A *large organisation* cannot govern by proximity: there are too many decisions, too many teams, too many concurrent threads for any single role to cover. Without articulated roles, decisions either bottleneck on the few authoritative voices (slowing the organisation), or get made locally without alignment (producing drift and exceptions). The architectural response is to design the role structure — which roles exist, what authority each role has over which decision classes, who they consult, who they answer to — and to make this visible enough that the organisation can route decisions to the right place at the right time.

The role structure is not a single hierarchy. Different decision classes have different authority patterns. A change to authentication policy may require ARB approval and security-team consult; a change to a service's internal cache may be entirely within the team's authority; a change to a regulatory data-residency posture may require legal sign-off and CTO awareness. The pattern of *who decides what* is the role structure, and the patterns differ by decision class — RACI matrices are the canonical articulation, with each row a decision class and each column a role.

The architectural shift is not "we wrote down who's responsible for what." It is: **the role structure is a piece of organisational architecture with its own design properties — authority must match accountability, capacity must match flow, the structure must adapt as the organisation grows — and treating it as an HR concern rather than an architectural one produces a governance system that scales worse than the technology it governs.**

---

## Six principles

### 1. Different decision classes have different RACI patterns — and treating them uniformly produces both bottlenecks and gaps

A common pattern: an organisation defines "the architects" as responsible for architectural decisions, period. The role pattern is uniform, the answer to "who decides?" is the same regardless of decision class. The result is that high-volume routine decisions (which library to use for an internal service, which deployment pattern for a non-critical workload) bottleneck on the architects — slowing the organisation — while high-stakes decisions outside the architects' expertise (regulatory data residency, financial-compliance trade-offs, vendor lock-in implications) get treated identically with the same review depth, sometimes inadequately. The architectural discipline is to recognise that decision classes differ and the RACI pattern should differ accordingly: routine technology choices may be team-decided with architectural input on request; cross-cutting standards may require ARB approval; high-stakes regulatory or financial decisions may require additional roles (legal, security, finance) in the consulted column.

#### Architectural implications

- Decision classes are named explicitly: routine technology choices, service-internal architecture, cross-service integration, cross-cutting standards, security policy, regulatory posture, vendor selection — each with documented characteristics.
- A RACI matrix exists with decision classes as rows and roles as columns; for each row, the cells are populated explicitly (not inferred from titles).
- The matrix is documented and queryable: a team facing a decision can look up which class it falls into and route accordingly, rather than asking "who do I need to talk to?" each time.
- The matrix is reviewed periodically: as the organisation grows or the decision-class mix shifts, the patterns may need updating.

#### Quick test

> Pick three decisions made in the last quarter — one routine, one cross-cutting, one high-stakes. For each, which role was Responsible, who was Accountable, who was Consulted, who was Informed? If the answer is the same across all three, the role pattern is uniform — and either routine decisions are bottlenecking on senior reviewers or high-stakes decisions are getting routine-level attention. Both failure modes hurt.

#### Reference

[RACI Matrix (Wikipedia)](https://en.wikipedia.org/wiki/Responsibility_assignment_matrix) — the canonical reference for the responsibility-assignment matrix; the four roles (Responsible, Accountable, Consulted, Informed) provide the working vocabulary for articulating governance roles. The architectural application of RACI to decision classes (rather than to projects or tasks) is treated extensively in [TOGAF](https://www.opengroup.org/togaf)'s governance guidance.

---

### 2. Authority must match accountability — you cannot be accountable for outcomes you don't control

A role can be made accountable for an outcome (system reliability, security posture, cost trajectory) without being given the authority to influence that outcome (deciding which patterns are used, blocking unsafe patterns, controlling resource allocation). This mismatch is one of the most common dysfunctions in architectural governance: the architecture team is "accountable" for system quality but lacks authority to block decisions that worsen it; the security team is "accountable" for security but is consulted only after architectural decisions are made and the unsafe paths are already chosen. Without authority to match accountability, the role becomes either (1) a futile-objection role — raising concerns that get overruled by people with more authority — or (2) a blame role — taking responsibility for outcomes determined by others' decisions. The architectural discipline is to align the two: where a role is accountable for an outcome, the role has authority to decide or block on inputs that determine that outcome; where authority is held elsewhere, accountability follows the authority.

#### Architectural implications

- For each role, accountability is named explicitly: what outcomes is this role accountable for? And authority is named explicitly: what decisions can this role make or block?
- The two are aligned: a role accountable for security has authority to block insecure patterns; a role accountable for cost has authority to require cost analysis before approval; a role accountable for reliability has authority to require reliability standards.
- Where authority is delegated to teams (subsidiarity), accountability is delegated with it — the team becomes accountable for outcomes within its authority, and the architectural role's accountability shifts to ensuring the team has the standards and tools to be accountable effectively.
- Mismatches are recognised as governance bugs and remediated: either authority is added (giving the role the ability to influence outcomes) or accountability is removed (recognising that this role doesn't actually own the outcome).

#### Quick test

> Pick a role in your governance system that's accountable for an architectural quality (security posture, cost, reliability). What's the role's authority to block decisions that worsen that quality? If the role has accountability without corresponding authority, the role is structurally set up to fail — the next outcome failure will reveal the mismatch.

#### Reference

[Architecture Advice Process — Andrew Harmel-Law](https://martinfowler.com/articles/scaling-architecture-conversationally.html) treats the authority-accountability matching question explicitly, with a model that distributes decision-making authority while preserving advisory accountability — making the relationship between the two an architectural choice rather than an inherited assumption.

---

### 3. Centralised vs distributed governance is an architectural choice with explicit trade-offs

Governance can be centralised (decisions flow through a small number of authoritative roles — ARB, chief architect, principal engineers) or distributed (decisions are made by teams with reference to standards and patterns; central roles set the standards but don't decide each case). Both work. They have different trade-offs. *Centralised* governance produces high consistency, strong standards enforcement, and clear escalation paths — at the cost of decision-making throughput (the central roles are always the bottleneck) and team agency (teams accept what's decided rather than owning their decisions). *Distributed* governance produces high throughput, strong team ownership, and adaptability — at the cost of consistency (different teams reach different decisions), standards drift (without central enforcement, standards become advisory), and escalation difficulty (when a cross-cutting decision is needed, the structure for making it isn't in place). The architectural discipline is to choose deliberately, document the choice, and design the supporting structures (standards bodies for distributed, scaling-decision tooling for centralised) that mitigate the chosen approach's trade-offs.

#### Architectural implications

- The institution's choice of centralised, distributed, or hybrid governance is explicit, with documented reasoning and acknowledgment of trade-offs.
- Mitigations for the chosen approach are in place: centralised governance has tooling to scale decision throughput (delegation, decision templates, fast-track paths for routine cases); distributed governance has standards bodies, advice processes, and consistency-monitoring tooling.
- Hybrid approaches (some decision classes centralised, others distributed) name the decision classes per approach — not "it depends."
- The choice is reviewed periodically: as the organisation grows, the right balance may shift; centralised becomes infeasible past certain scales, distributed becomes unmanageable without tooling.

#### Quick test

> Where on the centralised-distributed spectrum is your governance, and where would your engineers say it is? If the answers differ, the gap is the actual operating model — and the espoused model is the goal you haven't reached. The next change to the governance system should be one that closes the gap rather than restating the espoused model.

#### Reference

[Apache Project Governance](https://www.apache.org/foundation/how-it-works.html) is a canonical example of a distributed governance model at scale (open-source projects across hundreds of communities), with explicit roles (committer, PMC, board) and decision processes (lazy consensus, voting). [Spotify Engineering Culture](https://engineering.atspotify.com/) documents a contrasting pattern of distributed governance with cross-cutting standards bodies (chapters, guilds, communities of practice).

---

### 4. ARB structure — composition, terms, recusal, conflicts of interest — is itself a designable property

When governance includes an Architecture Review Board (ARB) — a body that reviews high-stakes decisions — the ARB's structure is itself a piece of organisational architecture with design properties. *Composition*: who's on the board? Senior architects, principal engineers, product or business representatives, security and compliance leads? *Terms*: are members appointed indefinitely, or do they rotate? Indefinite terms produce institutional memory but also entrenched perspectives; rotating terms produce fresh perspectives but lose continuity. *Recusal*: how does the board handle members who have a conflict of interest in a decision (the proposal comes from their team, they advocate publicly for the chosen vendor, they have a personal relationship with the proposing engineer)? *Quorum*: how many members must be present to make a decision binding? *Tie-breaking*: when the board is split, who decides? The architectural discipline is to make these choices explicit rather than inheriting whatever structure happened to coalesce when the ARB was first formed — and to revisit the choices as the ARB matures and the organisation evolves.

#### Architectural implications

- ARB composition is documented with reasoning: which roles are represented, why, and how members are selected for those roles.
- Term length is documented: members serve for X years, with rotation patterns that maintain continuity (overlapping terms rather than full turnover).
- Conflict-of-interest and recusal policies are documented: how conflicts are declared, when recusal is required, what the board does when recusal would leave too few members.
- Quorum and tie-breaking rules are documented: how decisions are made when the board is split, who has the casting vote (often the chair), what happens when consensus can't be reached.

#### Quick test

> Pick your organisation's ARB (or equivalent). Who's on it, how long have they been on it, what happens when a member has a conflict of interest, and what happens when the board can't reach consensus? If any of these are unclear, the ARB is operating on tradition or improvisation rather than designed structure — and the next contentious decision will reveal the cracks.

#### Reference

[Apache Project Governance — Voting and Decision-Making](https://www.apache.org/foundation/voting.html) — the canonical reference for structured decision-making bodies in open-source governance, covering composition, voting rules, lazy consensus, and conflict-of-interest patterns at scale. The patterns transfer to enterprise ARBs with appropriate adaptation.

---

### 5. Review capacity is a constraint that shapes which roles must exist

A governance system can only review as many decisions as its reviewers have time to handle thoughtfully. If the rate of incoming decisions exceeds review capacity, queue grows: decisions wait, time-sensitive decisions slip, the team learns to bypass the system to ship on time. The architectural response is to recognise capacity as a constraint and design the role structure to match: more reviewers, more delegation, faster paths for routine decisions, decision authority promoted to lower levels for cases that don't need the highest-authority review. The opposite failure mode is also real: under-utilised reviewers (decision rate well below capacity) produces a governance system that searches for things to review, with bikeshedding (extensive review of trivial decisions because the reviewers have time) and missed-the-real-issue effects. Capacity should match flow — and the role structure is the lever that matches them.

#### Architectural implications

- Review capacity is measured: hours-per-reviewer-per-week, decisions-reviewed-per-week, queue depth, lead time from submission to decision.
- Capacity-vs-demand mismatches are recognised and remediated: high-demand-vs-low-capacity drives delegation, fast-track paths, or additional reviewers; low-demand-vs-high-capacity drives consolidation or repurposing.
- The role structure has documented capacity expectations: this role should spend X hours per week on architectural review; if more, escalate; if less, role may be over-provisioned.
- Lead-time SLAs exist for decision classes — routine decisions have a target turnaround of days, high-stakes decisions of weeks — and missed SLAs are tracked.

#### Quick test

> Pick the role most commonly described as "the architect" in your organisation. How many hours per week does this role spend on review work, and what's the queue depth they face? If the answer is "essentially full-time" with non-trivial queue, the role is at or beyond capacity, and the governance system is bottlenecking. If the answer is "very little, but they could do more," the role is over-provisioned, and the governance system may be searching for things to review.

#### Reference

[Architecture Advice Process — Andrew Harmel-Law](https://martinfowler.com/articles/scaling-architecture-conversationally.html) frames decision-making capacity as a primary architectural concern at scale; the advice process is itself a response to the capacity problem (distributing decision authority to teams while preserving cross-cutting awareness through advice-seeking). [DORA Metrics](https://dora.dev/) treats lead time as a first-class engineering metric; the discipline transfers to architectural-decision lead time as a measurable governance health signal.

---

### 6. Promoting decision authority to lower levels is a governance pattern, not a loss of control

Centralised governance accumulates authority at high levels; the longer the organisation runs in this pattern, the more decisions live at high levels and the slower the organisation gets. The architectural response is to promote decision authority to lower levels deliberately: a class of decisions that previously required ARB review now requires only team-lead approval; a class that previously required architect review now requires only a team-decision recorded as an ADR. The pattern is the same as classical delegation: standards become the higher-level concern (what patterns are approved, what trade-offs are required to be considered), enforcement becomes lower-level (the team-lead or the team itself ensures compliance), exceptions are escalated. This is not a loss of control — it's a re-architecting of where control lives. Done well, the senior roles spend more time on the decisions where their judgment actually matters; the lower roles take ownership of decisions they understand best; the organisation's overall throughput improves; and the senior roles become available for the cross-cutting concerns that only they can address.

#### Architectural implications

- The role structure includes a deliberate practice of promoting decision authority downward as decision classes mature (routine pattern selection moves from "ARB review" to "team-lead approval" to "team decision") — with the criteria for promotion documented.
- Standards and patterns are kept current and discoverable so that lower-level decision-makers have what they need to decide well — without this, promotion becomes abdication.
- Escalation paths are clear: when a decision encountered at a lower level genuinely warrants higher-level attention, the path to escalate is explicit and used routinely without stigma.
- The senior roles' time becomes more focused on cross-cutting concerns, novel decision classes, and exception review — the work that genuinely requires their authority — rather than on routine-decision rubber-stamping.

#### Quick test

> Pick a class of decisions that currently requires ARB review in your organisation. Could it be promoted — to team-lead approval, to team decision recorded as ADR — without losing institutional quality? If yes, the class is a candidate for promotion, and not promoting it is keeping the ARB busy with work it doesn't add unique value to. If no, what would have to be true (better standards, better tooling, better reviewer capacity at lower levels) to make promotion safe?

#### Reference

[Team Topologies — Skelton & Pais](https://teamtopologies.com/) frames decision-authority placement as a primary organisational architectural concern, with patterns (stream-aligned teams, platform teams, enabling teams) that distribute different decision classes to different team types. The architectural framing of decision authority as a designable property — promoted down deliberately, escalated up as needed — is consistent with how mature open-source projects handle the same problem at internet scale.

---

## Architecture Diagram

The diagram below shows the canonical governance-roles architecture: decision classes at the input; the RACI matrix mapping decision classes to roles; the ARB as a structured decision body with documented composition, recusal, and quorum; tier-based authority levels (team, ARB, executive) with documented escalation paths; advice and consult relationships running across; capacity telemetry monitoring lead time and queue depth.

---

## Common pitfalls when adopting governance-roles thinking

### ⚠️ The uniform RACI

The institution treats all architectural decisions identically: the architects decide everything, full stop. Routine decisions bottleneck on the architects, slowing the organisation. High-stakes decisions get the same review depth as routine ones, sometimes inadequately. The role pattern is uniform; the costs are paid in slow throughput and missed risks.

#### What to do instead

A RACI matrix with decision classes as rows. Different decision classes get different role patterns. Routine technology decisions are team-led with optional architectural advice; cross-cutting standards require ARB approval; high-stakes decisions add legal, security, or finance roles. The pattern matches the decision class.

---

### ⚠️ Accountability without authority

The architecture team is "accountable" for system quality but doesn't have authority to block bad patterns. The security team is "accountable" for security but is only consulted after architectural decisions are committed. Outcomes are owned without the inputs that produce them being controlled.

#### What to do instead

For each role's accountability, document the corresponding authority. A role accountable for security has authority to block insecure patterns. A role accountable for cost has authority to require cost analysis. Where authority is delegated to teams, accountability follows.

---

### ⚠️ The ARB that hasn't reviewed its own structure

The ARB was formed five years ago. The same five people are on it. Conflicts of interest are handled informally. Quorum and tie-breaking are not documented. New decision classes have emerged that the ARB doesn't reach into. The structure has calcified, and the legitimacy of its decisions is gradually eroding because its operating rules are opaque.

#### What to do instead

ARB composition, terms, recusal, quorum, and tie-breaking are documented. Periodically reviewed — at least annually — for whether the structure still fits the organisation. Members rotate over documented terms. Conflicts of interest are declared and recorded.

---

### ⚠️ Capacity ignored

The architects are at capacity — full-time on review work, queue is days deep, team-leads are bypassing the system to ship on time. Nobody measures this; nobody acts on it. The system formally requires architectural review for class X; in practice, half of class-X decisions ship without it because the reviewers can't keep up.

#### What to do instead

Capacity is measured. Lead time and queue depth are tracked. Capacity-vs-demand mismatches are remediated: more reviewers, more delegation, faster paths for routine cases, decision authority promoted to lower levels.

---

### ⚠️ Decision authority concentrated and never re-evaluated

Five years ago, all architectural decisions required ARB approval. The organisation has grown 5x. The ARB still reviews everything. The bottleneck is structural; the throughput is permanently constrained. Nobody asks whether each decision class still warrants ARB-level review — the question hasn't been on the agenda.

#### What to do instead

Periodic review of decision classes for promotion. Routine pattern selection that's stable enough moves from ARB review to team-lead approval. Standards and patterns are kept current to support lower-level decision-making. Senior roles' time becomes focused on the decisions that genuinely require their judgment.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Decision classes are named explicitly with documented characteristics ‖ Routine technology choices, cross-cutting standards, security policy, regulatory posture, vendor selection — each its own class. The class structure is the precondition for differentiated RACI patterns. | ☐ |
| 2 | A RACI matrix maps decision classes to roles with explicit cells (R, A, C, I) per class ‖ Each decision class has documented Responsible, Accountable, Consulted, and Informed roles. The matrix is queryable; teams can route decisions to the right place without ad-hoc discovery. | ☐ |
| 3 | Authority and accountability are aligned per role ‖ Where a role is accountable for an outcome, it has authority to influence inputs. Mismatches are recognised as governance bugs and remediated. The role structure isn't set up to fail. | ☐ |
| 4 | The institution's choice on the centralised-distributed spectrum is explicit, with mitigations for that choice's trade-offs ‖ Centralised governance has decision-throughput tooling; distributed has standards bodies and advice processes; hybrid documents which classes follow which approach. The choice is deliberate. | ☐ |
| 5 | ARB composition, terms, recusal, quorum, and tie-breaking are documented and periodically reviewed ‖ The ARB's operating structure is itself a designed property, not inherited from formation. Reviewed annually for fit with the current organisation. | ☐ |
| 6 | Conflicts of interest are declared and recorded; recusal policies are clear ‖ Members declare conflicts proactively. Recusal is documented when it happens. Quorum policies handle the case where recusal would leave too few members. | ☐ |
| 7 | Review capacity is measured per role — hours, queue depth, lead time ‖ Capacity is operational data. Capacity-vs-demand mismatches are recognised and remediated. The governance system has an honest view of whether it's serving its decision flow. | ☐ |
| 8 | Lead-time SLAs exist for decision classes; missed SLAs are tracked ‖ Routine decisions have target turnaround of days, high-stakes of weeks. The system is held accountable to its own response times, not just to its decisions' content. | ☐ |
| 9 | Decision authority is periodically promoted downward as decision classes mature ‖ The role structure isn't static. As patterns stabilise, the authority to apply them moves to lower levels. Senior roles become focused on novel and cross-cutting decisions. | ☐ |
| 10 | Escalation paths are clear and used without stigma ‖ When a decision encountered at a lower level genuinely warrants higher attention, the path to escalate is explicit and used routinely. Promotion of authority downward depends on the safety net of escalation upward when needed. | ☐ |

---

## Related

[`governance/checklists`](../checklists) | [`governance/review-templates`](../review-templates) | [`governance/scorecards`](../scorecards) | [`adrs`](../../adrs) | [`patterns/structural`](../../patterns/structural)

---

## References

1. [RACI Matrix (Wikipedia)](https://en.wikipedia.org/wiki/Responsibility_assignment_matrix) — *Wikipedia*
2. [Architecture Advice Process — Andrew Harmel-Law](https://martinfowler.com/articles/scaling-architecture-conversationally.html) — *martinfowler.com*
3. [Team Topologies](https://teamtopologies.com/) — *teamtopologies.com*
4. [Apache Project Governance](https://www.apache.org/foundation/how-it-works.html) — *apache.org*
5. [Spotify Engineering Culture](https://engineering.atspotify.com/) — *atspotify.com*
6. [Kubernetes Governance](https://kubernetes.io/community/) — *kubernetes.io*
7. [TOGAF](https://www.opengroup.org/togaf) — *opengroup.org*
8. [DORA Metrics](https://dora.dev/) — *dora.dev*
9. [Conway's Law (Wikipedia)](https://en.wikipedia.org/wiki/Conway%27s_law) — *Wikipedia*
10. [ADR — Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — *cognitect.com*
