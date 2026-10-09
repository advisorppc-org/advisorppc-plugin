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
[![Version](https://img.shields.io/badge/version-0.2.0-informational.svg)](CHANGELOG.md)

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

- **Remote MCP servers**, all hosted, all browser OAuth on first use;
  credentials never live in your config files:
  - `advisorppc`: ads and analytics, `https://mcp.advisorppc.com/claude`
  - `advisorppc-gravity`: Gravity SEO blog, publishing and lead capture,
    `https://gravity.advisorppc.com/mcp`
  - `advisorppc-shield`: Shield click-fraud guard,
    `https://shield.advisorppc.ai/shield/mcp`
- **Skills** that teach Claude proven, repeatable workflows:
  - `google-ads-audit`: structured account and campaign audits covering baseline,
    wasted spend, search terms, recommendations, change history.
  - `ppc-reporting`: cross-platform performance reports over Ads, Analytics,
    Search Console, and YouTube.
  - `getting-connected`: first-run setup, plans and quotas, troubleshooting.
  - `website-setup`: hands website setup (Shield, Gravity, Tag Manager, the
    blog) to the AdvisorPPC setup planner on the Gravity server.

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

## Set up your website from one prompt

Paste the prompt in [SETUP-PROMPT.md](SETUP-PROMPT.md) into Claude with your
website address. Claude asks the AdvisorPPC setup planner what to do, then
installs Shield, connects Gravity lead capture, sets up Google Tag Manager if
needed and starts your blog, previewing every change before making it. The
steps it follows live on the AdvisorPPC servers and match your plan; any
step your plan does not include comes with the plan and checkout link.

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
