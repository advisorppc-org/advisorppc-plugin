FIX-FIRST
FAIL no-user-fees - cursor/README.md:37 Only installation is declared free; server capabilities depend on pricing plans (also :33). Establish fee-free Marketplace access/use against publisher terms 3.1 (.git/terms.md:47); plan gating leaves compliance unresolved.
FAIL local-install evidence - .git/cursor_package_lint.py:142 Lint explicitly excludes local installation testing; no Cursor installation/discovery receipt was supplied or found. Provide a local package-load test confirming cursor/ isolation; the accepted endpoint 404 is not this finding.
PASS reviewed head - cursor/.cursor-plugin/plugin.json:1 Reviewed fc416f6640f33865786c5f730b6c4997a3fde537 on submission-team/cursor-20261108; checkout was clean and matched its cached tracking branch. Remote state was not refreshed offline.
PASS marketplace schema - .cursor-plugin/marketplace.json:2 Valid JSON; name, owner.name, and plugins entry name/source/description are present.
PASS discovery isolation - .cursor-plugin/marketplace.json:12 String source is cursor; manifest and component discovery stay there under the supplied parser rules, excluding root Claude components.
PASS Claude unchanged - .claude-plugin/plugin.json:1 git diff origin/main...HEAD contains no changes under .claude-plugin/, .mcp.json, or skills/; only the five requested files were added.
PASS manifest and name - cursor/.cursor-plugin/plugin.json:2 advisorppc is valid lowercase kebab-case, matches the entry, and is unique within this marketplace; author.name is present. Global Marketplace uniqueness was not checked offline.
PASS description - cursor/.cursor-plugin/plugin.json:4 Clearly describes authorized advertising/analytics account access and browser sign-in.
PASS component paths - cursor/.cursor-plugin/plugin.json:12 mcp.json and assets/logo.svg resolve inside cursor/; neither paths nor marketplace source contain absolute paths or parent traversal.
PASS MCP configuration - cursor/mcp.json:2 Valid mcpServers object with one HTTPS remote server; no local executable or undeclared ${VAR} references.
PASS public endpoint selection - cursor/mcp.json:4 Uses /connector, never the private /mcp operator surface; today's /connector 404 is accepted per the brief, with deployment still required before submission.
PASS committed logo and colors - cursor/assets/logo.svg:3 Tracked at the reviewed commit, valid SVG, relative manifest reference; only #1F1E1D and #F5F4EF fills, with neither forbidden color.
PASS usage and configuration - cursor/README.md:7 Documents Marketplace connection, OAuth, manual MCP configuration, and example read requests.
PASS honest write disclosure - cursor/README.md:33 Explicitly warns that tools can change accounts; asks users to inspect calls in Cursor and makes no AdvisorPPC preview/confirmation guarantee.
PASS visible policies and support - cursor/README.md:41 Privacy, terms, and support links are visible; their network accessibility was not verified offline.
PASS permissive license - cursor/.cursor-plugin/plugin.json:10 Declares MIT and references the repository license; LICENSE:1 contains MIT licensing, with existing trademark reservation unchanged.
PASS naming and final copy - cursor/README.md:1 Shipped metadata/docs call the product Cursor; no Cursor AI, Cursor Code, draft, or do-not-submit wording.
PASS offline lint - .git/cursor_package_lint.py:1 python3 -I .git/cursor_package_lint.py . exited 0: PASS, zero errors, one local-install warning; static lint does not settle fees or runtime behavior.
Alhamdulillah
no repeat
