<div align="center">

<img src="assets/logo.png" alt="AdvisorPPC" width="96" />

# AdvisorPPC for Claude Code

**Work on your real ad accounts from Claude Code.**

Audit Google Ads campaigns, report across Google Analytics 4 and Search Console,
inspect Tag Manager, and review YouTube performance, all through one governed,
hosted connector. No API keys in config. No local server to run.

[Website](https://advisorppc.com) · [Documentation](https://advisorppc.com/docs) · [Install](#install) · [Plans](#plans) · [Security](SECURITY.md) · [Support](SUPPORT.md)

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-black.svg)](https://advisorppc.com/docs)
[![Version](https://img.shields.io/badge/version-0.4.0-informational.svg)](CHANGELOG.md)

</div>

---

## Overview

AdvisorPPC connects Claude Code to the accounts a performance marketer actually
works in. Once connected, Claude can pull live data, run structured audits, and,
on paid plans, manage budgets and campaigns, all under your plan's
permissions and quotas.

This repository is the official distribution point for the plugin. It contains
the plugin manifest, the marketplace definition, and the bundled skills. The
connector itself runs as a hosted service at `mcp.advisorppc.com`, operated by
Advisor Media.

## Capabilities

| Area | What Claude can do |
| --- | --- |
| **Google Ads** | Account and campaign audits, wasted-spend analysis, search-term review, recommendations, change history; budget and campaign management on paid plans |
| **Google Analytics 4** | Traffic and conversion reporting, cross-channel performance context |
| **Search Console** | Query and page performance, indexing insight for organic-vs-paid analysis |
| **Tag Manager** | Container and tag setup inspection |
| **YouTube** | Channel and video performance review |

## What's in the box

- **Remote MCP server** (`advisorppc`): the hosted connector at
  `https://mcp.advisorppc.com/claude`. Authentication is browser OAuth on first
  use; credentials never live in your config files.
- **Skills** that teach Claude proven, repeatable workflows. Claude picks the
  right one from what you ask; you can also run one as `/advisorppc:<skill>`.

| Skill | What it does | Ask things like |
| --- | --- | --- |
| `ppc-strategist` | Senior PPC advisor: confirms the account across Ads, GA4 and Tag Manager, checks tracking before trusting numbers, protects brand and core terms, proposes changes with before, after and risk | "What should I do with this account?", "Should I pause this?" |
| `google-ads-audit` | Structured read-only audit: tracking, baseline, campaigns, wasted spend, search terms, recommendations, change history | "Audit my Google Ads account" |
| `ppc-reporting` | Cross-platform reports over Google Ads, GA4, Search Console, YouTube and TikTok Ads, as cards and tables or a shareable dashboard page | "How did my ads do last month?", "Build my PPC dashboard" |
| `campaign-board` | Publishes the AdvisorPPC Campaign Board, a one-page live Google Ads board, as a claude.ai artifact | "Show me my campaigns on one page" |
| `cro-optimization` | Landing page and funnel audit for paid traffic: speed, message match, friction, fixes ranked by ICE | "Why aren't my ads converting?" |
| `landing-page-ab-testing` | Valid A/B tests on landing pages: hypothesis, sample size, assignment, readout, with a bundled calculator | "How long should this test run?" |
| `getting-connected` | First-run setup, sign-in, plans and troubleshooting | "Why am I getting a 401?" |

Every answer with numbers shows the connector's own KPI card and table, with
the insight above it.

### Campaign Board in claude.ai

The `campaign-board` skill publishes a page that reads Google Ads live through
each viewer's own claude.ai connector. Add the connector in claude.ai under
**Settings > Connectors** with the URL `https://mcp.advisorppc.com/claude` and
the name `AdvisorPPC` exactly. Live numbers show for signed-in members of your
organization; anyone else sees sample data and a link to connect.

## Install

From the terminal:

```
claude plugin marketplace add advisorppc/advisorppc-plugin
claude plugin install advisorppc@advisorppc
```

Or interactively inside Claude Code:

```
/plugin marketplace add advisorppc/advisorppc-plugin
/plugin install advisorppc@advisorppc
```

## First run

1. Install the plugin and start a new Claude Code session.
2. Run `/mcp`. The `advisorppc` server appears; connecting it opens OAuth
   sign-in in your browser.
3. Approve the connection, then link the Google account that has access to
   your ad accounts.
4. Ask Claude to list your accounts to confirm everything works.

## Plans

| Plan | Includes |
| --- | --- |
| **Free** | 100 tool calls per month, read-only tools for periodic audits and reports |
| **Paid** | Write tools (budget and campaign management) and higher quotas |

Current plans and pricing: [advisorppc.com](https://advisorppc.com).

## Security

- All product code runs server-side in the hosted connector; this repository
  contains only manifests and documentation, with no executable server code and no
  secrets.
- Authentication is OAuth 2.1 in your own browser. The plugin never asks for,
  stores, or transmits API keys or passwords through configuration files.
- Every write operation is plan-gated and quota-enforced server-side.

To report a vulnerability, see [SECURITY.md](SECURITY.md).

## Troubleshooting

Opening `https://mcp.advisorppc.com/claude` directly in a browser returns
**401, and this is expected**: it is an MCP endpoint, not a web page. For anything
else, see the `getting-connected` skill bundled with this plugin, the
[docs](https://advisorppc.com/docs), or [SUPPORT.md](SUPPORT.md).

## License

The contents of this repository (manifests, skills, and documentation) are
released under the [MIT License](LICENSE). The AdvisorPPC hosted service, its
server code, name, and logo remain the property of Advisor Media.

---

<div align="center">
<sub>© 2026 Advisor Media · <a href="https://advisorppc.com">advisorppc.com</a></sub>
</div>
