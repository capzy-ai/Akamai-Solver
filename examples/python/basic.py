"""
Solve Akamai Bot Manager with Capzy — minimal Python example, `requests` only.

Cost:   from $0.001 per solve (flat)
Speed:  ~12 seconds median

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
    #    solve runs on Capzy's infrastructure.
    created = requests.post(
        f"{API_BASE}/createTask",
        json={
            "clientKey": CAPZY_KEY,
            "task": {
                "type": "AntiAkamaiBMPTaskProxyLess",
                "websiteURL": "https://example.com/"
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
    # Set every returned cookie on your HTTP client and reuse the User-Agent. Cookies are IP-bound — keep the same source IP for follow-up requests.
