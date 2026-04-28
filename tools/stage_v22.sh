#!/usr/bin/env bash
set -euo pipefail

REPO=/home/claude/work/restoration
PREVIEW=/tmp/preview22
OUT=/mnt/user-data/outputs

rm -rf "$PREVIEW"
mkdir -p "$PREVIEW"

# Individual previews — copy each substantive page's index.html and rewrite CSS path
PATHS=(
  "patterns/data"
  "patterns/deployment"
  "principles/ai-native"
  "principles/domain-specific"
  "principles/foundational"
  "principles/modernization"
  "principles/cloud-native"
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
cat > "$PREVIEW/seven-emblems.html" <<'HTMLHEAD'
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
<h1>Seven pages, seven motion mechanics</h1>
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
  } >> "$PREVIEW/seven-emblems.html"
}

add_card "principles/ai-native"       "AI-Native"        "PARTICLE FLOW"                "Many small particles converge to a central reasoning core. Distributed inputs becoming one thought."
add_card "principles/domain-specific" "Domain-Specific"  "SHAPE OSCILLATION"            "Two whole shapes — circle and square — drift inward, briefly overlap, then return to their lanes."
add_card "principles/foundational"    "Foundational"     "RIGID-BODY ROTATION"          "A pendulum. Fixed pivot, rhythmic swing — natural easing at extremes, fast through centre."
add_card "principles/modernization"   "Modernization"    "CROSS-FADE METAMORPHOSIS"     "A monolith form cross-fades into a service grid. Two complete forms trading visibility in the same space."
add_card "principles/cloud-native"    "Cloud-Native"     "ELASTIC REPLICATION"          "Centre pod always present; surrounding pods appear and recede in waves under load."
add_card "patterns/data"              "Data Patterns"    "SEQUENTIAL FRAME ILLUMINATION" "Four temporal frames take turns being highlighted. The motion is time, not movement."
add_card "patterns/deployment"        "Deployment Patterns" "PROGRESSIVE THRESHOLD FILL" "A fill region grows left-to-right through canary checkpoints, pausing at each threshold. The motion is the deployment process itself."

printf '</div></body></html>\n' >> "$PREVIEW/seven-emblems.html"

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

tar czf "$OUT/ascendion-engineering-v22.tar.gz" \
    --exclude='.git' --exclude='node_modules' --exclude='*.pyc' \
    tools src content infra .github

# Restore full content tree
rm -rf content
mv content.full content

# Copy individual previews
cp "$PREVIEW/seven-emblems.html"             "$OUT/six-emblems-v22.html"
cp "$PREVIEW/patterns-data-preview.html"   "$OUT/data-patterns-preview-v22.html"
cp "$PREVIEW/knowledge-graph-preview.html" "$OUT/knowledge-graph-preview-v22.html"

echo
echo "═══ STAGED ═══"
ls -la "$OUT"/*v22* 2>&1
echo
echo "Tarball contents (top-level):"
tar tzf "$OUT/ascendion-engineering-v22.tar.gz" | head -30
