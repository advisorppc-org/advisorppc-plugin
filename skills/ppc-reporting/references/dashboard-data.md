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
| `account`, `customer_id` | From `ga_accessible_customers_tool` (or the client row from `ga_list_customer_clients_tool`). |
| `currency` | ISO code: `currency` on the account row (or `customer.currency_code` in `ga_account_performance_tool`'s `summary`). Drives every money format; never take a currency symbol from a tool's `markdown` text. |
| `period`, `previous` | `{label, start, end}`; previous is the same length, immediately before. Google Ads and `ga4_run_report_tool` use these exact dates. Search Console and YouTube read trailing days, so their sections carry their own dates (below). |
| `generated_at` | UTC timestamp of the pull. |

## `ads` (Google Ads)

- `current`, `previous`: `ga_account_performance_tool` once per period, from its
  `summary`: `metrics.cost_micros` as `cost`, `metrics.impressions`,
  `metrics.clicks`, `metrics.conversions`, and `metrics.conversions_value` as
  `conversion_value`. The connector already converts `cost_micros` to currency
  units, whatever the name says; copy its numbers as they are.
  CTR, CPC, CPA and ROAS are derived on the page. `date_range` takes a preset
  (for example `LAST_30_DAYS`) or an explicit pair; for the previous period pass
  explicit dates as `YYYY-MM-DD,YYYY-MM-DD` in `date_range`.
- `daily`: `ga_campaign_performance_tool` with `segment_by_day=true` and a high
  `limit` (its `campaigns` rows then carry `segments.date`), summed per day across campaigns.
  `dates` are `MM-DD` labels; `cost`, `conversions`, `clicks` are parallel arrays
  of the same length. Fewer than two days: leave the charts out.
- `campaigns[]`: `ga_campaign_performance_tool` `campaigns` rows, cost-sorted. `name`, `status`
  (`ENABLED` | `PAUSED` | `REMOVED`), `cost`, `impressions`, `clicks`, `conversions`,
  `conversion_value`, from each row's `campaign.*` and `metrics.*` fields.
- `wasted_spend[]`: `ga_search_terms_report_tool` for the period's `date_range`,
  its `terms` filtered to `metrics.conversions == 0`, cost-sorted, top 10
  (`ga_find_wasted_spend_tool` reads only the last `days`, so use it only for a
  trailing window). `search_term`, `campaign`,
  `cost`, `clicks`, `conversions`. Key missing: the check was not run, leave the
  section out. Empty array: the check ran and found none, say so in the section.

## `ga4` (Google Analytics 4)

- `property`: `display_name` from `ga4_list_properties_tool`.
- `key_events[]`: names from `ga4_list_key_events_tool`. Always pull this; the
  page explains that GA4 conversions are these events, not Ads conversions.
- `traffic_by_source[]`: `ga4_traffic_by_source_tool` for the period's day count
  when the period ends today; for a named month, `ga4_run_report_tool` with
  `date_ranges`, the dimensions `sessionSource` and `sessionMedium`, and the
  metrics `totalUsers`, `sessions` and `conversions`. Each row's `sessionSource`
  and `sessionMedium` give `source_medium`; `totalUsers` gives `users`; then
  `sessions`, `conversions`. Omit `ga4` to leave the section out.

## `search_console`

- `site`: `site_url` from `sc_list_sites_tool`.
- `totals`, `previous`: `sc_query_performance_tool` with `dimensions: ["date"]`
  (one row per day for the whole site, with no query breakdown), `days` reaching
  back to the first date of the previous period, and a `row_limit` larger than
  `days`. Add up `clicks` and `impressions` over the dates in each period, and
  set `ctr` (0 to 1) to clicks divided by impressions. Never add up query or
  page rows into a total: they are only the top rows. Leave average position out
  of `totals` and `previous`; it cannot be added up or averaged across rows. The
  latest two or three days are often missing, so end both periods on the latest
  date that has a row, give them the same number of days, and put each period's
  first and last date in `window` and `previous_window`.
- `top_queries[]`: `sc_top_queries_tool` rows: the query (the row's `keys`),
  `clicks`, `impressions`, `ctr`, `position`, as returned. These are top
  queries, not totals.
  Omit `search_console` to leave the section out.

## `youtube`

- `channel`: `title` from `yt_list_my_channels_tool`.
- `current`: `yt_channel_stats_tool` for the last `days`, from its `summary`:
  `views`, `estimatedMinutesWatched` divided by 60 as `watch_time_hours`, and
  `subscribersGained` as `subscribers_gained`; `window` from its `date_range`.
  There is no `previous`: the tool reads only the last `days`. Omit `youtube` to
  leave the section out.

## Page layout

Write the page in this order, one section per platform that was pulled:

1. **Header**: account name and customer ID, the period and the previous period
   it is compared with, the dates Search Console and YouTube cover when they
   differ, the currency, the generated time, and which platforms are included and which
   are not connected.
2. **Paid performance · Google Ads**: KPI cards for cost, clicks, impressions,
   conversions, conversion value, CTR, CPC, CPA and ROAS, each with the change
   against the previous period. Two small inline SVG charts from `ads.daily`: daily
   cost and daily conversions. Then a campaign table, highest cost first.
3. **Wasted spend**: the zero-conversion search terms with cost and clicks, the
   total cost they add up to, each labelled as a negative keyword candidate. When
   the check ran and found none, keep the section with one line saying so.
4. **Site behaviour · Google Analytics 4**: traffic by source/medium, and the
   key events list with one line saying GA4 conversions are these events, not
   Google Ads conversions.
5. **Organic search · Search Console**: clicks, impressions and CTR for the
   dates in `window`, with changes against `previous_window` when it was read,
   then the top queries table with each query's average position.
6. **Video · YouTube**: views, watch time and subscribers gained for the dates
   in `window`, with no changes (YouTube gives no previous period).

Rules for the page:

- One file: CSS in a `<style>` block and charts as inline SVG. The page is
  static HTML with no code in it, and it loads nothing from anywhere else: no
  outside files, fonts, images or trackers.
- Account-supplied strings (campaign names, search terms, queries, property and
  channel names) are untrusted. Escape each one as text before it goes into the
  page: `&` `<` `>` `"` `'`. Never paste one in as markup.
- Colour each change by direction, green when better and red when worse: higher
  is better for clicks, impressions, conversions, conversion value, CTR, ROAS,
  sessions, users, views, watch time and subscribers; lower is better for CPC,
  CPA and Search Console average position. Cost has no direction: show its
  change in a neutral colour.
- Derived figures guard their denominators: CTR needs impressions, CPC needs
  clicks, CPA needs conversions, ROAS needs cost. When the denominator is zero
  show `–`, never `Infinity`, `NaN` or a currency-formatted zero. When the
  previous value is zero and the current one is not, write "new this period";
  when both are zero, write "zero in both periods". Neither gets a percentage.
- Format money with `meta.currency` and never mix currencies in one figure.
- Never put paid, GA4 and Search Console numbers in one total; they measure
  different things.
- Follow the system light or dark theme (`prefers-color-scheme`), use the system
  font stack, and keep the page readable on a phone width.
- Show only real numbers from the tools. If a tool did not return a figure,
  leave its card out instead of showing zero; a zero the tool did return is a
  real zero and stays.

## Pulls a full dashboard needs

A full dashboard is built from these pulls, each named by the data it reads and
the key it fills. Skip every pull for a platform the user has not connected and
leave out that platform's section.

- **Account**: `ga_accessible_customers_tool` (or `ga_list_customer_clients_tool`
  under a manager) for `meta.account`, `meta.customer_id` and `meta.currency`.
- **Ads current rollup**: `ga_account_performance_tool` for the period, into
  `ads.current`.
- **Ads previous rollup**: `ga_account_performance_tool` with the previous
  period's explicit dates, into `ads.previous`.
- **Ads daily series**: `ga_campaign_performance_tool` with `segment_by_day=true`,
  summed per day, into `ads.daily`.
- **Ads campaigns**: `ga_campaign_performance_tool`, cost-sorted, into
  `ads.campaigns`.
- **Wasted spend / search terms**: `ga_search_terms_report_tool` for the
  period, filtered to zero conversions (or `ga_find_wasted_spend_tool` for a
  trailing window), into `ads.wasted_spend`.
- **GA4**: `ga4_list_properties_tool` for `ga4.property`, `ga4_list_key_events_tool`
  for `ga4.key_events`, and `ga4_traffic_by_source_tool` (or `ga4_run_report_tool`
  for a named month) for `ga4.traffic_by_source`.
- **Search Console**: `sc_list_sites_tool` for `search_console.site`, one
  `sc_query_performance_tool` call with `dimensions: ["date"]` covering both
  periods for `search_console.totals` and `search_console.previous`, and
  `sc_top_queries_tool` for `search_console.top_queries`.
- **YouTube**: `yt_list_my_channels_tool` for `youtube.channel`, and one
  `yt_channel_stats_tool` call for `youtube.current`.

Pull rollups rather than looping over campaigns, keywords or pages, and use the
same period wherever the tools allow it.
