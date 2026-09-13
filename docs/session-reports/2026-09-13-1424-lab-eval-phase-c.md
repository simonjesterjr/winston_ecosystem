# Session Report — Lab eval Phase C (Shell hop)

**Date:** 2026-09-13
**Time:** 14:09–14:24 MDT
**Duration:** ~15m wall
**Project:** Sawtooth / Winston ecosystem
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `ecosystem` `main` (dirty); `winston_unit_test` `main` (dirty, unchanged this slice). Sawtooth root is not a git repo (`bin/lab-eval` lives there).
**Model:** Grok 4.6
**Operator:** John

**Prior reports:**  
[`2026-09-13-1344-lab-eval-plan-and-phase-a.md`](2026-09-13-1344-lab-eval-plan-and-phase-a.md)  
[`2026-09-13-1409-lab-eval-phase-b.md`](2026-09-13-1409-lab-eval-phase-b.md)  
This file is **Phase C only**.

---

## 1. Goal & Outcome

**Stated goal:** Skip §14 tickets from the Phase B report; start Phase C (Shell-on-sawtooth hop) under the general-contractor pattern.

**Outcome:** Delivered.

**One-line summary:** Grok Bot / Chief of Staff can list and get lab cells from a Shell on this host (`./bin/lab-eval` or copy-paste MCP `call_tool`); cloud still cannot reach Winston MCP; execute of PBR #596 remains gated.

---

## 2. Work Completed

- Operator: `skip all` on the 14:09 report follow-ups.
- GC spawned two contractors: runbook; `bin/lab-eval`.
- Runbook: `ecosystem/docs/operations/grok-bot-shell-lab-eval.md` (Shell-only; no Serve `/mcp`; no Funnel).
- Pointers: operations README table; `recreate-winston-mcp.md` Related; companion `strategy77-rst-heat-risk-v1.md`.
- Wrapper: `bin/lab-eval` (`setup`, `list`, `get`, `score`, `create-smoke`, `execute` gated on `--i-mean-it`).
- Live: `list` → cell **#596**; `get 596` → **pending**; `execute 596` **REFUSE** (exit 1).
- Plan C4 marked landed.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/docs/operations/grok-bot-shell-lab-eval.md` | added | Phase C runbook |
| `ecosystem/docs/operations/README.md` | modified | Table row |
| `ecosystem/docs/operations/recreate-winston-mcp.md` | modified | Related link |
| `ecosystem/docs/analysis/strategy77-rst-heat-risk-v1.md` | modified | Pointer to runbook + `bin/lab-eval` |
| `ecosystem/plans/winston-lab-eval-grok-cli.md` | modified | C4 landed |
| `bin/lab-eval` | added | Executable; **sawtooth root — not in git** |

No WUT/MCP Python this slice.

### Commits

- _None._

### Branch / PR state at sign-off

- Branch: `ecosystem` `main` — dirty; `winston_unit_test` `main` — dirty (Phase A/B still uncommitted)
- Pushed: no
- PR: not opened

---

## 4. Decisions Made

### Decision 1: Shell-only remains the hop
- **Choice:** Document Shell-on-sawtooth; do not Serve `/mcp` or Funnel.
- **Why:** Operator lock 2026-09-13; Grok Bot cloud cannot reach compose-internal MCP.
- **Alternatives considered:** Tailscale Serve; Funnel.
- **Reversibility:** easy (docs)
- **Promote to ADR?** no unless Funnel is later chosen

### Decision 2: `execute` requires `--i-mean-it`
- **Choice:** `bin/lab-eval execute` exits 1 without the flag.
- **Why:** Full-window Turtle PBR is hours of CPU; #596 must not be enqueued by accident.
- **Alternatives considered:** Soft warning then proceed.
- **Reversibility:** easy
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- Preferred MCP hop from Shell is `podman exec winston_mcp python3` + `call_tool`, not curl SSE (already proven in Phase B).
- `bin/lab-eval` lives at sawtooth root with `bin/compose`; that tree is **not a git repo** — runbook in `ecosystem/` is the durable SOT; the wrapper can vanish on a clean clone unless copied elsewhere.
- `create-smoke` resolves portfolio `"Mint"` via WUT ILIKE (works for Portfolio Mint).

---

## 6. Issues & Tickets

### Resolved this session
- _None filed._ Operator skipped tickets again.

### Deferred
- Phase D: Grok Bot Lab Sweep / Edge Scorecard briefs.
- UAT `FULL=1` 32-cell panel.
- Optional execute of PBR #596.
- `/wrap` Graphify + commit lab-eval paths.
- Home for `bin/lab-eval` in a git repo.
- `wut_get_trades` / Wave 3–4.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| `bin/lab-eval list` | live MCP | ✅ 1 cell, PBR **#596** |
| `bin/lab-eval get 596` | live MCP | ✅ pending `mint_rst_turtle_r01` |
| `bin/lab-eval execute 596` | no flag | ✅ REFUSE, exit 1 |
| Execute with `--i-mean-it` | — | ⚠️ **not run** |
| `FULL=1` setup | — | ⚠️ **not run** |
| Graphify Graph | — | ⚠️ pending wrap (stamps 12:45 MDT) |

**Test command(s):**

```bash
./bin/lab-eval list
./bin/lab-eval get 596
./bin/lab-eval execute 596   # expect REFUSE
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None.
- **Services:** Used existing `winston_mcp` + `winston_unit_test`. No recreate this slice.
- **Migrations:** None. Lab DB: PBR **#596** still pending.

