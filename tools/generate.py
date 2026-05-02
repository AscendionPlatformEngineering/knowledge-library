#!/usr/bin/env python3
"""
Ascendion Engineering — Site Generator v4
All fixes: alignment, ghost boxes, light diagrams, section hero art,
white footer text, 18px base font.

Usage:
    python generate.py --src ./ascendionengineering --out ./dist --clean
Requirements:
    pip install markdown --break-system-packages

═══════════════════════════════════════════════════════════════════════════════
AUTHORING CONVENTIONS — single source of truth for every substantive page
═══════════════════════════════════════════════════════════════════════════════

These rules apply to every authored content page. The build enforces what it
can mechanically and documents the rest as guidance. New conventions are added
here when established; the comment below grows over time.

PAGE STRUCTURE (in order, every substantive page):
  1. # H1 title
  2. Description paragraph
  3. **Section:** `{slug}/` | **Subsection:** `{sub}/`
  4. **Alignment:** Standard 1 | Standard 2 | Standard 3 | Standard 4
  5. ---
  6. ## What "X" actually means        — definitional opening
  7. ## Six principles                  — exactly 6 numbered flip cards
  8. ## Architecture Diagram            — heading + intro + Mermaid
  9. ## Common pitfalls when adopting X — exactly 5 ⚠️ flip cards
 10. ## Adoption checklist              — 10 rows, ‖ separator triggers cards
 11. ## Related                         — chip row of 4–6 sister pages
 12. ## References                      — numbered list, all hyperlinked

LINK SECURITY (mechanical, build halts on violation):
  Every hyperlink in every page and content must be verified secure.
  - All URLs use https:// (http:// rejected)
  - No domains on KNOWN_INSECURE_DOMAINS blocklist
  - See verify_link_security() below for the enforcement code.
  - Add new bad-cert domains to the blocklist when reported; the next
    build catches every URL pointing at them.

EMBLEM MOTION MECHANICS (each page must use a DISTINCT mechanic):
  Every emblem must use a categorically different animation primitive,
  not just different geometry around the same recipe. Catalogue so far:
    ai-native            → particle flow (centripetal convergence)
    domain-specific      → shape oscillation (whole shapes drift in/out)
    foundational         → rigid-body rotation (pendulum)
    modernization        → cross-fade metamorphosis (two forms trade visibility)
    cloud-native         → elastic replication (pods appear/disappear in waves)
    patterns/data        → sequential frame illumination (fixed frames take turns
                           being highlighted; motion is time, not movement)
    patterns/deployment  → progressive threshold fill (a fill region grows
                           left-to-right through canary checkpoints, pausing
                           at each threshold; only the fill boundary moves)
    patterns/integration → bidirectional pulsation (two stable nodes pulse
                           in turn — scale + emphasis — while a static channel
                           brightens between pulses; nothing translates)
    patterns/security    → concentric perimeter tracing (rings draw themselves
                           into existence around a protected asset, building
                           defence in depth via stroke-dashoffset path tracing;
                           no translation, no scale, no fade)
    patterns/structural  → accretive composition (nine tiles in a 3×3 grid; the
                           core appears first, then the eight surrounding
                           modules accrete around it in spiral order; all hold,
                           all fade simultaneously; monotonic buildup followed
                           by unison reset, distinct from elastic replication's
                           oscillating waves and from sequential frame
                           illumination's pre-existing-frame highlighting)
    system-design/edge-ai → peripheral asynchronous pulse (six edge nodes
                           around a faint distant centre, each pulses (radius +
                           fill) on independent staggered phases sharing the
                           same period; parallel-independent rather than the
                           sequential alternation of bidirectional pulsation)
    system-design/event-driven → wave propagation (a single ring expands from
                           a source point — radius animates 0→50 — while three
                           subscriber dots at staggered distances flash
                           terracotta as the wavefront reaches them; distinct
                           from concentric perimeter tracing because the radius
                           itself grows rather than the path being drawn along
                           a fixed-radius circle)
    system-design/ha-dr  → primary-standby handoff (two persistent identical
                           rectangles; the active role's terracotta fill swaps
                           between them periodically with two role-swap events
                           per cycle; both shapes remain identical in geometry,
                           only colour/role swaps; distinct from cross-fade
                           metamorphosis where the two forms differ
                           geometrically)
    system-design/scalable → scaling envelope (five rectangles in a row; count
                           of active terracotta rectangles rises 1→2→3→4→5
                           and falls 5→4→3→2→1 across nested time intervals
                           centred at the cycle midpoint; distinct from
                           sequential frame illumination because multiple are
                           active simultaneously, and from accretive
                           composition because the envelope rises AND falls
                           rather than monotonic-buildup-then-bulk-fade)
    technology/ui-ux-cx  → layered depth reveal (three offset rectangles
                           representing UI/UX/CX layers reveal in z-axis depth
                           order — back-to-front — via opacity; all hold; all
                           fade simultaneously; distinct from cross-fade
                           metamorphosis where two GEOMETRICALLY DIFFERENT
                           forms swap, and from accretive composition where
                           tiles appear in spiral order)
    technology/api-backend → bidirectional pipeline traffic (two horizontal
                           lanes; in the upper lane request dots flow
                           left-to-right, in the lower lane response dots
                           flow right-to-left; continuous bidirectional
                           traffic; distinct from radial particle convergence
                           by being parallel-linear rather than radial)
    technology/databases → sedimentation stacking (small items appear at the
                           top, fall under gravity to a floor line, accumulate
                           into a stacked row; once full, all dissolve and the
                           cycle restarts; vertical translation with
                           accumulation, distinct from scaling envelope's
                           in-place colour swap and from accretive
                           composition's spiral appearance)
    technology/cloud     → sweeping beam scan (a vertical beam line translates
                           left-to-right across the canvas; six fixed dots at
                           staggered positions briefly flash terracotta as
                           the beam passes their column; distinct from radial
                           particle flow by being a single linear sweep with
                           reactive fixed receivers, and from wave propagation
                           by being a translating line rather than expanding
                           radius)
    technology/devops    → conveyor loop (five dots traverse a closed
                           rectangular path continuously; each dot is at a
                           different position around the loop; the pipeline
                           is never empty; distinct from radial particle
                           convergence and from bidirectional pipeline traffic
                           by being a single closed-loop perimeter traversal
                           rather than radial-inward or parallel-linear)
    technology/practice-circles → cardinal cluster cycle (four dot clusters
                           — three dots each — arranged in cardinal positions
                           N/E/S/W around a faint centre; each cluster lights
                           up in turn (cluster-level sequential illumination),
                           then the centre brightens to indicate
                           cross-pollination; distinct from sequential frame
                           illumination by having clusters as the unit and
                           an explicit cross-pollination phase, and from
                           peripheral asynchronous pulse by being synchronised
                           within clusters and sequential between them)
    technology/engagement-models → tier ascent (a token — small square —
                           progresses up three platform steps in sequence
                           representing Staffing → Managed Capacity →
                           Managed Services; the token holds at the top tier
                           briefly, then fades out and the cycle restarts
                           with a fresh token at the bottom; distinct from
                           conveyor loop by being unidirectional staircase
                           progression with a fade-and-restart, not closed
                           loop, and from scaling envelope by being a single
                           ascending token rather than an array)
    security/application-security → filtration cascade (five dots fall from
                           top through three horizontal filter layers at
                           y=30, y=50, y=70; some dots are blocked at each
                           layer and fade out, two reach the bottom and
                           briefly turn terracotta as they hit the protected
                           application baseline; distinct from progressive
                           threshold fill by having discrete items that
                           travel rather than a region that grows, and from
                           sedimentation stacking by having items rejected
                           at multiple intermediate layers rather than
                           accumulating on a single floor)
    security/authentication-authorization → challenge-response handshake
                           (two persistent shapes — a Subject rectangle on
                           the left and a Resource rectangle on the right;
                           tokens shuttle back and forth alternately, one
                           direction at a time, with explicit rest between
                           exchanges; the receiving node briefly turns
                           terracotta as the token arrives; distinct from
                           bidirectional pulsation by being sequential
                           discrete token movement rather than simultaneous
                           node activation, and from bidirectional pipeline
                           traffic by being one token at a time alternating
                           direction rather than continuous parallel flows
                           in opposite lanes)
    security/cloud-security → shield envelope pulsation (three concentric
                           rings around a persistent terracotta core asset
                           expand and contract in unison — same keyTimes,
                           synchronised breathing rhythm — over a 6s cycle;
                           rings at radii 12↔18, 22↔28, 32↔38; distinct
                           from concentric perimeter tracing which uses
                           stroke-dashoffset to draw rings sequentially,
                           and from wave propagation which has a single
                           ring expanding centrifugally from a source and
                           disappearing — here multiple rings persist and
                           breathe together)
    security/encryption  → key-merge / unmerge (two persistent shapes — a
                           data rectangle on the left and a key circle on
                           the right — translate toward the centre, fade
                           out as a single ciphertext rectangle fades in,
                           hold as ciphertext for the encrypted phase, then
                           reverse: ciphertext fades out, original two shapes
                           fade back in and translate to original positions;
                           distinct from particle flow which has many
                           particles converging from periphery to a single
                           central point — here it is two named persistent
                           shapes that meet and re-separate, and from
                           cross-fade metamorphosis which trades visibility
                           in the same spatial position with no movement —
                           here the two original shapes physically translate)
    security/vulnerability-management → triage funnel (eight dots enter
                           wide at the top of a visible inverted-trapezoid
                           funnel — diagonal walls drawn explicitly; six
                           descend through the funnel and four make it to
                           the narrow bottom output line, where they
                           briefly turn terracotta as remediated; the other
                           dots are blocked at the diagonal walls and fade;
                           distinct from filtration cascade which uses
                           horizontal filter layers as the visual constraint
                           — here the constraint is geometric convergence
                           via the funnel's diagonal walls; distinct from
                           particle flow which has radial centripetal
                           convergence to a central point)
    ai-native/architecture → token streaming emergence (six small dots in
                           a horizontal row appear one at a time from left
                           to right over a 6s cycle, each persisting after
                           appearance, building cumulatively until the full
                           row is visible — the autoregressive token-by-
                           token generation; after a brief hold all dots
                           clear simultaneously and the cycle restarts;
                           distinct from sequential frame illumination
                           which has frames take TURNS being lit — only
                           one active at a time, not cumulative; distinct
                           from sedimentation stacking which has items fall
                           VERTICALLY and accumulate on a floor — here the
                           emergence is HORIZONTAL with simultaneous clear)
    ai-native/ethics     → disparate-rate progression (two horizontal
                           progress bars side by side fill at independent
                           speeds — top bar fills 0→100% in 4s, bottom
                           bar fills in 6s, each cycles at 8s — visualising
                           the asymmetry between groups receiving the same
                           task; the visible rate difference IS the message,
                           fairness as the relationship between filling
                           rates; distinct from progressive threshold fill
                           which has a SINGLE region growing through canary
                           checkpoints; distinct from scaling envelope
                           which has a row of rectangles where the COUNT
                           of active rectangles rises and falls — here
                           two CONTINUOUS fill bars with disparate rates)
    ai-native/monitoring → rolling time-series window (five dots emerge
                           on the right edge of the canvas with staggered
                           phases over a 4s base cycle, shift left in
                           unison through five slot positions, with the
                           oldest dot exiting on the left edge and fading;
                           continuous unidirectional FIFO flow, the time
                           series in motion; distinct from conveyor loop
                           which is a CLOSED rectangular circuit where
                           items return to the start — here items have
                           explicit entry on the right and exit on the
                           left; distinct from particle flow which is
                           RADIAL centripetal convergence to a central
                           point — here LINEAR horizontal flow with
                           FIFO replacement; distinct from bidirectional
                           pipeline traffic which has TWO opposite-
                           direction parallel flows)
    ai-native/rag        → nearest-neighbor retrieval (a central terracotta
                           query node sits at the canvas centre with eight
                           stationary corpus nodes arranged in a ring
                           around it; each cycle three specific corpus
                           nodes light terracotta and connect to the centre
                           via thin terracotta lines, then fade back to
                           neutral as a different subset of three corpus
                           nodes lights for the next query; three subsets
                           rotate over a 6s cycle; distinct from peripheral
                           asynchronous pulse which has independent firings
                           of nodes WITHOUT any connection lines and no
                           central anchor; distinct from cardinal cluster
                           cycle which has CLUSTERS of nodes cycling
                           through being lit in rotation — here it is
                           SELECTIVE SUBSET retrieval, different specific
                           individual nodes light each cycle, not all-of-
                           cluster-A then all-of-cluster-B)
    ai-native/security   → latent threat unmasking (dots travel right-to-
                           left across the canvas through a vertical
                           detection band drawn at the centre; benign dots
                           pass straight through as warm neutral and exit
                           on the left; some dots reveal themselves as
                           adversarial while inside the band — they turn
                           terracotta and REVERSE direction, exiting back
                           to the right; the reversal-on-detection is the
                           visual signature, animating the architectural
                           reality that detected adversarial inputs are
                           sent back rather than absorbed; distinct from
                           filtration cascade which has VERTICAL descent
                           through HORIZONTAL filter layers and blocked
                           items fade IN PLACE rather than reversing;
                           distinct from triage funnel which has GEOMETRIC
                           convergence with directional reduction and
                           rejected items fade out — here items actively
                           travel BACKWARD past the boundary they entered)
    governance/checklists → vertical cascade checklist (a vertical column
                           of five rectangular checkbox outlines is always
                           visible in warm neutral; over a 6s cycle, a
                           terracotta checkmark POLYLINE PATH appears
                           inside each box one at a time from top to
                           bottom, each persisting after appearance, all
                           checkboxes filled by t=3.5s, hold until t=5s,
                           then all checkmarks clear simultaneously;
                           distinct from token streaming emergence which
                           is a HORIZONTAL row of CIRCULAR DOTS appearing
                           cumulatively L→R — here it is a VERTICAL
                           column of RECTANGULAR CHECKBOXES with
                           CHECKMARK PATHS appearing inside them; distinct
                           from sedimentation stacking which has items
                           FALL VERTICALLY and accumulate on a floor —
                           here the boxes are STATIONARY and only their
                           internal checkmark state changes)
    governance/review-templates → template reuse pattern (a fixed 2x3 grid
                           of nine cell outlines is always visible in
                           warm neutral, representing the template's
                           permanent structure; each cycle a different
                           SUBSET of three cells fills with terracotta
                           — Subset A: top-left, middle-mid, bottom-right;
                           Subset B: top-mid, middle-right, bottom-left;
                           Subset C: top-right, middle-left, bottom-mid;
                           subsets cycle through over 6s with brief
                           transitions between, representing the same
                           template being filled in differently for
                           different reviews; distinct from nearest-
                           neighbor retrieval which has a CIRCULAR ring
                           of 8 nodes around a CENTRAL anchor with
                           CONNECTION LINES from selected subset to
                           anchor — here it is a RECTANGULAR 2D GRID
                           with NO central anchor and NO connection
                           lines; distinct from vertical cascade
                           checklist which is a 1D column with cells
                           filling SEQUENTIALLY top-to-bottom — here
                           it is a 2D grid with cells filling in
                           SUBSETS per cycle, full clear between subsets)
    governance/roles     → tiered escalation cascade (three horizontal
                           tier-baselines are drawn in warm neutral,
                           each baseline carrying three dots — bottom
                           tier representing team authority, middle
                           representing ARB, top representing executive;
                           a 9-second cycle contains three sub-cycles
                           of 3s each: cycle 1 lights only the BOTTOM
                           tier (routine decision); cycle 2 lights
                           BOTTOM then MIDDLE in sequence (cross-cutting
                           decision escalating one tier); cycle 3
                           lights BOTTOM, MIDDLE, then TOP in sequence
                           (high-stakes decision cascading all the way
                           up); each tier's dots all light together,
                           variable cascade depth visualises authority
                           promotion across decision classes; distinct
                           from rolling time-series window which has
                           a SINGLE horizontal flow with FIFO
                           replacement, dots traveling RIGHT TO LEFT —
                           here it is THREE TIERED HORIZONTAL ROWS
                           where activation cascades UPWARD through
                           tiers; distinct from sequential frame
                           illumination which has a SINGLE row with
                           frames taking turns being lit — here the
                           cascade is VERTICAL across tiers, with
                           variable depth per cycle; distinct from
                           progressive threshold fill which has ONE
                           growing region — here three discrete tier
                           rows light independently per cycle)
    governance/scorecards → independent metric oscillation (five vertical
                           rectangular bars are arranged horizontally
                           across the canvas, each bar's HEIGHT
                           animates continuously between a minimum
                           and maximum value, each bar at a DIFFERENT
                           PERIOD — 3.0s, 4.2s, 5.0s, 6.0s, 7.5s — so
                           each oscillates at its own frequency, never
                           syncing, never resetting, just continuously
                           rising and falling like sine waves out of
                           phase; the bars share a baseline at y=78
                           and grow upward toward the canvas top;
                           multi-dimensional governance health metrics,
                           each measured continuously at its own rate;
                           distinct from disparate-rate progression
                           which has TWO HORIZONTAL bars filling
                           LEFT-TO-RIGHT MONOTONICALLY then RESETTING
                           — here FIVE VERTICAL bars CONTINUOUSLY
                           OSCILLATE, never reset, never fill in one
                           direction; distinct from scaling envelope
                           which has a row of rectangles where the
                           COUNT of active rectangles changes — here
                           FIXED count with CONTINUOUS height
                           variation; distinct from progressive
                           threshold fill which is a single growing
                           region — here five independent oscillators)
    observability/incident-response → incident spike pattern (five
                           horizontal service lanes drawn in warm neutral
                           are always visible, representing services in
                           steady-state; over an 8-second cycle the canvas
                           is mostly QUIET, then the MIDDLE lane spikes
                           to BRIGHT terracotta from t=1.5s, the
                           ADJACENT lanes (above and below) light to
                           DIMMER terracotta from t=2.0s representing
                           impact spread, the middle lane oscillates
                           briefly between bright and dim terracotta
                           from t=3.0s representing active response work,
                           all lanes return to warm neutral at t=5.0s,
                           and the cycle holds quiet through t=8.0s
                           before restarting; punctuated multi-lane
                           spike pattern with a mostly-quiet duty cycle;
                           distinct from #6 sequential frame illumination
                           which has a SINGLE row with frames taking
                           TURNS one at a time — here MULTIPLE lanes
                           with PUNCTUATED single-lane spike PLUS
                           ADJACENT IMPACT SPREAD, mostly quiet duty
                           cycle; distinct from #34 tiered escalation
                           cascade which has VARIABLE upward cascade
                           depth across tiers — here HORIZONTAL multi-
                           lane PUNCTUATED disturbance with adjacency
                           spread, NOT cascade-up tiers)
    observability/logs   → log tail scroll (six horizontal log-line
                           rectangles of slightly varied widths at six
                           vertical slot positions y=22/32/42/52/62/72;
                           over a 6-second cycle, all lines shift UPWARD
                           by one slot per second, with the line at
                           bottom slot (y=72) being freshly bright
                           terracotta and the line at top slot (y=22)
                           being faded warm neutral about to exit;
                           continuous bottom-to-top scroll like tail -f
                           on a log file, with new lines appearing at
                           the bottom and oldest exiting through the
                           top; distinct from #29 rolling time-series
                           window which has a SINGLE HORIZONTAL flow
                           with FIFO replacement, dots TRAVELING RIGHT
                           TO LEFT — here VERTICAL bottom-to-top scroll
                           of discrete log-line shapes at SIX simultaneous
                           slot positions; distinct from #23 sedimentation
                           stacking which has items FALL VERTICALLY from
                           top and ACCUMULATE PERMANENTLY at floor —
                           here CONTINUOUS scroll where items appear at
                           BOTTOM, exit at TOP, and never accumulate)
    observability/metrics → sweeping gauge needle (a 180-degree dial arc
                           drawn in warm neutral spans the upper half
                           of the canvas with centre pivot at (60, 65)
                           and radius 35, with five tick marks at 0°,
                           45°, 90°, 135°, 180°; a terracotta needle
                           rotates around the pivot using
                           animateTransform type=rotate over a 4-second
                           cycle, oscillating across rotation values
                           "-70; -30; 20; 60; 20; -30; -70" — sweeping
                           from low position (left) through medium (top)
                           to high (right) and back, like a metric
                           gauge showing values changing over time;
                           FIRST ROTATIONAL mechanic in the catalogue —
                           uses animateTransform type=rotate, distinct
                           from all 37 prior mechanics that use
                           translation, scale, or opacity changes;
                           distinct from #21 reciprocating arc which
                           uses ARCS as visual elements with
                           ZONE-CYCLING perimeter highlighting (the
                           arcs themselves don't rotate; the highlight
                           cycles through perimeter zones) — here a
                           SINGLE NEEDLE element ROTATES inside a
                           STATIC arc backdrop)
    observability/sli-slo → SLO compliance scatter (a horizontal
                           threshold line in warm neutral spans the
                           middle of the canvas at y=45 with dashed
                           stroke; eight discrete dots are placed at
                           fixed (x, y) positions across the canvas,
                           four BELOW the threshold (compliant —
                           coloured warm neutral) and four ABOVE the
                           threshold (SLO violations — coloured
                           terracotta); each dot has its own 8-second
                           lifetime cycle with staggered phase offsets,
                           appearing for ~4 seconds then fading,
                           producing continuous turnover with several
                           dots visible at any moment; the spatial
                           pattern reveals compliance at a glance —
                           which side of the threshold each dot sits
                           on; distinct from #29 rolling time-series
                           window which has CONTINUOUS HORIZONTAL flow
                           with FIFO replacement, dots TRAVELING RIGHT
                           TO LEFT — here STATIC threshold line as
                           architectural element + STATIONARY discrete
                           plots at fixed positions + COLOUR CODED by
                           which side of threshold; distinct from #1
                           particle flow which has RADIAL CENTRIPETAL
                           convergence to a centre — here scattered
                           DISCRETE plots in 2D space without
                           convergence motion, position relative to
                           threshold being the architectural reading)
    observability/traces → waterfall trace (five horizontal terracotta
                           bars at five different vertical positions
                           y=20/32/44/56/68, each bar at a different
                           x-offset and length representing a parent-
                           child span hierarchy: root span at top
                           spans full width x=15-95 (length 80), child
                           span offset right and shorter x=22-80
                           (length 58), grandchild deeper x=28-65
                           (length 37), sibling parallel branch x=70-88
                           (length 18), leaf span deepest x=32-52
                           (length 20); over a 5-second cycle, bars
                           appear in waterfall cascade order — root at
                           t=0.2s, child at t=0.5s, grandchild at
                           t=0.8s, sibling at t=0.9s, leaf at t=1.1s —
                           all hold visible for ~3 seconds, then fade
                           together at t=4.5s, brief pause, restart;
                           the visual is a true hierarchical span
                           tree captured as a waterfall view; distinct
                           from #34 tiered escalation cascade which
                           has THREE TIERS each with THREE ALIGNED
                           DOTS where dots within a tier light TOGETHER
                           with variable cascade depth — here FIVE
                           ROWS each a DIFFERENT-LENGTH BAR at
                           DIFFERENT X-OFFSET, true hierarchical span
                           visualisation; distinct from #28 disparate-
                           rate progression which has TWO HORIZONTAL
                           bars FILLING LEFT-TO-RIGHT MONOTONICALLY at
                           different rates and resetting — here
                           multiple bars APPEARING WHOLE in cascade
                           order, no fill animation, hierarchical
                           position not sequential rate)
    runbooks/incident    → sequential pointer descent (a vertical list
                           of five stationary text-line shapes with
                           bullet circles is always visible in warm
                           neutral on the canvas, representing runbook
                           steps; a terracotta pointer triangle on
                           the left descends through the list at
                           intervals using animateTransform type=
                           translate, pausing at each step before
                           advancing to the next; as the pointer
                           arrives at each step, that step's text-line
                           briefly brightens to terracotta (the
                           responder is on this step now), and when
                           the pointer moves on, the line returns to
                           warm neutral; over a 6-second cycle the
                           pointer descends through all five steps,
                           then disappears for a brief pause before
                           reappearing at the top for the next cycle;
                           captures a responder reading and executing
                           a runbook step by step; distinct from #32
                           vertical cascade checklist which has CHECKMARK
                           PATHS appearing inside checkbox rectangles
                           sequentially top-to-bottom and ALL PERSISTING
                           until cleared — here SINGLE MOVING POINTER
                           advances and ONLY the CURRENT STEP is
                           highlighted briefly, all others stay neutral;
                           distinct from #6 sequential frame
                           illumination which has a SINGLE HORIZONTAL
                           ROW of frames taking turns being lit — here
                           VERTICAL list with a SEPARATE MARKER ELEMENT
                           (the pointer triangle) as the moving piece
                           rather than the items themselves taking
                           turns; distinct from #34 tiered escalation
                           cascade by being SINGLE-COLUMN list with
                           marker descending through a fixed sequence)
    runbooks/migration   → anti-correlated fill (two stacked horizontal
                           bars span the canvas: top bar represents
                           the OLD system at y=28-38, bottom bar
                           represents the NEW system at y=52-62, both
                           with warm-neutral baselines always visible;
                           top bar's terracotta foreground starts at
                           full width 90 (representing 100% old-system
                           traffic) and animates down to width 0 over
                           the cycle, the rectangle shrinking from
                           the right edge as old-system traffic
                           retreats; bottom bar's terracotta foreground
                           starts at width 0 and animates up to width
                           90 (representing the new system gaining
                           traffic), the rectangle growing rightward;
                           the two bars are ANTI-CORRELATED — at any
                           moment, the visible terracotta totals to a
                           constant (representing total traffic remaining
                           constant as it shifts from old to new); over
                           a 6-second cycle the transition completes,
                           holds briefly, then snaps back to start;
                           captures migration as gradual traffic shift;
                           distinct from #28 disparate-rate progression
                           which has TWO horizontal bars filling
                           LEFT-TO-RIGHT MONOTONICALLY at DIFFERENT
                           RATES and BOTH RESET TOGETHER — here both
                           bars fill horizontally too, but ANTI-
                           CORRELATED: as one empties from RIGHT-TO-
                           LEFT, the other fills from LEFT-TO-RIGHT,
                           and the inverse relationship is the
                           architectural signature; distinct from #14
                           scaling envelope (count of active rectangles
                           changes — DISCRETE on/off states) by being
                           CONTINUOUS fill on fixed-position bars)
    runbooks/rollback    → forward-reverse fill (a single horizontal
                           bar at y=42-52 with warm-neutral baseline
                           always visible spans the canvas x=15-105; a
                           terracotta foreground rectangle within the
                           baseline animates its width through a
                           BIDIRECTIONAL pattern over a 6-second cycle:
                           starts empty (width=0), GROWS LEFT-TO-RIGHT
                           to width=67.5 (75% — the rollback decision
                           point), HOLDS BRIEFLY at the decision point
                           with a small terracotta indicator dot
                           appearing above the threshold tick, then
                           DRAINS RIGHT-TO-LEFT back to width=0
                           (rollback restoring prior state), then holds
                           empty before next cycle; subtle directional
                           arrow indicators (warm neutral) appear above
                           the bar during forward fill and below during
                           drain phase; the architectural signature is
                           the BIDIRECTIONAL motion on a SINGLE bar —
                           the same fill that grows then UNDOES itself;
                           FIRST BIDIRECTIONAL-FILL mechanic in the
                           catalogue; distinct from #7 progressive
                           threshold fill which is a SINGLE region
                           GROWING through canary checkpoints and then
                           RESETTING (monotonic forward then snap-back
                           to start) — here the fill GROWS forward,
                           HOLDS at decision point, then UN-GROWS
                           backward (drain) before the next cycle;
                           distinct from #28 disparate-rate progression
                           (TWO bars filling at different rates then
                           both reset) by being SINGLE bar with
                           BIDIRECTIONAL motion; distinct from #42
                           anti-correlated fill (TWO bars where one
                           fills as the other empties) by being a
                           SINGLE bar that fills then empties on its
                           own — the same bar undoes its own fill)
    checklists/architecture → radial check bloom (a central pivot at
                           (60, 45) with a warm-neutral outer ring and
                           terracotta inner dot represents the
                           architecture under review; six radial spokes
                           extend outward at angles 0°, 60°, 120°, 180°,
                           240°, 300° (clockwise from right) to terminal
                           markers (small filled circles) at distance 26;
                           initially all spokes and terminal markers are
                           warm neutral; over a 7-second cycle, each
                           terminal marker activates to terracotta in
                           CLOCKWISE SEQUENCE around the radial structure
                           (right → lower-right → lower-left → left →
                           upper-left → upper-right) with each marker's
                           spoke briefly highlighting terracotta as the
                           marker activates, and once activated the
                           terminal stays terracotta until the global
                           reset; after all six markers are illuminated
                           the structure holds briefly (the bloom-of-
                           verified-dimensions), then all reset to warm
                           neutral and the cycle repeats; FIRST
                           SPOKE-AND-TERMINAL RADIAL mechanic in the
                           catalogue; distinct from #1 particle flow
                           (RADIAL CENTRIPETAL convergence — particles
                           travel inward from edge to centre) by being
                           CENTRIFUGAL STATIC structure with terminal
                           markers ACTIVATING in CLOCKWISE TEMPORAL
                           SEQUENCE; distinct from #21 reciprocating arc
                           (uses ARCS as visual elements with zone-
                           cycling perimeter highlighting) by having
                           DISCRETE NUMBER OF SPOKES with TERMINAL
                           MARKERS that activate in CLOCKWISE SEQUENCE,
                           not zone-cycling; distinct from #38 sweeping
                           gauge needle (SINGLE rotating needle on a
                           STATIC arc) by being STATIC SPOKES with
                           SEQUENTIAL TERMINAL ACTIVATION rather than
                           one moving element)
    checklists/deployment → sequential vertical fill (five vertical
                           bars in a horizontal row at x=14/34/54/74/94,
                           each width 12 height 50 from y=20 to y=70,
                           with warm-neutral baseline always visible
                           and small warm-neutral dot below each bar
                           at y=78; over a 7-second cycle, each bar's
                           terracotta foreground rectangle fills from
                           BOTTOM-TO-TOP IN STRICT SEQUENCE — bar 1
                           fills from y=70/h=0 to y=20/h=50 over phase
                           0.043-0.200, then bar 2 fills over phase
                           0.200-0.357, then bar 3 over 0.357-0.514,
                           then bar 4 over 0.514-0.671, then bar 5 over
                           0.671-0.828; once all five are full the
                           structure holds (deploy complete) for phase
                           0.828-0.929, then all five empty
                           SIMULTANEOUSLY in a snap reset over
                           0.929-1.000 and the cycle restarts; captures
                           stage-by-stage gate progression through
                           deployment readiness; distinct from #35
                           independent metric oscillation which has
                           FIVE VERTICAL bars CONTINUOUSLY OSCILLATING
                           heights INDEPENDENTLY (each varies
                           asynchronously, never fully filling, never
                           fully emptying) — here FIVE VERTICAL bars
                           FILL FULLY from BOTTOM-TO-TOP IN STRICT
                           SEQUENCE then ALL RESET TO EMPTY
                           SIMULTANEOUSLY, the architectural signature
                           being SEQUENTIAL FILL with simultaneous
                           reset; distinct from #28 disparate-rate
                           progression (TWO HORIZONTAL bars filling at
                           different rates) by being FIVE VERTICAL bars
                           in STRICT SEQUENCE; distinct from #14
                           scaling envelope (HORIZONTAL row of
                           rectangles, count of active rectangles
                           varying, DISCRETE on/off) by being CONTINUOUS
                           FILL of fixed VERTICAL bars in SEQUENTIAL
                           order)
    checklists/security  → concentric ring activation (four concentric
                           circles centred at (60, 45) with radii 30,
                           23, 16, 9 — outermost to innermost — all
                           rendered as STROKE-ONLY (no fill) with
                           stroke-width 2; initially all four rings
                           are warm-neutral stroke; over a 7-second
                           cycle, each ring's stroke transitions to
                           terracotta in OUTERMOST-TO-INNERMOST
                           SEQUENCE — ring 1 (radius 30, perimeter)
                           activates over phase 0.07-0.243, ring 2
                           (radius 23) over 0.243-0.414, ring 3
                           (radius 16) over 0.414-0.586, ring 4
                           (innermost, radius 9, the core) over
                           0.586-0.757; once activated, each ring
                           stays terracotta until the global reset;
                           after all four rings are illuminated, a
                           small centre dot (radius 2.5) at (60, 45)
                           transitions from warm neutral to terracotta
                           during the hold phase 0.757-0.900
                           representing the protected asset at the
                           core of the defenses; all five elements
                           reset to warm neutral over phase 0.900-1.000;
                           captures defense-in-depth verified
                           perimeter inward; FIRST NESTED-CIRCLE
                           mechanic in the catalogue; distinct from
                           #1 particle flow (radial CENTRIPETAL
                           convergence — particles TRAVEL INWARD from
                           edge to centre) by being NESTED CIRCLES at
                           INCREASING RADII that ACTIVATE STATICALLY
                           in sequence, no particles travelling;
                           distinct from #21 reciprocating arc (uses
                           ARCS as visual elements with zone-cycling
                           perimeter highlighting on a SINGLE arc
                           geometry) by having FOUR DISTINCT NESTED
                           RINGS at DIFFERENT RADII activating in
                           SEQUENTIAL ORDER perimeter-to-core; distinct
                           from #44 radial check bloom (CENTRE PIVOT +
                           SPOKES + TERMINAL MARKERS, sequence around
                           the spokes) by having NO SPOKES, just
                           NESTED CIRCLES at INCREASING RADII; the
                           architectural signature is perimeter-to-core
                           defense layer activation)
    tools/ai-agents      → cyclic path marker (a single closed circular
                           path of radius 26 centred at (60, 45),
                           rendered as stroke-only with a dashed warm-
                           neutral stroke, with FOUR FIXED PHASE
                           MARKERS (small filled circles, radius 3) at
                           the quarter positions around the perimeter:
                           top (60, 19), right (86, 45), bottom
                           (60, 71), left (34, 45); a small terracotta
                           dot (radius 2.8) starts at the top of the
                           circle and travels around the perimeter
                           continuously via animateTransform type=rotate
                           with values "0 60 45; 360 60 45" over 6s,
                           tracing the full circumference; each fixed
                           phase marker briefly transitions from warm
                           neutral to terracotta when the traveling dot
                           is near it (its angular position aligned to
                           that phase) and back to warm neutral as the
                           dot moves on, so the markers light up in
                           clockwise sequence (top → right → bottom →
                           left → top); FIRST CLOSED-LOOP TRAVELING
                           MARKER mechanic in the catalogue; distinct
                           from #1 particle flow (RADIAL CENTRIPETAL
                           convergence — particles travel inward from
                           edge to centre on radial paths) by being a
                           SINGLE DOT traveling AROUND a closed
                           PERIMETER, never converging; distinct from
                           #21 reciprocating arc (uses ARCS as visual
                           elements with zone-cycling perimeter
                           highlighting) by having a SINGLE TRAVELING
                           DOT around a CIRCLE with FIXED PHASE
                           MARKERS that brighten as the dot passes —
                           not zone-cycling on the perimeter; distinct
                           from #38 sweeping gauge needle (SINGLE
                           rotating NEEDLE on a 180° arc) by being a
                           TRAVELING DOT on a 360° closed circle with
                           fixed markers along the path; distinct from
                           #44 radial check bloom (centre pivot +
                           SPOKES + terminal markers, terminals
                           activate clockwise) by having NO SPOKES and
                           NO CENTRE PIVOT, just a closed circular
                           path with traveling dot; distinct from #46
                           concentric ring activation (FOUR NESTED
                           circles at different radii activating
                           outermost-to-innermost) by being a SINGLE
                           CIRCLE with a traveling dot)
    tools/cli            → character sequence typing (six small
                           horizontal terracotta rectangles in a row
                           at fixed y=43, height=4, width=12, with
                           gaps of 2 between them and rounded corners
                           rx=0.8; positioned at x=19, 33, 47, 61, 75,
                           89; a small terracotta wedge prompt
                           indicator at x=9-13 always visible; a thin
                           warm-neutral baseline line at y=51 from
                           x=9 to x=103 always visible; over a
                           5-second cycle, each rectangle's opacity
                           is animated to fade in sequentially —
                           rectangle 1 at phase 0.10, rectangle 2 at
                           0.16, rectangle 3 at 0.22, rectangle 4 at
                           0.28, rectangle 5 at 0.34, rectangle 6 at
                           0.40; once visible, each stays visible
                           through phase 0.80 (command typed, ready
                           to execute); all six fade out
                           SIMULTANEOUSLY at phase 0.90 (terminal
                           cleared / command executed); brief pause
                           before restart; visual metaphor is typing
                           a command into a terminal character by
                           character; distinct from #6 sequential
                           frame illumination (SINGLE row of frames
                           where ONLY ONE is lit at any moment —
                           frames TAKE TURNS, do NOT ACCUMULATE) by
                           having items APPEAR and STAY VISIBLE
                           (accumulating until all six visible) then
                           ALL CLEAR SIMULTANEOUSLY; distinct from
                           #34 tiered escalation cascade (THREE TIERS
                           of dots, all dots within a tier light
                           TOGETHER with variable cascade depth) by
                           being SINGLE ROW of items appearing
                           SEQUENTIALLY and ACCUMULATING; distinct
                           from #41 sequential pointer descent
                           (VERTICAL list of stationary text-line
                           shapes with pointer triangle DESCENDING)
                           by being HORIZONTAL row with NO POINTER
                           ELEMENT, items fading in directly via
                           opacity animation; distinct from #45
                           sequential vertical fill (FIVE VERTICAL
                           bars filling bottom-to-top via y/height
                           animation) by being HORIZONTAL ROW of
                           small items fading in via OPACITY (no
                           fill animation, just opacity transitions))
    tools/scripts        → perimeter fill ring (a single circle of
                           radius 24 centred at (60, 45) rendered as
                           stroke-only; warm-neutral baseline circle
                           always visible at stroke-width 3 opacity
                           0.5; terracotta foreground circle with
                           same geometry and stroke-width 3 has its
                           stroke-dasharray animated from "0 151"
                           (empty) to "151 0" (full) over a 6-second
                           cycle, with -90° rotation transform
                           applied to the foreground circle around
                           (60, 45) so the fill grows clockwise from
                           the 12 o'clock position rather than 3
                           o'clock; circumference of 151 chosen as
                           2π * 24 ≈ 150.8 rounded; the cycle phases
                           are 0.000-0.067 empty (initial), 0.067-
                           0.750 fill grows clockwise (0% to 100%),
                           0.750-0.833 full (briefly hold completed
                           state), 0.833-1.000 snap back to empty
                           and brief pause; a small terracotta centre
                           dot at (60, 45) radius 2.8 pulses subtly
                           via radius animation (2.8 → 3.5 → 2.8)
                           during the fill phase representing the
                           task being processed; small warm-neutral
                           tick marks at quarter positions (12, 3,
                           6, 9 o'clock) frame the perimeter
                           decoratively; FIRST STROKE-DASHARRAY
                           PERIMETER-FILL mechanic in the catalogue;
                           visual metaphor is a loading-spinner-style
                           progress ring where the perimeter fills
                           rather than rotates; distinct from #21
                           reciprocating arc (uses ARCS as visual
                           elements with zone-cycling perimeter
                           highlighting — different zones light up
                           around the perimeter in a cycling pattern)
                           by being CONTINUOUS PERIMETER FILL that
                           GROWS from 0% to 100% then RESETS, not
                           zone-cycling; distinct from #38 sweeping
                           gauge needle (180° arc with rotating
                           needle) by being a 360° CIRCLE with
                           PERIMETER FILL animation, no rotating
                           element; distinct from #46 concentric ring
                           activation (FOUR NESTED RINGS at different
                           radii activating in sequence) by being a
                           SINGLE RING with PERIMETER FILL growing
                           clockwise; distinct from #44 radial check
                           bloom (centre pivot + spokes + terminal
                           markers) by being a perimeter fill on a
                           CIRCLE with NO SPOKES OR TERMINALS, just
                           continuous fill of the perimeter)
    tools/validators     → branching decision flow (a horizontal warm-
                           neutral entry line from (15, 45) to
                           (58, 45) representing input arrival; a
                           small terracotta diamond marker at
                           (60, 45) of width and height 8 (points at
                           60,41 / 64,45 / 60,49 / 56,45) representing
                           the validation decision point, always
                           visible; an UP-branch line from (62, 43)
                           to (100, 20) and a DOWN-branch line from
                           (62, 47) to (100, 70), both warm neutral;
                           terminal markers (small warm-neutral
                           circles radius 2.5) at (100, 20) and
                           (100, 70); a small terracotta dot of
                           radius 2.5 travels along the path through
                           a 14-second cycle composed of TWO
                           sub-cycles of 7 seconds each — sub-cycle 1
                           (pass): dot animates from (15, 45) along
                           main line to (58, 45) at decision, then
                           up-right to (100, 20), brief pause at
                           endpoint, fade and snap reset; sub-cycle 2
                           (fail): dot animates from (15, 45) along
                           main line to (58, 45), then down-right to
                           (100, 70), brief pause, fade and snap
                           reset; the two endpoint markers brighten
                           to terracotta as the traveling dot
                           reaches them in their respective
                           sub-cycles, then fade back to warm
                           neutral; FIRST BRANCHING-PATH-TRAVERSAL
                           mechanic in the catalogue; visual
                           metaphor is validation as a binary gate
                           that produces pass (up) or fail (down)
                           outcomes on alternating cycles; distinct
                           from #1 particle flow (RADIAL CENTRIPETAL
                           convergence — particles travel inward
                           from edge to centre on radial paths) by
                           being HORIZONTAL → BRANCHING travel path
                           with ALTERNATING up-branch and down-branch
                           across cycles; distinct from #41
                           sequential pointer descent (VERTICAL list
                           with pointer DESCENDING through stationary
                           items) by being HORIZONTAL travel with
                           BRANCHING DIVERGENCE at the decision
                           point; distinct from #15 simple horizontal
                           traversal (single horizontal motion left
                           to right with no branching) by having a
                           BRANCHING POINT in the middle that
                           alternates direction across cycles; the
                           architectural signature is BRANCHING with
                           cycle-level alternation between branches)
    templates/adr-template → lifecycle progression trail (a horizontal
                           lifecycle axis at y=45 with FOUR fixed
                           phase markers (small circles, radius 4) at
                           x positions (20, 47, 74, 101) representing
                           the four ADR statuses Proposed / Accepted /
                           Deprecated / Superseded; three warm-neutral
                           connecting line segments between adjacent
                           markers always visible at low opacity; each
                           marker has THREE distinct visual states
                           rather than the binary on/off of prior
                           mechanics: state A warm-neutral baseline
                           (#D6D2C8) — the marker has not yet been
                           visited; state B dim terracotta (opacity
                           0.45) — the marker has previously been
                           active and now represents accumulated
                           history; state C bright terracotta (full
                           opacity) — the marker is currently active;
                           a 9-second cycle moves the active state
                           from marker 1 (Proposed, 0.5-2.0s) through
                           marker 2 (Accepted, 2.0-3.5s), marker 3
                           (Deprecated, 3.5-5.0s), marker 4
                           (Superseded, 5.0-6.5s); after a marker has
                           been active and the active dot moves on,
                           that marker drops to the dim history state
                           and remains visible (so by the time marker
                           4 is active, markers 1-3 are all in dim
                           history state); brief hold at 6.5-7.5s
                           with all four markers visible (full
                           lifecycle complete), then all reset
                           simultaneously to warm-neutral at
                           7.5-8.5s, brief pause and restart;
                           implementation uses animate on the fill
                           attribute of each marker through the three
                           states with appropriate keyTimes; FIRST
                           ACTIVE-VS-HISTORY THREE-STATE MARKER
                           mechanic in the catalogue; visual metaphor
                           is an ADR moving through its lifecycle
                           with prior states accumulated as visible
                           history; distinct from #6 sequential frame
                           illumination (single horizontal row of
                           frames where ONLY ONE is lit at any moment
                           — frames TAKE TURNS, do NOT ACCUMULATE
                           HISTORY) by having THREE visual states per
                           marker with PRIOR markers accumulating in
                           DIM HISTORY state; distinct from #41
                           sequential pointer descent (VERTICAL list
                           with pointer triangle DESCENDING through
                           stationary text-line items) by being
                           HORIZONTAL with active state moving and
                           prior positions accumulating dimmed;
                           distinct from #44 radial check bloom
                           (centre pivot + spokes + terminal markers
                           that activate clockwise and STAY at FULL
                           BRIGHTNESS until global reset) by:
                           (a) being LINEAR HORIZONTAL not
                           RADIAL/CIRCULAR; (b) having THREE visual
                           states per marker (off/dim/bright) rather
                           than just two (off/on); (c) only ONE
                           marker is bright at a time, with PRIOR
                           markers DIMMED rather than at full
                           brightness; distinct from #48 character
                           sequence typing (six rectangles fading in
                           via opacity, all visible at end with all
                           clearing simultaneously) by having the
                           active state SHIFTING POSITION over time
                           rather than items being purely additive,
                           and by having three visual states per
                           marker rather than binary; the
                           architectural signature is lifecycle
                           progression with accumulated history
                           visible)
    templates/review-template → branching tree formation (a single
                           central terracotta node (filled circle
                           radius 4) at (60, 45) representing the
                           Review document itself, always visible;
                           three terminal nodes (warm-neutral filled
                           circles radius 3.5) at IRREGULAR positions
                           around the central node — top (35, 18),
                           right (98, 38), bottom (45, 72) —
                           representing the three review components
                           Findings / Decision / Outcomes; three
                           branch lines connecting central node to
                           each terminal at IRREGULAR angles, each
                           drawn via stroke-dasharray animation that
                           grows the line in from the central node
                           toward its terminal: branch line stroke-
                           dasharray animates from "0 length" (no
                           visible stroke) to "length 0" (full
                           stroke drawn from start to end), where
                           "length" is the line's actual length plus
                           a small buffer; an 8-second cycle draws
                           branch 1 in 0.4-1.6s, then terminal 1
                           brightens from warm-neutral to terracotta
                           1.6-1.8s; branch 2 draws in 1.8-3.0s,
                           terminal 2 brightens 3.0-3.2s; branch 3
                           draws in 3.2-4.4s, terminal 3 brightens
                           4.4-4.6s; hold complete with all branches
                           and terminals visible 4.6-6.5s; all clear
                           simultaneously 6.5-7.0s (snap reset);
                           brief pause 7.0-8.0s before restart;
                           FIRST STROKE-DASHARRAY-ON-LINE-SEGMENTS
                           mechanic in the catalogue (prior stroke-
                           dasharray usage in #49 was on a CIRCLE
                           PERIMETER, not on straight line segments);
                           visual metaphor is a review document
                           branching out into its constituent
                           findings/decision/outcomes; distinct from
                           #44 radial check bloom (centre pivot + 6
                           SPOKES at evenly distributed angles + 6
                           terminal markers; spokes ALWAYS VISIBLE
                           from cycle start, only terminal markers
                           brighten in clockwise sequence) by:
                           (a) only THREE branches not six;
                           (b) branches at IRREGULAR angles not
                           evenly distributed; (c) branches
                           THEMSELVES are ANIMATED to draw in via
                           stroke-dasharray (NOT always-visible —
                           they grow into existence sequentially);
                           (d) terminal nodes APPEAR (brighten)
                           AFTER their respective branch completes
                           drawing rather than the always-present-
                           then-brighten pattern; distinct from #46
                           concentric ring activation (FOUR NESTED
                           rings activating outermost-to-innermost)
                           by being SPOKES AT IRREGULAR ANGLES not
                           nested rings; distinct from #49 perimeter
                           fill ring (stroke-dasharray on a CIRCLE
                           PERIMETER filling clockwise) by being
                           stroke-dasharray on STRAIGHT LINE SEGMENTS
                           at different angles, with discrete
                           branches not a continuous perimeter; the
                           architectural signature is sequential
                           drawing-in of irregular branches with
                           terminal-after-branch activation)
    templates/scorecard-template → radial dimension bars (a central
                           terracotta pivot (filled circle radius
                           2.5) at (60, 45) always visible; SIX guide
                           spokes (warm neutral, opacity 0.4 always
                           visible at low contrast) extending from
                           centre to maximum-radius positions at
                           evenly-spaced 60° angles: spoke 1 to
                           (60, 15) (12 o'clock), spoke 2 to (86, 30)
                           (2 o'clock), spoke 3 to (86, 60) (4
                           o'clock), spoke 4 to (60, 75) (6 o'clock),
                           spoke 5 to (34, 60) (8 o'clock), spoke 6
                           to (34, 30) (10 o'clock); SIX max-position
                           guide markers (warm-neutral filled circles
                           radius 1.8 at the spoke endpoints, opacity
                           0.7 always visible) representing the
                           "max possible level" on each dimension;
                           SIX terracotta active bars (lines with
                           stroke-width 2.2, stroke-linecap round)
                           starting at centre and extending OUTWARD
                           to VARIABLE end positions representing
                           per-dimension current ratings: bar 1 to
                           (60, 21) (high readiness 24/30), bar 2 to
                           (76, 33) (moderate observability 19/30),
                           bar 3 to (83, 58) (strong security 26/30),
                           bar 4 to (60, 62) (moderate reliability
                           17/30), bar 5 to (41, 56) (good
                           performance 22/30), bar 6 to (49, 34)
                           (weak cost efficiency 13/30) — the SIX
                           VARIABLE end positions form a radar-chart
                           polygon when all bars are extended; an
                           8-second cycle: 0-0.4s all bars retracted
                           to centre; bar 1 extends 0.4-1.4s; bar 2
                           extends 1.4-2.4s; bar 3 extends 2.4-3.4s;
                           bar 4 extends 3.4-4.4s; bar 5 extends
                           4.4-5.4s; bar 6 extends 5.4-6.4s (all six
                           dimensions now rated, full radar polygon
                           visible); hold 6.4-7.4s; all bars retract
                           simultaneously 7.4-7.8s; brief pause
                           7.8-8.0s before restart; implementation
                           uses animate on x2 and y2 attributes of
                           each line element with keyTimes designed
                           for sequential extension and simultaneous
                           retraction; FIRST CENTRIFUGAL VARIABLE-
                           LENGTH RADIAL EXTENSION mechanic in the
                           catalogue; visual metaphor is a multi-
                           dimensional service rating extending
                           outward from a central pivot to encode
                           per-dimension scores in the polygon
                           shape; distinct from #1 particle flow
                           (RADIAL CENTRIPETAL — particles travel
                           inward from edge to centre) by being
                           CENTRIFUGAL (lines extend OUTWARD from
                           centre) and by extending to VARIABLE end
                           positions, not converging on a single
                           point; distinct from #44 radial check
                           bloom (centre pivot + 6 FIXED-LENGTH
                           SPOKES + 6 terminal markers at FIXED
                           max-radius positions; markers brighten in
                           clockwise sequence) by: (a) bars EXTEND
                           from centre OUTWARD via x2/y2 line-
                           endpoint animation — they grow into
                           existence — rather than fixed-length
                           spokes whose terminals brighten; (b) each
                           bar's endpoint is at a VARIABLE position
                           (per-dimension rating, lower than max),
                           not at the max-radius position; (c) the
                           accumulated radar shape (6 bars at
                           variable end positions) IS the rating
                           visual — a multi-dimensional polygon
                           whose shape encodes the per-dimension
                           scores; distinct from #46 concentric ring
                           activation (FOUR NESTED rings at different
                           radii activating outermost-to-innermost)
                           by being SPOKES at evenly-distributed
                           angles, not nested rings; distinct from
                           #47 cyclic path marker (single dot
                           traveling around a closed CIRCLE
                           perimeter; fixed phase markers brighten
                           as the dot passes) by having SIX STATIC
                           bars that EXTEND from centre, not a
                           traveling marker; distinct from #49
                           perimeter fill ring (stroke-dasharray on
                           a CIRCLE PERIMETER filling clockwise) by
                           extending RADIAL LINES outward via line-
                           endpoint animation, not by filling a
                           perimeter; distinct from #52 branching
                           tree formation (3 IRREGULAR branches with
                           stroke-dasharray growth and terminal
                           nodes that appear after each branch
                           completes) by having 6 EVENLY-SPACED bars
                           with VARIABLE end positions (radar-chart
                           polygon, not branching tree) and using
                           x2/y2 line-endpoint animation rather than
                           stroke-dasharray; the architectural
                           signature is multi-dimensional centrifugal
                           extension to variable end positions
                           encoding per-dimension scores)
    playbooks/api-lifecycle → dual-track parallel lifecycle (TWO
                           horizontal tracks at y=32 and y=58
                           with semi-transparent baselines (warm
                           neutral, opacity 0.4) running x=15
                           to x=105; each track has FOUR phase
                           markers (warm-neutral filled circles
                           radius 1.6, opacity 0.7) at evenly
                           spaced positions x=29, 54, 79, 104
                           representing FOUR LIFECYCLE PHASES
                           per track; upper track v1 phases are
                           GA→Maintenance→Deprecated→Retired;
                           lower track v2 phases are
                           Design→Beta→GA→Maintenance; TWO
                           terracotta version blocks (rounded
                           rectangles 14×6, rx=1.5) one per
                           track, sliding rightward through
                           phase positions over a 10-second
                           cycle; v1 block (upper) at full
                           opacity slides through GA at t=0,
                           Maintenance at t=2.5s, Deprecated at
                           t=5s, Retired at t=7.5s, fades to
                           opacity 0 by t=8.8s, snaps back to
                           start position at t=9s, fades back
                           in by t=10s; v2 block (lower) starts
                           at low opacity 0.35 in Design phase
                           at t=0, brightens to opacity 1 at
                           t=2.5s entering Beta, slides through
                           GA at t=5s, Maintenance at t=7.5s,
                           fades and snaps back at t=8.8-9s;
                           the two blocks at any given moment
                           are at DIFFERENT phase positions on
                           their respective tracks, encoding
                           multi-version coexistence (when v1
                           is in Deprecated, v2 is in GA — same
                           horizontal pixel position but
                           different lifecycle meaning per
                           track); FIRST DUAL-TRACK PARALLEL
                           TIMELINE mechanic in the catalogue;
                           visual metaphor is two API versions
                           coexisting through their lifecycles
                           on parallel tracks with version
                           blocks moving along them in sync but
                           encoding different lifecycle phases;
                           distinct from #51 lifecycle progression
                           trail (SINGLE track with FOUR phase
                           markers and an ACTIVE-STATE DOT moving
                           with HISTORY-BAR ACCUMULATION
                           connecting visited markers on the
                           same single track) by having TWO
                           PARALLEL tracks with TWO different
                           blocks at DIFFERENT phase positions
                           — encoding coexistence rather than
                           progression-with-history; distinct
                           from #15 horizontal traversal (single
                           marker traversing one track) by having
                           TWO blocks on TWO tracks; distinct
                           from #41 sequential pointer descent
                           (vertical pointer moving down through
                           items) by being HORIZONTAL with two
                           tracks; distinct from #50 branching
                           decision flow (one marker on a path
                           with branching alternation) by having
                           parallel non-branching tracks; the
                           architectural signature is multi-
                           version parallel lifecycle with
                           coexistence visible through different
                           positions on parallel tracks)
    playbooks/migration → proportional traffic shift (a SINGLE
                           composite horizontal bar centred at
                           y=45 with total span x=20 to x=100,
                           height 12, rx=1.5; bar is divided
                           into TWO segments by a vertical
                           DIVIDER line at variable x position;
                           LEFT segment (terracotta) is the
                           legacy share; RIGHT segment (warm
                           neutral, opacity 0.55) is the new
                           share; warm-neutral frame outline
                           wraps the full bar at low opacity;
                           "legacy" label at (28, 30) and "new"
                           label at (88, 30) above the bar in
                           warm neutral; FOUR tick marks below
                           the bar at x=36, 52, 68, 84 with
                           "25%" "50%" "75%" "100%" percentage
                           labels in warm neutral at low opacity;
                           DIVIDER LINE is a vertical warm-neutral
                           line of stroke-width 1.5 from y=35 to
                           y=55 with two cap dots (warm-neutral
                           filled circles radius 1.5) at the top
                           and bottom of the divider; over an
                           8-second cycle, the divider's x
                           position animates from x=100 (start,
                           full legacy: left segment width 80,
                           right segment width 0) to x=20 (end,
                           full new: left segment width 0, right
                           segment width 80); divider holds at
                           x=20 from t=7s to t=8s for "all-new
                           settled" pause; at t=8s the divider
                           snaps back to x=100 (cycle restart);
                           keyTimes are 0; 0.05; 0.875; 1; 1
                           with values 100; 100; 20; 20; 100 for
                           the divider position; the legacy
                           segment's WIDTH animates synchronously
                           from 80 to 0; the new segment's BOTH
                           x AND width animate synchronously (x
                           from 100 to 20, width from 0 to 80);
                           FIRST PROPORTIONAL-DIVIDER-MIGRATION
                           mechanic in the catalogue; visual
                           metaphor is strangler-fig progressive
                           cutover where traffic shifts
                           proportionally from legacy to new on
                           the same channel as the divider
                           migrates leftward over time; distinct
                           from #45 sequential vertical fill
                           (VERTICAL bars filling from BOTTOM
                           upward in DISCRETE STAGES that
                           ACCUMULATE) by being a HORIZONTAL
                           composite bar with a CONTINUOUS
                           MIGRATING DIVIDER between TWO co-
                           existing PROPORTIONAL SEGMENTS rather
                           than vertical bars filling
                           sequentially; distinct from #18
                           horizontal sliding bars (SEPARATE
                           bars sliding into POSITION) by having
                           ONE composite bar with an INTERNAL
                           DIVIDER, not separate bars; distinct
                           from #11 vertical bars rising (HEIGHT-
                           based growth from baseline) by being
                           WIDTH-based PROPORTION shift; distinct
                           from #15 single horizontal traversal
                           (one marker traversing a path) by
                           having a DIVIDING LINE between TWO
                           PROPORTIONAL SEGMENTS rather than a
                           traveling marker; distinct from #54
                           dual-track parallel lifecycle (TWO
                           tracks with TWO blocks moving along
                           them) by having ONE composite bar
                           with internal proportional division;
                           the architectural signature is
                           proportional-divider migration
                           encoding gradual cutover with old and
                           new co-existing on the same channel
                           at varying ratios)
    playbooks/resilience → elastic pulse propagation (FIVE
                           vertical bars at x = 24, 42, 60, 78,
                           96, each width 8 with rx=1.5, baseline
                           y=30 height=40 (extending from y=30
                           to y=70); horizontal baseline ground
                           line from x=15 to x=105 at y=72,
                           opacity 0.5 (warm neutral); a SHOCK
                           DOT (terracotta filled circle radius
                           2) traverses from x=10 to x=110 at
                           y=20 over the 7-second cycle, fading
                           in at the start and out at the end;
                           as the shock dot reaches each bar's
                           x position, that bar TEMPORARILY
                           COMPRESSES — the bar's TOP (y) animates
                           DOWN from y=30 to y=42 while its
                           HEIGHT animates DOWN from 40 to 20
                           (the bar's BOTTOM stays anchored at
                           y=70 since y+height = 70 in both
                           states), then the bar RESTORES to
                           full height; each bar's compression
                           lasts ~0.4 seconds with restoration
                           by ~0.5 seconds after compression;
                           the cascade is staggered by ~1 second
                           per bar; bar 1 compressed at t=0.7-1.5s
                           (keyTimes 0.1, 0.157, 0.214); bar 2
                           at t=1.7-2.5s (keyTimes 0.243, 0.3,
                           0.357); bar 3 at t=2.7-3.5s; bar 4
                           at t=3.7-4.5s; bar 5 at t=4.7-5.5s;
                           all bars at rest from 5.5-7s; the
                           bottom edge of each bar stays
                           anchored to the baseline ground line
                           throughout; FIRST ELASTIC-PULSE-
                           PROPAGATION mechanic in the catalogue
                           with TEMPORARY DEFORMATION AND FULL
                           RECOVERY; visual metaphor is a shock
                           wave passing through system layers,
                           each layer absorbing the impact
                           visibly (compressing) then restoring
                           to original height — encoding
                           resilience as the universal
                           restoration after the cascade;
                           distinct from #11 vertical bars
                           rising (bars GROWING UP from zero
                           height to full height as the
                           accumulating outcome) by having bars
                           at FULL HEIGHT that COMPRESS DOWN
                           and RECOVER (deformation, not growth);
                           distinct from #18 horizontal sliding
                           bars (bars moving in POSITION
                           horizontally) by changing bars' HEIGHT
                           and Y position temporarily, not
                           position; distinct from #45 sequential
                           vertical fill (bars filling bottom-
                           to-top in DISCRETE STAGES that
                           ACCUMULATE) by having bars deform
                           briefly and FULLY RESTORE to original
                           state — nothing accumulates; distinct
                           from #46 concentric ring activation
                           (rings expanding OUTWARD from a centre)
                           by propagating LATERALLY through
                           vertical bars; distinct from #54 dual-
                           track parallel lifecycle (two
                           horizontal tracks with version blocks
                           moving) and #55 proportional traffic
                           shift (composite horizontal bar with
                           migrating divider) by being FIVE
                           SEPARATE VERTICAL bars with cascade
                           DEFORM-RECOVER mechanics; the
                           architectural signature is elastic
                           pulse propagation: a shock that moves
                           through the system, leaves a
                           temporary impression on each layer,
                           and is fully absorbed with no
                           permanent deformation)
  #57 STAIR-STEP MATURITY ASCENT (strategy/ai-readiness:
                           four horizontal rungs at ascending
                           heights — Aware at y=70, Experiment
                           at y=55, Operate at y=40, Strategic
                           at y=25 — with vertical dashed risers
                           between them; a single terracotta
                           marker dot ascends the staircase by
                           sliding right along each rung then
                           jumping vertically to the next; each
                           rung lights up terracotta as the
                           marker reaches it and stays lit
                           until the cycle restarts; faint
                           trace dot follows the path as a
                           history marker; distinct from #11
                           (vertical bars rising) — that is
                           PURELY VERTICAL with no horizontal
                           traversal; distinct from #15
                           (horizontal traversal) — that is
                           PURELY HORIZONTAL with no vertical
                           ascent; distinct from #45 sequential
                           vertical fill bottom-to-top — that
                           shows BARS FILLING, not a marker
                           moving; distinct from #51 lifecycle
                           progression trail — that has SINGLE
                           HORIZONTAL TRACK with history; #57
                           is the first mechanic to compose
                           horizontal slide + vertical step
                           into a stair-step ascent — the
                           architectural signature is staged
                           progression: each level requires
                           the prior level's foundation; the
                           visual maps directly onto AI
                           maturity progression where each
                           stage builds on the previous one)
  #58 QUADRANT POSITIONING CASCADE (strategy/modernization:
                           a 2×2 grid with axis lines crossing
                           at center represents the Strategic
                           Value × System Health portfolio
                           matrix; multiple small dots — each
                           representing a system in the
                           portfolio — appear in DIFFERENT
                           quadrants in staggered sequence,
                           encoding that portfolio assessment
                           positions every system somewhere
                           on the grid simultaneously; one
                           dot migrates from upper-left
                           quadrant (Migrate: high value, low
                           health) to upper-right quadrant
                           (Invest: high value, high health)
                           mid-cycle, encoding modernization
                           completion; trailing dashed arc
                           shows the migration path; distinct
                           from ALL prior mechanics which are
                           1D-distributed (along a horizontal
                           or vertical axis or perimeter); #58
                           is the first to distribute multiple
                           markers across a 2D quadrant grid
                           SIMULTANEOUSLY, with semantically
                           labelled regions (Migrate / Invest /
                           Tolerate / Eliminate); the single-
                           dot migration BETWEEN regions is
                           also novel — no prior mechanic
                           shows a marker traversing between
                           named semantic regions as a
                           narrative trajectory; the
                           architectural signature is portfolio
                           assessment with a strategic
                           trajectory: many systems positioned,
                           one being modernized)
  #59 FORWARD-RETURN FEEDBACK CYCLE (strategy/principles:
                           four stations arranged horizontally
                           at y=55 — Intent, Decisions,
                           Execution, Measurement — a single
                           terracotta marker sweeps left-to-
                           right through them at y=55 (the
                           forward path), each station briefly
                           highlighting as the marker passes;
                           on reaching Measurement, the marker
                           transitions to a CURVED RETURN ARC
                           traced ABOVE the linear path,
                           traveling right-to-left back to
                           Intent via an apex at (60,16); the
                           return arc is implemented through
                           cx/cy keyframes sampled from a
                           quadratic Bezier curve (NOT
                           animateMotion, which is forbidden
                           by convention); sampled Bezier
                           points: (98,55) → (82,42) → (66,36)
                           → (58,36) → (50,36) → (32,42) →
                           (14,55); distinct from #15
                           horizontal traversal — that has
                           NO RETURN ARC; distinct from #47
                           perimeter circle marker — that is
                           PURELY CIRCULAR with no straight
                           segment; distinct from #51
                           lifecycle progression trail — that
                           is SINGLE HORIZONTAL TRACK with
                           NO RETURN; distinct from #57 stair-
                           step ascent — that is STAIRCASE
                           PATTERN with no return; distinct
                           from #58 quadrant positioning —
                           that is 2D STATIC distribution
                           with no path; #59 is the first to
                           compose a STRAIGHT forward sweep
                           with a CURVED return arc into a
                           single continuous path — encoding
                           the closed-loop nature of the
                           strategy cycle: forward execution
                           plus feedback return, where
                           measurement informs the next
                           cycle's intent)
  #60 STACKED HORIZONTAL BAR-FILL CASCADE (scorecards/architecture-review:
                           four horizontal score-tracks stacked
                           vertically at y=20, 36, 52, 68;
                           each track is a faint warm-neutral
                           baseline running x=12 to x=104;
                           a terracotta fill bar grows
                           left-to-right along each track,
                           starting at x=12 and ending at a
                           DIFFERENT target x per track —
                           encoding that each review dimension
                           scores independently and the
                           per-dimension scores VARY; bar
                           growths are staggered (each starts
                           at a later time than the prior one)
                           so the visual reads as a cascade of
                           independent ratings landing in
                           sequence; after all four bars have
                           completed their fills, a small
                           terracotta verdict mark appears
                           below the lowest bar (centred at
                           x=58, y=82) encoding the aggregate
                           verdict; distinct from #11 vertical
                           bars rising — that is PURELY
                           VERTICAL with bars all reaching the
                           same height; distinct from #45
                           sequential vertical fill — that is
                           bottom-to-top and all bars reach
                           the top; distinct from #51
                           lifecycle progression trail — that
                           is a SINGLE horizontal track with a
                           moving marker, not multiple tracks
                           with growing fills; distinct from
                           #56 progressive threshold fill —
                           that is a SINGLE horizontal fill
                           pausing at canary checkpoints, not
                           multiple parallel fills with
                           varying endpoints; #60 is the first
                           mechanic to use multiple parallel
                           horizontal fills WITH VARYING
                           endpoints PLUS a separate aggregate
                           verdict element appearing after the
                           cascade completes — encoding the
                           scorecard signature: independent
                           dimensional scoring producing one
                           collective verdict)
  #61 GAP-ARROW VISUALIZATION (scorecards/nfr:
                           three horizontal NFR-category
                           tracks at y=22, 45, 68; each track
                           runs x=10 to x=110 as a faint
                           warm-neutral baseline; each track
                           carries TWO markers — a terracotta
                           "current state" dot and a warm-
                           neutral "target state" dot — at
                           DIFFERENT x positions per track,
                           with target always to the right of
                           current; a terracotta dashed gap
                           line connects current to target on
                           each track, drawing itself via
                           stroke-dasharray animation; markers
                           appear in cascade (track 1 at
                           t=0.10, track 2 at t=0.30, track 3
                           at t=0.50), gap line for each
                           track draws immediately after both
                           markers settle; gap lengths vary
                           per track — encoding that NFR gaps
                           differ by category and prioritisation
                           targets the largest gaps; distinct
                           from #15 horizontal traversal —
                           that is a single dot moving, no
                           paired markers, no gap visualization;
                           distinct from #51 lifecycle
                           progression — that is a single
                           track with a moving marker and
                           historical trail; distinct from
                           #58 quadrant positioning — that
                           plots dots in 2D regions, not
                           pairs along 1D scales; distinct
                           from #60 stacked bar fill — that
                           shows fills GROWING from left to
                           target endpoints, not paired
                           current-target markers with a gap
                           line; #61 is the first mechanic to
                           pair TWO markers per track with an
                           explicit gap-line connector,
                           visualising the delta between
                           current and target — the
                           architectural signature is
                           gap-driven prioritisation: the
                           visible space between markers is
                           the work)
  #62 SPOKE CONVERGENCE TO CENTRE (scorecards/principles:
                           four outer "criterion" dots
                           positioned in a vertical column on
                           the LEFT at x=14, y=18/38/56/76;
                           one central "score" node at
                           (x=92, y=46); four spokes (lines)
                           extend from each outer dot to the
                           central node, each spoke drawing
                           itself in sequence via
                           stroke-dasharray animation; spoke
                           1 draws at t=0.10–0.25, spoke 2 at
                           t=0.30–0.45, spoke 3 at t=0.50–0.65,
                           spoke 4 at t=0.70–0.85; the central
                           node opacity rises progressively
                           from 0.25 → 0.50 → 0.75 → 1.0 as
                           each spoke completes (encoding
                           that each criterion contributes
                           to the aggregate score); after all
                           four spokes complete, the central
                           node pulses (radius 4 → 5 → 4) at
                           t=0.85–0.95 encoding the final
                           aggregate principle score; distinct
                           from #1 particle flow — that has
                           DOZENS of small particles, not
                           four discrete spokes; distinct from
                           patterns/security perimeter tracing
                           — that draws CONCENTRIC RINGS, not
                           radial spokes; distinct from #47
                           perimeter circle marker — that is a
                           moving dot on a circle, no
                           convergent geometry; distinct from
                           #61 gap-arrow — that uses parallel
                           horizontal tracks, not radial
                           convergence; #62 is the first
                           mechanic to use spoke-based
                           convergence (multiple discrete
                           lines drawing themselves toward a
                           single accumulating central node) —
                           the architectural signature is
                           evidence-aggregation: each
                           criterion contributes a discrete
                           strand of evidence and the
                           principle score accumulates as
                           strands attach)
  #63 ITERATIVE CONVERGENCE TO TARGET WITH DIMINISHING JUMPS
                          (maturity/guidelines: a faint warm-neutral
                           horizontal baseline runs at y=45 from
                           x=10 to x=110; a fixed warm-neutral target
                           marker (filled circle r=4 plus subtle outer
                           ring r=6) sits at (104, 45) on the right;
                           a terracotta current-state marker (filled
                           circle r=3) starts at x=14 on the left and
                           JUMPS via cx animation through three
                           successive discrete jumps of decreasing
                           length: jump 1 at t=0.18-0.22 covers
                           x=14→50, jump 2 at t=0.34-0.38 covers
                           x=50→78, jump 3 at t=0.50-0.54 covers
                           x=78→92; after each jump, the current
                           marker pulses r 3→4.5→3 confirming the
                           assessment landed; the marker holds at
                           x=92 from t=0.62-0.85, NEVER fully
                           reaching the target, encoding diminishing-
                           returns convergence; distinct from #15
                           horizontal traversal — that uses
                           continuous motion across a single trip,
                           no discrete jumps; distinct from #51
                           lifecycle progression — that has a
                           moving marker with historical trail along
                           a single track, no discrete jump
                           structure; distinct from #57 stair-step
                           ascent — that climbs vertical stairs in
                           equal-sized steps in 2D; distinct from
                           #61 paired-marker gap-arrow — that uses
                           paired static markers with a connecting
                           gap line, no marker movement; #63 is the
                           first mechanic to use cx jumps with
                           diminishing distances and per-jump pulse
                           confirmation — the architectural signature
                           is iterative-with-diminishing-returns:
                           maturity assessment cycles produce
                           shrinking improvements toward a target
                           that is rarely fully reached)
  #64 PARALLEL MULTI-LEVEL LADDERS WITH VARYING RUNG COUNTS
                          (maturity/models: four vertical "ladder"
                           spines (faint warm-neutral lines from
                           y=14 to y=78) at x=20, 50, 80, 110; each
                           ladder carries a DIFFERENT NUMBER of
                           horizontal terracotta "rungs" — ladder 1
                           has 3 rungs (at y=66/44/22), ladder 2 has
                           4 rungs (at y=70/52/34/16), ladder 3 has
                           5 rungs (at y=72/58/44/30/16), ladder 4
                           has 5 rungs (same y as ladder 3); rungs
                           light up bottom-to-top sequentially across
                           the cycle — ALL bottom rungs at t=0.10,
                           ALL second rungs at t=0.20, etc., with
                           ladders dropping out of the cascade once
                           their top rung is reached (ladder 1 stops
                           lighting after t=0.30, ladder 2 after
                           t=0.40, ladders 3/4 after t=0.50); after
                           all rungs light, each ladder's TOP rung
                           pulses stroke-width 2.4→3.6→2.4 on
                           independent sub-cycles (1.2s, 1.4s, 1.6s,
                           1.8s) encoding "maturity ceiling reached,
                           model staying alive in monitoring";
                           distinct from #11 vertical bars rising —
                           that has continuous bar fills all reaching
                           SAME height, no discrete rungs, no varying
                           total counts; distinct from #45 sequential
                           vertical fill — that is a single pillar
                           with continuous bottom-to-top fill;
                           distinct from #57 stair-step ascent —
                           that is a single zig-zag staircase in 2D
                           with equal-sized steps, not parallel
                           vertical ladders; distinct from #60
                           stacked horizontal bar-fill cascade —
                           that has horizontal fills, not vertical
                           rung-by-rung lighting; #64 is the first
                           mechanic to use multiple parallel vertical
                           ladders with STRUCTURALLY DIFFERENT rung
                           counts per ladder plus per-ladder ceiling
                           pulse — the architectural signature is
                           structural-heterogeneity-across-instruments:
                           the catalogue contains models whose level
                           structures genuinely differ, and a survey
                           across them must respect that difference
                           rather than averaging it away)
  #65 SAWTOOTH DEGRADATION-RECOVERY TRACE
                          (nfr/maintainability: a fixed warm-neutral
                           target band runs horizontally at y=58 from
                           x=10 to x=110; a single terracotta
                           polyline draws left-to-right via
                           stroke-dashoffset (220→0) shaped as a
                           sawtooth wave with three peaks — rises
                           from y=58 to y=22 (degradation), drops
                           back to y=58 (refactor), repeats two
                           more times, ending at (110,58); during
                           the held phase, two terracotta recovery
                           markers (r=2.4) pulse at the trough
                           positions (48,58) and (82,58) on 1.2s
                           sub-cycles encoding the refactor moments;
                           distinct from #15 horizontal traversal —
                           single dot moving along straight track
                           with no shape information; distinct from
                           #51 lifecycle progression — single track
                           with a moving marker plus historical
                           trail along a flat line, no waveform;
                           distinct from #57 stair-step ascent —
                           ascending vertical staircase with equal-
                           sized steps in 2D, not a horizontal
                           waveform; distinct from #60 stacked
                           horizontal bar-fill cascade — multiple
                           horizontal bars filling, not a single
                           shaped polyline; #65 is the first mechanic
                           to use a hand-shaped polyline drawn left-
                           to-right via stroke-dashoffset that
                           visibly exhibits both drift (upward
                           degradation) and recovery (downward
                           refactor) phases — the architectural
                           signature is cyclical-degradation-and-
                           recovery: code-health is a trajectory
                           shaped by the interplay of feature
                           delivery and refactor investment, neither
                           a steady decline nor a fixed equilibrium)
  #66 PERCENTILE TAIL FAN-OUT
                          (nfr/performance: three concurrent
                           horizontal traces share a common origin
                           at x=12 and grow rightward (via x2
                           animation) at the same rate over t=0.10
                           to t=0.20 but terminate at DIFFERENT
                           endpoints — P50 trace at y=24 ends at
                           x=42, P95 trace at y=46 ends at x=78,
                           P99 trace at y=68 ends at x=98; a fixed
                           warm-neutral budget marker (vertical
                           dashed line) sits at x=104 from y=14 to
                           y=78 showing the latency ceiling; the
                           three traces visibly fan out from a shared
                           origin to different endpoints encoding
                           distribution percentiles; after extension,
                           three terracotta endpoint markers (r=2.6)
                           pulse on independent sub-cycles 1.0s,
                           1.4s, 1.8s; distinct from #60 stacked
                           horizontal bar-fill cascade — that has
                           four sequential bars, not three concurrent;
                           no shared origin; distinct from #61
                           paired-marker gap-arrow — paired markers
                           with connecting line, no shared origin,
                           no fan-out shape; distinct from #65
                           sawtooth trace — single shaped polyline
                           not three traces; distinct from #63
                           iterative convergence — single marker
                           jumping toward fixed target, not three
                           markers fanning out; #66 is the first
                           mechanic to use three concurrent left-
                           to-right traces from a SHARED ORIGIN to
                           DIFFERENT endpoints encoding distribution
                           percentiles with a fixed budget threshold
                           visible — the architectural signature is
                           distribution-shape-exposure: averages
                           hide tail behaviour, the fan-out makes
                           the distinction visible)
  #67 DUAL-NODE FAILOVER ALTERNATION
                          (nfr/reliability: two discrete circular
                           nodes side-by-side — primary at (32,45)
                           with r=8, standby at (88,45) with r=8 —
                           connected by a horizontal heartbeat line
                           at y=45 from x=40 to x=80; each node has
                           a warm-neutral background circle (always
                           visible, opacity 0.4) layered with a
                           terracotta active overlay whose opacity
                           switches between full and zero; primary
                           active 0.10–0.40, then failover at 0.40–
                           0.45 simultaneously fades primary to dim
                           and brightens standby; standby active
                           0.45–0.75; recovery at 0.75–0.80 brightens
                           primary and fades standby; primary again
                           active 0.80–0.90; both nodes pulse via r
                           animation 8→9.5→8 on 1.0s sub-cycle while
                           active; the heartbeat line pulses stroke-
                           width 1.2→2.0→1.2 on 0.8s sub-cycle
                           continuously; distinct from #62 spoke
                           convergence to centre — multiple spokes
                           converging to one node, not alternating
                           roles between two; distinct from #65
                           sawtooth trace — single trace shape, no
                           two-node structure; distinct from #66
                           percentile fan-out — three traces from
                           shared origin, not alternation; #67 is
                           the first mechanic to use TWO DISCRETE
                           NODES that ALTERNATE active/inactive
                           states with simultaneous opposite
                           transitions, connected by a continuous
                           heartbeat line — the architectural
                           signature is reliability-as-redundancy:
                           traffic moves between nodes, individual
                           node failure does not cause system
                           failure, the system maintains availability
                           through alternation)
  #68 STACKED CONTROL-LAYER VERIFICATION
                          (nfr/security: four faint warm-neutral
                           horizontal divider lines at y=14, 26, 42,
                           58, 74 (from x=14 to x=88) define four
                           stacked layer bands; a terracotta packet
                           (r=2.6) at cx=24 descends top-to-bottom
                           via cy animation through the keyTimes
                           sequence 14→26→42→58→78 over t=0.10 to
                           t=0.56; as the packet exits each layer's
                           lower boundary, a terracotta verification
                           stamp (r=3) appears at the right edge at
                           x=98 with cy matching the layer middle
                           y=20, 34, 50, 66; stamps appear sequentially
                           at t=0.20, 0.32, 0.44, 0.56 and pulse on
                           independent sub-cycles 1.2s, 1.4s, 1.6s,
                           1.8s during the held phase; distinct from
                           #11 vertical bars rising — continuous bar
                           fills with no layer structure or traveling
                           marker; distinct from #46 concentric ring
                           activation — rings expanding from centre,
                           not horizontal stacked layers; distinct
                           from #57 stair-step ascent — zig-zag
                           staircase with single path, no per-layer
                           emit pattern; distinct from #60 stacked
                           horizontal bar-fill cascade — bars filling
                           left-to-right, not a marker descending
                           through layers emitting stamps; distinct
                           from #64 parallel ladders with rungs —
                           parallel vertical ladders with horizontal
                           rungs, not a single descending packet;
                           #68 is the first mechanic to use horizontal
                           layer-bands stacked vertically with a
                           top-to-bottom traveling marker that emits
                           a per-layer verification stamp at the
                           right edge as it traverses each layer —
                           the architectural signature is defence-
                           in-depth-with-explicit-verification: each
                           layer produces evidence of having
                           inspected the request, the system can
                           prove approval came from the full stack
                           rather than a single layer)
  #69 TASK-FLOW MARKER WITH FRICTION COMPRESSION
                          (nfr/usability: a horizontal warm-neutral
                           path baseline at y=45 from x=10 to x=110;
                           two warm-neutral vertical friction markers
                           at x=46 and x=80, each running from y=38
                           to y=52 (visible obstacles in the flow);
                           a terracotta ellipse marker (cx=16, cy=45,
                           rx=4, ry=4) traverses the path via cx
                           animation through five phases — start at
                           x=16, cross to x=46 (friction zone 1),
                           cross to x=80 (friction zone 2), cross
                           to x=104 (endpoint); at each friction
                           zone the ellipse COMPRESSES — rx animates
                           4→3 (slowed forward motion) and ry
                           animates 4→2 (squeezed vertically) over
                           a brief window, then relaxes back; after
                           reaching x=104, a terracotta completion
                           marker (r=2.6) appears at the endpoint
                           and pulses r 2.6→4→2.6 on 0.8s sub-cycle;
                           distinct from #15 horizontal traversal —
                           single dot moving across uniform track
                           with no compression events; distinct
                           from #51 lifecycle progression — single
                           track with marker AND historical trail,
                           no friction encoding; distinct from #67
                           dual-node failover — two static nodes
                           alternating, not a single moving marker;
                           distinct from #65 sawtooth trace — single
                           shaped polyline drawn via stroke-
                           dashoffset, not a moving ellipse with
                           shape compression; #69 is the first
                           mechanic to use ellipse rx/ry compression
                           to encode friction along a traversal
                           path — the architectural signature is
                           task-flow-with-friction: usability is not
                           the absence of friction but the ratio of
                           progress to friction across the path,
                           and the compression-and-resume rhythm
                           encodes that good UX acknowledges friction
                           explicitly rather than hiding it)
  #70 TIERED-CADENCE PARALLEL PROGRESS
                          (compliance/bsp-afasa: three horizontal
                           track-bars stacked vertically — top track
                           at y=22 (annual cadence), middle at y=45
                           (quarterly), bottom at y=68 (monthly) —
                           each with a faint warm-neutral baseline
                           x=14 to x=104; a terracotta progress bar
                           grows from x=14 rightward along each
                           track via x2 animation, but at INDEPENDENT
                           rates: annual track completes ONCE over
                           the cycle (single fill 14→104 over t=
                           0.10–0.85), quarterly track completes
                           4 times (4 fill-and-reset cycles within
                           t=0.10–0.85), monthly track completes 3
                           times (simplified for legibility); when
                           each progress bar reaches the right end,
                           a small terracotta "filed" badge (r=2.4)
                           pulses at (108, y) on a sub-cycle matched
                           to the cadence speed (annual badge 2.0s,
                           quarterly 1.4s, monthly 1.0s); distinct
                           from #11 vertical bars rising — those
                           are vertical and reach the SAME height,
                           #70 is horizontal with INDEPENDENT
                           completion times; distinct from #60
                           stacked horizontal bar-fill cascade —
                           that has 4 bars filling SEQUENTIALLY one
                           after another within a single cycle, #70
                           has 3 bars filling INDEPENDENTLY at
                           different rates with multiple completions
                           for the faster bars; distinct from #66
                           percentile fan-out — that has three
                           traces from a SHARED ORIGIN going to
                           different endpoints once, #70 has three
                           tracks completing cyclically at different
                           frequencies; the architectural signature
                           is multi-frequency-cyclical-obligation:
                           the compliance posture is defined by
                           accommodating multiple regulatory clocks
                           running simultaneously, each with its own
                           cadence and submission)
  #71 HEXAGONAL ROTATING ACTIVE-STATE
                          (compliance/gdpr: six discrete vertex
                           nodes arranged hexagonally at radius 24
                           from centre (60, 45) — vertex 0 at
                           (60, 21), vertex 1 at (80.78, 33), vertex
                           2 at (80.78, 57), vertex 3 at (60, 69),
                           vertex 4 at (39.22, 57), vertex 5 at
                           (39.22, 33); a faint warm-neutral hexagon
                           outline polygon connects the vertices as
                           guide; a static warm-neutral centre
                           marker (r=3) sits at (60, 45); each
                           vertex has a warm-neutral background
                           circle (r=5, opacity 0.4) layered with a
                           terracotta active overlay that toggles
                           opacity 0→1; the active state ROTATES
                           CLOCKWISE through all six vertices
                           sequentially, each active for ~0.11 of
                           the cycle (vertex 0: 0.10–0.21, vertex 1:
                           0.21–0.32, vertex 2: 0.32–0.43, vertex 3:
                           0.43–0.54, vertex 4: 0.54–0.65, vertex 5:
                           0.65–0.76), with EXACTLY ONE vertex
                           active at any time during sequential
                           phase; after sequence completes, ALL six
                           vertices brighten simultaneously during
                           t=0.76–0.85 (full register); each active
                           overlay pulses r 5→6→5 on 0.8s sub-cycle
                           while active; distinct from #46
                           concentric ring activation — those are
                           CIRCLES expanding outward from a centre
                           with continuous ring geometry, #71 has
                           DISCRETE VERTEX POINTS at fixed positions
                           with rotating active state; distinct
                           from #62 spoke convergence to centre —
                           that has spokes converging INWARD to a
                           centre with sustained pulse at centre,
                           #71 has rotating active state at OUTER
                           vertices with the centre as a static
                           marker; distinct from #67 dual-node
                           failover alternation — that has TWO
                           nodes alternating, #71 has SIX nodes
                           cycling with exactly one active at a
                           time; the architectural signature is
                           exclusive-state-rotation: at any moment
                           exactly one of N possible states is
                           active, encoding architectural decisions
                           like the GDPR rule that every processing
                           activity has exactly one lawful basis
                           chosen deliberately from a catalogue)
  #72 RISK-CONTROL CROSS-WALK LINES
                          (compliance/iso27001: two vertical
                           columns of nodes — left column with three
                           warm-neutral risk nodes (r=3.4) at (24,
                           24), (24, 45), (24, 66); right column
                           with three control-target positions at
                           (96, 30), (96, 50), (96, 60); three
                           terracotta diagonal lines drawn left-to-
                           right SEQUENTIALLY (not simultaneously)
                           via stroke-dashoffset (75→0) animation
                           connecting risk to control: line 1
                           (24,24)→(96,30) draws over t=0.10–0.30,
                           line 2 (24,45)→(96,50) draws over t=
                           0.30–0.50, line 3 (24,66)→(96,60) draws
                           over t=0.50–0.70; as each line completes,
                           the right-column endpoint becomes a
                           terracotta linkage indicator (r=3.4) with
                           opacity envelope appearing at line-end
                           and pulsing r 3.4→4.4→3.4 on independent
                           sub-cycles 1.0s, 1.4s, 1.8s; distinct
                           from #62 spoke convergence to centre —
                           that has multiple spokes converging from
                           outside to ONE central point (radial
                           convergence pattern), #72 has multiple
                           parallel diagonal lines between two
                           columns (lateral mapping pattern);
                           distinct from #64 parallel ladders —
                           those are vertical lines with horizontal
                           rungs, #72 is two columns of points
                           connected by diagonals; distinct from
                           #66 percentile fan-out — that has three
                           traces from a SHARED ORIGIN going to
                           different endpoints simultaneously, #72
                           has three lines from DIFFERENT ORIGINS
                           going to DIFFERENT endpoints drawn
                           SEQUENTIALLY; the architectural signature
                           is N-to-N traceability: every risk
                           traces to its mitigating control, every
                           control traces back to the risks it
                           mitigates, the trace is visible as the
                           architectural artefact)
  #73 BOUNDARY-CROSSING SHAPE TRANSFORMATION
                          (compliance/pci-dss: a vertical warm-
                           neutral boundary line at x=60, y=14 to
                           y=78, with dashed stroke pattern (3 3)
                           and tick-mark pips at top y=14 and bottom
                           y=78; three sequential "token paths" at
                           y=24, 45, 66 each carry a terracotta
                           CIRCLE (r=3.5) on the LEFT SIDE that
                           moves from x=14 to x=58 (just before
                           boundary), then at the boundary the
                           circle FADES OUT and a terracotta SQUARE
                           (rect 6×6) FADES IN at the same y
                           position, then the SQUARE moves from
                           x=62 to x=104 (right side); the three
                           paths run SEQUENTIALLY (not simultaneously)
                           with timing offsets — path 1 at t=
                           0.10–0.32, path 2 at t=0.30–0.52, path 3
                           at t=0.50–0.72; after all three crossings
                           complete, the three squares remain on the
                           right side and pulse via width and height
                           6→7→6 on independent sub-cycles 1.0s,
                           1.4s, 1.8s encoding tokens are persistent
                           in the non-CDE environment whereas the
                           PANs were ephemeral; distinct from #15
                           horizontal traversal — that uses a single
                           shape moving across uniform track with no
                           transformation, #73 has TWO DISTINCT
                           SHAPES representing different data states
                           with explicit transformation event at
                           boundary; distinct from #54 dual-track
                           parallel lifecycle — that has two parallel
                           horizontal tracks for two version blocks,
                           #73 has one track per path but with a
                           transformation point dividing pre- and
                           post-states; distinct from #67 dual-node
                           failover alternation — that has two
                           static nodes alternating, #73 has one
                           moving entity per path that changes form
                           during traversal; distinct from #68
                           stacked control-layer verification —
                           that has a marker descending vertically
                           through layers emitting per-layer stamps,
                           #73 has markers traversing horizontally
                           across a single boundary with shape
                           change; the architectural signature is
                           state-transformation-at-trust-boundary:
                           data exists in different forms on either
                           side of a trust boundary, and the
                           boundary's purpose is to perform the
                           transformation that converts sensitive to
                           non-sensitive form before propagation)
  Future pages must invent a new mechanic, not reuse one.
  Two colours only: warm neutral (#D6D2C8) + terracotta (#C96330).
  Basic SMIL primitives only (animate, animateTransform with type=rotate or translate; stroke-dasharray and opacity animations also valid via animate).
  No animateMotion / mpath (proven unreliable across browsers).

STUB CONTENT IS LOREM IPSUM:
  When a page is still a stub, only its TITLE and TAXONOMY (the
  section/subsection placement) are settled. The body text is a
  placeholder — feel free to expand it freely with proper content,
  add explanations, restructure it. Do not treat seed-generated
  stub prose as committed copy.

NO REPETITION ACROSS PAGES:
  Don't repeat the same concept, principle, or paragraph across
  multiple pages unless it is genuinely necessary (e.g. one page
  explicitly extends a concept from another, or a foundational
  concept is referenced as background). Each page should own its
  distinct lane. When two pages would naturally cover the same
  ground, reference the other page rather than restating.

═══════════════════════════════════════════════════════════════════════════════
"""

