---
name: campaign-board
description: Publish the AdvisorPPC Campaign Board, a one-page live Google Ads board, as a claude.ai artifact. Use when the user asks for "a board", "a live dashboard", "show me my campaigns on one page", "a campaign overview I can share", "a live Google Ads dashboard", "a dashboard that stays up to date" or "put my account on one page". The page reads Google Ads through the viewer's own AdvisorPPC connector each time it opens, so it needs the connector added in claude.ai under the exact name AdvisorPPC.
---

# Campaign Board

The Campaign Board is a single HTML page that shows a Google Ads account on one screen: KPI tiles with deltas against the previous 30 days and a sparkline, a headline finding, three "worth a look" lines, up to three next actions, spend against daily budget per campaign, daily spend and conversion charts, spend by campaign, the account > campaign > ad group tree and a campaign table.

The page file ships with this skill: `${CLAUDE_PLUGIN_ROOT}/skills/campaign-board/assets/campaign-board.html`. Publish that file as it is. For a one-off snapshot that also covers GA4, Search Console and YouTube, use the dashboard output of the `ppc-reporting` skill instead. Do not rebuild the board from scratch or retype its numbers: it fetches live data itself each time someone opens it.

## Before publishing, tell the user

Say both of these in plain words before you publish:

1. **The connector must be in claude.ai, named exactly `AdvisorPPC`.** The page calls the connector from the viewer's claude.ai account, not from this plugin. Add it under **Settings > Connectors > Add custom connector** with the URL `https://mcp.advisorppc.com/claude` and the name `AdvisorPPC`, with no extra spaces (a name with a trailing space is refused). Google Ads must be connected at `https://mcp.advisorppc.com/dashboard`.
2. **Live numbers show only for signed-in members of their own organization.** Each viewer's numbers come from that viewer's own connector. Someone who opens a public link without signing in, or from outside the organization, sees the sample board with a link to connect AdvisorPPC.

## Publish

Artifacts need Claude Code v2.1.209 or later, signed in with `/login` to a Pro, Max, Team or Enterprise claude.ai account, in an interactive session.

1. If the session offers an artifact runtime skill, load it first. If its documented connector call differs from `artifactConnector()` in the page, change only that function.
2. Publish the file with the Artifact tool, titled **AdvisorPPC Campaign Board**, and declare this capability and nothing more:

   ```json
   {
     "mcp": {
       "server": "AdvisorPPC",
       "tools": [
         "ga_accessible_customers_tool",
         "ga_campaign_performance_tool",
         "ga_list_ad_groups_tool",
         "ga_list_campaigns_tool"
       ]
     }
   }
   ```

   All four tools are read-only. Claude Code asks the user before a publish that declares capabilities; that approval is theirs to give.
3. Give the user the link. On first open, claude.ai asks them to allow the connector. Their account's numbers replace the "Sample data" banner.
4. Sharing is from the **Share** control in the page header. A public link works on Pro and Max; on Team and Enterprise an Owner must first turn on external sharing.

## If the board shows no live data

- The connector is missing, or named something other than `AdvisorPPC`: fix the name in Settings > Connectors and reload.
- The viewer declined the connector prompt: reload to be asked again.
- Google Ads is not connected: the page says so and links to the dashboard.
- On Team and Enterprise, an Owner may have turned off **Enable artifact connectors** under Organization settings > Capabilities.
- Tools that need approval for each call cannot run from an artifact. In claude.ai, set the four read tools above to always allow.

## Limits to mention when they apply

- A client account under a manager is read with that manager as `login_customer_id`; the board does this itself.
- Currency comes from the account list or the daily result; when neither has it, figures carry no symbol.
- Spend against budget uses today's daily budget; a mid-period budget change is not visible, and a shared budget shows per campaign.
- On large accounts a cut result is labelled "Partial" rather than showing wrong totals.

## Without an artifact

If artifacts are not available in the session (an API-key login, `-p` mode, or a Bedrock, Vertex or Foundry provider), say so and offer the same picture in chat instead: `ga_account_performance_tool` and `ga_campaign_performance_tool` for the current and previous 30 days, each shown as the tool's own KPI card and table with a one-line insight above it.
