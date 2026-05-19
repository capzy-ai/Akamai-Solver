#!/usr/bin/env bash
#
# Solve Akamai Bot Manager with Capzy — pure curl + jq.
#
# Cost:   from $0.001 per solve (flat)
# Speed:  ~12 seconds median
#
# Requires: curl, jq (brew install jq / apt install jq)
#
# Run with:
#   export CAPZY_KEY="capzy_xxxxxxxxxxxxxxxxxxxxxxxx"
#   bash basic.sh

set -euo pipefail

API_BASE="${API_BASE:-https://api.capzy.ai}"
: "${CAPZY_KEY:?set CAPZY_KEY in your env (grab one at https://capzy.ai/auth/register)}"

# Customize the task body to match the target site you're solving.
TASK=$(cat <<'JSON'
{
    "type": "AntiAkamaiBMPTaskProxyLess",
    "websiteURL": "https://example.com/"
}
JSON
)

# ─── 1) Create the task ───────────────────────────────────────────────
echo "creating task..."
CREATE_RESP=$(curl -sS -X POST "${API_BASE}/createTask" \
  -H 'Content-Type: application/json' \
  -d "{\"clientKey\":\"${CAPZY_KEY}\",\"task\":${TASK}}")

ERROR_ID=$(echo "$CREATE_RESP" | jq -r '.errorId // 0')
if [ "$ERROR_ID" != "0" ]; then
  echo "createTask failed:" >&2
  echo "$CREATE_RESP" | jq . >&2
  exit 1
fi

TASK_ID=$(echo "$CREATE_RESP" | jq -r '.taskId')
echo "created task ${TASK_ID}"

# ─── 2) Poll until ready ──────────────────────────────────────────────
DEADLINE=$(( $(date +%s) + 120 ))
while [ "$(date +%s)" -lt "$DEADLINE" ]; do
  RESULT=$(curl -sS -X POST "${API_BASE}/getTaskResult" \
    -H 'Content-Type: application/json' \
    -d "{\"clientKey\":\"${CAPZY_KEY}\",\"taskId\":\"${TASK_ID}\"}")

  STATUS=$(echo "$RESULT" | jq -r '.status // "unknown"')
  if [ "$STATUS" = "ready" ]; then
    echo "$RESULT" | jq '.solution'
    exit 0
  fi
  if [ "$STATUS" != "processing" ]; then
    echo "unexpected status: $STATUS" >&2
    echo "$RESULT" | jq . >&2
    exit 1
  fi
  sleep 2
done

echo "solve took longer than 120s — unusual; check https://capzy.ai/status" >&2
exit 1
