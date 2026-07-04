# Session Report — WUT Tailscale Serve + Mobile Access

**Date:** 2026-07-04
**Time:** ~11:00–15:11 America/Denver (approx.)
**Duration:** ~4h (multi-turn; includes discovery + fix iterations)
**Project:** Sawtooth / Winston ecosystem (WUT primary; DM + compose)
**Working directory:** /home/johnkoisch/Documents/com/sawtooth
**Branch:** main (winston_unit_test, data_manager, ecosystem)
**Model:** Grok
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Make Winston Unit Test (WUT), running in containers on `sawtooth-ai`, reachable from phone/other devices via Tailscale — ideally at a path like `sawtooth-ai/wut`.

**Outcome:** Delivered

**One-line summary:** WUT is live at `https://sawtooth-ai.tail944ffb.ts.net/wut/` with working nav, assets, ActionCable, and mobile styling; host-auth and subpath URL generation are deployment-agnostic via initializers + compose env.

---

## 2. Work Completed

- Identified Tailscale identity for this node (`sawtooth-ai`, `100.121.176.51`, MagicDNS `sawtooth-ai.tail944ffb.ts.net`)
- Confirmed user-configured `tailscale serve --bg --set-path=/wut http://127.0.0.1:3000`
- Diagnosed and fixed Rails `HostAuthorization` blocking MagicDNS (broken `/\.ts\.net$/` regex due to Rails sanitization)
- Added environment-agnostic `allowed_hosts.rb` initializers (WUT, Wv2, DM)
- Fixed subpath URL generation: `RAILS_RELATIVE_URL_ROOT=/wut` + `TailscaleScriptName` middleware (Serve strips prefix upstream)
- Restored mobile CSS/JS (assets now prefixed `/wut/assets/...`)
- Updated root `compose.yml` with `TAILSCALE_HOSTNAME`, `RAILS_RELATIVE_URL_ROOT`, `TAILSCALE_SERVE_PATH` for WUT (and hostname for DM/Wv2)

---

## 3. Code Delivered

### Files changed

| File | Repo | Change | Notes |
|------|------|--------|-------|
| `winston_unit_test/config/initializers/allowed_hosts.rb` | WUT | added | Compose + Tailscale hosts; ActionCable origins |
| `winston_unit_test/config/initializers/relative_url_root.rb` | WUT | added | Subpath + ActionCable `/wut/cable` |
| `winston_unit_test/lib/tailscale_script_name.rb` | WUT | added | Sets `Rack::SCRIPT_NAME` for URL helpers |
| `winston_unit_test/config/environments/development.rb` | WUT | modified | Host rules moved to initializer |
| `data_manager/config/initializers/allowed_hosts.rb` | DM | added | Same Tailscale patterns (future `/dm` serve) |
| `data_manager/config/environments/development.rb` | DM | modified | Host rules moved to initializer |
| `winston_v2/config/initializers/allowed_hosts.rb` | Wv2 | added | Already on main from prior commit |
| `compose.yml` | _(workspace root, unversioned)_ | modified | WUT subpath env vars — **not in any git repo** |

### Commits

- `ee23c3b` (winston_unit_test) — Enable WUT access via Tailscale Serve at /wut subpath
- `d9ff97e` (data_manager) — Add deployment-agnostic Tailscale host authorization initializer
- `028fd08` (ecosystem) — Add session report: WUT Tailscale Serve mobile access

### Branch / PR state at sign-off

- `winston_unit_test` main — clean, pushed
- `data_manager` main — clean for session files (other local changes remain unstaged)
- `ecosystem` main — clean for session report, pushed
- PR: not opened

---

## 4. Decisions Made

### Decision 1: Host auth via initializers (all environments)
- **Choice:** `config/initializers/allowed_hosts.rb` per monolith, not `development.rb` only
- **Why:** Production would block Tailscale hosts; same compose/Tailscale patterns apply everywhere
- **Alternatives considered:** `development.rb` only (rejected — not deployment-agnostic)
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 2: MagicDNS regex `/.*\.ts\.net/` not `".ts.net"` or `/\.ts\.net$/`
- **Choice:** Regex matching full hostname suffix
- **Why:** Rails wraps regexes with `\A...\z`; `$`-anchored patterns fail; string `".ts.net"` only allows one DNS label
- **Alternatives considered:** Per-machine hostname strings (rejected — not portable)
- **Reversibility:** easy
- **Promote to ADR?** no — note in initializer comment

### Decision 3: Subpath via env + SCRIPT_NAME middleware
- **Choice:** `RAILS_RELATIVE_URL_ROOT=/wut` + `TailscaleScriptName` middleware
- **Why:** Tailscale Serve strips `/wut` before proxying; Rails saw `/data_sets` but generated `/data_sets` links → 404; assets needed prefix too
- **Alternatives considered:** Serve at root port 3000 (rejected — user wants `/wut` path); `RAILS_RELATIVE_URL_ROOT` alone (insufficient for link helpers)
- **Reversibility:** easy — unset env on nodes not using path serve
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- Tailscale Serve `--set-path=/wut` **strips** the public prefix on the upstream request (`/wut/foo` → `http://127.0.0.1:3000/foo`)
- Rails `HostAuthorization` silently breaks common Tailscale regex patterns — always test with `Permissions.new(config.hosts).allows?(hostname)`
- Broken asset paths explain “unstyled mobile” — same subpath bug as nav links
- Root `compose.yml` lives outside any git repo; env changes need manual discipline or future orchestration repo

