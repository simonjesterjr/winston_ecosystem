# Session Report — Orange WUT 109 transfer / dual-active recovery

**Date:** 2026-07-22
**Time:** ~15:33–16:11 MDT (incident ~21:33–22:00 UTC; wrap 16:11 MDT)
**Duration:** ~40m investigation + ops recovery
**Project:** sawtooth Winston ecosystem (cross-monolith: Cromwell MCP + Wv2)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** ecosystem `main` (session report only); Wv2 operational state only
**Model:** Grok 4.5 (xAI)
**Operator:** John Koisch

---

## 1. Goal & Outcome

**Stated goal:** Diagnose failed Telegram attempt to transfer WUT portfolio/run 109 into Wv2 and activate “Portfolio Orange · 7ea76741”.

**Outcome:** Delivered (investigation + operational recovery + domain clarification)

**One-line summary:** Transfer had already created OP **#308**; activate failed on ADR-006 Active mutex vs engaged **#6**. Force dual-active activated #308; clarified that dual Orange with **different fingerprints** is intentional, while **same fingerprint** is the hard lineage rail.

---

## 2. Work Completed

- Reconstructed Cromwell/Telegram sequence from MCP audit `mcp_audit_20260722.jsonl` and live Wv2 internal APIs.
- Confirmed transfer of `run_id=109` returned HTTP **200** and landed OP **#308** (`wut:portfolio_run:109`, fingerprint `7ea76741…`, capital $10k, inactive).
- Confirmed activate **was** called and returned **422 `active_mutex`** against Active **#6** (same `seed_name` “Portfolio Orange”) — not a missing-arg failure.
- Explained Cromwell empty-response / hallucinated “`id_or_name` required” as agent noise after the real 422.
- Operator chose **force dual-active**; executed `POST /internal/portfolios/activate` with `{"id_or_name":"308","force":true}`.
- Verified Active band includes both #6 and #308 (plus Rust, Mango, Blue).
- Recorded operator domain clarification: dual seed + different fingerprints is fine; same fingerprint duplicate series is the true guard rail.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/docs/session-reports/2026-07-22-1611-orange-109-transfer-activate.md` | added | this report |

No application code, MCP, skills, or schema edits this session.

### Commits

- _Pending wrap commit of this report only._

### Branch / PR state at sign-off

- Branch: ecosystem `main` — report only.
- Pushed: pending wrap.
- PR: not opened.

---

## 4. Decisions Made

### Decision 1: Force dual-active #308 next to #6
- **Choice:** Activate OP **#308** with `force=true`; leave **#6** Active and Engaged.
- **Why:** Operator explicitly chose dual-active experiment over swap/close; #6 has open WMT short + journals; #308 is clean new methodology sample.
- **Alternatives considered:** Deactivate #6 then activate #308; close #6 series; leave #308 inactive.
- **Reversibility:** easy — deactivate either OP via internal/MCP.
- **Promote to ADR?** no (uses existing ADR-006 force path)

### Decision 2: Domain speech — fingerprint is the identity rail, not seed name
- **Choice:** Treat dual “Portfolio Orange” with different fingerprints as normal; hard rail is same fingerprint / same TS identity spawning a second independent open series.
- **Why:** Operator clarified; matches importer lineage (update/adopt/fork by fingerprint) more than Active mutex (seed/books attention).
- **Alternatives considered:** Treat dual Orange as always a problem (incorrect).
- **Reversibility:** n/a (documentation/ops speech)
- **Promote to ADR?** no — already in ADR-006 lineage; optional skill/docs clarity if Cromwell keeps confusing mutex with “duplicate”

---

## 5. Insights Surfaced

- **Transfer succeeded; activate failed for a real reason.** MCP audit: transfer 200 in ~189ms; activate 422 `active_mutex` with conflict `#6` / `same_seed_name`.
- **Cromwell still misreports tool failures.** Empty turns + retries produced user-facing “missing `id_or_name`” after activate had already been called with a valid name.
- **#6 vs #308 are different methodologies**, not clones:
  - #6: fingerprint `6622b2eb` — Breakout **5Day** — engaged, capital ~$6144, open WMT short
  - #308: fingerprint `7ea76741` — Breakout **20Day** + Volatility Exit — fresh $10k paper, no journals
- **Active mutex ≠ lineage uniqueness.** Mutex = attention (one Active per seed_name / identical Books unless force). Lineage hard rail = fingerprint merge/update, not “Orange may only exist once.”
- **Capital Activation exception:** paper + real can share the same fingerprint as separate capital spines — do not oversimplify as “never two OPs with same fingerprint.”
- Prefer numeric **`#308`** in ops speech; short fingerprint alone is ambiguous when multiple OPs share a seed display pattern.

---

## 6. Issues & Tickets

### Resolved this session
- Operational: WUT run 109 not Active / “not in Wv2” — transfer was present as **#308**; force-activated dual-active with **#6**.

