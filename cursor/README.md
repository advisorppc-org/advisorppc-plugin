# AdvisorPPC for Cursor

This plugin adds the AdvisorPPC MCP server to Cursor. It connects Cursor to the advertising and analytics accounts you have already authorized in AdvisorPPC, such as Google Ads, Google Analytics 4, Search Console, Tag Manager and YouTube.

No local process runs. The server is hosted at `https://mcp.advisorppc.com/connector`.

## Connect

1. Install the plugin from the Cursor Marketplace.
2. On first use, Cursor opens AdvisorPPC sign-in in your browser (OAuth). Sign in and approve the connection.
3. Connect the Google account that has access to your ad accounts from the AdvisorPPC page the sign-in lands on. The server can open only the accounts the signed-in user can already see.

To add the server by hand instead, merge this into `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "advisorppc": {
      "url": "https://mcp.advisorppc.com/connector"
    }
  }
}
```

When this plugin is installed, Cursor shows the server as `plugin-advisorppc-advisorppc`. Manage it from Customize in the sidebar. The hand-added entry above stays named `advisorppc`.

## Use

Ask in Cursor chat, for example:

- "List my Google Ads accounts."
- "Show campaign performance for the last 30 days."
- "Top Search Console queries for my site this month."

Read tools return data and change nothing. Some tools can change your ad accounts, depending on your plan. By default, Cursor asks before it runs a tool call. In Auto-review, an allowlisted tool runs immediately, and every other tool is routed through the classifier. `advisor_write` returns a preview and applies the change only after you confirm that preview. Some directly listed change tools apply on the first call and have no confirm argument. That includes `ga_pause_campaign_tool`, `ga_enable_campaign_tool`, `ga_pause_ad_group_tool`, `ga_enable_ad_group_tool`, `ga_pause_ad_tool`, `ga_enable_ad_tool`, `ga_pause_keyword_tool` and `ga_enable_keyword_tool`. `disconnect_platform_tool`, `switch_account_tool` and `update_settings_tool` return a preview when confirm is false and apply only when confirm is true.

## Plans

The plugin is free to install. What the server lets you do depends on your AdvisorPPC plan: https://advisorppc.com/pricing

## Privacy, terms and support

- Privacy policy: https://mcp.advisorppc.com/privacy
- Terms of service: https://mcp.advisorppc.com/terms
- Support: https://advisorppc.com/support
- Assistant and Google permissions the connector requests: https://mcp.advisorppc.com/docs/security

## License

MIT. See `LICENSE` at the repository root.
