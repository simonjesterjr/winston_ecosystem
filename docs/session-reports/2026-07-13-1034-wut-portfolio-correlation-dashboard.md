# Session Report — WUT Portfolio Correlation Dashboard + Primer/Deep Dives

**Date:** 2026-07-13  
**Time:** ~09:30–10:34 MDT  
**Duration:** ~1h  
**Project:** sawtooth / winston_unit_test + ecosystem  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `main` (WUT and ecosystem)  
**Model:** Grok (xAI)  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Build the correlation heatmap on the portfolios page (WUT PF Correlation dashboard).

**Follow-on goal (same session):** Navigational return to PF Correlation from heatmap; methodology primer sidebar (not tooltips); curated AI deep dives per color portfolio (not live LLM).

**Outcome:** Delivered

**One-line summary:** WUT now has a portfolio-centric correlation dashboard (rankings, heatmaps, PCS history), sticky methodology primer, breadcrumb back-nav, and curated deep-dive analyses for all eight color cohorts.

---

## 2. Work Completed

- Implemented `GET /portfolios/correlation` ranking dashboard (PCS table, flags, multi-series Plotly chart).
- Implemented `GET /portfolios/:id/correlation` live Books heatmap + matrix + transparency strip + optional manual refresh.
- Wired nav: sidebar “PF Correlation”, Portfolios index/show links, dual-threshold matrix reuse.
- Added sticky methodology primer (Max |r|, Mean |r|, Δ PCS, Rating, seed, trading impact).
- Added curated deep-dive YAML for Green/Pink/Blank/Rust/Red/Blue/Orange/White.
- Breadcrumb + prominent “Back to PF Correlation” on heatmap pages.
- Marked ticket + plan Phase 8 checkbox done.
- Specs for dashboard ranking/flags/empty book + deep dive loader + controller render paths.

---

## 3. Code Delivered

### Files changed

#### winston_unit_test

| File | Change | Notes |
|------|--------|-------|
| `app/services/portfolio_correlation_dashboard.rb` | added | Ranking, flags, history, detail, refresh |
| `app/services/portfolio_correlation_deep_dive.rb` | added | Primer + curated YAML loader |
| `app/controllers/portfolios/correlations_controller.rb` | added | index / show / refresh |
| `app/views/portfolios/correlations/*` | added | index, show, breadcrumb, primer, deep_dive |
| `config/correlation_deep_dives/primer.yml` | added | Methodology primer content |
| `config/correlation_deep_dives/{green,orange,white,red,blue,pink,blank,rust}.yml` | added | Curated deep dives |
| `config/routes.rb` | modified | collection/member correlation routes |
| `app/views/layouts/application.html.erb` | modified | PF Correlation nav item |
| `app/views/portfolios/index.html.erb` | modified | Dashboard + per-row Correlation link |
| `app/views/portfolios/show.html.erb` | modified | Correlation heatmap button |
| `spec/services/portfolio_correlation_dashboard_spec.rb` | added | Ranking / flags / empty / rating |
| `spec/services/portfolio_correlation_deep_dive_spec.rb` | added | Primer + Orange deep dive |
| `spec/controllers/portfolios/correlations_controller_spec.rb` | added | Index/show + back-nav + deep dive |

#### ecosystem

| File | Change | Notes |
|------|--------|-------|
| `docs/tickets/2026-07-12-wut-portfolio-correlation-dashboard.md` | modified | Status Done + acceptance checks + impl notes |
| `plans/portfolio-correlation-methodology-and-score.md` | modified | Phase 8 dashboard checkbox done |
| `docs/session-reports/2026-07-13-1034-wut-portfolio-correlation-dashboard.md` | added | This report |

### Commits

- _Pending wrap commit (this step)._

### Branch / PR state at sign-off

- Branch: `main` (WUT) — dirty until wrap commit  
- Branch: `main` (ecosystem) — dirty until wrap commit  
- Pushed: pending wrap  
- PR: not opened (direct `main`)

---

## 4. Decisions Made

### Decision 1: Dashboard under Portfolios, not a new top-level tool
- **Choice:** Routes under `/portfolios/correlation` and `/portfolios/:id/correlation`
- **Why:** Matches filed design; keeps Builder for assembly, dashboard for monitoring
- **Alternatives considered:** Actions only on `PortfoliosController`; separate top-level app
- **Reversibility:** easy
- **Promote to ADR?** no (implements ADR-007 UI surface)

### Decision 2: Deep dives are curated YAML, not live MCP/LLM
- **Choice:** Pre-authored `config/correlation_deep_dives/*.yml` labeled “AI deep dive · curated”
- **Why:** Operator asked for MCP-style insight without requiring live inference; content stable for Orange seed/theme narrative
- **Alternatives considered:** Live Cromwell MCP tool call on page load
- **Reversibility:** easy (swap loader for MCP later)
- **Promote to ADR?** no

### Decision 3: Methodology primer is sticky sidebar text, not tooltips
- **Choice:** Full primer partial on index + show
- **Why:** Foundational concepts (Max |r|, Mean |r|, Δ PCS) should be always visible
- **Alternatives considered:** Hover titles only
- **Reversibility:** easy

---

## 5. Insights Surfaced

- Live PCS ranking (2026-07-12 snapshots): Green ~83 Strong → Rust/Pink/Blue mid-70s Strong → Red ~73 → Blank ~71 → Orange ~68 **Good** → White ~42 **Weak**.
- Orange sidecar still says “strong” from mean-first era; live corr_v2 rating is **Good** because max |r| ~0.57 exceeds 0.55 build cap — deep dive documents this explicitly.
- White remains the twin case (DBE/OILK); primer’s max-|r|-first story is validated by live data.

