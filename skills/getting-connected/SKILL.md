---
name: getting-connected
description: Sets up, signs in and troubleshoots the AdvisorPPC connector that this plugin installs. Use for any first-run, sign-in, account or plan question, for example "connect my Google Ads", "how do I connect AdvisorPPC", "set up the AdvisorPPC plugin", "authorize my Google account", "which Google account is connected", "why am I getting a 401", "the connector won't connect", "my accounts don't show up", "can it read my Meta ads too" or "how many calls do I have left".
license: MIT
metadata:
  version: 0.2.0
---

# Getting Connected to AdvisorPPC

## Hard rules

- Authentication is browser OAuth only. Never ask for, accept or paste credentials, tokens or client secrets in chat or config.
- When a call is denied for quota or plan reasons, the tool result says so. Report the reason to the user verbatim and suggest an upgrade only when it answers the user's actual need. Do not quote prices; point to https://advisorppc.com for current plans.
- One connection maps to one Google identity. To report on accounts owned by a different identity, reconnect with that identity.

First-run setup, authentication, plans and troubleshooting for the AdvisorPPC remote connector bundled with this plugin. AdvisorPPC is Google-first (Google Ads, GA4, Tag Manager, Search Console, YouTube); the same connector also connects Meta, Microsoft Advertising, TikTok, LinkedIn, Pinterest and X, each from `connect_platform_tool` or the AdvisorPPC dashboard.

## What happens on first run

1. Installing this plugin registers the remote MCP server `advisorppc` (endpoint `https://mcp.advisorppc.com/claude`). No local process runs; the server is hosted.
2. On first tool use (or via the `/mcp` command), Claude Code starts the connector's OAuth flow in the browser. Sign in, then approve the connection on the consent screen.
3. After consent, connect the Google account that owns (or has access to) the ad accounts from the AdvisorPPC dashboard the flow lands on. The connector only ever reads accounts the signed-in Google identity can already access.
4. The connection persists across sessions. Tools appear automatically; verify with `/mcp`: the `advisorppc` server should list its tools (for example `ga_accessible_customers_tool`).

A good first call to prove the connection end-to-end: `ga_accessible_customers_tool` (no inputs). If it returns an account tree, everything works.

## Plans

- **Free plan**: reads one Google Ads account, with a monthly call allowance. Prefer rollup report tools over per-entity loops to stay inside it.
- **Paid plans**: unlock write tools (budget and campaign management) and higher allowances. Plans are listed at https://advisorppc.com.

## Troubleshooting

- **401 when opening `https://mcp.advisorppc.com/claude` in a browser: EXPECTED.** That URL is an MCP endpoint for MCP clients, not a web page. A bare browser GET returning 401 means the server is up and correctly refusing unauthenticated non-MCP traffic. Do not treat it as an outage.
- **Server missing from `/mcp`**: confirm the plugin is installed and enabled (`claude plugin list`), then restart Claude Code; MCP configuration loads at session start.
- **Authentication loop or stale connection**: use `/mcp` to disconnect and reconnect the `advisorppc` server, which restarts the OAuth flow cleanly.
- **Tools connect but return no accounts**: the Google identity granted during connect has no ad-account access. Reconnect and grant with the Google account that actually owns the accounts.
- **Another platform**: call `connect_platform_tool` with the platform name; it returns the authorization link.
- **Deeper help**: public docs at https://advisorppc.com/docs.
