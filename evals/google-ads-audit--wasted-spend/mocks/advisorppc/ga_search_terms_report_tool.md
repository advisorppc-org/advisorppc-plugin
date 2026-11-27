---
expect:
  customer_id: /^4455667788$/
---
{
  "customer_id": "4455667788",
  "date_range": "LAST_30_DAYS",
  "count": 5,
  "terms": [
    {
      "search_term_view.search_term": "sourdough delivery",
      "segments.search_term_match_type": "PHRASE",
      "campaign.id": 111,
      "campaign.name": "Search - Bakery",
      "ad_group.id": 1001,
      "ad_group.name": "Bakery",
      "metrics.impressions": 2900,
      "metrics.clicks": 150,
      "metrics.cost_micros": 240.5,
      "metrics.conversions": 14.0
    },
    {
      "search_term_view.search_term": "birthday cake order",
      "segments.search_term_match_type": "PHRASE",
      "campaign.id": 222,
      "campaign.name": "Search - Cakes",
      "ad_group.id": 2001,
      "ad_group.name": "Cakes",
      "metrics.impressions": 1500,
      "metrics.clicks": 70,
      "metrics.cost_micros": 118.4,
      "metrics.conversions": 6.0
    },
    {
      "search_term_view.search_term": "harbor bakery",
      "segments.search_term_match_type": "EXACT",
      "campaign.id": 111,
      "campaign.name": "Search - Bakery",
      "ad_group.id": 1001,
      "ad_group.name": "Bakery",
      "metrics.impressions": 900,
      "metrics.clicks": 88,
      "metrics.cost_micros": 96.1,
      "metrics.conversions": 11.0
    },
    {
      "search_term_view.search_term": "free bread recipe",
      "segments.search_term_match_type": "BROAD",
      "campaign.id": 111,
      "campaign.name": "Search - Bakery",
      "ad_group.id": 1001,
      "ad_group.name": "Bakery",
      "metrics.impressions": 2400,
      "metrics.clicks": 61,
      "metrics.cost_micros": 84.2,
      "metrics.conversions": 0.0
    },
    {
      "search_term_view.search_term": "bakery jobs",
      "segments.search_term_match_type": "BROAD",
      "campaign.id": 111,
      "campaign.name": "Search - Bakery",
      "ad_group.id": 1001,
      "ad_group.name": "Bakery",
      "metrics.impressions": 1300,
      "metrics.clicks": 38,
      "metrics.cost_micros": 52.75,
      "metrics.conversions": 0.0
    }
  ],
  "markdown": "## Search terms — LAST_30_DAYS\n\n| # | Search term | Campaign | Spend | Conv |\n|---|---|---|---:|---:|\n| 1 | sourdough delivery | Search - Bakery | $240.50 | 14 |\n| 2 | birthday cake order | Search - Cakes | $118.40 | 6 |\n| 3 | harbor bakery | Search - Bakery | $96.10 | 11 |\n| 4 | free bread recipe | Search - Bakery | $84.20 | 0 |\n| 5 | bakery jobs | Search - Bakery | $52.75 | 0 |"
}
