# Changelog

All notable changes to the AdvisorPPC plugin are documented here. The hosted
connector is continuously deployed and versioned separately; entries here cover
the plugin manifest and bundled skills.

## [0.5.0] - 2026-10-21

### Added
- Directory listing fields in `plugin.json`: `icon`, `documentationUrl`, `supportUrl`, `privacyPolicyUrl`, `termsOfServiceUrl`, plus `repository`, `license` and the author email. Anthropic's directory reads them from the manifest only.

- Slash commands: `/advisorppc:dashboard`, `/advisorppc:audit`, `/advisorppc:waste`,
  `/advisorppc:connect`. Each carries its exact steps, so a run loads a few lines
  instead of a whole skill.
- `google-ads-audit` can render the account audit as a review page
  (`skills/google-ads-audit/assets/audit.html`): severity tiles, category
  breakdown, numbered proposed actions with evidence and the tool that applies
  each, findings, partial failures.
- `fill-dashboard.py` takes `--template` so one script fills both pages.
- Dashboard footer shows plan and a "Plans and upgrade" link (advisorppc.com only);
  the pages never take payment.
- `/advisorppc:waste` reads the search terms report, sums each term across
  ad groups, skips brand-looking terms, reads the chosen list back, and only
  then adds EXACT negatives with `ga_add_negative_keyword_tool`, one call per
  term, on plans that allow writes.

## [0.3.0] - 2026-10-21

- `ppc-reporting` can now render its report as a dashboard: a self-contained
  HTML page (`skills/ppc-reporting/assets/dashboard.html`) with Google Ads KPIs
  and period deltas, daily cost and conversion charts, a sortable campaign
  table, zero-conversion search terms, GA4 traffic by source, Search Console
  totals and top queries, and YouTube channel stats. Light and dark themes.
- Data contract for the page in `skills/ppc-reporting/references/dashboard-data.md`,
  one connector tool per key.
- New trigger phrases: "show me a dashboard", "build my PPC dashboard".

## [0.2.0] - 2026-09-24

Copy and metadata only. No functional change.

- Manifest and marketplace descriptions rewritten; Analytics is now named
  Google Analytics 4.
- Author and marketplace owner set to Advisor Media Group LLC.
- Added keywords: `google-ads-audit`, `wasted-ad-spend`, `negative-keywords`,
  `ppc-reporting`.
- Removed em dashes from the README, SECURITY, SUPPORT and CHANGELOG copy.

## [0.1.0] - 2026-08-28

Initial public release.

- Remote MCP server registration for the hosted connector at
  `mcp.advisorppc.com/claude` (browser OAuth, no API keys in config).
- Bundled skills: `google-ads-audit`, `ppc-reporting`, `getting-connected`.
- Self-hosted marketplace definition: install directly from
  `advisorppc-org/advisorppc-plugin`.
