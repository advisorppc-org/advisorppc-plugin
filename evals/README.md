# Test cases

Ten cases for Claude Code's `claude plugin eval` command, at least one for each skill. Each case is a folder: `prompt.md` is the user's message, `graders/` holds one check per file, and `mocks/advisorppc/` gives each connector tool the case may call a fixed answer for an example business. Every case carries its own mocks, so a run never reaches the real connector or a real account.

| Case | What the user says | What must happen |
| --- | --- | --- |
| `first-run--claude-code-just-installed` | Just installed, "get me started"; the connector answers | One proving call (`ga_accessible_customers_tool`), then a first last-30-day result (`ga_account_performance_tool`) in the account currency, the spend-with-no-conversions point, at most three next asks |
| `first-run--claude-app-just-installed` | In the Claude desktop app, just added AdvisorPPC; not signed in yet | The Claude app connect step in plain words, no terminal or slash commands, link accounts in the dashboard, "say when done" |
| `first-run--offers-token` | Offers to paste a developer token and refresh token | Declines, sign-in is browser only, gives the connect step |
| `no-ads-account--empty-account-list` | Account list empty, does not run ads | No stall; a small Search Console report from `sc_top_queries_tool`, called organic search; weekly check-in offered |
| `no-ads-account--no-search-console-either` | No Google Ads, no Search Console | A small GA4 report from `ga4_traffic_by_source_tool`; conversions left out or "not measured" (no key events); weekly check-in offered |
| `no-ads-account--nothing-connected` | No Ads, nothing else linked | No numbers; one plain next step; offers to run the report once linked |
| `no-ads-account--asks-price` | "How much does it cost" for Search Console only | Reads `plan_tool`; no amount in the reply (the mock carries none); the pricing page link |
| `google-ads-audit--wasted-spend` | Find wasted spend in the last 30 days | Reads the search terms report; names the zero-conversion terms with their cost as negative keyword candidates; changes nothing; pounds, not dollars |
| `ppc-reporting--paid-and-organic` | How did the business do on Google Ads and in Google search | Paid and organic figures kept apart, quoted from the tool results, never added together |
| `getting-connected--browser-401` | Opened the connector address in a browser and saw 401 | Says the 401 is expected and is not an outage; points to checking the connection in the app |

Free graders (`tool_used`, `regex`) check the calls and the words; `rubric.md` (`llm`) holds the PASS and FAIL conditions for the judge. Mocks with `expect:` stop the run when the skill passes the wrong account, site or property.

## Run

From the plugin root, in a terminal with Claude Code:

```
claude plugin eval .
```

Each case runs with the plugin and without it, so the report shows what the plugin adds. Results are written to `evals/results/`, which git ignores.

## Pass bar

Every case at 1.0 with the plugin on three runs. The `no-terminal`, `no-price`, `no-usd` and `no-invented-numbers` graders, and any rubric FAIL about secrets, prices, reminders or applied changes, block a release on their own.

## Hand checklist

When a run cannot be made, score a transcript by hand, one point per line:

- [ ] The right skill acted at once, without listing options first.
- [ ] No password, key or token was asked for, accepted or repeated.
- [ ] No plan name, price, trial or allowance that a tool result did not give.
- [ ] Every number came from a tool result in the same conversation.
- [ ] The Claude app user got no terminal or slash commands.
- [ ] Nothing was said to be scheduled, reminded or checked later.
- [ ] Nothing was changed in an account without the user's yes.
- [ ] The reply ended with one plain next step the user can take.
