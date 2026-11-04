---
name: google-ads-audit
description: This skill should be used when the user asks to "audit my Google Ads account", "review my campaigns", "find wasted spend", "check my search terms", "why did my CPA go up", "what changed in my account", "audit page", "show me the audit", or requests any account or campaign health check using the AdvisorPPC connector.
version: 0.2.0
---

# Google Ads Account Audit

Run a structured audit of a real Google Ads account using the AdvisorPPC connector's read-only Google Ads tools. The audit itself is read-only; the optional Audit page step can apply approved rows with write tools on paid plans, only after a read-back and a plain yes.

## Audit workflow

Follow the steps in order. Skip a step only when the user already supplied the answer (for example, a known customer ID).

### 1. Discover the account

- Call `ga_accessible_customers_tool` (no inputs). It returns an MCC-aware account tree with account IDs, names, and manager flags.
- If the target is under a manager (MCC) account, call `ga_list_customer_clients_tool` with `manager_id` to enumerate client accounts up to three levels deep.
- Confirm the target `customer_id` with the user when more than one plausible account exists. Customer IDs are ten digits; pass them without dashes.

### 2. Establish the baseline

- Call `ga_account_performance_tool` with `customer_id` and `date_range` (for example `LAST_30_DAYS`). It returns impressions, clicks, CTR, cost, average CPC, conversions, conversion value, and cost per conversion in the account's own currency.
- Pull the same range for a prior period when the user asks "what changed" — compare the two summaries side by side.

### 3. Scan campaigns

- Call `ga_list_campaigns_tool` to map campaign IDs, statuses, channel types, bidding strategies, and daily budgets.
- Call `ga_campaign_performance_tool` for cost-sorted campaign rows. Flag campaigns with high cost and zero conversions, and campaigns whose CPA is far above the account average.

### 4. Go deep where the money is

- `ga_keyword_performance_tool` — cost-sorted keyword rows; set `min_impressions` to cut noise.
- `ga_search_terms_report_tool` — the actual queries that triggered ads. This is the primary wasted-spend detector: look for irrelevant queries with cost and no conversions, and propose them as negative keyword candidates; see Audit page for applying them.
- `ga_list_ad_groups_tool`, `ga_list_ads_tool`, `ga_list_keywords_tool` — structural checks: single-keyword ad groups, paused ads left in enabled ad groups, keyword/ad mismatch.

### 5. Check Google's own signals and recent changes

- `ga_list_recommendations_tool` — active recommendations with estimated impact. Report them; recommend acting only on ones consistent with the user's goals.
- `ga_list_change_events_tool` (accepts `days`, `limit`) — who changed what recently. Correlate performance shifts with change timestamps before blaming the market.

## Reporting the findings

Summarize as: baseline numbers → top findings ranked by monthly cost impact → concrete next actions. Quote real figures from the tool results; never estimate a number a tool already returned.

## Audit page

When the user wants the audit as a page (to share, to review, or whenever the result has more than a handful of actions), use the bundled page instead of the markdown:

1. Call `ga_audit_account_tool` once (`customer_id`, `days`, `login_customer_id` for MCC). If it returns an error object, report it and stop. Otherwise write the result to `advisorppc-reports/AUDIT.json` unchanged; the page reads `findings`, `proposed_actions`, `confidence`, `category_breakdown`, `partial_failures`, `truncated` and `error`. Optionally add `meta` with `account`, `generated_at`, `plan`.
2. Run `python3 "${CLAUDE_PLUGIN_ROOT}/skills/ppc-reporting/scripts/fill-dashboard.py" advisorppc-reports/AUDIT.json advisorppc-reports/ppc-audit.html --template "${CLAUDE_PLUGIN_ROOT}/skills/google-ads-audit/assets/audit.html"` (add `--artifact` for the Artifact tool). Do not read the template. The script sorts `proposed_actions` by severity and writes that order back to `AUDIT.json`, so the page's numbers are the file's numbers.
3. Publish or open the page. It is a review page; nothing on it applies anything.

Applying rows happens only when the user names numbers, under the rules in `/advisorppc:audit`: read each row back with keyword text, campaign and ad group; ad-group-scoped rows (`params.ad_group_id`) go through the connector's `advisor_write` door to `ga_add_ad_group_neg_kw_tool` or to `ga_pause_keyword_tool`, never to a campaign-level tool; a plain yes after the list and after each preview; a missing write tool or a plan denial ends the run with a paste-ready list, never a retry.

## Gotchas

- All monetary values are in the account's own currency — never assume USD.
- The free tier allows 100 tool calls per month. Prefer rollup reports (`ga_account_performance_tool`, `ga_campaign_performance_tool`) over per-entity listing loops, and pass `limit` parameters to bound result sizes.
- For accounts reached through an MCC, pass `login_customer_id` when a tool accepts it and direct access fails.
