# Scorecard Template

The artefact that rates a service across architecturally important dimensions — recognising that the scorecard's documented per-dimension criteria, level-based scoring (not aspirational numerics), calibration against actual operational outcomes, aggregation into portfolio views without reduction to a single composite number, owner-driven completion with peer review, and tracked improvement trajectory over time are what determine whether the scorecard becomes a portfolio-visibility instrument that drives investment decisions or a one-time exercise that produces ratings nobody trusts or revisits.

**Section:** `templates/` | **Subsection:** `scorecard-template/`
**Alignment:** Google SRE Workbook — Production Readiness Reviews | CNCF Cloud Native Maturity Model | DORA — DevOps Research and Assessment | Backstage — Software Catalog

---

## What "scorecard template" means — and how it differs from "checklists" and "ADRs"

This page is about the *scorecard template* — the structured instrument used to rate a service across multiple architectural dimensions and produce a per-dimension level that aggregates into a portfolio view of the organisation's engineering health. Three artefact families adjacent to this page need disambiguating up front. [`checklists/*`](../../checklists) are *per-change instruments* with binary pass/fail outcomes that gate a specific review or release; the question is "did this change meet the bar?" — applied many times, one change at a time. [`templates/adr-template`](../adr-template) is a *decision-record artefact* used at the moment a specific architectural decision is made; the question is "what did we choose, and why?" — applied per decision. The *scorecard template* is a *portfolio instrument* applied per-service, periodically, across multiple dimensions; the question is "where does this service stand on each dimension we care about, and which dimensions need investment?" — applied per service, repeatedly over time, to produce a multi-axis rating that supports investment decisions across a portfolio of services.

A *primitive* scorecard is what gets produced when "we should rate our services": a one-off spreadsheet circulated by a senior engineer; a single number from 1 to 10 per service representing "overall health"; a survey filled in by service owners with no documented criteria; a list of yes/no questions whose results are summed into a percentage. The instrument exists; ratings get assigned; a leadership review consumes the ratings; nothing improves. The criteria weren't documented, so reviewers and owners disagreed about what "good" meant on each dimension. The scoring was numeric, so a service rated 7/10 on security and a service rated 7/10 on observability looked equivalent despite measuring entirely different things. The single composite number averaged out signals that should have been visible separately. The exercise was point-in-time, so trends were invisible. Six months later the scorecard hasn't been updated; nobody trusts it; nobody references it.

A *production* scorecard is a *designed multi-dimensional rating instrument*. Its *dimensions* are explicit architectural concerns the organisation has decided to track — production readiness, observability, security posture, reliability, performance, cost efficiency, evolvability — chosen because they are the areas where investment decisions need to be made. Its *per-dimension criteria* are documented at the level granularity that the scoring uses: what does L1 mean for observability versus what does L4 mean, with the criteria written so that two reviewers looking at the same service produce the same rating. Its *scoring is level-based not numeric*: L1/L2/L3/L4 (or Bronze/Silver/Gold/Platinum, or any documented vocabulary) where each level represents a *qualitative state* the service has reached, calibrated against documented criteria, *not a numeric point on a continuous scale*. Its *calibration* comes from operational outcomes: a service rated L3 on reliability that suffered three sev-1 incidents this quarter signals the L3 criteria don't capture what reliability actually means, and the criteria get revised. Its *aggregation* produces a *portfolio view* — services as rows, dimensions as columns, levels as cell values — that surfaces *patterns across the portfolio* (most services L2 on observability suggests a platform investment opportunity) *without collapsing the multi-dimensional rating into a single composite score* that would hide which dimensions need attention. Its *completion* is owner-driven (the service owner fills in the scorecard with evidence) and peer-reviewed (an architect or platform team validates the ratings against the criteria). Its *trajectory* is tracked: scorecards are versioned over time so that improvement movement (or stagnation, or regression) on each dimension is visible.

