# Evals

Eight cases for `claude plugin eval`, in the `evals/<skill>--<case>/` layout: `prompt.md` is the user prompt, `graders/` holds one check per file.

- `skill-fired.md` (`tool_used: Skill`): the right skill fired on natural phrasing ("junk searches", "CPA spiked", "client report", "connect my Google Ads"). In a two-arm run it is a plugin-fired indicator, not part of the score.
- `regex` and `tool_used` graders: free checks on the reply and on the tool calls (account currency, no write tool called during an audit, the right report tool used).
- `rubric.md` (`llm`): concrete PASS and FAIL conditions for the judge model.
- `no-skill--unrelated`: a should-not-fire case (`min: 0`, `max: 0`, `arm: both`).

`mocks/advisorppc/<tool>.md` answers each read tool with a fixed result for an example account in EUR, so no run touches the real connector or a real ad account. The wasted-spend case also mocks `ga_add_negative_keyword_tool` so that a wrongful write would be seen and fail the case.

## Who runs them, and when

A maintainer runs them on a Claude seat before a release. They do not run in CI: every run is real model usage. CI runs only the free `claude plugin validate --strict --profile directory .` gate (`.github/workflows/validate.yml`).

```
claude plugin eval . --trust-plugin --judge-model sonnet --runs 3
```

Use `--case 'google-ads-audit--*'` to run one skill's cases. Results land in `evals/results/` (git-ignored).

## Pass bar

Every case at 1.0 with the plugin, and a positive with-without delta for each skill. A failed `no-write` grader blocks the release.
