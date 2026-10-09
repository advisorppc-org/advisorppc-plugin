---
name: website-setup
description: This skill should be used when the user asks to "set up my website with AdvisorPPC", "install Shield", "protect my ads from click fraud", "set up Gravity", "start my blog", "automate my blog posts", "capture leads from my site", "set up TrackTor", "track conversions on my site", or pastes the AdvisorPPC website setup prompt. It walks Claude through connecting the AdvisorPPC MCP servers and setting up Shield, Gravity (SEO blogging and lead capture) and TrackTor on one website, asking the user only for what the tools cannot find themselves.
version: 0.1.0
---

# Website Setup: Shield, Gravity, TrackTor

Set up the AdvisorPPC products on one website from inside Claude. Claude runs
the tools. The user only signs in, approves, and supplies what no tool can find
(a WordPress Application Password, which Google Ads account to protect, a
choice of topics). Ask for one thing at a time, and say why you need it.

## The servers

| Product | MCP server | Endpoint |
| --- | --- | --- |
| Ads, GA4, Search Console, Tag Manager | `advisorppc` | `https://mcp.advisorppc.com/claude` |
| Gravity (SEO blog, publishing, leads) | `advisorppc-gravity` | `https://gravity.advisorppc.com/mcp` |
| Shield (click-fraud guard) | `advisorppc-shield` | `https://shield.advisorppc.ai/shield/mcp` |
| TrackTor (conversion tag) | none yet | Not live. See step 6. |

The plugin registers all three servers. Every one signs in with browser OAuth;
never ask for or accept an API key, a password for the AdvisorPPC account, or a
token in chat.

## Rules

- **Preview, then confirm.** Every write tool returns a preview when called
  without `confirm=true`. Show the user the preview in one or two lines and get
  a yes before calling it again with `confirm=true`. Never confirm on the
  user's behalf.
- **Report errors as they come back.** Tools return `{"error": ...}` instead of
  failing. Tell the user what it says. If it says a plan or quota limit, name
  the limit and point to `gravity_plan` or `shield_upgrade_link`; do not retry.
- **Never publish live without an explicit yes for that page.**
  `gravity_publish_site` and `gravity_publish_wordpress` put a page on the
  public site the moment they are confirmed.
- **Do not invent tools.** If a tool named here is missing from the connected
  server, say so and carry on with the rest.

## 0. Check what is connected

List the tools you have. Look for `shield_*`, `gravity_*` and `ga_*` names.

- A server is missing: in Claude Code, ask the user to run `/mcp` and connect
  it (the plugin already registered it). In claude.ai, Claude Desktop or
  another client, give them the endpoint from the table above and ask them to
  add it as a custom connector: Settings, Connectors, Add custom connector,
  paste the URL, sign in. Then continue.
- The user only wants some products: set up only those.

## 1. Learn the site

Ask for the website address if you do not have it. Then call
`gravity_detect_platform(domain)`. It costs two requests and no credentials and
tells you whether the site is WordPress, Shopify, Wix, Webflow, Next.js and so
on, and what Gravity can connect to today. Use the platform for every
"where do I paste this" instruction below. Never ask a non-WordPress site for a
WordPress Application Password.

## 2. Shield: stop paying for fraudulent clicks

1. `shield_list_sites`. If a site exists, reuse it.
2. Otherwise `shield_create_site(name)`, show the preview, then confirm. Keep
   the returned `snippet`.
3. Give the user the snippet with placement steps for their platform
   (section "Placing a tag" below). It belongs in the `<head>` of every landing
   page that receives paid traffic.
4. `shield_google_status`. If not connected, `shield_connect_google` returns a
   one-time link valid for 15 minutes. Ask the user to open it and sign in with
   the Google account that owns or manages the ad account. Then call
   `shield_google_status` again.
5. Ask which customer id should receive the IP exclusions, then
   `shield_set_google_account(customer_id)`, preview, confirm.
6. Automatic exclusion is off by default. Explain it in one sentence (clicks
   scored as fraud at or above a threshold are excluded in Google Ads without
   asking each time) and ask whether to turn it on. Only on a yes:
   `shield_update_settings(auto_exclude_enabled=true)`, preview, confirm.
7. Optional: `shield_connect_bing` for Microsoft Advertising.
8. Verify: after the tag is live and a paid click has landed, `shield_overview`
   and `shield_recent_clicks` show traffic. Before that, say clearly that
   Shield is installed but has not seen a click yet.

## 3. Gravity: register the site and catch leads

