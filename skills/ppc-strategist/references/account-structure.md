# Account Structure Decisions

> Tool names here are AdvisorPPC operations. Call the ones in your connector's tool list directly. Run any other through `advisor_search_tools`, then `advisor_tool_help`, then `advisor_read` (reads) or `advisor_write` (changes); search by keyword if a name is not found, and treat a missing operation as not on the user's plan, never as a reason to improvise.

Account structure is upstream of everything else. A poorly structured account makes optimization impossible no matter how skilled the operator.

## The structuring principle

Group by **how you want to manage budget and message**, not by some theoretical taxonomy.

If two ad groups need different budgets, different bidding, different audiences, or different ad copy, they belong in different campaigns.
If two ad groups share all of those, they probably belong in the same campaign.

## Modern (2026) campaign structure for most local service businesses

A solid baseline structure for, e.g., a multi-location escape room:

```
Search:
  - Brand (own brand, defensive)
  - Brand-Adjacent (competitor names, if policy allows)
  - Generic - [Geo 1] (e.g., "Austin Core")
  - Generic - [Geo 2] (e.g., "Mississauga")
  - Themed Searches (e.g., horror rooms, family rooms, only if volume justifies)

Performance Max:
  - PMax - All Locations (with brand exclusions, audience signals, geo targeting)

Demand Gen / YouTube:
  - Awareness - Cold (lookalikes, in-market: entertainment)
  - Retargeting (visited site, didn't book)
```

Why this works:
- **Brand campaign** lets you defend cheaply and report on it cleanly
- **Generic by geo** lets you set budget per market based on demand
- **PMax** scales conversions across surfaces with proper guardrails
- **Demand Gen** funnel-feeds from cold → retargeting

## When to split a campaign

Split if any of these apply:
- The two intents need different budgets
- They need different bidding strategies
- They need different ad copy / value props
- They serve different geographies with different economics
- One is brand and the other is generic (always split, never let generic eat brand budget)

## When NOT to split

- Just because it would feel "cleaner"
- For SKAGs (single-keyword ad groups): outdated in 2026, smart bidding doesn't need them
- To create more reporting granularity: use labels (`ga_create_label_tool`) instead

## Naming conventions

Consistent naming saves hours of confusion across many accounts. A workable pattern:

```
[Channel] - [Campaign Type] - [Geo or Theme] - [Audience or Funnel Stage]
```

Examples:
- `Search - Brand - Austin - All`
- `Search - Generic - Austin - High Intent`
- `PMax - All Locations - Lookalikes`
- `DemandGen - Awareness - Lookalike Top Customers`

Use `naming_convention_tool` to validate or rename existing campaigns.

## SKAGs are dead. So is exact-match-only.

In 2026:
- Smart bidding works best with broader keyword themes, let it learn across variations
- Exact-match alone misses huge volume because Google's close-variant matching is more aggressive
- Use a mix: some exact (for control on top performers), mostly phrase, some broad (with strong negatives)
- Group by **theme**, not by **keyword variant**

## Auditing existing structure

To assess whether a structure is sane:

1. List all campaigns: `ga_list_campaigns_tool`
2. Check budget allocation vs. business priority, does the highest-priority campaign have the most budget?
3. Check for budget-starved campaigns (budget exhausted before noon): `ga_alert_budget_overrun_tool`
4. Check for under-pacing campaigns: `ga_budget_rebalance_tool`
5. Check for campaigns with overlapping themes (potential cannibalization)
6. Check brand vs. generic separation
7. Check PMax + Search overlap: does PMax have brand exclusions?

## When to restructure

Restructuring is expensive (loses learning data, requires re-warmup). Only do it when:
- Current structure makes optimization impossible
- A major business change happened (new locations, new product lines)
- Budget has grown 3x+ and the old structure can't absorb it

For minor issues, fix in place. Restructure as a last resort, and only with the client's explicit buy-in.

## Brief generator

Use `ga_acct_structure_brief_tool` to generate a starting structure for a new business, then refine based on the marketer's understanding of the business model.
