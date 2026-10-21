---
name: cro-optimization
description: Conversion-rate optimization for landing pages and lead or checkout flows that receive paid traffic. Use when the user asks "why aren't my ads converting", "my landing page isn't converting", "audit my landing page", "where is my funnel leaking", "which fix should we ship first", "my CPA is high but the clicks look right" or wants a friction audit or a ranked list of conversion fixes. Pulls landing-page performance, Core Web Vitals and on-page signals through the AdvisorPPC connector, checks ad-to-page message match, and ranks fixes by impact, confidence and ease.
---

# CRO optimization

Find the biggest leak in the funnel, fix the cheap obvious things, and send only real uncertainty to an A/B test. Evidence first, opinions last.

Related skills: `landing-page-ab-testing` validates a fix; `ppc-strategist` decides what the campaigns should do; `google-ads-audit` covers the account side.

## Ground rules

- Audit and recommend freely. Changing live pages, prices or offers is the user's call through their own release process.
- No fake urgency, fake scarcity or fake proof as a "CRO tactic". Real deadlines and real limits only.
- Check tracking before blaming the page: `ga_conv_tracking_health_tool` for Google Ads and `ga4_list_key_events_tool` for GA4. A "conversion drop" is often a broken tag.

## Show the numbers the tool rendered

Every metric answer shows the tool's KPI card and table from `content[0]` of the result (or rendered from `structuredContent.metrics_v1`), with one line of insight above it. Never give numbers in prose alone.

## 1. Define the real conversion

Pick the conversion that predicts money, not the easiest one to count. For lead generation that is a qualified lead or booked job, not a form view; for e-commerce it is a completed purchase, not add-to-cart. Agree it with the user before auditing.

## 2. Funnel math

```
Ad click > landing view > CTA click or form start > form submit or checkout > qualified lead or paid order
```

Overall conversion is the product of the step rates. A relative lift at any one step passes through 1:1 to the end, so fix the step with the biggest absolute loss that is cheapest to move.

Worked example (illustrative; replace with real counts):

| Step | Users | Step rate |
|---|---|---|
| Ad clicks | 10,000 | |
| Landing view (page loaded) | 8,600 | 86% |
| Form start | 1,032 | 12% |
| Form submit | 516 | 50% |
| Qualified lead | 310 | 60% |

Click to qualified lead is 3.1%. A 14% gap between clicks and landing views usually means slow loads or redirects: users who bounced before the page painted. Raising form completion from 50% to 65% gives 30% more leads, the same as buying 30% more clicks at no media cost.

Rules for the numbers:

- Count unique users, not sessions. Use fixed windows.
- Split by campaign, device and source. An average hides a broken mobile path.

## 3. Where the data comes from (AdvisorPPC connector)

| Need | Tool |
|---|---|
| Spend and conversions by final URL actually served, with mobile-friendliness | catalog `ga_landing_page_perf_tool` (via `advisor_search_tools`, `advisor_tool_help`, `advisor_read`) |
| Landing page sessions, engagement and key events in GA4 | `ga4_run_report_tool` with the `landingPage` dimension |
| Traffic by source and medium | `ga4_traffic_by_source_tool` |
| Field and lab Core Web Vitals for the page | `seo_core_web_vitals_tool` |
| On-page signals from the real HTML (title, H1, canonical, structured data, links, image alt coverage) | `seo_page_audit_tool` |
| Ad text and final URLs, for message match | `ga_list_ads_tool`, `ga_ad_performance_tool` |
| Queries that bought the clicks | `ga_search_terms_report_tool` |
| Quality score landing-page experience by keyword | `ga_quality_score_review_tool` |

## 4. Friction audit checklist

Score each line 0 (broken), 1 (weak), 2 (good). Audit on a real phone first, then desktop.

**Speed**

- [ ] LCP at or under 2.5 s at p75 on mobile; INP at or under 200 ms; CLS at or under 0.1
- [ ] Hero image preloaded, `fetchpriority="high"`, WebP or AVIF, width and height set, under 250 KB
- [ ] No render-blocking third-party script above the fold; no redirect chain from the ad's final URL

