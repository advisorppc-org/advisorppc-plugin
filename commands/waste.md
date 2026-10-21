---
description: Find zero-conversion search terms and, on approval, add them as negative keywords
argument-hint: [customer-id] [date_range, e.g. last_30_days]
---

Find wasted search-term spend in the Google Ads account in `$ARGUMENTS` (default last_30_days). Pick the account with `ga_accessible_customers_tool`; never a manager account (`is_manager`), list its clients with `ga_list_customer_clients_tool` instead.

1. Call `ga_search_terms_report_tool` once (`customer_id`, `date_range`, `limit` 200; `login_customer_id` for MCC accounts). If the result is an error object, report it in one line and stop. Never use `ga_find_wasted_spend_tool` here; it scans the account's own keywords and proposes pauses, not negatives.
2. If the report's rows carry zero conversions in total, stop: say that the account recorded no conversions in the period, so no term can be judged, and suggest `ga_conv_tracking_health_tool` first.
3. Sum each search term across its rows (the report splits a term by ad group and match type). Keep terms whose summed conversions are 0 and summed cost is above zero, sorted by cost. Drop any term that contains the account's brand name or a campaign name word; list those separately as "kept, looks like brand or core". If nothing remains, say so and stop.
4. Show the remaining terms as one table grouped by campaign: number, search term, campaign, clicks, cost, with a total line, quoting the tool's figures as they are.
5. Ask one question: which numbers to add as campaign-level EXACT negatives (all, some by number, or none). Exact blocks only that query, which is the safe default; offer PHRASE only if the user asks.
6. Before writing, call `ga_list_campaigns_tool` with status ENABLED to map each campaign name to its `campaign_id` (the report carries names only; if two enabled campaigns share a name, ask which). Then repeat back the exact list you will send: campaign name and id, search term, match type, one line each, and the number of calls (one per term). Wait for a plain yes. Any other answer means no write.
7. On yes, call `ga_add_negative_keyword_tool` once per term with `customer_id`, `campaign_id`, `keyword_text` and `match_type`. If that tool is missing from the tool list (free plan) or the connector answers that the plan does not allow writes, give the list ready to paste into Google Ads, point to https://mcp.advisorppc.com/dashboard for plans, and stop. Never retry a denied write. A failed term does not stop the others; report each.
8. Report what was added per campaign and the spend those terms cost in the period.
