#!/usr/bin/env bash
# Proves check_skills.sh catches what it claims to: each blocked word in plain,
# underscore_joined and CamelCase form, each secret shape, an em dash, a name
# mismatch and an over-long description. Also proves a clean skill passes.
set -u
here="$(cd "$(dirname "$0")" && pwd)"
check="$here/check_skills.sh"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
fails=0

make_skill() {  # make_skill <dir> <name> <description> <body>
  mkdir -p "$1"
  printf -- '---\nname: %s\ndescription: %s\n---\n\n%s\n' "$2" "$3" "$4" > "$1/SKILL.md"
}

expect() {  # expect pass|fail <label> <body> [name] [description]
  local want="$1" label="$2" body="$3" name="${4:-demo}" desc="${5:-A demo skill.}"
  rm -rf "$tmp/s"; mkdir -p "$tmp/s"
  make_skill "$tmp/s/demo" "$name" "$desc" "$body"
  if bash "$check" "$tmp/s" >/dev/null 2>&1; then got=pass; else got=fail; fi
  if [ "$got" != "$want" ]; then
    printf 'SELFTEST FAIL %-40s wanted %s, got %s\n' "$label" "$want" "$got"; fails=$((fails + 1))
  fi
}

expect pass "clean skill" "Plain body that mentions Google Ads and mcp.advisorppc.com."

for word in atmosagi coolify dgx wind1 macone tariqul monzurul handoffs agentpass; do
  upper="$(printf '%s' "${word:0:1}" | tr '[:lower:]' '[:upper:]')${word:1}"
  expect fail "plain $word"       "see $word here"
  expect fail "underscore $word"  "see invalid_${word}_ref here"
  expect fail "CamelCase $word"   "see Some${upper}Error here"
done
for path in '/home/someone/x' '/Users/someone/x' '~/notes/x' 'creds.local.env' 'localhost:8000' '178.156.0.1' '/orchestra/runs'; do
  expect fail "path $path" "see $path here"
done

for secret in 'sk_live_abc123' 'ghp_abcdefghij' 'github_pat_abc' 'xoxb-123-abc' 'AKIAABCDEFGHIJKLMNOP' \
              'sk-ant-abc' '-----BEGIN RSA PRIVATE KEY' 'Bearer abcdefghijklmnopqrstuvwxyz'; do
  expect fail "secret ${secret:0:12}" "token $secret here"
done

expect fail "em dash" "one $(printf '—') two"
expect fail "name mismatch" "body" "other-name"
expect fail "description too long" "body" "demo" "$(printf 'x%.0s' $(seq 1 1100))"

if [ "$fails" -eq 0 ]; then echo "SELFTEST OK"; else echo "SELFTEST $fails failure(s)"; exit 1; fi
