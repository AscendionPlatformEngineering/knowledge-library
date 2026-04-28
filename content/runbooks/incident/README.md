# Incident Runbook

The artefact a responder picks up at 3 AM when a specific class of incident fires — recognising that the runbook is the moment-of-truth interface between institutional knowledge and individual responder bandwidth, and that its structure, calibration, and discoverability determine whether the responder resolves the incident or compounds it.

**Section:** `runbooks/` | **Subsection:** `incident/`
**Alignment:** Google SRE Workbook | PagerDuty Incident Response | Atlassian Incident Handbook | Atul Gawande — The Checklist Manifesto

---

## What "incident runbook" means — and how it differs from "incident response"

This page is about the runbook as a designed artefact. The discipline of running incident response — detection, severity routing, coordination roles, blameless post-mortems, MTTD/MTTR as engineering metrics — lives in [`observability/incident-response`](../../observability/incident-response). That page covers *how the organisation handles incidents as an operational discipline*. This page covers *the document the responder reaches for once an incident is declared*: the runbook for "the database is rejecting connections," the runbook for "checkout is returning 5xx," the runbook for "the queue depth is climbing past threshold X." Two pages, two audiences, two update cadences, two failure modes.

A *primitive* runbook is what most teams have: a wiki page somewhere with prose like "if you see this alert, check the dashboard, then look at logs, then maybe restart the service." It exists; nobody can find it at 3 AM; the sections that the responder needs aren't where the responder is looking; and what the document teaches the responder is "use your judgment from here," which means the runbook is doing zero work and the responder is operating from individual knowledge plus the time pressure of an active incident.

A *production* incident runbook is a designed artefact with structural properties. It corresponds to a specific *incident class* (a category of incidents that have similar signatures, similar causes, similar remediations). It has a documented *trigger condition* (what alert or signal indicates that this runbook applies). It has *executable steps* with explicit branching for known unknowns ("if the queue depth is above 10000, do X; below 10000, do Y"). It has *verification* (how to know each step worked, how to know the incident is resolved). It is *discoverable* from the alert itself — the alert links to the runbook, the runbook is in the same tooling the responder is already in, no context-switching to find it. It has a *lifecycle* tied to the incident class — proposed when the class first emerges, refined through use, deprecated when the class no longer occurs because the underlying cause has been engineered away.

The architectural shift is not "we wrote some runbooks." It is: **incident runbooks are designed artefacts whose structure, calibration, discoverability, and lifecycle determine whether institutional knowledge is operationally available at the moment of pressure — and treating runbooks as documentation rather than as instruments of operation produces wikis full of prose that nobody can use when it matters.**

---

## Six principles

### 1. One runbook per incident class — generic runbooks fail at the moment they're needed

A common pattern: an organisation has a single "incident runbook" that's meant to apply to all incidents. It opens with "first, declare the incident" and proceeds through generic steps that any incident response would follow. By the time the responder reaches the part of the document that's specific to their actual problem (if such a part exists), they've waded through five pages of process they already know. Worse: the document offers no specific guidance on the particular failure mode they're facing because it's trying to be useful for everything. The architectural answer is one runbook per *incident class* — a category of incidents that share signatures, causes, and remediations. "Database connection pool exhaustion" gets its own runbook with specific symptoms, specific diagnostic queries, specific remediation steps. "API rate limit threshold breached on dependency X" gets its own runbook. The discipline takes more authoring work; it produces runbooks that actually help when called upon.

#### Architectural implications

- Incident classes are named explicitly with documented characteristics — what alert signals indicate this class, what symptoms users see, what underlying cause produces it.
- One runbook per class — not one master runbook with sections for different classes, but distinct artefacts that the alerting system can link to specifically.
- The class taxonomy is itself a designed artefact, reviewed periodically — new classes emerge as new incidents recur, classes consolidate when they prove to share enough structure, classes retire when their underlying cause is engineered away.
- Generic process content (declare the incident, assemble responders, document the timeline) lives in process documentation — not duplicated into every runbook, but referenced where the runbook needs to invoke it.

#### Quick test

> Pick the most recent incident in your organisation. Was there a specific runbook for that incident's class — with specific diagnostic steps and specific remediation guidance — or did the responder rely on a general document plus their judgment? If the latter, the runbook layer is doing less work than it could be, and the responder's individual bandwidth determined the outcome.

