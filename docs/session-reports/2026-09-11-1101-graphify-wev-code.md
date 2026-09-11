# Session Report — Graphify Graph + WEV Code tab

**Date:** 2026-09-11
**Time:** ~16:48–11:01 MDT (spans 2026-09-10 evening into 2026-09-11)
**Duration:** ~18h wall / one long session
**Project:** sawtooth (ecosystem + winston_v2 + skill mirrors)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` in each touched git repo (workspace root is not a git repo)
**Model:** Grok 4.6
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Build Graphify maps of the estate; encode Graphify-first + Ponytail as contractor law; put Graphify visuals on Winston Ecosystem View (WEV) Code tab (rename old Code → Monoliths).

**Outcome:** Delivered

**One-line summary:** Estate and per-monolith Graphify graphs exist; ADR-014 + `/graphify-ponytail` + `/wrap` refresh; WEV Code tab is the vis-network map (estate first, drill into monoliths).

---

## 2. Work Completed

- Ran Graphify extract per monolith (Rails `--code-only`; ecosystem + `ai/` semantic) and merged a workspace graph.
- **ADR-014:** Graphify-first traversal; Ponytail to collapse copies. Glossary terms **Graphify Graph** vs **Work Graph**.
- Skill `graphify-ponytail` mirrored to workspace, ecosystem, Data Manager (DM), Winston Unit Test (WUT), Winston v2 (Wv2), Broker Gateway (BG).
- Hooks: `lightweight-bug-fix` impact map, `investigate-system-variance` path, `rails-code-review` Phase 0, `/wrap` step 2 graph refresh, session-report §13 lines.
- WEV: tab **Code** → **Monoliths**; new **Code** tab = Graphify vis-network. `GET /operations/ecosystem/graphify`. Compose mounts `graphify-out/` into `winston_v2` as `GRAPHIFY_ROOT=/sawtooth`.

---

## 3. Code Delivered

### Files changed (this session only — other dirty trees left alone)

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/docs/adr/ADR-014-graphify-first-ponytail-harmonize.md` | added | Contractor decision |
| `ecosystem/CONTEXT.md` | modified | Graphify Graph, Ponytail, WEV tabs |
| `ecosystem/principles/01_core_principles.md` | modified | Principle 14 |
| `ecosystem/AGENTS.md` | modified | Skill table + wrap + ADR-014 |
| `ecosystem/README.md` | modified | Skills list |
| `ecosystem/docs/README.md` | modified | Skills list |
| `ecosystem/interfaces/winston-ecosystem-view-v1.md` | modified | `monoliths` + `code` planes |
| `ecosystem/plans/winston-ecosystem-view.md` | modified | Monoliths vs Code |
| `ecosystem/.grok/skills/graphify-ponytail/SKILL.md` | added | Overlay skill |
| `ecosystem/.grok/skills/wrap/SKILL.md` | modified | Step 2 Graphify refresh |
| `ecosystem/.grok/skills/session-report/SKILL.md` | modified | §13 Graphify / Ponytail |
| `ecosystem/.grok/skills/lightweight-bug-fix/SKILL.md` | modified | Query graph on impact |
| `ecosystem/.grok/skills/investigate-system-variance/SKILL.md` | modified | `graphify path` |
| `AGENTS.md` (workspace, no git) | modified | Session checklist + wrap |
| `WORK_GRAPH.md` (workspace, no git) | modified | Impact stage |
| `compose.yml` (workspace, no git) | modified | Graphify volume mounts + `GRAPHIFY_ROOT` |
| `winston_v2/app/services/graphify_graph.rb` | added | vis JSON from graph.json |
| `winston_v2/app/controllers/operations/ecosystem_controller.rb` | modified | `#graphify` |
| `winston_v2/config/routes.rb` | modified | `operations_ecosystem_graphify` |
| `winston_v2/app/views/operations/ecosystem/show.html.erb` | modified | Monoliths + Code planes |
| `winston_v2/public/ecosystem/wev-graphify.js` | added | vis-network client |
| `winston_v2/public/ecosystem/wev-live.js` | modified | plane `monoliths` / `code` |
| `winston_v2/public/ecosystem/wev-live.css` | modified | graph canvas |
| `winston_v2/spec/services/graphify_graph_spec.rb` | added | |
| `winston_v2/spec/fixtures/graphify/` | added | |
| `winston_v2/spec/requests/operations_ecosystem_spec.rb` | modified | tabs + JSON |
| `{dm,wut,wv2,bg}/.grok/skills/graphify-ponytail/` | added | mirrors |
| `{dm,wut,wv2,bg} AGENTS.md` + wrap/session-report/lbf/rcr | modified | mirrors |

