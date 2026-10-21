<div align="center">

<img src="assets/logo.png" alt="AdvisorPPC" width="96" />

# AdvisorPPC

**Work on your real ad accounts from Claude.**

Audit Google Ads campaigns, report across Google Analytics 4 and Search Console,
inspect Tag Manager, and review YouTube and TikTok Ads performance, all through
one governed, hosted connector. No API keys in config. No local server to run.

[Website](https://advisorppc.com) · [Documentation](https://advisorppc.com/docs) · [Install](#install) · [Requirements](#requirements) · [Connectors](CONNECTORS.md) · [Security](SECURITY.md) · [Support](SUPPORT.md)

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude plugin](https://img.shields.io/badge/Claude-plugin-black.svg)](https://advisorppc.com/docs)
[![Version](https://img.shields.io/badge/version-0.4.0-informational.svg)](CHANGELOG.md)

</div>

---

## Overview

AdvisorPPC connects Claude to the accounts a performance marketer actually
works in. Once connected, Claude can pull live data, run structured audits, and,
on paid plans and only with your approval, manage budgets, bids, keywords and
campaign status, all under your plan's permissions and quotas.

This repository is the official distribution point for the plugin. The
connector itself runs as a hosted service at `mcp.advisorppc.com`, operated by
Advisor Media. See [CONNECTORS.md](CONNECTORS.md) for what it reaches and how
it signs in.

## Works with

- **Claude Code**: install from this marketplace (below), then connect with `/mcp`.
- **Cowork**: [Install in Cowork](https://claude.ai/desktop/customize/plugins/new?marketplace=advisorppc-org/advisorppc-plugin&plugin=advisorppc).
- **Claude web and desktop**: add the connector under
  **Settings > Connectors > Add custom connector** with the URL
  `https://mcp.advisorppc.com/claude` and the name `AdvisorPPC` exactly (the Campaign Board calls the connector by that
  name, and a name with a trailing space is refused). Live numbers on a
  published Campaign Board show for signed-in members of your organization;
  anyone else sees sample data and a link to connect.

## Requirements

- **AdvisorPPC connector** (`mcp.advisorppc.com/claude`), connected and
  authenticated with browser OAuth through `/mcp`. It is registered by this
  plugin's `.mcp.json`; no tokens or environment variables.
- **A Google login with access to your ad accounts**, connected at
  `https://mcp.advisorppc.com/dashboard`. Other platforms (TikTok Ads) connect
  there too.
- **A plan**:

  | Plan | Includes |
  | --- | --- |
  | **Free** | 100 tool calls per month, read-only tools for periodic audits and reports |
  | **Paid** | Write tools (pause, enable, budgets, bids, keywords) and higher quotas |

  Current plans and pricing: [advisorppc.com](https://advisorppc.com).
- **Python 3** for the two bundled helpers (the dashboard filler and the A/B
  test calculator). Both use the standard library only.

## Skills

Skills are triggered conversationally. Describe what you want and Claude loads
the right skill.

| Skill | Trigger phrases |
| --- | --- |
| `ppc-strategist` | "What should I do with this account?", "why did my CPA go up?", "should I pause this?", "act as my PPC manager" |
| `google-ads-audit` | "Audit my Google Ads account", "find wasted spend", "check my search terms", "is my conversion tracking working?" |
| `ppc-reporting` | "How did my ads do last month?", "show me traffic by source", "compare this month to last month", "build my PPC dashboard" |
| `campaign-board` | "Show me my campaigns on one page", "a live Google Ads dashboard", "a campaign overview I can share" |
| `cro-optimization` | "Why aren't my ads converting?", "audit my landing page", "where is my funnel leaking?", "which fix should we ship first?" |
| `landing-page-ab-testing` | "Should we test this?", "how long should this test run?", "did the variant win?", "is this result real?" |
| `getting-connected` | "How do I connect AdvisorPPC?", "why am I getting a 401?", "my accounts don't show up", "how many calls do I have left?" |

## Commands

Every skill can also be run directly as a slash command:

| Command | Usage |
| --- | --- |
| `/advisorppc:ppc-strategist` | Advice on the connected account |
| `/advisorppc:google-ads-audit [customer-id] [days]` | Read-only audit of one Google Ads account |
| `/advisorppc:ppc-reporting [customer-id] [period]` | Cross-platform report or dashboard for a period |
| `/advisorppc:campaign-board` | Publish the live Campaign Board |
| `/advisorppc:cro-optimization <landing page URL>` | Conversion audit of one landing page |
| `/advisorppc:landing-page-ab-testing` | Plan, size or read out an A/B test |
| `/advisorppc:getting-connected` | Setup, sign-in and plan help |

Dedicated commands (`/advisorppc:dashboard`, `/advisorppc:audit`,
`/advisorppc:waste`, `/advisorppc:connect`) arrive in 0.5.0.

## What each skill produces

**PPC Strategist**: advisor answers grounded in your account. Confirms the
account across Google Ads, GA4 and Tag Manager, checks conversion tracking
before trusting numbers, protects brand, category and core-geo terms, and
proposes every change with before, after and risk. Nothing is paused or edited
until you say yes in the conversation.

**Google Ads Audit**: a structured, read-only audit: tracking blockers, account
baseline, campaigns, wasted spend, search terms, recommendations and change
history, with findings ranked by monthly cost impact and next actions. The
audit applies nothing.

**PPC Reporting**: reports across Google Ads, GA4, Search Console, YouTube and
TikTok Ads as the connector's KPI cards and tables, or a self-contained
dashboard page with period deltas, daily charts, a campaign table and
zero-conversion search terms.

**Campaign Board**: a one-page Google Ads board published as a claude.ai
artifact that reads live data through each viewer's own connector every time
it opens.

**CRO Optimization**: a landing page and funnel audit for paid traffic:
funnel math, Core Web Vitals, ad-to-page message match, a friction checklist
and the top fixes ranked by impact, confidence and ease.

**Landing Page A/B Testing**: a written hypothesis, sample size and run time,
assignment and logging rules, and a readout with significance, confidence
interval and sample-ratio check from the bundled calculator.

**Getting Connected**: first-run setup, sign-in, plan and quota answers, and
fixes for common connection errors.

Every answer with numbers shows the connector's own KPI card and table, with
the insight above it.

## What's in the box

- **`.mcp.json`**: registers one remote MCP server, `advisorppc`, at
  `https://mcp.advisorppc.com/claude`. Authentication is browser OAuth on first
  use; credentials never live in your config files.
- **`skills/`**: the seven skills above, as Markdown, with playbooks under
  `skills/ppc-strategist/references/`.
- **Two Python helpers**, standard library only, offline, no network:
  `skills/ppc-reporting/scripts/fill-dashboard.py` fills the dashboard template
  from a JSON file and writes one HTML file to the path you give it;
  `skills/landing-page-ab-testing/scripts/ab_stats.py` computes sample size,
  significance and sample-ratio mismatch and prints the result.
- **Two HTML pages**: `skills/ppc-reporting/assets/dashboard.html` (the
  dashboard template, system fonts, no external requests) and
  `skills/campaign-board/assets/campaign-board.html` (the Campaign Board, which
  calls only read-only AdvisorPPC tools through the viewer's own claude.ai
  connector).
- **`tests/`** and a CI workflow that check the skills, run the A/B
  calculator's behaviour cases and validate the manifests. The plugin does not
  load them.

## Install

From the terminal:

```
claude plugin marketplace add advisorppc-org/advisorppc-plugin
claude plugin install advisorppc@advisorppc
```

Or interactively inside Claude Code:

```
/plugin marketplace add advisorppc-org/advisorppc-plugin
/plugin install advisorppc@advisorppc
```

## First run

1. Install the plugin and start a new Claude Code session.
2. Run `/mcp`. The `advisorppc` server appears; connecting it opens OAuth
   sign-in in your browser.
3. Approve the connection, then link the Google account that has access to
   your ad accounts.
4. Ask Claude to list your accounts to confirm everything works.

## Security

- All product code runs server-side in the hosted connector. This repository
  holds manifests, Markdown skills, two HTML pages and two offline,
  standard-library Python helpers. It has no hooks, no telemetry, no server
  code and no secrets, and the plugin makes no network call except to
  `mcp.advisorppc.com`.
- Authentication is OAuth 2.1 in your own browser. The plugin never asks for,
  stores, or transmits API keys or passwords through configuration files.
- Every write operation is plan-gated and quota-enforced server-side, and the
  skills apply a change only after you approve it in the conversation.

To report a vulnerability, see [SECURITY.md](SECURITY.md).

## Troubleshooting

Opening `https://mcp.advisorppc.com/claude` directly in a browser returns
**401, and this is expected**: it is an MCP endpoint, not a web page. For anything
else, see the `getting-connected` skill bundled with this plugin, the
[docs](https://advisorppc.com/docs), or [SUPPORT.md](SUPPORT.md).

## License

The contents of this repository (manifests, skills, helpers, pages and
documentation) are released under the [MIT License](LICENSE). The AdvisorPPC
hosted service and its server code remain the property of Advisor Media.

The "AdvisorPPC" and "Advisor Media" names and logos are trademarks of
Advisor Media and are not licensed under the MIT License.

---

<div align="center">
<sub>© 2026 Advisor Media · <a href="https://advisorppc.com">advisorppc.com</a></sub>
</div>
