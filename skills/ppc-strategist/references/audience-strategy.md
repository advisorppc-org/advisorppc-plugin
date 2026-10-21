# Audience Strategy

> Tool names here are AdvisorPPC operations. Call the ones in your connector's tool list directly. Run any other through `advisor_search_tools`, then `advisor_tool_help`, then `advisor_read` (reads) or `advisor_write` (changes); search by keyword if a name is not found, and treat a missing operation as not on the user's plan, never as a reason to improvise.

Audiences in 2026 are no longer "set and forget", they're a primary lever, especially for PMax and Demand Gen where they're the main steering input.

## The four audience layers

Every account should have these, in priority order:

### 1. First-party data (highest value)

- **Customer match list**: uploaded customers (hashed email/phone). The most valuable audience you have.
- **Website visitors** (basic remarketing): segmented by depth (homepage only vs. checkout abandoners)
- **High-value visitor segments**: "Viewed pricing page", "Started booking flow", "Watched video > 50%"

Tools:
- `ga_create_basic_userlist_tool`: empty user list, then upload data
- `meta_create_custom_aud_tool`: for Meta side
- GA4 audiences: `ga4_create_audience_tool`, `ga4_audience_from_dim_tool`

### 2. Lookalike / similar audiences

- Built from your customer match list: Google's lookalike replacement for "similar audiences"
- Quality of seed list determines quality of lookalike, use top 20% of customers, not all of them
- Multiple seeds for different funnel stages (e.g., lookalike of "purchasers" vs. "high LTV purchasers")

### 3. In-market & affinity (Google's segments)

- Useful as **signals for PMax/Demand Gen**, weak as standalone targeting
- Pick segments that map to actual buyer intent (e.g., "Travel/Vacation Activities" for an escape room near a tourist area)
- Do NOT layer too many: dilutes the signal

### 4. Custom segments

- Built from search terms or competitor URLs
- Useful for top-of-funnel: telling Google "people researching these things"
- Examples: list of competitor brand URLs, list of high-intent search phrases

## Audiences for each campaign type

### Search campaigns

- **Audience targeting mode:** `OBSERVATION` (bid-only) by default, never `TARGETING` unless you want to limit reach
- Set via `ga_set_aud_target_mode_tool`
- Attach customer match + remarketing as observation: `ga_add_user_list_adgroup_tool`
- Use bid adjustments based on observed performance (don't set blind +/- )

### Performance Max

- Audience signals are critical: without them, PMax wanders for weeks
- Required signal types: customer match list (highest weight), top in-market segments (1-3 max), custom segments
- Use `ga_add_audience_signal_tool` per asset group

### Demand Gen / YouTube

- Lookalikes work especially well here
- Layer with topic / keyword / placement targeting for cold campaigns
- Use customer match for retargeting + suppression lists

## Suppression & exclusions

Just as important as inclusion:
- Exclude existing customers from acquisition campaigns (uploaded customer list as exclusion)
- Exclude employees / internal traffic
- Exclude past converters from aggressive retargeting (don't keep selling to people who bought)

## Customer match: the underrated weapon

If a client has any kind of CRM, email list, or POS system, you can:
- Upload customer list (`meta_upload_cust_list_tool`, `unified_audience_sync_tool`)
- Build a lookalike from it
- Use it as a PMax audience signal
- Use it for offline conversion uploads to teach Google what "good" looks like (`ga_upload_click_convs_tool`)

This is one of the highest-leverage things you can set up for a client. Most agencies skip it because it requires asking for data. Don't skip it.

## Diagnosing audience problems

| Symptom | Likely cause |
|---|---|
| PMax CPA high & not improving after 3+ weeks | Weak or missing audience signals, add stronger ones |
| Search CPA high on broad terms | Layer customer match observation, see if observed CPA is much better, if yes, raise bid for that audience |
| Retargeting underperforms | Audience too small (<1000 users) OR ads don't differ from cold ads |
| Lookalike doesn't perform | Seed list too small, too noisy, or includes low-value customers |

## The marketer's check

Before adding an audience, ask: **"Who am I trying to reach, and why this audience?"**

Don't add audiences because they're available, add them because they describe a real customer segment you have a real strategy for. Five well-chosen audiences beat fifty random ones.
