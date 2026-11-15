---
name: getting-connected
description: This skill should be used when the user asks "how do I connect AdvisorPPC", "set up the AdvisorPPC plugin", "authorize my Google account", "why am I getting a 401", "the connector won't connect", "what plan am I on", "how do I upgrade", or has first-run, authentication, or plan questions about the AdvisorPPC connector.
version: 0.1.0
---

# Getting Connected to AdvisorPPC

First-run setup, authentication, plans, and troubleshooting for the AdvisorPPC remote connector bundled with this plugin.

## What happens on first run

1. Installing this plugin registers the remote MCP server `advisorppc` (endpoint `https://mcp.advisorppc.com/claude`). No local process runs; the server is hosted.
2. On first tool use (or via the `/mcp` command), Claude Code starts the connector's OAuth flow in the browser. Sign in, then approve the connection on the consent screen.
3. **After consent, connect your ad accounts in the dashboard** at https://mcp.advisorppc.com/dashboard. Sign in to the ad platform with an identity that has access to the ad account; approving the connector alone does not link ad accounts. The connector only ever reads accounts that identity can already access.
4. The connection persists across sessions. Tools appear automatically; verify with `/mcp` — the `advisorppc` server should list its tools (for example `ga_accessible_customers_tool`).

A good first call to prove the connection end-to-end: `ga_accessible_customers_tool` (no inputs). If it returns an account tree, everything works.

## Plans

- **Free plan**: read-only tools, no card required. Enough for periodic audits and reports. The current allowance shows in the dashboard; prefer rollup report tools over per-entity loops to make it go further.
- **Paid plans**: unlock write tools (budget and campaign management) and larger allowances.
- **Showing the plan**: call `plan_tool` with action `"status"`. It returns the current plan and what it includes; quote it rather than stating terms from memory.
- **Buying or changing a plan**: when the user picks a plan, call `plan_tool` with action `"upgrade"` and that `plan`, and hand over the secure checkout link it returns. No card details are taken in chat; payment finishes on the linked page. The plans page is https://mcp.advisorppc.com/pricing.
- Never state a price, trial, discount, allowance or date that a tool result did not give you; `plan_tool` states the live terms.
- When a call is denied for quota or plan reasons, the tool result says so — report the reason to the user verbatim and suggest the upgrade path only when it answers the user's actual need.

## Headless or remote machine

Run `claude mcp login --no-browser advisorppc` in an **interactive terminal** on the machine running Claude Code. If the installed plugin uses a qualified server name, use the name shown by `claude mcp list` instead of `advisorppc`. `--no-browser` prints the authorization URL but still needs a TTY; piped stdin, scripts and `claude -p` are not a documented unattended login path.

1. Keep that terminal open and open the printed authorization URL in your browser.
2. Check the signed-in AdvisorPPC account, then approve consent.
3. The browser redirect targets `localhost` on the machine running Claude Code. With a browser on a different machine, its own localhost cannot reach that callback. Copy the full redirect URL from the browser address bar and paste it into the waiting Claude Code terminal when prompted, even if the browser shows a connection error. Paste it only into that login prompt; it contains a short-lived authorization code.
4. Alternatively, forward the callback port over SSH from the browser machine to the Claude Code machine. Use the actual port from this login attempt, bind it to loopback, and keep the tunnel open until login completes. For example, from the browser machine: `ssh -N -L 127.0.0.1:<callback-port>:127.0.0.1:<callback-port> <claude-code-host>`.
5. After authentication, connect your ad accounts in the dashboard as described above. Confirm the connector status with `claude mcp list`.

OAuth login belongs to the Claude Code configuration profile used for that session. Do not copy another person's credentials into an agent profile.

## Troubleshooting

- **401 when opening `https://mcp.advisorppc.com/claude` in a browser: EXPECTED.** That URL is an MCP endpoint for MCP clients, not a web page. A bare browser GET returning 401 means the server is up and correctly refusing unauthenticated non-MCP traffic. Do not treat it as an outage.
- **Server missing from `/mcp`**: confirm the plugin is installed and enabled (`claude plugin list`), then restart Claude Code — MCP configuration loads at session start.
- **Authentication loop or stale connection**: use `/mcp` to disconnect and reconnect the `advisorppc` server, which restarts the OAuth flow cleanly.
- **Tools connect but return no accounts**: open https://mcp.advisorppc.com/dashboard and connect the intended ad platform and account. Check that you signed in to the right AdvisorPPC account and that the platform identity can access the ad account.
- **Deeper help**: public docs at https://advisorppc.com/docs.

## Gotchas

- Never paste credentials, tokens, or client secrets into chat or config for this connector — authentication is entirely browser OAuth.
- One connection maps to one Google identity. To report on accounts owned by a different identity, reconnect with that identity.