**Not this session (left unstaged):** IBKR Client Portal Gateway (CPGW) keepalive / session-yield; Wv2 fulfillment/WQ desk; WUT ponytail tickets; ecosystem `vendor/`, ADR-013 dirt, other tickets; all `graphify-out/`.

### Commits

- `data_manager` `90b4f88` — docs(skills): Graphify-first wrap and ponytail overlay (ADR-014)
- `winston_unit_test` `41c1595` — docs(skills): Graphify-first wrap and ponytail overlay (ADR-014)
- `winston_v2` `2719548` — feat(wev): Graphify Code tab; rename cuboid catalog to Monoliths
- `broker_gateway` `041c4c5` — docs(skills): Graphify-first wrap and ponytail overlay (ADR-014)
- `ecosystem` — this report (SHA filled at commit)

### Branch / PR state at sign-off

- Branch: `main` in ecosystem, DM, WUT, Wv2, BG
- Workspace root: **no git** (`AGENTS.md`, `WORK_GRAPH.md`, `compose.yml`, `.grok/skills/` persist on disk only)
- Pushed: pending wrap push
- PR: not opened (pushing `main`)

---

## 4. Decisions Made

### Decision 1: Graphify-first + Ponytail (ADR-014)
- **Choice:** Query Graphify Graph, then read cited files, then Ponytail. `/wrap` refreshes graphs.
- **Why:** Grep misses cross-monolith copies; treating the graph as proof is stale/wrong.
- **Alternatives considered:** Grep-first; trust graph.json as runtime.
- **Reversibility:** easy (skills/ADR)
- **Promote to ADR?** Done (ADR-014)

### Decision 2: WEV Code tab is Graphify
- **Choice:** Rename cuboid catalog to **Monoliths**; **Code** = vis-network. Estate (merged) first; drill to per-monolith graphs.
- **Why:** Operator asked; per-monolith graphs differ (Rails AST vs GC docs).
- **Alternatives considered:** iframe 17MB `graph.html`; CodeScene (absent).
- **Reversibility:** easy
- **Promote to ADR?** No — WEV interface + CONTEXT

---

## 5. Insights Surfaced

- Merged Graphify Graph is large (~22k raw nodes at wrap time); WEV aggregates communities and omits thin ones.
- Wv2 compose only bind-mounts `./winston_v2`; Graphify files need `GRAPHIFY_ROOT=/sawtooth` plus per-repo `graphify-out` mounts. Recreate of `winston_v2` is blocked by dependents (`winston_mcp`, `nanobot_cromwell`) until those are stopped.
- Duplicate `Portfolio` / `Market` labels in the merged graph are same name in WUT vs Wv2 (`repo` attribute).
- vis-network is loaded from unpkg CDN.

---

## 6. Issues & Tickets

### Resolved this session
- _None (feature/process, not a defect ticket)._

### Deferred
- Browser click-through of WEV Code tab (curl/JSON only).
- Version workspace-root files (`AGENTS.md`, `WORK_GRAPH.md`, `compose.yml`) — no git at sawtooth root.
- vis-network CDN vs vendored copy if Tailscale clients block unpkg.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| GraphifyGraph + WEV request specs | `bin/compose exec -T winston_v2 bundle exec rspec spec/services/graphify_graph_spec.rb spec/requests/operations_ecosystem_spec.rb` | ✅ 10 examples, 0 failures |
| Graphify JSON (compose) | `GET /operations/ecosystem/graphify?scope=workspace` | ✅ ok, aggregated, catalog all available |
| Graphify JSON DM / Wv2 | same endpoint `scope=data_manager` / `winston_v2` | ✅ |
| WEV HTML | curl Tailscale `/wv2/operations/ecosystem` 200; tabs Monoliths + Code | ✅ |
| WEV Code tab click / double-click drill | browser | ❌ not exercised here |

