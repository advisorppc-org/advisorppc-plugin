---
expect:
  customer_id: /^\d{10}$/
---
{
  "customer_id": "{{input.customer_id}}",
  "status": "healthy",
  "conversion_actions": [
    {"name": "Contact form submit", "status": "ENABLED", "last_conversion": "2026-10-20", "primary": true}
  ]
}
