---
name: getting-connected
description: This skill should be used when the user asks "how do I connect AdvisorPPC", "set up the AdvisorPPC plugin", "authorize my Google account", "why am I getting a 401", "the connector won't connect", "how many calls do I have left", or has first-run, authentication, or plan questions about the AdvisorPPC connector.
version: 0.1.0
---

# Getting Connected to AdvisorPPC

First-run setup, authentication, plans, and troubleshooting for the AdvisorPPC remote connector bundled with this plugin.

## What happens on first run

1. Installing this plugin registers the remote MCP server `advisorppc` (endpoint `https://mcp.advisorppc.com/claude`). No local process runs; the server is hosted.
2. On first tool use (or via the `/mcp` command), Claude Code starts the connector's OAuth flow in the browser. Sign in, then approve the connection on the consent screen.
3. After consent, connect the Google account that owns (or has access to) the ad accounts from the AdvisorPPC dashboard the flow lands on. The connector only ever reads accounts the signed-in Google identity can already access.
4. The connection persists across sessions. Tools appear automatically; verify with `/mcp` — the `advisorppc` server should list its tools (for example `ga_list_accessible_customers_tool`).

A good first call to prove the connection end-to-end: `ga_list_accessible_customers_tool` (no inputs). If it returns an account tree, everything works.

## The other AdvisorPPC servers

The plugin also registers `advisorppc-gravity` (`https://gravity.advisorppc.com/mcp`) and `advisorppc-shield` (`https://shield.advisorppc.ai/shield/mcp`). Each connects through `/mcp` with the same browser OAuth. To set either up on a website, use the `website-setup` skill.

## Plans and quotas

- **Free tier**: 100 tool calls per month, read-only tools. Enough for periodic audits and reports; prefer rollup report tools over per-entity loops to stay inside it.
- **Paid plans**: unlock write tools (budget and campaign management) and higher call quotas. Plans are listed at https://advisorppc.com.
- When a call is denied for quota or plan reasons, the tool result says so — report the reason to the user verbatim and suggest the upgrade path only when it answers the user's actual need.

## Troubleshooting

- **401 when opening `https://mcp.advisorppc.com/claude` in a browser: EXPECTED.** That URL is an MCP endpoint for MCP clients, not a web page. A bare browser GET returning 401 means the server is up and correctly refusing unauthenticated non-MCP traffic. Do not treat it as an outage.
- **Server missing from `/mcp`**: confirm the plugin is installed and enabled (`claude plugin list`), then restart Claude Code — MCP configuration loads at session start.
- **Authentication loop or stale connection**: use `/mcp` to disconnect and reconnect the `advisorppc` server, which restarts the OAuth flow cleanly.
- **Tools connect but return no accounts**: the Google identity granted during connect has no ad-account access. Reconnect and grant with the Google account that actually owns the accounts.
- **Deeper help**: public docs at https://advisorppc.com/docs.

## Gotchas

- Never paste credentials, tokens, or client secrets into chat or config for this connector — authentication is entirely browser OAuth.
- One connection maps to one Google identity. To report on accounts owned by a different identity, reconnect with that identity.
