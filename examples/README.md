# Examples — Akamai Bot Manager

Copy-pasteable examples for solving **Akamai Bot Manager** through the
Capzy HTTP API. Three languages, same two-step protocol:

1. `POST /createTask` — get a `taskId`
2. `POST /getTaskResult` (poll every 2s) until `status === "ready"`

## Setup

1. **Sign up** at [capzy.ai/auth/register](https://capzy.ai/auth/register) — $0.10 in real credits on signup. No card required.
2. **Get your API key** at [capzy.ai/dashboard/api-keys](https://capzy.ai/dashboard/api-keys). Keys start with `capzy_`.
3. **Export it** — every example reads `CAPZY_KEY` from the environment:
   ```bash
   export CAPZY_KEY="capzy_xxxxxxxxxxxxxxxxxxxxxxxx"
   ```
4. **Update the example** — open the file you want to run and replace any `https://example.com` / placeholder sitekey / etc. with values from the page you're actually solving against.

## Files

| Language        | File                              |
|-----------------|-----------------------------------|
| **curl / bash** | [`curl/basic.sh`](curl/basic.sh)  |
| **Python**      | [`python/basic.py`](python/basic.py) |
| **Node.js**     | [`nodejs/basic.js`](nodejs/basic.js) |

Each example is fully self-contained and ~50 lines. No SDK, no client
library, no abstraction between you and the API.
