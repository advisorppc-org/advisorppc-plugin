# Changelog

All notable changes to the AdvisorPPC plugin are documented here. The hosted
connector is continuously deployed and versioned separately; entries here cover
the plugin manifest and bundled skills.

## [0.4.0] - 2026-10-21

New skills, and every skill brought up to date with the live connector.

- New `ppc-strategist`: the senior-advisor voice, with account checks across
  Google Ads, GA4 and Tag Manager, a tracking check before trusting numbers,
  safe-pause rules, and ten playbooks under `references/`.
- New `campaign-board`: publishes the AdvisorPPC Campaign Board artifact, which
  reads Google Ads live through the viewer's own claude.ai connector.
- New `cro-optimization` and `landing-page-ab-testing` for landing pages that
  receive paid traffic, with a bundled A/B test calculator.
- `getting-connected`, `google-ads-audit` and `ppc-reporting` use today's tool
  names (`ga_accessible_customers_tool`, `list_google_connections_tool`,
  `ga_conv_tracking_health_tool` and others), cover TikTok Ads reporting, and
  show every metric as the connector's KPI card and table. The `ppc-reporting`
  dashboard from 0.3.0 stays, and points to `campaign-board` for a live board.
- Skill descriptions list trigger phrases; the unsupported `version` key is
  removed from skill frontmatter.
- `tests/check_skills.sh` and a CI workflow check every skill's frontmatter,
  description length, em dashes, secret patterns and internal names, and
  validate the plugin and marketplace manifests.

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
  `advisorppc/advisorppc-plugin`.
