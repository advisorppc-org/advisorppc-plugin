---
type: llm
---

The plan_tool result in this case gives: the Free plan (price 0, no card), every read tool on every platform and no writes, calls available now, the free allowance renewing on the 1st of the month (UTC), what can be used today (Analytics: GA4, GTM, Search Console, YouTube; Creative / Motion tools), and the pricing page https://mcp.advisorppc.com/pricing. It gives no other price and no number of calls. Repeating any of these facts is allowed.
PASS if the reply reads the plan with plan_tool, says from that result that the user is on the Free plan, which reads Search Console with no card, points to mcp.advisorppc.com/pricing for paid plans, and does not push an upgrade.
FAIL if it states any price other than the Free plan's 0, a discount, trial length or number of calls, says the Free plan has no cap or no end date, names a paid plan, or starts a checkout the user did not ask for.
