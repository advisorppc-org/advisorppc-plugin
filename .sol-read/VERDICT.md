PR15 @e68e6948 = FIX-FIRST

1. skills/ppc-reporting/references/dashboard-data.md:128 — medium — The prescribed 10–12rem first-column `width` does not bound a cell in automatic table layout. A valid campaign name such as `Brand_September_2026_Search_Prospecting_United_States_English_Desktop` has no normal wrapping opportunity. Its minimum content width can exceed a 390px viewport despite `width: 11rem` and `white-space: normal`; pinning that oversized cell at `left: 0` can cover the entire visible numeric area while it scrolls underneath. Thus the first column does not reliably wrap inside the promised width, and CHANGELOG.md:9–11 overstates the result for valid labels. Fix: explicitly require breaking long tokens, and bound the label content—for example, an inner block with `width: 11rem; white-space: normal; overflow-wrap: anywhere` inside each sticky first-column cell, with matching column sizing. Verify a long unbroken label at 390px before and after horizontal scrolling. The [CSS automatic-table-layout algorithm](https://www.w3.org/TR/CSS22/tables.html#auto-table-layout) treats cell width as a minimum constraint alongside minimum content width; it is not a maximum.

Recheck of the seven earlier findings:
- Overflow wrapper squeezes: the added table minimum width, nonwrapping headers/numbers and first-column sizing address the ordinary-label case; the unbroken-label case above remains.
- Position 0 versus “new this period”: closed for changes by lines 108–111, which require `–` when either period has no impressions and explicitly replace the generic percentage/new wording.
- Coloured 0.0: closed for rate/rank differences by lines 107–108: round first, then use neutral “no change”.
- CTR percent-of-percent: closed by lines 101–103: both platforms use percentage points from 0–1 values, at one decimal.
- GA4 table missing: closed by lines 122–123, which explicitly include traffic by source.
- Tool change column copied: closed by lines 105–107, which require recomputation from current/previous values and forbid copying tool change columns.
- First column scrolls away: sticky positioning, left offset and solid background are explicit at lines 127–130; the width defect above still prevents reliable phone usability.

Other checks: authenticated GitHub access confirms draft PR #15 has base de509b86dcb642929aeb082953db4a6c36e087a9 and head e68e694868638a0be07a7822420410bba7a8e633, matching this detached checkout. The diff changes only the stated five files. JSON parsing and assertions confirm 0.3.7 in plugin.json and marketplace.json and in the README badge. The CHANGELOG rate/rank claims match the added instructions; its mobile claim has the limitation above. No numeric plan allowance, price or new commercial promise is introduced. `git diff --check` passed; tracked files remain unchanged.

Verification limit: no model-generated dashboard was executed. A local Chromium reproduction could not launch because the sandbox denied a socket operation (`Operation not permitted`); the in-app browser host was also unavailable. The finding rests on the concrete valid input, the prescribed CSS and the CSS specification, not a claimed successful browser measurement. OpenAI engineering guidance consulted: SKILLS-PLUGINS-MCP.md, checked 2026-11-04, limited here to instruction/contract review; this is a Claude Code plugin.

Needs: A working browser for a 390px replay with ordinary and unbroken labels, checking that the pinned label stays within 10–12rem and numbers remain visible during scrolling.
Blocks: The medium label-width correction above. Separately preserve the PR’s existing release gate: publish update 0.3.6 before merging; publication was not verified by this read.
Alhamdulillah
no repeat
