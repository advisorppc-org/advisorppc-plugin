---
name: landing-page-ab-testing
description: Design, size, run, read out and roll out a valid A/B test on a landing page that receives paid traffic. Use before proposing or building any split test, and when the user asks "should we test this", "how long should this test run", "how many visitors do I need", "did the variant win", "is this result real", "test a new headline on my landing page" or "my test results look too good". Includes a stdlib-only calculator for sample size, significance and sample-ratio mismatch.
---

# Landing page A/B testing

A test is a measurement, not a launch tactic. Most bad tests fail on setup (no fixed sample, leaky assignment, wrong metric), not on math. Run the checklist top to bottom.

Related skills: `cro-optimization` finds what to test and ranks it; `ppc-strategist` decides what the ads and budgets should do around the test.

## Ground rules

- By default every variant keeps the same offer: prices, plan names, trial terms and guarantees are identical. Only copy, layout, order, imagery and CTA wording change. Testing an offer is a business decision the user makes explicitly.
- Never invent a discount, coupon or "launch price" for a variant.
- This skill plans and analyzes. Shipping a variant goes through the user's normal release process.

## Step 0: should this be a test at all?

| Situation | Do this instead |
|---|---|
| Broken thing (dead button, error page, a 6 s LCP) | Fix it. Do not test a bug. |
| Required sample needs more than about 8 weeks | Do not test. Ship the best-judgment change, watch the funnel, run qualitative research (5 recorded sessions, sales-call or chat review). |
| Legal or truth fix (unproven "#1", a claim the business cannot back) | Fix it. Never keep a false claim as a "control". |
| Two credible designs, enough traffic, reversible | Test. |

Low-traffic rule: test the step with the most volume that still predicts money (landing view to form start, or form start to lead), not visit to sale.

## Step 1: hypothesis (write it before building)

```
Because we saw <evidence: data point, customer quote, heatmap, session replay>,
we believe that changing <element> for <audience/page> to <variant>
will increase <primary metric> by at least <MDE, relative>,
without hurting <guardrails>.
We will know after <n per arm> exposed visitors per arm (~<weeks> full weeks).
```

Worked example (illustrative counts; use real ones): Because 3 of 12 sales calls this month asked "do you charge a call-out fee", we believe adding "No call-out fee. Fixed quote before we start." under the hero CTA will raise landing-view to quote-request by at least 20% relative, without lowering lead quality (booked-job rate) or raising cost per booked job.

## Step 2: metrics

- **One primary metric** decides. Unit = visitor (stable id), not pageview or session. Good primaries for paid landing pages: landing view to CTA click, CTA click to form submit, form submit to qualified lead.
- **Secondary metrics** explain the result (scroll depth, FAQ opens, call clicks).
- **Guardrails** must not get worse: lead quality or booked-job rate, cost per acquisition, page errors, LCP p75, refund or cancellation rate.
- **Trust checks**: sample-ratio mismatch (Step 6), an A/A sanity run on a new setup, exposure counts per day.

Before trusting conversion counts, make sure the conversion is measured correctly. With the AdvisorPPC connector: `ga_conv_tracking_health_tool` for Google Ads and `ga4_list_key_events_tool` for GA4.

## Step 3: sample size and MDE

MDE = the smallest **relative** lift worth detecting. Pick it from business value, not hope. Halving the MDE roughly quadruples the sample.

