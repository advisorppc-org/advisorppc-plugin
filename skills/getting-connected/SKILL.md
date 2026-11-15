---
name: getting-connected
description: This skill should be used when the user asks "how do I connect AdvisorPPC", "set up the AdvisorPPC plugin", "authorize my Google account", "why am I getting a 401", "the connector won't connect", "what plan am I on", "how much do I have left", "what's left on my plan", "how do I upgrade", "change my billing", "cancel my plan", "can you apply this fix", or has first-run, authentication, plan, billing, or applying-a-change questions about the AdvisorPPC connector.
version: 0.1.0
---

# Getting Connected to AdvisorPPC

First-run setup, authentication, plans, applying changes, and troubleshooting for the AdvisorPPC remote connector bundled with this plugin.

## What happens on first run

1. Installing this plugin registers the AdvisorPPC remote MCP server (endpoint `https://mcp.advisorppc.com/claude`). No local process runs; the server is hosted.
2. On first tool use (or via the `/mcp` command), Claude Code starts the connector's OAuth flow in the browser. Sign in, then approve the connection on the consent screen.
3. **After consent, link your ad accounts in the dashboard** at https://mcp.advisorppc.com/dashboard. Linking ad accounts is separate from the connector sign-in: sign in to the ad platform there with a Google identity that has access to the ad account. More than one Google identity can be linked. The connector only ever reads accounts a linked identity can already access.
4. The connection persists across sessions. Tools appear automatically; verify with `/mcp`. The AdvisorPPC server should list its tools (for example `ga_accessible_customers_tool`).

A good first call to prove the connection end-to-end: `ga_accessible_customers_tool` (no inputs). If it returns an account tree, everything works.

## Plans

- **Free plan**: read-only tools, no card required. Prefer rollup report tools over per-entity loops to make the allowance go further.
- **Paid plans**: unlock change tools (budget and campaign management) and larger allowances.
- **Showing the plan and what is left**: call `plan_tool` with action `"status"`. It returns the current plan, what it includes, and the user's current allowance and renewal. The dashboard does not show the allowance, so do not send the user there for it. Quote the tool result rather than stating terms from memory.
- Never state a plan name, price, trial, discount, allowance or date that a tool result or the user did not give you.
- When a tool result refuses a call for plan reasons, report the reason to the user verbatim, and offer the plan steps below only if the user wants them.

## Buying, changing or cancelling a plan

`plan_tool` changes nothing itself: each action returns a status card or a link, and payment or cancellation finishes on the linked page. No card details are taken in chat.

- **Upgrade or change plan**:
  1. Call `plan_tool` with action `"status"` and tell the user their current plan.
  2. Ask which plan they want.
  3. If they do not know the plans, give them https://mcp.advisorppc.com/pricing to choose from. (Calling `"upgrade"` without a `plan` returns only the status card and that pricing link, with no plan names.)
  4. When the user names a plan, call `plan_tool` with action `"upgrade"` and that `plan`, and hand over the secure checkout link it returns.
- **Billing, invoices or payment method**: call `plan_tool` with action `"manage"` and hand over the billing page link.
- **Cancel or downgrade**: call `plan_tool` with action `"cancel"` and `confirm=false` first, and share its explanation. Only after the user says yes, call it again with `confirm=true` and hand over the cancel page link.
- Name only plans that a tool result or the user named. Never invent plan names, prices or terms.

## Applying a change and plans

The `google-ads-audit` and `ppc-reporting` skills only read and propose; they never apply a change themselves. When the user asks to apply a fix (for example pausing, a budget, negative keywords or bids):

1. Call `plan_tool` with action `"status"` to see whether the plan includes changes.
2. If it does and the connector's change tool for that fix is present in this session, describe each change exactly and get the user's explicit yes for that change before calling the tool. One yes covers one change.
3. If the change tool's result refuses the change for plan reasons, report that reason verbatim. Offer the upgrade steps above only if the user wants them.
4. If the plan does not include changes, or no change tool is present in this session, say so in one plain line and give the proposal as a list the user can apply by hand in the ad platform.

Upgrading changes what the connector's change tools allow; it never makes these skills apply changes themselves, so do not present checkout that way. Never push a plan when the user only wants to read, never claim savings the data does not show, and suggest the upgrade path only when it answers the user's actual need.

## Headless or remote machine

First run `claude mcp list` and read the AdvisorPPC server's name. A plugin-installed server appears in the qualified form `plugin:advisorppc:advisorppc`. Use that name in the login command, in an **interactive terminal** on the machine running Claude Code:

```
claude mcp login --no-browser plugin:advisorppc:advisorppc
```

Use the bare name (`claude mcp login --no-browser advisorppc`) only for a manual, non-plugin install that registered the server as `advisorppc`. `--no-browser` prints the authorization URL but still needs a TTY; piped stdin, scripts and `claude -p` are not a documented unattended login path.

1. Keep that terminal open and open the printed authorization URL in your browser.
2. Check the signed-in AdvisorPPC account, then approve consent.
3. The browser redirect targets `localhost` on the machine running Claude Code. With a browser on a different machine, its own localhost cannot reach that callback. Copy the full redirect URL from the browser address bar and paste it into the waiting Claude Code terminal when prompted, even if the browser shows a connection error. Paste it only into that login prompt; it contains a short-lived authorization code.
4. Alternatively, forward the callback port over SSH from the browser machine to the Claude Code machine. Use the actual port from this login attempt, bind it to loopback, and keep the tunnel open until login completes. For example, from the browser machine: `ssh -N -L 127.0.0.1:<callback-port>:127.0.0.1:<callback-port> <claude-code-host>`.
5. After authentication, link your ad accounts in the dashboard as described above. Confirm the connector status with `claude mcp list`.

OAuth login belongs to the Claude Code configuration profile used for that session. Do not copy another person's credentials into an agent profile.

## Troubleshooting

- **401 when opening `https://mcp.advisorppc.com/claude` in a browser: EXPECTED.** That URL is an MCP endpoint for MCP clients, not a web page. A bare browser GET returning 401 means the server is up and correctly refusing unauthenticated non-MCP traffic. Do not treat it as an outage.
- **Server missing from `/mcp`**: confirm the plugin is installed and enabled (`claude plugin list`), then restart Claude Code. MCP configuration loads at session start.
- **Authentication loop or stale connection**: use `/mcp` to disconnect and reconnect the AdvisorPPC server, which restarts the OAuth flow cleanly. Reconnecting does not change which Google identities or ad accounts are linked.
- **Tools connect but return no accounts, or not the accounts you expected**: open https://mcp.advisorppc.com/dashboard and link the intended ad platform, Google identity and account. Check that you signed in to the right AdvisorPPC account. If the accounts sit under another linked Google identity, call `list_google_connections_tool` and choose that identity with `select_google_connection_tool`.
- **Deeper help**: public docs at https://advisorppc.com/docs.

## Gotchas

- Never paste credentials, tokens, or client secrets into chat or config for this connector. Authentication is entirely browser OAuth.
- Ad accounts and Google identities are linked in the dashboard, not through the connector sign-in. To work on accounts under another Google identity, link that identity in the dashboard, then choose it with `select_google_connection_tool` (`list_google_connections_tool` lists the linked identities). Reconnecting the MCP server does not change linked identities.