import re, sys, shutil, argparse, json
from pathlib import Path

# Import the canonical TAXONOMY from seed_content so we can render only
# subsections that are actually registered. Walking the filesystem alone
# would render any orphan stub directory left behind from a prior seed —
# producing the v28 ascendion.engineering/security/index.html bug where
# obsolete `appsec/`, `cloud/`, `vulnerability/` directories appeared
# alongside the current `application-security/`, `cloud-security/`,
# `vulnerability-management/`. Strictness here makes the TAXONOMY the
# single source of truth.
sys.path.insert(0, str(Path(__file__).parent))
from seed_content import TAXONOMY, CONCEPT_LENSES

try:
    import markdown
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
    MD = True
except ImportError:
    MD = False

# ─────────────────────────────────────────────────────────────────────────────
# MILLER'S LAW GROUPING — 6 groups of ≤7
# ─────────────────────────────────────────────────────────────────────────────
GROUPS = [
    ("Foundations",    "Core principles, patterns, and decision records",
     ["principles", "patterns", "anti-patterns", "adrs", "views"]),
    ("Architecture",   "System design, DDD, frameworks, and design practices",
     ["system-design", "design", "ddd", "frameworks"]),
    ("Technology",     "UI/UX, backend, data, cloud, DevOps, and engagement models",
     ["technology", "cloud", "infra", "data", "integration"]),
    ("Quality & Risk", "Security, compliance, governance, and non-functional requirements",
     ["security", "compliance", "governance", "nfr"]),
    ("Operations",     "Observability, runbooks, checklists, and tooling",
     ["observability", "runbooks", "checklists", "tools"]),
    ("Excellence",     "AI-native, maturity, strategy, scorecards, roadmaps, playbooks",
     ["ai-native", "ai", "maturity", "scorecards", "strategy", "roadmaps", "playbooks", "templates"]),
]

