# Set up your website from Claude

Copy the prompt below, paste it into Claude (claude.ai, Claude Desktop or
Claude Code), and answer its questions. Claude connects the AdvisorPPC servers,
installs Shield, registers your site with Gravity, connects publishing and
starts your blog. You sign in and approve; Claude does the rest.

This page is also the source copy for the "Set up with Claude" section on
advisorppc.com.

## Before you paste

**Claude Code:** install the plugin. It registers every AdvisorPPC server and
the `website-setup` skill:

```
claude plugin marketplace add advisorppc/advisorppc-plugin
claude plugin install advisorppc@advisorppc
```

**claude.ai or Claude Desktop:** you can paste the prompt straight away. Claude
will ask you to add any connector it is missing (Settings, Connectors, Add
custom connector, paste the address, sign in):

| Connector | Address |
| --- | --- |
| AdvisorPPC (Ads, GA4, Search Console, Tag Manager) | `https://mcp.advisorppc.com/claude` |
| AdvisorPPC Gravity (SEO blog, publishing, leads) | `https://gravity.advisorppc.com/mcp` |
| AdvisorPPC Shield (click-fraud guard) | `https://shield.advisorppc.ai/shield/mcp` |

Every connector signs in with your AdvisorPPC account in the browser. Never
paste a password or API key into the chat.

## The prompt

```text
Set up AdvisorPPC on my website: <your website address>

Use the AdvisorPPC connectors to do the work for me. Ask me only for what you
cannot find yourself, one question at a time, and tell me why you need it.

1. Check which AdvisorPPC connectors you have: AdvisorPPC
   (https://mcp.advisorppc.com/claude), Gravity
   (https://gravity.advisorppc.com/mcp) and Shield
   (https://shield.advisorppc.ai/shield/mcp). For any that is missing, tell me
   exactly how to add it in the app I am using, wait for me, then continue.
2. Find out what my site is built on with gravity_detect_platform, and use
   that for every instruction you give me.
3. Shield: register my site, give me the tracking tag with step-by-step
   placement for my platform, connect my Google Ads account so fraudulent IPs
   are excluded, ask me which ad account to protect, and ask me before turning
   on automatic exclusion.
4. Gravity: register my site, give me the lead-capture tag for my contact
   form, save my business profile and branding (read my site first, then ask
   me only for the gaps), and offer to connect Search Console and GA4.
5. Blogging: connect publishing (WordPress Application Password, or a webhook
   or feed if I am not on WordPress), agree two or three topics with me, plan
   the first posts, write the first one for my review, and once I approve it,
   queue it on the publishing schedule.
6. TrackTor: tell me whether it is available yet. If it is not, check my
   current conversion tracking with the Tag Manager and GA4 tools instead.

Rules: show me a preview before every change and wait for my yes. Never
publish a post live without my explicit approval of that post. If a tool
returns an error or a plan limit, tell me what it said and what my options are.
Finish with a table: each product, its status, and the one thing left for me
to do.
```

## Website section copy (advisorppc.com)

Drop-in copy for a "Set up with Claude" section. Headline, one paragraph, the
three steps, then the prompt above in a code block with a Copy button.

> **Set it all up from one chat**
>
> Paste one prompt into Claude and it sets up Shield, Gravity and your blog
> on your website for you. Claude finds what your site is built on, creates
> your tags, connects Google Ads and WordPress, plans your first posts and
> asks you only for the few things it cannot look up.
>
> 1. Open Claude and add the AdvisorPPC connectors (or install the Claude Code
>    plugin).
> 2. Copy the prompt below and paste it in with your website address.
> 3. Answer Claude's questions and approve each step. Nothing changes and
>    nothing publishes without your yes.
>
> TrackTor conversion tracking is coming soon. Until then, Claude checks your
> existing Tag Manager and GA4 setup instead.
