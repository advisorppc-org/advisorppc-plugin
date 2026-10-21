# Attribution & GA4 Health

> Tool names here are AdvisorPPC operations. Call the ones in your connector's tool list directly. Run any other through `advisor_search_tools`, then `advisor_tool_help`, then `advisor_read` (reads) or `advisor_write` (changes); search by keyword if a name is not found, and treat a missing operation as not on the user's plan, never as a reason to improvise.

In 2026, attribution is messy by design. Cookies are limited, iOS strips signal, consent mode shapes data, and Google Ads & GA4 often disagree on numbers. A senior strategist knows what to trust and what to question.

## The "which number is right?" hierarchy

When Google Ads and GA4 show different conversion counts for the same event, neither is "wrong", they measure different things. Trust:

1. **Server-side / first-party measurement** (sGTM with offline conversion uploads), most accurate
2. **Google Ads conversions with enhanced conversions enabled**: closest to truth for paid media decisions
3. **GA4 key events**: better cross-channel view, but uses different attribution
4. **Platform-reported conversions (Meta, etc.)**: most inflated, treat as directional

If the client business has a backend system (CRM, POS, booking system) that knows about real revenue, **trust that over any ad platform.** Build the workflow to send that data back to Google via offline conversions.

## GA4 health audit

Run these checks before trusting any GA4 data:

- **Data retention**: should be 14 months: `ga4_set_data_retention_tool`
- **Key events configured**: primary business outcomes marked: `ga4_list_key_events_tool`
- **No duplicate events firing**: check via `ga_conv_source_integrity_tool`
- **Google Ads link healthy**: `ga4_list_ads_links_tool`
- **Cross-domain configured** if booking happens on different domain
- **Internal traffic excluded** (employees / agency IPs)
- **Data redaction on** for PII protection: `ga4_set_data_redaction_tool`
- **Realtime check**: fire a test event, see it in `ga4_realtime_tool`

## Attribution model

Default in 2026: **Data-Driven Attribution (DDA)**, set via `ga4_set_attr_settings_tool`

DDA is the right default because:
- Last-click undervalues upper-funnel (Demand Gen, YouTube)
- First-click undervalues bottom-funnel (Brand search)
- Position-based and linear are arbitrary

When DDA isn't right:
- Very low conversion volume (< 300/month): DDA can't model well, fall back to last-click
- Single-channel strategy (only one channel running), attribution model is irrelevant

## Comparing models: when to do it

Use `ga4_attr_model_compare_tool` periodically to:
- Spot channels that look bad in last-click but great in DDA (likely under-credited assist channels)
- Spot channels that look great in last-click but mediocre in DDA (likely cannibalizing)

Common patterns this surfaces:
- Brand search inflated under last-click (people would have come anyway via direct/organic)
- Demand Gen / YouTube undercredited under last-click (real assist value)
- PMax cannibalizing brand: see if PMax credit drops dramatically with brand exclusions

## Conversion paths analysis

For complex buyer journeys, use `ga4_conversion_paths_tool` and `ga4_assisted_conversions_tool` to see:
- How many touchpoints before conversion
- Which channels appear early (assist) vs. late (closer)
- Time-to-convert distribution

This is essential context before recommending "kill the campaign with no conversions", it might be the assist channel that makes everything else work.

## Cross-channel reconciliation

Best practice: pull spend + conversions from every paid channel and reconcile against GA4 + the client's actual business outcome (bookings, sales, leads in CRM).

Tools: `unified_reporting_tool` for cross-platform spend rollup.

If you see big gaps between platform-reported conversions and GA4 / business outcome:
1. Tracking integrity issue: fix first
2. Attribution mismatch: explain to client, don't try to "fix" it
3. Ad fraud / bot traffic: investigate

## Consent mode & modeling

Consent mode v2 is the EEA standard, increasingly the global default. When users decline cookies:
- Google models the missing conversions
- Modeled conversions appear in Google Ads as if observed
- GA4 also uses modeling

If a client is in EEA / UK and consent mode isn't configured properly:
- GA4 will show large gaps
- Google Ads conversions will undercount → smart bidding will under-deliver
- Fix: configure consent mode v2 in GTM, set `ads_data_redaction` and `url_passthrough`

## The marketer's read on attribution

Numbers will never perfectly match. The strategist's job is not to chase a perfect number, it's to:

- Know which numbers are directional vs. exact
- Use the right number for the right decision (Google Ads conversions for bid decisions, business-outcome for budget decisions)
- Communicate the difference to clients clearly
- Never let attribution debates paralyze action

A 10% measurement gap is normal. A 50% gap means something is broken. Fix the tracking, don't argue about the platforms.
