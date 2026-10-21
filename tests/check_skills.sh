#!/usr/bin/env bash
# Checks every bundled skill before it ships.
#
#   - SKILL.md opens with frontmatter whose `name` equals the skill's folder
#   - `description` is present and under 1024 characters
#   - no em dash anywhere under skills/
#   - no secret-shaped string anywhere under skills/
#   - no internal hostname, machine name, person name or private path
#
# Usage: tests/check_skills.sh [skills-dir]   (default: skills/ next to this file)
# Exit 0 when every check passes, 1 otherwise. Needs bash, grep -P and python3.
set -u

root="${1:-$(cd "$(dirname "$0")/.." && pwd)/skills}"
fail=0
err() { printf 'FAIL %s\n' "$*"; fail=1; }

[ -d "$root" ] || { echo "FAIL no skills directory at $root"; exit 1; }

count=0
for dir in "$root"/*/; do
  dir="${dir%/}"
  folder="$(basename "$dir")"
  skill="$dir/SKILL.md"
  count=$((count + 1))
  if [ ! -f "$skill" ]; then err "$folder: no SKILL.md"; continue; fi

  # Frontmatter: name and description, parsed without third-party modules.
  out="$(python3 -I - "$skill" <<'PY'
import sys
text = open(sys.argv[1], encoding="utf-8").read()
if not text.startswith("---\n"):
    print("ERR no frontmatter at line 1"); sys.exit()
end = text.find("\n---\n", 4)
if end < 0:
    print("ERR frontmatter not closed"); sys.exit()
fields = {}
for line in text[4:end].splitlines():
    if ":" in line and not line.startswith((" ", "\t")):
        key, _, value = line.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
print("NAME", fields.get("name", ""))
print("DESC", len(fields.get("description", "")))
print("LINES", text.count("\n") + 1)
PY
)"
  case "$out" in ERR*) err "$folder: ${out#ERR }"; continue ;; esac
  name="$(printf '%s\n' "$out" | sed -n 's/^NAME //p')"
  dlen="$(printf '%s\n' "$out" | sed -n 's/^DESC //p')"
  lines="$(printf '%s\n' "$out" | sed -n 's/^LINES //p')"
  [ "$name" = "$folder" ] || err "$folder: frontmatter name '$name' does not match the folder"
  [ "${dlen:-0}" -gt 0 ] || err "$folder: description is missing"
  [ "${dlen:-0}" -lt 1024 ] || err "$folder: description is $dlen characters (limit 1023)"
  [ "${lines:-0}" -le 500 ] || err "$folder: SKILL.md is $lines lines (keep it under 500; move detail to references/)"
done
[ "$count" -gt 0 ] || err "no skills found under $root"

# Text-level fences over every file under skills/.
scan() {  # scan <label> <perl-regex>
  local hits
  hits="$(grep -rnIP -- "$2" "$root" 2>/dev/null | cut -c1-200)"
  [ -z "$hits" ] || { err "$1:"; printf '%s\n' "$hits" | sed 's/^/    /'; }
}

scan "em dash" $'—'

scan "secret-shaped string" \
  '(sk_live_|sk_test_|rk_live_|whsec_|ghp_|gho_|ghs_|github_pat_|xox[abpr]-|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|sk-ant-|-----BEGIN [A-Z ]*PRIVATE KEY|[Bb]earer [A-Za-z0-9._-]{20,})'

# Case-insensitive substrings, deliberately without word boundaries, so a
# blocked word is caught plain, underscore_joined or CamelCased.
scan "internal hostname, machine, person or private path" \
  '(?i)(/home/|/Users/|~/|\.local\.env|atmosagi|coolify|localhost:8000|178\.156\.|178\.105\.|dgx|wind1|macone|mac-one|mac_one|macair|mac-air|mac_air|tariqul|monzurul|handoffs|orchestra/|engineering-library|agentpass|house-backup)'

if [ "$fail" -eq 0 ]; then
  echo "OK $count skills checked under $root"
fi
exit "$fail"
