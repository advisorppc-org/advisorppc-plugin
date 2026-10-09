# Changelog

All notable changes to the AdvisorPPC plugin are documented here. The hosted
connector is continuously deployed and versioned separately; entries here cover
the plugin manifest and bundled skills.

## [0.3.0] - 2026-10-09

- Registered two more hosted servers: `advisorppc-gravity`
  (`https://gravity.advisorppc.com/mcp`) and `advisorppc-shield`
  (`https://shield.advisorppc.ai/shield/mcp`).
- New skill `website-setup`: sets up Shield, Gravity lead capture, publishing
  and the automated blog on a website, preview first, with TrackTor reported as
  not yet available.
- New `SETUP-PROMPT.md`: the copy-paste setup prompt and the website section
  copy for advisorppc.com.

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
