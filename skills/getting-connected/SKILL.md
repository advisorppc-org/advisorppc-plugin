---
name: getting-connected
description: First-run setup, sign-in, plans and troubleshooting for the AdvisorPPC connector. Use when the user asks "how do I connect AdvisorPPC", "set up the AdvisorPPC plugin", "connect my Google Ads", "authorize my Google account", "which Google account is connected", "why am I getting a 401", "the connector won't connect", "my accounts don't show up", "how many calls do I have left" or "add AdvisorPPC to claude.ai", or has any first-run, authentication or plan question about the connector.
---

# Getting connected to AdvisorPPC

First-run setup, authentication, plans and troubleshooting for the AdvisorPPC remote connector bundled with this plugin.

## What happens on first run

1. Installing the plugin registers the remote MCP server `advisorppc` at `https://mcp.advisorppc.com/claude`. No local server runs; two bundled skills include small offline Python helpers.
2. On first use, or from `/mcp`, Claude Code opens the connector's OAuth sign-in in the browser. Sign in, then approve the connection on the consent screen.
3. Connect the Google account that owns or can reach the ad accounts. The flow lands on `https://mcp.advisorppc.com/dashboard`; other platforms connect there too, or from chat with `connect_platform_tool`, which returns the sign-in link.
4. The connection persists across sessions. Confirm it with `/mcp`: the `advisorppc` server lists its tools.

Prove the connection end to end with two calls:

- `list_google_connections_tool` shows each connected Google login and which Google Ads, GA4, Tag Manager, Search Console, Merchant Center and YouTube accounts it reaches.
- `ga_accessible_customers_tool` (no inputs) returns the Google Ads account tree. If it lists accounts, everything works.

If several Google logins are connected and the wrong one is answering, switch with `select_google_connection_tool`.

## Using it in claude.ai as well

The plugin covers Claude Code. To use the same connector in claude.ai (web, desktop, mobile), add it under **Settings > Connectors > Add custom connector** with the URL `https://mcp.advisorppc.com/claude`. Name it exactly `AdvisorPPC`: the Campaign Board and other published pages call the connector by that name, and a name with a trailing space is refused. `connector_help_tool` gives the endpoint for other apps.

## Plans and quotas

- **Free**: read-only tools with a monthly call allowance. Enough for periodic audits and reports; prefer rollup reports over per-entity loops to stay inside it.
- **Paid plans**: write tools (budgets, campaign, ad group and keyword status, negatives) and higher allowances. Current plans: https://advisorppc.com.
- A call refused for plan or quota says why. Quote the reason and mention the upgrade only when it answers the user's actual need.

## Troubleshooting

- **401 when opening `https://mcp.advisorppc.com/claude` in a browser is expected.** It is an MCP endpoint, not a web page; a 401 means the server is up and refusing a non-MCP request.
- **Is it us or the platform?** `health_check_tool` checks each connected platform; `advisor_apps_status_tool` reports AdvisorPPC's own services. Show the result card, then explain.
- **Server missing from `/mcp`**: check the plugin is installed and enabled (`claude plugin list`), then restart Claude Code. MCP configuration loads at session start.
- **Sign-in loop or stale connection**: in `/mcp`, disconnect and reconnect `advisorppc` to restart OAuth cleanly.
- **Connected but no accounts**: the Google login has no access to the ad accounts. `list_google_connections_tool` shows what each login reaches; connect the login that owns the accounts, then select it.
- **A tool you expected is not in the list**: the list shows the common tools. Search the rest with `advisor_search_tools`; anything missing there is not on the user's plan.
- **More help**: https://advisorppc.com/docs.

## Gotchas

- Never paste passwords, tokens or client secrets into chat or config. Authentication is browser OAuth only.
- Each Google login reaches only what that Google identity can already access.
