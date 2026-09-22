# Ticket: LEAP-aware DAR / EOD narrative (MCP-grounded)

**Status:** In progress  
**Date:** 2026-09-17  
**Updated:** 2026-09-22 (packaging excerpt is in the tool preview; quiet checkpoint still short)  
**Priority:** P2  
**Unblocked by:** [`archive/2026-09-22-dar-mcp-emit-option-fields.md`](archive/2026-09-22-dar-mcp-emit-option-fields.md) — [`../analysis/2026-09-22-dar-option-field-emit-harness.md`](../analysis/2026-09-22-dar-option-field-emit-harness.md)  
**Lane:** B (Cromwell/DAR tool-result packaging excerpt + narrator smoke; short System One harness)  
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
- Raising Ollama `num_ctx` / hoping skill survives truncation (not DoD)
- Committing `graphify-out/`
- Operator manually reviewing SMH as a resume gate

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

Skills were patched and seeded on 2026-09-22. Interactive smoke did not quote packaging. See Smoke stop below. Do not mark Done.

## System One harness

**State (for adjudication):** paste (1) excerpt of `wv2_get_daily_activity_report` / DAR MCP JSON for one Mode C book (option fields present or explicitly absent), and (2) the Telegram / narrator draft text from smoke.

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| excerpt_in_tool | Noul | Tool result Preview / top-level packaging excerpt (same turn, no grep) omits cash_outlay or BITQ option keys that exist in the saved DAR | noul ≥ 0.85 → FAIL before smoke |
| fields_only | Noul | Narrator mentions premium, expiry, or contract count only when those fields appear in the DAR/MCP state | noul ≥ 0.85 → PASS; else FAIL |
| no_invent | Noul | Narrator invents fills, prices, or packaging facts not in the payload | noul ≥ 0.85 → FAIL promote |
| no_edge_recompute | Noul | Narrator recomputes or redefines Edge (R) rather than quoting payload | noul ≥ 0.85 → FAIL |
| quiet_share_only | Noul | When payload has no option-like pending/fills, narrator stays quiet on LEAP packaging (or states payload has no option fields) | noul ≥ 0.85 → PASS |
| no_confirm | Noul | Narrator confirms trades or edits journals | noul ≥ 0.85 → FAIL |

**Runner:** deterministic skill review first; then  
`jev ask` on the state blob (or `./ecosystem/scripts/jev-desk-helpers.sh` patterns).  
**On fail:** do not mark Done; fix skill. Emit sibling is Done — do not re-file unless a regression drops the fields.

## Smoke stop (2026-09-22)

`winston-report-delivery` now says: if the report tool returns `Full output saved to:`, grep that file for `cash_outlay`, `notional_basis`, `premium`, and `expiry` before any other tool or reply. Quote those keys only when present. Keep `notional` on `notional_basis`. Share rows get no Long-term Equity Anticipation Security (LEAP) line. Never invent, never recompute Edge (R), never confirm. `winston-daily-loop` points at that section for STATE. Seeded with `bin/seed-cromwell-workspace`. No gateway restart. Skills are read from the workspace on each turn.

Three interactive “the daily” turns for 2026-09-21, `fetch_only` true (no Daily Analysis, no journal confirm, no `message` tool). The saved report is about 400k characters, so nanobot persists it and shows a 1,200-character preview. That preview is the portfolio index (Walnut, Mint, Blue, …). Indigo BITQ premium 4.75 / expiry 2027-04-16 / contracts 2 / cash_outlay 950 / notional 56.38 is later in the file. The narrator never grepped. Latest reply listed those preview names and “12 others,” and did not mention BITQ, premium, expiry, contracts, cash outlay, or SMH.

Ollama log: `truncating input prompt limit=4108 prompt=14218 keep=24` and again `prompt=23169`. Slot context is 8192. The model keeps 24 tokens from the start and the tail. The skill body is not in that tail once tool schemas and the tool result are present. Same pattern as Ollama issue 17427 (usable prompt about half of `num_ctx`). Raising `max_tokens` in the gitignored Cromwell config did not change the limit. No `num_ctx` change in this session.

Harness: [`../analysis/2026-09-22-leap-dar-narrator-harness.md`](../analysis/2026-09-22-leap-dar-narrator-harness.md). `fields_only` 0.38 and `quiet_share_only` 0.43 fail. No confirm and no Edge (R) recompute. DoD is not met.

