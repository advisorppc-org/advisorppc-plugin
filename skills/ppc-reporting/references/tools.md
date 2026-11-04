# Tools by platform

Read this when you need the connector tool for a platform you are reporting on.
Every tool here is read-only. AdvisorPPC is Google-first; the same connector can
also connect Meta, Microsoft Advertising, TikTok, LinkedIn, Pinterest and X, and
an operation that is not in the tool list is found with `advisor_search_tools`,
then `advisor_tool_help`, then `advisor_read`.

## Google Ads (paid performance)

- Discovery: `ga_accessible_customers_tool`, then `ga_list_customer_clients_tool` for MCC client accounts.
- `ga_account_performance_tool`: account-level rollup for a `date_range`.
- `ga_campaign_performance_tool`: cost-sorted campaign rows.
- `ga_keyword_performance_tool`: keyword-level traffic, cost and CPA (`min_impressions` filters noise).
- `ga_search_terms_report_tool`: the actual queries that generated paid traffic.

## Google Analytics 4 (site behavior)

- Discovery: `ga4_list_properties_tool`: property IDs, names, currencies.
- `ga4_run_report_tool`: general reports; pass `property_id`, `metrics`, `dimensions`, `date_ranges`, `limit`.
- `ga4_traffic_by_source_tool`: source/medium rows with users, sessions and conversions for the last `days`.
- `ga4_realtime_tool`: current active users, for "is the site getting traffic right now".
- `ga4_list_key_events_tool`: which conversion events the property actually measures; check this before reporting "conversions" from GA4.

## Search Console (organic search)

- Discovery: `sc_list_sites_tool`: verified sites and permission levels.
- `sc_query_performance_tool`: clicks, impressions, CTR and position by chosen `dimensions`; for "compare this month to last month" on organic, call it once per period and show the change.
- `sc_top_queries_tool` / `sc_top_pages_tool`: leading queries and pages for the period.
- `sc_inspect_url_tool`: indexing and coverage detail for a single URL when a page's traffic drop needs a technical explanation.

## YouTube (video)

- Discovery: `yt_list_my_channels_tool`: channels owned by the signed-in identity.
- `yt_channel_stats_tool`: views, watch time, subscribers and engagement for `days`.
- `yt_top_videos_tool`: leading videos in the period.
- `yt_traffic_sources_tool`: where video views come from.

## TikTok Ads (paid social, read-only)

- `tt_list_campaigns_tool`, `tt_campaign_performance_tool`, `tt_account_performance_tool`.

## Tag Manager (measurement verification)

When conversion numbers look wrong, verify the measurement layer instead of re-pulling reports:
`gtm_list_accounts_tool`, then `gtm_list_containers_tool`, then `gtm_list_workspaces_tool`, then
`gtm_list_tags_tool` (note paused tags). `gtm_audit_container_tool` checks a whole container in one call.
