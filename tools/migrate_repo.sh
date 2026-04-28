#!/usr/bin/env bash
#
# Ascendion Engineering — repo migration helper
#
# Run this from the root of the knowledge-library repo. It:
#   1. Removes the existing root-level HTML files (they will be regenerated)
#   2. Removes the root-level shared.css (it has moved to src/)
#   3. Removes the root-level wordmark.js (no longer used; embedded in template)
#   4. Removes empty section directories
#
# After this script runs, the repo's only directories should be:
#   .git/              ← preserved
#   .github/           ← preserved (will be replaced by the new workflow)
#   tools/             ← new
#   src/               ← new
#   content/           ← new
#
# This script is idempotent — running it twice is safe.

set -e

REPO_ROOT="$(pwd)"
echo "Working in: $REPO_ROOT"
echo ""

# Sanity check — refuse to run from anywhere except a knowledge-library checkout
if [ ! -d "$REPO_ROOT/.git" ]; then
    echo "ERROR: $REPO_ROOT does not look like a git repo."
    echo "       cd into your knowledge-library checkout and try again."
    exit 1
fi

if [ ! -f "$REPO_ROOT/.github/workflows/deploy.yml" ]; then
    echo "ERROR: $REPO_ROOT does not look like the knowledge-library repo."
    echo "       Refusing to run."
    exit 1
fi

# Step 1: remove root index.html, shared.css, wordmark.js
echo "[1/3] Removing legacy root files..."
for f in index.html shared.css wordmark.js README.md; do
    if [ -f "$REPO_ROOT/$f" ]; then
        rm -v "$REPO_ROOT/$f"
    fi
done
echo ""

# Step 2: remove all section directories that contain only HTML files
echo "[2/3] Removing section directories with only generated HTML..."
for dir in "$REPO_ROOT"/*/; do
    name=$(basename "$dir")
    case "$name" in
        .git|.github|tools|src|content|dist|node_modules)
            continue
            ;;
    esac
    # Confirm the directory contains only index.html files (i.e. is generated content)
    non_html=$(find "$dir" -type f ! -name 'index.html' | head -1)
    if [ -z "$non_html" ]; then
        echo "  removing $name/"
        rm -rf "$dir"
    else
        echo "  KEEPING $name/ (contains non-HTML files: $non_html)"
    fi
done
echo ""

# Step 3: confirm new structure
echo "[3/3] Final repo structure:"
ls -la "$REPO_ROOT" | grep -v '^total' | awk '{print "  " $NF}'
echo ""

echo "── Done ─────────────────────────────────────────────────────"
echo "Next: review with 'git status', then commit and push."