Pull the baseline rate and daily eligible traffic from real data (for example `ga4_run_report_tool` on the landing page, or the catalog operation `ga_landing_page_perf_tool`), then run the bundled calculator (Python 3 standard library only):

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/landing-page-ab-testing/scripts/ab_stats.py" size --p 0.04 --mde 0.2 --daily 600
python3 "${CLAUDE_PLUGIN_ROOT}/skills/landing-page-ab-testing/scripts/ab_stats.py" test --na 10400 --xa 416 --nb 10380 --xb 502
python3 "${CLAUDE_PLUGIN_ROOT}/skills/landing-page-ab-testing/scripts/ab_stats.py" srm  --na 10400 --nb 10380
```

Verified outputs, 600 eligible visitors a day, alpha 0.05, power 0.8:

| Baseline | MDE (relative) | Per arm | Run |
|---|---|---|---|
| 4% CTA click | +20% | 10,317 | 5 full weeks |
| 4% CTA click | +30% | 4,783 | 3 full weeks |
| 20% form start to submit | +10% | 6,510 | 4 full weeks |

Two arms only unless traffic is large. Each extra arm adds a full arm of sample and multiple-comparison risk (Bonferroni: alpha divided by the number of comparisons).

## Step 4: assignment (sticky, server-side, never by user agent)

- Stable id: a first-party cookie with a random UUID (90 days, `Secure`, `SameSite=Lax`, `HttpOnly` when only the server reads it). When the visitor converts, store `(lead_id, experiment_id, variant)` once so lead quality and revenue join back to the variant.
- Bucket: `int(sha256(f"{experiment_id}:{uid}").hexdigest()[:8], 16) % 100`, split 50/50. Salt with the experiment id so experiments do not correlate.
- Assign server-side at render. No client-side flicker that swaps the hero after paint.
- **Never pick the variant from the user agent.** Google treats that as cloaking. Bots are bucketed like anyone else and removed at analysis.
- Ads: keep both arms on the same final URL (server-side split), or use Google Ads custom experiments for an ad-level split. A redirect test uses 302 and `rel=canonical` to the original URL, is time-limited, and the losing branch is removed after the decision.
- One experiment per page element at a time. Overlapping tests on one page must be mutually exclusive, or the readout is confounded.

## Step 5: exposure logging and cleaning

Log an exposure when the variant actually renders, not when the cookie is set:

```
experiment_id, variant, uid, lead_id (nullable), ts_utc, path, referrer_host,
utm_source, utm_campaign, gclid_present, device_class, is_bot, is_internal
```

- Analyze exposed units only, deduplicated to the first exposure per uid. Conversions count only after that unit's first exposure.
- Bot filter at analysis: known crawler user agents, headless markers, zero-interaction units with sub-second dwell. Exclude staff IPs and test leads.
- Report the filter counts. A variant that "wins" only after a custom filter is not a win.

## Step 6: run it (no peeking)

- Fix the sample size and end date before launch. Run whole weeks (at least 2) so weekdays and weekends weigh the same in both arms.
- Stopping at the first p below 0.05 inflates false positives far above 5%. If you must look early, choose a sequential method before launch (group sequential with alpha spending, or always-valid p-values) and use its boundaries.
- Allowed early stops: guardrail harm (form broken, errors spiking), sample-ratio mismatch, or a bug. "It is clearly winning" is not one.
- **Check sample ratio daily**: chi-square on exposed counts against the planned split. p below 0.001 means assignment or logging is broken (redirect drops, bot skew, a cached variant). Stop, fix, restart with a new experiment id. Never analyze a mismatched test.
- Caching: pages behind a CDN must vary on the cookie or bypass the cache, or one variant is served to everyone.
- Novelty: split the readout by week and by new versus returning. An effect that fades week over week is novelty; report the last full week too.
- Freeze everything else: no copy edits, offer changes, or ad, bid or budget changes aimed at one arm during the run. Log any unavoidable change with its date. Ask before changing campaign budgets mid-test, because traffic mix shifts can swamp the effect.

## Step 7: readout template

```
Experiment: <id>  Page: <url>  Dates: <start>..<end> (<n> full weeks)
Hypothesis: <one line>
Traffic: exposed A <n> / B <n>; SRM p=<p> (ok | FAIL); bots removed <n>; internal <n>
Primary: <metric>  A <rate>  B <rate>  lift <+x%>  95% CI abs [<lo>, <hi>]  p=<p>
Guardrails: lead quality <A vs B>; CPA <A vs B>; errors <..>; LCP p75 <..>
Segments (descriptive only, not for the decision): mobile/desktop, new/returning, campaign
By week: W1 <lift>, W2 <lift>, ... (novelty?)
Decision: SHIP B | KEEP A | INCONCLUSIVE, keep simpler | RERUN (why)
Follow-up: <next hypothesis>
```

Segments found after the fact are hypotheses for the next test, never the result.

## Step 8: decide and roll out

| Result | Decision |
|---|---|
| Primary up, significant, guardrails flat or better | Ship B to 100%, delete the A branch and the flag |
| Primary up, a guardrail worse | Do not ship. Understand the tradeoff; the user decides when money is involved |
| Inconclusive (CI spans 0) | Keep the simpler or cheaper version; record "no detectable effect at MDE X" |
| Primary down, significant | Keep A; the learning is still worth recording |

- Remove experiment code within one release so it does not rot.
- Keep an experiments ledger (losers too): id, hypothesis, dates, n, result, decision, link to the readout.
- Downstream money metrics (lead-to-sale, refunds) lag the test. Re-read them for the test cohort once the window closes and append them.

## Anti-patterns (reject on sight)

- A test with no written hypothesis or no fixed sample size.
- Changing the offer in a variant without the user's explicit decision.
- A "winner" declared on day 3, or on a segment chosen after looking.
- Counting pageviews or sessions instead of stable visitors.
- A client-side testing script that flashes the control hero before swapping.
- Declaring a win on a metric that was not the pre-registered primary.

## Sources

- Evan Miller, How Not To Run an A/B Test: https://www.evanmiller.org/how-not-to-run-an-ab-test.html
- Kohavi, Tang and Xu, Trustworthy Online Controlled Experiments (Cambridge, 2020): guardrails, A/A, sample-ratio mismatch, novelty.
- Fabijan et al., Diagnosing Sample Ratio Mismatch (KDD 2019): https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/
- Johari et al., Always Valid Inference (KDD 2017): https://arxiv.org/abs/1512.04922
- Google Search Central, website testing and Search: https://developers.google.com/search/docs/crawling-indexing/website-testing