The architectural shift is not "we have scorecards." It is: **the scorecard is a designed portfolio instrument whose per-dimension criteria, level-based scoring, calibration against operational outcomes, multi-axis aggregation without composite collapse, owner-driven completion with peer review, and tracked trajectory over time determine whether the instrument drives investment decisions across the engineering portfolio or produces ratings nobody trusts — and treating scorecards as one-off surveys with single composite scores produces an instrument that doesn't survive contact with the operational reality it's supposed to measure.**

---

## Six principles

### 1. Each dimension has documented criteria per level — two reviewers should produce the same rating

The scorecard's load-bearing field is the per-dimension criteria. A scorecard with dimensions like "Observability" and levels L1–L4 but no documented criteria for what L2 versus L3 means produces ratings that vary by reviewer mood: one reviewer rates a service L3 because "they have dashboards"; another rates the same service L2 because "the dashboards aren't comprehensive." Both reviewers acted in good faith; the instrument is broken. The architectural discipline is to document, per dimension, what each level requires — *concretely enough that two reviewers looking at the same service evidence produce the same level assignment*. L1 for Observability might be "Service emits structured logs to a central system; basic uptime metric exists." L2 might be "Service has SLO-aligned metrics; log queries are practical for incident debugging; dashboards exist for primary user journeys." L3 might be "Service has documented SLOs with error budgets; alerts fire on SLO burn; distributed tracing covers critical paths; dashboards are linked from runbooks." Each level adds *specific, verifiable* capabilities that build on the prior level. The criteria are themselves a designed artefact, refined over time as ambiguity surfaces during scoring.

#### Architectural implications

- Criteria are written at the granularity the scoring uses: if scoring is L1–L4, criteria exist for each of the four levels per dimension, not a single paragraph "what observability means."
- Criteria use *verifiable* language: "structured logs emitted to a central system" is verifiable; "good observability practices" is not. A reviewer should be able to inspect the service and determine whether the criterion holds.
- Levels are *cumulative* in most frameworks: L3 requires everything in L1 and L2 plus the L3-specific additions. The criteria are written so the cumulative dependency is explicit.
- Criteria are revisited when scoring disagreements surface: two reviewers producing different ratings is a signal that the criteria are ambiguous, not that one reviewer is wrong. The criteria revision goes back to the scorecard's authors for refinement.

#### Quick test

> Take your scorecard's most-commonly-scored dimension. Without context, can you write down what L2 versus L3 requires in concrete terms a third party could verify by inspecting a service? If you find yourself writing "good X" or "comprehensive X" or "mature X," the criteria aren't yet operational and reviewers will produce different ratings on the same evidence.

#### Reference

