---
name: ppc-reporting
description: Builds performance reports and a shareable dashboard page from the user's own Google Ads, Google Analytics 4, Search Console and YouTube accounts through the AdvisorPPC connector. Use when the user wants numbers on how their marketing did, even without the word "report", for example "how did my ads do last month", "pull a performance report", "weekly report for my client", "client report", "monthly recap for my boss", "compare this month to last month", "show me traffic by source", "top search queries", "YouTube channel stats", "how are my TikTok campaigns doing", "show me a dashboard" or "build my PPC dashboard". Read-only; it never changes an account.
license: MIT
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/fill-dashboard.py *)
metadata:
  version: 0.3.0
---

# Cross-Platform PPC Reporting

## Hard rules

- Money is in each account's own currency. Read it from the tool result and never assume USD.
- Never estimate a number a tool can return. Quote the tool's figures; if a figure is missing, say so.
- Reporting is read-only. Any change you suggest is a proposal for the user to approve, never applied from this skill.
- Paid (Ads), site (GA4) and organic (Search Console) numbers measure different things. Never sum them; give each channel its own heading.
- Free plans have a monthly call allowance: one rollup per platform, not loops, and use `limit`.
- GA4 conversions depend on configured key events; confirm with `ga4_list_key_events_tool` before comparing GA4 conversions to Ads conversions.

Pull performance reports from the signed-in user's own accounts using the AdvisorPPC connector. AdvisorPPC is Google-first (Google Ads, GA4, Search Console, YouTube, Tag Manager); the same connector also connects Meta, Microsoft Advertising, TikTok, LinkedIn, Pinterest and X, reached through its operation search.

## Reporting workflow

1. Pin the reporting period first (for example last 30 days, or a named month). Use the same period across every platform in one report.
2. Discover the right resource IDs before reporting; each platform has its own discovery tool.
3. Pull each platform's report, then merge into one narrative: paid performance, then site behavior, then organic search, then video.
4. Present real numbers with period-over-period deltas where available.

Which tool to call for each platform: [references/tools.md](references/tools.md). A report you need that is not in the tool list may be in the catalog: `advisor_search_tools`, then `advisor_tool_help`, then `advisor_read`.

## Dashboard output

When the user asks for a dashboard, a visual report, or something to share with a client or a manager, render the report as the bundled dashboard instead of prose.

1. Pull the data as above, one rollup per platform, with the same period everywhere.
2. Write the numbers as one JSON file in the shape of [references/dashboard-data.md](references/dashboard-data.md), key by key. Do not read `assets/dashboard.html`; it is a template and costs nothing to fill.
3. Run `python3 ${CLAUDE_SKILL_DIR}/scripts/fill-dashboard.py DATA.json OUT.html` (add `--artifact` when publishing with the Artifact tool). It runs locally with no network access, merges the JSON into the template, escapes it, and marks the data as real.
4. Leave out any platform the user has not connected; the page hides a section whose key is missing.
5. Publish OUT.html as an artifact when the session has the Artifact tool, otherwise open it from disk in the browser. Say where it is and which period and account it covers.

The page shows paid, site, organic and video figures under separate headings with period-over-period deltas, daily cost and conversion charts, a sortable campaign table, and the zero-conversion search terms as negative keyword candidates. It uses system fonts and loads nothing from the network. Treat every metric answer this way when the user wants to look at numbers rather than read them.
