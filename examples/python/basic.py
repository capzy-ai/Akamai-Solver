"""
Solve Akamai Bot Manager (Web / desktop variant) with Capzy — minimal
Python example, `requests` only. Returns the `_abck` cookie + matched
User-Agent which you paste into your scraper's HTTP client.

For the MOBILE BMP variant (X-acf-sensor-data header from native iOS/
Android apps), see ../../akamai-bmp/examples/python/basic.py — different
task type (`AntiAkamaiBMPTask`), different inputs (`packageName` +
`version`), different output (`sensors[]` + `useragent`).

Cost:   $0.05 per solve
Speed:  ~14 seconds median

Run with:
    pip install requests
    export CAPZY_KEY="capzy_xxxxxxxxxxxxxxxxxxxxxxxx"
    python basic.py
"""

import os
import time

import requests

API_BASE = "https://api.capzy.ai"

# Grab a key for free at https://capzy.ai/auth/register ($0.10 starter credit).
CAPZY_KEY = os.environ["CAPZY_KEY"]


def solve() -> dict:
    # 1) Create the task. Returns immediately with a taskId; the actual
    #    solve runs on Capzy's infrastructure (real Chrome via residential).
    created = requests.post(
        f"{API_BASE}/createTask",
        json={
            "clientKey": CAPZY_KEY,
            "task": {
                "type": "AntiAkamaiWebTaskProxyLess",
                "websiteURL": "https://example.com/protected-path",
            },
        },
        timeout=15,
    ).json()

    if created.get("errorId"):
        raise RuntimeError(f"createTask failed: {created.get('errorCode')} — "
                           f"{created.get('errorDescription')}")

    task_id = created["taskId"]
    print(f"created task {task_id}")

    # 2) Poll until ready. Cap the wait at 120s for slower captcha types.
    deadline = time.time() + 120
    while time.time() < deadline:
        result = requests.post(
            f"{API_BASE}/getTaskResult",
            json={"clientKey": CAPZY_KEY, "taskId": task_id},
            timeout=15,
        ).json()

        if result.get("errorId"):
            raise RuntimeError(f"getTaskResult failed: {result.get('errorCode')} — "
                               f"{result.get('errorDescription')}")

        if result["status"] == "ready":
            return result["solution"]

        time.sleep(2)

    raise TimeoutError("solve took longer than 120s")


if __name__ == "__main__":
    solution = solve()
    print("solution:", solution)
    # ─── How to use the result ────────────────────────────────────
    # solution has: cookies[], userAgent, ipBound=true
    # Set every cookie on your HTTP client + reuse the userAgent. The
    # _abck cookie is IP-bound — keep the same source IP for follow-up
    # requests (or use AntiAkamaiWebTask with your own proxy so the
    # cookie is bound to YOUR IP).
