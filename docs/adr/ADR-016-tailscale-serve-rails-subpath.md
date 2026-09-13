# ADR-016: Tailscale Serve subpath — emit prefix, never redirect stripped root

**Status:** Accepted
**Date:** 2026-09-12
**Deciders:** Operator + Architecture
**Builds on:** ADR-001 (majestic monoliths), ADR-005 (responsive user pages — MagicDNS is a human UI)
**Incident seed:** 2026-09-12 — `https://sawtooth-ai.tail944ffb.ts.net/wut/` infinite 302 (`Location: /wut/`). Nested pages (`/wut/portfolio_backtest_runs`) stayed 200.
**Glossary:** Winston Unit Test (WUT), Winston v2 (Wv2), data_manager (DM)
**Analysis:** `docs/analysis/2026-07-04-tailscale-serve-rails-subpath.md`
**Hint:** `hints/tailscale-serve-no-root-redirect.md`

## Context

Winston operator UIs are reached on the tailnet as path prefixes on one MagicDNS name:

| Public path | Upstream | Compose host port |
|-------------|----------|-------------------|
| `/wut` | WUT Puma | 3000 |
| `/wv2` | Wv2 Puma | 3002 |
| `/dm` | DM Puma | 3001 |

`tailscale serve --set-path=/wut http://127.0.0.1:3000` **strips** `/wut` before proxying. `GET /wut/` arrives at Puma as `GET /`. Rails must still **emit** `/wut/...` for links, CSS, JS, and Action Cable.

Two implementations existed:

- **A. SCRIPT_NAME only (2026-07-04 `ee23c3b`)** — set `Rack::SCRIPT_NAME=/wut`; do not redirect `/`. Serve-stripped home is the real home.
- **B. Also 302 `/` → `/wut/` (2026-07-06 `1a91ef5`)** — “bare root UX” so `localhost:3000/` lands on `/wut/`. Under Serve, that 302 is an infinite loop.

**B** shipped inside a WUT trend-vetting commit, was verified only with an in-process Ruby mock, and was copied into Wv2 on 2026-07-22 (`740bbae`). Nested MagicDNS URLs kept working, so the loop stayed hidden until someone opened `/wut/` itself (Winston logo = `root_path` = `/wut/`).

## Decision

Choose **A**. Estate rule:

1. **Serve strips; Rails emits.** `RAILS_RELATIVE_URL_ROOT` / `TailscaleScriptName` set `SCRIPT_NAME` and strip a *present* prefix so `localhost:3000/wut/...` still routes. They must not 302 `/`, `""`, or `/wut` to `/wut/`.
2. **MagicDNS home must be 200.** After any change to this middleware, `curl -sI https://sawtooth-ai.tail944ffb.ts.net/wut/` and `/wv2/` must be **200**, not 302 to the same path.
3. **Copy the spec with the middleware.** `spec/lib/tailscale_script_name_spec.rb` is the lock. A new monolith behind Serve gets the spec, not a “helpful” root redirect.
4. **Do not sniff Host / X-Forwarded-*.** Prefix is boot-time config. Detection logic was rejected on 2026-07-06; keep that. The forbidden move is the redirect, not the always-prefix model.
5. **Internal compose paths stay unprefixed.** `/internal/*` between containers is not a Serve URL.

## Rationale

- **Not B:** Serve-stripped `/` is the public home. Redirecting it to the prefix Serve just stripped cannot converge.
- **Not a Business Rule:** this is access topology, not fills, risk, or journals.
- **Not only a hint:** the same middleware was copied across monoliths. An ADR is the contract; the hint is the session-start gotcha.

## Consequences

### Positive

- `/wut/` and `/wv2/` on MagicDNS stay reachable.
- Localhost `:3000/` serves the app (links still `/wut/...`) instead of bouncing through Serve.
- Agents have a named prohibition when “fixing” subpath URLs.

### Negative

- Address bar on `localhost:3000/` is not forced to `/wut/`. First click into nav still goes under the prefix.

### Risks mitigated

- “Make `/` consistent with `/wut/`” UX redirects.
- Copying WUT middleware into Wv2/DM without the regression spec.
- Treating a Tailscale client bump as the cause when the landmine is in Rails.

## Smoke

```bash
curl -sI https://sawtooth-ai.tail944ffb.ts.net/wut/  | grep -E 'HTTP/|location:'
curl -sI https://sawtooth-ai.tail944ffb.ts.net/wv2/  | grep -E 'HTTP/|location:'
# expect HTTP/2 200 and no location: /wut/ or /wv2/

cd winston_unit_test && bundle exec rspec spec/lib/tailscale_script_name_spec.rb
cd winston_v2         && bundle exec rspec spec/lib/tailscale_script_name_spec.rb
```
