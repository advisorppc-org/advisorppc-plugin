---
description: Build a shareable cross-platform PPC dashboard page from your connected accounts
argument-hint: [customer-id] [period, e.g. last_30_days or 2026-09-01..2026-09-30]
---

Build the AdvisorPPC dashboard for the account and period in `$ARGUMENTS` (ask for the account only if more than one is accessible and none was given; default period last_30_days).

Follow the `ppc-reporting` skill's "Dashboard output" section exactly, and nothing else from it:

1. If the connector lists `ppc_dashboard_data_tool`, call it once and write its result to `DATA.json`. Otherwise pull one rollup per platform as the skill's `references/dashboard-data.md` maps them (about 12 calls), using the same period everywhere, and write the JSON yourself.
2. Run `python3 "${CLAUDE_PLUGIN_ROOT}/skills/ppc-reporting/scripts/fill-dashboard.py" DATA.json ppc-dashboard.html` (add `--artifact` when you will publish with the Artifact tool). Do not read the template.
3. Publish `ppc-dashboard.html` as an artifact when the Artifact tool exists, else open it from disk.

Reply with the link or path, the account, the period, and the connector calls used. Keep it to three lines; the page carries the numbers.
