# Session Report — WEV Code plane Completed tab

**Date:** 2026-09-09
**Time:** ~18:00–18:08 MDT
**Duration:** ~10m
**Project:** sawtooth Winston ecosystem — `winston_v2`, `ecosystem/`
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on each touched repo (from `origin/main`)
**Model:** Grok 4.6
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** On Winston Ecosystem View (WEV) Code plane (`/wv2/operations/ecosystem`), add a **Completed** tab and rename **tickets / issues** to **open tickets / issues**.

**Outcome:** Delivered. Live Tailscale and local `:3002` already serve the four-tab strip (bind-mounted). Request spec updated and passing in compose.

**One-line summary:** Code plane now splits tickets and issues into open vs completed instead of dumping Done rows into one backlog tab.

---

## 2. Work Completed

- Renamed Code work tab `tickets / issues` → `open tickets / issues`.
- Added `Completed` tab (`data-kind="completed"`) between open tickets and plans.
- Client filter: tickets/issues whose status starts with Done / Completed / Closed / Resolved / Fixed / Superseded / Won't fix, plus any path under `docs/tickets/archive/`. `Partially fixed` stays open.
- Status fallback reads YAML `status:` and `**Status banner:**` from the catalog body when the indexed `status` field is empty (issues that only have frontmatter).
- Cache-bust `wev-live.js?v=20260909r`.
- Updated visual-QA ticket DoD to four sub-tabs.

---

## 3. Code Delivered

### Files changed (this session only — do not stage the rest of the dirty trees)

#### winston_v2

| File | Change | Notes |
|------|--------|-------|
| `app/views/operations/ecosystem/show.html.erb` | modified | four work tabs; JS cache-bust `20260909r` |
| `public/ecosystem/wev-live.js` | modified | `isCompletedWork` / `workStatus`; counts; kind column on Completed |
| `spec/requests/operations_ecosystem_spec.rb` | modified | asserts open label + `data-kind="completed"` |

**Do not stage:** Quiver Tracking / Fulfillment Desk / ops-shell / `db/schema.rb` / other dirty Wv2 files.

#### ecosystem

| File | Change | Notes |
|------|--------|-------|
| `docs/tickets/2026-09-09-wev-code-plane-visual-qa.md` | modified | four tabs; cache-bust `20260909r` |
| `docs/tickets/2026-09-09-wev-index-work-yaml-status.md` | added | wrap promotion |
| `docs/tickets/2026-09-09-wev-index-work-archive-tickets.md` | added | wrap promotion |
| `docs/tickets/2026-09-09-wev-index-work-refresh-hook.md` | modified | cross-link the two new tickets |
| `docs/tickets/INDEX.md` | modified | two P3 rows only — do not stage the extra-modal leap line |
| `docs/session-reports/2026-09-09-1808-wev-code-completed-tab.md` | added | this report |

**Do not stage:** `AGENTS.md`, `CONTEXT.md`, `docs/README.md`, unrelated tickets, `hints/`, `plans/cromwell-staff-roster.md`, `vendor/`.

### Commits

- `winston_v2` `39f22a1` — feat(wev): Code plane open vs Completed work tabs
- `ecosystem` — this wrap commit (docs + tickets)

### Branch / PR state at sign-off

- Branch: `main` (both repos)
- Pushed: pending this wrap
- PR: not opened (direct `main`, matching recent WEV wraps)

---

## 4. Decisions Made

