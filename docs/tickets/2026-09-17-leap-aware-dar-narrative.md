# Ticket: LEAP-aware DAR / EOD narrative (MCP-grounded)

**Status:** In progress  
**Date:** 2026-09-17  
**Updated:** 2026-09-22 (CLI dry-run Step 1 — narrator seed refreshed after emit unblock)  
**Priority:** P2  
**Unblocked by:** [`archive/2026-09-22-dar-mcp-emit-option-fields.md`](archive/2026-09-22-dar-mcp-emit-option-fields.md) — [`../analysis/2026-09-22-dar-option-field-emit-harness.md`](../analysis/2026-09-22-dar-option-field-emit-harness.md)  
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
- Inventory: [`../analysis/2026-09-22-dar-mode-c-option-field-inventory.md`](../analysis/2026-09-22-dar-mode-c-option-field-inventory.md)
- Unblock (Done): [`archive/2026-09-22-dar-mcp-emit-option-fields.md`](archive/2026-09-22-dar-mcp-emit-option-fields.md)

## Inventory stop (2026-09-22)

Specimen: `winston_v2/storage/cromwell_notifications/wv2_20260921.json` (the `wv2_get_daily_activity_report` file). Structured option keys are absent. `fulfillment_label` is null. Open-lot `notional` is underlying mark × `units`.

Indigo BITQ (position 889 / journal 1946) is 2 contracts, premium 4.75, expiry 2027-04-16, strike 28, cash outlay 950. The DAR row is units 2, entry 4.75, mark 28.19, notional 56.38. Same pattern on Mango SEF, Mango/Blue RXT calls, and Teal XLU put. `wv2_get_journal` already has `fulfillment_details`. Pending MCP (`serialize_pending_task`) does not.

`winston-report-delivery` and `winston-daily-loop` were not edited. No Cromwell reseed. No Telegram smoke. Jev was not called: the harness compares narrator text to the payload, and there is no narrator text. The stop is the key walk in the analysis.

Resume condition met 2026-09-22. See Emit landed below. Patch the existing narrator skills only.

## Emit landed (2026-09-22)

The Daily Analysis Report (DAR) serializer now copies stored option packaging. Indigo BITQ (journal 1946) on the patched `wv2_20260921.json` and on a read-only builder slice: premium 4.75, expiry 2027-04-16, contracts 2, cash_outlay 950. Notional is still 56.38 and labeled `underlying_mark_x_contracts`. Orange SMH 17 @ 580.81 has no option keys. Edge (R) was not added. Jev checkpoints on that excerpt passed.

`winston-report-delivery` and `winston-daily-loop` are still unedited. No Cromwell reseed. No new Telegram send. Next work on this ticket is the skill patch only, quoting fields that are on the payload.

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
**On fail:** do not mark Done; fix skill. Emit sibling is Done — do not re-file unless a regression drops the fields.

## Work items

- [x] Inventory option-like fields — initially share-only; **emit landed** (premium/expiry/contracts/cash_outlay on BITQ 1946)
- [ ] Patch `ecosystem/ai/skills/winston-report-delivery/SKILL.md` (+ `winston-daily-loop` only if needed) — unblocked 2026-09-22; not started in the emit session
- [ ] Seed Cromwell workspace / restart nanobot_cromwell if that is how skills ship
- [ ] Smoke: interactive or EOD “the daily” on one Mode C LEAP draft
- [ ] Run System One harness on smoke transcript vs payload — not run; no narrator text
- [ ] Wrap + push `ecosystem` main; update INDEX → Done when DoD met — emit session set this ticket back to In progress; narrator DoD still open
- [ ] Optional: `python3 ecosystem/ecosystem_view/bin/index_work` so WEV Monoliths sees status

## CLI seed

```
cwd: /home/johnkoisch/Documents/com/sawtooth
Lane B. Fresh session (do not resume the share-only stop chat).
Ticket: ecosystem/docs/tickets/2026-09-17-leap-aware-dar-narrative.md

Goal: Patch Cromwell narrator skills so EOD/DAR commentary quotes LEAP/option packaging from the DAR/MCP payload. Skills only: ecosystem/ai/skills/winston-report-delivery (and winston-daily-loop only if required). Do not add a third narrator. Do not change packaging math, confirm, Edge (R), or Wv2 serializers (emit already Done: Wv2 1401177).

Unblocked facts (use as smoke state):
- Fixture/MCP file: winston_v2/storage/cromwell_notifications/wv2_20260921.json (patched on sawtooth; other hosts need a new daily write)
- Indigo BITQ journal 1946 / open lot: premium 4.75, expiry 2027-04-16, contracts 2, cash_outlay 950, notional 56.38 with notional_basis underlying_mark_x_contracts, fulfillment_type standard_call
- Share control: Orange SMH 17 @ 580.81 — no option keys

Steps:
1. Read this ticket (Emit landed + System One harness) and ecosystem/docs/business-context/leap-extra-modal-proxy.md for vocabulary only.
2. Read ecosystem/ai/skills/winston-report-delivery/SKILL.md and winston-daily-loop/SKILL.md.
3. Confirm option fields on the BITQ row in wv2_20260921.json (or wv2_get_daily_activity_report). If missing on this host, regenerate DAR or stop and say so — do not invent.
4. Patch skill instructions: when option-like pending/fills/open lots have premium/expiry/contracts/cash_outlay, narrate those (and distinguish cash_outlay from underlying mark×contracts notional). Quiet on packaging when no option-like rows. Never invent fields; never recompute Edge; never confirm or edit journals.
5. Deploy skills the desk way (bin/seed-cromwell-workspace and/or nanobot_cromwell restart if that is how Cromwell loads skills).
6. Smoke: interactive “the daily” (or equivalent) on a Mode C book with an option lot — prefer Indigo/BITQ. Capture narrator/Telegram text.
7. System One: jev ask on (payload excerpt + narrator text) per ticket harness; write ecosystem/docs/analysis/… or attach on ticket.
8. In-band wrap; push ecosystem main (no PR). Mark ticket Done / archive + INDEX when DoD met. Optional: python3 ecosystem/ecosystem_view/bin/index_work.

DoD: smoke quotes packaging fields from payload (premium, expiry, contracts, cash outlay vs notional as labeled); share-only books stay quiet on LEAP lines; harness checkpoints pass; no invent / Edge recompute / confirm.
```