**Above the fold (5-second test: what is it, who is it for, what do I do next)**

- [ ] Headline states the outcome for the searcher, not a category label
- [ ] One primary CTA, visible without scrolling at 360 x 640
- [ ] Real proof visible: the product, the work, the team, real reviews
- [ ] Price, "free quote" or the offer visible or one tap away

**Relevance (message match)**

- [ ] The headline echoes the ad and the keyword that sent the visitor
- [ ] Each ad group lands on the page for its intent, not the homepage
- [ ] Multi-location businesses send each city's traffic to that city's page

**Trust and anxiety**

- [ ] The main objection is answered next to the CTA, not in FAQ item 14
- [ ] Business name, address or service area, phone, privacy link, real reviews
- [ ] Only real, permitted logos and testimonials; none is better than a fake one

**Forms and checkout**

- [ ] Minimum fields; every optional field earns its place
- [ ] Inline validation; errors say how to fix; no CAPTCHA unless abuse is proven
- [ ] Offer, price and terms identical in the ad, on the page and at checkout
- [ ] Phone number tap-to-call on mobile, with call conversions tracked

**Mobile**

- [ ] Tap targets at least 24 x 24 CSS px (WCAG 2.5.8), 44 px for primary CTAs
- [ ] No horizontal scroll at 360 px; sticky CTA after the hero
- [ ] Inputs use the right type (`email`, `tel`) with autocomplete on

**After the conversion**

- [ ] Thank-you page fires the conversion once, and only once
- [ ] Says what happens next and when

## 5. Heuristics (LIFT)

Score the page against six forces and turn each weak one into a hypothesis:

| Force | Question | Example |
|---|---|---|
| Value proposition | Why this, why now? | "Same-day repair, fixed quote before we start" |
| Relevance | Does it match what they searched or clicked? | "Emergency plumber" ads land on the emergency page, not the homepage |
| Clarity | Can they say what it does after 5 s? | Replace jargon with the outcome |
| Anxiety | What worries them? | "Is there a call-out fee?" answered at the CTA |
| Distraction | What competes with the CTA? | Remove the newsletter popup and the full site menu on paid landing pages |
| Urgency | Is there a true reason to act now? | Only real dates and real capacity limits |

## 6. Prioritize (ICE)

ICE = Impact x Confidence x Ease, 1 to 10 each. Confidence must cite evidence.

| Idea | I | C | E | ICE | Evidence | Route |
|---|---|---|---|---|---|---|
| Compress the hero image, remove the redirect | 7 | 8 | 9 | 504 | LCP 4.8 s, 14% click-to-view loss | Ship (fix) |
| Answer "call-out fee" under the CTA | 6 | 6 | 9 | 324 | sales-call notes | A/B test |
| New hero headline | 7 | 4 | 7 | 196 | opinion only | Research, then test |
| Full redesign | 6 | 3 | 2 | 36 | none | Park |

Route rule: bugs and clear friction ship as fixes; plausible but uncertain changes with enough traffic go to `landing-page-ab-testing`; low-traffic ideas get qualitative research (5 recorded sessions, sales-call review) instead.

## 7. Deliverable

```
CRO audit: <page or flow>  Date: <UTC>  Device tested: <phone + desktop>
Funnel: <counts, step rates, campaign and device split>  Data source and window: <...>
Biggest leak: <step> (<rate>, <users lost per week>)
Friction audit: <score>/<max>, zeros first
Top 5 by ICE: <table>  Route: fix | test | research | park
Decisions the user needs to make: <offer, price, page release>
```

## Sources

- web.dev, Web Vitals and thresholds: https://web.dev/articles/vitals
- Conversion.com, the LIFT model: https://www.conversion.com/framework/the-lift-model/
- Baymard Institute, checkout form fields: https://baymard.com/blog/checkout-flow-average-form-fields
- W3C WCAG 2.2, 2.5.8 Target Size (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- Sean Ellis, ICE scoring.