1. `gravity_list_sites`. Reuse a site for the same domain.
2. Otherwise `gravity_register_site(name, domain)`, preview, confirm. Keep the
   returned site id and lead-form `api_key`.
3. Lead capture: give the user this tag with their key and the CSS selector of
   their contact form (ask for it, or suggest `#contact-form`):

   ```html
   <script src="https://gravity.advisorppc.com/snippet.js?key=SITE_API_KEY"
           data-gravity-form="#contact-form"></script>
   ```

4. Business profile, so every post sounds like the business:
   `gravity_set_business_profile(site_id, ...)`. Fill what you can from the
   site itself, then ask the user only for the gaps (services, location, tone,
   audience). Preview, confirm.
5. Branding: `gravity_brand_learn(site_id)`, preview, confirm. It reads the
   live site politely and stores colors, fonts and logo for post layout.
6. Search data (optional, recommended): `gravity_google_connect_url(site_id)`
   returns a single-use Google link (10 minutes) for Search Console and GA4.
   After the user signs in, `gravity_gsc_sites` and `gravity_google_link_site`
   bind the right property.

## 4. Gravity: connect publishing

Pick the route from step 1.

- **WordPress.** Ask the user to create an Application Password (WordPress
  admin, Users, Profile, Application Passwords; `gravity_detect_platform`
  may return the exact `authorize_url`). It is not their login password. Then
  `gravity_connect_wordpress(site_id, wp_url, wp_username, wp_app_password)`,
  preview, confirm. The result carries a `wordpress.ok` check; if it is false,
  read the reason to the user and ask them to recheck the user name and
  password.
- **Any other site** (Shopify, Webflow, Wix, Next.js, static):
  - a signed webhook their site or developer owns:
    `gravity_webhook_connect(site_id, endpoint_url)`; the signing secret is
    shown once, tell the user to store it in their site's settings;
  - or a feed: `gravity_feed_enable(site_id)` returns a JSON Feed and RSS URL
    once; treat the URL like a password;
  - or export per post: `gravity_export_content(content_id, format)`.

## 5. Gravity: the automated blog

1. Topics: agree two or three topics with the user, then
   `gravity_set_topic(site_id, name, keywords, questions, competitors)` for
   each, preview, confirm.
2. Plan: `gravity_topic_plan(site_id, slug)` turns topic gaps into planned
   posts (preview, confirm). Or write a plan yourself and save it with
   `gravity_plan_calendar(site_id, items)`.
3. Write: read `gravity_business_profile` first, then write the first post
   yourself and save it with `gravity_save_article(site_id, ...)`. Show it to
   the user. Only when they approve, save it again with `status='approved'`.
4. Schedule: `gravity_queue_page(content_id, publish_fields)` reserves a slot
   on the publishing queue (preview, confirm). The queue publishes on a fixed
   cadence after preflight checks. `gravity_publish_queue` shows the slots and
   `gravity_publish_receipts` shows what happened. If the user wants one post
   live now instead, use `gravity_publish_site` (or
   `gravity_publish_wordpress`) with an explicit yes for that page.
5. Tell the user how to keep it going: in any new chat, "write and queue next
   week's posts for my site" runs steps 2 to 4 again.

## 6. TrackTor: conversion tracking

TrackTor is not live yet. There is no TrackTor tool to call and no tag to
install today. Tell the user that plainly, offer to note their interest, and
do not hand them a placeholder tag. Until it ships, conversion tracking runs
through their existing Google Tag Manager and GA4: with the `advisorppc`
server connected, `gtm_audit_container_tool` and `ga_conv_tracking_health_tool`
check what is already firing.

## Placing a tag

Give the steps for the platform `gravity_detect_platform` found.

- **WordPress**: a header-code plugin (for example WPCode, "Header and
  Footer") or the theme's header settings. Paste in the header, save.
- **Shopify**: Online Store, Themes, Edit code, `theme.liquid`, paste just
  before `</head>`.
- **Wix**: Settings, Custom code, Add code, place in Head, all pages.
- **Webflow**: Site settings, Custom code, Head code, publish.
- **Squarespace**: Settings, Advanced, Code injection, Header.
- **Google Tag Manager**: a Custom HTML tag on All Pages.
- **Code-based site**: the shared layout's `<head>`.

Then ask the user to tell you when it is saved, and open the site's home page
source to confirm the tag is present if you can fetch pages.

## Finish with a summary

End with one short table: product, status (done, waiting on the user, not
available), and the one next action for each.
