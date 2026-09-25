#!/usr/bin/env bash
# Run this before pushing anything to this PUBLIC repo.
#
# The private working copy and this one are maintained separately, so nothing stops a file
# being copied across by hand. These are the five sweeps this repo was cleared with.
# Exits non-zero on any hit.
#
#     ./verify.sh
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
fail=0
check () {  # name, pattern
  local hits
  hits=$(grep -rIn -E "$2" . --exclude-dir=.git --exclude=verify.sh 2>/dev/null || true)
  if [ -n "$hits" ]; then
    printf '  FAIL  %s\n' "$1"; printf '%s\n' "$hits" | head -20 | sed 's/^/        /'
    fail=1
  else
    printf '  ok    %s\n' "$1"
  fi
}

echo "Checking $(pwd)"
check "no credentials"            'AQ[A-Za-z0-9]{30,}|ghp_[A-Za-z0-9]{20,}|github_pat_|sk-[A-Za-z0-9]{20,}|Bearer [A-Za-z0-9]{20,}'
check "no personal file paths"    '/Users/|/home/[a-z]'
check "no former-employer ad accounts" '504994684|506397648|506407296|508183416'
check "no live campaign ids"      '\b557560141\b|\b1214533624\b|\b900[0-9]{6}\b|\b89613535\b|urn:li:(share|sponsoredCreative):[0-9]'
check "no invented ticket ids"    'INC-[0-9]{4,}'
# Nothing in this repo should be a verbatim copy of somebody else's writing. The two
# knowledge-base documents that were were removed; this stops them coming back.
check "no third-party bylines"    'By Ivan Falco'

# Every example page still has to clear the quality gate and carry its disclosure.
nodisc=0
for d in examples/*/accounts/*/landing-page; do
  [ -d "$d" ] || continue
  # case-insensitive, and on a single word, because the sentence wraps in the raw HTML
  if ! grep -qi "affiliated" "$d/index.html" 2>/dev/null; then
    printf '  FAIL  missing disclosure: %s\n' "$d"; nodisc=1; fail=1
  fi
done
[ $nodisc -eq 0 ] && printf '  ok    every example page carries its disclosure\n'

# Every local file a page asks for has to be beside it. A WYN page shipped without its
# scrollcraft.js once: the page still rendered, and every interactive element was dead.
missing=0
for f in examples/*/accounts/*/landing-page/index.html; do
  [ -f "$f" ] || continue
  d=$(dirname "$f")
  for ref in $(grep -ohE '(src|href)="[^"#:]+\.(js|css|mp4|png|jpg|svg|webm)"' "$f" \
               | sed -E 's/.*="([^"]+)"/\1/' | sort -u); do
    if [ ! -f "$d/$ref" ]; then
      printf '  FAIL  %s references %s, which is not there\n' "$f" "$ref"; missing=1; fail=1
    # On disk is not enough. A gitignore rule can silently drop a file that the page needs,
    # and the working tree looks perfect while the published page 404s. Ask git, not the disk.
    elif git ls-files --error-unmatch "$d/$ref" >/dev/null 2>&1; then :
    else
      printf '  FAIL  %s is on disk but NOT tracked by git (check .gitignore)\n' "$d/$ref"
      missing=1; fail=1
    fi
  done
done
[ $missing -eq 0 ] && printf '  ok    every page has the files it asks for\n'

# No committee table names a real individual. These pages are unsolicited demonstrations
# published to the open web, and nobody on them asked to be there. Jean's rule is seats, not
# people. This is checked STRUCTURALLY rather than against a list of names, because the first
# sweep was a hardcoded list of four and it missed fifteen on another run.
named=0
for f in examples/*/accounts/*/landing-page/index.html examples/*/handover.html; do
  [ -f "$f" ] || continue
  bad=$(grep -oE '<tr><td><b>[^<]{4,70}</b><br><span class="cap">[^<]{2,60}</span>' "$f" \
        | sed -E 's/.*<span class="cap">([^<]*)<.*/\1/' \
        | grep -vxE 'open seat|named by role, not by person' || true)
  if [ -n "$bad" ]; then
    printf '  FAIL  %s names a person in a committee table: %s\n' "$f" "$(echo "$bad" | tr '\n' ';')"
    named=1; fail=1
  fi
done
[ $named -eq 0 ] && printf '  ok    no committee table names an individual\n'

echo
if [ $fail -eq 0 ]; then echo "PASS. Safe to push."; else echo "DO NOT PUSH. Fix the above."; fi
exit $fail