---

## 6. Issues & Tickets

### Resolved this session
- Ticket `docs/tickets/2026-07-12-wut-portfolio-correlation-dashboard.md` — **Done**
- Plan Phase 8 dashboard checkbox — **Done**

### Deferred
- Live MCP “analyze portfolio PCS” tool — **ticket:** [`2026-07-13-pcs-deep-dive-mcp-tool.md`](../tickets/2026-07-13-pcs-deep-dive-mcp-tool.md)
- Re-curate deep-dive YAML when membership/PCS methodology changes — **ticket:** [`2026-07-13-correlation-deep-dive-yaml-refresh.md`](../tickets/2026-07-13-correlation-deep-dive-yaml-refresh.md)
- Orange/White membership rebuild still out of scope (archived stance unchanged)
- Blank/Rust trade-ready re-vet — **already tracked:** `2026-07-12-re-vet-blank-rust-trade-ready.md` (skipped new ticket)
- PCS business-context doc — **already tracked:** `2026-07-12-pcs-business-context-doc.md` (skipped new ticket)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Dashboard service specs | rspec | ✅ 9 then expanded set green |
| Deep dive + controller specs | rspec | ✅ 7 examples, 0 failures |
| Routes | `rails routes -g correlation` | ✅ |
| Live HTTP index | curl `/wut/portfolios/correlation` | ✅ 200, rankings + primer |
| Live HTTP Orange heatmap | curl `/wut/portfolios/35/correlation` | ✅ back-nav, primer, AI deep dive, GLTR |

**Test command(s):**

```bash
./bin/compose exec -T winston_unit_test bundle exec rspec \
  spec/services/portfolio_correlation_dashboard_spec.rb \
  spec/services/portfolio_correlation_deep_dive_spec.rb \
  spec/controllers/portfolios/correlations_controller_spec.rb
```

Note: rspec still prints a non-fatal `db:test:load` connection warning to localhost:5432; examples run and pass against the compose DB.

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new (Plotly CDN already used for heatmaps)
- **Services:** `winston_unit_test` on host :3000 (`/wut` relative root)
- **Migrations:** None (reuses `portfolio_correlation_snapshots`)

---

## 9. Risks & Technical Debt

- Deep-dive PCS numbers are **reference** as-of dates; live strip may diverge after daily score — pages note this.
- Sidecar diversification labels can disagree with live rating (Orange); operators should trust live dashboard + deep-dive narrative.
- `db:test:load` host-postgres noise in container rspec remains pre-existing friction.

---

## 10. Open Questions

- **Should curated deep dives be promoted into Cromwell MCP as read-only tools?** — needs product call; blocks: optional MCP skill wiring only
- **When to re-author deep dives after next membership rebuild?** — after any corr_v2 rebuild or methodology_version bump

---

## 11. Handoff & Resume Notes

- **Where I left off:** UI feature complete; wrap in progress (report written; commit/push pending).
- **Next concrete step:** Commit + push WUT and ecosystem; optional follow-up tickets for live MCP deep dive or deep-dive refresh process.
- **Files to read first:**
  1. `winston_unit_test/app/services/portfolio_correlation_dashboard.rb`
  2. `winston_unit_test/app/controllers/portfolios/correlations_controller.rb`
  3. `winston_unit_test/config/correlation_deep_dives/primer.yml` + `orange.yml`
  4. `ecosystem/docs/tickets/2026-07-12-wut-portfolio-correlation-dashboard.md`

**Operator URLs (local):**
- Ranking: `http://localhost:3000/wut/portfolios/correlation`
- Example heatmap: `http://localhost:3000/wut/portfolios/63/correlation` (Green) or `…/35/correlation` (Orange)

---

## 12. Stakeholder Communications

- _None required._ Optional: note to operators that PF Correlation is the lab home for PCS heatmaps and that deep dives are curated narratives, not live model output.

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report (this file)
- **What worked well:** Reusing Phase 3 heatmap/matrix/transparency strip; design ticket already specified routes.
- **Friction points:** Controller `assigns` gem missing (used `render_views` + body assertions); multi-repo wrap (WUT + ecosystem).
- **Subagent usage:** _None._

---

## 14. Follow-up Actions

- [ ] Optional: live MCP tool for portfolio PCS deep dive — **ticket:** [`docs/tickets/2026-07-13-pcs-deep-dive-mcp-tool.md`](../tickets/2026-07-13-pcs-deep-dive-mcp-tool.md)  
- [ ] Re-author deep-dive YAML after membership/methodology changes — **ticket:** [`docs/tickets/2026-07-13-correlation-deep-dive-yaml-refresh.md`](../tickets/2026-07-13-correlation-deep-dive-yaml-refresh.md)  
- [ ] Continue open tickets (no new file): PCS business-context doc; Blank/Rust trade-ready re-vet  

---

## 15. Appendix (optional)

### Routes added

```
GET  /portfolios/correlation              → portfolios/correlations#index
GET  /portfolios/:id/correlation          → portfolios/correlations#show
POST /portfolios/:id/refresh_correlation  → portfolios/correlations#refresh
```

### Live ranking snapshot (session)

| Portfolio | Seed | PCS ≈ | Rating |
|-----------|------|-------|--------|
| Green | ICLN | 83.4 | Strong |
| Rust | XLI | 77.3 | Strong |
| Pink | PINK | 76.3 | Strong |
| Blue | TSMC | 76.2 | Strong |
| Red | AMAT | 73.0 | Strong |
| Blank | ZROZ | 71.3 | Strong |
| Orange | GLTR | 68.3 | Good |
| White | CPER | 41.8 | Weak |
