#!/usr/bin/env bash
# CLEANUP_v31.sh — run from the root of the knowledge-library repo.
#
# v31 (Governance group) added 4 new pages under content/governance/.
# These slugs (checklists, review-templates, roles, scorecards) were
# already pre-registered in TAXONOMY, so no orphan stubs are expected.
#
# This script checks for any orphan governance subdirectories
# (anything under content/governance/ that's NOT one of the four
# expected slugs) and removes them. Under the strict-build introduced
# in v29, orphan directories produce loud build-time warnings; this
# script keeps the repo clean.
#
# Safe to re-run; idempotent. After this script runs, commit any
# deletions and push:
#   git add -A
#   git commit -m "chore: remove orphan governance subdirs (v31 governance group)"
#   git push origin main

set -e

if [ ! -d "content" ]; then
  echo "ERROR: run this script from the root of the knowledge-library repo"
  echo "(expected to find a content/ directory)"
  exit 1
fi

if [ ! -d "content/governance" ]; then
  echo "No content/governance/ directory found — nothing to check."
  exit 0
fi

EXPECTED="checklists review-templates roles scorecards"
REMOVED=0

for sub in $(ls content/governance/ 2>/dev/null); do
  case " $EXPECTED " in
    *" $sub "*)
      ;; # expected slug, keep it
    *)
      echo "  removing orphan content/governance/$sub/"
      git rm -rf "content/governance/$sub" 2>/dev/null || rm -rf "content/governance/$sub"
      REMOVED=$((REMOVED + 1))
      ;;
  esac
done

if [ $REMOVED -eq 0 ]; then
  echo "No orphan directories found under content/governance/ — already clean."
  echo "(Expected slugs: $EXPECTED — all present.)"
else
  echo
  echo "Removed $REMOVED orphan director(y/ies). Next:"
  echo "  git add -A"
  echo "  git commit -m 'chore: remove orphan governance subdirs (v31 governance group)'"
  echo "  git push origin main"
fi
