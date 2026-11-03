# Mission: Playwright with Claude

## Why
Drive a real browser from Claude Code through the Playwright MCP server, to inspect, test and automate web apps such as the inventory-management demo, instead of clicking through them by hand.

## Success looks like
- Prompt Claude to open the local app, find elements and complete a multi-step flow, and know why each step worked or failed.
- Configure the Playwright MCP server (flags, profile, headless) for a given task.
- Spot when a run is slow, flaky or unsafe, and fix the prompt or config.

## Constraints
- Starting point: basic Playwright knowledge, little experience using it through Claude.
- Practice target: this repo (`http://localhost:3000` frontend, `http://localhost:8001` API).

## Out of scope
- Writing a full Playwright Test suite by hand (revisit later if the mission shifts).
