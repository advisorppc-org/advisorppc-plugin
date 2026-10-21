# Ad Copy & PMax Asset Quality

> Tool names here are AdvisorPPC operations. Call the ones in your connector's tool list directly. Run any other through `advisor_search_tools`, then `advisor_tool_help`, then `advisor_read` (reads) or `advisor_write` (changes); search by keyword if a name is not found, and treat a missing operation as not on the user's plan, never as a reason to improvise.

Modern ad strength is not about pleasing Google's "Ad Strength" indicator, it's about whether the ad would make a real customer click and convert. Both matter. Hold both bars.

## Responsive Search Ads (RSAs)

### Quality bar

A senior strategist's RSA has:
- **15 distinct headlines** covering different angles: brand, product, benefit, urgency, social proof, USP, location, offer, question, comparison
- **4 distinct descriptions** that work standalone, Google will mix them
- **No keyword-stuffing**: write for humans first
- **Pinned only when necessary**: pin headline 1 for brand/legal, pin H2 for offer, leave the rest unpinned for the algorithm to test
- **Final URL aligned** with the ad's promise (see `landing-page-message-match.md`)
- **Ad extensions present:** sitelinks (≥6), callouts (≥6), structured snippets, call extension (if phone matters), promotion asset if running an offer

### Tools

- Audit existing RSAs: `ga_ad_copy_audit_tool`, `ga_ad_strength_report_tool`
- Generate brief for new copy: `ga_gen_ad_copy_brief_tool`
- Create new RSA: `ga_create_rsa_tool`
- Sitelinks: `ga_create_sitelink_asset_tool`
- Callouts: `ga_create_callout_asset_tool`
- Structured snippets: `ga_create_struct_snippet_tool`
- Call: `ga_create_call_asset_tool`
- Promotions: `ga_create_promo_asset_tool`

### Common ad-copy mistakes (and the fix)

| Mistake | Fix |
|---|---|
| All 15 headlines say roughly the same thing | Diversify, different angles, not different wordings |
| Description is just a list of features | Make it a benefit + CTA |
| Generic CTAs ("Learn More" everywhere) | Specific CTAs ("Book Your 60-Min Adventure") |
| No social proof | Add review count, ratings, "trusted by X+ players" |
| No urgency or differentiation | Find one true differentiator and lead with it |

## Performance Max asset groups

PMax in 2026 is asset-quality-driven. Garbage assets = garbage results, regardless of how much budget you throw at it.

### Asset checklist per asset group

- **Headlines:** 5 short (≤30 chars), 5 long (≤90 chars). Mix benefit, brand, offer, social proof.
- **Descriptions:** 4 short, 1 long. Each works standalone.
- **Images:** at least 4, ideally 15+. Mix landscape (1.91:1), square (1:1), portrait (4:5). High quality, on-brand, NO text overlay (or minimal).
- **Logos:** at least 1 square, 1 landscape.
- **Videos:** at least 1, ideally 3-5. **Don't let Google auto-generate**, they're embarrassing. Provide real videos: 6s, 15s, 30s.
- **Audience signals:** ALWAYS attach. Customer match list + your top in-market segments + custom segments based on competitor URLs/keywords. Use `ga_add_audience_signal_tool`.
- **Final URL expansion:** turn OFF for most accounts unless you've audited where it sends traffic. It will send people to blog posts and 404s if you let it.
- **Brand exclusions:** ALWAYS attach a brand list with your client's brand + competitor brands you don't want PMax stealing. Use `ga_add_brand_excl_camp_tool`.

### Tools

- Inspect: `ga_pmax_gallery_tool`, `ga_asset_group_strength_tool`
- Build: `ga_create_asset_group_tool`, `ga_link_assets_campaign_tool`
- Brand controls: `ga_create_brand_list_tool`, `ga_add_brand_excl_camp_tool`

## Demand Gen ads

Demand Gen replaced Discovery and now also serves YouTube Shorts + in-stream + Gmail.

- Visual-first format: invest in the creative
- Multi-asset creatives perform best
- Lookalike segments + customer match are essential signals
- Tools: `ga_create_demandgen_camp_tool`, `ga_create_demand_gen_ad_tool`

## The marketer's test

Before publishing any ad, read it out loud as if you were the customer searching:
- Does it answer my question?
- Does it differentiate from the next ad in the SERP?
- Would I click it?
- If I clicked, does the landing page deliver what was promised?

If any answer is "no", rewrite, don't publish.
