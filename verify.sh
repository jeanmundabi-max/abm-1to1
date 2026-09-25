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
for d in examples/*/accounts/*/landing-page; do
  [ -d "$d" ] || continue
  if ! grep -q "not affiliated with" "$d/index.html" 2>/dev/null; then
    printf '  FAIL  missing disclosure: %s\n' "$d"; fail=1
  fi
done
[ $fail -eq 0 ] && printf '  ok    every example page carries its disclosure\n'

echo
if [ $fail -eq 0 ]; then echo "PASS. Safe to push."; else echo "DO NOT PUSH. Fix the above."; fi
exit $fail
