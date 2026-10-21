#!/usr/bin/env bash
# Behavioural cases for skills/landing-page-ab-testing/scripts/ab_stats.py `test`:
# sparse data must not be called SIGNIFICANT, 0% and 100% arms must give a readable
# line with exit 0, invalid counts must be refused, a clear large win stays SIGNIFICANT.
set -u
cd "$(dirname "$0")/.."
AB="skills/landing-page-ab-testing/scripts/ab_stats.py"
fail=0; n=0

# case <name> <want exit> <must contain> <must not contain or -> <args...>
case_() {
  local name="$1" want_rc="$2" has="$3" hasnt="$4"; shift 4
  local out rc
  out="$(python3 -I "$AB" test "$@" 2>&1)"; rc=$?
  n=$((n + 1))
  if [ "$rc" -ne "$want_rc" ]; then echo "FAIL $name: exit $rc, want $want_rc"; echo "$out"; fail=1; return; fi
  if ! grep -qF -- "$has" <<<"$out"; then echo "FAIL $name: missing '$has'"; echo "$out"; fail=1; return; fi
  if [ "$hasnt" != "-" ] && grep -qF -- "$hasnt" <<<"$out"; then echo "FAIL $name: has '$hasnt'"; echo "$out"; fail=1; return; fi
  if grep -q Traceback <<<"$out"; then echo "FAIL $name: traceback"; echo "$out"; fail=1; fi
}

case_ sparse-0-vs-5      0 "method: Fisher exact" "SIGNIFICANT" --na 10000 --xa 0 --nb 10000 --xb 5
case_ sparse-p-exact     0 "p 0.0625"             "-"           --na 10000 --xa 0 --nb 10000 --xb 5
case_ both-zero          0 "insufficient data"    "SIGNIFICANT" --na 100 --xa 0 --nb 100 --xb 0
case_ both-all           0 "insufficient data"    "SIGNIFICANT" --na 100 --xa 100 --nb 100 --xb 100
case_ large-clear-win    0 "SIGNIFICANT"          "not significant" --na 10400 --xa 416 --nb 10380 --xb 502
case_ large-uses-normal  0 "method: two-proportion z-test" "-"  --na 10400 --xa 416 --nb 10380 --xb 502
case_ small-real-win     0 "SIGNIFICANT"          "not significant" --na 30 --xa 2 --nb 30 --xb 12
case_ zero-visitors      2 "visitors must be > 0" "-"           --na 0 --xa 0 --nb 10 --xb 1
case_ more-conv-than-n   2 "conversions must be between" "-"   --na 10 --xa 11 --nb 10 --xb 1
case_ negative-conv      2 "conversions must be between" "-"   --na 10 --xa -1 --nb 10 --xb 1

if [ "$fail" -ne 0 ]; then echo "AB_STATS CASES FAILED"; exit 1; fi
echo "AB_STATS CASES OK ($n cases)"
