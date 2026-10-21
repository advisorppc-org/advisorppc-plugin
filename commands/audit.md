---
description: Audit a Google Ads account and show the findings as a review page
argument-hint: [customer-id] [days]
---

Audit the Google Ads account in `$ARGUMENTS` (default 30 days). Pick the account with `ga_accessible_customers_tool`; never use a manager account (`is_manager`) as the customer id, list its clients with `ga_list_customer_clients_tool` instead, and ask only if more than one client fits.

1. Call `ga_audit_account_tool` once with `customer_id` and `days` (`login_customer_id` for MCC accounts). Do not run the specialist audits unless the user asks.
2. If the result is an error object, report it in one line and stop. Otherwise write the result to `advisorppc-reports/AUDIT.json` unchanged (the folder holds account data; keep it out of version control).
3. Run `python3 "${CLAUDE_PLUGIN_ROOT}/skills/ppc-reporting/scripts/fill-dashboard.py" advisorppc-reports/AUDIT.json advisorppc-reports/ppc-audit.html --template "${CLAUDE_PLUGIN_ROOT}/skills/google-ads-audit/assets/audit.html"` (add `--artifact` for the Artifact tool). Do not read the template. The script sorts `proposed_actions` by severity and writes that order back to `AUDIT.json`, so page numbers are file numbers.
4. Publish or open the page. Reply with the link or path, the count of proposed actions, and the tool's own recoverable-spend figure in the account's currency if it reports one.

The page is for review. Applying rows is a separate step and only happens when the user names numbers:

- Read each named row from `AUDIT.json`. Show kind, reason, the keyword text and the campaign and ad group from the row's `params` and matching finding, one line per row. A row whose keyword text you cannot find is shown and skipped.
- A negative row with neither `params.ad_group_id` nor a campaign you can name from its finding: show it and skip it.
- A row with `params.ad_group_id` is ad-group scoped. Never apply it with a campaign-level tool. Use the connector's `advisor_write` door for `ga_add_ad_group_neg_kw_tool` (first call returns a preview, the second with confirm applies) or `ga_pause_keyword_tool` with the row's `ad_group_id` and `criterion_id`.
- Wait for a plain yes after the list and after each preview. Any other answer means no write.
- If the write tools are missing from the tool list or the connector answers that the plan does not allow writes, give the rows as a paste-ready list, point to https://mcp.advisorppc.com/dashboard for plans, and stop. Never retry a denied write.
