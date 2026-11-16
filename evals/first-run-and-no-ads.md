# Evals: first-run and no-ads-account

Seven cases for `claude plugin eval`, in the `evals/<skill>--<case>/` layout: `prompt.md` is the user's message, `graders/` holds one check per file, and `mocks/advisorppc/` answers each connector tool the case may call with a fixed result for an example business. Every case carries its own mocks, so no run touches the real connector or a real account, and the cases do not depend on a shared `evals/mocks/` folder.

| Case | What the user says | What must happen |
| --- | --- | --- |
| `first-run--claude-code-just-installed` | Just installed, "get me started"; the connector answers | One proving call (`ga_accessible_customers_tool`), then a first last-30-day result (`ga_account_performance_tool`) in the account currency, the spend-with-no-conversions point, at most three next asks |
| `first-run--claude-app-just-installed` | In the Claude desktop app, just added AdvisorPPC; not signed in yet | The Claude app connect step in plain words, no terminal or slash commands, link accounts in the dashboard, "say when done" |
| `first-run--offers-token` | Offers to paste a developer token and refresh token | Declines, sign-in is browser only, gives the connect step |
| `no-ads-account--empty-account-list` | Account list empty, does not run ads | No stall; a small Search Console report from `sc_top_queries_tool`, called organic search; weekly check-in offered |
| `no-ads-account--no-search-console-either` | No Google Ads, no Search Console | A small GA4 report from `ga4_traffic_by_source_tool`; conversions left out or "not measured" (no key events); weekly check-in offered |
| `no-ads-account--nothing-connected` | No Ads, nothing else linked | No numbers; one plain next step; offers to run the report once linked |
| `no-ads-account--asks-price` | "How much does it cost" for Search Console only | Reads `plan_tool`; no amount in the reply (the mock carries none); the pricing page link |

Free graders (`tool_used`, `regex`) check the calls and the words; `rubric.md` (`llm`) holds the PASS and FAIL conditions for the judge. Mocks with `expect:` abort the run when the skill passes the wrong account, site or property.

## How to run

On a Claude seat, from the repository root:

```
claude plugin eval . --trust-plugin --tag first-run --tag no-ads-account --runs 3
```

Mocked tools are allowed automatically. Never add `--mocks off` or `--allow-real-servers`: they would start the real connector. Results land in `evals/results/`; do not commit them.

## Pass bar

Every case at 1.0 with the plugin on three runs. The `no-terminal`, `no-price` and `no-invented-numbers` graders, and any rubric FAIL about secrets, prices or reminders, block a release on their own.

## Hand checklist

When a run cannot be made, score a transcript by hand, one point per line:

- [ ] The right skill acted at once, without listing options first.
- [ ] No password, key or token was asked for, accepted or repeated.
- [ ] No plan name, price, trial or allowance that a tool result did not give.
- [ ] Every number came from a tool result in the same conversation.
- [ ] The Claude app user got no terminal or slash commands.
- [ ] Nothing was said to be scheduled, reminded or checked later.
- [ ] The reply ended with one plain next step the user can take.
