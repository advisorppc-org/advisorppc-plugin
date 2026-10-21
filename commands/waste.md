---
description: Find zero-conversion search terms and, on approval, add them as negative keywords
argument-hint: [customer-id] [days]
---

Find wasted spend in the Google Ads account in `$ARGUMENTS` (default 30 days).

1. Call `ga_find_wasted_spend_tool` once. Show the result as one table: search term, campaign, clicks, cost, with a total line. Group by campaign.
2. Ask one question: which rows to add as campaign-level PHRASE negatives (all, some by number, or none).
3. On a yes, call `ga_add_negative_keywords_bulk_tool` once per campaign with the chosen terms. If the connector answers that the plan does not allow writes, say so in one line, give the list ready to paste into Google Ads, and point to https://mcp.advisorppc.com/dashboard for plans. Never retry a denied write.
4. Report what was added, per campaign, and the spend those terms cost in the period.
