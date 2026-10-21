#!/usr/bin/env python3
"""Fill the AdvisorPPC dashboard template from a JSON file.

Usage:
    python3 fill-dashboard.py DATA.json OUT.html [--artifact] [--template PATH]

Writes OUT.html from assets/dashboard.html with the <script id="ppc-data">
block replaced by DATA.json. Without --artifact the output is a complete
standalone document (doctype and charset) for opening from disk; with
--artifact it is the fragment form the Artifact tool wraps itself. --template
points at another page built on the same ppc-data block (the audit page in
skills/google-ads-audit/assets/audit.html).

When DATA.json has proposed_actions (an audit), the script sorts them by
severity and rewrites DATA.json in place in that order, so page numbers and
file numbers match.

Why: Claude never needs to read the template into context. It writes the
JSON, runs this script, and publishes or opens the result.
"""
import json
import re
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "dashboard.html"
BLOCK = re.compile(r'(<script id="ppc-data" type="application/json">)(.*?)(</script>)', re.S)


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    data_path, out_path = Path(argv[1]), Path(argv[2])
    artifact = "--artifact" in argv[3:]
    template = TEMPLATE
    if "--template" in argv[3:]:
        i = argv.index("--template")
        if i + 1 >= len(argv):
            sys.exit("--template needs a path")
        template = Path(argv[i + 1])
    if not template.is_file():
        sys.exit(f"template not found: {template}")
    if not data_path.is_file():
        sys.exit(f"data file not found: {data_path}")
    data = json.loads(data_path.read_text(encoding="utf-8"))
    data.setdefault("meta", {})["example"] = False
    # Audit pages number proposed actions; sort by severity here (stable) and
    # write the same order back to DATA.json so the user's "apply 1, 3" means
    # the same rows on the page and in the file Claude reads.
    actions = data.get("proposed_actions")
    if isinstance(actions, list):
        rank = {"high": 0, "medium": 1, "low": 2}
        data["proposed_actions"] = sorted(
            [a for a in actions if isinstance(a, dict)],
            key=lambda a: rank.get(str(a.get("severity") or "low").lower(), 2),
        )
        data["partial_failures"] = [p for p in (data.get("partial_failures") or []) if isinstance(p, dict)]
        data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Every "<" becomes \\u003c so no value can end the script block early.
    payload = json.dumps(data, ensure_ascii=False, indent=2).replace("<", "\\u003c")
    html = template.read_text(encoding="utf-8")
    html, n = BLOCK.subn(lambda m: m.group(1) + "\n" + payload + "\n" + m.group(3), html, count=1)
    if n != 1:
        sys.exit("template has no ppc-data block")
    if not artifact:
        html = "<!doctype html>\n<html lang=\"en\"><head>" + html.split("</style>", 1)[0] + "</style></head><body>" + html.split("</style>", 1)[1] + "</body></html>"
    out_path.write_text(html, encoding="utf-8")
    print(f"wrote {out_path} ({len(html)} bytes, {'artifact fragment' if artifact else 'standalone document'})")


if __name__ == "__main__":
    main(sys.argv)
