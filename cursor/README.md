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

## Use

Ask in Cursor chat, for example:

- "List my Google Ads accounts."
- "Show campaign performance for the last 30 days."
- "Top Search Console queries for my site this month."

Read tools return data and change nothing. Some tools can change your ad accounts (for example, pause a campaign or change a budget), depending on your plan. By default, Cursor asks before it runs a tool call. In Auto-review, an allowlisted tool can run without that ask. `advisor_write` returns a preview and applies the change only after you confirm. Other change tools do not return a preview, so a call that runs is applied.

## Plans

The plugin is free to install. What the server lets you do depends on your AdvisorPPC plan: https://advisorppc.com/pricing

## Privacy, terms and support

- Privacy policy: https://mcp.advisorppc.com/privacy
- Terms of service: https://mcp.advisorppc.com/terms
- Support: https://advisorppc.com/support

## License

MIT. See `LICENSE` at the repository root.
