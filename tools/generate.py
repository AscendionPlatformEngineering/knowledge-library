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
  Future pages must invent a new mechanic, not reuse one.
  Two colours only: warm neutral (#D6D2C8) + terracotta (#C96330).
  Basic SMIL primitives only (animate, animateTransform with type=rotate).
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
     ["ai", "maturity", "scorecards", "strategy", "roadmaps", "playbooks", "templates"]),
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
    "security":      ("Security Architecture",                "End-to-end security design: AuthN/AuthZ, encryption, and cloud controls."),
    "compliance":    ("Compliance & Regulatory Frameworks",   "Standards mappings and compliance controls for enterprise environments."),
    "governance":    ("Architecture Governance",              "Governance structures, review boards, and decision workflows."),
    "nfr":           ("Non-Functional Requirements",          "Performance, availability, scalability, and security NFR evaluation."),
    "data":          ("Data Architecture",                    "Data modeling, governance, lineage, mesh patterns, and analytics."),
    "integration":   ("Integration Architecture",             "API, event, messaging, workflow, and partner integration patterns."),
    "observability": ("Observability",                        "Metrics, traces, logging, SLIs/SLOs, and SRE operational practices."),
    "tools":         ("Architecture Tooling",                 "Automation, validation, and architecture-as-code tooling."),
    "checklists":    ("Review Checklists",                    "Architecture, security, and deployment readiness checklists."),
    "runbooks":      ("Operational Runbooks",                 "Incident response, rollback, and migration runbooks."),
    "scorecards":    ("Architecture Scorecards",              "Scoring templates for continuous architecture quality measurement."),
    "maturity":      ("Architecture Maturity Models",         "Capability scoring and maturity criteria for engineering advancement."),
    "playbooks":     ("Engineering Playbooks",                "Step-by-step playbooks for common architecture challenges."),
    "strategy":      ("Architecture Strategy",                "AI readiness, modernization roadmaps, and foundational strategy."),
    "roadmaps":      ("Architecture Roadmaps",                "Platform evolution and capability uplift roadmaps."),
    "templates":     ("Architecture Templates",               "Reusable templates for ADRs, reviews, and scorecards."),
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
TAG_LINKS = {
    "TOGAF ADM": "https://en.wikipedia.org/wiki/The_Open_Group_Architecture_Framework",
    "NIST AI RMF": "https://www.nist.gov/itl/ai-risk-management-framework",
    "NIST CSF": "https://www.nist.gov/cyberframework",
    "ISO/IEC 42001": "https://learn.microsoft.com/en-us/compliance/regulatory/offering-iso-42001",
    "ISO 27001": "https://en.wikipedia.org/wiki/ISO/IEC_27001",
    "AWS Well-Architected ML Lens": "https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html",
    "AWS Well-Architected": "https://aws.amazon.com/architecture/well-architected/",
    "Domain-Driven Design": "https://en.wikipedia.org/wiki/Domain-driven_design",
    "Conway's Law": "https://en.wikipedia.org/wiki/Conway%27s_law",
    "BIAN": "https://bian.org/",
    "HL7 FHIR": "https://hl7.org/fhir/",
    "Team Topologies": "https://teamtopologies.com/",
    "SOLID": "https://en.wikipedia.org/wiki/SOLID",
    "Clean Architecture": "https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html",
    "Hexagonal Architecture": "https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)",
    "Strangler Fig Pattern": "https://martinfowler.com/bliki/StranglerFigApplication.html",
    "Continuous Delivery": "https://en.wikipedia.org/wiki/Continuous_delivery",
    "Twelve-Factor App": "https://12factor.net/",
    "CNCF Cloud Native": "https://github.com/cncf/toc/blob/main/DEFINITION.md",
    "Site Reliability Engineering": "https://sre.google/sre-book/table-of-contents/",
    "SLSA": "https://slsa.dev/",
    "CQRS Pattern": "https://martinfowler.com/bliki/CQRS.html",
    "Event Sourcing": "https://martinfowler.com/eaaDev/EventSourcing.html",
    "Polyglot Persistence": "https://martinfowler.com/bliki/PolyglotPersistence.html",
    "DORA Metrics": "https://dora.dev/",
    "Feature Toggles": "https://martinfowler.com/articles/feature-toggles.html",
    "Trunk-Based Development": "https://trunkbaseddevelopment.com/",
    "Enterprise Integration Patterns": "https://www.enterpriseintegrationpatterns.com/",
    "AsyncAPI": "https://www.asyncapi.com/",
    "OpenAPI": "https://www.openapis.org/",
    "CloudEvents": "https://cloudevents.io/",
    "OWASP": "https://owasp.org/",
    "Zero Trust Architecture": "https://csrc.nist.gov/publications/detail/sp/800-207/final",
    "GoF Design Patterns": "https://en.wikipedia.org/wiki/Design_Patterns",
    "Pattern-Oriented Software Architecture": "https://en.wikipedia.org/wiki/Pattern-Oriented_Software_Architecture",
    "ONNX": "https://onnx.ai/",
    "TensorFlow Lite": "https://www.tensorflow.org/lite",
    "Federated Learning": "https://en.wikipedia.org/wiki/Federated_learning",
    "Edge Computing": "https://en.wikipedia.org/wiki/Edge_computing",
    "Apache Kafka": "https://kafka.apache.org/",
    "ISO 22301": "https://en.wikipedia.org/wiki/ISO_22301",
    "Chaos Engineering": "https://principlesofchaos.org/",
    "AWS Well-Architected Reliability Pillar": "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html",
    "CAP Theorem": "https://en.wikipedia.org/wiki/CAP_theorem",
    "Reactive Manifesto": "https://www.reactivemanifesto.org/",
    # Frontend frameworks and UX
    "React": "https://react.dev/",
    "Angular": "https://angular.dev/",
    "Vue.js": "https://vuejs.org/",
    "Svelte": "https://svelte.dev/",
    "Web Vitals": "https://web.dev/articles/vitals",
    "Laws of UX": "https://lawsofux.com/",
    "WCAG": "https://www.w3.org/WAI/standards-guidelines/wcag/",
    "Material Design": "https://m3.material.io/",
    "Storybook": "https://storybook.js.org/",
    # Backend stacks
    "Spring Boot": "https://spring.io/projects/spring-boot",
    "Node.js": "https://nodejs.org/",
    "FastAPI": "https://fastapi.tiangolo.com/",
    "Django": "https://www.djangoproject.com/",
    "OpenAPI": "https://www.openapis.org/",
    "GraphQL": "https://graphql.org/",
    "gRPC": "https://grpc.io/",
    # Databases
    "PostgreSQL": "https://www.postgresql.org/",
    "MongoDB": "https://www.mongodb.com/",
    "Redis": "https://redis.io/",
    "Apache Cassandra": "https://cassandra.apache.org/",
    "Elasticsearch": "https://www.elastic.co/elasticsearch",
    "Neo4j": "https://neo4j.com/",
    "Snowflake": "https://www.snowflake.com/",
    "ClickHouse": "https://clickhouse.com/",
    "InfluxDB": "https://www.influxdata.com/",
    "Pinecone": "https://www.pinecone.io/",
    "pgvector": "https://github.com/pgvector/pgvector",
    # Cloud platforms
    "AWS": "https://aws.amazon.com/",
    "Microsoft Azure": "https://azure.microsoft.com/",
    "Google Cloud Platform": "https://cloud.google.com/",
    "AWS Well-Architected": "https://aws.amazon.com/architecture/well-architected/",
    "Azure Well-Architected Framework": "https://learn.microsoft.com/en-us/azure/well-architected/",
    "GCP Architecture Framework": "https://cloud.google.com/architecture/framework",
    "Terraform": "https://www.terraform.io/",
    "Pulumi": "https://www.pulumi.com/",
    # DevOps
    "GitHub Actions": "https://docs.github.com/en/actions",
    "GitLab CI": "https://docs.gitlab.com/ee/ci/",
    "Argo CD": "https://argo-cd.readthedocs.io/",
    "Flux CD": "https://fluxcd.io/",
    "OpenTelemetry": "https://opentelemetry.io/",
    "Prometheus": "https://prometheus.io/",
    "Grafana": "https://grafana.com/",
    "GitOps": "https://opengitops.dev/",
    "SLSA": "https://slsa.dev/",
    "DORA Metrics": "https://dora.dev/",
    # Practice Circles platforms
    "Salesforce": "https://www.salesforce.com/",
    "MuleSoft": "https://www.mulesoft.com/",
    "Microsoft Power Platform": "https://www.microsoft.com/en-us/power-platform",
    "Power BI": "https://www.microsoft.com/en-us/power-platform/products/power-bi",
    "Tableau": "https://www.tableau.com/",
    "Microsoft Fabric": "https://www.microsoft.com/en-us/microsoft-fabric",
    "Databricks": "https://www.databricks.com/",
    # Engagement models
    "SAFe": "https://framework.scaledagile.com/",
    "Lean Software Development": "https://en.wikipedia.org/wiki/Lean_software_development",
    "Outcomes-Based Contracting": "https://en.wikipedia.org/wiki/Performance-based_contracting",
    # Security — application security
    "OWASP Top 10": "https://owasp.org/www-project-top-ten/",
    "OWASP ASVS": "https://owasp.org/www-project-application-security-verification-standard/",
    "OWASP SAMM": "https://owaspsamm.org/",
    "STRIDE": "https://en.wikipedia.org/wiki/STRIDE_model",
    "SLSA Framework": "https://slsa.dev/",
    "Sigstore": "https://www.sigstore.dev/",
    "CycloneDX": "https://cyclonedx.org/",
    "SPDX": "https://spdx.dev/",
    "CWE": "https://cwe.mitre.org/",
    # Security — authentication and authorization
    "OAuth 2.0": "https://oauth.net/2/",
    "OpenID Connect": "https://openid.net/connect/",
    "SAML 2.0": "https://en.wikipedia.org/wiki/SAML_2.0",
    "FIDO2": "https://fidoalliance.org/fido2/",
    "WebAuthn": "https://www.w3.org/TR/webauthn-2/",
    "Open Policy Agent": "https://www.openpolicyagent.org/",
    "JWT": "https://jwt.io/introduction",
    "RBAC": "https://en.wikipedia.org/wiki/Role-based_access_control",
    "ABAC": "https://en.wikipedia.org/wiki/Attribute-based_access_control",
    "ReBAC": "https://en.wikipedia.org/wiki/Relationship-based_access_control",
    # Security — cloud security
    "AWS Shared Responsibility Model": "https://aws.amazon.com/compliance/shared-responsibility-model/",
    "CIS Benchmarks": "https://www.cisecurity.org/cis-benchmarks",
    "AWS Well-Architected Security Pillar": "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html",
    "NIST SP 800-207 Zero Trust": "https://csrc.nist.gov/publications/detail/sp/800-207/final",
    "CSA Cloud Controls Matrix": "https://cloudsecurityalliance.org/research/cloud-controls-matrix",
    # Security — encryption
    "NIST FIPS 140-3": "https://csrc.nist.gov/publications/detail/fips/140/3/final",
    "TLS 1.3 (RFC 8446)": "https://datatracker.ietf.org/doc/html/rfc8446",
    "AES (FIPS 197)": "https://csrc.nist.gov/publications/detail/fips/197/final",
    "NIST Post-Quantum Cryptography": "https://csrc.nist.gov/projects/post-quantum-cryptography",
    "Let's Encrypt": "https://letsencrypt.org/",
    "Certificate Transparency": "https://certificate.transparency.dev/",
    "libsodium": "https://doc.libsodium.org/",
    "Tink": "https://developers.google.com/tink",
    # Security — vulnerability management
    "CVE Program": "https://www.cve.org/",
    "CVSS": "https://www.first.org/cvss/",
    "EPSS": "https://www.first.org/epss/",
    "KEV Catalog": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
    "NVD": "https://nvd.nist.gov/",
    "ISO 27001": "https://www.iso.org/standard/27001",
    "NIST SP 800-53": "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final",
}


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
    A page is substantive iff it has either Six principles or an Architecture
    Diagram section — both signals indicate an authored, full-template page."""
    return "## Six principles" in text or "## Architecture Diagram" in text


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
        for sub_dir in sorted(section_dir.iterdir()):
            if not sub_dir.is_dir():
                continue
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

    # 1) Add page nodes for all substantive pages
    for pid in substantive_ids:
        m = metadata[pid]
        nodes[pid] = {
            "id": pid,
            "label": m["title"],
            "section": m["section"],
            "type": "page",
            "url": f"/{pid}/",
            "description": m["description"],
        }

    # 2) Add standard/concept nodes from alignments + alignment edges
    for pid in substantive_ids:
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
    for pid in substantive_ids:
        for target in metadata[pid]["related_links"]:
            if target in substantive_ids and target != pid:
                edges.append({"source": pid, "target": target, "kind": "related"})

    return {"nodes": list(nodes.values()), "links": edges}


def nav_html(prefix, active=""):
    links = ""
    for label, href in NAV_LINKS:
        key = href.split("/")[0]
        cls = ' class="active"' if key == active else ""
        links += f'    <a href="{prefix}{href}"{cls}>{label}</a>\n'
    return (
        f'<nav class="nav">\n'
        f'  <a href="{prefix}index.html" class="nav-wordmark" id="nav-wm">'
        f'Ascendion Engineering</a>\n'
        f'  <div class="nav-sep"></div>\n'
        f'  <div class="nav-links">\n{links}  </div>\n'
        f'  <a href="{prefix}knowledge-graph/" class="nav-cta">Knowledge Graph</a>\n'
        f'  <a href="{prefix}index.html#topics" class="nav-cta">All Topics</a>\n'
        f'</nav>'
    )


def footer_html(label=""):
    return (
        f'<footer class="footer" role="button" tabindex="0" '
        f'aria-label="Scroll to top of page">\n  <div class="shell">\n'
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
        sum(1 for d in (src / s).iterdir() if d.is_dir() and (d / "README.md").exists())
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
    subs = []
    for d in sorted(src_dir.iterdir()):
        if d.is_dir() and (d / "README.md").exists():
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
        f'{footer_html(f"{slug}/")}\n\n'
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
    #   1. If README already has "## Architecture Diagram", insert wrap right after it.
    #   2. Otherwise, fall back to inserting "<h2>Architecture Diagram</h2>" + wrap
    #      before "Related Sections" / "Related" / "References".
    if diag_wrap_html:
        arch_h2_re = re.compile(r'(<h2[^>]*>\s*Architecture Diagram\s*</h2>)',
                                re.IGNORECASE)
        m = arch_h2_re.search(body)
        if m:
            insert_at = m.end()
            body = body[:insert_at] + '\n' + diag_wrap_html + body[insert_at:]
        else:
            full_block = '<h2>Architecture Diagram</h2>\n' + diag_wrap_html
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
        f'{footer_html(f"{slug}/{sub_slug}/")}\n\n'
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
    foot = footer_html()

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
    .force('collision', d3.forceCollide().radius(d => d.type === 'page' ? 36 : 24));

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
    }} else {{
      // diamond
      sel.append('rect')
        .attr('width', 16).attr('height', 16)
        .attr('x', -8).attr('y', -8)
        .attr('transform', 'rotate(45)');
    }}
  }});

  node.append('text')
    .attr('class', 'kg-label')
    .attr('dy', d => d.type === 'page' ? 28 : 20)
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
        print(f"\n[{slug}/]")
        gen_section(slug, sd, out_sec)
        for sub in sorted(sd.iterdir()):
            if sub.is_dir() and (sub / "README.md").exists():
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
