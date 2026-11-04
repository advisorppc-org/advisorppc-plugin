---
name: ppc-reporting
description: This skill should be used when the user asks to "pull a performance report", "how did my ads do last month", "show me traffic by source", "top search queries", "compare this month to last month", "YouTube channel stats", "show me a dashboard", "build my PPC dashboard", or wants marketing performance data from Google Ads, Google Analytics, Search Console, or YouTube via the AdvisorPPC connector.
version: 0.4.0
---

# Cross-Platform PPC Reporting

Pull performance reports from the signed-in user's own accounts across Google Ads, Google Analytics 4, Search Console, and YouTube using the AdvisorPPC connector. All tools are read-only.

## Reporting workflow

1. Pin the reporting period first (for example last 30 days, or a named month). Use the same period across every platform in one report.
2. Discover the right resource IDs before reporting (each platform has its own discovery tool — see below).
3. Pull each platform's report, then merge into one narrative: paid performance → site behavior → organic search → video.
4. Present real numbers with period-over-period deltas where available. Monetary values are in the account's own currency.

## Tools by platform

### Google Ads (paid performance)

- Discovery: `ga_accessible_customers_tool`, then `ga_list_customer_clients_tool` for MCC client accounts.
- `ga_account_performance_tool` — account-level rollup for a `date_range`.
- `ga_campaign_performance_tool` — cost-sorted campaign rows.
- `ga_keyword_performance_tool` — keyword-level traffic, cost, and CPA (`min_impressions` filters noise).
- `ga_search_terms_report_tool` — actual queries that generated paid traffic.

### Google Analytics 4 (site behavior)

- Discovery: `ga4_list_properties_tool` — property IDs, names, currencies.
- `ga4_run_report_tool` — general reports: pass `property_id`, `metrics`, `dimensions`, `date_ranges`, `limit`.
- `ga4_traffic_by_source_tool` — source/medium rows with users, sessions, conversions for the last `days`.
- `ga4_realtime_tool` — current active users, for "is the site getting traffic right now".
- `ga4_list_key_events_tool` — which conversion events the property actually measures; check this before reporting "conversions" from GA4.

### Search Console (organic search)

- Discovery: `sc_list_sites_tool` — verified sites and permission levels.
- `sc_query_performance_tool` — clicks, impressions, CTR, position by chosen `dimensions`.
- `sc_top_queries_tool` / `sc_top_pages_tool` — leading queries and pages for the period.
- `sc_compare_periods_tool` — current vs previous period with change columns; the default choice for "compare this month to last month" on organic.
- `sc_inspect_url_tool` — indexing and coverage detail for a single URL when a page's traffic drop needs a technical explanation.

### YouTube (video)

- Discovery: `yt_list_my_channels_tool` — channels owned by the signed-in identity.
- `yt_channel_stats_tool` — views, watch time, subscribers, engagement for `days`.
- `yt_top_videos_tool` — leading videos in the period.
- `yt_traffic_sources_tool` — where video views come from.

### Tag Manager (measurement verification)

When conversion numbers look wrong, verify the measurement layer instead of re-pulling reports: `gtm_list_accounts_tool` → `gtm_list_containers_tool` → `gtm_list_workspaces_tool` → `gtm_list_tags_tool` (note paused tags) and `gtm_list_triggers_tool`.

## Dashboard output

When the user asks for a dashboard, a visual report, or something to share with a client or a manager, render the report as the bundled dashboard instead of prose.

1. Call `ppc_dashboard_data_tool` once with `customer_id` and `date_range` (plus `login_customer_id` for an MCC client, and `ga4_property_id`, `sc_site_url` or `yt_channel_id` when the user has several). Its result is already the whole `references/dashboard-data.md` block: write it to DATA.json as it is, nothing recomputed. Read `meta.warnings` and tell the user which platform was skipped and why. Only when that tool is missing from the connector, pull the data platform by platform as above, one rollup each, the same period everywhere.
2. When you filled DATA.json by hand, keep to the shape of `references/dashboard-data.md`, key by key. Do not read `assets/dashboard.html`; it is a template and costs nothing to fill.
3. Run `python3 <skill dir>/scripts/fill-dashboard.py DATA.json OUT.html` (add `--artifact` when publishing with the Artifact tool). It merges the JSON into the template, escapes it, and marks the data as real.
4. Leave out any platform the user has not connected; the page hides a section whose key is missing.
5. Publish OUT.html as an artifact when the session has the Artifact tool, otherwise open it from disk in the browser. Say where it is and which period and account it covers.

The page shows paid, site, organic and video figures under separate headings with period-over-period deltas, daily cost and conversion charts, a sortable campaign table, and the zero-conversion search terms as negative keyword candidates. Treat every metric answer this way when the user wants to look at numbers rather than read them.

## Gotchas

- Paid (Ads), behavioral (GA4), and organic (Search Console) numbers measure different things — never sum them; present each channel under its own heading.
- The free tier has a monthly call allowance (20 calls by default; the connector tells you when it is spent). A dashboard through `ppc_dashboard_data_tool` costs one call; otherwise pull one rollup per platform rather than looping over entities, and use `limit`/`row_limit` parameters.
- GA4 conversions depend on configured key events — confirm with `ga4_list_key_events_tool` before comparing GA4 conversions to Ads conversions.
