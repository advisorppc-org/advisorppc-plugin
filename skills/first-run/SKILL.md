---
name: first-run
description: This skill should be used when the user has just installed the AdvisorPPC plugin or connector and wants to start, or says "get started", "get me started", "I just installed AdvisorPPC", "I just added AdvisorPPC", "what can you do with my ads", "is AdvisorPPC working", "try AdvisorPPC", or is in their first session with the AdvisorPPC connector. It connects the user in the app they are using and proves the connection with one real result from their own account.
version: 0.1.0
---

# First Run

Take a new user from "just installed" to one real result from their own account, in this conversation. Reference detail (plans, headless login, troubleshooting) lives in the `getting-connected` skill; this skill is the walk-through.

**Act at once.** When this skill loads, start at step 1. Do not summarize these steps, list options or ask what the user would like to do first. Stop only where a step needs the user.

## 1. Check whether the connector already answers

If AdvisorPPC tools are present in this session (for example `ga_accessible_customers_tool`), go straight to step 3. If they are absent, or the first call fails because the user is not signed in, go to step 2.

## 2. Give the connect step for the app the user is in

Work out the app from what you can observe, never from a guess:

- **Claude Code**: you can run terminal commands, or the conversation shows Claude Code commands such as `/mcp` or `/plugin`.
- **Claude app** (desktop, web or Cowork): you have no terminal. Give no commands, file paths or config edits.
- **Cannot tell**: ask one plain question: "Are you using Claude Code, or the Claude app?"

When the user says which app they are in, go by their words.

Then give the one next action for that app, in plain words:

- **Claude Code**: "Type `/mcp`, pick the AdvisorPPC server and sign in. Your browser opens."
- **Claude app**: "Open your connectors list in the Claude app, find AdvisorPPC and press Connect. A sign-in window opens."

If the user cannot find that, ask what they see on screen; never guess menu names.

For both, add: sign in with the Google account that can already see the ad, Analytics or Search Console accounts, and approve. Then link those accounts in the dashboard at https://mcp.advisorppc.com/dashboard; linking is separate from the sign-in. Ask the user to say when they are done, then run step 3.

For a machine with no browser, follow "Headless or remote machine" in `getting-connected`.

## 3. Prove it with one real read call

Call `ga_accessible_customers_tool` (no inputs). Say plainly that the connection works only after this call returns.

- **Accounts returned**: go to step 4.
- **Empty list**: the user has no Google Ads account under this sign-in. Do not stall: follow the `no-ads-account` skill, which starts from Search Console or Google Analytics 4.
- **Sign-in error**: go back to step 2 for the user's app.
- **Refused for plan reasons**: quote the reason as the tool gave it, then follow "Plans" in `getting-connected`.

## 4. Show one useful first result

1. Pick the account. With one account, use it. With several, list them by name and ID and ask which one. For a manager account, list its clients with `ga_list_customer_clients_tool` (`manager_id`) and ask which one.
2. Call `ga_account_performance_tool` with that `customer_id` for the last 30 days.
3. Reply in at most six lines: the account name, cost, clicks, conversions and cost per conversion for the last 30 days, in the account's own currency. Add one plain observation only when the numbers show it, for example spend with no conversions. If the account had no spend in the period, say so and offer the `no-ads-account` report instead.
4. Close with up to three next things the user can ask for, in their words: "audit my Google Ads account", "find wasted spend", "build my PPC dashboard".

## Gotchas

- Never ask for, accept or repeat a password, API key, developer token, refresh token, client secret or one-time code. Sign-in happens only in the browser. If the user offers one, say it is not needed and give the connect step. If they already pasted it, do not use or repeat it, and suggest they change it because it was shared in a chat.
- Plan facts come only from `plan_tool` with action `"status"`. Never state a plan name, price, trial or allowance that a tool result did not give.
- First run only reads. Never call a change tool during first run.
- This skill fires when the user asks; it cannot see an install happen and creates no reminder or schedule. Never say it will check back later.
- Never claim the connection works, or quote a number, before a tool result shows it.
