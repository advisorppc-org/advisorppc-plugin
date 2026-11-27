---
name: ppc-reporting
description: This skill should be used when the user asks to "pull a performance report", "how did my ads do last month", "show me traffic by source", "top search queries", "compare this month to last month", "YouTube channel stats", "show me a dashboard", "build my PPC dashboard", or wants marketing performance data from Google Ads, Google Analytics, Search Console, or YouTube via the AdvisorPPC connector.
metadata:
  version: "0.3.8"
---

# Cross-Platform PPC Reporting

Pull performance reports from the signed-in user's own accounts across Google Ads, Google Analytics 4, Search Console, and YouTube using the AdvisorPPC connector. Every tool this skill uses is read-only: it reads and proposes, and never applies changes itself (see "From a finding to a change" below).

## Reporting workflow

1. Pin the reporting period first (for example the last 30 days, or a named month) and say which dates each figure covers. Google Ads tools (`date_range`) and `ga4_run_report_tool` (`date_ranges`) take exact dates, so they can cover a named month and the period before it. Search Console, YouTube, `ga4_traffic_by_source_tool` and `ga_find_wasted_spend_tool` read only the last `days` up to today: label those figures "last N days" (Search Console can still be cut to exact dates, see "Search Console totals and periods" below).
2. Discover the right resource IDs before reporting (each platform has its own discovery tool — see below).
3. Pull each platform's report, then merge into one narrative: paid performance → site behavior → organic search → video.
4. Present real numbers, with period-over-period changes only where both periods were read over the same number of days. Monetary values are in the account's own currency.

## Tools by platform

Most tools below are listed in the session directly. If a tool named in this skill is not in your tool list (for example `sc_compare_periods_tool` or `gtm_list_triggers_tool`), find it with `advisor_search_tools` and run it with `advisor_read`, passing its name as `tool` and its inputs as `arguments`.

### Google Ads (paid performance)

- Discovery: `ga_accessible_customers_tool`, then `ga_list_customer_clients_tool` for MCC client accounts.
- `ga_account_performance_tool` — account-level rollup for a `date_range`.
- `ga_campaign_performance_tool` — cost-sorted campaign rows.
- `ga_keyword_performance_tool` — keyword-level traffic, cost, and CPA (`min_impressions` filters noise).
- `ga_search_terms_report_tool` — actual queries that generated paid traffic.

### Google Analytics 4 (site behavior)

- Discovery: `ga4_list_properties_tool` — property IDs and display names.
- `ga4_run_report_tool` — general reports: pass `property_id`, `metrics`, `dimensions`, `date_ranges`, `limit`.
- `ga4_traffic_by_source_tool` — source/medium rows with users, sessions, conversions and engagement rate for the last `days`. For a named month, use `ga4_run_report_tool` with `date_ranges` and the dimensions `sessionSource` and `sessionMedium` instead.
- `ga4_realtime_tool` — current active users, for "is the site getting traffic right now".
- `ga4_list_key_events_tool` — which conversion events the property actually measures; check this before reporting "conversions" from GA4.

### Search Console (organic search)

- Discovery: `sc_list_sites_tool` — verified sites and permission levels.
- `sc_query_performance_tool` — clicks, impressions, CTR and average position per row, for the `dimensions` you pass (`query`, `page`, `country`, `device`, `date`; with none it returns `query` rows), over the last `days`.
- `sc_top_queries_tool` / `sc_top_pages_tool` — the leading queries and pages over the last `days`. These are the top rows only, not the site's total.
- `sc_compare_periods_tool` — the top queries (or pages, with `dimensions`) for the last `days` against the same number of days before, with the change per row. Top rows only, not site totals.
- `sc_inspect_url_tool` — indexing and coverage detail for a single URL when a page's traffic drop needs a technical explanation.

**Search Console totals and periods.** Never add up query or page rows into a site total: they are only the top rows. For totals, call `sc_query_performance_tool` with `dimensions: ["date"]` and a `row_limit` larger than `days`; it returns one row per day for the whole site. Add up `clicks` and `impressions` over the dates in the period, and work out CTR as clicks divided by impressions. Never add up or average `position` across rows; leave it out of totals. For a named month, or a period and the one before it, set `days` to reach back to the first date you need and add up only the dates inside each period. The latest two or three days are often not in Search Console yet, so end both periods on the latest date that has a row, give them the same number of days, and say which dates each covers.

### YouTube (video)

- Discovery: `yt_list_my_channels_tool` — channels owned by the signed-in identity.
- `yt_channel_stats_tool` — views, estimated minutes watched, average view duration, and subscribers gained and lost for the last `days`. It returns no likes, comments or shares.
- `yt_top_videos_tool` — leading videos by views for the last `days`, with likes, comments and watch minutes per video.
- `yt_traffic_sources_tool` — where video views come from, with views and watch minutes per source.

YouTube tools read only the last `days` up to today and give no previous period, so report YouTube without period-over-period changes.

### Tag Manager (measurement verification)

When conversion numbers look wrong, verify the measurement layer instead of re-pulling reports: `gtm_list_accounts_tool` → `gtm_list_containers_tool` → `gtm_list_workspaces_tool` → `gtm_list_tags_tool` (note paused tags) and `gtm_list_triggers_tool`.

## Dashboard output

When the user asks for a dashboard, a visual report, or something to share with a client or a manager, build the report as one dashboard page instead of prose.

1. Pull the data as above, one rollup per platform, with the same period wherever the tools allow it (see step 1 of the workflow).
2. Collect the numbers as one JSON object in the shape of `references/dashboard-data.md`, key by key.
3. Write one self-contained HTML page from that object, following the layout in `references/dashboard-data.md`: inline CSS and inline SVG charts, nothing loaded from elsewhere, and every account-supplied text (campaign names, search terms, queries) escaped.
4. Leave out any platform the user has not connected; drop its section rather than showing empty numbers.
5. Publish the page as an artifact when the session has the Artifact tool, otherwise save it and open it from disk in the browser. Say where it is and which period and account it covers.

The page shows paid, site, organic and video figures under separate headings with period-over-period changes where both periods were read, daily cost and conversion charts, a campaign table sorted by cost, and the zero-conversion search terms as negative keyword candidates. Treat every metric answer this way when the user wants to look at numbers rather than read them.

## Gotchas

- Paid (Ads), behavioral (GA4), and organic (Search Console) numbers measure different things — never sum them; present each channel under its own heading.
- Money: take the currency from the account (`currency` on its row from `ga_accessible_customers_tool` or `ga_list_customer_clients_tool`, or `customer.currency_code` in a Google Ads performance result). A tool's `markdown` text can show a `$` sign whatever the account's currency, so never copy a currency symbol from it.
- The Free plan is read-only with no card required; `plan_tool` with action `"status"` shows the plan, what it includes and whether calls are available now. Pull one rollup per platform rather than looping over entities, and use `limit`/`row_limit` parameters.
- **From a finding to a change**: this skill only reads and proposes; it never applies a change itself. When the user asks to apply a fix, follow "Applying a change and plans" in the `getting-connected` skill.
- GA4 conversions depend on configured key events — confirm with `ga4_list_key_events_tool` before comparing GA4 conversions to Ads conversions.
