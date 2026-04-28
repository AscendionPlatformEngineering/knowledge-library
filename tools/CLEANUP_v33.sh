#!/usr/bin/env bash
# CLEANUP_v33.sh — run from the root of the knowledge-library repo.
#
# v33 (Operational Runbooks group) added 3 new pages under content/runbooks/.
# The slugs (incident, migration, rollback) were already pre-registered in
# TAXONOMY, so no orphan stubs are expected.
#
# This script is idempotent: it scans content/runbooks/ for any
# subdirectory that is NOT in the expected slug list and removes it.
# Safe to re-run. After this script runs, commit any deletions:
#   git add -A
#   git commit -m "chore: remove orphan runbooks subdirs (v33 operational runbooks group)"
#   git push origin main

set -e

if [ ! -d "content" ]; then
  echo "ERROR: run this script from the root of the knowledge-library repo"
  echo "(expected to find a content/ directory)"
  exit 1
fi

if [ ! -d "content/runbooks" ]; then
  echo "No content/runbooks/ directory found — nothing to check."
  exit 0
fi

EXPECTED="incident migration rollback"
REMOVED=0

for sub in $(ls content/runbooks/ 2>/dev/null); do
  case " $EXPECTED " in
    *" $sub "*)
      ;; # expected, keep
    *)
      echo "  removing orphan content/runbooks/$sub/"
      git rm -rf "content/runbooks/$sub" 2>/dev/null || rm -rf "content/runbooks/$sub"
      REMOVED=$((REMOVED + 1))
      ;;
  esac
done

if [ $REMOVED -eq 0 ]; then
  echo "No orphan directories found under content/runbooks/ — already clean."
  echo "(Expected slugs: $EXPECTED — all present.)"
else
  echo
  echo "Removed $REMOVED orphan director(y/ies). Next:"
  echo "  git add -A"
  echo "  git commit -m 'chore: remove orphan runbooks subdirs (v33 operational runbooks group)'"
  echo "  git push origin main"
fi
