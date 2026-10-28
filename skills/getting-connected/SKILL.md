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
3. **After consent, connect your ad accounts in the dashboard** at https://advisorppc.com/dashboard/settings. Sign in to the chosen ad platform with an identity that has access to the ad account. Approving the connector alone does not link ad accounts.
4. The connection persists across sessions. Tools appear automatically; verify with `/mcp`. The `advisorppc` server should list its tools (for example `ga_list_accessible_customers_tool`).

For a connected Google Ads account, a first read to check the connection is `ga_list_accessible_customers_tool` (no inputs). A successful account-tree response confirms Google Ads access.

## Plans and quotas

- **Free tier**: read-only, no card required, with one ad account on any ONE ad platform: Google Ads, Meta, TikTok, Microsoft Advertising, LinkedIn, Pinterest or X. Usage is subject to the current Free allowance; check the dashboard for your remaining quota. Prefer rollup reports over per-entity loops.
- **Paid plans**: write access and usage allowances depend on the plan and platform. Check current plan details at https://advisorppc.com and your dashboard; do not assume a numeric quota.
- When a call is denied for quota or plan reasons, the tool result says so. Report the reason to the user verbatim and suggest the upgrade path only when it answers the user's actual need.

## Headless or remote machine

Run `claude mcp login --no-browser advisorppc` in an **interactive terminal** on the machine running Claude Code. If the installed plugin uses a qualified server name, use the name shown by `claude mcp list` instead of `advisorppc`. `--no-browser` prints the authorization URL, but still needs a TTY; piping stdin, scripts, Agent SDK and `claude -p` are not a documented unattended login path.

1. Keep that terminal open and open the printed authorization URL in your browser.
2. Check the signed-in AdvisorPPC account, then approve consent.
3. The browser redirect targets `localhost` on the machine running Claude Code. With a browser on a different machine, its own localhost cannot reach that callback. Copy the full redirect URL from the browser address bar and paste it into the waiting Claude Code terminal when prompted, even if the browser shows a connection error. Paste it only into that login prompt; it contains a short-lived authorization code.
4. Alternatively, forward the callback port over SSH from the browser machine to the Claude Code machine. Use the actual port from this login attempt, bind it to loopback, and keep the tunnel open until login completes. For example, from the browser machine: `ssh -N -L 127.0.0.1:<callback-port>:127.0.0.1:<callback-port> <claude-code-host>`.
5. After authentication, connect your ad accounts in the dashboard as described above. Confirm the connector status with `claude mcp list`.

OAuth login belongs to the Claude Code configuration profile used for that session. Do not copy another seat's credentials into an agent profile. An unattended Agent SDK or CI token path is not documented here; a workspace agent-token or device-code option requires a separate product decision.

## Troubleshooting

- **401 when opening `https://mcp.advisorppc.com/claude` in a browser: EXPECTED.** That URL is an MCP endpoint for MCP clients, not a web page. A bare browser GET returning 401 means the server is up and correctly refusing unauthenticated non-MCP traffic. Do not treat it as an outage.
- **Server missing from `/mcp`**: confirm the plugin is installed and enabled (`claude plugin list`), then restart Claude Code. MCP configuration loads at session start.
- **Authentication loop or stale connection**: use `/mcp` to disconnect and reconnect the `advisorppc` server, which restarts the OAuth flow cleanly.
- **Tools connect but return no accounts**: check https://advisorppc.com/dashboard/settings and connect the intended ad platform and account. Confirm that you signed in to the correct AdvisorPPC workspace and that the platform identity can access the account.
- **Deeper help**: public docs at https://advisorppc.com/docs.

## Gotchas

- Never paste credentials, tokens, or client secrets into chat or config for this connector. Authentication is entirely browser OAuth.
- Consent authorizes the signed-in AdvisorPPC account. Check that identity before approving, then manage platform connections and ad-account selection in the dashboard.
