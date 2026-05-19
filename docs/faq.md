# FAQ — Akamai Bot Manager

## Pricing

**How much does a solve cost?** From $0.001 per solve. Flat — no
per-account tier, no monthly minimum, no retainer.

**Do I get free credit to try?** Yes — every account gets $0.10 in
real credits on signup, no card required.

**How do I pay?** Card (Stripe) or crypto. Top up the balance at
[capzy.ai/dashboard/billing](https://capzy.ai/dashboard/billing).

## Setup

**How do I get an API key?** Sign up at
[capzy.ai/auth/register](https://capzy.ai/auth/register), then grab a
key from [capzy.ai/dashboard/api-keys](https://capzy.ai/dashboard/api-keys).
Keys start with `capzy_`.

## Behaviour

**How long does a solve take?** ~12 seconds median for Akamai Bot Manager.
Cap your polling loop at 120 seconds — solves that take longer than
that are abnormal.

**Can I solve in parallel?** Yes. Account default is 30 concurrent
in-flight tasks; raised on request.

**Is there a rate limit?** Account default is 30 `createTask` requests
per second. Capzy's infrastructure scales horizontally — contact us
if you need higher limits.

## Errors and refunds

**What if a solve fails?** Failed solves auto-refund. Capzy only
deducts the solve fee when it successfully returns a solution.

**Are successful solves refundable?** No. Once a solution is handed
back, the work is done. If the solution doesn't behave the way you
expected at the target site, open a [support ticket](https://capzy.ai/support).

**Are there hidden fees?** No. The flat per-solve price is everything.

## Integration

**Can I use this with Selenium / Puppeteer / Playwright?** Yes — call
the Capzy API, get the solution, then apply it to the page (set a
field, click a coordinate, paste a token, whatever the task type
returns).

**Can I call Capzy from the browser?** No — your API key would be
exposed. Always call from a backend you control.

**Is there an SDK?** Yes — official Python SDK at
[github.com/capzy-ai/capzy-pip](https://github.com/capzy-ai/capzy-pip).
This repo is the SDK-free path for everyone else.

## Captcha-specific questions

**How long do the cookies last?** Typically the browser session or a few hours. Re-solve after expiry or after protected actions (login, checkout) which often invalidate them.

**Banking / big-retail sites are tougher — anything I can do?** Strict deployments add per-customer ML on top of standard Bot Manager. Use the proxy variant with your own clean IP.

## Operational

**Where can I see uptime / incidents?**
[capzy.ai/status](https://capzy.ai/status).

**Where can I see my usage / spend?** The
[dashboard](https://capzy.ai/dashboard) shows your balance, recent
tasks, error rates, and a usage breakdown.

**How do I get help?** Open a [support ticket](https://capzy.ai/support).
Include the `taskId` for solve-specific questions.
