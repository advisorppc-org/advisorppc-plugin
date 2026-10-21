---
description: Check the AdvisorPPC connection, plan and remaining calls
---

Check the AdvisorPPC connector for this session.

1. Call `health_check_tool`. If the server is missing, follow the `getting-connected` skill's troubleshooting section.
2. Call `ga_accessible_customers_tool` to prove the Google connection; list the accounts in one short table (name, id, manager yes/no).
3. Call `list_google_connections_tool` and report which platforms are connected (Ads, GA4, Search Console, Tag Manager, YouTube) and which are not, with the one link to connect more: https://mcp.advisorppc.com/dashboard.
4. State the plan and the calls remaining this month if the tool results carry them.

Four lines at most. No advice unless something is broken.
