# Bidding Strategy Fit by Account Stage

> Tool names here are AdvisorPPC operations. Call the ones in your connector's tool list directly. Run any other through `advisor_search_tools`, then `advisor_tool_help`, then `advisor_read` (reads) or `advisor_write` (changes); search by keyword if a name is not found, and treat a missing operation as not on the user's plan, never as a reason to improvise.

Bidding strategy is one of the most over-changed and under-understood settings. Choose based on **account maturity** and **conversion volume**, not on what's trendy.

## The decision tree

### Stage 1: New account / new campaign / < 15 conversions/month

- **Use:** Maximize Conversions (no tCPA), or Manual CPC if you want tight control
- **Avoid:** tCPA, tROAS: they need data to learn, you don't have any yet
- **Why:** Smart bidding without data = Google guessing. Build conversion volume first.
- **Tools:** `ga_create_max_conv_strat_tool`

### Stage 2: Building data / 15-50 conversions/month

- **Use:** Maximize Conversions with target CPA (loose target), or stay on Max Conversions
- **Why:** Enough data for direction, not enough for tight constraints
- **Watch:** CPA volatility: if CPA swings wildly, the algo doesn't have enough signal yet
- **Tools:** `ga_create_tcpa_strategy_tool` (set tCPA ~20% above current avg CPA)

### Stage 3: Mature / 50+ conversions/month, stable CPA

- **Use:** tCPA or tROAS depending on goal
- **tCPA when:** Lead gen, fixed CPL goal, conversion value not meaningful
- **tROAS when:** Ecommerce, services with clear revenue per conversion, value-based bidding properly set up
- **Tools:** `ga_create_troas_strategy_tool`

### Stage 4: Scale phase / 100+ conversions/month, want more volume

- **Use:** Maximize Conversion Value with tROAS (slightly lower than current actual)
- **Why:** Tells Google "find me more, just stay above this floor"
- **Watch:** Don't lower tROAS too aggressively, it's a constraint, not a target

## When to NOT change bidding strategy

- **Within 2 weeks of last change:** algorithm is still in learning phase. Wait it out.
- **During a tracking change:** never change bidding while tracking is being modified. Bidding will misread signals.
- **During seasonal swings:** changing strategy mid-Black-Friday is asking for chaos. Use seasonality adjustments instead.
- **Just because last week was bad:** one week is noise.

## Bidding & PMax

PMax has its own bidding nuances:
- Always provide audience signals (`ga_add_audience_signal_tool`), not optional in 2026
- Use brand exclusions to keep PMax from cannibalizing branded search (`ga_add_brand_excl_camp_tool`)
- For new PMax: start with Max Conversions, transition to tROAS once value data is reliable
- Don't run PMax + Search on identical themes without a plan, they will compete

## Diagnosing bidding problems

Symptoms → likely cause:

| Symptom | Likely cause |
|---|---|
| CPA spike with no other change | Tracking change, seasonal shift, or competitor entry |
| Volume drop after going to tCPA | tCPA set too low, algorithm constrained |
| ROAS dropped after tROAS change | Target was unrealistic, or value tracking is off |
| Spend dropped to near zero | Bid strategy can't hit target, loosen it or check tracking |
| Wild CPA day-to-day | Not enough data for smart bidding, go to Max Conversions |

Use `ga_alert_cpa_spike_tool` and `ga_alert_cvr_drop_tool` for ongoing monitoring.

## The marketer's check

Before changing bidding strategy, ask: **"Is the strategy actually the problem, or is something upstream broken?"**

Often, "bad bidding performance" is really:
- Broken conversion tracking (Rule 2 of the main skill)
- A landing page change that hurt CVR
- A new competitor undercutting bids
- A match-type expansion that pulled in junk

Diagnose the upstream cause first. Don't change bidding to mask a different problem.
