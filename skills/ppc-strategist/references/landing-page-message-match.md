# Landing Page ↔ Ad Message Match

> Tool names here are AdvisorPPC operations. Call the ones in your connector's tool list directly. Run any other through `advisor_search_tools`, then `advisor_tool_help`, then `advisor_read` (reads) or `advisor_write` (changes); search by keyword if a name is not found, and treat a missing operation as not on the user's plan, never as a reason to improvise.

The single biggest lever between "ad got clicked" and "user converted." Most accounts have an ad-quality problem that's actually a landing-page problem.

## The match check

For every important ad in the account, ask:

1. **Does the headline of the landing page match the headline of the ad?** (or at least echo the same promise)
2. **Is the primary CTA on the page the same as the ad's CTA?** ("Book Now" ad → "Book Now" button above the fold)
3. **Is the offer stated in the ad visible without scrolling?** (if the ad says "20% off this week", that 20% must be on the page)
4. **Is the page focused, or does it have 14 other distractions?** (footer links, blog teasers, newsletter popups stealing attention)
5. **Does it load in < 2.5 seconds on mobile?**
6. **Is the conversion path (booking, form, call) one click away?**

If any answer is "no", the ad's CVR is being throttled by the page.

## Common message-match failures

| Ad says | Page says | Result |
|---|---|---|
| "Austin's #1 Escape Room" | "Welcome to [Brand]" | Disconnect, user wonders if they clicked the right link |
| "20% off this weekend" | No mention of 20% | Trust loss, user thinks it was a bait-and-switch |
| "Book a Horror Room" | Generic homepage with all room types | User has to find horror rooms themselves, most won't |
| "Free Cancellation" | Cancellation policy buried in footer | User doesn't trust the claim |

## Diagnostic workflow

When CVR is low for a specific campaign or ad group:

1. Pull the top ads and their final URLs (`ga_list_ads_tool`)
2. Click through each one. Read the ad, then read the page header. Do they match?
3. Use `ga_score_landing_brief_tool` to generate a quality score brief
4. Check page load time (PageSpeed Insights via web)
5. Check for booking/form completion in GA4 to confirm tracking is healthy on the LP

## Fixes the marketer recommends (and the strategist requests from the client)

- **Build a campaign-specific landing page** for high-spend campaigns instead of pointing all ads to the homepage
- **Match the page's headline to the ad's headline word-for-word** for the top ad in each ad group
- **Move the CTA above the fold** with no friction
- **Remove unrelated content** from the LP: every link out is a conversion lost
- **Dedicated geo-specific landing pages** for multi-location businesses (Austin traffic → Austin LP, not generic)

## Specific to escape rooms / experience businesses

- **Show the rooms.** Photos of the actual rooms convert way better than stock imagery.
- **Show the booking calendar above the fold** if the booking flow allows.
- **Real reviews with name + photo** beat aggregated star ratings.
- **Group / corporate booking** should be a separate landing page if you're advertising for it, different buyer, different objections.
- **Mobile-first**: most escape room searches and bookings happen on mobile.

## When you can't change the LP

Sometimes the client can't or won't change the landing page. Then:
- Adjust ad copy to match what the page actually delivers (don't promise things the page doesn't show)
- Use ad extensions to fill gaps (sitelinks for "Book Now", "View Rooms", "Group Bookings" can take users where they actually want to go)
- Lower expectations on CVR, communicate that to the client honestly
- Document the constraint in the client's worklog (`client_log_entry_tool`)

## The marketer's test

Before launching an ad, do a 5-second test on the landing page:
1. Click the ad
2. Spend 5 seconds on the page
3. Ask yourself: "Do I know what to do, and do I want to do it?"

If the answer is no, the ad will have a low CVR. Fix the page or rewrite the ad.
