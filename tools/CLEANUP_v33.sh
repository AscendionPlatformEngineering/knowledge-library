#!/usr/bin/env bash
# CLEANUP_v33.sh — run from the root of the knowledge-library repo.
#
# Removes the five orphan stub directories under content/ai/ — these
# were the pre-v33 placeholder seeds for AI System Architecture, AI
# Ethics, AI Monitoring, RAG, and AI Security. The substantive
# replacements now live under content/ai-native/ as part of v33.
#
# Under the v29 strict build, these directories produce loud orphan
# warnings at build time. This script removes them from the repo so
# the build is clean.
#
# After this script runs, commit the deletions and push:
#   git add -A
#   git commit -m "chore: remove content/ai/* orphan stubs (v33 ai-native group)"
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
  echo "  git commit -m 'chore: remove content/ai/* orphan stubs (v33 ai-native group)'"
  echo "  git push origin main"
fi
