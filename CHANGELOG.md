# Changelog

All notable changes to the AdvisorPPC plugin are documented here. The hosted
connector is continuously deployed and versioned separately; entries here cover
the plugin manifest and bundled skills.

## [0.3.3] - 2026-10-21

Spec upgrade against the 2026-10 plugin, skills and directory docs.

- Skills: `version` moved into `metadata.version` and `license: MIT` added in
  every `SKILL.md`; descriptions now say what each skill does and when to use
  it, key case first, with indirect triggers ("CPA spiked", "wasted spend",
  "client report", "connect my Google Ads"). Hard rules (account currency,
  never estimate, proposals only) sit at the top of each skill.
- Tool names follow the live connector (`ga_accessible_customers_tool`;
  stale `sc_compare_periods_tool` and `gtm_list_triggers_tool` references
  removed from the reporting catalogue).
- `ppc-reporting`: runs its helper as `${CLAUDE_SKILL_DIR}/scripts/fill-dashboard.py`
  with a matching `allowed-tools` rule, links `references/dashboard-data.md`,
  and moves the per-platform tool catalogue to `references/tools.md`.
- `dashboard.html` uses system fonts and no longer loads Google Fonts, so the
  plugin makes no network calls of its own.
- README and SECURITY name the one local script and what it does, instead of
  "no executable code"; README install lines use `advisorppc-org/advisorppc-plugin`.
- Copy says Google-first and names the other platforms the connector connects
  (Meta, Microsoft Advertising, TikTok, LinkedIn, Pinterest, X).
- `plugin.json`: `displayName`; `repository` points at
  `github.com/advisorppc-org/advisorppc-plugin` (also in the marketplace entry).
- New `evals/` suite (8 cases, mocked connector) for `claude plugin eval`, and a
  `validate` GitHub Actions workflow running
  `claude plugin validate --strict --profile directory .` on pull requests.
- The MCP endpoint stays `https://mcp.advisorppc.com/claude`, the URL the
  directory connector listing uses.

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
  `advisorppc/advisorppc-plugin`.
