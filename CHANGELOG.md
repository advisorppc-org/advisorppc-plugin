# Changelog

All notable changes to the AdvisorPPC plugin are documented here. The hosted
connector is continuously deployed and versioned separately; entries here cover
the plugin manifest and bundled skills.

## [0.3.3] - 2026-10-28

- Correct Free plan facts: read-only, no card required, one ad account on any ONE
  of Google Ads, Meta, TikTok, Microsoft Advertising, LinkedIn, Pinterest or X.
  Remove stale numeric quotas from the README and bundled skills.
- Name the supported ad platforms in plugin and marketplace descriptions.
- Document interactive headless OAuth login, manual localhost redirect paste,
  callback port forwarding, and the separate dashboard ad-account connection step.
- Use the advisorppc-org GitHub organization in repository and install references.

## [0.3.2] - 2026-10-21

- Directory listing links: `documentationUrl`, `supportUrl`, `privacyPolicyUrl`
  and `termsOfServiceUrl` in `plugin.json` (the directory reads these from
  `plugin.json` only), so Documentation, Support and Terms stop showing
  "No value".

## [0.3.1] - 2026-10-21

- Directory listing metadata: the marketplace plugin entry now carries the
  same `keywords` as `plugin.json`, plus `repository` and `license`, so the
  Claude directory shows discovery keywords instead of "No value".

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
