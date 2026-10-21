---
description: Audit a Google Ads account and show the findings as an approval page
argument-hint: [customer-id] [days]
---

Audit the Google Ads account in `$ARGUMENTS` (default 30 days; ask for the account only if more than one is accessible and none was given).

1. Call `ga_audit_account_tool` once with `customer_id` and `days` (pass `login_customer_id` for MCC accounts). Do not run the specialist audits unless the user asks.
2. Write the tool's result to `AUDIT.json` as it is.
3. Run `python3 "${CLAUDE_PLUGIN_ROOT}/skills/ppc-reporting/scripts/fill-dashboard.py" AUDIT.json ppc-audit.html --template "${CLAUDE_PLUGIN_ROOT}/skills/google-ads-audit/assets/audit.html"` (add `--artifact` for the Artifact tool). Do not read the template.
4. Publish or open `ppc-audit.html`.

Reply with the link or path, the estimated recoverable spend from the tool's own figure, and the count of proposed actions. The page lists every proposed action as an approval row; nothing is applied until the user names the rows to apply, and then only on a plan that allows writes (`ga_pause_keyword_tool`, `ga_add_negative_keywords_bulk_tool`).
