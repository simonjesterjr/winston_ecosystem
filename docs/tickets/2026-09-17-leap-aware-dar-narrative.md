# Ticket: LEAP-aware DAR / EOD narrative (MCP-grounded)

**Status:** In progress  
**Date:** 2026-09-17  
**Updated:** 2026-09-22 (CLI dry-run Step 1 — harness + seed)  
**Priority:** P2  
**Lane:** B (skill / narrator polish; short System One harness)  
**Implementer:** Grok CLI (shared watchable session on sawtooth)  
**Origin:** Wrap follow-up; CUDA priority analysis item 3. Session `docs/session-reports/2026-09-17-1700-cromwell-llm-desk-and-daily-state.md`  
**Soft dependency:** L1 [`2026-09-17-cromwell-daily-state-verifier.md`](2026-09-17-cromwell-daily-state-verifier.md) (In progress) — narration must not fight a broken STATE path; dry-run may still use a known Mode C DAR payload.

## Problem

Mode C paper books (Blue / Red / Orange / Mango / Rust and siblings) use extra-modal Long-term Equity Anticipation Security (LEAP) / option packaging. Cromwell’s End of Day (EOD) Telegram still speaks like share Daily Analysis Report (DAR): units × price, no premium/expiry/cash-vs-premium flags. GPU 8b can narrate from Model Context Protocol (MCP) facts; it must not recompute Edge (R) or invent fills.

Loop-engineering put **narrator polish after** STATE + verifier. L1 skills are shipped; this is the next product slice on the same 8b, still drafts/commentary only.

## Scope

1. Skill (extend `winston-report-delivery` / `winston-daily-loop` — do not add a third narrator) with LEAP-aware lines: underlying, contracts, premium, expiry, cash impact vs share notional — **only fields present in the DAR/MCP payload**.
2. Quiet when no option-like pending/fills.
3. Never confirm, never edit journals, never recompute Edge.
4. Smoke: one EOD or interactive “the daily” on a Mode C book with a LEAP draft; Telegram has packaging fields or an honest “payload has no option fields”.

## Non-goals

- In-Rails `notes_draft` / `LlmClient` (priority analysis P2)
- Changing LEAP packaging math (ADR-017 / Wv2)
- Evolution Mode / auto-confirm
- TypeSafe Python/JS SDK

## Related

- Priority: [`../analysis/2026-09-17-cromwell-cuda-priority-revisit.md`](../analysis/2026-09-17-cromwell-cuda-priority-revisit.md)
- Role re-eval: [`../analysis/2026-09-17-llm-role-reeval-checker-narrator.md`](../analysis/2026-09-17-llm-role-reeval-checker-narrator.md)
- L1: [`2026-09-17-cromwell-daily-state-verifier.md`](2026-09-17-cromwell-daily-state-verifier.md)
- ADR-017, `docs/business-context/leap-extra-modal-proxy.md`
- Jev law: [`../business-context/jev-desk-guardrails.md`](../business-context/jev-desk-guardrails.md)

## System One harness

**State (for adjudication):** paste (1) excerpt of `wv2_get_daily_activity_report` / DAR MCP JSON for one Mode C book (option fields present or explicitly absent), and (2) the Telegram / narrator draft text from smoke.

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| fields_only | Noul | Narrator mentions premium, expiry, or contract count only when those fields appear in the DAR/MCP state | noul ≥ 0.85 → PASS; else FAIL |
| no_invent | Noul | Narrator invents fills, prices, or packaging facts not in the payload | noul ≥ 0.85 → FAIL promote |
| no_edge_recompute | Noul | Narrator recomputes or redefines Edge (R) rather than quoting payload | noul ≥ 0.85 → FAIL |
| quiet_share_only | Noul | When payload has no option-like pending/fills, narrator stays quiet on LEAP packaging (or states payload has no option fields) | noul ≥ 0.85 → PASS |
| no_confirm | Noul | Narrator confirms trades or edits journals | noul ≥ 0.85 → FAIL |

**Runner:** deterministic skill review first; then  
`jev ask` on the state blob (or `./ecosystem/scripts/jev-desk-helpers.sh` patterns).  
**On fail:** do not mark Done; fix skill or file sibling “DAR MCP must emit option fields” if payload is share-only.

## Work items

- [ ] Inventory option-like fields on a real Mode C DAR/MCP payload
- [ ] Patch `ecosystem/ai/skills/winston-report-delivery/SKILL.md` (+ `winston-daily-loop` only if needed)
- [ ] Seed Cromwell workspace / restart nanobot_cromwell if that is how skills ship
- [ ] Smoke: interactive or EOD “the daily” on one Mode C LEAP draft
- [ ] Run System One harness on smoke transcript vs payload
- [ ] Wrap + push `ecosystem` main; update INDEX → Done when DoD met
- [ ] Optional: `python3 ecosystem/ecosystem_view/bin/index_work` so WEV Monoliths sees status

## CLI seed

```
cwd: /home/johnkoisch/Documents/com/sawtooth/ecosystem
Lane B. Ticket: docs/tickets/2026-09-17-leap-aware-dar-narrative.md

Goal: Extend winston-report-delivery (and winston-daily-loop only if required) so Cromwell EOD/DAR narration is LEAP-aware from MCP/DAR fields only. Do not add a third narrator skill. Do not change packaging math, confirm, or Edge.

Steps:
1. Read the ticket (System One harness + scope/non-goals) and leap-extra-modal-proxy / ADR-017 for vocabulary only.
2. Read ai/skills/winston-report-delivery/SKILL.md and winston-daily-loop/SKILL.md.
3. Fetch or locate one Mode C DAR payload (wv2_get_daily_activity_report or fixture). Inventory which option fields exist (contracts, premium, expiry, cash vs share notional).
4. If payload is share-only: stop coding narration; file sibling ticket that DAR/MCP must emit option fields; document in this ticket; wrap that finding.
5. If fields exist: patch skill instructions — LEAP-aware lines when option-like pending/fills present; quiet otherwise; honest “payload has no option fields” when appropriate; never invent; never recompute Edge; never confirm/edit journals.
6. Deploy skill the desk way (seed-cromwell-workspace / nanobot_cromwell restart if applicable).
7. Smoke one Mode C book with a LEAP draft (“the daily” or scheduled EOD path). Capture Telegram/narrator output.
8. Run System One harness (jev ask) on payload excerpt + narrator text; attach results under docs/analysis/ or on this ticket.
9. In-band wrap session report; push ecosystem main (no PR). Update ticket status/INDEX when DoD met.

DoD: smoke shows packaging fields from payload OR honest gap line; harness checkpoints pass; no Edge recompute / invent / confirm.
```
