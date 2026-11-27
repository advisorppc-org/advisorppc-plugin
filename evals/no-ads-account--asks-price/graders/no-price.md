---
type: regex
pattern: "[$€£]\\s?[1-9]|[1-9][0-9]*(\\.[0-9]+)?\\s?(USD|EUR|GBP|dollars|euros|pounds)"
match: not_contains
---

The plan_tool result gives only the Free plan's price of 0, so any other amount in the reply is invented.