Resume is **not** waiting on logs or Operator reviewing SMH. Skill-only resumes stay open-ended because the skill falls out of the Ollama window.

## Next slice (2026-09-22) — packaging excerpt in the tool result

**Problem:** nanobot persists large MCP results and returns ~1,200 characters of **Preview** (portfolio index first). Ollama then cuts the prompt (~4108 usable tokens). The 8b never greps and never sees Indigo BITQ packaging. Raising `max_tokens` did not help; do not treat `num_ctx` bumps as the DoD.

**Fix (proactive, closed loop):** put a **compact packaging excerpt into the tool result the model sees** (Preview and/or a top-level DAR field), before the LLM speaks. Do not rely on the skill surviving truncation.

Preferred order (pick the smallest desk-owned path that works):

1. **Wv2 DAR JSON** — add a top-level key early in the payload (e.g. `narrator_packaging` / `packaging_excerpt`) listing open lots / actions that carry `premium` | `expiry` | `contracts` | `cash_outlay` | `notional_basis`, plus share-only controls with those keys absent (Orange SMH). Keep existing rows; do not change packaging math.
2. **Or** nanobot Sawtooth patch under `ecosystem/ai/nanobot/patches/` — when persisting `wv2_get_daily_activity_report` (and siblings), enrich the `Full output saved to:` Preview with that same excerpt scraped from the saved file.
3. Re-seed / rebuild only as required by the path chosen. Then one `fetch_only` “the daily” smoke.

**Gate to resume smoke:** tool result Preview (or top-level excerpt) already contains BITQ packaging keys **in the same turn’s tool text**, without a follow-up grep. Then smoke must quote them.

**Pass smoke:** quote BITQ premium **4.75**, expiry **2027-04-16**, **2** contracts, cash outlay **950**, notional **56.38** as underlying mark times contracts; Orange SMH stays share-shaped (no LEAP line). Jev harness checkpoints pass. Then Done/archive.

## Excerpt in the tool preview (2026-09-22)

`DarOptionFields.lead_with_packaging_excerpt` is the first key of the daily-report JSON. `InternalController#cromwell_notifications` adds it on fetch, including the saved 2026-09-21 file. `CromwellNotifier` writes it on the next Daily Analysis. Packaging math is unchanged. The excerpt rounds binary dust (for example 1839.9999999999998 → 1840) so a line stays short. Share rows are one open lot per book and omit option keys.

Nanobot persists the Model Context Protocol (MCP) body and shows the first 1,200 characters. MCP pretty-prints with indent 2. The excerpt is lines, so that preview contains the whole list: Indigo BITQ premium 4.75, expiry 2027-04-16, contracts 2, cash_outlay 950, notional 56.38, and Orange SMH 17 at 580.81 with no option keys.

Prove (no model, no grep of the saved file):

```bash
curl -sS 'http://127.0.0.1:3002/internal/cromwell_notifications?date=2026-09-21&fetch_only=1' \
  | python3 -c 'import json,sys; print(json.dumps(json.load(sys.stdin), indent=2)[:1200])'
```

The first 1,200 characters include `cash_outlay 950`, `BITQ`, `4.75`, `2027-04-16`, `56.38`, `SMH`, and `580.81`. Spec: `winston_v2/spec/services/dar_option_fields_packaging_excerpt_spec.rb`.

Smoke that quoted those figures: `nanobot agent --session cli:leap-dar-excerpt-2`, prompt “the daily”, date 2026-09-21, `fetch_only` true. Narration quoted BITQ premium 4.75, expiry 2027-04-16, 2 contracts, cash outlay 950, notional 56.38 as underlying mark times contracts. Orange SMH was 17 units at 580.81 under shares, with no Long-term Equity Anticipation Security (LEAP) line. No journal confirm. No Daily Analysis. Harness: [`../analysis/2026-09-22-leap-dar-packaging-excerpt-harness.md`](../analysis/2026-09-22-leap-dar-packaging-excerpt-harness.md). `quiet_share_only` is 0.75 on the SMH row alone (gate is 0.85). Not Done.

**Not the gate:** Operator eyeballing SMH; Telegram send; journal confirm; Edge (R); waiting for context to “validate” in logs; committing `graphify-out/`.

