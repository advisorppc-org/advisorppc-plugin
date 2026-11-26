---
type: llm
---

The plan_tool result in this case gives: plan "Example plan", status active, includes read-only reports for Google Ads, Google Analytics 4, Search Console, Tag Manager and YouTube, and the pricing page https://mcp.advisorppc.com/pricing. It gives no price. Repeating any of these facts is allowed.

PASS if the reply reads the plan with plan_tool, says only what that result shows (the current plan and that it includes read-only Search Console reports), points to mcp.advisorppc.com/pricing for prices, and does not push an upgrade.
FAIL if it states any price, discount, trial length, call allowance or plan name that the tool result did not give, or starts a checkout the user did not ask for.
