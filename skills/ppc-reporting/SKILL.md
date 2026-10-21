---
name: ppc-reporting
description: Cross-platform performance reports from the user's own Google Ads, Google Analytics 4, Search Console, YouTube and TikTok Ads accounts through the AdvisorPPC connector. Use when the user asks to "pull a performance report", "how did my ads do last month", "show me traffic by source", "top search queries", "compare this month to last month", "weekly report for my client", "YouTube channel stats", "how are my TikTok campaigns doing", "show me a dashboard" or "build my PPC dashboard". Every number is shown as the tool's own KPI card and table with a one-line insight above it.
argument-hint: "[customer-id] [period]"
---

# Cross-platform PPC reporting

Pull performance reports from the signed-in user's own accounts across Google Ads, Google Analytics 4, Search Console, YouTube and TikTok Ads with the AdvisorPPC connector. All tools here are read-only.

## Show the numbers the tool rendered

- Every metric answer shows the tool's KPI card and table from `content[0]` of the result, or rendered from `structuredContent.metrics_v1` (`columns`, `rows`, `totals`, `currency`, `period`) when the host shows only data.
- One line of insight goes **above** each table: what changed and why it matters.
- Never give numbers in prose alone, never retype a number a tool returned, and never sum numbers across platforms.
- If `metrics_v1.truncated` is true, call the table partial and take totals from the card.
- When the user wants to look at the numbers rather than read them, use the dashboard output below.

## Reporting workflow

1. Fix the period first (for example last 30 days, or a named month) and use the same period on every platform in the report.
2. Find the right ids with each platform's discovery tool (below). `list_google_connections_tool` shows which Google accounts the active login reaches.
3. Pull one rollup per platform, then tell one story: paid performance, then site behavior, then organic search, then video.
4. Show period-over-period change where the tool returns it. Money is in each account's own currency.

## Tools by platform

### Google Ads (paid)

- Discovery: `ga_accessible_customers_tool`, then `ga_list_customer_clients_tool` for clients under a manager.
- `ga_account_performance_tool`: account rollup for a `date_range`.
- `ga_campaign_performance_tool`: cost-sorted campaign rows; `segment_by_day=true` for a daily trend and the account currency.
- `ga_ad_performance_tool` and `ga_keyword_performance_tool`: ad and keyword rows.
- `ga_search_terms_report_tool`: the queries that bought traffic.

### Google Analytics 4 (site behavior)

- Discovery: `ga4_list_properties_tool` (ids, names, currencies).
- `ga4_run_report_tool`: general report with `property_id`, `metrics`, `dimensions`, `date_ranges`, `limit`.
- `ga4_traffic_by_source_tool`: source and medium with users, sessions, conversions.
- `ga4_realtime_tool`: "is the site getting traffic right now".
- `ga4_list_key_events_tool`: which conversions GA4 measures. Check it before comparing GA4 conversions with Ads conversions.

### Search Console (organic)

- Discovery: `sc_list_sites_tool`.
- `sc_query_performance_tool`: clicks, impressions, CTR, position by `dimensions`. For "this month vs last month", run it for both periods.
- `sc_top_queries_tool` and `sc_top_pages_tool`: leading queries and pages.
- `sc_inspect_url_tool`: index status of one URL when a page's traffic drop needs a technical reason.

### YouTube (video)

- Discovery: `yt_list_my_channels_tool`.
- `yt_channel_stats_tool`, `yt_top_videos_tool`, `yt_traffic_sources_tool`.

### TikTok Ads

- `tt_list_campaigns_tool`, `tt_account_performance_tool`, `tt_campaign_performance_tool`.

### When conversion numbers look wrong

Check measurement before re-pulling reports: `ga_conv_tracking_health_tool` for Google Ads, then `gtm_list_accounts_tool`, `gtm_list_containers_tool`, `gtm_list_tags_tool` (note paused tags) and `gtm_audit_container_tool`.

## Dashboard output

When the user asks for a dashboard, a visual report, or something to share with a client or a manager, render the report as the bundled dashboard instead of prose. It is a snapshot across every connected platform it covers (Google Ads, TikTok Ads, GA4, Search Console and YouTube), filled from this session's tool results. For a Google Ads board that refreshes itself live each time it is opened, use the `campaign-board` skill instead.

1. Pull the data as above, one rollup per platform, with the same period everywhere.
2. Write the numbers as one JSON file in the shape of `references/dashboard-data.md`, key by key. Do not read `assets/dashboard.html`; it is a template and costs nothing to fill.
3. Run `python3 "${CLAUDE_PLUGIN_ROOT}/skills/ppc-reporting/scripts/fill-dashboard.py" DATA.json OUT.html` (add `--artifact` when publishing with the Artifact tool). It merges the JSON into the template, escapes it, and marks the data as real.
4. Leave out any platform the user has not connected; the page hides a section whose key is missing.
5. Publish OUT.html as an artifact when the session has the Artifact tool, otherwise open it from disk in the browser. Say where it is and which period and account it covers.

The page shows paid (Google Ads and TikTok Ads, each under its own heading), site, organic and video figures under separate headings with period-over-period deltas, daily cost and conversion charts, a sortable campaign table, and the zero-conversion search terms as negative keyword candidates.

## Gotchas

- Paid (Ads), site (GA4) and organic (Search Console) numbers measure different things. Never sum them; give each channel its own heading.
- Free plans have a monthly call allowance: one rollup per platform, not loops, and use `limit`.
- A report you need that is not in the tool list may be in the catalog: `advisor_search_tools`, then `advisor_tool_help`, then `advisor_read`.
