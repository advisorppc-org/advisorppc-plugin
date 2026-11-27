<div align="center">

![AdvisorPPC](assets/logo-192.png)

# AdvisorPPC for Claude Code

**Work on your real ad accounts from Claude Code.**

Audit Google Ads campaigns, report across Google Analytics 4 and Search Console,
inspect Tag Manager, and review YouTube performance, all through one governed,
hosted connector. No API keys in config. No local server to run.

[Website](https://advisorppc.com) · [Documentation](https://advisorppc.com/docs) · [Install](#install) · [Plans](#plans) · [Security](SECURITY.md) · [Support](SUPPORT.md)

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-black.svg)](https://advisorppc.com/docs)
[![Version](https://img.shields.io/badge/version-0.3.8-informational.svg)](CHANGELOG.md)

</div>

---

## Overview

AdvisorPPC connects Claude Code to the accounts a performance marketer actually
works in. Once connected, Claude can pull live data, run structured audits, and,
on paid plans, manage budgets and campaigns, all within what your plan
permits.

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
- **Skills** that teach Claude proven, repeatable workflows:
  - `google-ads-audit`: structured account and campaign audits covering baseline,
    wasted spend, search terms, recommendations, change history.
  - `ppc-reporting`: cross-platform performance reports over Ads, Analytics,
    Search Console, and YouTube, as prose or as a shareable dashboard page.
  - `getting-connected`: first-run setup, plans and billing, applying changes, troubleshooting.

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
3. After consent, connect your ad accounts in the
   [dashboard](https://mcp.advisorppc.com/dashboard). Sign in to the ad platform
   with an identity that has access to the account.
4. Ask Claude to list your accounts to confirm everything works.

For a headless or remote machine, use an interactive terminal and follow the
[headless login steps](skills/getting-connected/SKILL.md#headless-or-remote-machine),
including pasting the localhost redirect URL back into the login prompt or
forwarding the callback port.

## Plans

| Plan | Includes |
| --- | --- |
| **Free** | Read-only tools for periodic audits and reports, no card required |
| **Paid** | Write tools (budget and campaign management) and larger allowances |

Ask Claude "what plan am I on?" to see your plan, what it includes and what is
left; the connector's `plan_tool` shows the live terms. To upgrade, ask Claude:
it shows your current plan, asks which plan you want (the plans are listed at
[mcp.advisorppc.com/pricing](https://mcp.advisorppc.com/pricing)), and then
hands over a secure checkout link for the plan you name. Ask about billing or
invoices for a link to the billing page; ask to cancel and Claude explains first,
then gives the cancel link once you confirm.

## What this plugin runs, sends and fetches

- **Runs:** nothing on your machine. The plugin has no hooks, scripts, local
  servers or executables. It is manifests, skills and documentation.
- **Sends and fetches:** only through its one declared connector,
  `https://mcp.advisorppc.com/claude` (in `.mcp.json`). Tool calls you approve
  in Claude go there, and their results come back from there. The connector
  reads and, on paid plans with your approval, changes the ad accounts you
  linked, using the official Google and other platform APIs under your own
  sign-in.
- **Writes:** when you ask for a dashboard, the `ppc-reporting` skill has
  Claude write one static HTML report from the numbers the connector returned.
  It is published as an artifact, or saved as one `.html` file in your working
  folder for you to open. The page contains no code and loads nothing from
  anywhere else.
- **Links:** skills may hand you links to `mcp.advisorppc.com` (dashboard,
  pricing, checkout, billing) and `advisorppc.com` (docs, support). Nothing is
  opened or paid for without you.

## Security

- All product code runs server-side in the hosted connector; this repository
  contains only manifests and documentation, with no executable server code and no
  secrets.
- Authentication is OAuth 2.1 in your own browser. The plugin never asks for,
  stores, or transmits API keys or passwords through configuration files.
- Every write operation is plan-enforced server-side.

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
