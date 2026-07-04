# Ticket: Tailscale Serve deployment docs + Wv2/DM subpath parity

**Status:** Proposed
**Context:** WUT mobile access via `https://sawtooth-ai.tail944ffb.ts.net/wut/` shipped in session `2026-07-04-1511`; root `compose.yml` Tailscale env is on disk but the sawtooth workspace root is **not** a git repo (deployment README incorrectly says compose.yml is "committed").

## Problem

1. **Undocumented operator path** — Tailscale Serve + compose env vars are tribal knowledge; `ecosystem/deployment/README.md` has no Tailscale section.
2. **Unversioned orchestration** — `compose.yml` changes (`RAILS_RELATIVE_URL_ROOT`, `TAILSCALE_HOSTNAME`) risk drift across machines (overlaps `2026-07-02-compose-orchestrator-unification` for tooling; this ticket is **access/env** specific).
3. **Wv2 / DM not served** — Only WUT has subpath middleware; DM host-auth initializer needs image rebuild.
4. **AI profile gap** — `winston_mcp` / `nanobot_cromwell` were removed during WUT container recreate; operator may need `./bin/compose --profile ai up -d`.

## Goal

Reproducible Tailscale access pattern for all three majestic monoliths, documented in ecosystem deployment.

## Proposed work

| # | Task | Owner repo |
|---|------|------------|
| 1 | Add **Tailscale Serve** section to `ecosystem/deployment/README.md` (serve commands, env vars, phone URLs, smoke curls) | ecosystem |
| 2 | Cite analysis `docs/analysis/2026-07-04-tailscale-serve-rails-subpath.md` — do not duplicate | ecosystem |
| 3 | Copy `TailscaleScriptName` + `relative_url_root.rb` pattern to Wv2 (`/wv2`, port 3002) and DM (`/dm`, port 3001) when operator wants phone access | winston_v2, data_manager |
| 4 | Extend root `compose.yml` env for Wv2/DM subpaths (mirror WUT block) | workspace root |
| 5 | Rebuild `data_manager` after `d9ff97e` host-auth initializer | ops |
| 6 | Resolve compose versioning — submodule, meta-repo, or copy env template to `ecosystem/deployment/tailscale-serve.env.template` | ecosystem + decision |

### Suggested Serve layout (one node)

```bash
tailscale serve --bg --set-path=/wut http://127.0.0.1:3000
tailscale serve --bg --set-path=/dm  http://127.0.0.1:3001
tailscale serve --bg --set-path=/wv2 http://127.0.0.1:3002
```

## Acceptance criteria

- [ ] `ecosystem/deployment/README.md` documents WUT Tailscale access end-to-end (host serve + compose env + verification)
- [ ] `ecosystem/deployment/tailscale-serve.env.template` (or equivalent) lists `TAILSCALE_HOSTNAME`, `RAILS_RELATIVE_URL_ROOT`, `TAILSCALE_SERVE_PATH` per monolith — no secrets
- [ ] Operator can reproduce WUT phone access on a fresh `sawtooth-ai` from docs alone
- [ ] DM container rebuilt and MagicDNS host-auth verified after pull
- [ ] (Optional) Wv2 + DM subpath middleware committed and verified at `/wv2/`, `/dm/`
- [ ] Deployment README corrected: clarify whether root `compose.yml` is versioned and where

## Out of scope

- Tailscale Funnel (public internet) — tailnet-only Serve is sufficient
- TLS termination inside Rails — Serve handles HTTPS

## Related

- Analysis: `docs/analysis/2026-07-04-tailscale-serve-rails-subpath.md`
- Session report: `docs/session-reports/2026-07-04-1511-wut-tailscale-serve-mobile-access.md`
- Ticket: `docs/tickets/2026-07-02-compose-orchestrator-unification.md` (compose tooling, not Tailscale)
- WUT: `ee23c3b` | DM host auth: `d9ff97e`