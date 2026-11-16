# Changelog

All notable changes to the AdvisorPPC plugin are documented here. The hosted
connector is continuously deployed and versioned separately; entries here cover
the plugin manifest and bundled skills.

## [0.3.8] - 2026-11-16

- New skill `first-run`: on "get me started" or just after install, it acts
  at once. It works out from what it can see whether the user is in Claude
  Code or the Claude app (or asks one question), gives that app's connect
  step in plain words (no terminal commands in the Claude app), proves the
  connection with one `ga_accessible_customers_tool` call, and shows a first
  last-30-day result from `ga_account_performance_tool`. Plan facts come only
  from `plan_tool` with action `status`. It never asks for or accepts a
  password, key or token.
- New skill `no-ads-account`: when the user has no Google Ads access or the
  account list comes back empty, it does not stall. It starts from Search
  Console (`sc_top_queries_tool`), or Google Analytics 4
  (`ga4_traffic_by_source_tool`) when no site is listed, gives one small
  report, and offers a weekly check-in the user can ask for. Nothing is
  scheduled.
- `getting-connected`: one line pointing new users to `first-run` and empty
  account lists to `no-ads-account`.
- Evals: seven `claude plugin eval` cases for the two skills under
  `evals/first-run--*` and `evals/no-ads-account--*`, each with its own mocks
  (no real connector or account is touched). How to run them and the pass bar
  are in `evals/first-run-and-no-ads.md`.
- README: the two skills are listed; first run ends with "get me started".

## [0.3.6] - 2026-11-15

- Plans: the README and skills no longer quote usage numbers. The Free plan is
  described as read-only with no card required. The plan and what is left are
  shown by the connector's `plan_tool` with action `status`; the dashboard is no
  longer named as the place to see the allowance. No paid-plan names, prices or
  numeric usage allowances are hard-coded.
- `getting-connected`: new "Buying, changing or cancelling a plan" section.
  Upgrade checks `status`, asks which plan the user wants, points to
  `mcp.advisorppc.com/pricing` when they do not know the plans, then calls
  `upgrade` with the plan they name and hands over the checkout link. Billing and
  invoices go to `manage`; cancelling or downgrading goes to `cancel`, explained
  first and confirmed only after the user says yes. New trigger phrases for
  "how much do I have left", billing, cancelling and applying a fix.
- `getting-connected`: new "Applying a change and plans" section, the single
  rule for turning a finding into a change: check `status`; with a plan that
  includes changes and a change tool present, ask for a yes on each change; if
  the tool refuses for plan reasons, quote the reason and offer the plan steps
  only if wanted; otherwise give the proposal as a list to apply by hand.
  `google-ads-audit` and `ppc-reporting` state that they only read and propose
  and point to that section.
- `getting-connected`: headless login reads the server name from
  `claude mcp list` (`plugin:advisorppc:advisorppc` for a plugin install) and
  uses it in `claude mcp login --no-browser`; the bare name is only for a
  manual install. Manual localhost redirect paste and SSH callback forwarding
  stay.
- `getting-connected`: ad accounts and Google identities are linked in the
  dashboard, separately from the connector sign-in; accounts under another
  identity are reached with `list_google_connections_tool` and
  `select_google_connection_tool`. Reconnecting the MCP server does not change
  linked identities.
- `ppc-reporting` dashboard reference: the usage fields and the header line that
  showed them are removed. The previous period is passed as explicit dates in
  `date_range` (`YYYY-MM-DD,YYYY-MM-DD`). A "Pulls a full dashboard needs"
  section lists each pull by what it fetches and the key it fills.
- `google-ads-audit`: "what changed" comparisons pass the prior period as
  explicit dates in `date_range`.
- README: plan wording without fixed usage numbers, the upgrade, billing and
  cancel routes, and write operations described as plan-enforced server-side.
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