SECTIONS = {
    "principles":    ("Architecture Principles",              "Core principles and philosophies guiding all design decisions across the practice."),
    "patterns":      ("Architecture & Design Patterns",       "Canonical structural, integration, security, and data patterns."),
    "anti-patterns": ("Anti-Patterns",                        "Common design mistakes and legacy pitfalls to recognise and avoid."),
    "adrs":          ("Architecture Decision Records",        "ADRs documenting rationale, context, alternatives, and impact of key decisions."),
    "views":         ("Architecture Views",                   "Perspectives: logical, physical, process, deployment, and scenario."),
    "design":        ("Detailed Design Practices",            "Component and service-level design patterns and practices."),
    "system-design": ("System Design Reference Scenarios",    "End-to-end reference scenarios and trade-off analysis for scalable systems."),
    "ddd":           ("Domain-Driven Design",                 "Context mapping, bounded-context patterns, and aggregate design."),
    "frameworks":    ("Industry Frameworks Mapping",          "TOGAF, NIST CSF, ISO 27001, Zachman, and Gartner — mapped to practice."),
    "tech":          ("Technology Stack Best Practices",      "AWS, Azure, GCP, Java, Angular, DevOps, and AI/ML best practices."),
    "technology":    ("Technology",                            "Frontend, backend, data, cloud, DevOps, practice circles, and engagement models — how we deliver across the stack."),
    "infra":         ("Infrastructure Architecture",          "IaC, networking, CI/CD, and operational excellence practices."),
    "cloud":         ("Cloud Architecture",                   "Multi-cloud reference architectures across AWS, Azure, and GCP."),
    "ai":            ("AI-Native Architecture",               "AI-native patterns, LLMOps, RAG, agentic systems, and governance."),
    "ai-native":     ("AI-Native",                             "Production-grade AI systems: architecture, responsible-AI engineering, observability, retrieval, and the AI-specific threat surface."),
    "security":      ("Security Architecture",                "End-to-end security design: AuthN/AuthZ, encryption, and cloud controls."),
    "compliance":    ("Compliance & Regulatory Frameworks",   "Standards mappings and compliance controls for enterprise environments."),
    "governance":    ("Architecture Governance",              "How the governance system itself runs: checklists, review templates, roles and authority, and scorecards measuring whether governance is working."),
    "nfr":           ("Non-Functional Requirements",          "Performance, availability, scalability, and security NFR evaluation."),
    "data":          ("Data Architecture",                    "Data modeling, governance, lineage, mesh patterns, and analytics."),
    "integration":   ("Integration Architecture",             "API, event, messaging, workflow, and partner integration patterns."),
    "observability": ("Observability",                        "The foundational observability primitives — incident response, structured logging, metrics, SLIs/SLOs, and distributed tracing — that any production system depends on, separate from AI-specific monitoring."),
    "tools":         ("Architecture Tooling",                 "The engineering tools the team uses to build, validate, and operate systems — AI agents, CLI tools, scripts, and validators — as designed artefacts with composability, observability, and lifecycle properties, distinct from the systems they help build."),
    "checklists":    ("Review Checklists",                    "The artefacts a reviewer applies during structured review work — architecture, deployment readiness, and security checklists — as designed coverage instruments with dimensions, calibration, and tier-awareness, distinct from the governance disciplines that produce them."),
    "runbooks":      ("Operational Runbooks",                 "The artefacts a responder picks up under pressure — incident, migration, and rollback runbooks — as designed documents with structure, calibration, and lifecycle, distinct from the operational disciplines they execute."),
    "scorecards":    ("Architecture Scorecards",              "Scoring templates for continuous architecture quality measurement."),
    "maturity":      ("Architecture Maturity Models",         "Capability scoring and maturity criteria for engineering advancement."),
    "playbooks":     ("Engineering Playbooks",                "Step-by-step playbooks for common architecture challenges."),
    "strategy":      ("Architecture Strategy",                "AI readiness, modernization roadmaps, and foundational strategy."),
    "roadmaps":      ("Architecture Roadmaps",                "Platform evolution and capability uplift roadmaps."),
    "templates":     ("Architecture Templates",               "The structured artefacts the team uses to record decisions, document designs for review, and rate services across dimensions — ADRs, review templates, and scorecards — as designed instruments whose fields, lifecycle, and calibration determine whether they accumulate as institutional memory or as ceremonial paperwork."),
}

