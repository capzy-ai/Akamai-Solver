# Parameters reference — Akamai Bot Manager

Every field you can pass to `POST /createTask` for this task type.

## Envelope

```json
{
  "clientKey": "capzy_xxxxxxxxxxxxxxxxxxxxxxxx",
  "task": { ... }
}
```

| Field        | Required | Notes                                                       |
|--------------|:--------:|-------------------------------------------------------------|
| `clientKey`  | yes      | Your Capzy API key. Starts with `capzy_`. Find it at [capzy.ai/dashboard/api-keys](https://capzy.ai/dashboard/api-keys). |
| `task`       | yes      | The task object — see below.                                |

## Task object

### Required + optional fields

| Field | Type | Required | Notes |
|-------|------|:--------:|-------|
| `type` | `string` | yes | AntiAkamaiBMPTaskProxyLess or AntiAkamaiBMPTask |
| `websiteURL` | `string` | yes | Full URL of the Akamai-protected page |


### Proxy fields (only for `AntiAkamaiBMPTask`)

| Field | Type | Required | Notes |
|-------|------|:--------:|-------|
| `proxyType` | `string` | no | http | https | socks4 | socks5 |
| `proxyAddress` | `string` | no | IP or hostname of your proxy |
| `proxyPort` | `integer` | no | Port number of your proxy |
| `proxyLogin` | `string` | no | Optional — omit if your proxy doesn't require auth |
| `proxyPassword` | `string` | no | Optional — omit if your proxy doesn't require auth |


## Response

### `POST /createTask` success

```json
{
  "errorId": 0,
  "taskId":  "12345"
}
```

### `POST /getTaskResult` while processing

```json
{
  "errorId": 0,
  "status":  "processing"
}
```

### `POST /getTaskResult` when ready

```json
{
  "errorId":  0,
  "status":   "ready",
  "solution": { ... }
}
```

The `solution` object contains:

| Field | Type | Notes |
|-------|------|-------|
| `cookies` | `array`   | Cookie objects `{name, value, domain, path}`. Always includes `_abck` (with `~0~`) and `bm_sz`. Also includes any secondary Akamai cookies the deployment set (`ak_bmsc`, `bm_sv`, `bm_mi`, `bm_so`, `sbsd_o`). |
| `userAgent`   | `string`  | Exact User-Agent the browser used while earning the cookies. Reuse verbatim on replay. |
| `ipBound`     | `boolean` | Always `true`. Cookies are bound to the IP that solved the challenge. |
| `domain`      | `string`  | Hostname the cookies were validated against (host portion of `websiteURL`). |
| `sensorPosts` | `integer` | bmak sensor_data POST count during the solve. Normal: 1–3. Diagnostic only. |

#### Concrete example

```json
{
  "errorId": 0,
  "status": "ready",
  "solution": {
    "cookies": [
      { "name": "_abck",   "value": "0F8B...~0~YAAQa...~-1~|...", "domain": ".example.com", "path": "/" },
      { "name": "bm_sz",   "value": "8E6A...AAQAAQ==",            "domain": ".example.com", "path": "/" },
      { "name": "ak_bmsc", "value": "C4F2...0000",                "domain": ".example.com", "path": "/" }
    ],
    "userAgent":   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "ipBound":     true,
    "domain":      "www.example.com",
    "sensorPosts": 2
  }
}
```

### How to use the solution

Set every cookie from `cookies` on your HTTP client preserving `domain` and `path`, reuse the exact `userAgent`, and replay through the same IP that solved the challenge. Akamai validates the cookie set as a unit — missing any cookie (especially `bm_sz`, which seeds the PRNG for subsequent sensor posts), swapping the UA, or coming from a different egress IP all invalidate the session.

### Error

```json
{
  "errorId":          1,
  "errorCode":        "ERROR_KEY_DOES_NOT_EXIST",
  "errorDescription": "Invalid API key"
}
```

`errorId` is `0` on success, `1` on any error. The `errorCode` is the
stable machine-readable identifier. Common codes:

- `ERROR_KEY_DOES_NOT_EXIST` — bad API key
- `ERROR_NO_BALANCE` — account balance below the cost of this task
- `ERROR_INVALID_PARAMS` — missing required field or malformed value
- `ERROR_MAX_TASKS_REACHED` — concurrent in-flight cap reached (default 30)
- `ERROR_RATE_LIMITED` — too many createTask calls per second
- `ERROR_TIMEOUT` — solve took longer than the cap (auto-refunded)
- `ERROR_CAPTCHA_UNSOLVABLE` — solver gave up (auto-refunded)

## Naming conventions

Field names are camelCase on the wire (`websiteURL`, `websiteKey`,
`proxyAddress`). Stick to that exactly when you build the JSON.
