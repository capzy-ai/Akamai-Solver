/**
 * Solve Akamai Bot Manager (Web / desktop variant) with Capzy —
 * minimal Node.js example. Returns the _abck cookie + matched UA
 * which you paste into your scraper's HTTP client.
 *
 * For the MOBILE BMP variant (X-acf-sensor-data header from native
 * iOS/Android apps), see ../../akamai-bmp/examples/nodejs/basic.js —
 * different task type (AntiAkamaiBMPTask), different inputs
 * (packageName + version), different output (sensors[] + useragent).
 *
 * Cost:   $0.05 per solve
 * Speed:  ~14 seconds median
 *
 * Run with (Node 18+):
 *   export CAPZY_KEY="capzy_xxxxxxxxxxxxxxxxxxxxxxxx"
 *   node basic.js
 *
 * Uses the built-in global `fetch` — no dependencies, no npm install.
 */

const API_BASE = "https://api.capzy.ai";
const CAPZY_KEY = process.env.CAPZY_KEY;

async function postJson(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return res.json();
}

async function solve() {
  // 1) Create the task.
  const created = await postJson("/createTask", {
    clientKey: CAPZY_KEY,
    task: {
      "type": "AntiAkamaiWebTaskProxyLess",
      "websiteURL": "https://example.com/protected-path"
    },
  });
  if (created.errorId) {
    throw new Error(`createTask: ${created.errorCode} — ${created.errorDescription}`);
  }
  const taskId = created.taskId;
  console.log("created task", taskId);

  // 2) Poll until ready.
  const deadline = Date.now() + 120_000;
  while (Date.now() < deadline) {
    const result = await postJson("/getTaskResult", {
      clientKey: CAPZY_KEY,
      taskId,
    });
    if (result.errorId) {
      throw new Error(`getTaskResult: ${result.errorCode} — ${result.errorDescription}`);
    }
    if (result.status === "ready") return result.solution;
    await new Promise((r) => setTimeout(r, 2000));
  }
  throw new Error("solve took longer than 120s");
}

(async () => {
  const solution = await solve();
  console.log("solution:", solution);
  // ─── How to use the result ──────────────────────────────────
  // Set every returned cookie on your HTTP client and reuse the User-Agent. Cookies are IP-bound — keep the same source IP for follow-up requests.
})();
