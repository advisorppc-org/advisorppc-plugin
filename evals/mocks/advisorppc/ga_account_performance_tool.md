---
expect:
  customer_id: /^\d{10}$/
---
{
  "customer_id": "{{input.customer_id}}",
  "currency_code": "EUR",
  "date_range": "LAST_30_DAYS",
  "impressions": 48210, "clicks": 1912, "ctr": 0.0397, "cost": 4180.55,
  "average_cpc": 2.19, "conversions": 61, "conversion_value": 0, "cost_per_conversion": 68.53
}
