#!/usr/bin/env bash
# CLEANUP_v37.sh — run from the root of the knowledge-library repo.
#
# Removes any orphan stub directories under content/playbooks/ — the
# v37 batch authoritatively introduced exactly three playbooks pages:
#   playbooks/api-lifecycle
#   playbooks/migration
#   playbooks/resilience
# Any other directory under content/playbooks/ is a leftover stub from
# pre-v37 seeding (typically auto-generated lorem-ipsum stubs from
# tools/seed_content.py or older partial deliveries).
#
# Under the v29 strict build, these orphan directories produce loud
# warnings. This script removes them from the repo so the build is
# clean.
#
# After this script runs, commit the deletions and push:
#   git add -A
#   git commit -m "chore: remove content/playbooks/* orphan stubs (v37 engineering-playbooks group)"
#   git push origin main
set -e

if [ ! -d "content" ]; then
  echo "ERROR: run this script from the root of the knowledge-library repo"
  echo "(expected to find a content/ directory)"
  exit 1
fi

if [ ! -d "content/playbooks" ]; then
  echo "No content/playbooks/ directory found — your repo is already clean."
  exit 0
fi

EXPECTED="api-lifecycle migration resilience"
REMOVED=0
for sub in content/playbooks/*/; do
  [ -d "$sub" ] || continue
  name=$(basename "$sub")
  keep=0
  for expected in $EXPECTED; do
    if [ "$name" = "$expected" ]; then
      keep=1
      break
    fi
  done
  if [ $keep -eq 0 ]; then
    echo "  removing orphan content/playbooks/$name/"
    git rm -rf "content/playbooks/$name" 2>/dev/null || rm -rf "content/playbooks/$name"
    REMOVED=$((REMOVED + 1))
  fi
done

if [ $REMOVED -eq 0 ]; then
  echo "No orphan directories found under content/playbooks/ — already clean."
else
  echo
  echo "Removed $REMOVED orphan director(y/ies) under content/playbooks/. Next:"
  echo "  git add -A"
  echo "  git commit -m 'chore: remove content/playbooks/* orphan stubs (v37 engineering-playbooks group)'"
  echo "  git push origin main"
fi
