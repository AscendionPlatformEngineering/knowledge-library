#!/usr/bin/env bash
set -euo pipefail

REPO=/home/claude/work/restoration
PREVIEW=/tmp/preview30
OUT=/mnt/user-data/outputs

rm -rf "$PREVIEW"
mkdir -p "$PREVIEW"

# Individual previews — copy each substantive page's index.html and rewrite CSS path
PATHS=(
  "patterns/data"
  "patterns/deployment"
  "patterns/integration"
  "patterns/security"
  "patterns/structural"
  "principles/ai-native"
  "principles/domain-specific"
  "principles/foundational"
  "principles/modernization"
  "principles/cloud-native"
  "system-design/edge-ai"
  "system-design/event-driven"
  "system-design/ha-dr"
  "system-design/scalable"
  "technology/ui-ux-cx"
  "technology/api-backend"
  "technology/databases"
  "technology/cloud"
  "technology/devops"
  "technology/practice-circles"
  "technology/engagement-models"
  "security/application-security"
  "security/authentication-authorization"
  "security/cloud-security"
  "security/encryption"
  "security/vulnerability-management"
  "ai-native/architecture"
  "ai-native/ethics"
  "ai-native/monitoring"
  "ai-native/rag"
  "ai-native/security"
)
for p in "${PATHS[@]}"; do
  name="${p//\//-}"
  cp "$REPO/dist/$p/index.html" "$PREVIEW/${name}-preview.html"
  sed -i 's|href="../../shared.css"|href="shared.css"|' "$PREVIEW/${name}-preview.html"
done

cp "$REPO/dist/knowledge-graph/index.html" "$PREVIEW/knowledge-graph-preview.html"
sed -i 's|href="../shared.css"|href="shared.css"|' "$PREVIEW/knowledge-graph-preview.html"
cp "$REPO/dist/shared.css" "$PREVIEW/shared.css"

