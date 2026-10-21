---
description: Find zero-conversion search terms and, on approval, add them as negative keywords
argument-hint: [customer-id] [date_range, e.g. last_30_days]
---

Find wasted search-term spend in the Google Ads account in `$ARGUMENTS` (default last_30_days; ask for the account only if more than one is accessible and none was given).

1. Call `ga_search_terms_report_tool` once (`customer_id`, `date_range`, `limit` 200; `login_customer_id` for MCC accounts). This is the only correct source: it returns the queries people typed. Never use `ga_find_wasted_spend_tool` here; it scans the account's own keywords and its proposals are keyword pauses, not negatives.
2. Keep rows with `conversions` equal to 0 and cost above zero, sorted by cost. Show them as one table grouped by campaign: number, search term, campaign, clicks, cost, with a total line. If none qualify, say so and stop.
3. Ask one question: which numbers to add as campaign-level PHRASE negatives (all, some by number, or none).
4. Before writing, repeat back the exact list you will send: campaign, search term, match type, one line each, and the number of calls (one per term). Wait for a plain yes. Any other answer means no write.
5. On yes, call `ga_list_campaigns_tool` once to map each campaign name from the report to its `campaign_id` (the search terms report carries names only; if two campaigns share a name, ask which). Then call `ga_add_negative_keyword_tool` once per term with `campaign_id`, the term as `text` and `match_type` PHRASE. If the connector answers that the plan does not allow writes, say so in one line, give the list ready to paste into Google Ads, point to https://mcp.advisorppc.com/dashboard for plans, and stop. Never retry a denied write.
6. Report what was added per campaign and the spend those terms cost in the period.
