FIX-FIRST

| File:line | Defect | Concrete failure scenario | Disposition |
| --- | --- | --- | --- |
| skills/first-run/SKILL.md:21 | Terminal availability is treated as evidence of the host app. | Claude Code with shell tools withheld and an unauthenticated connector gets Claude app connector instructions. Terminal access alone also cannot establish Claude Code. | FIX: require explicit host evidence or the user's words; otherwise ask the existing clarification question. |
| evals/no-ads-account--empty-account-list/graders/weekly-check-in.md:3; evals/no-ads-account--no-search-console-either/graders/weekly-check-in.md:3 | Both graders require wording rather than behaviour. | “Ask me each week and I can refresh this report for the previous seven days” fails both regexes despite offering the requested user-initiated report. Reproduced offline. | FIX: grade the offer and absence of autonomous scheduling semantically. |
| evals/no-ads-account--asks-price/mocks/advisorppc/plan_tool.md:1; evals/no-ads-account--asks-price/graders/plan-status.md:3 | Neither mock nor call grader requires `action: status`. | An `upgrade` call receives the same status fixture and satisfies tool-presence grading; a correct-looking final answer can conceal the wrong action. | FIX: enforce `action: status` in the mock and inspect call arguments. Repeats M-017. |
| evals/first-run--claude-code-just-installed/mocks/advisorppc/ga_account_performance_tool.md:2 | Reporting periods are not guarded; Search Console and GA4 mocks have the same gap. | Passing `LAST_7_DAYS` with the correct customer still returns the 30-day fixture, allowing a wrong-period request to look correct. | FIX: assert `date_range`, `days` and the requested row limit where applicable. |
| CHANGELOG.md:9 | “Just after install, it acts” implies installation-triggered execution. | Installing silently produces no conversation or result; first-run explicitly says it cannot observe installation. | FIX: say “when the user asks after installing.” Other added changelog descriptions match the diff as intended workflows. |

Verified at `9e429fd4385620a0a17cfe7cc006bcbcf2eed835`: all 63 changed files read; seven case layouts, 26 graders and 22 mocks parse and referenced files exist; diff whitespace check passes. Version 0.3.8 agrees across both manifests, README and CHANGELOG. All 12 tool names occur in origin/main skills; the only newly mentioned parameter name is `site_url`. No new hardcoded plan terms, requests for chat secrets, automatic ad-account writes/spend, private paths, internal machine names or apparent private account identifiers found; fixture identifiers are presented as examples.

Not checked: live tool schemas, authentication/UI flows, model baseline or candidate execution; no network used.
Needs: corroborate `site_url` against the tool schema; baseline/candidate evidence on a Claude seat. The stated pass bar is every case at 1.0 across three plugin-on runs, with specified safety failures independently blocking release.
Blocks: the five FIX rows; model behaviour remains unverified.

Alhamdulillah for the verified offline checks.
repeat of M-017
