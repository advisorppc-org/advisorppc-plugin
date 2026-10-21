---
description: Build a shareable cross-platform PPC dashboard page from your connected accounts
argument-hint: [customer-id] [period, e.g. last_30_days or last_7_days]
---

Build the AdvisorPPC dashboard for the account and period in `$ARGUMENTS` (default last_30_days). Pick the account with `ga_accessible_customers_tool`; never a manager account (`is_manager`), list its clients with `ga_list_customer_clients_tool` instead, and ask only if more than one client fits. The period is a trailing window ending today; GA4, Search Console and YouTube tools take a day count, so a custom date range applies to Google Ads only and the page says so.

Follow the `ppc-reporting` skill's "Dashboard output" section exactly, and nothing else from it:

1. If the connector lists `ppc_dashboard_data_tool`, call it once and write its result to `advisorppc-reports/DATA.json` (the folder holds account data; keep it out of version control). Otherwise pull one rollup per platform as the skill's `references/dashboard-data.md` maps them, using the same window everywhere, and write the JSON yourself. A platform whose read comes back as not connected or as a plan denial (upgrade_required) is left out, and its name goes into `meta.warnings`; never stop the whole dashboard for one platform.
2. Run `python3 "${CLAUDE_PLUGIN_ROOT}/skills/ppc-reporting/scripts/fill-dashboard.py" advisorppc-reports/DATA.json advisorppc-reports/ppc-dashboard.html` (add `--artifact` when you will publish with the Artifact tool). Do not read the template.
3. Publish the page as an artifact when the Artifact tool exists, else open it from disk.

Reply with the link or path, the account, the window, the platforms left out and why, and the connector calls used. Keep it to four lines; the page carries the numbers.
