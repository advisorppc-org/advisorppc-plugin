# Security Policy

## Scope

This repository contains only the plugin manifest, marketplace definition,
skills, and documentation. It ships no executable server code and holds no
secrets. The AdvisorPPC connector itself is a hosted service operated by
Advisor Media Group LLC at `mcp.advisorppc.com`.

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
