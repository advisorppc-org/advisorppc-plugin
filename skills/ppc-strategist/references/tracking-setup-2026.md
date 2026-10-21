# Tracking Setup: 2026 Stack

> Tool names here are AdvisorPPC operations. Call the ones in your connector's tool list directly. Run any other through `advisor_search_tools`, then `advisor_tool_help`, then `advisor_read` (reads) or `advisor_write` (changes); search by keyword if a name is not found, and treat a missing operation as not on the user's plan, never as a reason to improvise.

The current best-practice stack as of April 2026. This is what a senior tracking expert sets up for a new client (or fixes for an existing one).

## The non-negotiable foundation

Every client should have:

1. **GA4** with at least one web data stream and (if app exists) a Firebase link
2. **GTM** (web container): server-side GTM (sGTM) where budget allows, especially for ecommerce / lead gen with high CPL
3. **Google Ads** account linked to GA4 (`ga4_create_ads_link_tool`)
4. **Enhanced Conversions for Web** enabled and verified
5. **Consent Mode v2** implemented (required for EEA traffic, strongly recommended everywhere)
6. **Server-side conversion API** for high-value events when feasible

## Step-by-step setup workflow

### Phase 1: Discovery & verification (always first)

- Confirm the **business**: name, primary domain, secondary domains, country
- Identify all destination URLs the ads will use, confirm they're all on confirmed-owned domains
- Verify the user has admin access in GA4 (`ga4_list_properties_tool`), GTM (`gtm_list_accounts_tool`), and Google Ads (`ga_accessible_customers_tool`)

### Phase 2: GA4 baseline

- Confirm property currency, timezone, industry category
- Set data retention to 14 months: `ga4_set_data_retention_tool`
- Enable Google Signals if appropriate: `ga4_set_google_signals_tool`
- Enable enhanced measurement on web stream: `ga4_set_enhanced_meas_tool`
- Set attribution model + lookback windows: `ga4_set_attr_settings_tool`, default to data-driven attribution unless there's a reason not to
- Configure data redaction (PII protection): `ga4_set_data_redaction_tool`

### Phase 3: Define key events (formerly "conversions")

- List the actual business outcomes: for an escape room: `booking_complete`, `add_to_cart` (room selection), `phone_call_click`, `gift_card_purchase`, `inquiry_form_submit`
- Mark them as key events: `ga4_create_key_event_tool`
- For each, decide counting method (once per session vs. every) and default value
- Tier them: primary (booking_complete) vs. secondary (form_submit), primary should be what bidding optimizes toward

### Phase 4: GTM tags & triggers

- Create GA4 config tag (`gtm_quick_setup_ga4_tool`)
- Create Google Ads conversion tag for each primary key event (`gtm_setup_ads_conv_tool`)
- Create Meta Pixel if running Meta ads (`gtm_setup_meta_pixel_tool`)
- Triggers tied to actual events from the data layer, not URL-based unless there's no choice
- Always test in GTM Preview Mode before publishing
- Use folders to keep tags organized by purpose: `gtm_create_folder_tool`

### Phase 5: Conversion actions in Google Ads

- Create one conversion action per key event: `ga_create_conv_action_tool`
- **Avoid duplicate-named actions**: they silently double-count. Run `ga_conv_source_integrity_tool` after setup to confirm
- Configure attribution: data-driven default
- Enable enhanced conversions: pass through hashed email/phone via the conversion tag
- Set inclusion in "Conversions" column thoughtfully, only primary events, not every micro-event

### Phase 6: Enhanced conversions for web

- Verify enhanced conversions configured: `ga_enhanced_conv_status_tool`
- Should see match rate ≥ 60% within 2-3 weeks; below that means PII isn't being passed correctly

### Phase 7: Server-side (when justified)

- For accounts with CPL > $30 or any iOS-heavy traffic, set up sGTM
- Create sGTM destinations: `gtm_create_sgtm_dest_tool`
- Build sGTM client + transformation: `gtm_create_sgtm_client_tool`, `gtm_create_sgtm_xform_tool`
- Forward GA4 + Ads + Meta server-side
- Use Conversions API for Meta (`meta_send_capi_event_tool`) and offline conversions for Ads (`ga_upload_click_convs_tool`)

### Phase 8: Verification (mandatory)

Before declaring tracking "done":

- Run `ga_conv_tracking_health_tool`
- Trigger each key event manually and confirm via `ga4_realtime_tool`
- Confirm Google Ads is receiving conversions (status = "Recording conversions")
- Confirm GA4 ↔ Ads link is healthy
- Run `gtm_audit_container_tool` for unfired tags / unused triggers

## Common tracking failures to watch for

- **Double-counting:** two conversion actions firing for the same event. Audit with `ga_conv_source_integrity_tool`
- **Cross-domain failures:** GA4 not configured for cross-domain → user shows as new visitor on payment processor domain
- **Consent mode misconfig:** all traffic showing as denied, no conversion modeling
- **Form submit firing on page load:** the trigger fires before form is actually submitted
- **Phone call click on iOS not firing:** iOS Safari handles `tel:` links differently, verify the click trigger
- **PMax over-attribution:** PMax taking credit for branded search; check via `ga4_attr_model_compare_tool`