### Decision 1: Classify Completed in the browser, not by regenerating `work.json`
- **Choice:** `isCompletedWork()` in `wev-live.js` over status + `/archive/` path; YAML/`Status banner` fallback from `body`.
- **Why:** `index_work` + `work.json` regen is a ~1.1 MB tracked blob; INDEX already lists many Done tickets. Operator asked for a tab, not a catalog rewrite.
- **Alternatives considered:** re-run `index_work` and walk all `tickets/archive/*.md`; add a `closed` boolean to the catalog.
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 2: "Scored" lab tickets stay on Open
- **Choice:** only INDEX-style Done / Completed / Superseded (plus Fixed / Closed / Resolved / Won't fix).
- **Why:** `docs/tickets/INDEX.md` and `archive/README.md` name those three as the archive statuses. "Scored — keep …" is a lab conclusion still sitting in the active index.
- **Alternatives considered:** treat Scored as Completed.
- **Reversibility:** easy (one regex)
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- INDEX still lists dozens of **Done** tickets in the active table; the Code tab was mixing them with Proposed / In progress. The Completed tab is a UI split, not INDEX hygiene.
- Nine ecosystem issues have empty catalog `status` because `index_work` only reads `**Status:**`, not YAML `status:` or `**Status banner:**`. Body fallback covers classification without a catalog regen.
- ~84 `tickets/archive/` files are **not** in INDEX and therefore not in `work.json`. Completed shows INDEX-listed Done/archive rows, not the full archive directory.

---

## 6. Issues & Tickets

### Resolved this session
- Operator request: Code plane open vs completed split.

### Deferred
- Operator visual QA of Code plane (click cuboids + four tabs) — already [`docs/tickets/2026-09-09-wev-code-plane-visual-qa.md`](../tickets/2026-09-09-wev-code-plane-visual-qa.md)
- Optionally teach `index_work` YAML / Status-banner status so catalog `status` is filled (JS fallback already classifies) — [`docs/tickets/2026-09-09-wev-index-work-yaml-status.md`](../tickets/2026-09-09-wev-index-work-yaml-status.md)
- Optionally index remaining `tickets/archive/*.md` not listed in INDEX (grows `work.json`) — [`docs/tickets/2026-09-09-wev-index-work-archive-tickets.md`](../tickets/2026-09-09-wev-index-work-archive-tickets.md)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Request spec | compose `rspec spec/requests/operations_ecosystem_spec.rb` | ✅ 5 examples, 0 failures |
| Live HTML (local `:3002`) | `curl` — four tabs + `wev-live.js?v=20260909r` | ✅ 200 |
| Live HTML (Tailscale `/wv2`) | `curl` same markup | ✅ 200 |
| Live JS | `curl /wv2/ecosystem/wev-live.js?v=20260909r` contains `isCompletedWork` | ✅ 200 |
| Classifier vs `work.json` | Python replica of JS rules | ✅ 0 false-closed, 0 missed Done/Fixed; ecosystem cuboid ~97 open / ~12 completed |
| Browser click-through | no browser MCP this session | ⚠️ operator visual QA still open |

**Test command(s):**

```bash
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 \
  bundle exec rspec spec/requests/operations_ecosystem_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None
- **Services:** existing compose `winston_v2` (bind-mount served the ERB/JS without rebuild)
- **Migrations:** None

---

## 9. Risks & Technical Debt

- Status heuristic is string-prefix, not a closed enum. A future "Done enough to start" Proposed ticket could be misfiled; current INDEX rows were checked (0 false-closed).
- Completed is not the full archive; archive-only files stay invisible until INDEX or `index_work` includes them.

---

## 10. Open Questions

- **Should "Scored — keep …" lab tickets move to Completed?** — operator; does not block this tab.
- **Should INDEX hygiene move Done rows into `archive/`?** — operator; separate from the UI split.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Code tabs live on Tailscale; wrap commit not yet made.
- **Next concrete step:** hard-refresh Code plane, click **open tickets / issues** then **Completed**, then `/wrap` commit of the four session files (plus this report).
- **Files to read first:**
  1. `winston_v2/public/ecosystem/wev-live.js` (`KIND_LABEL` / `isCompletedWork`)
  2. `winston_v2/app/views/operations/ecosystem/show.html.erb` (`#wev-work-tabs`)
  3. `ecosystem/docs/tickets/2026-09-09-wev-code-plane-visual-qa.md`

Pages: `http://127.0.0.1:3002/operations/ecosystem` and `https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/ecosystem`. Cache-bust `?v=20260909r`.

---

## 12. Stakeholder Communications

- _None._ Operator-facing console only.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, session-report, wrap
- **What worked well:** bind-mount meant Tailscale picked up ERB/JS without compose rebuild; classifier dry-run against `work.json` caught the "planning done" false-positive before shipping a substring match.
- **Friction points:** host `rspec` cannot reach Wv2 Postgres (need compose `TEST_DB_HOST=wv2_postgres`); no `node` / `rg` on PATH; no browser MCP.
- **Subagent usage:** none

---

## 14. Follow-up Actions

Already filed (do not duplicate):

- [ ] Operator visual QA of Code plane — [`docs/tickets/2026-09-09-wev-code-plane-visual-qa.md`](../tickets/2026-09-09-wev-code-plane-visual-qa.md)
- [ ] Tighten `index_work` owner heuristic — [`docs/tickets/2026-09-09-wev-index-work-owner-heuristic.md`](../tickets/2026-09-09-wev-index-work-owner-heuristic.md)
- [ ] Re-run `index_work` when docs change — [`docs/tickets/2026-09-09-wev-index-work-refresh-hook.md`](../tickets/2026-09-09-wev-index-work-refresh-hook.md)
- [ ] Optional split work.json index vs bodies — [`docs/tickets/2026-09-09-wev-work-json-split-bodies.md`](../tickets/2026-09-09-wev-work-json-split-bodies.md)

Filed 2026-09-09 (wrap promotion):

- [ ] Parse YAML / Status-banner into catalog `status` — [`docs/tickets/2026-09-09-wev-index-work-yaml-status.md`](../tickets/2026-09-09-wev-index-work-yaml-status.md)
- [ ] Index archive tickets not listed in INDEX — [`docs/tickets/2026-09-09-wev-index-work-archive-tickets.md`](../tickets/2026-09-09-wev-index-work-archive-tickets.md)

---

## 15. Appendix

- Cache-bust: `wev-live.js?v=20260909r`
- Classifier sample (ecosystem cuboid): adr 6, open 97, completed 12, plans 1
- Live URLs returned 200 with `data-kind="completed"` in HTML
