# Set up your website from Claude

Paste the prompt below into Claude (claude.ai, Claude Desktop or Claude Code)
with your website address. Claude uses the AdvisorPPC setup planner to install
Shield, connect Gravity lead capture, set up Google Tag Manager if you need it,
and start your blog, asking you only for what it cannot look up. Nothing
changes and nothing publishes without your yes.

This page is also the source copy for the "Set up with Claude" section on
advisorppc.com.

## Before you paste

**Claude Code:** install the plugin, which connects every AdvisorPPC server:

```
claude plugin marketplace add advisorppc/advisorppc-plugin
claude plugin install advisorppc@advisorppc
```

**claude.ai or Claude Desktop:** add the Gravity connector (Settings,
Connectors, Add custom connector, `https://gravity.advisorppc.com/mcp`, sign
in). Claude will tell you if the setup needs another one.

## The prompt

```text
Set up AdvisorPPC on my website: <your website address>
Use the AdvisorPPC setup planner and guide me through it.
```

## Plans

Gravity, Shield and the AdvisorPPC connector are paid products. Claude shows
your current plan, what the setup needs and the checkout link before any step
your plan does not include. Plans and pricing: [advisorppc.com](https://advisorppc.com).

## Website section copy (advisorppc.com)

> **Set it all up from one chat**
>
> Paste one prompt into Claude and it sets up Shield, Gravity and your blog
> on your website. Claude finds what your site is built on, places your tags,
> connects Google Ads and your site, plans your first posts and asks you only
> for the few things it cannot look up.
>
> 1. Add the AdvisorPPC Gravity connector to Claude (or install the Claude
>    Code plugin).
> 2. Paste the prompt with your website address.
> 3. Answer Claude's questions and approve each step.
