#!/usr/bin/env bash
# Fills the ppc-reporting dashboard with fixed cases through the real
# fill-dashboard.py and checks the rendered page with tests/dashboard_probe.cjs:
# each platform's money shows in that platform's own currency, TikTok without a
# currency says so instead of borrowing the Google Ads one, and pages without a
# TikTok block render Google Ads as before.
#
# Usage: tests/check_dashboard.sh [dashboard.html]   (default: the shipped template)
# Exit 0 when every case passes, 1 otherwise. Needs bash, python3 and node.
set -u
here="$(cd "$(dirname "$0")" && pwd)"
skill="$here/../skills/ppc-reporting"
template="${1:-$skill/assets/dashboard.html}"
probe="$here/dashboard_probe.cjs"
command -v node >/dev/null || { echo "FAIL node is required"; exit 1; }
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

# A private copy of the skill so a candidate template is filled by the real script.
mkdir -p "$tmp/skill/assets" "$tmp/skill/scripts" "$tmp/out"
cp "$skill/scripts/fill-dashboard.py" "$tmp/skill/scripts/"
cp "$template" "$tmp/skill/assets/dashboard.html"

fail=0
for case in mixed tiktok-only tiktok-unknown google-only hostile; do
  node "$probe" fixture "$case" > "$tmp/out/$case.json" || { echo "FAIL $case: no fixture"; fail=1; continue; }
  python3 -I "$tmp/skill/scripts/fill-dashboard.py" "$tmp/out/$case.json" "$tmp/out/$case.html" >/dev/null \
    || { echo "FAIL $case: fill-dashboard.py"; fail=1; continue; }
  node "$probe" check "$tmp/out/$case.html" "$case" || fail=1
done
[ "$fail" -eq 0 ] && echo "DASHBOARD OK"
exit "$fail"
