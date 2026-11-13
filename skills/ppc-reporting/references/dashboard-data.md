# Dashboard data and layout

The dashboard is one self-contained HTML page that Claude writes for each
report. All of its numbers come from one JSON object in the shape below, so the
page never shows a figure that a connector tool did not return. Every key maps
to one connector tool.

`meta` and `ads.current` are required. Every other key is optional and its
section is left out when the key is missing.

## `meta`

| Key | Value |
|---|---|
| `account`, `customer_id` | From `ga_list_accessible_customers_tool` (or the client row from `ga_list_customer_clients_tool`). |
| `currency` | ISO code from the Ads account (`currency_code`). Drives every money format. |
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
  of the same length. Fewer than two days: leave the charts out.
- `campaigns[]`: `ga_campaign_performance_tool`, cost-sorted. `name`, `status`
  (`ENABLED` | `PAUSED` | `REMOVED`), `cost`, `impressions`, `clicks`, `conversions`,
  `conversion_value`.
- `wasted_spend[]`: `ga_find_wasted_spend_tool` (or `ga_search_terms_report_tool`
  filtered to `conversions == 0`, cost-sorted, top 10). `search_term`, `campaign`,
  `cost`, `clicks`, `conversions`. An empty array: leave the section out.

## `ga4` (Google Analytics 4)

- `property`: display name from `ga4_list_properties_tool`.
- `key_events[]`: names from `ga4_list_key_events_tool`. Always pull this; the
  page explains that GA4 conversions are these events, not Ads conversions.
- `traffic_by_source[]`: `ga4_traffic_by_source_tool` for the period's day count.
  `source_medium`, `users`, `sessions`, `conversions`. Omit `ga4` to leave the section out.

## `search_console`

- `site`: from `sc_list_sites_tool`.
- `totals`, `previous`: `sc_compare_periods_tool` (or `sc_query_performance_tool`
  with no dimension, once per period). `clicks`, `impressions`, `ctr` (0 to 1), `position`.
- `top_queries[]`: `sc_top_queries_tool`. `query`, `clicks`, `impressions`, `ctr`, `position`.
  Omit `search_console` to leave the section out.

## `youtube`

- `channel`: from `yt_list_my_channels_tool`.
- `current`, `previous`: `yt_channel_stats_tool` once per period. `views`,
  `watch_time_hours`, `subscribers_gained`. Omit `youtube` to leave the section out.

## Page layout

Write the page in this order, one section per platform that has data:

1. **Header**: account name and customer ID, the period and the previous period
   it is compared with, the currency, the generated time, and the tool calls used
   when known.
2. **Paid performance · Google Ads**: KPI cards for cost, clicks, impressions,
   conversions, conversion value, CTR, CPC, CPA and ROAS, each with the change
   against the previous period (green when better, red when worse; for cost, CPC
   and CPA lower is better). Two small inline SVG charts from `ads.daily`: daily
   cost and daily conversions. Then a campaign table that sorts when a column
   header is clicked.
3. **Wasted spend**: the zero-conversion search terms with cost and clicks, the
   total cost they add up to, each labelled as a negative keyword candidate.
4. **Site behaviour · Google Analytics 4**: traffic by source/medium, and the
   key events list with one line saying GA4 conversions are these events, not
   Google Ads conversions.
5. **Organic search · Search Console**: clicks, impressions, CTR and average
   position with changes, then the top queries table.
6. **Video · YouTube**: views, watch time and subscribers gained with changes.

Rules for the page:

- One file. CSS in a `<style>` block, charts as inline SVG, and only the small
  amount of inline script the sortable table needs. No external scripts, fonts,
  images, trackers or network requests of any kind.
- Escape every account-supplied string (campaign names, search terms, queries,
  property and channel names) as HTML text: `&` `<` `>` `"` `'`. If the data is
  kept in a JSON `<script>` block, also write every `<` inside it as `\u003c` so
  no value can close the block.
- Format money with `meta.currency` and never mix currencies in one figure.
- Never put paid, GA4 and Search Console numbers in one total; they measure
  different things.
- Follow the system light or dark theme (`prefers-color-scheme`), use the system
  font stack, and keep the page readable on a phone width.
- Show only real numbers from the tools. If a figure is missing, leave its card
  out instead of showing zero.

## Budget of calls

A full dashboard costs about 12 connector calls: 2 Ads rollups, 1 daily, 1
campaigns, 1 wasted spend, 2 GA4, 3 Search Console, 2 YouTube. Skip platforms
the user has not connected rather than failing on them; leave out the section
of any platform whose key is missing.
