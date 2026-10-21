# Full Audit Playbook

> Tool names here are AdvisorPPC operations. Call the ones in your connector's tool list directly. Run any other through `advisor_search_tools`, then `advisor_tool_help`, then `advisor_read` (reads) or `advisor_write` (changes); search by keyword if a name is not found, and treat a missing operation as not on the user's plan, never as a reason to improvise.

Use this when the user asks for a full audit of an account ("audit this account", "review this client", "what should we do with this account"). Adapt depth to context: a brand-new client gets the full thing, an existing client may only need a focused refresh.

## Pre-audit setup

Before opening any tool:

1. **Confirm the account.** Ask which client. Cross-verify Google Ads ↔ GA4 ↔ GTM by domain.
2. **Pull the client's brand voice and structure notes:** `client_get_brand_voice_tool`, `client_get_struct_notes_tool`, so the audit reflects who they actually are.
3. **Pull recent worklog:** `client_get_worklog_tool`, so you don't re-recommend things that were just tried.
4. **Set timeframe:** typically 30 days for trends, 90 days for stability checks.

## Audit phases: run in order

### Phase 1: Tracking & data integrity (always first)

**Why first:** every subsequent finding depends on whether the data is trustworthy.

- `ga_conv_tracking_health_tool`
- `ga_conv_source_integrity_tool`
- `ga_enhanced_conv_status_tool`
- `ga4_list_key_events_tool`: confirm primary business events are key events
- `gtm_audit_container_tool`: unfired tags, unused triggers
- Verify GA4 ↔ Google Ads link
- Note any tracking issues at the top of the audit; flag them as **blockers** for performance interpretation

### Phase 2: Account hygiene snapshot

- `ga_audit_account_tool`: full hygiene report
- `ga_disapproved_ads_tool`: disapproved ads (pause preview, then the user's go; see the safe-pause rule)
- `ga_alert_disapproved_ads_tool`: broader policy issues
- `ga_alert_budget_overrun_tool`: campaigns burning budget early
- `ga_quality_score_review_tool`: keywords with low QS

### Phase 3: Performance overview

- `ga_account_performance_tool` for last 30 + 90 days
- `ga_year_over_year_tool`: context vs. last year (especially important for seasonal businesses like escape rooms)
- `ga_campaign_performance_tool`: per-campaign breakdown
- `ga_alert_cpa_spike_tool`, `ga_alert_cvr_drop_tool`, `ga_alert_conv_drift_tool`

### Phase 4: Wasted spend deep-dive

Follow `references/wasted-spend-playbook.md`:
- Search terms report
- Placements
- Geo
- Device
- Day-of-week / time-of-day

### Phase 5: Bidding strategy fit

Follow `references/bidding-strategy-fit.md`: is the strategy right for this account's stage?

### Phase 6: Account structure review

Follow `references/account-structure.md`:
- Brand vs. generic separation
- Budget allocation matches business priority
- PMax + Search overlap with brand exclusions
- Naming convention consistency

### Phase 7: Ad copy & assets

Follow `references/ad-copy-and-pmax-assets.md`:
- RSA quality, ad strength, extension coverage
- PMax asset group strength
- Disapproved or limited ads

### Phase 8: Audience strategy

Follow `references/audience-strategy.md`:
- Customer match list uploaded?
- Lookalikes built from quality seeds?
- Audiences attached to campaigns appropriately?
- Suppression lists for existing customers?

### Phase 9: Landing page & message match

Follow `references/landing-page-message-match.md`:
- Spot-check top 3-5 ads
- Note any obvious mismatches

### Phase 10: Attribution sanity check

Follow `references/attribution-and-ga4-health.md`:
- Compare attribution models
- Look for cannibalization patterns
- Check assist conversions before recommending pause anywhere

## Audit deliverable format

Structure the audit output as:

### Executive summary (3-5 bullet points)
What the marketer needs to know if they only read this section.

### Critical issues (fix immediately)
- Tracking integrity problems
- Disapproved / broken ads
- Budget being lit on fire on terms with no business value

### Strategic opportunities (recommend & discuss)
- Structural changes
- New campaigns / channels to test
- Bidding strategy changes
- Audience additions
- Asset gaps

### Diagnostic notes (context for decisions)
- What's working that should be protected
- What looks bad in data but is strategically important (don't cut)
- Seasonal / external context

### Proposed action plan
For each recommendation:
- **What:** specific change
- **Why:** business reasoning + supporting data
- **Expected impact:** rough magnitude
- **Risk:** what could get worse short-term
- **Approval needed:** yes for every change to the account

### What I propose to pause (waiting on your yes)
- The safe-pause batch (disapproved ads, 404 ad groups, non-core zero-conversion keywords)
- Show before/after

### What I'm waiting on you for
- The list of things needing approval

## Logging the audit

After delivering, log it:
- `client_log_entry_tool`: title: "Full audit", details: summary + key actions
- This builds an audit trail across audits, useful for the next session

## Optional output formats

- HTML dashboard: `ga_optimization_report_tool`, `client_dashboard_html_tool`
- Client-friendly PDF: `client_export_pdf_tool`
- Email digest: `ga_send_weekly_digest_tool`

Use these when the user wants to share the audit externally, but the conversation deliverable should always come first, in the format above.
