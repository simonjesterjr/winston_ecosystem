# Wv2 public base URL (DAR desk links)

**Env:** `WV2_PUBLIC_BASE_URL` (alias: `WV2_OPS_BASE_URL`)  
**Set in:** root `compose.yml` on `winston_v2` and `winston_v2_sidekiq`

## Purpose

Daily Activity Report PDF/MD **DESK HANDOFFS** embed absolute form URLs. Default without env is `http://localhost:3002`, which is unusable on phone Telegram.

## Current ops value

```text
WV2_PUBLIC_BASE_URL=https://sawtooth-ai.tail944ffb.ts.net/wv2
```

Matches host Tailscale Serve:

```text
https://sawtooth-ai.tail944ffb.ts.net
|-- /wv2 proxy http://127.0.0.1:3002
```

Desk paths are `/operations/desk?...` → full URL  
`https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/desk?...`

## After changing hostname / serve

1. Update compose env on both `winston_v2` and `winston_v2_sidekiq`.
2. `./bin/compose up -d winston_v2 winston_v2_sidekiq` (recreate to pick env).
3. Re-render a DAR PDF or wait for next Daily Analysis.

## Verify

```bash
./bin/compose exec -T winston_v2 printenv WV2_PUBLIC_BASE_URL
curl -sI "https://sawtooth-ai.tail944ffb.ts.net/wv2/operations" | head -5
```