NAV_LINKS = [
    ("Principles",    "principles/index.html"),
    ("Patterns",      "patterns/index.html"),
    ("System Design", "system-design/index.html"),
    ("Technology",    "technology/index.html"),
    ("Security",      "security/index.html"),
    ("AI-Native",     "ai/index.html"),
    ("Governance",    "governance/index.html"),
]

# Mermaid theme — Ascendion Engineering diagram standard.
# Aligns to site palette; produces clean, professional, finished output.
# Color tokens chosen to match shared.css --dg-* with stronger fills for legibility.
MERMAID_INIT = """{
  startOnLoad: true,
  theme: 'base',
  securityLevel: 'loose',
  flowchart: {
    useMaxWidth: true,
    htmlLabels: true,
    curve: 'basis',
    padding: 25,
    nodeSpacing: 40,
    rankSpacing: 50,
    diagramPadding: 16
  },
  themeVariables: {
    background:          '#FFFFFF',
    primaryColor:        '#DCEAFC',
    primaryTextColor:    '#1A2840',
    primaryBorderColor:  '#3D6395',
    lineColor:           '#5079A8',
    secondaryColor:      '#EAF1FB',
    tertiaryColor:       '#FBEDE0',
    edgeLabelBackground: '#FFFFFF',
    clusterBkg:          '#F8F8F6',
    clusterBorder:       '#A8C0DD',
    titleColor:          '#1A2840',
    fontFamily:          'IBM Plex Sans, system-ui, sans-serif',
    fontSize:            '13px',
    nodeBorder:          '#3D6395',
    mainBkg:             '#DCEAFC'
  }
}"""

# ─────────────────────────────────────────────────────────────────────────────
# ANIMATED SVG ILLUSTRATIONS
# Each section gets a unique concept-driven looping SVG.
# Used small (80×58) on landing cards and large (240×180) in section heroes.
# ─────────────────────────────────────────────────────────────────────────────
SVGS = {

"principles": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes needle{0%,100%{transform:rotate(-20deg)}50%{transform:rotate(20deg)}}
.nd{transform-origin:60px 46px;animation:needle 3.5s ease-in-out infinite}
</style>
<circle cx="60" cy="46" r="32" stroke="#C8C4BC" stroke-width="1"/>
<circle cx="60" cy="46" r="3.5" fill="#C96330"/>
<text x="60" y="21" text-anchor="middle" font-size="8" fill="#AAAAAA" font-family="IBM Plex Mono">N</text>
<text x="60" y="76" text-anchor="middle" font-size="8" fill="#CCCCCC" font-family="IBM Plex Mono">S</text>
<text x="26" y="49" text-anchor="middle" font-size="8" fill="#CCCCCC" font-family="IBM Plex Mono">W</text>
<text x="96" y="49" text-anchor="middle" font-size="8" fill="#CCCCCC" font-family="IBM Plex Mono">E</text>
<g class="nd">
  <line x1="60" y1="46" x2="60" y2="20" stroke="#C96330" stroke-width="2" stroke-linecap="round"/>
  <line x1="60" y1="46" x2="60" y2="66" stroke="#CCCCCC" stroke-width="1.2" stroke-linecap="round"/>
</g>
</svg>""",

"patterns": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes hp{0%,100%{opacity:0.2}33%{opacity:1}66%{opacity:0.4}}
.h1{animation:hp 2.4s 0s ease-in-out infinite}
.h2{animation:hp 2.4s 0.8s ease-in-out infinite}
.h3{animation:hp 2.4s 1.6s ease-in-out infinite}
.h4{animation:hp 2.4s 1.2s ease-in-out infinite}
</style>
<polygon class="h1" points="30,18 44,18 51,30 44,42 30,42 23,30" stroke="#C96330" stroke-width="1.5" fill="none"/>
<polygon class="h2" points="54,18 68,18 75,30 68,42 54,42 47,30" stroke="#C96330" stroke-width="1.5" fill="none"/>
<polygon class="h3" points="30,46 44,46 51,58 44,70 30,70 23,58" stroke="#C96330" stroke-width="1.5" fill="none"/>
<polygon class="h4" points="54,46 68,46 75,58 68,70 54,70 47,58" stroke="#DDDDDD" stroke-width="1" fill="none"/>
<line x1="51" y1="30" x2="47" y2="30" stroke="#AAAAAA" stroke-width="0.8"/>
<line x1="37" y1="42" x2="37" y2="46" stroke="#AAAAAA" stroke-width="0.8"/>
<line x1="61" y1="42" x2="61" y2="46" stroke="#AAAAAA" stroke-width="0.8"/>
</svg>""",

"anti-patterns": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes warn{0%,100%{opacity:0.3}50%{opacity:1}}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-3px)}75%{transform:translateX(3px)}}
.warn{animation:warn 2s ease-in-out infinite}
.icon{animation:shake 2s ease-in-out infinite}
</style>
<circle cx="60" cy="45" r="32" stroke="#CCCCCC" stroke-width="1.2" fill="none"/>
<g class="icon">
<line class="warn" x1="46" y1="30" x2="74" y2="60" stroke="#C96330" stroke-width="2.5" stroke-linecap="round"/>
<line class="warn" x1="74" y1="30" x2="46" y2="60" stroke="#C96330" stroke-width="2.5" stroke-linecap="round"/>
</g>
</svg>""",

"adrs": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes ln{from{stroke-dashoffset:36}to{stroke-dashoffset:0}}
@keyframes ck{from{stroke-dashoffset:18}to{stroke-dashoffset:0}}
@keyframes rep{0%,70%{opacity:1}80%,100%{opacity:0}}
.doc{animation:rep 4s ease-in-out infinite}
.l1{stroke-dasharray:36;stroke-dashoffset:36;animation:ln 0.5s 0.3s ease forwards}
.l2{stroke-dasharray:28;stroke-dashoffset:28;animation:ln 0.5s 0.9s ease forwards}
.l3{stroke-dasharray:22;stroke-dashoffset:22;animation:ln 0.5s 1.5s ease forwards}
.ck{stroke-dasharray:18;stroke-dashoffset:18;animation:ck 0.4s 2.2s ease forwards}
</style>
<g class="doc">
<rect x="28" y="12" width="64" height="66" rx="3" stroke="#CCCCCC" stroke-width="1.2" fill="none"/>
<line class="l1" x1="38" y1="26" x2="74" y2="26" stroke="#AAAAAA" stroke-width="1.5" stroke-linecap="round"/>
<line class="l2" x1="38" y1="36" x2="68" y2="36" stroke="#AAAAAA" stroke-width="1.5" stroke-linecap="round"/>
<line class="l3" x1="38" y1="46" x2="70" y2="46" stroke="#AAAAAA" stroke-width="1.5" stroke-linecap="round"/>
<polyline class="ck" points="40,62 48,70 72,56" stroke="#C96330" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</g>
</svg>""",

"views": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes v1{0%,100%{opacity:1}50%{opacity:0.25}}
@keyframes v2{0%,33%{opacity:0.25}66%{opacity:1}100%{opacity:0.25}}
@keyframes v3{0%,66%{opacity:0.25}100%{opacity:1}50%{opacity:0.5}}
.v1{animation:v1 3s ease-in-out infinite}
.v2{animation:v2 3s ease-in-out infinite}
.v3{animation:v3 3s ease-in-out infinite}
</style>
<rect class="v1" x="14" y="14" width="52" height="38" rx="3" stroke="#C96330" stroke-width="1.8" fill="none"/>
<rect class="v2" x="28" y="26" width="52" height="38" rx="3" stroke="#AAAAAA" stroke-width="1.4" fill="none"/>
<rect class="v3" x="42" y="38" width="52" height="38" rx="3" stroke="#CCCCCC" stroke-width="1" fill="none"/>
</svg>""",

"design": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes grid{0%,100%{opacity:0.15}50%{opacity:0.5}}
@keyframes line1{from{stroke-dashoffset:90}to{stroke-dashoffset:0}}
@keyframes rep{0%,75%{opacity:1}85%,100%{opacity:0}}
.g{animation:grid 2.5s ease-in-out infinite}
.rep{animation:rep 4s linear infinite}
.ln1{stroke-dasharray:90;stroke-dashoffset:90;animation:line1 1.2s 0.4s ease forwards}
</style>
<g class="g">
<line x1="30" y1="10" x2="30" y2="80" stroke="#DDDDDD" stroke-width="0.7"/>
<line x1="60" y1="10" x2="60" y2="80" stroke="#DDDDDD" stroke-width="0.7"/>
<line x1="90" y1="10" x2="90" y2="80" stroke="#DDDDDD" stroke-width="0.7"/>
<line x1="10" y1="25" x2="110" y2="25" stroke="#DDDDDD" stroke-width="0.7"/>
<line x1="10" y1="45" x2="110" y2="45" stroke="#DDDDDD" stroke-width="0.7"/>
<line x1="10" y1="65" x2="110" y2="65" stroke="#DDDDDD" stroke-width="0.7"/>
</g>
<g class="rep">
<polyline class="ln1" points="30,65 30,25 90,25 90,65 30,65" stroke="#C96330" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</g>
</svg>""",

"system-design": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes edge{from{stroke-dashoffset:50}to{stroke-dashoffset:0}}
@keyframes pulse{0%,100%{r:5}50%{r:7}}
@keyframes rep{0%,70%{opacity:1}80%,100%{opacity:0}}
.rep{animation:rep 4s ease-in-out infinite}
.e1{stroke-dasharray:50;stroke-dashoffset:50;animation:edge 0.7s 0.2s ease forwards}
.e2{stroke-dasharray:50;stroke-dashoffset:50;animation:edge 0.7s 0.7s ease forwards}
.e3{stroke-dasharray:50;stroke-dashoffset:50;animation:edge 0.7s 1.2s ease forwards}
.e4{stroke-dasharray:50;stroke-dashoffset:50;animation:edge 0.7s 1.7s ease forwards}
.n1{animation:pulse 2s 0.2s ease-in-out infinite}
.n2{animation:pulse 2s 0.7s ease-in-out infinite}
.n3{animation:pulse 2s 1.2s ease-in-out infinite}
.n4{animation:pulse 2s 0s ease-in-out infinite}
</style>
<g class="rep">
<line class="e1" x1="30" y1="35" x2="60" y2="18" stroke="#AAAAAA" stroke-width="1.2"/>
<line class="e2" x1="60" y1="18" x2="90" y2="35" stroke="#AAAAAA" stroke-width="1.2"/>
<line class="e3" x1="30" y1="35" x2="60" y2="72" stroke="#AAAAAA" stroke-width="1.2"/>
<line class="e4" x1="90" y1="35" x2="60" y2="72" stroke="#AAAAAA" stroke-width="1.2"/>
</g>
<circle class="n4" cx="60" cy="18" r="5" fill="#C96330"/>
<circle class="n1" cx="30" cy="35" r="5" fill="#C96330"/>
<circle class="n2" cx="90" cy="35" r="5" fill="#C96330"/>
<circle class="n3" cx="60" cy="72" r="5" fill="#C96330"/>
</svg>""",

"ddd": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes bc{0%,100%{stroke-dashoffset:160}50%{stroke-dashoffset:0}}
.bc1{stroke-dasharray:160;animation:bc 3.5s ease-in-out infinite}
.bc2{stroke-dasharray:160;animation:bc 3.5s 1.75s ease-in-out infinite}
</style>
<rect class="bc1" x="8" y="16" width="54" height="38" rx="4" stroke="#C96330" stroke-width="1.8" fill="none"/>
<text x="35" y="38" text-anchor="middle" font-size="9" fill="#AAAAAA" font-family="IBM Plex Mono">Domain A</text>
<rect class="bc2" x="58" y="36" width="54" height="38" rx="4" stroke="#AAAAAA" stroke-width="1.4" fill="none"/>
<text x="85" y="58" text-anchor="middle" font-size="9" fill="#BBBBBB" font-family="IBM Plex Mono">Domain B</text>
<line x1="62" y1="37" x2="62" y2="54" stroke="#C96330" stroke-width="1" stroke-dasharray="3,3"/>
</svg>""",

"frameworks": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes ring{0%,100%{opacity:0.2}50%{opacity:1}}
.r1{animation:ring 2.4s 0s ease-in-out infinite}
.r2{animation:ring 2.4s 0.6s ease-in-out infinite}
.r3{animation:ring 2.4s 1.2s ease-in-out infinite}
.r4{animation:ring 2.4s 1.8s ease-in-out infinite}
</style>
<rect class="r1" x="6" y="6" width="108" height="78" rx="4" stroke="#CCCCCC" stroke-width="1" fill="none"/>
<rect class="r2" x="18" y="16" width="84" height="58" rx="4" stroke="#C96330" stroke-width="1.4" fill="none"/>
<rect class="r3" x="32" y="26" width="56" height="38" rx="4" stroke="#AAAAAA" stroke-width="1.2" fill="none"/>
<rect class="r4" x="46" y="36" width="28" height="18" rx="3" stroke="#C96330" stroke-width="1.5" fill="none"/>
</svg>""",

"tech": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes rise{from{transform:scaleY(0);opacity:0}to{transform:scaleY(1);opacity:1}}
@keyframes rep{0%,70%{opacity:1}80%,100%{opacity:0}}
.rep{animation:rep 4s ease-in-out infinite}
.s1{transform-origin:60px 72px;animation:rise 0.4s 0.2s ease forwards}
.s2{transform-origin:60px 58px;animation:rise 0.4s 0.6s ease forwards}
.s3{transform-origin:60px 44px;animation:rise 0.4s 1.0s ease forwards}
.s4{transform-origin:60px 30px;animation:rise 0.4s 1.4s ease forwards}
</style>
<g class="rep">
<rect class="s1" x="20" y="62" width="80" height="14" rx="3" stroke="#CCCCCC" stroke-width="1.2" fill="none"/>
<rect class="s2" x="28" y="48" width="64" height="14" rx="3" stroke="#AAAAAA" stroke-width="1.2" fill="none"/>
<rect class="s3" x="36" y="34" width="48" height="14" rx="3" stroke="#C96330" stroke-width="1.5" fill="none"/>
<rect class="s4" x="44" y="20" width="32" height="14" rx="3" stroke="#C96330" stroke-width="1.8" fill="none"/>
</g>
</svg>""",

"infra": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes blink{0%,90%,100%{opacity:1}95%{opacity:0.1}}
.b1{animation:blink 2s 0s ease-in-out infinite}
.b2{animation:blink 2s 0.5s ease-in-out infinite}
.b3{animation:blink 2s 1s ease-in-out infinite}
</style>
<rect x="14" y="14" width="92" height="18" rx="3" stroke="#CCCCCC" stroke-width="1.2" fill="none"/>
<rect x="14" y="36" width="92" height="18" rx="3" stroke="#CCCCCC" stroke-width="1.2" fill="none"/>
<rect x="14" y="58" width="92" height="18" rx="3" stroke="#AAAAAA" stroke-width="1" fill="none"/>
<circle class="b1" cx="96" cy="23" r="4" fill="#C96330"/>
<circle class="b2" cx="96" cy="45" r="4" fill="#C96330"/>
<circle class="b3" cx="96" cy="67" r="3.5" fill="#AAAAAA"/>
<line x1="24" y1="23" x2="82" y2="23" stroke="#DDDDDD" stroke-width="1"/>
<line x1="24" y1="45" x2="76" y2="45" stroke="#DDDDDD" stroke-width="1"/>
</svg>""",

"cloud": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes float{0%{transform:translateY(0);opacity:0}50%{opacity:0.7}100%{transform:translateY(-20px);opacity:0}}
.d1{animation:float 2.4s 0s ease-in-out infinite}
.d2{animation:float 2.4s 0.6s ease-in-out infinite}
.d3{animation:float 2.4s 1.2s ease-in-out infinite}
.d4{animation:float 2.4s 1.8s ease-in-out infinite}
</style>
<circle class="d1" cx="32" cy="62" r="3.5" fill="#CCCCCC"/>
<circle class="d2" cx="52" cy="68" r="3.5" fill="#CCCCCC"/>
<circle class="d3" cx="72" cy="62" r="3.5" fill="#CCCCCC"/>
<circle class="d4" cx="90" cy="66" r="3" fill="#AAAAAA"/>
<ellipse cx="50" cy="38" rx="26" ry="14" stroke="#C96330" stroke-width="1.8" fill="none"/>
<ellipse cx="76" cy="43" rx="18" ry="12" stroke="#AAAAAA" stroke-width="1.4" fill="none"/>
<ellipse cx="30" cy="44" rx="16" ry="11" stroke="#BBBBBB" stroke-width="1.2" fill="none"/>
</svg>""",

