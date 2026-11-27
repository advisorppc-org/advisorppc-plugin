---
expect:
  customer_id: /^4455667788$/
---
{
  "customer_id": "4455667788",
  "date_range": "LAST_7_DAYS",
  "summary": {
    "customer.id": 4455667788,
    "customer.descriptive_name": "Harbor Bakery (example)",
    "customer.currency_code": "GBP",
    "metrics.impressions": 4980,
    "metrics.clicks": 201,
    "metrics.ctr": 0.0404,
    "metrics.cost_micros": 305.2,
    "metrics.average_cpc": 1.52,
    "metrics.conversions": 9.0,
    "metrics.all_conversions": 10.0,
    "metrics.conversions_value": 630.0,
    "metrics.cost_per_conversion": 33.91
  },
  "markdown": "## Account performance — LAST_7_DAYS\n\n**Spend:** $305.20\n**Conversions:** 9\n**Blended CPA:** $33.91\n**CTR:** 4.0%\n**CPC:** $1.52\n**Impressions:** 4,980 | **Clicks:** 201\n"
}
