---
name: website-setup
description: This skill should be used when the user asks to "set up my website with AdvisorPPC", "install Shield", "protect my ads from click fraud", "set up Gravity", "start my blog", "automate my blog posts", "capture leads from my site", "set up Tag Manager", "install the AdvisorPPC WordPress plugin", or pastes the AdvisorPPC website setup prompt. It hands the setup to the AdvisorPPC setup planner on the Gravity server.
version: 0.2.0
---

# Website Setup

The setup steps live on the AdvisorPPC servers, not in this skill, so they
always match the customer's plan and the tools that exist today.

1. Make sure the `advisorppc-gravity` server is connected (`/mcp` in Claude
   Code). If it is missing in another app, ask the user to add
   `https://gravity.advisorppc.com/mcp` as a custom connector and sign in.
2. Call `gravity_setup_planner` with the website address as `domain`. It
   returns the questions to ask, the servers to connect, the customer's
   Gravity plan and what the full setup needs.
3. Ask the questions one at a time, then call it again with the `guide_id`,
   the chosen `selected_leaf_nodes` and `accept=true`. Follow the steps it
   returns, in order, and its `rules`.
4. Plans: Gravity, Shield and the AdvisorPPC connector are paid products, each
   with its own plan. When the planner returns `upgrade`, or a step is locked,
   show the plan, the price and the checkout link once, and continue with the
   steps the plan includes. For Shield and the AdvisorPPC connector, use the
   plan tools the planner names in `other_plans`.

Never ask for a password, API key or token in chat. Every server signs in
through the browser.
