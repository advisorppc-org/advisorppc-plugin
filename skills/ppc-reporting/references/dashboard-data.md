# Dashboard data contract

`assets/dashboard.html` is a self-contained page. All of its numbers come from one
JSON block, `<script id="ppc-data" type="application/json">`, so filling the
dashboard means replacing that block and nothing else. Every key below maps to
one connector tool. Write the JSON to a file and run
`scripts/fill-dashboard.py DATA.json OUT.html` (add `--artifact` for the Artifact
tool); the script escapes every `<` as `\u003c` so a search term or campaign
name can never close the script block, and it sets `meta.example` to false.
Never read the template into context; the script does the merge.

`meta` is required, plus at least one platform key. Every platform key is
optional and its section hides when the key is missing, so a TikTok-only or
GA4-only account renders just that section.

## `meta`

| Key | Value |
|---|---|
| `example` | `false` once real data is in. `true` shows the "Example data" chip. |
| `account`, `customer_id` | From `ga_accessible_customers_tool` (or the client row from `ga_list_customer_clients_tool`). |
| `currency` | ISO code from the Ads account (`currency_code`). Drives every Google Ads money format; TikTok uses `tiktok.currency`. |
| `period`, `previous` | `{label, start, end}`; previous is the same length, immediately before. Use the same period for every platform. |
| `generated_at` | UTC timestamp of the pull. |
| `tool_calls_used`, `tool_calls_quota` | Optional. Count the calls you made; quota 100 on the free tier. |

## `ads` (Google Ads)

- `current`, `previous`: `ga_account_performance_tool` once per period. Fields:
  `cost`, `impressions`, `clicks`, `conversions`, `conversion_value`. The connector
  already converts `cost_micros` to currency units; copy its numbers as they are.
  CTR, CPC, CPA and ROAS are derived on the page. `date_range` accepts a
  `BETWEEN` range, so the previous period is one extra call with explicit dates.
- `daily`: `ga_campaign_performance_tool` with `segment_by_day=true` and a high
  `limit` (daily rows carry `segments.date`), summed per day across campaigns.
  `dates` are `MM-DD` labels; `cost`, `conversions`, `clicks` are parallel arrays
  of the same length. Fewer than two days hides the charts.
- `campaigns[]`: `ga_campaign_performance_tool`, cost-sorted. `name`, `status`
  (`ENABLED` | `PAUSED` | `REMOVED`), `cost`, `impressions`, `clicks`, `conversions`,
  `conversion_value`.
- `wasted_spend[]`: `ga_find_wasted_spend_tool` (or `ga_search_terms_report_tool`
  filtered to `conversions == 0`, cost-sorted, top 10). `search_term`, `campaign`,
  `cost`, `clicks`, `conversions`. An empty array hides the section.

## `tiktok` (TikTok Ads)

- `advertiser`: display name and advertiser id from the TikTok connection.
- `currency`: the advertiser's ISO 4217 code (for example `JPY`) as
  `tt_account_performance_tool` or the advertiser record returns it. Every
  TikTok money cell is formatted in it, never in `meta.currency`. When the
  tool gives no currency, omit the key: the page then shows TikTok money
  without a symbol and labels it "currency unknown". Never copy the Google
  Ads currency here and never convert amounts.
- `current`, `previous`: `tt_account_performance_tool` once per period, with the
  same period as every other platform. Fields: `cost` (the tool's `spend`),
  `impressions`, `clicks`, `conversions`, and `conversion_value` when the tool
  returns it (spend times ROAS); without it the ROAS card is left out. CTR, CPC
  and CPA are derived on the page. The tool takes a `date_range_preset`; when no
  preset matches the previous period, omit `previous` and the cards show no
  delta. Never label a period of a different length as previous.
- `campaigns[]`: `tt_campaign_performance_tool` for the period, cost-sorted, with
  `status` joined from `tt_list_campaigns_tool` by campaign id. `name`, `status`
  (`ENABLE` | `DISABLE` | `DELETE`, as TikTok returns it), `cost`, `impressions`,
  `clicks`, `conversions`. Omit `tiktok` to hide the section.

TikTok and Google Ads are separate paid sections; the page never adds their
cost or conversions together, and each shows money in its own account currency.

## `ga4` (Google Analytics 4)

- `property`: display name from `ga4_list_properties_tool`.
- `key_events[]`: names from `ga4_list_key_events_tool`. Always pull this; the
  page explains that GA4 conversions are these events, not Ads conversions.
- `traffic_by_source[]`: `ga4_traffic_by_source_tool` for the period's day count.
  `source_medium`, `users`, `sessions`, `conversions`. Omit `ga4` to hide the section.

## `search_console`

- `site`: from `sc_list_sites_tool`.
- `totals`, `previous`: `sc_query_performance_tool` with no dimension, once per
  period. `clicks`, `impressions`, `ctr` (0 to 1), `position`.
- `top_queries[]`: `sc_top_queries_tool`. `query`, `clicks`, `impressions`, `ctr`, `position`.
  Omit `search_console` to hide the section.

## `youtube`

- `channel`: from `yt_list_my_channels_tool`.
- `current`, `previous`: `yt_channel_stats_tool` once per period. `views`,
  `watch_time_hours`, `subscribers_gained`. Omit `youtube` to hide the section.

## Budget of calls

A full dashboard costs about 16 connector calls: 2 Ads rollups, 1 daily, 1
campaigns, 1 wasted spend, 4 TikTok (2 rollups, 1 campaigns, 1 campaign list),
2 GA4, 3 Search Console, 2 YouTube. Skip platforms
the user has not connected rather than failing on them; the page hides any
section whose key is missing.