### Deferred
- Cromwell empty responses + wrong error copy after 422 mutex — related to `docs/tickets/2026-07-21-cromwell-activate-id-or-name.md` and transfer reply-contract hardening; still open as agent quality.
- Active mutex messaging could better distinguish “different fingerprint OK / use force for dual attention” vs “duplicate recipe” — optional UX/docs for weak local models.
- Pre-existing dirty WUT tree (`portfolio_overlap_policy.rb`, cohort rake, mint script) — **unrelated**, do not touch this wrap.
- Dual-active Orange is intentional short experiment — operator should deactivate one when comparison ends (ops hygiene, not a ticket unless forgotten).

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Transfer audit | `mcp_audit_20260722.jsonl` `wv2_transfer_portfolio_from_wut` | ✅ 200 |
| Status audit | `wv2_get_portfolio_status` 308 | ✅ 200 |
| Activate audit (Cromwell) | `wv2_activate_portfolio` | ✅ 422 `active_mutex` (expected) |
| Force activate #308 | `POST /internal/portfolios/activate` force | ✅ `action=activated`, `forced=true` |
| Dual Active | `GET /internal/portfolios` + status 6/308 | ✅ both active |

**Test command(s):**

```bash
curl -sS "http://localhost:3002/internal/portfolio_status?portfolio_id_or_name=308"
curl -sS -X POST "http://localhost:3002/internal/portfolios/activate" \
  -H 'Content-Type: application/json' -d '{"id_or_name":"308","force":true}'
curl -sS "http://localhost:3002/internal/portfolios"  # filter active
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None
- **Services:** compose stack already up (Wv2 :3002, WUT, DM, MCP, Cromwell, Postgres/Redis)
- **Migrations:** None
- **Operational data:** OP #308 created earlier by transfer; Active flag flipped true (forced)

---

## 9. Risks & Technical Debt

- Dual-active same seed means **two Daily Analysis tracks** on the same 15-symbol Orange book set — higher task noise until one is deactivated.
- #6 remains engaged with open risk; #308 is empty — do not assume capital or positions shared.
- Cromwell continues to bury structured MCP errors under empty replies / schema inventing.

---

## 10. Open Questions

- **How long keep dual-active Orange?** — needs answer from: operator; blocks: attention hygiene.
- **Is #308 meant to replace #6 eventually (successor/close) or pure parallel observation?** — operator; blocks: lifecycle next step.

---

## 11. Handoff & Resume Notes

- **Where I left off:** #308 Active (forced dual with #6); session report only pending commit.
- **Next concrete step:** When dual experiment ends, deactivate #6 or #308 via `POST /internal/portfolios/deactivate` with numeric id; do not re-transfer run 109 unless re-export changed.
- **Files to read first:**
  1. This report
  2. `ecosystem/docs/adr/ADR-006-operational-portfolio-lineage-and-lifecycle.md`
  3. `ecosystem/docs/session-reports/2026-07-21-0927-wut80-transfer-activate-recovery.md` (similar Cromwell pattern)
  4. `winston_v2/app/services/operations/portfolio_activation_service.rb`
  5. `winston_v2/app/services/operations/portfolio_config_importer.rb` (fingerprint lineage)

---

## 12. Stakeholder Communications

- Operator already has Telegram history; no external stakeholder email required.
- Optional one-liner for desk: “Orange 20-Day (run 109) is live as paper OP #308 dual-active with engaged 5-Day Orange #6.”

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report (via wrap)
- **What worked well:** MCP audit + direct curl to Wv2 internal APIs cut through Cromwell narrative failure in minutes.
- **Friction points:** Agent empty responses; user believed portfolio “not in Wv2” when #308 was already imported inactive.
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [ ] Optionally harden Cromwell/MCP user-facing text for `active_mutex` (different fp vs same seed attention) — owner: agent/ops — due: backlog
- [ ] When dual-Orange experiment ends, deactivate one OP — owner: operator — due: when done comparing
- [ ] Consider skill note on winston-wut-to-wv2 / portfolio-lifecycle: dual seed+different fp is OK; mutex is attention — owner: agent — due: if confusion recurs

---

## 15. Appendix

### Timeline (UTC from MCP audit 2026-07-22)

| Time | Event |
|------|--------|
| 21:33:06 | `wv2_transfer_portfolio_from_wut` run_id 109 — progress started |
| 21:33:06+ | transfer **200** ~189ms — multi: WUT export → Wv2 import |
| 21:36:27 | `wv2_get_portfolio_status` 308 — **200** |
| 21:40:16 | `wv2_activate_portfolio` — **422** active_mutex vs #6 |
| ~16:11 MDT wrap | force activate #308 confirmed both Active |

### Activate error (Cromwell attempt)

```
Active mutex blocked #308 "Portfolio Orange · 7ea76741":
conflicts with #6 "Portfolio Orange · 6622b2eb" (same_seed_name).
Pass force=true for a short dual-active experiment.
```

### Force activate response (ops recovery)

```json
{
  "status": "ok",
  "action": "activated",
  "forced": true,
  "portfolio": {
    "id": 308,
    "name": "Portfolio Orange · 7ea76741",
    "active": true,
    "execution_mode": "paper"
  }
}
```

### Active band after recovery

| id | name | capital (approx) |
|----|------|------------------|
| 6 | Portfolio Orange · 6622b2eb | 6143.96 |
| 11 | Portfolio Rust · dd7e7c7a | (negative book cash) |
| 157 | Portfolio Mango (WUT run 57) | ~891 |
| 240 | Portfolio Blue · 9cf64e64 | 10000 |
| 308 | Portfolio Orange · 7ea76741 | 10000 |
```
