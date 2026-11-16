PR15 @bbeb8dbb = MERGE

Findings: none. No new actionable failure in the r1-to-r2 diff.

Closed r1 finding: skills/ppc-reporting/references/dashboard-data.md:127-132, formerly medium. The sticky cell now contains an explicit 11rem block with normal whitespace and overflow-wrap:anywhere. Long unbroken labels can wrap inside that block instead of forcing the sticky column beyond the phone viewport. This implements the requested fix. The [CSS Text specification](https://www.w3.org/TR/css-text-3/#overflow-wrap-property) defines arbitrary breaks for otherwise unbreakable sequences and includes those opportunities in minimum-content sizing.

Replay fidelity: .sol-read/page.html:3-11 implements the prescribed overflow container, table minimum width, nonwrapping headers/numbers, sticky first-column cells with an opaque background, and the exact inner-block declarations. Its padding, collapsed borders and alignment are ordinary presentation choices; no hidden max-width, clipping or fixed-layout workaround supplies the fix. Both header and row labels use the block. The long label is actually 69 characters, with no whitespace, which still exercises the reported failure.

Evidence limits: .sol-read/RESULT.json is the author's Chromium measurement, inspected here but not independently rerun. At viewport 390 and rem 16 it records 192px first-column cells (176px content plus 16px padding), 764px scroll width versus 374px client width, first-column left 8px after full scroll, and final numeric right edge 382px. Numeric cell heights reflect whole-row height, so they alone do not prove single-line text; page.html:5 explicitly supplies nowrap. This is a focused table fixture, not a full generated dashboard or a cross-browser test.

Earlier findings remain closed in skills/ppc-reporting/references/dashboard-data.md:
- :122-129, overflow wrapper squeezes: table min-width, nonwrapping figures and bounded wrapping label content are explicit.
- :108-111, position zero versus "new this period": either period without impressions yields a dash for the difference, overriding generic percentage/new wording.
- :107-108, coloured 0.0: a difference rounding to zero is neutral "no change".
- :101-103, CTR percent-of-percent: both platforms use percentage-point differences from 0-to-1 rates.
- :122-123, GA4 table missing: traffic by source is explicitly included among all data tables.
- :105-107, copied tool change column: recompute from current/previous values; copying is forbidden.
- :127-132, first column scrolls away: sticky positioning, left zero and solid background remain, with the long-label defect now addressed.

CHANGELOG.md:9-14 still matches the rules: scrolling figures with visible labels, CTR changes in points, position changes in positions, on-page computation and neutral rounded-zero changes. Version 0.3.7 remains consistent in both manifests and the README badge. The revision adds no numeric allowance, plan-limit or price promise.

Verification: read the complete dashboard reference, exact e68e6948-to-bbeb8dbb diff, prior verdict, fixture and measurement; git diff --check exited 0. Authenticated GitHub access confirmed advisorppc-org/advisorppc-plugin PR #15 has head bbeb8dbbf8de9d6859e36b6a5897fd09dc4ea603, matching this detached checkout. No tracked file edited, push or post performed.

Needs: none for this bounded revision review; browser replay and plugin validation were not rerun.
Blocks: no review defect. Preserve the PR's existing release gate: publish the 0.3.6 update in the developer portal before merging #15; completion of that gate was not verified here. MERGE is a review verdict, not release authorization.
Alhamdulillah
