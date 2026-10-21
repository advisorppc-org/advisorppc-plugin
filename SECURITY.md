# Security Policy

## Scope

This repository contains the plugin manifest, marketplace definition and MCP
registration, Markdown skills and documentation, two HTML pages
(`skills/ppc-reporting/assets/dashboard.html` and
`skills/campaign-board/assets/campaign-board.html`) and two offline Python
helpers that use the standard library only and make no network calls
(`skills/ppc-reporting/scripts/fill-dashboard.py` and
`skills/landing-page-ab-testing/scripts/ab_stats.py`). It ships no hooks, no
telemetry and no server code, and holds no secrets. The AdvisorPPC connector
itself is a hosted service operated by Advisor Media at `mcp.advisorppc.com`.

## Reporting a vulnerability

If you believe you have found a security issue in the hosted connector, the
OAuth flow, or anything distributed from this repository:

- Email **contact@advisorppc.com** with the subject line `SECURITY`.
- Include what you found, how to reproduce it, and the impact you believe it
  has. Proof-of-concept detail is welcome; live exploitation of customer data
  is not.
- Please do **not** open a public GitHub issue for security reports.

We acknowledge reports within 3 business days and will keep you informed
through triage and remediation.

## Supported versions

Only the latest published version of the plugin is supported. The hosted
service is continuously deployed; server-side fixes reach all users
immediately, with no plugin update required.
