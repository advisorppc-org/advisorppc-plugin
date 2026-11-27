---
expect:
  customer_id: /^4455667788$/
---
{
  "customer_id": "4455667788",
  "count": 2,
  "changes": [
    {
      "change_event.change_date_time": "2026-11-24 09:12:44.418302",
      "change_event.user_email": "owner@harborbakery.example",
      "change_event.client_type": "GOOGLE_ADS_WEB_CLIENT",
      "change_event.change_resource_type": "CAMPAIGN_BUDGET",
      "change_event.resource_change_operation": "UPDATE",
      "change_event.changed_fields": "amount_micros",
      "change_event.campaign": "customers/4455667788/campaigns/111",
      "change_event.ad_group": ""
    },
    {
      "change_event.change_date_time": "2026-11-23 16:40:02.120944",
      "change_event.user_email": "owner@harborbakery.example",
      "change_event.client_type": "GOOGLE_ADS_WEB_CLIENT",
      "change_event.change_resource_type": "AD_GROUP_CRITERION",
      "change_event.resource_change_operation": "REMOVE",
      "change_event.changed_fields": "",
      "change_event.campaign": "customers/4455667788/campaigns/111",
      "change_event.ad_group": "customers/4455667788/adGroups/1001"
    }
  ],
  "markdown": "## Recent account changes — last 7 days\n\n- **2026-11-24 09:12:44.418302** — owner@harborbakery.example: UPDATE CAMPAIGN_BUDGET\n  Fields: amount_micros\n- **2026-11-23 16:40:02.120944** — owner@harborbakery.example: REMOVE AD_GROUP_CRITERION"
}