---

## 6. Issues & Tickets

### Resolved this session
- WUT 403 via MagicDNS / Tailscale Serve — host auth initializer
- Nav 404 after home page — `TailscaleScriptName` + `RAILS_RELATIVE_URL_ROOT`
- Mobile styling broken — asset prefix fixed by same subpath config

### Deferred
- `compose.yml` not versioned at workspace root — consider ticket to track in ecosystem or meta-repo
- DM container needs **rebuild** to pick up `allowed_hosts.rb` (no bind mount on `data_manager`)
- Future `tailscale serve --set-path=/wv2` and `/dm` — initializers ready; compose env + subpath middleware pattern is WUT-only today
- `winston_mcp` / `nanobot_cromwell` containers were removed during WUT recreate — operator may need `./bin/compose --profile ai up -d`

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| WUT home via Serve | `curl -sk https://sawtooth-ai.tail944ffb.ts.net/wut/` | ✅ 200 |
| Nav links prefixed | grep `href="/wut/data_sets"` on home HTML | ✅ |
| Subpages via Serve | `curl -sk .../wut/data_sets`, `/wut/portfolios` | ✅ 200 |
| Assets prefixed | `href="/wut/assets/..."` + CSS 200 | ✅ |
| ActionCable meta | `content="/wut/cable"` | ✅ |
| Internal API (compose) | `curl http://127.0.0.1:3000/internal/active_markets` | ✅ 200 |
| User confirmation | Phone browsing + mobile styling | ✅ reported |

**Test command(s):**
```bash
curl -sk -o /dev/null -w "%{http_code}" https://sawtooth-ai.tail944ffb.ts.net/wut/
curl -sk https://sawtooth-ai.tail944ffb.ts.net/wut/ | grep -o 'href="/wut/data_sets"'
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:3000/internal/active_markets
tailscale serve status
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None added
- **Services:** `winston_unit_test` recreated with new env; `winston_unit_test_sidekiq` restarted; AI profile containers (`winston_mcp`, `nanobot_cromwell`) may need restart
- **Migrations:** None
- **Tailscale Serve (user-run):** `tailscale serve --bg --set-path=/wut http://127.0.0.1:3000`
- **Compose env (WUT):** `TAILSCALE_HOSTNAME=sawtooth-ai`, `RAILS_RELATIVE_URL_ROOT=/wut`, `TAILSCALE_SERVE_PATH=/wut`

---

## 9. Risks & Technical Debt

- WUT with subpath env generates `/wut/...` links even on direct `localhost:3000` — intentional for this node; unset env for local-only dev
- `compose.yml` changes not in git — risk of drift across machines
- DM host-auth initializer not live until image rebuild
- Podman compose recreate friction (dependent containers) — used `podman rm --depend` workaround

---

## 10. Open Questions

- **Should root `compose.yml` move into a versioned repo?** — needs answer from: operator; blocks: reproducible Tailscale deploys on other nodes

---

## 11. Handoff & Resume Notes

- **Where I left off:** User confirmed fix works (nav + mobile styling). `/wrap` requested.
- **Next concrete step:** If using Cromwell AI profile: `./bin/compose --profile ai up -d`. If serving Wv2/DM via Tailscale: mirror WUT pattern (`serve` + env + optional middleware).
- **Files to read first:**
  1. `winston_unit_test/config/initializers/relative_url_root.rb`
  2. `winston_unit_test/config/initializers/allowed_hosts.rb`
  3. Root `compose.yml` (WUT env block)
  4. `tailscale serve status` on host

**Phone URL:** `https://sawtooth-ai.tail944ffb.ts.net/wut/`

---

## 12. Stakeholder Communications

- _None required — infrastructure/access improvement for operator mobile use._

---

## 13. Tools & Workflow Notes

- **Skills used:** session-report, wrap
- **What worked well:** Systematic diagnosis of HostAuthorization regex sanitization; curl-based verification of Serve path stripping
- **Friction points:** Podman compose recreate with dependent containers; root compose.yml unversioned
- **Subagent usage:** None

---

## 14. Follow-up Actions

- [ ] Rebuild `data_manager` image after pulling DM initializer commit — owner: operator
- [ ] Restart AI profile if needed: `./bin/compose --profile ai up -d` — owner: operator
- [ ] Version root `compose.yml` or document Tailscale env in `ecosystem/deployment/` — owner: operator

---

## 15. Appendix

**Tailscale node:**
```
100.121.176.51  sawtooth-ai  (MagicDNS: sawtooth-ai.tail944ffb.ts.net)
```

**Serve status:**
```
https://sawtooth-ai.tail944ffb.ts.net (tailnet only)
|-- /wut proxy http://127.0.0.1:3000
```

**Rails host-auth gotcha (actionpack `HostAuthorization::Permissions#sanitize_regexp`):**
```ruby
/\A#{host}#{PORT_REGEX}?\z/   # user regex is wrapped — /\.ts\.net$/ does NOT match FQDNs
```