---

## 9. Risks & Technical Debt

- `bin/lab-eval` not versioned (sawtooth root).
- Accidental `--i-mean-it` on #596 still hours of Sidekiq.
- Lab-eval still uncommitted across ecosystem + WUT + compose.yml.

---

## 10. Open Questions

- **Start Phase D (Grok Bot briefs)?** — operator.
- **Commit/wrap before D?** — operator; Graphify still stale.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Phase C accepted. Shell hop works. Phase D not started. `/session-report` only (not `/wrap`).
- **Next concrete step:** Phase D — Lab Sweep + Edge Scorecard briefs pointing at the runbook + MCP v0.5. Do **not** `FULL=1` until UAT.
- **Files to read first:**
  1. `ecosystem/docs/operations/grok-bot-shell-lab-eval.md`
  2. `ecosystem/plans/winston-lab-eval-grok-cli.md` (C4 landed)
  3. `ecosystem/interfaces/winston-mcp-tools.md` v0.5
  4. Prior reports 13:44 (A) and 14:09 (B)

---

## 12. Stakeholder Communications

- _None._

---

## 13. Tools & Workflow Notes

- **Skills used:** session-report. GC + two contractors.
- **Graphify Graph:** **pending wrap.**
- **Ponytail flags:** none.
- **What worked well:** Disjoint ownership (runbook vs `bin/`). Execute gate verified immediately.
- **Friction points:** Wrapper cannot live in `ecosystem` git without a second copy or a new home.
- **Subagent usage:** `Phase C Shell runbook`; `bin/lab-eval wrapper`. GC tightened execute example, README smoke-script list, plan C4, companion pointer; re-ran list/get/execute-refuse.

---

## 14. Follow-up Actions

- [ ] Phase D Grok Bot briefs — owner: operator + Grok CLI — due: when operator starts D
- [ ] Optional execute PBR #596 — owner: operator — due: not a D gate
- [ ] `/wrap` Graphify + commit — owner: operator + agent — due: unset
- [ ] Version `bin/lab-eval` — owner: operator — due: unset

---

## 15. Appendix

**Wrapper:** `/home/johnkoisch/Documents/com/sawtooth/bin/lab-eval`  
**Auth:** `lab_geometry_report_only`  
**Do not:** Funnel; Serve `/mcp`; Cromwell cron execute; `FULL=1` except UAT.
