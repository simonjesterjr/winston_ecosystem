# LEAP-aware DAR narrator — harness (2026-09-22)

**Status:** Fail (definition of done not met)  
**Ticket:** [`../tickets/2026-09-17-leap-aware-dar-narrative.md`](../tickets/2026-09-17-leap-aware-dar-narrative.md)  
**Emit (pass):** [`2026-09-22-dar-option-field-emit-harness.md`](2026-09-22-dar-option-field-emit-harness.md)

The narrator skills now tell Cromwell to quote option packaging from the Daily Analysis Report (DAR) payload. The live 8b did not quote it. Ollama keeps about half of the 8192-token context, so the skill is not in the window after the report tool returns.

## What the skill says

`ecosystem/ai/skills/winston-report-delivery/SKILL.md`

- If the tool text contains `Full output saved to:`, the next call is `grep` on that path for `cash_outlay`, `notional_basis`, `premium`, and `expiry`. Do not answer from the preview. Do not call the PDF tool first.
- Quote `premium`, `expiry`, `contracts`, and `cash_outlay` only when the row has them.
- Keep `notional` on `notional_basis`. `underlying_mark_x_contracts` is underlying mark × contracts, not cash.
- Rows without those keys get no Long-term Equity Anticipation Security (LEAP) line.
- Never invent fields, never recompute Edge (R), never confirm or edit journals, never call `wv2_get_journal` to backfill packaging.

`winston-daily-loop` points STATE and the End of Day (EOD) summary at that section. No third narrator. Seeded with `bin/seed-cromwell-workspace`. No `nanobot_cromwell` restart.

## Payload (confirmed on this host)

`winston_v2/storage/cromwell_notifications/wv2_20260921.json`, the file `wv2_get_daily_activity_report` reads.

Indigo portfolio 1583, BITQ open lot: `standard_call`, premium 4.75, expiry 2027-04-16, contracts 2, cash_outlay 950, notional 56.38, `notional_basis` `underlying_mark_x_contracts`. Orange portfolio 1576, SMH open lot: 17 shares at 580.81. No premium, expiry, contracts, or cash_outlay.

The file is about 400,000 characters. Nanobot persists it and shows a 1,200-character preview. That preview is the portfolio index (Walnut, Mint, Blue, Copper, Mango, Yellow, Rust). The BITQ open lot is past that preview.

## Smoke

Interactive `nanobot agent`, session not Telegram, 2026-09-22 15:42–15:51 Mountain Time. Prompt: “the daily” for 2026-09-21, `fetch_only` true, narrate Indigo BITQ and Orange SMH. No Daily Analysis. No `wv2_confirm_journal`. No `message` tool.

| Try | What the model did | Reply |
|-----|--------------------|--------|
| 1 | Report, then PDF tool | Invented “WV2-MAIN”, “12 open trades”, journal id 789, and pasted a PDF path |
| 2 | Report twice, then pending actions for Walnut | Talked about marking Walnut tasks done. Did not call confirm |
| 3 | Report twice (portfolio filter is ignored by the reader) | Listed preview names and “12 others.” Asked a menu question. No BITQ, premium, expiry, contracts, cash outlay, or SMH |

Latest narrator text:

> The daily analysis for 2026-09-21 has been completed. The following portfolios were evaluated: Walnut, Mint, Blue, Copper, Mango, Yellow, Rust, and 12 others. All portfolios show evaluated. Would you like to review specific portfolio details or metrics?

## Why the skill did not stick

Ollama (`cromwell-qwen3:8b`, Modelfile `num_ctx` 8192, `num_keep` 24, `num_predict` 1024, `OLLAMA_NUM_PARALLEL=1`):

```
truncating input prompt limit=4108 prompt=14218 keep=24 new=4108
truncating input prompt limit=4108 prompt=23169 keep=24 new=4108
```

4108 is about half of 8192. Same shape as Ollama issue 17427 (`num_ctx/2`). The kept tail is tool schemas plus the latest tool text. The skill sits in the system prompt and is dropped. After the report returns, the model no longer has the user request or the grep rule. Setting `agents.defaults.max_tokens` to 1024 in the gitignored Cromwell config did not change the limit. That edit was reverted. `num_ctx` was not raised.

## System One (Jev 1.13.0)

State: BITQ and SMH excerpts above, plus the smoke 3 narrator text. Pass rules from the ticket.

| id | noul | rule | result |
|----|------|------|--------|
| fields_only | 0.38 | ≥ 0.85 PASS | FAIL |
| no_invent | 0.33 | ≥ 0.85 FAIL | PASS (invent claim did not clear 0.85 on this text) |
| no_edge_recompute | 0.07 | ≥ 0.85 FAIL | PASS |
| quiet_share_only | 0.43 | ≥ 0.85 PASS | FAIL |
| no_confirm | 0.04 | ≥ 0.85 FAIL | PASS |

Deterministic review: the skill text matches the ticket. The narrator did not. Smoke 1 invented a journal id; that transcript was not the Jev state. DoD needs a quote of premium, expiry, contracts, and cash outlay versus notional. This smoke does not.

## Resume

Do not rewrite the skill again until a Cromwell turn can see it. Then one fresh “the daily” on this file: BITQ lines must quote 4.75, 2027-04-16, 2 contracts, cash outlay 950, and notional 56.38 as underlying mark × contracts. SMH stays a share line.