# Six-emblem comparison page
cat > "$PREVIEW/thirtyone-emblems.html" <<'HTMLHEAD'
<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Six motion mechanics</title>
<style>
  body { font-family: -apple-system, system-ui, sans-serif; background: #FAF6EE;
         margin: 0; padding: 3rem 2rem; color: #0E0E0E; }
  h1 { font-weight: 500; font-size: 1.6rem; margin: 0 0 0.5rem; letter-spacing: -0.01em; }
  .lede { font-size: 0.95rem; color: #4A4A4A; max-width: 60rem;
          margin: 0 0 2.5rem; line-height: 1.55; }
  .row { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
         gap: 1.5rem; max-width: 80rem; }
  .card { background: #FFFFFF; border-radius: 12px; padding: 1.5rem 1.25rem;
          border: 1px solid #E0DED7; }
  .card h2 { font-size: 1rem; font-weight: 500; margin: 0 0 0.25rem; }
  .card .meta { font-family: ui-monospace, monospace; font-size: 0.74rem;
                color: #C96330; margin-bottom: 1rem; letter-spacing: 0.04em; }
  .emblem-frame { background: #FAF6EE; border-radius: 8px; padding: 1rem;
                  display: flex; align-items: center; justify-content: center;
                  aspect-ratio: 4/3; }
  .emblem-frame svg { width: 100%; height: 100%; }
  .desc { font-size: 0.82rem; color: #4A4A4A; line-height: 1.5; margin-top: 1rem; }
</style></head><body>
<h1>Thirty-one pages, thirty-one motion mechanics — AI-Native group complete</h1>
<p class="lede">Each emblem uses a categorically different animation primitive. Same colour palette, same SVG primitives, same visual minimalism — but the motion itself carries the meaning of the page.</p>
<div class="row">
HTMLHEAD

# One card per page — heredoc-free, just printf into the file
add_card() {
  local path="$1" title="$2" meta="$3" desc="$4"
  {
    printf '<div class="card"><h2>%s</h2><div class="meta">%s</div>\n' "$title" "$meta"
    printf '<div class="emblem-frame">\n'
    cat "$REPO/content/$path/hero.svg"
    printf '</div><p class="desc">%s</p></div>\n' "$desc"
  } >> "$PREVIEW/thirtyone-emblems.html"
}

add_card "principles/ai-native"       "AI-Native"        "PARTICLE FLOW"                "Many small particles converge to a central reasoning core. Distributed inputs becoming one thought."
add_card "principles/domain-specific" "Domain-Specific"  "SHAPE OSCILLATION"            "Two whole shapes — circle and square — drift inward, briefly overlap, then return to their lanes."
add_card "principles/foundational"    "Foundational"     "RIGID-BODY ROTATION"          "A pendulum. Fixed pivot, rhythmic swing — natural easing at extremes, fast through centre."
add_card "principles/modernization"   "Modernization"    "CROSS-FADE METAMORPHOSIS"     "A monolith form cross-fades into a service grid. Two complete forms trading visibility in the same space."
add_card "principles/cloud-native"    "Cloud-Native"     "ELASTIC REPLICATION"          "Centre pod always present; surrounding pods appear and recede in waves under load."
add_card "patterns/data"              "Data Patterns"    "SEQUENTIAL FRAME ILLUMINATION" "Four temporal frames take turns being highlighted. The motion is time, not movement."
add_card "patterns/deployment"        "Deployment Patterns" "PROGRESSIVE THRESHOLD FILL" "A fill region grows left-to-right through canary checkpoints, pausing at each threshold. The motion is the deployment process itself."
add_card "patterns/integration"       "Integration Patterns" "BIDIRECTIONAL PULSATION" "Two nodes pulse in turn while a static channel brightens between them. The motion is the conversation: speak, transit, respond, transit, rest."
add_card "patterns/security"          "Security Patterns" "CONCENTRIC PERIMETER TRACING" "Concentric rings draw themselves into existence around a protected asset, building defence in depth. The motion is line-tracing along closed paths."
add_card "patterns/structural"        "Structural Patterns" "ACCRETIVE COMPOSITION" "Nine tiles assemble in a 3×3 grid — core first, then surrounding modules in spiral order — hold, then dissolve simultaneously. The motion is composition itself."
add_card "system-design/edge-ai"       "Edge AI Systems"        "PERIPHERAL ASYNCHRONOUS PULSE" "Six edge nodes around a faint distant centre, each pulsing on its own staggered phase. The rhythm of asynchronous on-device inference — devices working on independent clocks with no coordinator."
add_card "system-design/event-driven"  "Event-Driven Systems"   "WAVE PROPAGATION"             "A single ring expands from a source point — radius grows, opacity fades — while subscribers at staggered distances flash as the wavefront reaches them. The motion is the event itself, propagating outward through indifferent receivers."
add_card "system-design/ha-dr"         "HA & DR Systems"        "PRIMARY-STANDBY HANDOFF"      "Two identical replicas; the active role swaps periodically between them. Both shapes are persistent, identical in geometry — only the colour and the role indicator move."
add_card "system-design/scalable"      "Scalable Systems"       "SCALING ENVELOPE"             "Five rectangles in a row; the count of active rectangles rises 1→5 then falls 5→1 across nested time intervals. The motion is the load curve itself: capacity rising to meet demand, then receding when the surge passes."
add_card "technology/ui-ux-cx"          "UI, UX & CX"               "LAYERED DEPTH REVEAL"           "Three offset rectangles — CX, UX, UI — reveal back-to-front in sequence. The motion is the design stack itself: customer experience as the outer envelope, user experience the layer within, user interface the surface that touches the user."
add_card "technology/api-backend"       "API & Backend Technologies" "BIDIRECTIONAL PIPELINE TRAFFIC" "Two parallel horizontal lanes carry dots in opposite directions — request flows down, response flows up. The motion is the contract: every request is owed a response, every response was preceded by a request, the pipeline runs continuously."
add_card "technology/databases"         "Databases"                  "SEDIMENTATION STACKING"         "Five small items fall from above and accumulate at the floor in sequence, building up a stack. The motion is persistence itself: data settles, accumulates, becomes durable; the floor is the storage layer that catches everything."
add_card "technology/cloud"             "Cloud"                      "SWEEPING BEAM SCAN"             "A vertical beam line translates left to right; fixed dots flash terracotta as the beam passes. The motion is the cloud control plane sweeping over distributed resources — discovering, observing, evaluating each one in turn."
add_card "technology/devops"            "DevOps"                     "CONVEYOR LOOP"                  "Five dots travel a closed rectangular path continuously, each at a staggered position around the loop. The motion is the pipeline: continuous integration, continuous delivery, continuous deployment — work moves around the loop without ever stopping."
add_card "technology/practice-circles"  "Practice Circles"           "CARDINAL CLUSTER CYCLE"         "Four small dot clusters arranged at cardinal positions cycle through being lit, with the centre brightening to indicate cross-pollination between circles. The motion is the practice itself: communities working in parallel, sharing what they learn at the centre."
add_card "technology/engagement-models" "Engagement Models"          "TIER ASCENT"                    "A token climbs three persistent platform steps in sequence — Staffing, Managed Capacity, Managed Services — before resetting. The motion is the maturity arrow: partnerships ascending through tiers as trust accumulates over engagements."
add_card "security/application-security"           "Application Security"            "FILTRATION CASCADE"             "Five dots fall from the top through three horizontal filter layers; some are blocked at each layer and fade out, two reach the bottom and briefly turn terracotta as they hit the protected application baseline. The motion is purification: the dots that survive every filter are the inputs the application can safely consume."
add_card "security/authentication-authorization"   "Authentication and Authorization" "CHALLENGE-RESPONSE HANDSHAKE"   "Two persistent shapes — Subject on the left, Resource on the right — exchange tokens alternately, one direction at a time, with explicit rest between exchanges. The receiving node briefly turns terracotta as the token arrives. The motion is the protocol itself: a verified identity is established through discrete challenge and response, not continuous chatter."
add_card "security/cloud-security"                 "Cloud Security"                  "SHIELD ENVELOPE PULSATION"      "Three concentric rings around a persistent terracotta core asset expand and contract in unison — synchronised breathing rhythm over a 6-second cycle. The motion is the layered defensive envelope: org SCPs, CSPM, CIEM, and CWPP maintaining a protective scope around the workload that is never absent, only modulated."
add_card "security/encryption"                     "Encryption"                      "KEY-MERGE / UNMERGE"            "Two persistent shapes — a Data rectangle on the left and a Key circle on the right — translate toward the centre, fade as a single Ciphertext rectangle fades in, hold as ciphertext, then reverse: ciphertext fades out and the original two shapes return to their original positions. The motion is symmetric encryption itself: data + key produce ciphertext; ciphertext + key recover the data."
add_card "security/vulnerability-management"       "Vulnerability Management"        "TRIAGE FUNNEL"                  "Eight dots enter wide at the top of a visible inverted-trapezoid funnel; six descend through prioritisation pressure, four make it to the narrow bottom output line where they briefly turn terracotta as remediated. The other dots are blocked at the diagonal walls and fade. The motion is the reduction itself: many vulnerabilities discovered, fewer reach remediation per cycle."

printf '</div></body></html>\n' >> "$PREVIEW/thirtyone-emblems.html"

# Stage tarball — exclude stub directories so the package is lean
cd "$REPO"
rm -rf dist
find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true

# Backup, then prune content to only the substantive directories
mv content content.full
mkdir -p content/principles content/patterns
for d in ai-native domain-specific foundational modernization cloud-native; do
  cp -r "content.full/principles/$d" "content/principles/$d"
done
cp -r "content.full/patterns/data" "content/patterns/data"
cp -r "content.full/patterns/deployment" "content/patterns/deployment"
cp -r "content.full/patterns/integration" "content/patterns/integration"
cp -r "content.full/patterns/security" "content/patterns/security"
mkdir -p content/system-design
cp -r "content.full/patterns/structural" "content/patterns/structural"
cp -r "content.full/system-design/edge-ai"      "content/system-design/edge-ai"
cp -r "content.full/system-design/event-driven" "content/system-design/event-driven"
cp -r "content.full/system-design/ha-dr"        "content/system-design/ha-dr"
cp -r "content.full/system-design/scalable"     "content/system-design/scalable"
mkdir -p content/technology
cp -r "content.full/technology/ui-ux-cx"          "content/technology/ui-ux-cx"
cp -r "content.full/technology/api-backend"       "content/technology/api-backend"
cp -r "content.full/technology/databases"         "content/technology/databases"
cp -r "content.full/technology/cloud"             "content/technology/cloud"
cp -r "content.full/technology/devops"            "content/technology/devops"
cp -r "content.full/technology/practice-circles"  "content/technology/practice-circles"
cp -r "content.full/technology/engagement-models" "content/technology/engagement-models"
mkdir -p content/security
cp -r "content.full/security/application-security"           "content/security/application-security"
cp -r "content.full/security/authentication-authorization"   "content/security/authentication-authorization"
cp -r "content.full/security/cloud-security"                 "content/security/cloud-security"
cp -r "content.full/security/encryption"                     "content/security/encryption"
cp -r "content.full/security/vulnerability-management"       "content/security/vulnerability-management"
mkdir -p content/ai-native
cp -r "content.full/ai-native/architecture" "content/ai-native/architecture"
cp -r "content.full/ai-native/ethics"       "content/ai-native/ethics"
cp -r "content.full/ai-native/monitoring"   "content/ai-native/monitoring"
cp -r "content.full/ai-native/rag"          "content/ai-native/rag"
cp -r "content.full/ai-native/security"     "content/ai-native/security"


# ─── v30 cleanup script (deletes orphan stub directories from user's repo) ───
cat > "$REPO/tools/CLEANUP_v30.sh" <<'CLEANUP_EOF'
#!/usr/bin/env bash
# CLEANUP_v30.sh — run from the root of the knowledge-library repo.
#
# Removes the five orphan stub directories under content/ai/ — these
# were the pre-v30 placeholder seeds for AI System Architecture, AI
# Ethics, AI Monitoring, RAG, and AI Security. The substantive
# replacements now live under content/ai-native/ as part of v30.
#
# Under the v29 strict build, these directories produce loud orphan
# warnings at build time. This script removes them from the repo so
# the build is clean.
#
# After this script runs, commit the deletions and push:
#   git add -A
#   git commit -m "chore: remove content/ai/* orphan stubs (v30 ai-native group)"
#   git push origin main
set -e

if [ ! -d "content" ]; then
  echo "ERROR: run this script from the root of the knowledge-library repo"
  echo "(expected to find a content/ directory)"
  exit 1
fi

if [ ! -d "content/ai" ]; then
  echo "No content/ai/ directory found — your repo is already clean."
  exit 0
fi

REMOVED=0
for orphan in architecture ethics monitoring rag security; do
  if [ -d "content/ai/$orphan" ]; then
    echo "  removing content/ai/$orphan/"
    git rm -rf "content/ai/$orphan" 2>/dev/null || rm -rf "content/ai/$orphan"
    REMOVED=$((REMOVED + 1))
  fi
done

# If content/ai/ is now empty, remove it too
if [ -d "content/ai" ] && [ -z "$(ls -A content/ai 2>/dev/null)" ]; then
  echo "  removing now-empty content/ai/"
  rmdir content/ai 2>/dev/null || true
fi

if [ $REMOVED -eq 0 ]; then
  echo "No orphan directories found under content/ai/ — already clean."
else
  echo
  echo "Removed $REMOVED orphan director(y/ies). Next:"
  echo "  git add -A"
  echo "  git commit -m 'chore: remove content/ai/* orphan stubs (v30 ai-native group)'"
  echo "  git push origin main"
fi
CLEANUP_EOF
chmod +x "$REPO/tools/CLEANUP_v30.sh"

tar czf "$OUT/ascendion-engineering-v30.tar.gz" \
    --exclude='.git' --exclude='node_modules' --exclude='*.pyc' \
    tools src content infra .github

# Also expose CLEANUP_v30.sh as a standalone output (user can run it before
# extracting the tarball, without having to extract the tarball first).
cp "$REPO/tools/CLEANUP_v30.sh" "$OUT/CLEANUP_v30.sh"

# AI-Native preview copies
cp "$PREVIEW/ai-native-architecture-preview.html" "$OUT/ai-native-architecture-preview-v30.html"
cp "$PREVIEW/ai-native-ethics-preview.html"       "$OUT/ai-native-ethics-preview-v30.html"
cp "$PREVIEW/ai-native-monitoring-preview.html"   "$OUT/ai-native-monitoring-preview-v30.html"
cp "$PREVIEW/ai-native-rag-preview.html"          "$OUT/ai-native-rag-preview-v30.html"
cp "$PREVIEW/ai-native-security-preview.html"     "$OUT/ai-native-security-preview-v30.html"

# Restore full content tree
rm -rf content
mv content.full content

# Copy individual previews
cp "$PREVIEW/thirtyone-emblems.html"                       "$OUT/thirtyone-emblems-v30.html"
cp "$PREVIEW/patterns-data-preview.html"                  "$OUT/data-patterns-preview-v30.html"
cp "$PREVIEW/knowledge-graph-preview.html"                "$OUT/knowledge-graph-preview-v30.html"
cp "$PREVIEW/system-design-edge-ai-preview.html"          "$OUT/edge-ai-preview-v30.html"
cp "$PREVIEW/system-design-event-driven-preview.html"     "$OUT/event-driven-preview-v30.html"
cp "$PREVIEW/system-design-ha-dr-preview.html"            "$OUT/ha-dr-preview-v30.html"
cp "$PREVIEW/system-design-scalable-preview.html"         "$OUT/scalable-preview-v30.html"
cp "$PREVIEW/technology-ui-ux-cx-preview.html"            "$OUT/ui-ux-cx-preview-v30.html"
cp "$PREVIEW/technology-api-backend-preview.html"         "$OUT/api-backend-preview-v30.html"
cp "$PREVIEW/technology-databases-preview.html"           "$OUT/databases-preview-v30.html"
cp "$PREVIEW/technology-cloud-preview.html"               "$OUT/cloud-preview-v30.html"
cp "$PREVIEW/technology-devops-preview.html"              "$OUT/devops-preview-v30.html"
cp "$PREVIEW/technology-practice-circles-preview.html"    "$OUT/practice-circles-preview-v30.html"
cp "$PREVIEW/technology-engagement-models-preview.html"   "$OUT/engagement-models-preview-v30.html"
cp "$PREVIEW/security-application-security-preview.html"           "$OUT/application-security-preview-v30.html"
cp "$PREVIEW/security-authentication-authorization-preview.html"   "$OUT/authentication-authorization-preview-v30.html"
cp "$PREVIEW/security-cloud-security-preview.html"                 "$OUT/cloud-security-preview-v30.html"
cp "$PREVIEW/security-encryption-preview.html"                     "$OUT/encryption-preview-v30.html"
cp "$PREVIEW/security-vulnerability-management-preview.html"       "$OUT/vulnerability-management-preview-v30.html"

echo
echo "═══ STAGED ═══"
ls -la "$OUT"/*v30* 2>&1
echo
echo "Tarball contents (top-level):"
tar tzf "$OUT/ascendion-engineering-v30.tar.gz" | head -30