#### Reference

[Google SRE Workbook — Operational Continuity](https://sre.google/workbook/) covers the per-incident-class runbook discipline at practitioner depth. [Atul Gawande — The Checklist Manifesto](https://atulgawande.com/book/the-checklist-manifesto/) covers the general principle of class-specific checklists in high-stakes domains; the same architecture applies to incident runbooks — generic checklists fail where class-specific ones succeed.

---

### 2. Three-part structure — trigger condition, executable steps, verification

The internal structure of a useful incident runbook has three parts. First, the *trigger condition*: what specific alert or signal indicates that this runbook applies. Without a clear trigger, the responder doesn't know whether they're in the right runbook (and either reads a runbook that isn't theirs, wasting time, or skips over the right one because they couldn't tell). Second, the *executable steps*: the specific actions to take, in order, with whatever branching is needed for known variations. The steps are imperative ("run this query," "check this dashboard," "restart this service") with concrete artefacts (specific queries, specific URLs, specific commands) — not aspirational prose. Third, the *verification*: how to know each step worked, and how to know the incident is resolved. Verification is what distinguishes "I followed the runbook" from "I resolved the incident." Each part can be evaluated independently for whether it serves the responder; missing or weak parts produce predictable failure modes.

#### Architectural implications

- Each runbook opens with its trigger condition stated explicitly — the alert name, the dashboard signature, the threshold value — so the responder confirms in seconds that they're in the right document.
- Steps are imperative and concrete: "Run `psql -c 'SELECT count(*) FROM connections'` against the primary; if greater than 80% of max_connections, proceed to step 3" — not "investigate connection state."
- Each step has its own verification criterion: "expected output: count below 1000" — so the responder knows whether to proceed or escalate.
- The runbook ends with a global verification: "the incident is resolved when X metric returns to baseline AND Y user-facing surface is healthy." Resolution is defined, not inferred.

#### Quick test

> Pick a runbook in your organisation. Does it have an explicit trigger condition (the responder knows in seconds whether this runbook applies)? Are its steps imperative with concrete artefacts (commands, queries, URLs) rather than aspirational prose ("investigate the issue")? Does each step have verification, and is incident resolution explicitly defined? If any are missing or weak, the runbook is leaving work for the responder to invent under pressure.

#### Reference

[The Checklist Manifesto — Atul Gawande](https://atulgawande.com/book/the-checklist-manifesto/) treats the structure of high-stakes checklists in detail; the trigger-action-verification structure transfers directly to incident runbooks. [Google SRE Workbook — Practical Alerting](https://sre.google/workbook/) covers the alert-to-runbook linking that makes trigger conditions actionable.

---

### 3. Branching for known unknowns — runbooks that handle variation are worth more than runbooks that don't

A real incident class has variations. The "database connection pool exhaustion" runbook needs to handle the case where the cause is a slow query (different remediation than a connection leak), and the case where the cause is a downstream dependency timing out (different again). The runbook can pretend the cases are the same — and produce wrong actions for two of three cases — or it can branch explicitly: "Step 4: check the slow query log. If queries are above N seconds, proceed to step 5a. If queries are normal but connections are stuck open, proceed to step 5b. If neither, proceed to step 5c." The branching makes the runbook longer but distinctly more useful, because the cases the runbook actually covers are the cases the responder actually faces. The architectural discipline is to recognise where variation matters and to encode it explicitly, not to paper over it with prose like "use your judgment."

#### Architectural implications

- Decision points in the runbook are explicit: "if X, do A; if Y, do B; if neither, escalate" — not embedded in prose that the responder has to interpret.
- The branches are mutually exclusive and collectively exhaustive (or there's a clear "neither — escalate" branch that handles the leftover).
- Branches that prove to occur with similar frequency may be candidates for separate runbooks; the runbook structure reflects what the responder actually needs to handle.
- Branches that prove to never occur in practice are candidates for retirement; the runbook stays focused on cases that actually happen.

#### Quick test

> Pick a runbook for an incident class your organisation has handled multiple times. Does the runbook explicitly cover the variations that have actually occurred — different root causes, different remediations — with explicit branching? Or does it cover one case and leave the others to the responder's judgment? If the latter, the runbook is doing only the work for the most common case, and the second-most-common case is being handled badly each time.

#### Reference

[The Checklist Manifesto — Atul Gawande](https://atulgawande.com/book/the-checklist-manifesto/) covers the read-do checklist (read each step, then act) versus do-confirm (act, then verify) distinction; the branching pattern this principle requires is a read-do checklist with explicit decision points. The aviation industry's [QRH (Quick Reference Handbook)](https://en.wikipedia.org/wiki/Quick_reference_handbook) for emergency procedures is the canonical reference for branching emergency-response artefacts.

---

### 4. Runbooks are calibrated through use — what didn't work in the last incident becomes the next revision

A runbook is rarely correct on its first version. The author's mental model of the incident class doesn't fully match the reality the responders face; steps that seemed clear in calm reflection turn out to be ambiguous under pressure; commands that were correct at authoring time become wrong as the system evolves. The discipline is to treat the runbook as a living artefact calibrated through use: every time a runbook is invoked, the post-incident review surfaces what worked, what was unclear, what was wrong, and what was missing — and the runbook is updated based on those findings before the next time the same class fires. Runbooks that aren't used produce no calibration signal; runbooks that are used but not updated calcify into wrong-but-trusted documents whose errors persist for years.

#### Architectural implications

- Every runbook invocation produces a brief post-incident note: was the runbook applicable, did it cover the case faced, were any steps unclear or wrong, what's missing?
- Findings feed into a queue of runbook revisions, prioritised by frequency of class occurrence and severity of the gap.
- Revisions are themselves versioned and reviewed — the change is documented (what changed, why, which incident motivated it), and the revision is reviewed by someone who didn't author it.
- Runbooks that haven't been invoked in a long time are flagged for review — either the class no longer occurs (candidate for retirement), or the runbook isn't being found at incident time (discoverability problem).

#### Quick test

> Pick the most-invoked runbook in your organisation. When was it last revised, what motivated the revision, and how many findings from invocations are currently in the queue waiting to be addressed? If the answers are "we don't track that" or "we last revised it years ago," the runbook is calcifying — and the gaps that current responders are working around are the next responder's problems too.

#### Reference

[Etsy — How to Conduct a Postmortem (Allspaw)](https://www.etsy.com/codeascraft/blameless-postmortems) treats post-incident learning at the discipline level; the same learning applies to runbook revision specifically. [Google SRE Book — Postmortem Culture](https://sre.google/sre-book/postmortem-culture/) covers how post-incident findings translate into engineering changes, including runbook updates.

---

### 5. Discoverability under pressure — the runbook the responder can't find is worth nothing

A perfect runbook that the responder can't find at 3 AM is operationally equivalent to no runbook. Discoverability is the architectural property that determines whether all the careful authoring work pays off in practice. The discipline has several layers. *Alert-to-runbook linking* — the alert that fires includes a direct link to the runbook for that incident class — is the most important one; the responder who's already looking at the alert is one click away from the runbook, with no search needed. *Tooling integration* — the runbook is in the same tooling the responder is already in (the chat platform, the incident management system, the alerting platform), not on a wiki that requires a separate login — keeps the responder in flow. *Naming and tagging conventions* — runbooks are named consistently and tagged with the incident-class taxonomy, so search at least works for cases where alert-to-runbook linking is missing. The discipline is to recognise that authoring a runbook nobody can find is doing zero operational work.

#### Architectural implications

- Every alert that should trigger a runbook includes a direct link to the runbook — embedded in the alert payload, the notification, the ticket, the status page entry.
- Runbooks are stored in tooling integrated with the alerting and incident-management surfaces — the responder doesn't context-switch to a separate wiki to find the runbook.
- The runbook URL is stable: it survives renames, reorganisation, and tooling migrations; broken links from years-old alerts are recognised as a regression to fix, not normal decay.
- Naming conventions and incident-class taxonomy tags make search work as a fallback path: a responder facing an unrecognised alert can search for the closest-matching incident class and find related runbooks.

#### Quick test

> Pick a recent incident in your organisation. From the alert that fired, how many clicks did it take to reach the runbook for that incident class? If the answer is "we found it eventually" or "we used Slack search," discoverability is operating on luck — and at 3 AM with adrenaline, the search-by-luck path frequently doesn't end at the right runbook.

#### Reference

[PagerDuty Incident Response — Runbooks](https://response.pagerduty.com/training/incident_response/) covers the alert-to-runbook linking and tooling integration as first-class operational concerns. [Google SRE Workbook — On-Call](https://sre.google/workbook/being-on-call/) treats discoverability under pressure as a primary architectural property of the runbook system.

---

### 6. Runbook lifecycle is tied to incident-class lifecycle — proposed, in-use, deprecated

A runbook isn't permanent. It's tied to a specific incident class, and that class has its own lifecycle: it emerges when a kind of incident first occurs, becomes a recognised class once it recurs enough times to be worth a dedicated runbook, becomes mature as the runbook is calibrated through use, and eventually retires when the underlying cause is engineered away (the database that kept exhausting connections gets a connection pool with proper limits, and the class stops occurring). Each phase has different runbook properties: a *proposed* runbook is the first attempt at handling a newly-recognised class, expected to be revised heavily; an *in-use* runbook is mature, calibrated, and trusted for the class it covers; a *deprecated* runbook is one whose class no longer occurs but is kept for historical reference and in case the cause re-emerges. The architectural discipline is to treat runbooks as having lifecycle status — visible to responders, queryable in tooling — rather than as an undifferentiated pile of documents accumulating over time.

#### Architectural implications

- Each runbook has documented lifecycle status: proposed (new, expected to revise), in-use (mature and trusted), deprecated (class no longer occurs).
- Status is visible to responders — a proposed runbook's status warns the responder that this is a first attempt; an in-use runbook is the trusted reference; a deprecated runbook explains why and what to do if the underlying class re-emerges.
- The status is updated as the runbook matures or as the underlying cause is engineered away — not left at the initial value forever.
- Deprecated runbooks are not deleted; they're retained with their deprecation note, so a responder facing a re-emerged class has institutional memory available rather than starting from scratch.

#### Quick test

> Pick five runbooks in your organisation. For each, what's the lifecycle status — proposed, in-use, deprecated, unknown? When was status last reviewed? If status doesn't exist or hasn't been reviewed, the runbook layer is operating without lifecycle discipline — and proposed runbooks (untrustworthy) sit alongside mature ones (trustworthy) without distinction.

#### Reference

The lifecycle discipline is treated implicitly in [Google SRE Workbook — Operational Continuity](https://sre.google/workbook/) (mature runbooks vs. emerging ones), and explicitly in [PagerDuty Incident Response](https://response.pagerduty.com/) (runbook status fields). The conceptual framing transfers from how mature open-source projects handle documentation lifecycle generally.

---

## Architecture Diagram

The diagram below shows the canonical incident-runbook architecture: the incident-class taxonomy as the organising principle; one runbook per class with documented trigger / steps / verification structure; alert-to-runbook linking that makes the runbook discoverable from the alert; the post-incident learning loop where runbook invocations produce findings that feed back into revisions; the lifecycle status (proposed / in-use / deprecated) tracked alongside each runbook.

---

## Common pitfalls when adopting incident-runbook thinking

### ⚠️ The all-purpose runbook

A single document tries to cover all incidents. It opens with generic process and never reaches the specifics the responder needs. Generic at every point; useful at none.

#### What to do instead

One runbook per incident class. Class-specific symptoms, diagnostics, remediations. Generic process content lives in process documentation, referenced where needed.

---

### ⚠️ Aspirational prose where executable steps belong

Steps read "investigate the issue," "check the relevant logs," "consider whether to escalate." The responder has to translate prose into concrete actions while under pressure.

#### What to do instead

Imperative steps with concrete artefacts: specific commands, specific queries, specific URLs, specific thresholds. The responder reads the step, types the command, checks the output against the verification criterion.

---

### ⚠️ One-case-only runbook

The runbook covers one cause for the incident class. The other causes are handled by the responder's judgment, less well, every time the class fires.

#### What to do instead

Branching for known unknowns. Mutually-exclusive collectively-exhaustive decision points. Branches calibrated through use; rare branches retired, common branches potentially split into their own runbooks.

---

### ⚠️ The runbook nobody can find

The runbook exists. The responder at 3 AM can't find it through alert linking, search, or tooling integration. The careful authoring work pays zero dividends.

#### What to do instead

Alert-to-runbook linking embedded in alerts. Runbooks in tooling integrated with the alerting and incident-management surfaces. Stable URLs. Naming and tagging that make fallback search work.

---

### ⚠️ The runbook that hasn't been touched in years

The runbook was authored for the system as it existed three years ago. The system has changed. Half the commands are wrong; half the URLs are broken; the responders who use it work around the wrong parts based on tribal knowledge.

#### What to do instead

Calibration through use. Every invocation produces a finding queue. Revisions are versioned, motivated, and reviewed. Runbooks that haven't been invoked in a long time are flagged for review or retirement.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Incident classes are named explicitly with documented characteristics ‖ The class taxonomy is the organising principle. New classes emerge as incidents recur; classes consolidate or retire as patterns become clear. The taxonomy is reviewed periodically. | ☐ |
| 2 | One runbook per incident class — class-specific symptoms, diagnostics, remediations ‖ Generic master runbooks fail at the moment they're needed. Class-specific runbooks do the operational work. Generic process content lives separately, referenced as needed. | ☐ |
| 3 | Each runbook has explicit trigger condition stated upfront ‖ The responder confirms in seconds whether this runbook applies. Alert name, dashboard signature, threshold value — explicit, not embedded in prose. | ☐ |
| 4 | Steps are imperative with concrete artefacts — specific commands, queries, URLs, thresholds ‖ "Run psql -c '...'" not "check the database state." The responder reads, acts, checks; the runbook minimises the in-pressure translation work. | ☐ |
| 5 | Each step has its own verification criterion; resolution is explicitly defined ‖ "I followed the runbook" is distinguished from "I resolved the incident." Step-level verification informs the next decision; resolution definition prevents premature claim-of-resolution. | ☐ |
| 6 | Decision points are explicit with mutually-exclusive collectively-exhaustive branches ‖ "If X, do A; if Y, do B; if neither, escalate." Branching for known unknowns. The runbook handles the variation that occurs in practice, not just the most common case. | ☐ |
| 7 | Every alert that should trigger a runbook includes a direct link to it ‖ Alert-to-runbook linking embedded in the alert payload. The responder is one click from the runbook, no search needed. The most important discoverability primitive. | ☐ |
| 8 | Runbooks are stored in tooling integrated with alerting and incident-management surfaces ‖ The responder doesn't context-switch to a wiki. Runbooks live where the responder is already working — chat platform, incident system, alerting tool. | ☐ |
| 9 | Calibration loop — every invocation produces findings; revisions are versioned and reviewed ‖ Runbooks are living artefacts. What didn't work in the last incident becomes the next revision. Runbooks that calcify produce wrong-but-trusted documents whose errors persist. | ☐ |
| 10 | Lifecycle status is tracked per runbook — proposed, in-use, deprecated ‖ Status is visible to responders. Proposed runbooks are flagged as first attempts; in-use are trusted; deprecated retain institutional memory for re-emerging classes. | ☐ |

---

## Related

[`runbooks/migration`](../migration) | [`runbooks/rollback`](../rollback) | [`observability/incident-response`](../../observability/incident-response) | [`observability/sli-slo`](../../observability/sli-slo) | [`checklists/architecture`](../../checklists/architecture) | [`governance/checklists`](../../governance/checklists)

---

## References

1. [Google SRE Workbook](https://sre.google/workbook/table-of-contents/) — *sre.google*
2. [PagerDuty Incident Response](https://response.pagerduty.com/) — *response.pagerduty.com*
3. [Atlassian Incident Handbook](https://www.atlassian.com/incident-management/handbook) — *atlassian.com*
4. [The Checklist Manifesto — Atul Gawande](https://atulgawande.com/book/the-checklist-manifesto/) — *atulgawande.com*
5. [Etsy — How to Conduct a Postmortem](https://www.etsy.com/codeascraft/blameless-postmortems) — *etsy.com*
6. [Google SRE Book — Postmortem Culture](https://sre.google/sre-book/postmortem-culture/) — *sre.google*
7. [Runbook (Wikipedia)](https://en.wikipedia.org/wiki/Runbook) — *Wikipedia*
8. [Game Days (Google SRE)](https://sre.google/sre-book/testing-reliability/) — *sre.google*
9. [Distributed Systems Observability (Cindy Sridharan)](https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/) — *oreilly.com*
10. [ITIL Incident Management](https://www.axelos.com/certifications/propath/itil-4) — *axelos.com*
