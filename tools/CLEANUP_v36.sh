#!/usr/bin/env bash
# CLEANUP_v36.sh — run from the root of the knowledge-library repo.
#
# v36 (Architecture Templates group) added 3 new pages under content/templates/.
# The slugs (adr-template, review-template, scorecard-template) were already
# pre-registered in TAXONOMY, so no orphan stubs are expected.
#
# This script is idempotent: it scans content/templates/ for any
# subdirectory that is NOT in the expected slug list and removes it.
# Safe to re-run. After this script runs, commit any deletions:
#   git add -A
#   git commit -m "chore: remove orphan templates subdirs (v36 architecture templates group)"
#   git push origin main

set -e

if [ ! -d "content" ]; then
  echo "ERROR: run this script from the root of the knowledge-library repo"
  echo "(expected to find a content/ directory)"
  exit 1
fi

if [ ! -d "content/templates" ]; then
  echo "No content/templates/ directory found — nothing to check."
  exit 0
fi

EXPECTED="adr-template review-template scorecard-template"
REMOVED=0

for sub in $(ls content/templates/ 2>/dev/null); do
  case " $EXPECTED " in
    *" $sub "*)
      ;; # expected, keep
    *)
      echo "  removing orphan content/templates/$sub/"
      git rm -rf "content/templates/$sub" 2>/dev/null || rm -rf "content/templates/$sub"
      REMOVED=$((REMOVED + 1))
      ;;
  esac
done

if [ $REMOVED -eq 0 ]; then
  echo "No orphan directories found under content/templates/ — already clean."
  echo "(Expected slugs: $EXPECTED — all present.)"
else
  echo
  echo "Removed $REMOVED orphan director(y/ies). Next:"
  echo "  git add -A"
  echo "  git commit -m 'chore: remove orphan templates subdirs (v36 architecture templates group)'"
  echo "  git push origin main"
fi