## Work items

- [x] Inventory option-like fields — initially share-only; **emit landed** (premium/expiry/contracts/cash_outlay on BITQ 1946)
- [x] Patch `ecosystem/ai/skills/winston-report-delivery/SKILL.md` (+ one pointer in `winston-daily-loop`) — instructions only; the 8b did not follow them
- [x] Seed Cromwell workspace. No `nanobot_cromwell` restart (skills load from disk; restart does not widen the prompt)
- [x] Smoke: interactive “the daily” — did not quote packaging
- [x] System One harness — fail on `fields_only` and `quiet_share_only`
- [x] Wrap + push `ecosystem` main. INDEX stays In progress. Not archived — definition of done not met
- [x] `index_work` ran, then reverted. `work.json` is one line and would have absorbed other uncommitted docs
- [x] **Packaging excerpt in tool result** — `packaging_excerpt` is the first key; the 1,200-character preview contains BITQ and SMH
- [x] Deterministic check: pretty preview of `fetch_only` 2026-09-21 contains `cash_outlay 950` and BITQ before any LLM turn (curl above)
- [x] Smoke `cli:leap-dar-excerpt-2` quoted 4.75 / 2027-04-16 / 2 / 950 / 56.38; SMH stayed a share line
- [ ] System One `quiet_share_only` 0.75 on the SMH row (need ≥ 0.85). Do not Done/archive
- [x] In-band wrap; push `ecosystem` and `winston_v2` main. Never commit `graphify-out/`

## CLI seed

```
cwd: /home/johnkoisch/Documents/com/sawtooth
Lane B. Fresh session (do not resume the skill-only smoke chat).
Ticket: ecosystem/docs/tickets/2026-09-17-leap-aware-dar-narrative.md
Read: Smoke stop + Next slice (packaging excerpt in the tool result) + System One harness.

Goal: Make the DAR/report tool result the 8b actually sees include a compact packaging excerpt (Indigo BITQ option keys + Orange SMH share control) so narration does not depend on winston-report-delivery surviving Ollama truncation or on a follow-up grep. Then one fetch_only “the daily” smoke.

Unblocked facts:
- Skill text already greps Full output saved to: — insufficient alone (prompt cut ~4108).
- Fixture: winston_v2/storage/cromwell_notifications/wv2_20260921.json — BITQ journal 1946: premium 4.75, expiry 2027-04-16, contracts 2, cash_outlay 950, notional 56.38 notional_basis underlying_mark_x_contracts; Orange SMH 17 @ 580.81 no option keys.
- Emit serializers Done (Wv2 1401177). Do not re-litigate packaging math / ADR-017.
- Never commit graphify-out/.

Steps:
1. Read this ticket sections Smoke stop + Next slice. Locate nanobot “Full output saved to:” / Preview persist (PyPI nanobot-ai inside nanobot_cromwell image; Sawtooth patches live in ecosystem/ai/nanobot/patches/). Locate Wv2 daily activity report JSON builder if using serializer path.
2. Implement the smallest path: (A) top-level early DAR key packaging_excerpt / narrator_packaging, or (B) nanobot patch that enriches Preview for wv2_get_daily_activity_report from the persisted file. Prefer desk-owned, testable without raising num_ctx.
3. Deterministic prove: after tool persist, Preview or tool text contains cash_outlay and BITQ packaging without grep. Document the prove command on the ticket or analysis note.
4. Seed/rebuild as required (bin/seed-cromwell-workspace; rebuild nanobot_cromwell only if patch). Do not restart hoping skills widen context.
5. Smoke: interactive “the daily” with fetch_only on a DAR that still has BITQ + SMH. Capture narrator text. No journal confirm. Telegram optional.
6. System One: jev ask on (payload/tool excerpt + narrator text) per harness; write ecosystem/docs/analysis/… if useful.
7. In-band wrap; push main (ecosystem and winston_v2 if touched). Mark Done/archive + INDEX only when smoke + harness pass.

DoD: tool result visible to the model includes packaging excerpt; smoke quotes 4.75 / 2027-04-16 / 2 contracts / cash outlay 950 / notional 56.38 as underlying mark times contracts; SMH has no LEAP line; harness fields_only + quiet_share_only + no_invent pass; no Edge recompute / confirm.
```
