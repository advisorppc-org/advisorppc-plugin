---
type: regex
pattern: "claude (mcp|plugin)|(^|\\s)/mcp\\b|/plugin\\b|\\.mcp\\.json|~/\\."
match: not_contains
---

A Claude app user gets no terminal commands, slash commands or config file edits.