**Test command(s):** `bin/compose exec -T winston_v2 bundle exec rspec spec/services/graphify_graph_spec.rb spec/requests/operations_ecosystem_spec.rb`

---

## 8. Environment, Dependencies, Data

- **Dependencies:** vis-network 9.1.6 from unpkg (browser); graphify CLI on host
- **Services:** `winston_v2` recreated with Graphify volume mounts; `GRAPHIFY_ROOT=/sawtooth`
- **Migrations:** None this session (BG/Wv2 dirty migrations are other work)

---

## 9. Risks & Technical Debt

- Estate graph ~22k nodes; UI shows ~1.5k community nodes — still heavy on first paint.
- CDN for vis-network can fail offline / locked-down browsers.
- Compose recreate of Wv2 is sticky (MCP/nanobot dependents).
- Workspace-root contractor files are unversioned.

---

## 10. Open Questions

- **Should sawtooth root (`compose.yml`, `AGENTS.md`, `WORK_GRAPH.md`) become a git repo or live only under `ecosystem/`?** — needs operator; blocks durable wrap of those files.
- **Pin `graphify-out/` in git?** ADR-014 says no unless asked.

---

## 11. Handoff & Resume Notes

- **Where I left off:** WEV Code tab live via JSON + vis-network; wrap not yet committed.
- **Next concrete step:** Operator hard-refresh Tailscale WEV, open Code, try Ecosystem → DM/Wv2 chips and double-click a community. Then finish wrap commit after follow-up promotion.
- **Files to read first:** `ecosystem/docs/adr/ADR-014-graphify-first-ponytail-harmonize.md`; `winston_v2/app/services/graphify_graph.rb`; `winston_v2/public/ecosystem/wev-graphify.js`; `ecosystem/.grok/skills/wrap/SKILL.md`

---

## 12. Stakeholder Communications

- _None._ Operator-facing WEV change only.

---

## 13. Tools & Workflow Notes

- **Skills used:** graphify, graphify-ponytail, wrap, session-report, operator-prose
- **Graphify Graph:** updated `graphify update` (AST, `--no-cluster`) on ecosystem (13098n), data_manager (632), winston_unit_test (4613), winston_v2 (4652), broker_gateway (606); re-merged workspace `graphify-out/graph.json` → 23857 nodes, 32270 edges. Not staged.
- **Ponytail flags:** `GraphifyGraph` is new in Wv2 — no prior vis helper on the graph. Did not add a second WEV cuboid renderer; reused vis-network. No extra ATR/load helper.
- **What worked well:** Per-monolith extract then `merge-graphs`; WEV JSON aggregation instead of 17MB iframe.
- **Friction points:** podman-compose cannot recreate `winston_v2` until MCP/nanobot are stopped; Graphify semantic extract was 32 subagents.
- **Subagent usage:** 32 ecosystem semantic chunks + 1 `ai/` chunk (earlier in session).

---

## 14. Follow-up Actions

- [ ] Browser-verify WEV Code tab drill-down — owner: operator — due: next look at the page
- [ ] Decide how to version sawtooth-root `compose.yml` / `AGENTS.md` / `WORK_GRAPH.md` — owner: operator
- [ ] Optional: vendor vis-network instead of unpkg — owner: agent if CDN fails

---

## 15. Appendix (optional)

WEV: https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/ecosystem  
Graphify JSON: `GET /wv2/operations/ecosystem/graphify?scope=workspace` (also `ecosystem`, `data_manager`, `winston_unit_test`, `winston_v2`, `broker_gateway`, `ai`).
