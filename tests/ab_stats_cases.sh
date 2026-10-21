#!/usr/bin/env bash
# Behavioural cases for skills/landing-page-ab-testing/scripts/ab_stats.py `test`:
# sparse data must not be called SIGNIFICANT, 0% and 100% arms must give a readable
# line with exit 0, invalid counts must be refused, a clear large win stays SIGNIFICANT.
# `srm`: sparse expected counts use the exact binomial test (no false STOP on a valid
# split), large counts keep the chi-square line, a real sparse mismatch still STOPs.
set -u
cd "$(dirname "$0")/.."
AB="skills/landing-page-ab-testing/scripts/ab_stats.py"
fail=0; n=0

# run_ <subcommand> <name> <want exit> <must contain> <must not contain or -> <args...>
run_() {
  local cmd="$1" name="$2" want_rc="$3" has="$4" hasnt="$5"; shift 5
  local out rc
  out="$(python3 -I "$AB" "$cmd" "$@" 2>&1)"; rc=$?
  n=$((n + 1))
  if [ "$rc" -ne "$want_rc" ]; then echo "FAIL $name: exit $rc, want $want_rc"; echo "$out"; fail=1; return; fi
  if ! grep -qF -- "$has" <<<"$out"; then echo "FAIL $name: missing '$has'"; echo "$out"; fail=1; return; fi
  if [ "$hasnt" != "-" ] && grep -qF -- "$hasnt" <<<"$out"; then echo "FAIL $name: has '$hasnt'"; echo "$out"; fail=1; return; fi
  if grep -q Traceback <<<"$out"; then echo "FAIL $name: traceback"; echo "$out"; fail=1; fi
}
case_() { run_ test "$@"; }
srm_() { run_ srm "$@"; }

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

srm_ srm-sparse-valid-90-10 0 "exact binomial" "STOP"            --na 1 --nb 3 --ratio 0.9
srm_ srm-sparse-p-exact     0 "p 0.003700  -> ok" "-"            --na 1 --nb 3 --ratio 0.9
srm_ srm-large-chi-square   0 "chi2 17.82  p 0.000024  -> SRM: STOP, debug assignment" "exact" --na 10400 --nb 9800
srm_ srm-large-balanced     0 "chi2 0.05  p 0.821129  -> ok" "-" --na 10000 --nb 10032
srm_ srm-sparse-mismatch    0 "exact binomial" "-> ok"           --na 0 --nb 40 --ratio 0.9
srm_ srm-sparse-mismatch-stop 0 "SRM: STOP" "-"                  --na 0 --nb 40 --ratio 0.9
srm_ srm-zero-total         2 "positive total" "-"               --na 0 --nb 0
srm_ srm-sparse-50-a        0 "p 0.070312  -> ok" "STOP"         --na 1 --nb 7
srm_ srm-sparse-50-b        0 "p 0.070312  -> ok" "STOP"         --na 7 --nb 1 --ratio 0.5

if [ "$fail" -ne 0 ]; then echo "AB_STATS CASES FAILED"; exit 1; fi
echo "AB_STATS CASES OK ($n cases)"
