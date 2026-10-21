# Connectors

This plugin works in two modes:

- Standalone: Claude uses the bundled skills and playbooks with no connection at all.
- Connected: Claude also uses the hosted AdvisorPPC connector from [`.mcp.json`](./.mcp.json) to read your live accounts and, on paid plans, apply changes you approve.

## Included MCP server

The plugin registers one remote MCP server, `advisorppc`, at
`https://mcp.advisorppc.com/claude`. It is operated by Advisor Media. Every
platform below is reached through that one server, using the provider's
official API under your own authorization. The plugin calls no other host.

| Connector | Endpoint | Use for |
| --- | --- | --- |
| Google Ads | `https://mcp.advisorppc.com/claude` | Accounts, campaigns, keywords, search terms, audits, wasted spend, change history; on paid plans, approved pauses, enables, budgets, bids and keywords |
| Google Analytics 4 | `https://mcp.advisorppc.com/claude` | Properties, key events, traffic by source, reports, realtime |
| Search Console | `https://mcp.advisorppc.com/claude` | Sites, top queries and pages, URL inspection |
| Tag Manager | `https://mcp.advisorppc.com/claude` | Accounts, containers, workspaces, tags, container audit |
| YouTube | `https://mcp.advisorppc.com/claude` | Channel stats, top videos, traffic sources |
| TikTok Ads | `https://mcp.advisorppc.com/claude` | Campaign list and account and campaign performance |

## Authentication

Browser OAuth. Run `/mcp` in Claude Code and connect `advisorppc`; the
sign-in opens in your browser. Then connect the Google account that can reach
your ad accounts, and any other platform, at
`https://mcp.advisorppc.com/dashboard`. There are no API keys, tokens or
environment variables to set, and nothing is stored in your config files.

To use the same connector in claude.ai (web, desktop, mobile), add a custom
connector under **Settings > Connectors** with the URL
`https://mcp.advisorppc.com/claude` and the name `AdvisorPPC` exactly.

## What you can do without the connector

- `ppc-strategist`: senior PPC advice, account structure, bidding fit, ad copy and tracking setup from the bundled playbooks
- `cro-optimization`: a landing page friction audit and ICE-ranked fixes from a page you describe or share
- `landing-page-ab-testing`: hypotheses, sample size, significance and sample-ratio checks with the bundled offline calculator

## What the connector adds

- Live data from your own accounts in every skill, shown as the connector's KPI cards and tables
- Structured audits, cross-platform reports, the ppc-reporting dashboard and the live Campaign Board
- On paid plans, write tools for pauses, enables, budgets, bids and keywords, applied only after you approve the exact change
