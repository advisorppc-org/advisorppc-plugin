# Wasted Spend Playbook

> Tool names here are AdvisorPPC operations. Call the ones in your connector's tool list directly. Run any other through `advisor_search_tools`, then `advisor_tool_help`, then `advisor_read` (reads) or `advisor_write` (changes); search by keyword if a name is not found, and treat a missing operation as not on the user's plan, never as a reason to improvise.

The single highest-leverage activity in most accounts. The goal: kill spend that has no chance of producing a conversion *and* no strategic value, while protecting spend that does have strategic value (brand defense, awareness, retargeting feeders, etc.) even if its direct ROAS looks weak.

## The marketer's filter: apply before any "cut"

Before pausing a keyword, placement, geo, or campaign, ask:

1. **Is this strategically core?** (brand, primary category, primary geo) → Do not cut even if low-converting. Diagnose instead.
2. **Is conversion tracking healthy here?** → If not, fix tracking first.
3. **Is the lookback window long enough?** → 7 days of data on a low-volume keyword is noise, not signal.
4. **Is there a structural issue causing the waste?** (broad match pulling junk, wrong landing page, broken final URL) → Fix the cause, don't just pause the symptom.
5. **Does the search term/placement match a real person we want as a customer?** (this is the marketer test, not a number)

Only if all five filters are passed is "pause" the right answer.

## Search terms: the #1 source of waste

Workflow:

1. Pull search terms with `ga_search_terms_report_tool` for last 30-90 days
2. Sort by spend descending
3. Categorize each high-spend term:
   - **Converting:** leave alone (or move to its own ad group if volume justifies)
   - **Relevant but not converting yet:** keep watching, check if QS / landing page / message match is the issue
   - **Irrelevant junk** (e.g., "free escape room games online" for a paid in-person escape room): negative keyword
   - **Brand of competitor:** decide policy (some agencies bid, some don't, confirm with user)
4. Add negatives at appropriate level:
   - Account-level for terms that should never apply: `ga_add_account_neg_kw_tool`
   - Campaign-level for campaign-specific exclusions: `ga_add_negative_keyword_tool`
   - Shared negative list for portfolio-wide patterns: `ga_add_shared_neg_list_tool`
5. For PMax: use `ga_create_brand_list_tool` for brand exclusions and audience signals to steer it

**Use the dedicated tool:** `ga_propose_negatives_tool` and `ga_find_wasted_spend_tool` are scan-only, they propose, you decide.

## Placements (Display, YouTube, PMax)

- Pull placements via `ga_list_placements_tool`
- Mobile app placements are notorious waste, exclude broadly: `ga_excl_website_plcs_tool` for known-junk apps
- Set content exclusions: `ga_set_content_excl_tool` to exclude sensitive content / parked domains / made-for-advertising sites
- For YouTube: review channel + video placements, exclude irrelevant ones with `ga_excl_yt_channel_plcs_tool` / `ga_excl_yt_video_plcs_tool`

## Geography

- Pull geo performance: `ga_hist_geo_perf_tool`
- For local businesses (escape rooms): geo waste is usually showing in adjacent cities or wrong country
- Check the **geo target type setting**: `Presence` vs `Presence or Interest`. For most local businesses, set to `Presence` only: `ga_set_geo_target_type_tool`
- If a geo has high spend, zero conversions, AND is outside the realistic catchment area → exclude with `ga_set_camp_locations_tool`
- For escape rooms specifically: people travel for them. Don't exclude a 60-min-drive city just because conversions are low, they may be searching, comparing, then driving

## Devices

- Pull device split: `ga_hist_device_perf_tool`
- Mobile often converts worse for high-consideration purchases, but that doesn't mean cut it. Check:
  - Is the mobile landing page actually mobile-optimized?
  - Is the booking flow mobile-friendly?
  - Are users researching on mobile and converting later on desktop? (cross-device, `ga4_attr_model_compare_tool`)
- Bid adjustments only after diagnosis: `ga_set_device_bid_adjust_tool`

## Time-of-day / day-of-week

- Pull seasonality: `ga_seasonality_by_hour_tool`, `ga_season_by_weekday_tool`
- Don't cut hours without considering: are customers researching at 11pm but booking at 10am the next day? (assist conversions matter)
- Use `ga4_assisted_conversions_tool` to check first-touch role before cutting

## What "good" looks like after a cleanup

- Search terms report has < 10% obviously-junk spend in the next 30 days
- No mobile app placements running unless intentional
- Geo targets aligned with catchment area + presence-only setting
- Device bid adjustments backed by actual ROAS by device, not vanity CVR
- A documented audit trail (use `client_log_entry_tool`) so the client knows what was changed and why
