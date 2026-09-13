# Tailscale Serve: never 302 `/` to `/wut/` or `/wv2/`

**As of 2026-09-12:** MagicDNS `https://sawtooth-ai.tail944ffb.ts.net/wut/` looping is almost never a Tailscale outage. Serve **strips** `--set-path=/wut` before Puma. `GET /wut/` arrives as `GET /`. Redirecting `/` to `/wut/` is an infinite loop.

Nested pages (`/wut/portfolio_backtest_runs`) can stay 200 while home is dead. `localhost:3000/wut/` can stay 200 (prefix still on PATH). That is how this stayed hidden from 2026-07-06 until someone opened `/wut/`.

**Do:** `TailscaleScriptName` sets `SCRIPT_NAME` and strips a present prefix. Spec: `spec/lib/tailscale_script_name_spec.rb`.

**Do not:** 302 `/`, `""`, or `/wut` to `/wut/` (same for `/wv2`). Do not add Host / X-Forwarded sniffing.

**Smoke:** `curl -sI https://sawtooth-ai.tail944ffb.ts.net/wut/` → 200, not `location: /wut/`.

ADR-016. Analysis: `docs/analysis/2026-07-04-tailscale-serve-rails-subpath.md`.