[Google SRE Workbook — Production Readiness Reviews](https://sre.google/workbook/evolving-sre-engagement-model/) treats per-dimension criteria as the load-bearing component of the PRR instrument. [CNCF Cloud Native Maturity Model](https://maturitymodel.cncf.io/) provides documented level criteria across dimensions of cloud-native adoption.

---

### 2. Scoring is level-based, not a numeric point on a continuous scale

A scorecard that rates services on a 1–10 numeric scale per dimension implies a precision the instrument doesn't have: there is no measured difference between a 6 and a 7 on observability, but the instrument forces reviewers to choose. The numeric framing also invites averaging — adding scores across dimensions to produce a composite "service health index" that hides which dimensions are weak. *Level-based scoring*, by contrast, encodes that the rating is qualitative and discrete: L1 / L2 / L3 / L4 (or Bronze / Silver / Gold / Platinum, or Foundational / Proficient / Advanced / Optimised) where each level represents *a documented state* the service has reached on that dimension, not a point on a continuous scale. Levels resist averaging because the difference between L1 and L2 isn't the same magnitude as the difference between L3 and L4; the levels capture qualitative jumps in capability, not arithmetic increments. The architectural discipline is to choose a level vocabulary, document what each level means, and refuse to translate levels back into numbers for aggregation.

#### Architectural implications

- The level vocabulary is small and fixed: 3–5 levels per dimension. More levels invite false precision; fewer levels collapse useful distinctions.
- Levels are *named* not just numbered, in many frameworks: "Foundational / Proficient / Advanced / Optimised" carries more semantic weight than "L1 / L2 / L3 / L4" and resists conversion back to numbers.
- The level definition makes clear the *qualitative nature* of the jumps: L2 isn't twice as good as L1; L2 represents a different *kind* of capability state.
- Scoring instructions explicitly forbid numeric averaging: there is no formula that converts a service's per-dimension levels into a single numeric score; the multi-dimensional view is the rating.

#### Quick test

> Look at how your scorecard's results are presented. Is each dimension reported separately at its level, or has someone aggregated the per-dimension levels into a single score "for executive consumption"? If a composite number exists, the level discipline has already been broken: the readers stopped seeing the multi-dimensional reality and started consuming a single number that hides which dimensions need investment.

#### Reference

[CNCF Cloud Native Maturity Model](https://maturitymodel.cncf.io/) uses named level vocabulary across dimensions to encode qualitative states rather than numeric points. [DORA — DevOps Research and Assessment](https://dora.dev/) uses bucketed performance categories (Low / Medium / High / Elite) for the same reason.

---

### 3. Criteria are calibrated against actual operational outcomes — not aspirational targets

A scorecard whose criteria were written by a senior architect's view of "what good looks like" — without reference to which dimensions actually correlate with operational stability — produces ratings that don't predict operational reality. A service rated L4 on every dimension that nonetheless suffers regular sev-1 incidents signals that the scorecard's criteria don't capture what matters. A service rated L1 on observability that rarely has incidents signals the same. The architectural discipline is to *calibrate criteria against operational outcomes*: collect data on incidents, recovery times, change failure rates, and customer-facing reliability per service, and check whether scorecard ratings predict the operational data. When ratings and outcomes diverge, the criteria need revision. The criteria evolve over time, driven by what the operational data reveals about which capabilities actually matter for which outcomes.

#### Architectural implications

- The scorecard team maintains a feedback loop with operational data: incidents are tagged with the affected service's scorecard ratings at the time; recovery times are tracked by ratings; change failure rates are tracked by ratings.
- When the operational data diverges from what the scorecard predicts, the criteria — not the operational reality — are what need adjustment. Adjusting the operational reality to match the scorecard inverts the discipline.
- Criteria revisions are themselves recorded: "L3 Observability criteria revised on 2025-01-15 because services rated L3 had 23% higher MTTR than services rated L4; adding 'distributed tracing' as L3 minimum based on outcome data."
- The DORA-style approach is the canonical example: the four key DORA metrics (deployment frequency, lead time, change failure rate, MTTR) emerged from research on what actually correlates with elite-performing engineering organisations, not from theory about what should matter.

#### Quick test

> Take your scorecard's last calibration cycle (if any). Was the calibration driven by operational data — checking whether ratings predict incidents, recovery, change success — or by senior-architect judgement about what should be in the criteria? If the criteria evolve only by senior judgement without operational validation, the scorecard's authority is structural-not-empirical, and ratings may not predict the outcomes the instrument is supposed to track.

#### Reference

[DORA — DevOps Research and Assessment](https://dora.dev/) is the canonical example of calibration-by-operational-outcomes: the four key metrics emerged from research on what actually correlates with high-performing engineering organisations. [Google SRE Workbook — Production Readiness Reviews](https://sre.google/workbook/evolving-sre-engagement-model/) emphasises post-PRR retrospectives that compare predicted readiness against actual production behaviour.

---

### 4. Aggregation produces a portfolio view, not reduction to a single composite number

A scorecard's value increases when it surfaces *patterns across the portfolio* of services: most services are L2 on observability (suggests a platform investment opportunity); the payments service is L4 on security but L1 on cost efficiency (suggests a focused intervention); reliability levels have improved from L2-median to L3-median over six quarters (suggests the reliability investment is working). The natural visualisation is a *matrix*: services as rows, dimensions as columns, levels as cell values, often colour-coded by level. The portfolio view *preserves* the multi-dimensional rating: a reader scanning the matrix sees both per-service and per-dimension patterns. The natural temptation — collapsing the matrix into a single composite "engineering health score" per service for executive consumption — *destroys* the instrument's value: services with the same composite number have entirely different actual ratings, and the dimensions that need investment become invisible. The architectural discipline is to refuse the composite collapse. The matrix is the rating; what gets aggregated for executive presentation is *patterns across the matrix* (median levels per dimension, distribution of services at each level, trajectory over time) — not single composite numbers per service.

#### Architectural implications

- The portfolio view is published as a matrix at minimum, with services and dimensions both visible. Dashboards may add filters (by team, by service tier, by criticality) but never collapse to a single number per service.
- Pattern aggregations are computed on the matrix, not on a derived composite: "median observability level across critical-tier services" or "percentage of services at L3+ on security."
- Trajectory is visualised by versioning the matrix over time; ridge plots, sparklines per dimension, or per-service multi-period views show movement.
- Executive presentations show portfolio patterns, not service rankings. "Security investment has moved median from L2 to L3" is the kind of claim the scorecard supports; "the top 5 services" is the kind of claim it shouldn't.

#### Quick test

> If your organisation's leadership consumes scorecard results, what do they actually see — the portfolio matrix with all dimensions visible, or a single "engineering health score" per service? If they see composite numbers, the multi-dimensional discipline has been collapsed at the presentation layer, and decisions are being made on aggregations that hide which dimensions are weak.

#### Reference

[Backstage — Software Catalog](https://backstage.io/docs/features/software-catalog/) provides infrastructure for service-level scorecard data without enforcing composite aggregation. [Spotify Engineering — Tech Health](https://engineering.atspotify.com/) describes the multi-dimensional approach where the matrix preserves per-dimension visibility.

---

### 5. Completion is owner-driven with peer review — ownership without isolation

A scorecard filled in only by a central architecture team produces ratings that don't reflect the service owners' knowledge of the system: the central team can score against documented criteria but lacks the context of what's actually deployed, what edge cases exist, what known issues haven't been resolved. A scorecard filled in only by service owners produces ratings inflated by the social pressure of self-rating: owners rate generously because the rating reflects on their team. The architectural discipline is *owner-driven completion with peer review*: the service owner fills in the scorecard with *evidence* for each rating (a pointer to dashboards for observability rating, a link to the threat model for security rating, a runbook reference for incident-response rating); a peer reviewer — typically an architect, a platform engineer, or a peer service owner — validates the ratings against the criteria and the evidence, and either confirms or challenges each rating. The two-step structure produces ratings that are both *informed by service-owner knowledge* and *validated against documented criteria by an outside perspective*.

#### Architectural implications

- The scorecard form requires per-rating evidence: each level assignment links to evidence (dashboard URL, document link, code reference) that supports the rating.
- Peer reviewers are named and accountable: the reviewer's name appears on the scorecard, and the reviewer takes responsibility for having validated each rating against the criteria.
- Rating disagreements between owner and reviewer are recorded, not suppressed: when the reviewer challenges a rating, the disagreement and its resolution become part of the scorecard's history, useful for criteria refinement.
- The peer reviewer rotates over time so that no single perspective dominates; cross-team peer reviewing builds shared calibration across the organisation.

#### Quick test

> Pick your most recent scorecard cycle. For a non-trivial dimension (say, security) on a non-trivial service, can you trace the rating to the evidence that supported it and identify the peer reviewer who validated the rating? If the rating exists without evidence pointers and without an identifiable validator, the scorecard's completion process has collapsed into either central-team-decree or owner-self-rating, and the ratings don't carry the dual validation the instrument depends on.

#### Reference

[Google SRE Workbook — Production Readiness Reviews](https://sre.google/workbook/evolving-sre-engagement-model/) describes the two-party PRR process where service teams produce evidence and SRE teams validate. [Backstage — Software Catalog](https://backstage.io/docs/features/software-catalog/) supports scorecard plugins that enforce evidence-linkage and reviewer accountability.

---

### 6. Trajectory is tracked over time — improvement movement matters more than absolute level

A scorecard captured once and never refreshed is an artefact of historical interest. A scorecard refreshed quarterly with versioned results becomes an *instrument for tracking improvement trajectory*: a service that moved from L1 to L3 on observability over four quarters has *signal* (the team's investment is producing measurable improvement on documented criteria); a service stuck at L2 on the same dimension across the same period has different signal (the investment isn't translating, or the team isn't investing, or the criteria are being interpreted inconsistently). The architectural discipline is to *version the scorecard over time and treat trajectory as primary signal alongside absolute level*. Services investing in their weak dimensions show movement; services neglecting their weak dimensions don't. Trajectory data informs investment decisions in ways absolute-level data alone can't: a service stuck at L2 may need *external help* (a platform team partnering with them), not just *more pressure* to improve.

#### Architectural implications

- Scorecards are versioned: each cycle produces a new version with the date, the ratings, the evidence, and the reviewer. Old versions remain accessible.
- Trajectory visualisations are part of the portfolio view: per-service per-dimension level over time, often as small multiples or sparklines.
- Movement is treated as signal: a service moving L2→L3 in one cycle is recognised; a service stuck at L2 across cycles is flagged for support, not penalty.
- Cycle cadence is documented: quarterly is common; some organisations use semi-annual; the cadence trades off freshness against the ceremony cost of completion.

#### Quick test

> Look at your scorecard's last four cycles for any service. Can you trace per-dimension movement across the cycles, or does each cycle live as an independent artefact with no trajectory visible? If trajectory isn't visible, the scorecard is functioning as a point-in-time rating rather than as an improvement-tracking instrument, and investment decisions can't draw on the movement signal.

#### Reference

[CNCF Cloud Native Maturity Model](https://maturitymodel.cncf.io/) treats maturity progression as the primary intended use, with the model designed for repeated assessment over time. [DORA — DevOps Research and Assessment](https://dora.dev/) emphasises trajectory across reporting periods as the primary signal of organisational performance.

---

## Common pitfalls when adopting scorecard-template thinking

### ⚠️ Numeric scoring instead of levels

A 1–10 scale per dimension produces false precision and invites averaging into composite scores. Reviewers can't reliably distinguish a 6 from a 7; aggregations hide which dimensions are weak.

#### What to do instead

Level-based scoring with a small documented vocabulary (L1–L4 or named tiers). Levels resist averaging because qualitative jumps aren't arithmetic increments. The multi-dimensional view is the rating.

---

### ⚠️ Single composite score per service for "executive consumption"

The matrix gets collapsed into one number per service so leadership can rank services. Information about which dimensions need investment is lost; services with the same composite number have entirely different actual ratings.

#### What to do instead

Refuse the composite collapse. Publish the matrix; aggregate patterns across the matrix (median per dimension, distribution at each level, trajectory) for executive presentation, never single composite numbers per service.

---

### ⚠️ Criteria written without reference to operational data

Criteria reflect senior-architect judgement of "what good looks like" but don't predict operational outcomes. A service rated L4 on every dimension still suffers regular incidents; the scorecard's authority is structural-not-empirical.

#### What to do instead

Calibrate criteria against operational data: incidents, recovery times, change failure rates, customer-facing reliability per service. When ratings don't predict outcomes, revise the criteria — not the operational reality.

---

### ⚠️ Owner-only ratings or central-team-only ratings — no dual validation

Owner-only produces inflation (social pressure to rate generously); central-only produces ratings that don't reflect service-owner knowledge of edge cases and known issues.

#### What to do instead

Owner-driven completion with peer review. Owners fill in evidence-backed ratings; peer reviewers (architects, platform engineers, peer service owners) validate against criteria. Both sides named on the scorecard.

---

### ⚠️ Point-in-time exercise — no versioning, no trajectory

A scorecard captured once never refreshed, or refreshed without versioning, loses the trajectory signal. Improvement movement on weak dimensions is invisible; services stuck at low levels look identical to services investing in improvement.

#### What to do instead

Versioned scorecards with documented cycle cadence (quarterly is common). Trajectory visualisations as part of the portfolio view. Movement treated as primary signal; stuck services flagged for support, not penalty.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Each dimension has documented criteria per level, written in verifiable language ‖ "Service emits structured logs to a central system" not "good observability practices." Two reviewers looking at the same service evidence produce the same rating. | ☐ |
| 2 | Scoring uses a small fixed level vocabulary, not a numeric scale ‖ L1–L4 or named tiers (Foundational / Proficient / Advanced / Optimised). Levels resist averaging because qualitative jumps aren't arithmetic increments. | ☐ |
| 3 | Criteria are calibrated against operational data, not senior-architect judgement alone ‖ Incidents, recovery times, change failure rates per service tracked by rating; ratings revised when they don't predict outcomes. The scorecard's authority is empirical. | ☐ |
| 4 | The portfolio view is a matrix — services × dimensions × levels — not a single composite score per service ‖ The multi-dimensional rating preserved at the presentation layer. Patterns aggregated across the matrix (median per dimension, distribution at each level), not collapsed to one number. | ☐ |
| 5 | Each rating links to evidence ‖ Dashboard URLs for observability, threat model links for security, runbook references for incident response. The rating is traceable to the artefacts that justify it. | ☐ |
| 6 | Completion is owner-driven with peer review ‖ Service owners fill in evidence-backed ratings; peer reviewers (architects, platform engineers) validate against criteria. Both sides named on the scorecard; rating disagreements recorded. | ☐ |
| 7 | Scorecards are versioned over time with documented cycle cadence ‖ Quarterly or semi-annual completion; each cycle produces a new version. Old versions remain accessible. The instrument tracks change, not just current state. | ☐ |
| 8 | Trajectory visualisations are part of the portfolio view ‖ Per-service per-dimension movement across cycles. Movement treated as signal: services stuck at low levels flagged for support; services moving up recognised. | ☐ |
| 9 | The scorecard template itself is a versioned artefact, with criteria revisions documented ‖ Criteria changes recorded with date and reason. The scorecard's evolution is itself trackable. New cycles use the current criteria; historical comparisons account for criteria revisions. | ☐ |
| 10 | Executive presentations show portfolio patterns and trajectory, not service rankings ‖ "Median security level moved from L2 to L3 over four quarters" is supported. "Top five services by composite score" is not. The instrument's multi-dimensional integrity preserved at every presentation layer. | ☐ |

---

## Related

[`templates/adr-template`](../adr-template) | [`templates/review-template`](../review-template) | [`checklists/architecture`](../../checklists/architecture) | [`governance/review-templates`](../../governance/review-templates) | [`observability/slos`](../../observability/slos)

---

## References

1. [Google SRE Workbook — Production Readiness Reviews](https://sre.google/workbook/evolving-sre-engagement-model/) — *sre.google*
2. [CNCF Cloud Native Maturity Model](https://maturitymodel.cncf.io/) — *maturitymodel.cncf.io*
3. [DORA — DevOps Research and Assessment](https://dora.dev/) — *dora.dev*
4. [Backstage — Software Catalog](https://backstage.io/docs/features/software-catalog/) — *backstage.io*
5. [OWASP Software Assurance Maturity Model (SAMM)](https://owaspsamm.org/) — *owaspsamm.org*
6. [Spotify Engineering Culture](https://engineering.atspotify.com/) — *engineering.atspotify.com*
7. [Building Evolutionary Architectures (Ford et al.)](https://www.oreilly.com/library/view/building-evolutionary-architectures/9781491986356/) — *oreilly.com*
8. [ThoughtWorks Tech Radar](https://www.thoughtworks.com/radar) — *thoughtworks.com*
9. [Diátaxis Documentation Framework](https://diataxis.fr/) — *diataxis.fr*
10. [Documenting Architecture Decisions (Nygard)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — *cognitect.com*
