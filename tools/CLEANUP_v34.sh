#!/usr/bin/env bash
# CLEANUP_v34.sh — run from the root of the knowledge-library repo.
#
# v34 (Review Checklists group) added 3 new pages under content/checklists/.
# The slugs (architecture, deployment, security) were already pre-registered
# in TAXONOMY, so no orphan stubs are expected.
#
# This script is idempotent: it scans content/checklists/ for any
# subdirectory that is NOT in the expected slug list and removes it.
# Safe to re-run. After this script runs, commit any deletions:
#   git add -A
#   git commit -m "chore: remove orphan checklists subdirs (v34 review checklists group)"
#   git push origin main

set -e

if [ ! -d "content" ]; then
  echo "ERROR: run this script from the root of the knowledge-library repo"
  echo "(expected to find a content/ directory)"
  exit 1
fi

if [ ! -d "content/checklists" ]; then
  echo "No content/checklists/ directory found — nothing to check."
  exit 0
fi

EXPECTED="architecture deployment security"
REMOVED=0

for sub in $(ls content/checklists/ 2>/dev/null); do
  case " $EXPECTED " in
    *" $sub "*)
      ;; # expected, keep
    *)
      echo "  removing orphan content/checklists/$sub/"
      git rm -rf "content/checklists/$sub" 2>/dev/null || rm -rf "content/checklists/$sub"
      REMOVED=$((REMOVED + 1))
      ;;
  esac
done

if [ $REMOVED -eq 0 ]; then
  echo "No orphan directories found under content/checklists/ — already clean."
  echo "(Expected slugs: $EXPECTED — all present.)"
else
  echo
  echo "Removed $REMOVED orphan director(y/ies). Next:"
  echo "  git add -A"
  echo "  git commit -m 'chore: remove orphan checklists subdirs (v34 review checklists group)'"
  echo "  git push origin main"
fi
