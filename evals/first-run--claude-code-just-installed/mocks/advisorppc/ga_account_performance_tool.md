---
expect:
  customer_id: /^4455667788$/
---
{
  "customer_id": "4455667788",
  "date_range": "LAST_30_DAYS",
  "summary": {
    "customer.id": 4455667788,
    "customer.descriptive_name": "Harbor Bakery (example)",
    "customer.currency_code": "GBP",
    "metrics.impressions": 21340,
    "metrics.clicks": 866,
    "metrics.ctr": 0.0406,
    "metrics.cost_micros": 1312.4,
    "metrics.average_cpc": 1.52,
    "metrics.conversions": 0.0,
    "metrics.all_conversions": 0.0,
    "metrics.conversions_value": 0.0,
    "metrics.cost_per_conversion": 0
  },
  "markdown": "## Account performance — LAST_30_DAYS\n\n**Spend:** $1,312.40\n**Conversions:** 0\n**Blended CPA:** –\n**CTR:** 4.1%\n**CPC:** $1.52\n**Impressions:** 21,340 | **Clicks:** 866\n"
}
