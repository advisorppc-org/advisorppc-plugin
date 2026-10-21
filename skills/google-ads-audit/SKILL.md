---
name: google-ads-audit
description: Structured, read-only audit of a real Google Ads account through the AdvisorPPC connector. Use when the user asks to "audit my Google Ads account", "review my campaigns", "find wasted spend", "check my search terms", "is my conversion tracking working", "why did my CPA go up", "what changed in my account", "check my quality scores" or wants any account or campaign health check. Confirms the account and checks tracking before trusting numbers, shows every metric as the tool's own card and table, and proposes changes without applying them.
---

# Google Ads account audit

Run a structured audit of a real Google Ads account with the AdvisorPPC connector. Every tool below is read-only: an audit never changes the account. For advisor judgment on what to do with the findings, the `ppc-strategist` skill takes over.

## Show the numbers the tool rendered

- Every metric answer shows the tool's KPI card and table from `content[0]` of the result, or rendered from `structuredContent.metrics_v1` when the host shows only data.
- One line of insight goes **above** the table. Never give numbers in prose alone and never retype a number a tool returned.
- If `metrics_v1.truncated` is true, call the table partial and take totals from the card.
- Money is in the account's own currency. Never assume USD.

## Audit workflow

Run the steps in order. Skip a step only when the user already gave the answer.

### 1. Confirm the account

- `list_google_connections_tool` shows which Google login is active and what it reaches. Switch with `select_google_connection_tool` if needed.
- `ga_accessible_customers_tool` (no inputs) returns the account tree with ids, names and manager flags. Under a manager (MCC), `ga_list_customer_clients_tool` lists the clients.
- Confirm the target `customer_id` with the user when more than one account fits. Ids are ten digits, no dashes. For a client reached through a manager, pass the manager as `login_customer_id`.

### 2. Check tracking before trusting numbers

- `ga_conv_tracking_health_tool`: orphaned conversion actions, volume drift, campaigns with clicks and no conversions.
- If the user has GA4 or GTM connected: `ga4_list_key_events_tool` and `gtm_audit_container_tool`.
- Put any tracking problem at the top of the audit as a **blocker** for reading performance.

### 3. Baseline and full scan

- `ga_account_performance_tool` with `date_range` (for example `last_30_days`). For "what changed", pull the previous period too and compare.
- `ga_audit_account_tool`: bidding, ad copy, quality score and tracking findings, prioritized.

### 4. Campaigns

- `ga_list_campaigns_tool`: ids, status, channel, bidding strategy, daily budget.
- `ga_campaign_performance_tool`: cost-sorted rows. Flag high cost with zero conversions, and CPA far above the account average.

### 5. Where the money goes

- `ga_find_wasted_spend_tool`: keywords, placements and terms spending with no conversions.
- `ga_search_terms_report_tool`: the actual queries. Propose irrelevant, costly, non-converting queries as negative candidates. Never propose brand, category or core-geo terms as negatives.
- `ga_keyword_performance_tool` (set `min_impressions` to cut noise) and `ga_quality_score_review_tool` (low quality score clustered by cause).
- `ga_list_ad_groups_tool`, `ga_list_ads_tool`, `ga_list_keywords_tool`: structure checks such as single-keyword ad groups, ad groups with no enabled ads, keyword and ad mismatch.

### 6. Google's signals and recent changes

- `ga_list_recommendations_tool`: report them; recommend only those that fit the user's goals.
- `ga_list_change_events_tool`: match performance shifts to change timestamps before blaming the market.
- `ga_auction_insights_tool`: whether a competitor moved in.

## Reporting the findings

Lead with a three-to-five line summary, then: tracking blockers, top findings ranked by monthly cost impact, and concrete next actions. Each action names what, why, expected impact, risk, and whether it needs approval. The audit itself applies nothing; on paid plans the user can approve specific changes afterwards.

## Gotchas

- Free plans have a monthly call allowance. Prefer rollups (`ga_account_performance_tool`, `ga_campaign_performance_tool`) over per-entity loops, and pass `limit`.
- A tool you need that is not in the list may be in the catalog: `advisor_search_tools`, then `advisor_tool_help`, then `advisor_read`.
