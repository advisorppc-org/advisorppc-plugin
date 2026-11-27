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
    "metrics.impressions": 4100,
    "metrics.clicks": 150,
    "metrics.ctr": 0.0366,
    "metrics.cost_micros": 240.0,
    "metrics.average_cpc": 1.6,
    "metrics.conversions": 3.0,
    "metrics.all_conversions": 3.0,
    "metrics.conversions_value": 210.0,
    "metrics.cost_per_conversion": 80.0
  },
  "markdown": "## Account performance — LAST_7_DAYS\n\n**Spend:** $240.00\n**Conversions:** 3\n**Blended CPA:** $80.00\n**CTR:** 3.7%\n**CPC:** $1.60\n**Impressions:** 4,100 | **Clicks:** 150\n"
}