"ai": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes act{0%,100%{fill:#CCCCCC;r:3.5}50%{fill:#C96330;r:5.5}}
@keyframes pulse{0%,100%{stroke-opacity:0.2}50%{stroke-opacity:0.85}}
.n1{animation:act 1.8s 0s ease-in-out infinite}
.n2{animation:act 1.8s 0.4s ease-in-out infinite}
.n3{animation:act 1.8s 0.8s ease-in-out infinite}
.n4{animation:act 1.8s 1.2s ease-in-out infinite}
.n5{animation:act 1.8s 0.2s ease-in-out infinite}
.e{animation:pulse 1.8s ease-in-out infinite}
</style>
<line class="e" x1="22" y1="28" x2="52" y2="18" stroke="#AAAAAA" stroke-width="1"/>
<line class="e" x1="22" y1="28" x2="52" y2="42" stroke="#AAAAAA" stroke-width="1"/>
<line class="e" x1="22" y1="62" x2="52" y2="18" stroke="#AAAAAA" stroke-width="1"/>
<line class="e" x1="22" y1="62" x2="52" y2="42" stroke="#AAAAAA" stroke-width="1"/>
<line class="e" x1="22" y1="62" x2="52" y2="66" stroke="#AAAAAA" stroke-width="1"/>
<line class="e" x1="52" y1="18" x2="98" y2="30" stroke="#AAAAAA" stroke-width="1"/>
<line class="e" x1="52" y1="42" x2="98" y2="30" stroke="#AAAAAA" stroke-width="1"/>
<line class="e" x1="52" y1="42" x2="98" y2="60" stroke="#AAAAAA" stroke-width="1"/>
<line class="e" x1="52" y1="66" x2="98" y2="60" stroke="#AAAAAA" stroke-width="1"/>
<circle class="n1" cx="22" cy="28" r="3.5"/>
<circle class="n2" cx="22" cy="62" r="3.5"/>
<circle class="n3" cx="52" cy="18" r="3.5"/>
<circle class="n4" cx="52" cy="42" r="3.5"/>
<circle class="n5" cx="52" cy="66" r="3.5"/>
<circle cx="98" cy="30" r="6" fill="#C96330"/>
<circle cx="98" cy="60" r="6" fill="#C96330"/>
</svg>""",

"security": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes pulse{0%,100%{stroke-width:1.5}50%{stroke-width:3}}
@keyframes lock{0%,40%{transform:translateY(5px)}60%,100%{transform:translateY(0)}}
.sh{animation:pulse 2.5s ease-in-out infinite}
.lk{animation:lock 2s ease-in-out infinite;transform-origin:60px 48px}
</style>
<path class="sh" d="M60 8 L90 18 L90 46 Q90 72 60 82 Q30 72 30 46 L30 18 Z" stroke="#C96330" stroke-width="1.8" fill="none"/>
<g class="lk">
<rect x="48" y="44" width="24" height="18" rx="3" stroke="#CCCCCC" stroke-width="1.8" fill="none"/>
<path d="M52 44 Q52 34 60 34 Q68 34 68 44" stroke="#CCCCCC" stroke-width="1.8" fill="none"/>
<circle cx="60" cy="53" r="2.5" fill="#C96330"/>
</g>
</svg>""",

"compliance": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes ck{from{stroke-dashoffset:22}to{stroke-dashoffset:0}}
@keyframes rep{0%,65%{opacity:1}75%,100%{opacity:0}}
.rep{animation:rep 4.5s ease-in-out infinite}
.c1{stroke-dasharray:22;stroke-dashoffset:22;animation:ck 0.35s 0.2s ease forwards}
.c2{stroke-dasharray:22;stroke-dashoffset:22;animation:ck 0.35s 1s ease forwards}
.c3{stroke-dasharray:22;stroke-dashoffset:22;animation:ck 0.35s 1.8s ease forwards}
</style>
<g class="rep">
<rect x="14" y="14" width="16" height="16" rx="2" stroke="#CCCCCC" stroke-width="1.2" fill="none"/>
<rect x="14" y="37" width="16" height="16" rx="2" stroke="#CCCCCC" stroke-width="1.2" fill="none"/>
<rect x="14" y="60" width="16" height="16" rx="2" stroke="#CCCCCC" stroke-width="1.2" fill="none"/>
<line x1="38" y1="22" x2="106" y2="22" stroke="#DDDDDD" stroke-width="1"/>
<line x1="38" y1="45" x2="96" y2="45" stroke="#DDDDDD" stroke-width="1"/>
<line x1="38" y1="68" x2="100" y2="68" stroke="#DDDDDD" stroke-width="1"/>
<polyline class="c1" points="16,22 20,26 28,16" stroke="#C96330" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<polyline class="c2" points="16,45 20,49 28,39" stroke="#C96330" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<polyline class="c3" points="16,68 20,72 28,62" stroke="#C96330" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</g>
</svg>""",

"governance": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes bal{0%,100%{transform:rotate(-7deg)}50%{transform:rotate(7deg)}}
.arm{animation:bal 3s ease-in-out infinite;transform-origin:60px 30px}
</style>
<line x1="60" y1="14" x2="60" y2="74" stroke="#CCCCCC" stroke-width="1.8" stroke-linecap="round"/>
<g class="arm">
<line x1="28" y1="30" x2="92" y2="30" stroke="#C96330" stroke-width="2" stroke-linecap="round"/>
<line x1="28" y1="30" x2="22" y2="54" stroke="#AAAAAA" stroke-width="1.2"/>
<line x1="92" y1="30" x2="98" y2="54" stroke="#AAAAAA" stroke-width="1.2"/>
<ellipse cx="22" cy="56" rx="8" ry="5" stroke="#AAAAAA" stroke-width="1.2" fill="none"/>
<ellipse cx="98" cy="56" rx="8" ry="5" stroke="#AAAAAA" stroke-width="1.2" fill="none"/>
</g>
<line x1="52" y1="74" x2="68" y2="74" stroke="#CCCCCC" stroke-width="1.8" stroke-linecap="round"/>
</svg>""",

"nfr": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes needle{0%{transform:rotate(-65deg)}100%{transform:rotate(65deg)}}
.ndl{animation:needle 3s ease-in-out infinite alternate;transform-origin:60px 60px}
</style>
<path d="M20 60 A40 40 0 0 1 100 60" stroke="#DDDDDD" stroke-width="2" fill="none"/>
<path d="M22 60 A38 38 0 0 1 50 28" stroke="#C96330" stroke-width="4" fill="none" stroke-linecap="round"/>
<g class="ndl">
<line x1="60" y1="60" x2="60" y2="28" stroke="#C96330" stroke-width="2" stroke-linecap="round"/>
<circle cx="60" cy="60" r="4" fill="#C96330"/>
</g>
<text x="22" y="76" font-size="9" fill="#AAAAAA" font-family="IBM Plex Mono">slow</text>
<text x="86" y="76" font-size="9" fill="#AAAAAA" font-family="IBM Plex Mono">fast</text>
</svg>""",

"data": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes flow{from{stroke-dashoffset:60}to{stroke-dashoffset:0}}
.f1{stroke-dasharray:10,5;animation:flow 1.6s 0s linear infinite}
.f2{stroke-dasharray:10,5;animation:flow 1.6s 0.5s linear infinite}
.f3{stroke-dasharray:10,5;animation:flow 1.6s 1s linear infinite}
</style>
<rect x="8" y="14" width="28" height="62" rx="4" stroke="#CCCCCC" stroke-width="1.2" fill="none"/>
<ellipse cx="22" cy="20" rx="14" ry="6" stroke="#CCCCCC" stroke-width="1.2" fill="none"/>
<line class="f1" x1="36" y1="32" x2="82" y2="32" stroke="#C96330" stroke-width="2" stroke-linecap="round"/>
<line class="f2" x1="36" y1="45" x2="82" y2="45" stroke="#C96330" stroke-width="2" stroke-linecap="round"/>
<line class="f3" x1="36" y1="58" x2="82" y2="58" stroke="#AAAAAA" stroke-width="1.6" stroke-linecap="round"/>
<rect x="82" y="18" width="28" height="54" rx="4" stroke="#AAAAAA" stroke-width="1.2" fill="none"/>
</svg>""",

"integration": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes pulse{0%,100%{opacity:0.2}50%{opacity:1}}
.p1{animation:pulse 2s 0s ease-in-out infinite}
.p2{animation:pulse 2s 0.5s ease-in-out infinite}
.p3{animation:pulse 2s 1s ease-in-out infinite}
</style>
<circle cx="28" cy="45" r="22" stroke="#CCCCCC" stroke-width="1.4" fill="none"/>
<circle cx="92" cy="45" r="22" stroke="#C96330" stroke-width="1.4" fill="none"/>
<line class="p1" x1="50" y1="30" x2="70" y2="30" stroke="#C96330" stroke-width="2" stroke-linecap="round"/>
<line class="p2" x1="50" y1="45" x2="70" y2="45" stroke="#C96330" stroke-width="2" stroke-linecap="round"/>
<line class="p3" x1="50" y1="60" x2="70" y2="60" stroke="#AAAAAA" stroke-width="1.5" stroke-linecap="round"/>
</svg>""",

"observability": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes ecg{from{stroke-dashoffset:180}to{stroke-dashoffset:0}}
@keyframes rep{0%,70%{opacity:1}80%,100%{opacity:0}}
.ecg{stroke-dasharray:180;stroke-dashoffset:180;animation:ecg 2.2s 0.2s ease forwards}
.rep{animation:rep 3.5s ease-in-out infinite}
</style>
<line x1="10" y1="56" x2="110" y2="56" stroke="#EEEEEA" stroke-width="1"/>
<g class="rep">
<polyline class="ecg" points="10,56 26,56 32,28 40,72 48,40 56,56 78,56 84,14 92,78 100,56 110,56"
  stroke="#C96330" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</g>
</svg>""",

"tools": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
@keyframes spinR{from{transform:rotate(0deg)}to{transform:rotate(-360deg)}}
.g1{animation:spin 6s linear infinite;transform-origin:40px 45px}
.g2{animation:spinR 4s linear infinite;transform-origin:80px 45px}
</style>
<g class="g1">
<circle cx="40" cy="45" r="16" stroke="#C96330" stroke-width="1.8" fill="none"/>
<circle cx="40" cy="45" r="5" fill="#C96330"/>
<line x1="40" y1="28" x2="40" y2="25" stroke="#C96330" stroke-width="4" stroke-linecap="round"/>
<line x1="40" y1="62" x2="40" y2="65" stroke="#C96330" stroke-width="4" stroke-linecap="round"/>
<line x1="23" y1="45" x2="20" y2="45" stroke="#C96330" stroke-width="4" stroke-linecap="round"/>
<line x1="57" y1="45" x2="60" y2="45" stroke="#C96330" stroke-width="4" stroke-linecap="round"/>
</g>
<g class="g2">
<circle cx="80" cy="45" r="12" stroke="#AAAAAA" stroke-width="1.4" fill="none"/>
<circle cx="80" cy="45" r="4" fill="#AAAAAA"/>
<line x1="80" y1="32" x2="80" y2="30" stroke="#AAAAAA" stroke-width="3" stroke-linecap="round"/>
<line x1="80" y1="58" x2="80" y2="60" stroke="#AAAAAA" stroke-width="3" stroke-linecap="round"/>
<line x1="67" y1="45" x2="65" y2="45" stroke="#AAAAAA" stroke-width="3" stroke-linecap="round"/>
<line x1="93" y1="45" x2="95" y2="45" stroke="#AAAAAA" stroke-width="3" stroke-linecap="round"/>
</g>
</svg>""",

"checklists": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes ck{from{stroke-dashoffset:22}to{stroke-dashoffset:0}}
@keyframes rep{0%,70%{opacity:1}80%,100%{opacity:0}}
.rep{animation:rep 5s ease-in-out infinite}
.c1{stroke-dasharray:22;stroke-dashoffset:22;animation:ck 0.3s 0.2s ease forwards}
.c2{stroke-dasharray:22;stroke-dashoffset:22;animation:ck 0.3s 0.9s ease forwards}
.c3{stroke-dasharray:22;stroke-dashoffset:22;animation:ck 0.3s 1.6s ease forwards}
.c4{stroke-dasharray:22;stroke-dashoffset:22;animation:ck 0.3s 2.3s ease forwards}
</style>
<g class="rep">
<rect x="10" y="12" width="16" height="16" rx="2" stroke="#CCCCCC" stroke-width="1.2" fill="none"/>
<rect x="10" y="34" width="16" height="16" rx="2" stroke="#CCCCCC" stroke-width="1.2" fill="none"/>
<rect x="10" y="56" width="16" height="16" rx="2" stroke="#CCCCCC" stroke-width="1.2" fill="none"/>
<rect x="10" y="74" width="16" height="10" rx="2" stroke="#DDDDDD" stroke-width="0.9" fill="none"/>
<line x1="34" y1="20" x2="108" y2="20" stroke="#DDDDDD" stroke-width="1"/>
<line x1="34" y1="42" x2="98" y2="42" stroke="#DDDDDD" stroke-width="1"/>
<line x1="34" y1="64" x2="102" y2="64" stroke="#DDDDDD" stroke-width="1"/>
<line x1="34" y1="79" x2="82" y2="79" stroke="#EEEEEE" stroke-width="0.8"/>
<polyline class="c1" points="12,20 16,24 24,14" stroke="#C96330" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<polyline class="c2" points="12,42 16,46 24,36" stroke="#C96330" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<polyline class="c3" points="12,64 16,68 24,58" stroke="#C96330" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<polyline class="c4" points="12,79 15,82 22,74" stroke="#AAAAAA" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</g>
</svg>""",

"runbooks": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes step{0%,100%{transform:translateX(0);opacity:0.3}50%{transform:translateX(6px);opacity:1}}
.s1{animation:step 2.4s 0s ease-in-out infinite}
.s2{animation:step 2.4s 0.6s ease-in-out infinite}
.s3{animation:step 2.4s 1.2s ease-in-out infinite}
.s4{animation:step 2.4s 1.8s ease-in-out infinite}
</style>
<polygon points="10,32 10,58 32,45" stroke="#C96330" stroke-width="1.8" fill="none"/>
<g class="s1"><rect x="40" y="26" width="72" height="12" rx="3" stroke="#CCCCCC" stroke-width="1.1" fill="none"/></g>
<g class="s2"><rect x="40" y="41" width="60" height="12" rx="3" stroke="#AAAAAA" stroke-width="1.1" fill="none"/></g>
<g class="s3"><rect x="40" y="56" width="68" height="12" rx="3" stroke="#CCCCCC" stroke-width="1.1" fill="none"/></g>
<g class="s4"><rect x="40" y="71" width="52" height="10" rx="3" stroke="#BBBBBB" stroke-width="0.9" fill="none"/></g>
</svg>""",

"scorecards": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes bar{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes rep{0%,70%{opacity:1}80%,100%{opacity:0}}
.rep{animation:rep 4s ease-in-out infinite}
.b1{transform-origin:28px 72px;animation:bar 0.4s 0.2s ease forwards}
.b2{transform-origin:52px 72px;animation:bar 0.4s 0.5s ease forwards}
.b3{transform-origin:76px 72px;animation:bar 0.4s 0.8s ease forwards}
.b4{transform-origin:100px 72px;animation:bar 0.4s 1.1s ease forwards}
</style>
<g class="rep">
<rect class="b1" x="18" y="44" width="20" height="28" rx="2" stroke="#AAAAAA" stroke-width="1.2" fill="none"/>
<rect class="b2" x="42" y="30" width="20" height="42" rx="2" stroke="#C96330" stroke-width="1.5" fill="none"/>
<rect class="b3" x="66" y="36" width="20" height="36" rx="2" stroke="#C96330" stroke-width="1.5" fill="none"/>
<rect class="b4" x="90" y="50" width="20" height="22" rx="2" stroke="#AAAAAA" stroke-width="1.2" fill="none"/>
<line x1="10" y1="72" x2="114" y2="72" stroke="#DDDDDD" stroke-width="1"/>
</g>
</svg>""",

"maturity": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes climb{0%{cx:14;cy:72}20%{cx:34;cy:58}40%{cx:54;cy:44}60%{cx:74;cy:30}80%,100%{cx:94;cy:18}}
.dot{animation:climb 3.5s ease-in-out infinite}
</style>
<polyline points="14,74 34,74 34,60 54,60 54,46 74,46 74,32 94,32 94,18" stroke="#CCCCCC" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
<circle class="dot" cx="14" cy="72" r="5" fill="#C96330"/>
</svg>""",

"playbooks": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes expand{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}
.ring1{animation:expand 2.4s 0s ease-in-out infinite;transform-origin:60px 45px}
.ring2{animation:expand 2.4s 0.8s ease-in-out infinite;transform-origin:60px 45px}
.ring3{animation:expand 2.4s 1.6s ease-in-out infinite;transform-origin:60px 45px}
</style>
<circle class="ring3" cx="60" cy="45" r="38" stroke="#E0DDDA" stroke-width="1" fill="none"/>
<circle class="ring2" cx="60" cy="45" r="26" stroke="#CCCCCC" stroke-width="1.2" fill="none"/>
<circle class="ring1" cx="60" cy="45" r="14" stroke="#C96330" stroke-width="1.8" fill="none"/>
<circle cx="60" cy="45" r="5" fill="#C96330"/>
</svg>""",

"strategy": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes scan{0%,100%{transform:rotate(-45deg)}50%{transform:rotate(45deg)}}
.scope{animation:scan 4s ease-in-out infinite;transform-origin:60px 45px}
</style>
<circle cx="60" cy="45" r="36" stroke="#DDDDDD" stroke-width="1" fill="none"/>
<circle cx="60" cy="45" r="24" stroke="#CCCCCC" stroke-width="1" fill="none"/>
<circle cx="60" cy="45" r="5" fill="#C96330"/>
<g class="scope">
  <line x1="60" y1="45" x2="60" y2="12" stroke="#C96330" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="4,4"/>
</g>
<line x1="10" y1="45" x2="110" y2="45" stroke="#EEEEEA" stroke-width="0.8"/>
<line x1="60" y1="5" x2="60" y2="85" stroke="#EEEEEA" stroke-width="0.8"/>
</svg>""",

"roadmaps": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes travel{0%{cx:10;opacity:0}20%{opacity:1}80%{opacity:1}100%{cx:108;opacity:0}}
.car{animation:travel 3s ease-in-out infinite}
</style>
<line x1="10" y1="54" x2="110" y2="54" stroke="#DDDDDD" stroke-width="1.5"/>
<circle cx="28" cy="54" r="6" stroke="#AAAAAA" stroke-width="1.2" fill="none"/>
<circle cx="60" cy="54" r="6" stroke="#AAAAAA" stroke-width="1.2" fill="none"/>
<circle cx="92" cy="54" r="6" stroke="#C96330" stroke-width="1.5" fill="none"/>
<line x1="28" y1="48" x2="28" y2="34" stroke="#AAAAAA" stroke-width="1" stroke-dasharray="2,3"/>
<line x1="60" y1="48" x2="60" y2="36" stroke="#AAAAAA" stroke-width="1" stroke-dasharray="2,3"/>
<line x1="92" y1="48" x2="92" y2="22" stroke="#C96330" stroke-width="1.2" stroke-dasharray="2,3"/>
<text x="20" y="30" font-size="9" fill="#AAAAAA" font-family="IBM Plex Mono">v1</text>
<text x="52" y="32" font-size="9" fill="#AAAAAA" font-family="IBM Plex Mono">v2</text>
<text x="84" y="18" font-size="9" fill="#C96330" font-family="IBM Plex Mono">v3</text>
<circle class="car" cx="10" cy="54" r="4" fill="#C96330"/>
</svg>""",

"templates": """<svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes appear{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
@keyframes rep{0%,70%{opacity:1}80%,100%{opacity:0}}
.rep{animation:rep 5s ease-in-out infinite}
.t1{animation:appear 0.35s 0.2s ease both}
.t2{animation:appear 0.35s 0.7s ease both}
.t3{animation:appear 0.35s 1.2s ease both}
.t4{animation:appear 0.35s 1.7s ease both}
.t5{animation:appear 0.35s 2.2s ease both}
</style>
<rect x="16" y="6" width="88" height="78" rx="3" stroke="#CCCCCC" stroke-width="1.2" fill="none"/>
<g class="rep">
<rect class="t1" x="26" y="16" width="68" height="10" rx="2" stroke="#C96330" stroke-width="1.5" fill="none"/>
<line class="t2" x1="26" y1="34" x2="94" y2="34" stroke="#CCCCCC" stroke-width="1.5" stroke-linecap="round"/>
<line class="t3" x1="26" y1="46" x2="80" y2="46" stroke="#CCCCCC" stroke-width="1.5" stroke-linecap="round"/>
<line class="t4" x1="26" y1="58" x2="86" y2="58" stroke="#BBBBBB" stroke-width="1.2" stroke-linecap="round"/>
<line class="t5" x1="26" y1="70" x2="68" y2="70" stroke="#BBBBBB" stroke-width="1.2" stroke-linecap="round"/>
</g>
</svg>""",
}

# ─────────────────────────────────────────────────────────────────────────────
# MARKDOWN HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def md_to_html(text):
    """Render markdown to HTML, stripping duplicated metadata that already
    appears in the article hero (title, description, Section/Subsection/
    Alignment chips). Keeps READMEs readable as standalone files while
    avoiding duplication on the rendered page."""
    lines = text.split("\n")
    out = []
    state = "before_h1"
    for line in lines:
        stripped = line.strip()
        if state == "before_h1":
            if line.startswith("# "):
                state = "after_h1_seek_desc"
            continue
        if state == "after_h1_seek_desc":
            # Skip blank lines, then capture the first non-blank/non-heading
            # paragraph as the "description" and strip it.
            if not stripped:
                continue
            if stripped.startswith(("#", ">")):
                state = "in_body"
                out.append(line)
                continue
            # This is the description paragraph — skip it.
            state = "after_desc_strip_meta"
            continue
        if state == "after_desc_strip_meta":
            # Skip blank lines, **Section:**, **Subsection:**, **Alignment:**,
            # and a single trailing --- separator.
            if not stripped:
                continue
            if (stripped.startswith("**Section:**") or
                stripped.startswith("**Subsection:**") or
                stripped.startswith("**Alignment:**")):
                continue
            if stripped == "---":
                state = "in_body"
                continue
            state = "in_body"
            out.append(line)
            continue
        # state == "in_body" — emit as-is
        out.append(line)
    body = "\n".join(out)
    if MD:
        html = markdown.markdown(body, extensions=[
            TableExtension(), FencedCodeExtension(), "nl2br", "sane_lists"])
    else:
        result = []
        for p in re.split(r"\n{2,}", body):
            p = p.strip()
            if not p: continue
            if p.startswith("## "): result.append(f"<h2>{p[3:]}</h2>")
            elif p.startswith("### "): result.append(f"<h3>{p[4:]}</h3>")
            elif p.startswith("#### "): result.append(f"<h4>{p[5:]}</h4>")
            elif p.startswith("> "): result.append(f"<blockquote><p>{p[2:]}</p></blockquote>")
            else:
                p = re.sub(r"`([^`]+)`", r"<code>\1</code>", p)
                p = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", p)
                result.append(f"<p>{p}</p>")
        html = "\n".join(result)
    return enhance_html(html)


# ─────────────────────────────────────────────────────────────────────────────
# HTML POST-PROCESSING — adds semantic wrappers for richer styling
#
#   1. <h3>1. Title</h3> ... <h3>2. ...</h3>      → wraps each block as principle-card
#   2. <h3>⚠️ Title</h3> ...                      → wraps each block as pitfall-card
#   3. Adoption checklist <table>                 → adds class="checklist"
#   4. External links (http/https)                → adds target="_blank" rel=...
# ─────────────────────────────────────────────────────────────────────────────

PRINCIPLE_HEADING_RE = re.compile(
    r'<h3>\s*(\d+)\.\s+(.+?)</h3>', re.IGNORECASE)
PITFALL_HEADING_RE = re.compile(
    r'<h3>\s*⚠️\s+(.+?)</h3>', re.IGNORECASE)


# Inline SVG used to mark pitfall cards (replacing the ⚠️ emoji).
# Drawn as a no-entry / prohibition glyph in red — communicates "do not do
# this" without an emoji that might render inconsistently across systems.
PITFALL_ICON_SVG = (
    '<svg class="pitfall-icon" viewBox="0 0 20 20" '
    'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    '<circle cx="10" cy="10" r="8" fill="none" '
    'stroke="#C62828" stroke-width="1.8"/>'
    '<line x1="4.8" y1="10" x2="15.2" y2="10" '
    'stroke="#C62828" stroke-width="1.8" stroke-linecap="round"/>'
    '</svg>'
)


def enhance_html(html):
    """Apply post-processing transforms that add UX-system wrappers."""

    # 1. Principle cards — flip-cards. Front: heading + first paragraph.
    #    Back: everything else (architectural implications, quick test, reference).
    html = _wrap_h3_blocks(
        html,
        match_re=PRINCIPLE_HEADING_RE,
        wrapper_classes='flip-card principle-card',
        # Drop the number badge — keep number inline in the heading text.
        heading_transform=lambda m: f'<h3>{m.group(1)}. {m.group(2)}</h3>',
        flip=True,
    )

    # 2. Pitfall cards — flip-cards. Replace ⚠️ emoji with inline red SVG icon.
    #    Front: icon + heading + first paragraph.
    #    Back: "What to do instead" content.
    html = _wrap_h3_blocks(
        html,
        match_re=PITFALL_HEADING_RE,
        wrapper_classes='flip-card pitfall-card',
        heading_transform=lambda m: (
            f'<h3>{PITFALL_ICON_SVG}<span>{m.group(1)}</span></h3>'
        ),
        flip=True,
    )

    # 3. Adoption checklist
    #    If any cell contains the front/back separator '‖' (U+2016), transform
    #    the table into a vertical stack of flippable cards: front shows
    #    [number, criterion, checkbox], back shows the explanation.
    #    Otherwise keep as a styled table with class="checklist".
    html = _process_adoption_checklist(html)

    # 4. External links open in new tab with safe rel
    html = re.sub(
        r'<a href="(https?://[^"]+)"([^>]*)>',
        r'<a href="\1" target="_blank" rel="noopener noreferrer"\2>',
        html
    )

    # 5. "## Related" — turn the link-list paragraph into chip-styled list.
    #    Looks for <h2>Related[ Sections]</h2> followed by a <p> that contains
    #    only <a>...</a> | <a>...</a> | ... and rewrites to .related-chips.
    html = _stylize_related_links(html)

    return html


def _stylize_related_links(html):
    """Find a Related-section paragraph that's only made of links and
    pipe separators, and rewrite to use .related-chips chip styling."""
    pattern = re.compile(
        r'(<h2[^>]*>\s*Related(?:\s+Sections)?\s*</h2>)\s*'
        r'<p>(.*?)</p>',
        re.IGNORECASE | re.DOTALL,
    )

    def replace(m):
        heading = m.group(1)
        para = m.group(2)
        # The inner content should be a series of <a>...</a> separated by ' | '.
        # Extract anchors and re-emit as chips.
        anchors = re.findall(r'<a [^>]*>.*?</a>', para)
        if not anchors:
            return m.group(0)
        # Remove inner <code> wrapping if present so chip styling applies cleanly.
        chips = []
        for a in anchors:
            cleaned = re.sub(r'<code>(.*?)</code>', r'\1', a)
            # Add chip class to the anchor.
            cleaned = re.sub(
                r'<a ',
                '<a class="related-chip" ',
                cleaned, count=1
            )
            chips.append(cleaned)
        return heading + '\n<div class="related-chips-row">' + ''.join(chips) + '</div>'

    return pattern.sub(replace, html)


def _process_adoption_checklist(html):
    """Process the adoption-checklist table.

    Detect a table whose thead row contains a 'Criterion' column. If any cell
    contains the U+2016 double-vertical-bar separator '‖', transform the
    entire table into a vertical stack of flippable cards (front: number +
    criterion + checkbox; back: explanation). Otherwise keep the table as-is
    but add class='checklist' so it picks up table styling.
    """
    # Locate the first checklist table
    table_pattern = re.compile(
        r'<table>\s*<thead>\s*<tr>\s*<th>[^<]*</th>\s*<th>\s*Criterion[^<]*</th>'
        r'\s*<th>[^<]*</th>\s*</tr>\s*</thead>\s*<tbody>(.*?)</tbody>\s*</table>',
        re.DOTALL,
    )
    m = table_pattern.search(html)
    if not m:
        return html

    full_table = m.group(0)
    tbody = m.group(1)

    if "‖" in tbody:
        # Transform into checklist-cards
        row_pattern = re.compile(
            r'<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>',
            re.DOTALL,
        )
        cards = []
        for num, criterion, _status in row_pattern.findall(tbody):
            num = num.strip()
            criterion = criterion.strip()
            if "‖" in criterion:
                front_text, back_text = criterion.split("‖", 1)
                front_text = front_text.strip()
                back_text = back_text.strip()
            else:
                front_text = criterion
                back_text = ""
            cards.append(
                '<div class="check-card flip-card" tabindex="0" '
                'role="button" aria-pressed="false">\n'
                '  <div class="flip-card-inner">\n'
                '    <div class="flip-card-front">\n'
                '      <div class="flip-card-front-inner">\n'
                '        <div class="check-card-row">\n'
                f'          <span class="check-card-num">{num}</span>\n'
                f'          <span class="check-card-criterion">{front_text}</span>\n'
                '          <span class="check-card-checkbox" '
                'data-checked="false" '
                'aria-label="Mark complete">☐</span>\n'
                '        </div>\n'
                '        <div class="flip-card-hint" aria-hidden="true">'
                'Flip<span class="flip-arrow"> ↻</span></div>\n'
                '      </div>\n'
                '    </div>\n'
                '    <div class="flip-card-back">\n'
                '      <div class="flip-card-back-inner">\n'
                f'        <p class="check-card-explanation">{back_text}</p>\n'
                '        <div class="flip-card-hint" aria-hidden="true">'
                'Flip<span class="flip-arrow"> ↺</span></div>\n'
                '      </div>\n'
                '    </div>\n'
                '  </div>\n'
                '</div>'
            )
        replacement = (
            '<div class="checklist-cards">\n'
            + '\n'.join(cards)
            + '\n</div>'
        )
        return html.replace(full_table, replacement)

    # No separator: just style the existing table with class="checklist"
    styled_table = full_table.replace(
        '<table>', '<table class="checklist">', 1
    )
    return html.replace(full_table, styled_table)


def _wrap_h3_blocks(html, match_re, wrapper_classes, heading_transform, flip=False):
    """Wrap each <h3>...matched...</h3> through the next <h3>/<h2> in a div.

    If flip=True, the wrapper produces a 2-sided flip-card structure:
        front = heading + first <p>
        back  = everything else after that first <p>, plus a 'Flip back' hint
    """
    parts = re.split(r'(<h[23][^>]*>)', html)
    result = []
    i = 0
    while i < len(parts):
        chunk = parts[i]
        if i % 2 == 0:
            result.append(chunk)
            i += 1
            continue

        if i + 1 < len(parts):
            next_text = parts[i + 1]
            close_idx = next_text.find('</h3>')
            if chunk.startswith('<h3') and close_idx >= 0:
                heading_html = chunk + next_text[:close_idx + len('</h3>')]
                m = match_re.match(heading_html)
                if m:
                    rest = next_text[close_idx + len('</h3>'):]
                    j = i + 2
                    body_parts = [rest]
                    while j < len(parts):
                        if parts[j].startswith('<h3') or parts[j].startswith('<h2'):
                            break
                        body_parts.append(parts[j])
                        j += 1
                    body_html = ''.join(body_parts)
                    new_heading = heading_transform(m)

                    if flip:
                        front_para, remaining = _split_first_paragraph(body_html)
                        front_html = (
                            f'    <div class="flip-card-front">\n'
                            f'      <div class="flip-card-front-inner">\n'
                            f'        {new_heading}\n'
                            f'        {front_para}\n'
                            f'        <div class="flip-card-hint" aria-hidden="true">'
                            f'Flip<span class="flip-arrow"> ↻</span></div>\n'
                            f'      </div>\n'
                            f'    </div>\n'
                        )
                        back_html = (
                            f'    <div class="flip-card-back">\n'
                            f'      <div class="flip-card-back-inner">\n'
                            f'        {remaining}\n'
                            f'        <div class="flip-card-hint" aria-hidden="true">'
                            f'Flip<span class="flip-arrow"> ↺</span></div>\n'
                            f'      </div>\n'
                            f'    </div>\n'
                        )
                        wrapper = (
                            f'<div class="{wrapper_classes}" tabindex="0" '
                            f'role="button" aria-pressed="false" '
                            f'aria-label="Show details for: '
                            f'{_strip_tags(new_heading)}">\n'
                            f'  <div class="flip-card-inner">\n'
                            f'{front_html}{back_html}'
                            f'  </div>\n'
                            f'</div>\n'
                        )
                        result.append(wrapper)
                    else:
                        result.append(
                            f'<div class="{wrapper_classes}">{new_heading}{body_html}</div>'
                        )
                    i = j
                    continue
        result.append(chunk)
        i += 1
    return ''.join(result)


def _split_first_paragraph(html):
    """Return (first_p_tag, rest_of_html). If no <p> found, returns ('', html)."""
    m = re.search(r'<p[^>]*>.*?</p>', html, re.DOTALL)
    if not m:
        return ('', html)
    return (m.group(0), html[:m.start()] + html[m.end():])


def _strip_tags(html):
    """Remove HTML tags for use in plain-text contexts (e.g. aria-label)."""
    return re.sub(r'<[^>]+>', '', html).strip()


def extract_title_desc(text):
    title, desc = "", ""
    for line in text.split("\n"):
        if not title and line.startswith("# "):
            title = line[2:].strip()
        elif title and not desc and line.strip() and not line.startswith(("#", ">", "---")):
            desc = line.strip(); break
    return title or "Untitled", desc


def extract_tags(text):
    tags = []
    m = re.search(r"\*\*Alignment:\*\*\s*(.+)", text)
    if m:
        tags = [t.strip() for t in m.group(1).split("|") if t.strip()]
    # Section is shown as a chip linking to the parent section page.
    # Subsection is intentionally NOT extracted — it would link to the
    # current page, which is useless to the reader.
    m_sec = re.search(r"\*\*Section:\*\*\s*`([^`]+)`", text)
    if m_sec: tags.insert(0, m_sec.group(1))
    return tags[:5]


# Known mappings from chip text to URL. Targets accessible public sources
# (no account/paywall required). For framework standards that ARE paywalled
# at the source (e.g. ISO/IEC 42001), we link to a publicly accessible
# Microsoft Learn / Wikipedia summary instead.
GOLD_REFERENCES = {
    "TOGAF ADM": {
        "id": "TOGAF ADM",
        "label": "TOGAF ADM",
        "url": "https://en.wikipedia.org/wiki/The_Open_Group_Architecture_Framework",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "NIST AI RMF": {
        "id": "NIST AI RMF",
        "label": "NIST AI RMF",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "organization": "NIST",
        "license": "public-domain",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "NIST CSF": {
        "id": "NIST CSF",
        "label": "NIST CSF",
        "url": "https://www.nist.gov/cyberframework",
        "organization": "NIST",
        "license": "public-domain",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ISO/IEC 42001": {
        "id": "ISO/IEC 42001",
        "label": "ISO/IEC 42001",
        "url": "https://learn.microsoft.com/en-us/compliance/regulatory/offering-iso-42001",
        "organization": "Microsoft",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ISO 27001": {
        "id": "ISO 27001",
        "label": "ISO 27001",
        "url": "https://en.wikipedia.org/wiki/ISO/IEC_27001",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "AWS Well-Architected ML Lens": {
        "id": "AWS Well-Architected ML Lens",
        "label": "AWS Well-Architected ML Lens",
        "url": "https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html",
        "organization": "AWS",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "AWS Well-Architected": {
        "id": "AWS Well-Architected",
        "label": "AWS Well-Architected",
        "url": "https://aws.amazon.com/architecture/well-architected/",
        "organization": "AWS",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Domain-Driven Design": {
        "id": "Domain-Driven Design",
        "label": "Domain-Driven Design",
        "url": "https://en.wikipedia.org/wiki/Domain-driven_design",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Conway's Law": {
        "id": "Conway's Law",
        "label": "Conway's Law",
        "url": "https://en.wikipedia.org/wiki/Conway%27s_law",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "BIAN": {
        "id": "BIAN",
        "label": "BIAN",
        "url": "https://bian.org/",
        "organization": "BIAN",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "HL7 FHIR": {
        "id": "HL7 FHIR",
        "label": "HL7 FHIR",
        "url": "https://hl7.org/fhir/",
        "organization": "HL7",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Team Topologies": {
        "id": "Team Topologies",
        "label": "Team Topologies",
        "url": "https://teamtopologies.com/",
        "organization": "Team Topologies",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "SOLID": {
        "id": "SOLID",
        "label": "SOLID",
        "url": "https://en.wikipedia.org/wiki/SOLID",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Clean Architecture": {
        "id": "Clean Architecture",
        "label": "Clean Architecture",
        "url": "https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Hexagonal Architecture": {
        "id": "Hexagonal Architecture",
        "label": "Hexagonal Architecture",
        "url": "https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Strangler Fig Pattern": {
        "id": "Strangler Fig Pattern",
        "label": "Strangler Fig Pattern",
        "url": "https://martinfowler.com/bliki/StranglerFigApplication.html",
        "organization": "Martin Fowler",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Continuous Delivery": {
        "id": "Continuous Delivery",
        "label": "Continuous Delivery",
        "url": "https://en.wikipedia.org/wiki/Continuous_delivery",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Twelve-Factor App": {
        "id": "Twelve-Factor App",
        "label": "Twelve-Factor App",
        "url": "https://12factor.net/",
        "organization": "Heroku",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "CNCF Cloud Native": {
        "id": "CNCF Cloud Native",
        "label": "CNCF Cloud Native",
        "url": "https://github.com/cncf/toc/blob/main/DEFINITION.md",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Site Reliability Engineering": {
        "id": "Site Reliability Engineering",
        "label": "Site Reliability Engineering",
        "url": "https://sre.google/sre-book/table-of-contents/",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "SLSA": {
        "id": "SLSA",
        "label": "SLSA",
        "url": "https://slsa.dev/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "CQRS Pattern": {
        "id": "CQRS Pattern",
        "label": "CQRS Pattern",
        "url": "https://martinfowler.com/bliki/CQRS.html",
        "organization": "Martin Fowler",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Event Sourcing": {
        "id": "Event Sourcing",
        "label": "Event Sourcing",
        "url": "https://martinfowler.com/eaaDev/EventSourcing.html",
        "organization": "Martin Fowler",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Polyglot Persistence": {
        "id": "Polyglot Persistence",
        "label": "Polyglot Persistence",
        "url": "https://martinfowler.com/bliki/PolyglotPersistence.html",
        "organization": "Martin Fowler",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "DORA Metrics": {
        "id": "DORA Metrics",
        "label": "DORA Metrics",
        "url": "https://dora.dev/",
        "organization": "DORA",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Feature Toggles": {
        "id": "Feature Toggles",
        "label": "Feature Toggles",
        "url": "https://martinfowler.com/articles/feature-toggles.html",
        "organization": "Martin Fowler",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Trunk-Based Development": {
        "id": "Trunk-Based Development",
        "label": "Trunk-Based Development",
        "url": "https://trunkbaseddevelopment.com/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Enterprise Integration Patterns": {
        "id": "Enterprise Integration Patterns",
        "label": "Enterprise Integration Patterns",
        "url": "https://www.enterpriseintegrationpatterns.com/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "AsyncAPI": {
        "id": "AsyncAPI",
        "label": "AsyncAPI",
        "url": "https://www.asyncapi.com/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "OpenAPI": {
        "id": "OpenAPI",
        "label": "OpenAPI",
        "url": "https://www.openapis.org/",
        "organization": "OpenAPI Initiative",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "CloudEvents": {
        "id": "CloudEvents",
        "label": "CloudEvents",
        "url": "https://cloudevents.io/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "OWASP": {
        "id": "OWASP",
        "label": "OWASP",
        "url": "https://owasp.org/",
        "organization": "OWASP",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Zero Trust Architecture": {
        "id": "Zero Trust Architecture",
        "label": "Zero Trust Architecture",
        "url": "https://csrc.nist.gov/publications/detail/sp/800-207/final",
        "organization": "NIST",
        "license": "public-domain",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "GoF Design Patterns": {
        "id": "GoF Design Patterns",
        "label": "GoF Design Patterns",
        "url": "https://en.wikipedia.org/wiki/Design_Patterns",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Pattern-Oriented Software Architecture": {
        "id": "Pattern-Oriented Software Architecture",
        "label": "Pattern-Oriented Software Architecture",
        "url": "https://en.wikipedia.org/wiki/Pattern-Oriented_Software_Architecture",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ONNX": {
        "id": "ONNX",
        "label": "ONNX",
        "url": "https://onnx.ai/",
        "organization": "Linux Foundation",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "TensorFlow Lite": {
        "id": "TensorFlow Lite",
        "label": "TensorFlow Lite",
        "url": "https://www.tensorflow.org/lite",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Federated Learning": {
        "id": "Federated Learning",
        "label": "Federated Learning",
        "url": "https://en.wikipedia.org/wiki/Federated_learning",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Edge Computing": {
        "id": "Edge Computing",
        "label": "Edge Computing",
        "url": "https://en.wikipedia.org/wiki/Edge_computing",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Apache Kafka": {
        "id": "Apache Kafka",
        "label": "Apache Kafka",
        "url": "https://kafka.apache.org/",
        "organization": "Apache",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ISO 22301": {
        "id": "ISO 22301",
        "label": "ISO 22301",
        "url": "https://en.wikipedia.org/wiki/ISO_22301",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Chaos Engineering": {
        "id": "Chaos Engineering",
        "label": "Chaos Engineering",
        "url": "https://principlesofchaos.org/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "AWS Well-Architected Reliability Pillar": {
        "id": "AWS Well-Architected Reliability Pillar",
        "label": "AWS Well-Architected Reliability Pillar",
        "url": "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html",
        "organization": "AWS",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "CAP Theorem": {
        "id": "CAP Theorem",
        "label": "CAP Theorem",
        "url": "https://en.wikipedia.org/wiki/CAP_theorem",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Reactive Manifesto": {
        "id": "Reactive Manifesto",
        "label": "Reactive Manifesto",
        "url": "https://www.reactivemanifesto.org/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Frontend frameworks and UX
    "React": {
        "id": "React",
        "label": "React",
        "url": "https://react.dev/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Angular": {
        "id": "Angular",
        "label": "Angular",
        "url": "https://angular.dev/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Vue.js": {
        "id": "Vue.js",
        "label": "Vue.js",
        "url": "https://vuejs.org/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Svelte": {
        "id": "Svelte",
        "label": "Svelte",
        "url": "https://svelte.dev/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Web Vitals": {
        "id": "Web Vitals",
        "label": "Web Vitals",
        "url": "https://web.dev/articles/vitals",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Laws of UX": {
        "id": "Laws of UX",
        "label": "Laws of UX",
        "url": "https://lawsofux.com/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "WCAG": {
        "id": "WCAG",
        "label": "WCAG",
        "url": "https://www.w3.org/WAI/standards-guidelines/wcag/",
        "organization": "W3C",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Material Design": {
        "id": "Material Design",
        "label": "Material Design",
        "url": "https://m3.material.io/",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Storybook": {
        "id": "Storybook",
        "label": "Storybook",
        "url": "https://storybook.js.org/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Backend stacks
    "Spring Boot": {
        "id": "Spring Boot",
        "label": "Spring Boot",
        "url": "https://spring.io/projects/spring-boot",
        "organization": "VMware",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Node.js": {
        "id": "Node.js",
        "label": "Node.js",
        "url": "https://nodejs.org/",
        "organization": "OpenJS Foundation",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "FastAPI": {
        "id": "FastAPI",
        "label": "FastAPI",
        "url": "https://fastapi.tiangolo.com/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Django": {
        "id": "Django",
        "label": "Django",
        "url": "https://www.djangoproject.com/",
        "organization": "Django Software Foundation",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "OpenAPI": {
        "id": "OpenAPI",
        "label": "OpenAPI",
        "url": "https://www.openapis.org/",
        "organization": "OpenAPI Initiative",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "GraphQL": {
        "id": "GraphQL",
        "label": "GraphQL",
        "url": "https://graphql.org/",
        "organization": "GraphQL Foundation",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "gRPC": {
        "id": "gRPC",
        "label": "gRPC",
        "url": "https://grpc.io/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Databases
    "PostgreSQL": {
        "id": "PostgreSQL",
        "label": "PostgreSQL",
        "url": "https://www.postgresql.org/",
        "organization": "PostgreSQL",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "MongoDB": {
        "id": "MongoDB",
        "label": "MongoDB",
        "url": "https://www.mongodb.com/",
        "organization": "MongoDB",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Redis": {
        "id": "Redis",
        "label": "Redis",
        "url": "https://redis.io/",
        "organization": "Redis",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Apache Cassandra": {
        "id": "Apache Cassandra",
        "label": "Apache Cassandra",
        "url": "https://cassandra.apache.org/",
        "organization": "Apache",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Elasticsearch": {
        "id": "Elasticsearch",
        "label": "Elasticsearch",
        "url": "https://www.elastic.co/elasticsearch",
        "organization": "Elastic",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Neo4j": {
        "id": "Neo4j",
        "label": "Neo4j",
        "url": "https://neo4j.com/",
        "organization": "Neo4j",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Snowflake": {
        "id": "Snowflake",
        "label": "Snowflake",
        "url": "https://www.snowflake.com/",
        "organization": "Snowflake",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ClickHouse": {
        "id": "ClickHouse",
        "label": "ClickHouse",
        "url": "https://clickhouse.com/",
        "organization": "ClickHouse",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "InfluxDB": {
        "id": "InfluxDB",
        "label": "InfluxDB",
        "url": "https://www.influxdata.com/",
        "organization": "InfluxData",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Pinecone": {
        "id": "Pinecone",
        "label": "Pinecone",
        "url": "https://www.pinecone.io/",
        "organization": "Pinecone",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "pgvector": {
        "id": "pgvector",
        "label": "pgvector",
        "url": "https://github.com/pgvector/pgvector",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Cloud platforms
    "AWS": {
        "id": "AWS",
        "label": "AWS",
        "url": "https://aws.amazon.com/",
        "organization": "AWS",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Microsoft Azure": {
        "id": "Microsoft Azure",
        "label": "Microsoft Azure",
        "url": "https://azure.microsoft.com/",
        "organization": "Microsoft",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Google Cloud Platform": {
        "id": "Google Cloud Platform",
        "label": "Google Cloud Platform",
        "url": "https://cloud.google.com/",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "AWS Well-Architected": {
        "id": "AWS Well-Architected",
        "label": "AWS Well-Architected",
        "url": "https://aws.amazon.com/architecture/well-architected/",
        "organization": "AWS",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Azure Well-Architected Framework": {
        "id": "Azure Well-Architected Framework",
        "label": "Azure Well-Architected Framework",
        "url": "https://learn.microsoft.com/en-us/azure/well-architected/",
        "organization": "Microsoft",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "GCP Architecture Framework": {
        "id": "GCP Architecture Framework",
        "label": "GCP Architecture Framework",
        "url": "https://cloud.google.com/architecture/framework",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Terraform": {
        "id": "Terraform",
        "label": "Terraform",
        "url": "https://www.terraform.io/",
        "organization": "HashiCorp",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Pulumi": {
        "id": "Pulumi",
        "label": "Pulumi",
        "url": "https://www.pulumi.com/",
        "organization": "Pulumi",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # DevOps
    "GitHub Actions": {
        "id": "GitHub Actions",
        "label": "GitHub Actions",
        "url": "https://docs.github.com/en/actions",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "GitLab CI": {
        "id": "GitLab CI",
        "label": "GitLab CI",
        "url": "https://docs.gitlab.com/ee/ci/",
        "organization": "GitLab",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Argo CD": {
        "id": "Argo CD",
        "label": "Argo CD",
        "url": "https://argo-cd.readthedocs.io/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Flux CD": {
        "id": "Flux CD",
        "label": "Flux CD",
        "url": "https://fluxcd.io/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "OpenTelemetry": {
        "id": "OpenTelemetry",
        "label": "OpenTelemetry",
        "url": "https://opentelemetry.io/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Prometheus": {
        "id": "Prometheus",
        "label": "Prometheus",
        "url": "https://prometheus.io/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Grafana": {
        "id": "Grafana",
        "label": "Grafana",
        "url": "https://grafana.com/",
        "organization": "Grafana Labs",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "GitOps": {
        "id": "GitOps",
        "label": "GitOps",
        "url": "https://opengitops.dev/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "SLSA": {
        "id": "SLSA",
        "label": "SLSA",
        "url": "https://slsa.dev/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "DORA Metrics": {
        "id": "DORA Metrics",
        "label": "DORA Metrics",
        "url": "https://dora.dev/",
        "organization": "DORA",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Practice Circles platforms
    "Salesforce": {
        "id": "Salesforce",
        "label": "Salesforce",
        "url": "https://www.salesforce.com/",
        "organization": "Salesforce",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "MuleSoft": {
        "id": "MuleSoft",
        "label": "MuleSoft",
        "url": "https://www.mulesoft.com/",
        "organization": "Salesforce",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Microsoft Power Platform": {
        "id": "Microsoft Power Platform",
        "label": "Microsoft Power Platform",
        "url": "https://www.microsoft.com/en-us/power-platform",
        "organization": "Microsoft",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Power BI": {
        "id": "Power BI",
        "label": "Power BI",
        "url": "https://www.microsoft.com/en-us/power-platform/products/power-bi",
        "organization": "Microsoft",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Tableau": {
        "id": "Tableau",
        "label": "Tableau",
        "url": "https://www.tableau.com/",
        "organization": "Salesforce",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Microsoft Fabric": {
        "id": "Microsoft Fabric",
        "label": "Microsoft Fabric",
        "url": "https://www.microsoft.com/en-us/microsoft-fabric",
        "organization": "Microsoft",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Databricks": {
        "id": "Databricks",
        "label": "Databricks",
        "url": "https://www.databricks.com/",
        "organization": "Databricks",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Engagement models
    "SAFe": {
        "id": "SAFe",
        "label": "SAFe",
        "url": "https://framework.scaledagile.com/",
        "organization": "Scaled Agile",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Lean Software Development": {
        "id": "Lean Software Development",
        "label": "Lean Software Development",
        "url": "https://en.wikipedia.org/wiki/Lean_software_development",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Outcomes-Based Contracting": {
        "id": "Outcomes-Based Contracting",
        "label": "Outcomes-Based Contracting",
        "url": "https://en.wikipedia.org/wiki/Performance-based_contracting",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Security — application security
    "OWASP Top 10": {
        "id": "OWASP Top 10",
        "label": "OWASP Top 10",
        "url": "https://owasp.org/www-project-top-ten/",
        "organization": "OWASP",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "OWASP ASVS": {
        "id": "OWASP ASVS",
        "label": "OWASP ASVS",
        "url": "https://owasp.org/www-project-application-security-verification-standard/",
        "organization": "OWASP",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "OWASP SAMM": {
        "id": "OWASP SAMM",
        "label": "OWASP SAMM",
        "url": "https://owaspsamm.org/",
        "organization": "OWASP",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "STRIDE": {
        "id": "STRIDE",
        "label": "STRIDE",
        "url": "https://en.wikipedia.org/wiki/STRIDE_model",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "SLSA Framework": {
        "id": "SLSA Framework",
        "label": "SLSA Framework",
        "url": "https://slsa.dev/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Sigstore": {
        "id": "Sigstore",
        "label": "Sigstore",
        "url": "https://www.sigstore.dev/",
        "organization": "Linux Foundation",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "CycloneDX": {
        "id": "CycloneDX",
        "label": "CycloneDX",
        "url": "https://cyclonedx.org/",
        "organization": "OWASP",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "SPDX": {
        "id": "SPDX",
        "label": "SPDX",
        "url": "https://spdx.dev/",
        "organization": "Linux Foundation",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "CWE": {
        "id": "CWE",
        "label": "CWE",
        "url": "https://cwe.mitre.org/",
        "organization": "MITRE",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Security — authentication and authorization
    "OAuth 2.0": {
        "id": "OAuth 2.0",
        "label": "OAuth 2.0",
        "url": "https://oauth.net/2/",
        "organization": "IETF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "OpenID Connect": {
        "id": "OpenID Connect",
        "label": "OpenID Connect",
        "url": "https://openid.net/connect/",
        "organization": "OpenID Foundation",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "SAML 2.0": {
        "id": "SAML 2.0",
        "label": "SAML 2.0",
        "url": "https://en.wikipedia.org/wiki/SAML_2.0",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "FIDO2": {
        "id": "FIDO2",
        "label": "FIDO2",
        "url": "https://fidoalliance.org/fido2/",
        "organization": "FIDO Alliance",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "WebAuthn": {
        "id": "WebAuthn",
        "label": "WebAuthn",
        "url": "https://www.w3.org/TR/webauthn-2/",
        "organization": "W3C",
        "license": "cc-by-4.0",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Open Policy Agent": {
        "id": "Open Policy Agent",
        "label": "Open Policy Agent",
        "url": "https://www.openpolicyagent.org/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "JWT": {
        "id": "JWT",
        "label": "JWT",
        "url": "https://jwt.io/introduction",
        "organization": "Auth0",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "RBAC": {
        "id": "RBAC",
        "label": "RBAC",
        "url": "https://en.wikipedia.org/wiki/Role-based_access_control",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ABAC": {
        "id": "ABAC",
        "label": "ABAC",
        "url": "https://en.wikipedia.org/wiki/Attribute-based_access_control",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ReBAC": {
        "id": "ReBAC",
        "label": "ReBAC",
        "url": "https://en.wikipedia.org/wiki/Relationship-based_access_control",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Security — cloud security
    "AWS Shared Responsibility Model": {
        "id": "AWS Shared Responsibility Model",
        "label": "AWS Shared Responsibility Model",
        "url": "https://aws.amazon.com/compliance/shared-responsibility-model/",
        "organization": "AWS",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "CIS Benchmarks": {
        "id": "CIS Benchmarks",
        "label": "CIS Benchmarks",
        "url": "https://www.cisecurity.org/cis-benchmarks",
        "organization": "CIS",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "AWS Well-Architected Security Pillar": {
        "id": "AWS Well-Architected Security Pillar",
        "label": "AWS Well-Architected Security Pillar",
        "url": "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html",
        "organization": "AWS",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "NIST SP 800-207 Zero Trust": {
        "id": "NIST SP 800-207 Zero Trust",
        "label": "NIST SP 800-207 Zero Trust",
        "url": "https://csrc.nist.gov/publications/detail/sp/800-207/final",
        "organization": "NIST",
        "license": "public-domain",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "CSA Cloud Controls Matrix": {
        "id": "CSA Cloud Controls Matrix",
        "label": "CSA Cloud Controls Matrix",
        "url": "https://cloudsecurityalliance.org/research/cloud-controls-matrix",
        "organization": "CSA",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Security — encryption
    "NIST FIPS 140-3": {
        "id": "NIST FIPS 140-3",
        "label": "NIST FIPS 140-3",
        "url": "https://csrc.nist.gov/publications/detail/fips/140/3/final",
        "organization": "NIST",
        "license": "public-domain",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "TLS 1.3 (RFC 8446)": {
        "id": "TLS 1.3 (RFC 8446)",
        "label": "TLS 1.3 (RFC 8446)",
        "url": "https://datatracker.ietf.org/doc/html/rfc8446",
        "organization": "IETF",
        "license": "cc-by-4.0",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "AES (FIPS 197)": {
        "id": "AES (FIPS 197)",
        "label": "AES (FIPS 197)",
        "url": "https://csrc.nist.gov/publications/detail/fips/197/final",
        "organization": "NIST",
        "license": "public-domain",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "NIST Post-Quantum Cryptography": {
        "id": "NIST Post-Quantum Cryptography",
        "label": "NIST Post-Quantum Cryptography",
        "url": "https://csrc.nist.gov/projects/post-quantum-cryptography",
        "organization": "NIST",
        "license": "public-domain",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Let's Encrypt": {
        "id": "Let's Encrypt",
        "label": "Let's Encrypt",
        "url": "https://letsencrypt.org/",
        "organization": "Let's Encrypt",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Certificate Transparency": {
        "id": "Certificate Transparency",
        "label": "Certificate Transparency",
        "url": "https://certificate.transparency.dev/",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "libsodium": {
        "id": "libsodium",
        "label": "libsodium",
        "url": "https://doc.libsodium.org/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Tink": {
        "id": "Tink",
        "label": "Tink",
        "url": "https://developers.google.com/tink",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Security — vulnerability management
    "CVE Program": {
        "id": "CVE Program",
        "label": "CVE Program",
        "url": "https://www.cve.org/",
        "organization": "MITRE",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "CVSS": {
        "id": "CVSS",
        "label": "CVSS",
        "url": "https://www.first.org/cvss/",
        "organization": "FIRST",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "EPSS": {
        "id": "EPSS",
        "label": "EPSS",
        "url": "https://www.first.org/epss/",
        "organization": "FIRST",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "KEV Catalog": {
        "id": "KEV Catalog",
        "label": "KEV Catalog",
        "url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
        "organization": "CISA",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "NVD": {
        "id": "NVD",
        "label": "NVD",
        "url": "https://nvd.nist.gov/",
        "organization": "NIST",
        "license": "public-domain",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ISO 27001": {
        "id": "ISO 27001",
        "label": "ISO 27001",
        "url": "https://www.iso.org/standard/27001",
        "organization": "ISO",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "NIST SP 800-53": {
        "id": "NIST SP 800-53",
        "label": "NIST SP 800-53",
        "url": "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final",
        "organization": "NIST",
        "license": "public-domain",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # AI-Native — system architecture
    "Anthropic Engineering": {
        "id": "Anthropic Engineering",
        "label": "Anthropic Engineering",
        "url": "https://www.anthropic.com/engineering",
        "organization": "Anthropic",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Hugging Face": {
        "id": "Hugging Face",
        "label": "Hugging Face",
        "url": "https://huggingface.co/",
        "organization": "Hugging Face",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "vLLM": {
        "id": "vLLM",
        "label": "vLLM",
        "url": "https://docs.vllm.ai/",
        "organization": "vLLM",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "TensorRT-LLM": {
        "id": "TensorRT-LLM",
        "label": "TensorRT-LLM",
        "url": "https://github.com/NVIDIA/TensorRT-LLM",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Ray Serve": {
        "id": "Ray Serve",
        "label": "Ray Serve",
        "url": "https://docs.ray.io/en/latest/serve/index.html",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "LangGraph": {
        "id": "LangGraph",
        "label": "LangGraph",
        "url": "https://langchain-ai.github.io/langgraph/",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ReAct (Yao et al.)": {
        "id": "ReAct (Yao et al.)",
        "label": "ReAct (Yao et al.)",
        "url": "https://arxiv.org/abs/2210.03629",
        "organization": "arXiv",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "OpenAI Function Calling": {
        "id": "OpenAI Function Calling",
        "label": "OpenAI Function Calling",
        "url": "https://platform.openai.com/docs/guides/function-calling",
        "organization": "OpenAI",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # AI-Native — ethics & responsible AI
    "EU AI Act": {
        "id": "EU AI Act",
        "label": "EU AI Act",
        "url": "https://artificialintelligenceact.eu/the-act/",
        "organization": "EU",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "NIST AI Risk Management Framework": {
        "id": "NIST AI Risk Management Framework",
        "label": "NIST AI Risk Management Framework",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "organization": "NIST",
        "license": "public-domain",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ISO/IEC 42001": {
        "id": "ISO/IEC 42001",
        "label": "ISO/IEC 42001",
        "url": "https://www.iso.org/standard/81230.html",
        "organization": "ISO",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Model Cards (Mitchell et al.)": {
        "id": "Model Cards (Mitchell et al.)",
        "label": "Model Cards (Mitchell et al.)",
        "url": "https://arxiv.org/abs/1810.03993",
        "organization": "arXiv",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Datasheets for Datasets": {
        "id": "Datasheets for Datasets",
        "label": "Datasheets for Datasets",
        "url": "https://arxiv.org/abs/1803.09010",
        "organization": "arXiv",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Fairlearn": {
        "id": "Fairlearn",
        "label": "Fairlearn",
        "url": "https://fairlearn.org/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Aequitas Fairness Toolkit": {
        "id": "Aequitas Fairness Toolkit",
        "label": "Aequitas Fairness Toolkit",
        "url": "https://github.com/dssg/aequitas",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "OECD AI Principles": {
        "id": "OECD AI Principles",
        "label": "OECD AI Principles",
        "url": "https://oecd.ai/en/ai-principles",
        "organization": "OECD",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # AI-Native — monitoring & observability
    "OpenTelemetry GenAI Conventions": {
        "id": "OpenTelemetry GenAI Conventions",
        "label": "OpenTelemetry GenAI Conventions",
        "url": "https://opentelemetry.io/docs/specs/semconv/gen-ai/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Evidently AI": {
        "id": "Evidently AI",
        "label": "Evidently AI",
        "url": "https://www.evidentlyai.com/",
        "organization": "Evidently",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Arize Phoenix": {
        "id": "Arize Phoenix",
        "label": "Arize Phoenix",
        "url": "https://phoenix.arize.com/",
        "organization": "Arize",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "LangSmith": {
        "id": "LangSmith",
        "label": "LangSmith",
        "url": "https://docs.smith.langchain.com/",
        "organization": "LangChain",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Helicone": {
        "id": "Helicone",
        "label": "Helicone",
        "url": "https://www.helicone.ai/",
        "organization": "Helicone",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Langfuse": {
        "id": "Langfuse",
        "label": "Langfuse",
        "url": "https://langfuse.com/",
        "organization": "Langfuse",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "RAGAS": {
        "id": "RAGAS",
        "label": "RAGAS",
        "url": "https://docs.ragas.io/",
        "organization": "Ragas",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # AI-Native — RAG
    "FAISS": {
        "id": "FAISS",
        "label": "FAISS",
        "url": "https://github.com/facebookresearch/faiss",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Pinecone": {
        "id": "Pinecone",
        "label": "Pinecone",
        "url": "https://www.pinecone.io/",
        "organization": "Pinecone",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Weaviate": {
        "id": "Weaviate",
        "label": "Weaviate",
        "url": "https://weaviate.io/",
        "organization": "Weaviate",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Qdrant": {
        "id": "Qdrant",
        "label": "Qdrant",
        "url": "https://qdrant.tech/",
        "organization": "Qdrant",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ChromaDB": {
        "id": "ChromaDB",
        "label": "ChromaDB",
        "url": "https://www.trychroma.com/",
        "organization": "Chroma",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "BM25 (Wikipedia)": {
        "id": "BM25 (Wikipedia)",
        "label": "BM25 (Wikipedia)",
        "url": "https://en.wikipedia.org/wiki/Okapi_BM25",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "MTEB Embedding Benchmark": {
        "id": "MTEB Embedding Benchmark",
        "label": "MTEB Embedding Benchmark",
        "url": "https://huggingface.co/spaces/mteb/leaderboard",
        "organization": "Hugging Face",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "HyDE (Gao et al.)": {
        "id": "HyDE (Gao et al.)",
        "label": "HyDE (Gao et al.)",
        "url": "https://arxiv.org/abs/2212.10496",
        "organization": "arXiv",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ColBERT (Khattab & Zaharia)": {
        "id": "ColBERT (Khattab & Zaharia)",
        "label": "ColBERT (Khattab & Zaharia)",
        "url": "https://arxiv.org/abs/2004.12832",
        "organization": "arXiv",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # AI-Native — security
    "OWASP Top 10 for LLM Applications": {
        "id": "OWASP Top 10 for LLM Applications",
        "label": "OWASP Top 10 for LLM Applications",
        "url": "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
        "organization": "OWASP",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "MITRE ATLAS": {
        "id": "MITRE ATLAS",
        "label": "MITRE ATLAS",
        "url": "https://atlas.mitre.org/",
        "organization": "MITRE",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "NIST AI 100-2 (Adversarial ML)": {
        "id": "NIST AI 100-2 (Adversarial ML)",
        "label": "NIST AI 100-2 (Adversarial ML)",
        "url": "https://csrc.nist.gov/publications/detail/ai/100-2/final",
        "organization": "NIST",
        "license": "public-domain",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Google Secure AI Framework (SAIF)": {
        "id": "Google Secure AI Framework (SAIF)",
        "label": "Google Secure AI Framework (SAIF)",
        "url": "https://safety.google/cybersecurity-advancements/saif/",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Anthropic Responsible Scaling Policy": {
        "id": "Anthropic Responsible Scaling Policy",
        "label": "Anthropic Responsible Scaling Policy",
        "url": "https://www.anthropic.com/news/announcing-our-updated-responsible-scaling-policy",
        "organization": "Anthropic",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Garak LLM Vulnerability Scanner": {
        "id": "Garak LLM Vulnerability Scanner",
        "label": "Garak LLM Vulnerability Scanner",
        "url": "https://github.com/NVIDIA/garak",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Prompt Injection (Greshake et al.)": {
        "id": "Prompt Injection (Greshake et al.)",
        "label": "Prompt Injection (Greshake et al.)",
        "url": "https://arxiv.org/abs/2302.12173",
        "organization": "arXiv",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Governance — frameworks, ADR, architecture authority
    "ADR (Michael Nygard)": {
        "id": "ADR (Michael Nygard)",
        "label": "ADR (Michael Nygard)",
        "url": "https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions",
        "organization": "Cognitect",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ADR GitHub Organization": {
        "id": "ADR GitHub Organization",
        "label": "ADR GitHub Organization",
        "url": "https://adr.github.io/",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "RFC Process (IETF)": {
        "id": "RFC Process (IETF)",
        "label": "RFC Process (IETF)",
        "url": "https://www.ietf.org/standards/rfcs/",
        "organization": "IETF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ATAM (SEI)": {
        "id": "ATAM (SEI)",
        "label": "ATAM (SEI)",
        "url": "https://insights.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/",
        "organization": "SEI",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "TOGAF": {
        "id": "TOGAF",
        "label": "TOGAF",
        "url": "https://www.opengroup.org/togaf",
        "organization": "The Open Group",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "COBIT 2019 (ISACA)": {
        "id": "COBIT 2019 (ISACA)",
        "label": "COBIT 2019 (ISACA)",
        "url": "https://www.isaca.org/resources/cobit",
        "organization": "ISACA",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "AWS Well-Architected Framework": {
        "id": "AWS Well-Architected Framework",
        "label": "AWS Well-Architected Framework",
        "url": "https://aws.amazon.com/architecture/well-architected/",
        "organization": "AWS",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Team Topologies": {
        "id": "Team Topologies",
        "label": "Team Topologies",
        "url": "https://teamtopologies.com/",
        "organization": "Team Topologies",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Spotify Engineering Culture": {
        "id": "Spotify Engineering Culture",
        "label": "Spotify Engineering Culture",
        "url": "https://engineering.atspotify.com/",
        "organization": "Spotify",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ThoughtWorks Technology Radar": {
        "id": "ThoughtWorks Technology Radar",
        "label": "ThoughtWorks Technology Radar",
        "url": "https://www.thoughtworks.com/radar",
        "organization": "ThoughtWorks",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "DORA Metrics": {
        "id": "DORA Metrics",
        "label": "DORA Metrics",
        "url": "https://dora.dev/",
        "organization": "DORA",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Conway's Law (Wikipedia)": {
        "id": "Conway's Law (Wikipedia)",
        "label": "Conway's Law (Wikipedia)",
        "url": "https://en.wikipedia.org/wiki/Conway%27s_law",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Architecture Advice Process (Andrew Harmel-Law)": {
        "id": "Architecture Advice Process (Andrew Harmel-Law)",
        "label": "Architecture Advice Process (Andrew Harmel-Law)",
        "url": "https://martinfowler.com/articles/scaling-architecture-conversationally.html",
        "organization": "Martin Fowler",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Apache Project Governance": {
        "id": "Apache Project Governance",
        "label": "Apache Project Governance",
        "url": "https://www.apache.org/foundation/how-it-works.html",
        "organization": "Apache",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Kubernetes Governance": {
        "id": "Kubernetes Governance",
        "label": "Kubernetes Governance",
        "url": "https://kubernetes.io/community/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "RACI Matrix (Wikipedia)": {
        "id": "RACI Matrix (Wikipedia)",
        "label": "RACI Matrix (Wikipedia)",
        "url": "https://en.wikipedia.org/wiki/Responsibility_assignment_matrix",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Observability — SRE foundations
    "Google SRE Book": {
        "id": "Google SRE Book",
        "label": "Google SRE Book",
        "url": "https://sre.google/sre-book/table-of-contents/",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Google SRE Workbook": {
        "id": "Google SRE Workbook",
        "label": "Google SRE Workbook",
        "url": "https://sre.google/workbook/table-of-contents/",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Prometheus": {
        "id": "Prometheus",
        "label": "Prometheus",
        "url": "https://prometheus.io/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Grafana": {
        "id": "Grafana",
        "label": "Grafana",
        "url": "https://grafana.com/",
        "organization": "Grafana Labs",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "OpenTelemetry": {
        "id": "OpenTelemetry",
        "label": "OpenTelemetry",
        "url": "https://opentelemetry.io/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Jaeger": {
        "id": "Jaeger",
        "label": "Jaeger",
        "url": "https://www.jaegertracing.io/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Zipkin": {
        "id": "Zipkin",
        "label": "Zipkin",
        "url": "https://zipkin.io/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Honeycomb": {
        "id": "Honeycomb",
        "label": "Honeycomb",
        "url": "https://www.honeycomb.io/",
        "organization": "Honeycomb",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ELK Stack (Elastic)": {
        "id": "ELK Stack (Elastic)",
        "label": "ELK Stack (Elastic)",
        "url": "https://www.elastic.co/elastic-stack/",
        "organization": "Elastic",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Datadog": {
        "id": "Datadog",
        "label": "Datadog",
        "url": "https://www.datadoghq.com/",
        "organization": "Datadog",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Observability — methods
    "RED Method (Tom Wilkie)": {
        "id": "RED Method (Tom Wilkie)",
        "label": "RED Method (Tom Wilkie)",
        "url": "https://www.weave.works/blog/the-red-method-key-metrics-for-microservices-architecture/",
        "organization": "Weaveworks",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "USE Method (Brendan Gregg)": {
        "id": "USE Method (Brendan Gregg)",
        "label": "USE Method (Brendan Gregg)",
        "url": "https://www.brendangregg.com/usemethod.html",
        "organization": "Brendan Gregg",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "The Four Golden Signals (Google SRE)": {
        "id": "The Four Golden Signals (Google SRE)",
        "label": "The Four Golden Signals (Google SRE)",
        "url": "https://sre.google/sre-book/monitoring-distributed-systems/",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Multi-Window Multi-Burn-Rate Alerts (Google SRE)": {
        "id": "Multi-Window Multi-Burn-Rate Alerts (Google SRE)",
        "label": "Multi-Window Multi-Burn-Rate Alerts (Google SRE)",
        "url": "https://sre.google/workbook/alerting-on-slos/",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Service Level Objectives (Alex Hidalgo)": {
        "id": "Service Level Objectives (Alex Hidalgo)",
        "label": "Service Level Objectives (Alex Hidalgo)",
        "url": "https://www.oreilly.com/library/view/implementing-service-level/9781492076803/",
        "organization": "O'Reilly",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Charity Majors on Observability": {
        "id": "Charity Majors on Observability",
        "label": "Charity Majors on Observability",
        "url": "https://charity.wtf/",
        "organization": "Charity Majors",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "PagerDuty Incident Response": {
        "id": "PagerDuty Incident Response",
        "label": "PagerDuty Incident Response",
        "url": "https://response.pagerduty.com/",
        "organization": "PagerDuty",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Atlassian Incident Handbook": {
        "id": "Atlassian Incident Handbook",
        "label": "Atlassian Incident Handbook",
        "url": "https://www.atlassian.com/incident-management/handbook",
        "organization": "Atlassian",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Postmortem (Wikipedia)": {
        "id": "Postmortem (Wikipedia)",
        "label": "Postmortem (Wikipedia)",
        "url": "https://en.wikipedia.org/wiki/Postmortem_documentation",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "HDR Histogram": {
        "id": "HDR Histogram",
        "label": "HDR Histogram",
        "url": "https://github.com/HdrHistogram/HdrHistogram",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "T-Digest (Dunning)": {
        "id": "T-Digest (Dunning)",
        "label": "T-Digest (Dunning)",
        "url": "https://github.com/tdunning/t-digest",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "OpenTelemetry Sampling": {
        "id": "OpenTelemetry Sampling",
        "label": "OpenTelemetry Sampling",
        "url": "https://opentelemetry.io/docs/concepts/sampling/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Distributed Tracing in Practice (Parker et al.)": {
        "id": "Distributed Tracing in Practice (Parker et al.)",
        "label": "Distributed Tracing in Practice (Parker et al.)",
        "url": "https://www.oreilly.com/library/view/distributed-tracing-in/9781492056621/",
        "organization": "O'Reilly",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Brendan Gregg Performance Tools": {
        "id": "Brendan Gregg Performance Tools",
        "label": "Brendan Gregg Performance Tools",
        "url": "https://www.brendangregg.com/perf.html",
        "organization": "Brendan Gregg",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "W3C Trace Context": {
        "id": "W3C Trace Context",
        "label": "W3C Trace Context",
        "url": "https://www.w3.org/TR/trace-context/",
        "organization": "W3C",
        "license": "cc-by-4.0",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Allspaw — Blameless Postmortems": {
        "id": "Allspaw — Blameless Postmortems",
        "label": "Allspaw — Blameless Postmortems",
        "url": "https://www.etsy.com/codeascraft/blameless-postmortems",
        "organization": "Etsy",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Distributed Systems Observability (Cindy Sridharan)": {
        "id": "Distributed Systems Observability (Cindy Sridharan)",
        "label": "Distributed Systems Observability (Cindy Sridharan)",
        "url": "https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/",
        "organization": "O'Reilly",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Error Budget Policy (Google SRE)": {
        "id": "Error Budget Policy (Google SRE)",
        "label": "Error Budget Policy (Google SRE)",
        "url": "https://sre.google/workbook/error-budget-policy/",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ITIL Incident Management": {
        "id": "ITIL Incident Management",
        "label": "ITIL Incident Management",
        "url": "https://www.axelos.com/certifications/propath/itil-4",
        "organization": "AXELOS",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Runbooks — execution, deployment, migration, rollback patterns
    "Runbook (Wikipedia)": {
        "id": "Runbook (Wikipedia)",
        "label": "Runbook (Wikipedia)",
        "url": "https://en.wikipedia.org/wiki/Runbook",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "GitOps Principles": {
        "id": "GitOps Principles",
        "label": "GitOps Principles",
        "url": "https://opengitops.dev/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Argo CD": {
        "id": "Argo CD",
        "label": "Argo CD",
        "url": "https://argo-cd.readthedocs.io/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Spinnaker — Continuous Delivery Platform": {
        "id": "Spinnaker — Continuous Delivery Platform",
        "label": "Spinnaker — Continuous Delivery Platform",
        "url": "https://spinnaker.io/",
        "organization": "Linux Foundation",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Feature Flags (Martin Fowler)": {
        "id": "Feature Flags (Martin Fowler)",
        "label": "Feature Flags (Martin Fowler)",
        "url": "https://martinfowler.com/articles/feature-toggles.html",
        "organization": "Martin Fowler",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Blue-Green Deployment (Martin Fowler)": {
        "id": "Blue-Green Deployment (Martin Fowler)",
        "label": "Blue-Green Deployment (Martin Fowler)",
        "url": "https://martinfowler.com/bliki/BlueGreenDeployment.html",
        "organization": "Martin Fowler",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Canary Release (Martin Fowler)": {
        "id": "Canary Release (Martin Fowler)",
        "label": "Canary Release (Martin Fowler)",
        "url": "https://martinfowler.com/bliki/CanaryRelease.html",
        "organization": "Martin Fowler",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Strangler Fig Pattern (Martin Fowler)": {
        "id": "Strangler Fig Pattern (Martin Fowler)",
        "label": "Strangler Fig Pattern (Martin Fowler)",
        "url": "https://martinfowler.com/bliki/StranglerFigApplication.html",
        "organization": "Martin Fowler",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Database Refactoring (Ambler & Sadalage)": {
        "id": "Database Refactoring (Ambler & Sadalage)",
        "label": "Database Refactoring (Ambler & Sadalage)",
        "url": "https://martinfowler.com/books/refactoringDatabases.html",
        "organization": "Martin Fowler",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Online Schema Migration (gh-ost)": {
        "id": "Online Schema Migration (gh-ost)",
        "label": "Online Schema Migration (gh-ost)",
        "url": "https://github.com/github/gh-ost",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Continuous Delivery (Humble & Farley)": {
        "id": "Continuous Delivery (Humble & Farley)",
        "label": "Continuous Delivery (Humble & Farley)",
        "url": "https://www.oreilly.com/library/view/continuous-delivery-reliable/9780321670250/",
        "organization": "O'Reilly",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Accelerate (Forsgren, Humble, Kim)": {
        "id": "Accelerate (Forsgren, Humble, Kim)",
        "label": "Accelerate (Forsgren, Humble, Kim)",
        "url": "https://itrevolution.com/product/accelerate/",
        "organization": "IT Revolution",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "The Phoenix Project (Kim et al.)": {
        "id": "The Phoenix Project (Kim et al.)",
        "label": "The Phoenix Project (Kim et al.)",
        "url": "https://itrevolution.com/product/the-phoenix-project/",
        "organization": "IT Revolution",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Chaos Engineering (Rosenthal et al.)": {
        "id": "Chaos Engineering (Rosenthal et al.)",
        "label": "Chaos Engineering (Rosenthal et al.)",
        "url": "https://www.oreilly.com/library/view/chaos-engineering/9781492043850/",
        "organization": "O'Reilly",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Game Days (Google SRE)": {
        "id": "Game Days (Google SRE)",
        "label": "Game Days (Google SRE)",
        "url": "https://sre.google/sre-book/testing-reliability/",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Decommissioning Patterns (Lewis)": {
        "id": "Decommissioning Patterns (Lewis)",
        "label": "Decommissioning Patterns (Lewis)",
        "url": "https://martinfowler.com/articles/distributed-objects-microservices.html",
        "organization": "Martin Fowler",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Review checklists — architecture review, deployment readiness, security review
    "ATAM (Architecture Tradeoff Analysis Method)": {
        "id": "ATAM (Architecture Tradeoff Analysis Method)",
        "label": "ATAM (Architecture Tradeoff Analysis Method)",
        "url": "https://www.sei.cmu.edu/our-work/projects/display.cfm?customel_datapageid_4050=21859",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Software Architecture in Practice (Bass et al.)": {
        "id": "Software Architecture in Practice (Bass et al.)",
        "label": "Software Architecture in Practice (Bass et al.)",
        "url": "https://www.oreilly.com/library/view/software-architecture-in/9780136885979/",
        "organization": "O'Reilly",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "AWS Well-Architected Framework": {
        "id": "AWS Well-Architected Framework",
        "label": "AWS Well-Architected Framework",
        "url": "https://aws.amazon.com/architecture/well-architected/",
        "organization": "AWS",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Azure Well-Architected Framework": {
        "id": "Azure Well-Architected Framework",
        "label": "Azure Well-Architected Framework",
        "url": "https://learn.microsoft.com/en-us/azure/well-architected/",
        "organization": "Microsoft",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Google Cloud Architecture Framework": {
        "id": "Google Cloud Architecture Framework",
        "label": "Google Cloud Architecture Framework",
        "url": "https://cloud.google.com/architecture/framework",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "OWASP Top 10": {
        "id": "OWASP Top 10",
        "label": "OWASP Top 10",
        "url": "https://owasp.org/www-project-top-ten/",
        "organization": "OWASP",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "OWASP Application Security Verification Standard": {
        "id": "OWASP Application Security Verification Standard",
        "label": "OWASP Application Security Verification Standard",
        "url": "https://owasp.org/www-project-application-security-verification-standard/",
        "organization": "OWASP",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "OWASP Software Assurance Maturity Model (SAMM)": {
        "id": "OWASP Software Assurance Maturity Model (SAMM)",
        "label": "OWASP Software Assurance Maturity Model (SAMM)",
        "url": "https://owaspsamm.org/",
        "organization": "OWASP",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "NIST Secure Software Development Framework": {
        "id": "NIST Secure Software Development Framework",
        "label": "NIST Secure Software Development Framework",
        "url": "https://csrc.nist.gov/projects/ssdf",
        "organization": "NIST",
        "license": "public-domain",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "STRIDE Threat Model": {
        "id": "STRIDE Threat Model",
        "label": "STRIDE Threat Model",
        "url": "https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats",
        "organization": "Microsoft",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Threat Modeling Manifesto": {
        "id": "Threat Modeling Manifesto",
        "label": "Threat Modeling Manifesto",
        "url": "https://www.threatmodelingmanifesto.org/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "SLSA Framework": {
        "id": "SLSA Framework",
        "label": "SLSA Framework",
        "url": "https://slsa.dev/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "12-Factor App": {
        "id": "12-Factor App",
        "label": "12-Factor App",
        "url": "https://12factor.net/",
        "organization": "Heroku",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Production-Ready Microservices (Fowler)": {
        "id": "Production-Ready Microservices (Fowler)",
        "label": "Production-Ready Microservices (Fowler)",
        "url": "https://www.oreilly.com/library/view/production-ready-microservices/9781491965962/",
        "organization": "O'Reilly",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Release It! (Nygard)": {
        "id": "Release It! (Nygard)",
        "label": "Release It! (Nygard)",
        "url": "https://pragprog.com/titles/mnee2/release-it-second-edition/",
        "organization": "Pragmatic Bookshelf",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Code Review Best Practices (Google)": {
        "id": "Code Review Best Practices (Google)",
        "label": "Code Review Best Practices (Google)",
        "url": "https://google.github.io/eng-practices/review/",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Pull Request Review Patterns": {
        "id": "Pull Request Review Patterns",
        "label": "Pull Request Review Patterns",
        "url": "https://martinfowler.com/articles/ship-show-ask.html",
        "organization": "Martin Fowler",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Architecture Tooling — agents, CLI, scripts, validators
    "Anthropic Model Context Protocol (MCP)": {
        "id": "Anthropic Model Context Protocol (MCP)",
        "label": "Anthropic Model Context Protocol (MCP)",
        "url": "https://modelcontextprotocol.io/",
        "organization": "Anthropic",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Anthropic Building Effective Agents": {
        "id": "Anthropic Building Effective Agents",
        "label": "Anthropic Building Effective Agents",
        "url": "https://www.anthropic.com/research/building-effective-agents",
        "organization": "Anthropic",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Anthropic Tool Use": {
        "id": "Anthropic Tool Use",
        "label": "Anthropic Tool Use",
        "url": "https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview",
        "organization": "Anthropic",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ReAct (Reasoning and Acting)": {
        "id": "ReAct (Reasoning and Acting)",
        "label": "ReAct (Reasoning and Acting)",
        "url": "https://arxiv.org/abs/2210.03629",
        "organization": "arXiv",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Toolformer (Schick et al.)": {
        "id": "Toolformer (Schick et al.)",
        "label": "Toolformer (Schick et al.)",
        "url": "https://arxiv.org/abs/2302.04761",
        "organization": "arXiv",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "OpenAI Function Calling": {
        "id": "OpenAI Function Calling",
        "label": "OpenAI Function Calling",
        "url": "https://platform.openai.com/docs/guides/function-calling",
        "organization": "OpenAI",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "LangChain Agents": {
        "id": "LangChain Agents",
        "label": "LangChain Agents",
        "url": "https://python.langchain.com/docs/concepts/agents/",
        "organization": "LangChain",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Click — Python CLI Framework": {
        "id": "Click — Python CLI Framework",
        "label": "Click — Python CLI Framework",
        "url": "https://click.palletsprojects.com/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Cobra — Go CLI Framework": {
        "id": "Cobra — Go CLI Framework",
        "label": "Cobra — Go CLI Framework",
        "url": "https://cobra.dev/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Clap — Rust CLI Framework": {
        "id": "Clap — Rust CLI Framework",
        "label": "Clap — Rust CLI Framework",
        "url": "https://docs.rs/clap/latest/clap/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "12-Factor CLI Apps": {
        "id": "12-Factor CLI Apps",
        "label": "12-Factor CLI Apps",
        "url": "https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Command Line Interface Guidelines": {
        "id": "Command Line Interface Guidelines",
        "label": "Command Line Interface Guidelines",
        "url": "https://clig.dev/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "POSIX Utility Conventions": {
        "id": "POSIX Utility Conventions",
        "label": "POSIX Utility Conventions",
        "url": "https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html",
        "organization": "The Open Group",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Bash Pitfalls": {
        "id": "Bash Pitfalls",
        "label": "Bash Pitfalls",
        "url": "https://mywiki.wooledge.org/BashPitfalls",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Idempotence (Wikipedia)": {
        "id": "Idempotence (Wikipedia)",
        "label": "Idempotence (Wikipedia)",
        "url": "https://en.wikipedia.org/wiki/Idempotence",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Make as Build Tool": {
        "id": "Make as Build Tool",
        "label": "Make as Build Tool",
        "url": "https://www.gnu.org/software/make/",
        "organization": "GNU",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Ansible — Configuration Management": {
        "id": "Ansible — Configuration Management",
        "label": "Ansible — Configuration Management",
        "url": "https://docs.ansible.com/",
        "organization": "Red Hat",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Salt — Configuration Management": {
        "id": "Salt — Configuration Management",
        "label": "Salt — Configuration Management",
        "url": "https://saltproject.io/",
        "organization": "VMware",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Terraform — Infrastructure as Code": {
        "id": "Terraform — Infrastructure as Code",
        "label": "Terraform — Infrastructure as Code",
        "url": "https://www.terraform.io/",
        "organization": "HashiCorp",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Pulumi — Infrastructure as Code": {
        "id": "Pulumi — Infrastructure as Code",
        "label": "Pulumi — Infrastructure as Code",
        "url": "https://www.pulumi.com/",
        "organization": "Pulumi",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "JSON Schema": {
        "id": "JSON Schema",
        "label": "JSON Schema",
        "url": "https://json-schema.org/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "OpenAPI Specification": {
        "id": "OpenAPI Specification",
        "label": "OpenAPI Specification",
        "url": "https://www.openapis.org/",
        "organization": "OpenAPI Initiative",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Protobuf — Protocol Buffers": {
        "id": "Protobuf — Protocol Buffers",
        "label": "Protobuf — Protocol Buffers",
        "url": "https://protobuf.dev/",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Pydantic — Python Validation": {
        "id": "Pydantic — Python Validation",
        "label": "Pydantic — Python Validation",
        "url": "https://docs.pydantic.dev/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Pact — Contract Testing": {
        "id": "Pact — Contract Testing",
        "label": "Pact — Contract Testing",
        "url": "https://pact.io/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Schemathesis — API Testing": {
        "id": "Schemathesis — API Testing",
        "label": "Schemathesis — API Testing",
        "url": "https://schemathesis.readthedocs.io/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Open Policy Agent (OPA) Rego": {
        "id": "Open Policy Agent (OPA) Rego",
        "label": "Open Policy Agent (OPA) Rego",
        "url": "https://www.openpolicyagent.org/docs/latest/policy-language/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Conftest — Policy Testing": {
        "id": "Conftest — Policy Testing",
        "label": "Conftest — Policy Testing",
        "url": "https://www.conftest.dev/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ESLint — JavaScript Linter": {
        "id": "ESLint — JavaScript Linter",
        "label": "ESLint — JavaScript Linter",
        "url": "https://eslint.org/",
        "organization": "OpenJS Foundation",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ruff — Python Linter": {
        "id": "ruff — Python Linter",
        "label": "ruff — Python Linter",
        "url": "https://docs.astral.sh/ruff/",
        "organization": "Astral",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "shellcheck — Bash Linter": {
        "id": "shellcheck — Bash Linter",
        "label": "shellcheck — Bash Linter",
        "url": "https://www.shellcheck.net/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Architecture Templates — ADRs, review docs, scorecards
    "Documenting Architecture Decisions (Nygard)": {
        "id": "Documenting Architecture Decisions (Nygard)",
        "label": "Documenting Architecture Decisions (Nygard)",
        "url": "https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions",
        "organization": "Cognitect",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "MADR — Markdown ADRs": {
        "id": "MADR — Markdown ADRs",
        "label": "MADR — Markdown ADRs",
        "url": "https://adr.github.io/madr/",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Building Evolutionary Architectures (Ford et al.)": {
        "id": "Building Evolutionary Architectures (Ford et al.)",
        "label": "Building Evolutionary Architectures (Ford et al.)",
        "url": "https://www.oreilly.com/library/view/building-evolutionary-architectures/9781491986356/",
        "organization": "O'Reilly",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ThoughtWorks Tech Radar": {
        "id": "ThoughtWorks Tech Radar",
        "label": "ThoughtWorks Tech Radar",
        "url": "https://www.thoughtworks.com/radar",
        "organization": "ThoughtWorks",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Google Engineering Practices Documentation": {
        "id": "Google Engineering Practices Documentation",
        "label": "Google Engineering Practices Documentation",
        "url": "https://google.github.io/eng-practices/",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Rust RFC Process": {
        "id": "Rust RFC Process",
        "label": "Rust RFC Process",
        "url": "https://rust-lang.github.io/rfcs/",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Python PEP Process": {
        "id": "Python PEP Process",
        "label": "Python PEP Process",
        "url": "https://peps.python.org/",
        "organization": "Python",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "IETF RFC Process": {
        "id": "IETF RFC Process",
        "label": "IETF RFC Process",
        "url": "https://www.ietf.org/standards/rfcs/",
        "organization": "IETF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ARID — Active Reviews for Intermediate Designs": {
        "id": "ARID — Active Reviews for Intermediate Designs",
        "label": "ARID — Active Reviews for Intermediate Designs",
        "url": "https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=6276",
        "organization": "SEI",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "CNCF Cloud Native Maturity Model": {
        "id": "CNCF Cloud Native Maturity Model",
        "label": "CNCF Cloud Native Maturity Model",
        "url": "https://maturitymodel.cncf.io/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "DORA — DevOps Research and Assessment": {
        "id": "DORA — DevOps Research and Assessment",
        "label": "DORA — DevOps Research and Assessment",
        "url": "https://dora.dev/",
        "organization": "DORA",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Google SRE Workbook — Production Readiness Reviews": {
        "id": "Google SRE Workbook — Production Readiness Reviews",
        "label": "Google SRE Workbook — Production Readiness Reviews",
        "url": "https://sre.google/workbook/evolving-sre-engagement-model/",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Backstage — Software Catalog": {
        "id": "Backstage — Software Catalog",
        "label": "Backstage — Software Catalog",
        "url": "https://backstage.io/docs/features/software-catalog/",
        "organization": "CNCF",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Diátaxis Documentation Framework": {
        "id": "Diátaxis Documentation Framework",
        "label": "Diátaxis Documentation Framework",
        "url": "https://diataxis.fr/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },

    # ─── v37 Engineering Playbooks references ───
    # API Lifecycle
    "Stripe API Reference": {
        "id": "Stripe API Reference",
        "label": "Stripe API Reference",
        "url": "https://stripe.com/docs/api",
        "organization": "Stripe",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Microsoft REST API Guidelines": {
        "id": "Microsoft REST API Guidelines",
        "label": "Microsoft REST API Guidelines",
        "url": "https://github.com/microsoft/api-guidelines",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Google API Improvement Proposals (AIP)": {
        "id": "Google API Improvement Proposals (AIP)",
        "label": "Google API Improvement Proposals (AIP)",
        "url": "https://google.aip.dev/",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Semantic Versioning 2.0": {
        "id": "Semantic Versioning 2.0",
        "label": "Semantic Versioning 2.0",
        "url": "https://semver.org/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "RFC 8594 — Sunset HTTP Header": {
        "id": "RFC 8594 — Sunset HTTP Header",
        "label": "RFC 8594 — Sunset HTTP Header",
        "url": "https://www.rfc-editor.org/rfc/rfc8594",
        "organization": "IETF",
        "license": "cc-by-4.0",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "API Stylebook": {
        "id": "API Stylebook",
        "label": "API Stylebook",
        "url": "https://apistylebook.com/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Migration Playbook
    "Branch by Abstraction (Fowler)": {
        "id": "Branch by Abstraction (Fowler)",
        "label": "Branch by Abstraction (Fowler)",
        "url": "https://martinfowler.com/bliki/BranchByAbstraction.html",
        "organization": "Martin Fowler",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Refactoring Databases": {
        "id": "Refactoring Databases",
        "label": "Refactoring Databases",
        "url": "https://databaserefactoring.com/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Working Effectively with Legacy Code (Feathers)": {
        "id": "Working Effectively with Legacy Code (Feathers)",
        "label": "Working Effectively with Legacy Code (Feathers)",
        "url": "https://www.oreilly.com/library/view/working-effectively-with/0131177052/",
        "organization": "O'Reilly",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "AWS Migration Strategies — 7 Rs": {
        "id": "AWS Migration Strategies — 7 Rs",
        "label": "AWS Migration Strategies — 7 Rs",
        "url": "https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-strategies/migration-strategies.html",
        "organization": "AWS",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Liquibase": {
        "id": "Liquibase",
        "label": "Liquibase",
        "url": "https://www.liquibase.org/",
        "organization": "Liquibase",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Flyway Database Migrations": {
        "id": "Flyway Database Migrations",
        "label": "Flyway Database Migrations",
        "url": "https://flywaydb.org/",
        "organization": "Redgate",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Resilience Playbook
    "Resilience4j": {
        "id": "Resilience4j",
        "label": "Resilience4j",
        "url": "https://resilience4j.readme.io/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Polly — .NET resilience library": {
        "id": "Polly — .NET resilience library",
        "label": "Polly — .NET resilience library",
        "url": "https://www.thepollyproject.org/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Hystrix (Netflix)": {
        "id": "Hystrix (Netflix)",
        "label": "Hystrix (Netflix)",
        "url": "https://github.com/Netflix/Hystrix",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Bulkhead Pattern (Microsoft)": {
        "id": "Bulkhead Pattern (Microsoft)",
        "label": "Bulkhead Pattern (Microsoft)",
        "url": "https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead",
        "organization": "Microsoft",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Circuit Breaker (Fowler)": {
        "id": "Circuit Breaker (Fowler)",
        "label": "Circuit Breaker (Fowler)",
        "url": "https://martinfowler.com/bliki/CircuitBreaker.html",
        "organization": "Martin Fowler",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Erlang/OTP": {
        "id": "Erlang/OTP",
        "label": "Erlang/OTP",
        "url": "https://www.erlang.org/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "FMEA — Failure Mode and Effects Analysis": {
        "id": "FMEA — Failure Mode and Effects Analysis",
        "label": "FMEA — Failure Mode and Effects Analysis",
        "url": "https://en.wikipedia.org/wiki/Failure_mode_and_effects_analysis",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Antifragile (Taleb)": {
        "id": "Antifragile (Taleb)",
        "label": "Antifragile (Taleb)",
        "url": "https://www.penguinrandomhouse.com/books/176227/antifragile-by-nassim-nicholas-taleb/",
        "organization": "Penguin Random House",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },

    # ─── v38 Architecture Strategy references ───
    # Strategy principles
    "Wardley Mapping": {
        "id": "Wardley Mapping",
        "label": "Wardley Mapping",
        "url": "https://learnwardleymapping.com/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Wardley Map (overview)": {
        "id": "Wardley Map (overview)",
        "label": "Wardley Map (overview)",
        "url": "https://en.wikipedia.org/wiki/Wardley_map",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Good Strategy / Bad Strategy (Rumelt)": {
        "id": "Good Strategy / Bad Strategy (Rumelt)",
        "label": "Good Strategy / Bad Strategy (Rumelt)",
        "url": "https://en.wikipedia.org/wiki/Good_Strategy_Bad_Strategy",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Good Strategy / Bad Strategy (publisher)": {
        "id": "Good Strategy / Bad Strategy (publisher)",
        "label": "Good Strategy / Bad Strategy (publisher)",
        "url": "https://profilebooks.com/work/good-strategy-bad-strategy/",
        "organization": "Profile Books",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Continuous Architecture in Practice": {
        "id": "Continuous Architecture in Practice",
        "label": "Continuous Architecture in Practice",
        "url": "https://www.oreilly.com/library/view/continuous-architecture-in/9780136523710/",
        "organization": "O'Reilly",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Playing to Win (HBS)": {
        "id": "Playing to Win (HBS)",
        "label": "Playing to Win (HBS)",
        "url": "https://www.hbs.edu/faculty/Pages/item.aspx?num=44469",
        "organization": "Harvard",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Modernization strategy
    "Application Portfolio Management": {
        "id": "Application Portfolio Management",
        "label": "Application Portfolio Management",
        "url": "https://en.wikipedia.org/wiki/Application_portfolio_management",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # AI readiness
    "McKinsey — The State of AI": {
        "id": "McKinsey — The State of AI",
        "label": "McKinsey — The State of AI",
        "url": "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai",
        "organization": "McKinsey",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "AI Transformation Playbook (Landing AI)": {
        "id": "AI Transformation Playbook (Landing AI)",
        "label": "AI Transformation Playbook (Landing AI)",
        "url": "https://landing.ai/ai-transformation-playbook",
        "organization": "Landing AI",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "CRISP-DM": {
        "id": "CRISP-DM",
        "label": "CRISP-DM",
        "url": "https://en.wikipedia.org/wiki/Cross-industry_standard_process_for_data_mining",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Google AI Adoption Framework": {
        "id": "Google AI Adoption Framework",
        "label": "Google AI Adoption Framework",
        "url": "https://services.google.com/fh/files/misc/ai_adoption_framework_whitepaper.pdf",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Cross-cutting
    "DORA Capabilities Catalog": {
        "id": "DORA Capabilities Catalog",
        "label": "DORA Capabilities Catalog",
        "url": "https://dora.dev/capabilities/",
        "organization": "DORA",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    # Scorecards / assessment frameworks
    "ISO/IEC 25010 (Software Quality Model)": {
        "id": "ISO/IEC 25010 (Software Quality Model)",
        "label": "ISO/IEC 25010 (Software Quality Model)",
        "url": "https://iso25000.com/index.php/en/iso-25000-standards/iso-25010",
        "organization": "ISO",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "arc42 Architecture Template": {
        "id": "arc42 Architecture Template",
        "label": "arc42 Architecture Template",
        "url": "https://arc42.org/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Architecture Tradeoff Analysis Method (Wikipedia)": {
        "id": "Architecture Tradeoff Analysis Method (Wikipedia)",
        "label": "Architecture Tradeoff Analysis Method (Wikipedia)",
        "url": "https://en.wikipedia.org/wiki/Architecture_tradeoff_analysis_method",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ATAM at SEI": {
        "id": "ATAM at SEI",
        "label": "ATAM at SEI",
        "url": "https://insights.sei.cmu.edu/library/atam-criteria-evaluation-of-software-and-system-architectures/",
        "organization": "SEI",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "CISQ Software Quality Standards": {
        "id": "CISQ Software Quality Standards",
        "label": "CISQ Software Quality Standards",
        "url": "https://www.it-cisq.org/standards/",
        "organization": "CISQ",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Quality Attribute Workshop (SEI)": {
        "id": "Quality Attribute Workshop (SEI)",
        "label": "Quality Attribute Workshop (SEI)",
        "url": "https://insights.sei.cmu.edu/library/quality-attribute-workshop-third-edition-participants-handbook/",
        "organization": "SEI",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "TOGAF (overview)": {
        "id": "TOGAF (overview)",
        "label": "TOGAF (overview)",
        "url": "https://en.wikipedia.org/wiki/The_Open_Group_Architecture_Framework",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Capability Maturity Model Integration (CMMI)": {
        "id": "Capability Maturity Model Integration (CMMI)",
        "label": "Capability Maturity Model Integration (CMMI)",
        "url": "https://en.wikipedia.org/wiki/Capability_Maturity_Model_Integration",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "C4 Model": {
        "id": "C4 Model",
        "label": "C4 Model",
        "url": "https://c4model.com/",
        "organization": "Unknown",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Architecture Decision Records (ADR community)": {
        "id": "Architecture Decision Records (ADR community)",
        "label": "Architecture Decision Records (ADR community)",
        "url": "https://adr.github.io/",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Web Vitals (Google)": {
        "id": "Web Vitals (Google)",
        "label": "Web Vitals (Google)",
        "url": "https://web.dev/articles/vitals",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Google SRE Workbook — SLOs": {
        "id": "Google SRE Workbook — SLOs",
        "label": "Google SRE Workbook — SLOs",
        "url": "https://sre.google/workbook/implementing-slos/",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Active Reviews for Intermediate Designs (ARID)": {
        "id": "Active Reviews for Intermediate Designs (ARID)",
        "label": "Active Reviews for Intermediate Designs (ARID)",
        "url": "https://insights.sei.cmu.edu/library/active-reviews-for-intermediate-designs-arid/",
        "organization": "SEI",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Software Architecture Analysis Method (SAAM)": {
        "id": "Software Architecture Analysis Method (SAAM)",
        "label": "Software Architecture Analysis Method (SAAM)",
        "url": "https://en.wikipedia.org/wiki/Software_Architecture_Analysis_Method",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ISO/IEC/IEEE 42010 (Architecture description)": {
        "id": "ISO/IEC/IEEE 42010 (Architecture description)",
        "label": "ISO/IEC/IEEE 42010 (Architecture description)",
        "url": "https://en.wikipedia.org/wiki/ISO/IEC/IEEE_42010",
        "organization": "Wikipedia",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Microsoft Azure Well-Architected Framework": {
        "id": "Microsoft Azure Well-Architected Framework",
        "label": "Microsoft Azure Well-Architected Framework",
        "url": "https://learn.microsoft.com/en-us/azure/well-architected/",
        "organization": "Microsoft",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Google Cloud Architecture Framework": {
        "id": "Google Cloud Architecture Framework",
        "label": "Google Cloud Architecture Framework",
        "url": "https://cloud.google.com/architecture/framework",
        "organization": "Google",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "ThoughtWorks Technology Radar": {
        "id": "ThoughtWorks Technology Radar",
        "label": "ThoughtWorks Technology Radar",
        "url": "https://www.thoughtworks.com/radar",
        "organization": "ThoughtWorks",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },
    "Architecture Decision Records (ADR GitHub Org)": {
        "id": "Architecture Decision Records (ADR GitHub Org)",
        "label": "Architecture Decision Records (ADR GitHub Org)",
        "url": "https://adr.github.io/",
        "organization": "GitHub",
        "license": "link-only",
        "last_verified": "2026-04-30",
        "summary": "",
        "summary_author": "Platform Engineering",
        "summary_date": "2026-04-30",
    },

}


# Backwards-compat shim — preserves existing call sites that read TAG_LINKS[label] -> url.
# Remove in EPIC-3 once all call sites consume GOLD_REFERENCES directly.
TAG_LINKS = {k: v["url"] for k, v in GOLD_REFERENCES.items()}


# ─────────────────────────────────────────────────────────────────────────────
# LINK SECURITY — convention enforced at build time
#
# Convention: "Every hyperlink in every page and content must be verified
# that it is secure to access."
#
# The build verifier below walks every URL referenced by the site (TAG_LINKS
# values, plus every markdown hyperlink inside every README) and rejects:
#   1. Any URL not using https:// — http and other schemes are insecure
#   2. Any URL whose host is on KNOWN_INSECURE_DOMAINS — domains we have
#      manually verified to be serving invalid TLS certificates or browser
#      security warnings
#
# When a new bad-cert domain is reported, add it to the blocklist below and
# the next build will fail until the URL is replaced. Replacement is always
# preferred over removal — Wikipedia is the safe fallback for any concept
# that lacks a working canonical reference.
# ─────────────────────────────────────────────────────────────────────────────

KNOWN_INSECURE_DOMAINS = {
    # Domains observed serving invalid/expired TLS certificates or otherwise
    # triggering browser security warnings. Add new ones here as reported.
    "alistair.cockburn.us",
}


def verify_link_security(content_root):
    """Walk every URL in the site and fail the build if any is insecure.
    Runs before generation so we never publish insecure links."""
    issues = []
    seen = set()

    def check(url, where):
        if url in seen:
            return
        seen.add(url)
        if not url.startswith("https://"):
            issues.append(f"non-HTTPS URL: {url}\n      (in {where})")
            return
        # Pull out the host and lowercase it for blocklist comparison
        try:
            host = url.split("/", 3)[2].split(":")[0].lower()
        except IndexError:
            return
        if host in KNOWN_INSECURE_DOMAINS:
            issues.append(
                f"known-insecure host {host!r}: {url}\n      (in {where})"
            )

    # 1. Check every URL in TAG_LINKS
    for tag, url in TAG_LINKS.items():
        check(url, f"TAG_LINKS[{tag!r}]")

    # 2. Check every markdown hyperlink in every README
    md_link_re = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
    for readme in sorted(content_root.rglob("README.md")):
        text = readme.read_text(encoding="utf-8")
        rel = readme.relative_to(content_root)
        for match in md_link_re.finditer(text):
            label = match.group(1).strip()[:60]
            check(match.group(2), f"{rel} — '{label}'")

    if issues:
        print("\n!!! LINK SECURITY VIOLATIONS — build halted !!!")
        print(f"!!! Convention: every hyperlink must use https:// and not be on the")
        print(f"!!! KNOWN_INSECURE_DOMAINS blocklist in tools/generate.py.\n")
        for n, issue in enumerate(issues, 1):
            print(f"  {n}. {issue}")
        print()
        sys.exit(1)
    print(f"  ✓ link security: {len(seen)} unique URLs verified secure")


def tag_url(tag, prefix="../../"):
    """Resolve a tag chip to a URL.
    Returns (url, is_external). If unresolvable, returns (None, False)."""
    t = tag.strip()
    if t in TAG_LINKS:
        return (TAG_LINKS[t], True)
    # Path-shaped tag like 'principles/' or 'ai-native/'
    if t.endswith("/") and "/" in t:
        path = t.rstrip("/")
        if "/" in path:
            return (f"{prefix}{path}/index.html", False)
        return (f"{prefix}{path}/index.html", False)
    if t.endswith("/"):
        return (f"{prefix}{t}index.html", False)
    return (None, False)


# ─────────────────────────────────────────────────────────────────────────────
# HTML COMPONENTS
# ─────────────────────────────────────────────────────────────────────────────

WORDMARK_JS = """<script>
(function(){
  // ─── Header wordmark animation ─────────────────────────────────
  // Animate the header brand letter-by-letter. Spaces converted to
  // U+00A0 (nbsp) because display:inline-block collapses whitespace
  // inside the .wm-char spans.
  var nav = document.getElementById('nav-wm');
  if (nav) {
    var html = '';
    var i = 0;
    nav.textContent.split('').forEach(function(ch){
      var safe = ch === ' '
        ? '\\u00a0'
        : ch.replace('&','&amp;').replace('<','&lt;');
      html += '<span class="wm-char" style="animation-delay:' + (i * 26) + 'ms">' +
        safe + '</span>';
      i++;
    });
    nav.innerHTML = html;
  }

  // ─── Flip cards (principles + pitfalls) ──────────────────────────
  // Click anywhere on the card — except an internal link — to toggle.
  // Keyboard: Enter or Space toggles. Esc unflips.
  // Card height is dynamically set to the visible face's height,
  // so the card grows when content is taller and shrinks when shorter.
  document.querySelectorAll('.flip-card').forEach(function(card){
    var frontInner = card.querySelector('.flip-card-front-inner');
    var backInner  = card.querySelector('.flip-card-back-inner');
    if (!frontInner || !backInner) return;

    function measure(el) {
      // Add the card face's vertical padding (1.6rem top + 1.4rem bottom ≈ 48px)
      return el.offsetHeight + 48;
    }
    function applyHeight() {
      var face = card.classList.contains('is-flipped') ? backInner : frontInner;
      card.style.height = measure(face) + 'px';
    }
    requestAnimationFrame(function(){
      requestAnimationFrame(applyHeight);
    });
    var resizeTimer;
    window.addEventListener('resize', function(){
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(applyHeight, 100);
    });

    function toggle() {
      var flipped = card.classList.toggle('is-flipped');
      card.setAttribute('aria-pressed', flipped ? 'true' : 'false');
      applyHeight();
    }
    card.addEventListener('click', function(e){
      if (e.target.closest('a')) return;

      // Special case for adoption-checklist cards: if the user clicked
      // the checkbox specifically, toggle its visual state. The card
      // still flips below (per spec: 'flip on click of the record OR
      // when the tick mark is checked').
      var checkbox = e.target.closest('.check-card-checkbox');
      if (checkbox) {
        var checked = checkbox.getAttribute('data-checked') === 'true';
        checkbox.setAttribute('data-checked', checked ? 'false' : 'true');
        checkbox.textContent = checked ? '☐' : '☑';
      }

      toggle();
    });
    card.addEventListener('keydown', function(e){
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggle();
      } else if (e.key === 'Escape' && card.classList.contains('is-flipped')) {
        toggle();
      }
    });
  });

  // ─── Footer click → smooth scroll to top of page ─────────────────
  // The entire footer is the click target.
  var footer = document.querySelector('.footer');
  if (footer) {
    function scrollTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    footer.addEventListener('click', function(e){
      if (e.target.closest('a')) return;  // let internal links work
      e.preventDefault();
      scrollTop();
    });
    footer.addEventListener('keydown', function(e){
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        scrollTop();
      }
    });
  }
})();
</script>"""


# ─────────────────────────────────────────────────────────────────────────────
# KNOWLEDGE GRAPH — build-time metadata collection
# ─────────────────────────────────────────────────────────────────────────────

def is_substantive_readme(text):
    """True if README has the canonical full-page structure (not a stub).
    A page is substantive iff it has either Six principles or any diagram-section
    heading — both signals indicate an authored, full-template page. The diagram
    heading text varies by diagram type (Flowchart, Mind Map, Quadrant Chart,
    State Diagram, Class Diagram, Sequence Diagram, Timeline, Gantt Chart,
    User Journey, Entity Relationship Diagram, Git Graph, Architecture Diagram)
    so we match by the structural marker '## ' followed by any of the known
    diagram-section titles."""
    if "## Six principles" in text:
        return True
    for title in _ALL_DIAGRAM_SECTION_TITLES:
        if f"## {title}" in text:
            return True
    return False


# Mermaid type token (first non-blank line, first token) → human-readable title.
# Used for the diagram section heading on each page.
_DIAGRAM_TYPE_TO_TITLE = {
    "flowchart":      "Flowchart",
    "graph":          "Flowchart",
    "stateDiagram":   "State Diagram",
    "stateDiagram-v2": "State Diagram",
    "classDiagram":   "Class Diagram",
    "sequenceDiagram": "Sequence Diagram",
    "timeline":       "Timeline",
    "mindmap":        "Mind Map",
    "gantt":          "Gantt Chart",
    "quadrantChart":  "Quadrant Chart",
    "journey":        "User Journey",
    "userJourney":    "User Journey",
    "erDiagram":      "Entity Relationship Diagram",
    "gitGraph":       "Git Graph",
    "C4Context":      "C4 Context Diagram",
    "C4Container":    "C4 Container Diagram",
    "C4Component":    "C4 Component Diagram",
    "block-beta":     "Block Diagram",
    "pie":            "Pie Chart",
    "requirementDiagram": "Requirement Diagram",
    "sankey-beta":    "Sankey Diagram",
}

_ALL_DIAGRAM_SECTION_TITLES = sorted(set(list(_DIAGRAM_TYPE_TO_TITLE.values()) + ["Architecture Diagram"]))


def _diagram_type_to_title(mmd_text):
    """Derive the diagram-section H2 heading from the Mermaid source's first
    non-blank, non-comment line. Returns 'Architecture Diagram' as a generic
    fallback for unknown diagram types or empty/malformed input."""
    if not mmd_text:
        return "Architecture Diagram"
    for line in mmd_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("%%") or stripped.startswith("---"):
            continue
        # First word of the first content line is the diagram type token
        first_token = stripped.split()[0] if stripped.split() else ""
        return _DIAGRAM_TYPE_TO_TITLE.get(first_token, "Architecture Diagram")
    return "Architecture Diagram"


def _extract_alignment_list(text):
    """Pull the alignment chips from the **Alignment:** line."""
    m = re.search(r"\*\*Alignment:\*\*\s*(.+)", text)
    if not m:
        return []
    return [a.strip() for a in m.group(1).split("|") if a.strip()]


def _extract_related_paths(text):
    """Pull internal page paths from the ## Related section.
    Returns paths like 'principles/ai-native' (no trailing slash)."""
    m = re.search(r"## Related\s*\n+(.*?)(?=\n##|\Z)", text, re.DOTALL)
    if not m:
        return []
    block = m.group(1)
    # Look for relative paths: (../../section/subsection) or (../../section/subsection/)
    paths = re.findall(r"\(\.\./\.\./([^)]+?)/?\)", block)
    return paths


def _short_description(text):
    """Get a 1-2 sentence description from just below the H1."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            # Look for first non-blank line after H1 that isn't a metadata marker
            for j in range(i + 1, min(i + 8, len(lines))):
                ln = lines[j].strip()
                if ln and not ln.startswith("**") and not ln.startswith("---"):
                    return ln[:240]
    return ""


def collect_site_metadata(content_root):
    """Walk the content tree, parse each README, return a dict mapping
    'section/subsection' -> {title, section, is_substantive, alignments,
    related_links, description}. Used by both the knowledge-graph generator
    and the per-page 'Referenced by' injector."""
    metadata = {}
    for section_dir in sorted(content_root.iterdir()):
        if not section_dir.is_dir():
            continue
        section_slug = section_dir.name
        registered_subs = TAXONOMY.get(section_slug, {})
        for sub_dir in sorted(section_dir.iterdir()):
            if not sub_dir.is_dir():
                continue
            if sub_dir.name not in registered_subs:
                continue  # orphan — skip
            readme = sub_dir / "README.md"
            if not readme.exists():
                continue
            text = readme.read_text(encoding="utf-8")
            title, _ = extract_title_desc(text)
            metadata[f"{section_slug}/{sub_dir.name}"] = {
                "section": section_slug,
                "subsection": sub_dir.name,
                "title": title or sub_dir.name.replace("-", " ").title(),
                "is_substantive": is_substantive_readme(text),
                "alignments": _extract_alignment_list(text),
                "related_links": [
                    p.strip() for p in _extract_related_paths(text)
                ],
                "description": _short_description(text),
            }
    return metadata


def compute_referenced_by(metadata):
    """For each page, find which OTHER substantive pages link to it via
    their Related section. Returns dict: page_id -> [list of referencing
    page_ids]. Only substantive pages contribute incoming links (stubs
    aren't authored content yet, so their auto-generated Related sections
    don't count as deliberate cross-references)."""
    refs = {pid: [] for pid in metadata}
    for source_id, meta in metadata.items():
        if not meta["is_substantive"]:
            continue
        for target in meta["related_links"]:
            if target in refs and target != source_id:
                refs[target].append(source_id)
    return refs


def compute_graph_data(metadata):
    """Build the nodes/edges JSON for the D3 force-directed graph.

    Inclusion rules (Level 1 — start small, grow automatically):
      - Substantive pages → page nodes (always included).
      - Standards/concepts referenced via **Alignment:** by any substantive
        page → standard nodes.
      - Related-section links between substantive pages → edges.
    Stubs are NOT included. As stub pages gain real content, they
    automatically begin appearing in the graph on the next build."""
    nodes = {}
    edges = []
    substantive_ids = {pid for pid, m in metadata.items() if m["is_substantive"]}
    sorted_substantive = sorted(substantive_ids)

    # Reverse index: page_id → [lens_id, ...] for lens annotation on page nodes.
    page_lenses = {}
    for lens_id, lens in CONCEPT_LENSES.items():
        for member_id in lens["members"]:
            page_lenses.setdefault(member_id, []).append(lens_id)

    # 1) Add page nodes for all substantive pages
    for pid in sorted_substantive:
        m = metadata[pid]
        nodes[pid] = {
            "id": pid,
            "label": m["title"],
            "section": m["section"],
            "type": "page",
            "url": f"/{pid}/",
            "description": m["description"],
            "lenses": page_lenses.get(pid, []),
        }

    # 2) Add standard/concept nodes from alignments + alignment edges
    for pid in sorted_substantive:
        for tag in metadata[pid]["alignments"]:
            tag_id = f"tag:{tag}"
            if tag_id not in nodes:
                nodes[tag_id] = {
                    "id": tag_id,
                    "label": tag,
                    "type": "standard",
                    "url": TAG_LINKS.get(tag, ""),
                    "description": "",
                }
            edges.append({"source": pid, "target": tag_id, "kind": "alignment"})

    # 3) Add related-page edges (both endpoints must be substantive)
    for pid in sorted_substantive:
        for target in metadata[pid]["related_links"]:
            if target in substantive_ids and target != pid:
                edges.append({"source": pid, "target": target, "kind": "related"})

    # 4) Add section nodes — derived from already-emitted page nodes
    #    (EPIC-4 T4.1: section nodes + contains-edges).
    substantive_sections = sorted({
        n["id"].split("/")[0]
        for n in nodes.values()
        if n["type"] == "page"
    })
    for section_id in substantive_sections:
        title, description = SECTIONS.get(section_id, (section_id.title(), ""))
        nodes[section_id] = {
            "id": section_id,
            "type": "section",
            "label": title,
            "description": description,
        }

    # 5) Add contains-edges: one per substantive page (section → page).
    for pid in sorted_substantive:
        edges.append({
            "source": pid.split("/")[0],
            "target": pid,
            "kind": "contains",
        })

    # Final sort guarantees byte-deterministic output across runs.
    sorted_nodes = sorted(nodes.values(), key=lambda n: n["id"])
    sorted_edges = sorted(edges, key=lambda e: (e["source"], e["target"], e["kind"]))
    return {"nodes": sorted_nodes, "links": sorted_edges}


def nav_html(prefix, active=""):
    links = ""
    for label, href in NAV_LINKS:
        key = href.split("/")[0]
        cls = ' class="active"' if key == active else ""
        links += f'    <a href="{prefix}{href}"{cls}>{label}</a>\n'
    return (
        f'<nav class="nav">\n'
        f'  <a href="{prefix}index.html" class="nav-brand" aria-label="Ascendion Engineering — home">\n'
        f'    <img class="brand-logo" src="{prefix}logo.png" alt="" aria-hidden="true">\n'
        f'    <span class="nav-wordmark" id="nav-wm">Ascendion Engineering</span>\n'
        f'  </a>\n'
        f'  <div class="nav-sep"></div>\n'
        f'  <div class="nav-links">\n{links}  </div>\n'
        f'  <a href="{prefix}knowledge-graph/" class="nav-cta">Knowledge Graph</a>\n'
        f'  <a href="{prefix}index.html#topics" class="nav-cta">All Topics</a>\n'
        f'</nav>'
    )


def footer_html(label="", prefix=""):
    return (
        f'<footer class="footer" role="button" tabindex="0" '
        f'aria-label="Scroll to top of page">\n  <div class="shell">\n'
        f'    <img class="footer-logo" src="{prefix}footer-logo.png" alt="" aria-hidden="true">\n'
        f'    <div class="footer-meta">© 2025 Ascendion Solutions Architecture Practice</div>\n'
        f'  </div>\n</footer>'
    )


def head(title, css, has_mermaid=False):
    m = ""
    if has_mermaid:
        m = (f'  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>\n'
             f'  <script>mermaid.initialize({MERMAID_INIT});</script>\n')
    return (
        f'<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        f'  <meta charset="UTF-8">\n'
        f'  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'  <title>{title}</title>\n'
        f'  <link rel="icon" type="image/x-icon" href="{css}favicon.ico">\n'
        f'  <link rel="icon" type="image/png" sizes="32x32" href="{css}favicon-32.png">\n'
        f'  <link rel="stylesheet" href="{css}shared.css">\n'
        f'{m}</head>\n<body>\n'
        f'<a class="skip-link" href="#main">Skip to main content</a>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE GENERATORS
# ─────────────────────────────────────────────────────────────────────────────

def gen_root(src, out):
    total_s = len([s for s in SECTIONS if (src / s).exists()])
    total_sub = sum(
        sum(
            1 for d in (src / s).iterdir()
            if d.is_dir()
            and d.name in TAXONOMY.get(s, {})
            and (d / "README.md").exists()
        )
        for s in SECTIONS if (src / s).exists()
    )

    # Filter tabs — one per group
    filter_html = '<a href="#topics" class="filter-tag active">All</a>\n'
    for gname, _, gslugs in GROUPS:
        first = next((s for s in gslugs if (src / s).exists()), None)
        if first:
            filter_html += f'    <a href="#{gname.lower().replace(" & ","").replace(" ","")}" class="filter-tag">{gname}</a>\n'

    # Groups + cards
    groups_html = ""
    for gname, gdesc, gslugs in GROUPS:
        gid = gname.lower().replace(" & ", "").replace(" ", "")
        cards = ""
        for slug in gslugs:
            if slug not in SECTIONS or not (src / slug).exists(): continue
            title, desc = SECTIONS[slug]
            svg = SVGS.get(slug, "")
            cards += (
                f'    <a href="{slug}/index.html" class="section-card">\n'
                f'      <div class="sc-illustration">{svg}</div>\n'
                f'      <div class="sc-path">{slug}/</div>\n'
                f'      <div class="sc-title">{title}</div>\n'
                f'      <div class="sc-desc">{desc}</div>\n'
                f'      <div class="sc-footer"><span class="sc-arrow">&#8594;</span></div>\n'
                f'    </a>\n'
            )
        groups_html += (
            f'<div class="group-section shell" id="{gid}">\n'
            f'  <div class="group-label">{gname} '
            f'<span class="group-label-desc">{gdesc}</span></div>\n'
            f'  <div class="section-grid">\n{cards}  </div>\n'
            f'</div>\n\n'
        )

    html = (
        f'{head("Ascendion Engineering — Architecture Best-Practice Library", "")}\n\n'
        f'{nav_html("", "")}\n\n'
        f'<main id="main">\n'
        f'<section class="hero">\n  <div class="shell">\n'
        f'    <div class="hero-label">Ascendion Solutions Architecture Practice</div>\n'
        f'    <h1><strong>Architecture</strong><br>Best-Practice Library</h1>\n'
        f'    <p class="hero-desc">Practitioner-grade architecture guidance, patterns, and '
        f'frameworks — aligned to TOGAF, NIST CSF, ISO 27001, and AWS Well-Architected.</p>\n'
        f'  </div>\n</section>\n\n'
        f'<div class="filter-bar"><div class="shell">{filter_html}</div></div>\n\n'
        f'<div class="shell"><div class="stats-row" id="topics">\n'
        f'  <div><div class="stat-n">{total_s}</div><div class="stat-l">Domains</div></div>\n'
        f'  <div><div class="stat-n">{total_sub}</div><div class="stat-l">Subsections</div></div>\n'
        f'  <div><div class="stat-n">408</div><div class="stat-l">Documents</div></div>\n'
        f'</div></div>\n\n'
        f'{groups_html}'
        f'</main>\n\n'
        f'{footer_html()}\n\n'
        f'{WORDMARK_JS}\n</body>\n</html>'
    )
    (out / "index.html").write_text(html, encoding="utf-8")
    print(f"  ✓ index.html")


def gen_section(slug, src_dir, out_dir):
    title, desc = SECTIONS.get(slug, (slug.title(), ""))

    # STRICT: only render subsections registered in TAXONOMY. Orphan
    # directories left behind from prior seeds are skipped with a warning,
    # not silently rendered. The TAXONOMY is the single source of truth.
    registered = TAXONOMY.get(slug, {})
    subs = []
    found_dirs = sorted(d.name for d in src_dir.iterdir() if d.is_dir())
    orphans = [name for name in found_dirs if name not in registered]
    if orphans:
        for name in orphans:
            print(f"  ⚠ orphan directory skipped: content/{slug}/{name}/ (not in TAXONOMY) — delete this directory to clean up the repo")

    for d in sorted(src_dir.iterdir()):
        if not d.is_dir():
            continue
        if d.name not in registered:
            continue  # orphan — skip
        if not (d / "README.md").exists():
            continue
        t, de = extract_title_desc((d / "README.md").read_text(encoding="utf-8"))
        subs.append((d.name, t, de))

    rows = ""
    for sub_slug, sub_title, sub_desc in subs:
        rows += (
            f'  <a href="{sub_slug}/index.html" class="article-row">\n'
            f'    <div>\n'
            f'      <div class="ar-label">{slug}/{sub_slug}/</div>\n'
            f'      <div class="ar-title">{sub_title}</div>\n'
            f'      <div class="ar-desc">{sub_desc or "&nbsp;"}</div>\n'
            f'    </div>\n'
            f'    <div class="ar-arrow">&#8594;</div>\n'
            f'  </a>\n'
        )

    # Title weight contrast
    words = title.split()
    h1 = f"<strong>{words[0]}</strong><br>{'  '.join(words[1:])}" if len(words) > 1 else f"<strong>{title}</strong>"

    # Section hero SVG — scaled up for hero display
    svg_art = SVGS.get(slug, "")

    html = (
        f'{head(f"{title} — Ascendion Engineering", "../")}\n\n'
        f'{nav_html("../", slug)}\n\n'
        f'<main id="main">\n'
        f'<section class="hero-section">\n  <div class="shell">\n'
        f'    <div class="hero-section-inner">\n'
        f'      <div class="hero-section-text">\n'
        f'        <div class="breadcrumb"><a href="../index.html">Home</a>'
        f'<span class="sep">›</span><span class="curr">{title}</span></div>\n'
        f'        <div class="hero-label">{slug}/</div>\n'
        f'        <h1>{h1}</h1>\n'
        f'        <p class="hero-desc">{desc}</p>\n'
        f'      </div>\n'
        f'      <div class="hero-section-art">{svg_art}</div>\n'
        f'    </div>\n'
        f'  </div>\n</section>\n\n'
        f'<div class="shell">\n'
        f'  <div class="article-list">\n'
        f'    <div class="list-label">{len(subs)} topics in this section</div>\n'
        f'{rows}  </div>\n</div>\n'
        f'</main>\n\n'
        f'{footer_html(f"{slug}/", prefix="../")}\n\n'
        f'{WORDMARK_JS}\n</body>\n</html>'
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"  ✓ {slug}/index.html")


def gen_article(slug, sub_slug, sub_dir, out_sub, referenced_by=None, metadata=None):
    readme = sub_dir / "README.md"
    diagram = sub_dir / "diagram.mmd"
    hero_svg_file = sub_dir / "hero.svg"
    md_text = readme.read_text(encoding="utf-8")
    title, desc = extract_title_desc(md_text)
    tags = extract_tags(md_text)
    body = md_to_html(md_text)
    sec_title = SECTIONS.get(slug, (slug.title(),))[0]
    has_d = diagram.exists()
    has_hero_art = hero_svg_file.exists()

    tag_html = ""
    if tags:
        tag_items = []
        for t in tags:
            url, external = tag_url(t, prefix="../../")
            if url:
                tgt = ' target="_blank" rel="noopener noreferrer"' if external else ''
                tag_items.append(f'<a class="hero-tag" href="{url}"{tgt}>{t}</a>')
            else:
                # Unknown tag — render as plain chip (not interactive)
                tag_items.append(f'<span class="hero-tag hero-tag-static">{t}</span>')
        tag_html = '<div class="hero-tags">' + "".join(tag_items) + "</div>"

    diag_wrap_html = ""
    if has_d:
        mmd = diagram.read_text(encoding="utf-8").replace("&", "&amp;")
        diag_wrap_html = (
            f'<div class="diagram-wrap"><div class="mermaid">\n{mmd}\n  </div></div>\n'
        )

    # Hero structure: text on the left, optional animated SVG on the right.
    # Note: removed duplicate <div class="hero-label"> — breadcrumb already
    # carries the path information.
    hero_text = (
        f'    <div class="breadcrumb"><a href="../../index.html">Home</a>'
        f'<span class="sep">›</span>'
        f'<a href="../index.html">{sec_title}</a>'
        f'<span class="sep">›</span>'
        f'<span class="curr">{title}</span></div>\n'
        f'    <h1>{title}</h1>\n'
        f'    <p class="hero-desc">{desc}</p>\n'
        f'    {tag_html}\n'
    )

    if has_hero_art:
        hero_svg = hero_svg_file.read_text(encoding="utf-8")
        hero_block = (
            f'<section class="hero-article">\n  <div class="shell">\n'
            f'    <div class="hero-article-inner">\n'
            f'      <div class="hero-article-text">\n{hero_text}'
            f'      </div>\n'
            f'      <div class="hero-article-art">{hero_svg}</div>\n'
            f'    </div>\n'
            f'  </div>\n</section>\n\n'
        )
    else:
        hero_block = (
            f'<section class="hero-article">\n  <div class="shell">\n'
            f'{hero_text}'
            f'  </div>\n</section>\n\n'
        )

    # Diagram placement strategy:
    #   1. Derive the diagram-section title from the Mermaid source (e.g.
    #      "Flowchart", "State Diagram", "Quadrant Chart"). Falls back to
    #      "Architecture Diagram" for unknown types or if there is no diagram.
    #   2. If README already contains an H2 matching ANY known diagram-section
    #      title (the dynamic title or any prior title), insert wrap right after it
    #      AND rewrite that H2 to the current dynamic title (so existing
    #      "Architecture Diagram" headings get auto-upgraded to type-specific
    #      headings on rebuild).
    #   3. Otherwise, fall back to inserting "<h2>{dynamic_title}</h2>" + wrap
    #      before "Related Sections" / "Related" / "References".
    if diag_wrap_html:
        diagram_title = _diagram_type_to_title(mmd)
        # Match ANY known diagram-section H2, not just "Architecture Diagram"
        any_diagram_h2_re = re.compile(
            r'<h2[^>]*>\s*(' +
            '|'.join(re.escape(t) for t in _ALL_DIAGRAM_SECTION_TITLES) +
            r')\s*</h2>',
            re.IGNORECASE)
        m = any_diagram_h2_re.search(body)
        if m:
            # Rewrite the H2 to the current dynamic title and insert wrap after it
            new_h2 = f'<h2>{diagram_title}</h2>'
            body = body[:m.start()] + new_h2 + body[m.end():]
            insert_at = m.start() + len(new_h2)
            body = body[:insert_at] + '\n' + diag_wrap_html + body[insert_at:]
        else:
            full_block = f'<h2>{diagram_title}</h2>\n' + diag_wrap_html
            body = _insert_before_heading(
                body, full_block,
                ['Related Sections', 'Related', 'References'])

    html = (
        f'{head(f"{title} — {sec_title} · Ascendion Engineering", "../../", has_d)}\n\n'
        f'{nav_html("../../", slug)}\n\n'
        f'<main id="main">\n'
        f'{hero_block}'
        f'<div class="shell">\n'
        f'  <div class="article-body">\n{body}\n'
        f'  </div>\n'
        f'</div>\n'
        f'</main>\n\n'
        f'{footer_html(f"{slug}/{sub_slug}/", prefix="../../")}\n\n'
        f'{WORDMARK_JS}\n</body>\n</html>'
    )
    # If this page has incoming references from other substantive pages,
    # inject a "Referenced by" section. Placed AFTER body construction but
    # BEFORE the final write — uses the metadata dict to render proper titles.
    if referenced_by and metadata:
        chips = []
        for ref_id in sorted(referenced_by):
            if ref_id not in metadata:
                continue
            ref_title = metadata[ref_id]["title"]
            chips.append(
                f'<a class="related-chip" href="../../{ref_id}/">{ref_title}</a>'
            )
        if chips:
            section = (
                '<hr>\n<h2 id="referenced-by">Referenced by</h2>\n'
                '<p class="referenced-by-intro">'
                'Other substantive pages in the library that link here:'
                '</p>\n'
                '<div class="related-chips-row referenced-by-chips">'
                + "".join(chips)
                + '</div>\n'
            )
            # Insert before <h2>References</h2>; fall back to before final
            # </div> of article-body if References doesn't exist.
            new_body = _insert_before_heading(body, section, ["References"])
            html = html.replace(body, new_body)

    out_sub.mkdir(parents=True, exist_ok=True)
    (out_sub / "index.html").write_text(html, encoding="utf-8")
    print(f"  ✓ {slug}/{sub_slug}/index.html")


def _insert_before_heading(body, insert_html, heading_titles):
    """Insert insert_html immediately before the first <h2> matching any of heading_titles.
    If no match, append at the end of body."""
    for ht in heading_titles:
        pattern = re.compile(rf'(<h2[^>]*>\s*{re.escape(ht)}\s*</h2>)', re.IGNORECASE)
        m = pattern.search(body)
        if m:
            return body[:m.start()] + insert_html + body[m.start():]
    return body + insert_html


# ─────────────────────────────────────────────────────────────────────────────
# KNOWLEDGE GRAPH PAGE GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

def gen_knowledge_graph_page(graph_data, out_root):
    """Generate /knowledge-graph/index.html with embedded graph JSON and a
    D3 force-directed visualisation. Header/footer match other pages.
    The graph contains only substantive pages and their referenced standards;
    new pages join automatically as they gain canonical content."""
    out_dir = out_root / "knowledge-graph"
    out_dir.mkdir(parents=True, exist_ok=True)

    graph_json = json.dumps(graph_data, ensure_ascii=False)
    page_count = sum(1 for n in graph_data["nodes"] if n.get("type") == "page")
    standard_count = sum(1 for n in graph_data["nodes"] if n.get("type") == "standard")

    head_html = head("Knowledge Graph — Ascendion Engineering", "../")
    nav = nav_html("../")
    foot = footer_html(prefix="../")

    body = f"""
{nav}
<main id="main">
  <div class="shell">
    <div class="article-hero">
      <div class="hero-row">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <a href="../index.html">Home</a>
          <span class="crumb-sep">›</span>
          <span class="crumb-current">Knowledge Graph</span>
        </nav>
      </div>
      <div class="hero-article">
        <div class="hero-article-text">
          <h1>Knowledge Graph</h1>
          <p>An interconnected map of substantive content across Ascendion Engineering.
          Pages, standards, and the relationships between them — turning the library
          into a navigable network rather than a stack of documents.</p>
          <div class="kg-summary">
            <span class="kg-summary-stat"><strong>{page_count}</strong> page{"s" if page_count != 1 else ""}</span>
            <span class="kg-summary-stat"><strong>{standard_count}</strong> standard{"s" if standard_count != 1 else ""}</span>
            <span class="kg-summary-stat"><strong>{len(graph_data["links"])}</strong> connection{"s" if len(graph_data["links"]) != 1 else ""}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="article-body">
      <div class="kg-shell">
        <div class="kg-controls">
          <div class="kg-legend">
            <div class="kg-legend-item">
              <span class="kg-legend-swatch kg-swatch-page"></span>
              <span>Substantive page</span>
            </div>
            <div class="kg-legend-item">
              <span class="kg-legend-swatch kg-swatch-standard"></span>
              <span>Standard / concept</span>
            </div>
            <div class="kg-legend-item">
              <span class="kg-legend-swatch kg-swatch-section"></span>
              <span>Topic group</span>
            </div>
            <div class="kg-legend-item">
              <span class="kg-legend-line kg-line-alignment"></span>
              <span>Alignment</span>
            </div>
            <div class="kg-legend-item">
              <span class="kg-legend-line kg-line-related"></span>
              <span>Related</span>
            </div>
          </div>
          <div class="kg-hint">Click a node to open · drag to rearrange · scroll to zoom</div>
        </div>
        <div class="kg-canvas-wrap">
          <svg id="kg-svg" role="img" aria-label="Knowledge graph visualization"></svg>
          <div id="kg-tooltip" class="kg-tooltip" aria-hidden="true"></div>
        </div>
        <p class="kg-note">
          Only pages with canonical, authored content appear in the graph today.
          Stub pages join automatically as they gain real content (Six principles,
          Architecture Diagram, etc.). Standards are linked to their primary
          public reference; clicking opens it in a new tab.
        </p>
      </div>
    </div>

  </div>
</main>
{foot}

<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script>
const GRAPH_DATA = {graph_json};

(function() {{
  const svg = d3.select('#kg-svg');
  const tooltip = document.getElementById('kg-tooltip');
  const wrap = document.querySelector('.kg-canvas-wrap');

  const width = 1100;
  const height = 620;
  svg.attr('viewBox', `0 0 ${{width}} ${{height}}`);

  // Container <g> for pan/zoom
  const root = svg.append('g').attr('class', 'kg-root');

  // Force simulation
  const simulation = d3.forceSimulation(GRAPH_DATA.nodes)
    .force('link', d3.forceLink(GRAPH_DATA.links)
      .id(d => d.id)
      .distance(d => d.kind === 'alignment' ? 110 : 160)
      .strength(0.4))
    .force('charge', d3.forceManyBody().strength(-420))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(d => {{
      if (d.type === 'page') return 36;
      if (d.type === 'section') return 30;
      return 24;
    }}));

  // Edges (lines)
  const link = root.append('g')
    .attr('class', 'kg-links')
    .selectAll('line')
    .data(GRAPH_DATA.links)
    .enter().append('line')
    .attr('class', d => 'kg-link kg-link-' + d.kind);

  // Nodes (groups containing circle + label)
  const node = root.append('g')
    .attr('class', 'kg-nodes')
    .selectAll('g')
    .data(GRAPH_DATA.nodes)
    .enter().append('g')
    .attr('class', d => 'kg-node kg-node-' + d.type)
    .call(d3.drag()
      .on('start', (event, d) => {{
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x; d.fy = d.y;
      }})
      .on('drag', (event, d) => {{
        d.fx = event.x; d.fy = event.y;
      }})
      .on('end', (event, d) => {{
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null; d.fy = null;
      }}));

  // Circles for pages, diamonds (rotated squares) for standards
  node.each(function(d) {{
    const sel = d3.select(this);
    if (d.type === 'page') {{
      sel.append('circle').attr('r', 14);
    }} else if (d.type === 'section') {{
      // hexagon at radius 14: 6 vertices on a flat-top regular hexagon
      const r = 14;
      const points = [];
      for (let i = 0; i < 6; i++) {{
        const angle = Math.PI / 3 * i; // 60° increments
        points.push((r * Math.cos(angle)).toFixed(2) + ',' + (r * Math.sin(angle)).toFixed(2));
      }}
      sel.append('polygon').attr('points', points.join(' '));
    }} else {{
      // diamond
      sel.append('rect')
        .attr('width', 8).attr('height', 8)
        .attr('x', -4).attr('y', -4)
        .attr('transform', 'rotate(45)');
    }}
  }});

  node.append('text')
    .attr('class', 'kg-label')
    .attr('dy', d => {{
      if (d.type === 'page') return 28;
      if (d.type === 'section') return 24;
      return 20;
    }})
    .attr('text-anchor', 'middle')
    .text(d => d.label);

  // Hover tooltips
  node.on('mouseenter', function(event, d) {{
    const desc = d.description || (d.type === 'standard'
      ? 'External standard or concept'
      : 'Substantive engineering library page');
    tooltip.innerHTML = `<strong>${{d.label}}</strong><br><span>${{desc}}</span>`;
    tooltip.style.opacity = '1';
    tooltip.setAttribute('aria-hidden', 'false');
  }}).on('mousemove', function(event) {{
    const rect = wrap.getBoundingClientRect();
    tooltip.style.left = (event.clientX - rect.left + 14) + 'px';
    tooltip.style.top = (event.clientY - rect.top + 14) + 'px';
  }}).on('mouseleave', function() {{
    tooltip.style.opacity = '0';
    tooltip.setAttribute('aria-hidden', 'true');
  }});

  // Click navigation
  node.on('click', function(event, d) {{
    if (event.defaultPrevented) return;  // ignore drag-end clicks
    if (!d.url) return;
    if (d.type === 'standard') {{
      window.open(d.url, '_blank', 'noopener');
    }} else {{
      window.location.href = '..' + d.url;
    }}
  }}).style('cursor', 'pointer');

  simulation.on('tick', () => {{
    link
      .attr('x1', d => d.source.x).attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
    node.attr('transform', d => `translate(${{d.x}},${{d.y}})`);
  }});

  // Pan & zoom
  svg.call(d3.zoom()
    .scaleExtent([0.5, 3])
    .on('zoom', event => root.attr('transform', event.transform)));
}})();
</script>
{WORDMARK_JS}
</body>
</html>
"""

    out_file = out_dir / "index.html"
    out_file.write_text(head_html + body, encoding="utf-8")
    print(f"  ✓ knowledge-graph/index.html "
          f"({page_count} pages, {standard_count} standards, "
          f"{len(graph_data['links'])} edges)")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="Ascendion Engineering site generator")
    p.add_argument("--src", default="./content",
                   help="Source content folder (default: ./content)")
    p.add_argument("--out", default="./dist",
                   help="Build output folder (default: ./dist)")
    p.add_argument("--clean", action="store_true",
                   help="Remove output folder before building")
    args = p.parse_args()

    src = Path(args.src).resolve()
    out = Path(args.out).resolve()

    if not src.exists():
        print(f"ERROR: not found: {src}"); sys.exit(1)

    if args.clean and out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    # Copy shared.css. Search relative to the generator script and to the repo root.
    here = Path(__file__).parent
    for candidate in [
        here.parent / "src" / "shared.css",      # tools/generate.py + src/shared.css
        here / "src" / "shared.css",              # generator and src/ co-located
        here / "shared.css",                      # generator next to css (legacy)
    ]:
        if candidate.exists():
            shutil.copy(candidate, out / "shared.css")
            print(f"  ✓ shared.css (from {candidate})")
            break
    else:
        print(f"  ! shared.css not found near {here}")
        sys.exit(1)

    # Copy brand assets (logo + favicons). Same search strategy as shared.css.
    # logo.png         — header brand mark (the A), transparent background
    # footer-logo.png  — footer wordmark (Ascendion), transparent background
    # favicon.ico      — multi-resolution browser tab icon
    # favicon-32.png   — modern browsers prefer PNG favicons
    for asset in ("logo.png", "footer-logo.png", "favicon.ico", "favicon-32.png"):
        for candidate in [
            here.parent / "src" / asset,
            here / "src" / asset,
            here / asset,
        ]:
            if candidate.exists():
                shutil.copy(candidate, out / asset)
                print(f"  ✓ {asset} (from {candidate})")
                break
        else:
            print(f"  ! {asset} not found near {here} (skipping)")

    print("\n── Generating v4 ─────────────────────────────────────────────")

    # Phase 0: Link security verification. Halts the build if ANY URL in
    # the site (TAG_LINKS or markdown hyperlinks in any README) is non-HTTPS
    # or on the known-insecure-domains blocklist. Convention enforced
    # mechanically so it can't be forgotten.
    verify_link_security(src)

    # Phase 1: Walk all content to collect metadata. We need this before
    # generating individual articles so each page knows which other pages
    # reference it (via Related sections in OTHER substantive pages).
    site_metadata = collect_site_metadata(src)
    referenced_by = compute_referenced_by(site_metadata)

    print("\n[root]")
    gen_root(src, out)

    for slug in sorted(SECTIONS):
        sd = src / slug
        if not sd.exists(): continue
        out_sec = out / slug
        registered_subs = TAXONOMY.get(slug, {})
        print(f"\n[{slug}/]")
        gen_section(slug, sd, out_sec)
        for sub in sorted(sd.iterdir()):
            if not sub.is_dir():
                continue
            if sub.name not in registered_subs:
                continue  # orphan — skip
            if not (sub / "README.md").exists():
                continue
            page_id = f"{slug}/{sub.name}"
            gen_article(
                slug, sub.name, sub, out_sec / sub.name,
                referenced_by=referenced_by.get(page_id, []),
                metadata=site_metadata,
            )

    # Phase 2: Generate the Knowledge Graph page from collected metadata.
    print(f"\n[knowledge-graph/]")
    graph_data = compute_graph_data(site_metadata)
    gen_knowledge_graph_page(graph_data, out)

    n = sum(1 for _ in out.rglob("*.html"))
    print(f"\n── Done: {n} pages → {out}\n")


if __name__ == "__main__":
    main()
