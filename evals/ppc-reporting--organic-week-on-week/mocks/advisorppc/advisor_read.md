---
expect:
  tool: sc_compare_periods_tool
---
{
  "site_url": "https://harborbakery.example/",
  "dimensions": [
    "query"
  ],
  "current_period": [
    "2026-11-20",
    "2026-11-27"
  ],
  "prev_period": [
    "2026-11-12",
    "2026-11-19"
  ],
  "row_count": 3,
  "rows": [
    {
      "query": "harbor bakery",
      "clicks_curr": 120,
      "clicks_prev": 98,
      "clicks_delta": 22,
      "impressions_curr": 900,
      "impressions_prev": 840,
      "impressions_delta": 60,
      "ctr_curr": 0.1333,
      "ctr_prev": 0.1167,
      "pos_curr": 1.1,
      "pos_prev": 1.2
    },
    {
      "query": "sourdough near me",
      "clicks_curr": 30,
      "clicks_prev": 25,
      "clicks_delta": 5,
      "impressions_curr": 2100,
      "impressions_prev": 1900,
      "impressions_delta": 200,
      "ctr_curr": 0.0143,
      "ctr_prev": 0.0132,
      "pos_curr": 9.2,
      "pos_prev": 9.6
    },
    {
      "query": "birthday cake order",
      "clicks_curr": 21,
      "clicks_prev": 19,
      "clicks_delta": 2,
      "impressions_curr": 400,
      "impressions_prev": 380,
      "impressions_delta": 20,
      "ctr_curr": 0.0525,
      "ctr_prev": 0.05,
      "pos_curr": 6.1,
      "pos_prev": 6.3
    }
  ]
}
