---
type: llm
---

PASS if the reply says a 401 from opening the MCP endpoint in a browser is expected (it is an endpoint for MCP clients, not a web page) and the service is not down, and suggests /mcp in Claude Code to connect.
FAIL if it says the service is down or tells the user to contact support about an outage.
