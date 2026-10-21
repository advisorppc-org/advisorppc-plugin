# AdvisorPPC tools

The connector's tool list on Claude (`https://mcp.advisorppc.com/claude`), read from a live `tools/list` on 2026-10-21: 65 tools. Plans decide which ones run; a refused call says why. In Claude Code a plugin tool shows with a prefix such as `mcp__plugin_advisorppc_advisorppc__`; the bare names below are the part after it.

Everything not listed here is a catalog operation. Find it with `advisor_search_tools` (keywords), read its inputs with `advisor_tool_help`, and run it with `advisor_read` (read-only) or `advisor_write` (changes; previews first, applies only with `confirm=true`). The catalog only shows operations the user's plan includes.

## Connection and account identity

| Tool | Use it for |
|---|---|
| `list_google_connections_tool` | Which Google logins are connected and which Ads, GA4, GTM, Search Console, Merchant Center and YouTube accounts each reaches |
| `select_google_connection_tool` | Switch the Google login later calls run under |
| `ga_accessible_customers_tool` | Google Ads account tree (direct, manager, client), no inputs |
| `ga_list_customer_clients_tool` | Client accounts under a manager (MCC) |
| `connect_platform_tool` | Start connecting a platform; returns the sign-in link |
| `connector_help_tool` | How to add the connector to other apps |
| `health_check_tool` | Is each connected platform responding |
| `advisor_apps_status_tool` | Status of AdvisorPPC's own services |

## Google Ads reads and audits

| Tool | Use it for |
|---|---|
| `ga_account_performance_tool` | Account rollup for a date range |
| `ga_campaign_performance_tool` | Cost-sorted campaign rows; `segment_by_day` for trends and currency |
| `ga_ad_performance_tool` | Per-ad performance, spend-sorted |
| `ga_keyword_performance_tool` | Keyword cost, conversions, CPA |
| `ga_search_terms_report_tool` | The queries that triggered ads |
| `ga_list_campaigns_tool` | Campaign ids, status, channel, bidding, daily budget |
| `ga_list_ad_groups_tool`, `ga_list_ads_tool`, `ga_list_keywords_tool` | Structure checks; ads carry final URLs |
| `ga_list_recommendations_tool` | Google's own recommendations |
| `ga_list_change_events_tool` | Who changed what, and when |
| `ga_auction_insights_tool` | Competitors in the same auctions |
| `ga_audit_account_tool` | Full audit: bidding, ad copy, quality score, tracking |
| `ga_conv_tracking_health_tool` | Orphaned conversion actions, volume drift, no-conversion campaigns |
| `ga_find_wasted_spend_tool` | Keywords, placements and terms spending with no conversions |
| `ga_quality_score_review_tool` | Low quality-score keywords clustered by cause |
| `ga_keyword_research_tool` | Keyword Planner ideas and historical metrics (`action="explain"` first) |

## Google Ads writes (paid plans)

These apply on the first call. Confirm the exact change with the user first, except the safe pauses in the main skill.

| Tool | Use it for |
|---|---|
| `ga_pause_campaign_tool`, `ga_enable_campaign_tool` | Campaign status |
| `ga_pause_ad_group_tool`, `ga_enable_ad_group_tool` | Ad group status |
| `ga_pause_keyword_tool`, `ga_enable_keyword_tool` | Keyword status |
| `ga_update_camp_budget_tool` | Daily budget in account currency (a shared budget changes every campaign on it) |
| `ga_update_ad_group_cpc_tool` | Ad group default CPC |
| `ga_add_keywords_tool` | Add keywords |
| `ga_add_negative_keyword_tool` | One campaign-level negative (negatives do not block close variants) |

## Google Analytics 4

| Tool | Use it for |
|---|---|
| `ga4_list_properties_tool` | Property ids, names, currencies |
| `ga4_run_report_tool` | General report: metrics, dimensions, date ranges |
| `ga4_traffic_by_source_tool` | Source and medium with users, sessions, conversions |
| `ga4_realtime_tool` | Active users right now |
| `ga4_list_key_events_tool` | Which conversions the property actually measures |

## Tag Manager

| Tool | Use it for |
|---|---|
| `gtm_list_accounts_tool`, `gtm_list_containers_tool`, `gtm_list_workspaces_tool` | Find the container for a site |
| `gtm_list_tags_tool` | Tags, including paused ones |
| `gtm_audit_container_tool` | Unfired tags, unused triggers, setup issues |

## Search Console and SEO

| Tool | Use it for |
|---|---|
| `sc_list_sites_tool` | Verified sites and permission levels |
| `sc_query_performance_tool` | Clicks, impressions, CTR, position by dimension |
| `sc_top_queries_tool`, `sc_top_pages_tool` | Leading queries and pages |
| `sc_inspect_url_tool` | Index status of one URL |
| `seo_page_audit_tool` | On-page audit of a live URL from its real HTML |
| `seo_core_web_vitals_tool` | Field and lab Core Web Vitals for a URL |
| `seo_keyword_intent_brief_tool` | Brief for classifying seed keywords by intent |

## YouTube and TikTok

| Tool | Use it for |
|---|---|
| `yt_list_my_channels_tool`, `yt_channel_stats_tool`, `yt_top_videos_tool`, `yt_traffic_sources_tool` | Channel discovery, stats, top videos, traffic sources |
| `tt_list_campaigns_tool`, `tt_account_performance_tool`, `tt_campaign_performance_tool` | TikTok Ads campaigns and performance |

## Catalog runners

| Tool | Use it for |
|---|---|
| `advisor_search_tools` | Find any other operation by keyword |
| `advisor_tool_help` | One operation's description and inputs |
| `advisor_read` | Run a read-only operation |
| `advisor_write` | Run a changing operation: preview, then `confirm=true` after approval |
| `advisor_cancel_removal` | Undo a scheduled removal inside its 90-minute window |

Catalog operations the playbooks use often (names verified 2026-10-21): `ga_disapproved_ads_tool`, `ga_ad_diagnosis_tool`, `ga_pause_ad_tool`, `ga_conv_source_integrity_tool`, `ga_alert_conv_drift_tool`, `ga_landing_page_perf_tool`, `ga_rsa_asset_performance_tool`, `ga4_list_data_streams_tool`, `ga_run_gaql_tool`.
