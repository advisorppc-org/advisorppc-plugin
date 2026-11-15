# Changelog

All notable changes to the AdvisorPPC plugin are documented here. The hosted
connector is continuously deployed and versioned separately; entries here cover
the plugin manifest and bundled skills.

## [0.3.6] - 2026-11-15

- Plans: the README and skills no longer quote usage numbers. The Free plan is
  described as read-only with no card required, with the current allowance in
  the dashboard. Claude now shows the plan with the connector's `plan_tool`
  (`status`) and hands over its secure checkout link (`upgrade`); the plans page
  is `mcp.advisorppc.com/pricing`. No prices or terms are written into the plugin.
- `google-ads-audit` and `ppc-reporting`: when the user wants a finding applied
  and the plan does not include changes, Claude says so in one line and offers
  the checkout link, and never pushes a plan on read-only requests.
- `getting-connected`: headless and remote login steps (manual localhost
  redirect paste, SSH callback forwarding) and the separate dashboard step for
  connecting ad accounts.
- Repository and install references use `advisorppc-org/advisorppc-plugin`.

## [0.3.5] - 2026-11-13

- Plugin directory file types: the plugin now ships only Markdown, JSON and
  images. `ppc-reporting` no longer bundles an HTML template or a Python fill
  script; Claude writes the dashboard page itself from the data contract and
  page layout in `skills/ppc-reporting/references/dashboard-data.md`, with the
  same sections, charts and escaping rules.
- Logo: `assets/logo.png` re-encoded as a dithered 256-colour PNG (536 KB to
  133 KB), same design, no metadata.
- Skills name the account discovery tool by its live name,
  `ga_accessible_customers_tool` (was `ga_list_accessible_customers_tool`,
  renamed on the connector).

## [0.3.4] - 2026-11-13

- Logo: the plugin now uses the AdvisorPPC directory icon (silver Ai with the green dot).

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
  HTML page bundled with the skill (removed in 0.3.5) with Google Ads KPIs
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
