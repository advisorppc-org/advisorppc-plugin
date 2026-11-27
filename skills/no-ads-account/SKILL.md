---
name: no-ads-account
description: This skill should be used when the user says "I don't have Google Ads", "I don't run ads", "I have no ad account", "it says I have no accounts", "no Google Ads accounts found", "can I use this without ads", "I only have Search Console", "I only have Google Analytics", "weekly check-in", or when the Google Ads account list from the AdvisorPPC connector comes back empty. It gives a first report from Search Console or Google Analytics 4 instead of stalling.
metadata:
  version: "0.3.8"
---

# No Google Ads Account

When the user has no Google Ads access, still give them one real report in this conversation, from Search Console or Google Analytics 4. Every tool here is read-only.

**Do not stall.** Do not keep asking the user to connect Google Ads, and do not pitch running ads. Start at step 1.

## 1. See what is connected

Call `sc_list_sites_tool` and `ga4_list_properties_tool` (both take no inputs).

If the user expected Google Ads accounts and the list was empty, add one line: the accounts may sit under another Google login. Linked logins are listed by `list_google_connections_tool` and chosen with `select_google_connection_tool`; new ones are linked in the dashboard at https://mcp.advisorppc.com/dashboard. Then carry on with the report.

## 2. Search Console first

Search Console shows the Google searches the site appeared for, so it is the nearest view to what an ad would target. When a site is listed:

1. Use the site the user names; with several sites and no name, ask which one.
2. Call `sc_top_queries_tool` with that `site_url`, `days: 28` and `row_limit: 10`. Add `sc_top_pages_tool` only if the user asks about pages.
3. Report the top five queries by clicks with impressions, CTR and average position, and the period. Call it organic search, never ad performance. These are the top queries, not the site's total, so do not add them up into one.
4. Add at most two observations the rows show, for example a query with many impressions and a low CTR, or a query sitting just below the first page. Name the query and its numbers.

## 3. Google Analytics 4 when there is no Search Console site

When no site is listed but a property is:

1. Use the property the user names; with several and no name, ask which one.
2. Call `ga4_traffic_by_source_tool` with that `property_id` and `days: 30`.
3. Report the top five source and medium rows with users and sessions, and the period.
4. Before reporting conversions, call `ga4_list_key_events_tool`. With no key events, say conversions are not measured yet instead of reporting zero.

## 4. Nothing connected

When neither a site nor a property is listed, show no numbers. Give one plain next step: link Search Console or Google Analytics in the dashboard at https://mcp.advisorppc.com/dashboard with the Google account that manages the website. If the site is in neither yet, suggest asking whoever runs the website to add it to Google Search Console. Offer to run the report as soon as the user says it is linked.

## 5. Offer a weekly check-in

End with one line the user can reuse: "Say 'weekly check-in' any time and I'll pull this report for the latest week." When the user says it, run the same report with `days: 7`, and compare only with figures already in this conversation that cover the same number of days. Nothing is scheduled: never say you will remind the user, run on your own, or check back later.

## Gotchas

- Report only numbers a tool returned in this conversation. Search Console and GA4 measure different things: never add them together, and never present either as ad results.
- Plan questions: call `plan_tool` with action `"status"` and quote what it returns. Never state a plan name, price or allowance that a tool result did not give. For prices the tool does not show, give https://mcp.advisorppc.com/pricing.
- Never ask for or accept a password, key or token in chat; sign-in is in the browser only.
- If Google Ads accounts appear later, hand over to `ppc-reporting` or `google-ads-audit`.
- If a tool named in this skill is not in your tool list, find it with `advisor_search_tools` and run it with `advisor_read`, passing its name as `tool` and its inputs as `arguments`.
