# Analysis: Tailscale Serve + Rails subpath (WUT `/wut`)

**Date:** 2026-07-04
**Scope:** Exposing Sawtooth Rails monoliths behind `tailscale serve --set-path=...`
**Reference implementation:** WUT on `sawtooth-ai` (session `2026-07-04-1511-wut-tailscale-serve-mobile-access`)

## Summary

Tailscale Serve can expose a local upstream (e.g. `http://127.0.0.1:3000`) under a public path on the node's MagicDNS name (e.g. `https://sawtooth-ai.tail944ffb.ts.net/wut/`). Rails needs **two** fixes beyond opening port 3000 on the tailnet:

1. **Host authorization** — allow MagicDNS and CGNAT IPs (initializer pattern, all environments).
2. **Subpath URL generation** — Serve **strips** the public prefix before proxying; Rails must still **emit** prefixed links and asset paths.

Missing (2) produces: home page loads, nav clicks 404, mobile looks unstyled (CSS/JS 404 at `/assets/...` instead of `/wut/assets/...`).

## Architecture

```
Phone/browser
  → https://sawtooth-ai.<tailnet>.ts.net/wut/data_sets
Tailscale Serve (host)
  → http://127.0.0.1:3000/data_sets     # /wut stripped
Podman publish
  → winston_unit_test:3000/data_sets
Rails
  must generate links as /wut/data_sets  # prefix added back
```

## Host authorization

**Location:** `config/initializers/allowed_hosts.rb` per monolith (not `development.rb` only).

| Allow | Pattern | Notes |
|-------|---------|-------|
| Compose DNS | `winston_unit_test`, `data_manager:3000`, etc. | Internal monolith-to-monolith |
| MagicDNS FQDN | `/.*\.ts\.net/` regex | **Not** `/\.ts\.net$/` — Rails wraps regexes with `\A...\z` |
| Tailscale CGNAT | `IPAddr.new("100.64.0.0/10")` | Direct `http://100.x.x.x:port` access |
| Short hostname | `ENV["TAILSCALE_HOSTNAME"]` | e.g. `sawtooth-ai` |
| Extras | `ENV["RAILS_ALLOWED_HOSTS"]` | Comma-separated |

**Gotcha:** `config.hosts << /\.ts\.net$/` appears correct but **never matches** FQDNs after `HostAuthorization::Permissions#sanitize_regexp`.

WUT ActionCable: set `allowed_request_origins` for `https?://.*\.ts\.net.*` in the same initializer.

## Subpath URL generation (WUT-specific today)

**Env (compose):**

```yaml
RAILS_RELATIVE_URL_ROOT=/wut
TAILSCALE_SERVE_PATH=/wut      # alias read by initializer
TAILSCALE_HOSTNAME=sawtooth-ai
```

**Code:**

| File | Role |
|------|------|
| `config/initializers/relative_url_root.rb` | Sets `relative_url_root`, ActionCable `url` → `/wut/cable` |
| `lib/tailscale_script_name.rb` | Middleware: `env[Rack::SCRIPT_NAME] = "/wut"` |

Rails 7 reads `RAILS_RELATIVE_URL_ROOT` at boot, but **link helpers still fail** without `SCRIPT_NAME` middleware because views merge `request.script_name` (empty after Serve strips the path) over `default_url_options`.

**Why assets broke on mobile:** `stylesheet_link_tag` uses `relative_url_root` → `/wut/assets/...` ✅. Nav `link_to` used empty `script_name` → `/data_sets` ❌.

## Internal APIs unaffected

Compose calls `http://winston_unit_test:3000/internal/...` arrive **without** `/wut` prefix. Routing still works; `SCRIPT_NAME` middleware only affects URL **generation**, not path matching for unprefixed internal requests.

## Operator commands (host)

```bash
# One-time (sudo may be required)
tailscale serve --bg --set-path=/wut http://127.0.0.1:3000

tailscale serve status
# https://sawtooth-ai.<tailnet>.ts.net (tailnet only)
# |-- /wut proxy http://127.0.0.1:3000
```

**Phone URL:** `https://sawtooth-ai.tail944ffb.ts.net/wut/`

## Extending to Wv2 / DM

| Monolith | Host port | Suggested serve path | Subpath middleware needed? |
|----------|-----------|----------------------|----------------------------|
| WUT | 3000 | `/wut` | ✅ shipped (`TailscaleScriptName`) |
| DM | 3001 | `/dm` | Yes — copy middleware + env pattern |
| Wv2 | 3002 | `/wv2` | Yes — copy middleware + env pattern |

Host-auth initializers for DM and Wv2 are already on `main`; DM image needs **rebuild** (no bind mount). Subpath middleware is **WUT-only** until copied.

## Local dev trade-off

With `RAILS_RELATIVE_URL_ROOT=/wut` set, `http://localhost:3000` also generates `/wut/...` links. Intentional on Tailscale nodes. Unset env for pure local dev without Serve.

## Verification smoke

```bash
curl -sk -o /dev/null -w "%{http_code}\n" https://sawtooth-ai.tail944ffb.ts.net/wut/
curl -sk https://sawtooth-ai.tail944ffb.ts.net/wut/ | grep -o 'href="/wut/data_sets"'
curl -sk -o /dev/null -w "%{http_code}\n" https://sawtooth-ai.tail944ffb.ts.net/wut/data_sets
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3000/internal/active_markets
```

## Related

- Session report: `docs/session-reports/2026-07-04-1511-wut-tailscale-serve-mobile-access.md`
- Ticket: `docs/tickets/2026-07-04-tailscale-serve-ecosystem-deployment.md`
- WUT commits: `ee23c3b` (subpath), initializers in same commit
- DM commit: `d9ff97e` (host auth only)