<div align="center">

<img src="https://capzy.ai/capzy-logo.svg" alt="Capzy" width="220" />

# Akamai Bot Manager Solver

**Bypass Akamai BMP. Returns validated _abck, bm_sz, ak_bmsc cookies.**

[![Solve cost](https://img.shields.io/badge/from-%240.001%20%2F%20solve-%23ff5d2a)](https://capzy.ai/pricing)
[![Speed](https://img.shields.io/badge/avg%20solve-~12%20seconds-%2322c55e)](https://capzy.ai/products/akamai)
[![Uptime](https://img.shields.io/badge/uptime-99.9%25-%2322c55e)](https://capzy.ai/status)
[![License: MIT](https://img.shields.io/badge/license-MIT-%23ff5d2a)](LICENSE)

[Live Demo](https://capzy.ai/products/akamai/demo) ·
[Get Free $0.10 Credit](https://capzy.ai/auth/register) ·
[Dashboard](https://capzy.ai/dashboard) ·
[Full Docs](https://capzy.ai/docs) ·
[Pricing](https://capzy.ai/pricing)

</div>

---

## What this repo is

Copy-pasteable examples for solving **Akamai Bot Manager** through the
[Capzy](https://capzy.ai) HTTP API — no SDK required. Pure curl, Python,
and Node.js using the raw API. Easy to read, easy to port, easy to audit.

## What is Akamai Bot Manager?

Akamai Bot Manager is one of the most widely deployed enterprise bot defense systems. Collects 100+ browser signals via obfuscated JS (bmak), posts sensor_data, and validates via the `_abck` cookie (must contain `~0~`). Capzy returns the validated cookies plus the matching User-Agent.

## Why Capzy

- **From $0.001 per solve.** Flat pricing — no tiers, no retainer, no monthly minimum.
- **~12 seconds average solve.** Production-grade speed.
- **Drop-in compatible.** `createTask` / `getTaskResult` protocol. If your code already speaks the standard solver shape, swap the host to `https://api.capzy.ai`.
- **$0.10 in real credits on sign-up.** No card. 100 free test solves.

## Pricing

| Task type | When to use | Cost / solve |
|-----------|-------------|-------------:|
| `AntiAkamaiBMPTaskProxyLess`             | Proxyless (Capzy supplies the IP) | **$0.001**   |
| `AntiAkamaiBMPTask`                       | You supply the proxy              | **$0.001**   |

For consistency across the target site, use the proxy variant with the
**same proxy your session is already running through** — the solver
mints the token from that IP, so when you submit it back through the
same proxy everything looks consistent.

## 60-second quickstart

```bash
# 1. Sign up — gets you $0.10 in free credits (100 solves)
open https://capzy.ai/auth/register

# 2. Copy your API key from the dashboard
#    https://capzy.ai/dashboard/api-keys

# 3. Run any example
export CAPZY_KEY="capzy_..."
bash examples/curl/basic.sh
```

Minimal Python:

```python
import requests, time

KEY = "capzy_xxxxxxxxxxxxxxxxxxxxxxxx"

# 1) Create the task
created = requests.post("https://api.capzy.ai/createTask", json={
    "clientKey": KEY,
    "task": {
        "type": "AntiAkamaiBMPTaskProxyLess",
        "websiteURL": "https://example.com/"
    },
}).json()
task_id = created["taskId"]

# 2) Poll until ready
while True:
    result = requests.post("https://api.capzy.ai/getTaskResult", json={
        "clientKey": KEY, "taskId": task_id,
    }).json()
    if result["status"] == "ready":
        break
    time.sleep(2)

print(result["solution"])
```

That's the whole protocol. The rest of this repo is just that, in every
language we could think of.

## Pick your language

| Language        | Example                                       |
|-----------------|-----------------------------------------------|
| **curl / bash** | [`examples/curl/basic.sh`](examples/curl/basic.sh)    |
| **Python**      | [`examples/python/basic.py`](examples/python/basic.py) |
| **Node.js**     | [`examples/nodejs/basic.js`](examples/nodejs/basic.js) |

See [`examples/README.md`](examples/README.md) for setup details.

## Request envelope

```json
{
  "clientKey": "capzy_xxxxxxxxxxxxxxxxxxxxxxxx",
  "task": {
    "type": "AntiAkamaiBMPTaskProxyLess",
    "websiteURL": "https://example.com/"
  }
}
```

| Field | Type | Required | Notes |
|-------|------|:--------:|-------|
| `type` | `string` | yes | AntiAkamaiBMPTaskProxyLess or AntiAkamaiBMPTask |
| `websiteURL` | `string` | yes | Full URL of the Akamai-protected page |
| `proxyType` | `string` | no  | http | https | socks4 | socks5 (only for `AntiAkamaiBMPTask`) |
| `proxyAddress` | `string` | no  | IP or hostname of your proxy (only for `AntiAkamaiBMPTask`) |
| `proxyPort` | `integer` | no  | Port number of your proxy (only for `AntiAkamaiBMPTask`) |
| `proxyLogin` | `string` | no  | Optional — omit if your proxy doesn't require auth (only for `AntiAkamaiBMPTask`) |
| `proxyPassword` | `string` | no  | Optional — omit if your proxy doesn't require auth (only for `AntiAkamaiBMPTask`) |

Full reference in [`docs/parameters.md`](docs/parameters.md).

## Response shape

When the task is ready (`status: "ready"`), `solution` contains:

| Field | Type | Notes |
|-------|------|-------|
| `cookies` | `array` | Cookie objects `{name, value, domain, path}`. Always includes `_abck` (containing `~0~`) and `bm_sz`. Also includes any other Akamai cookies the deployment set (`ak_bmsc`, `bm_sv`, `bm_mi`, `bm_so`, `sbsd_o`). |
| `userAgent` | `string` | Exact User-Agent the browser used. Reuse verbatim on replay — Akamai correlates UA with the TLS fingerprint. |
| `ipBound` | `boolean` | Always `true`. Cookies are bound to the IP that solved the challenge. |
| `domain` | `string` | Hostname the cookies were validated against (host of `websiteURL`). |
| `sensorPosts` | `integer` | Number of bmak sensor_data POSTs fired during the solve. Normal: 1–3. Diagnostic only. |

### Example

```json
{
  "errorId": 0,
  "status": "ready",
  "solution": {
    "cookies": [
      {
        "name": "_abck",
        "value": "0F8B...~0~YAAQa...~-1~|...",
        "domain": ".example.com",
        "path": "/"
      },
      {
        "name": "bm_sz",
        "value": "8E6A...AAQAAQ==",
        "domain": ".example.com",
        "path": "/"
      },
      {
        "name": "ak_bmsc",
        "value": "C4F2...0000",
        "domain": ".example.com",
        "path": "/"
      }
    ],
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "ipBound": true,
    "domain": "www.example.com",
    "sensorPosts": 2
  }
}
```

### How to use the result

Set every cookie from the `cookies` array on your HTTP client (keep `domain` and `path` intact), reuse the exact `userAgent`, and replay through the same IP that solved the challenge. Akamai validates the full set as a unit — missing `bm_sz`, swapping the UA, or coming from a different egress IP all invalidate the session immediately.

## Features

- Returns validated _abck (`~0~`) + bm_sz + ak_bmsc cookies
- User-Agent + cookie pairing for direct session reuse
- Handles standard Bot Manager deployments end-to-end

## FAQ

**How long do the cookies last?** Typically the browser session or a few hours. Re-solve after expiry or after protected actions (login, checkout) which often invalidate them.

**Banking / big-retail sites are tougher — anything I can do?** Strict deployments add per-customer ML on top of standard Bot Manager. Use the proxy variant with your own clean IP.

## What you'll need

- A Capzy API key — [sign up](https://capzy.ai/auth/register) (free, $0.10 credit).
- Network access to `https://api.capzy.ai`.

## Other captcha types

Capzy solves 25+ captcha types. Full catalog at
[capzy.ai/pricing](https://capzy.ai/pricing). Each type has its own
solver repo on [github.com/capzy-ai](https://github.com/capzy-ai).

## License

[MIT](LICENSE).

---

<div align="center">

**[Sign up for free credits →](https://capzy.ai/auth/register)**

Built by [Capzy](https://capzy.ai). Issues + PRs welcome.

</div>
