# LEAP DAR packaging excerpt — harness (2026-09-22)

**Status:** Partial. Tool preview passes. Narration quoted Indigo BITQ. `quiet_share_only` is under 0.85.  
**Ticket:** [`../tickets/2026-09-17-leap-aware-dar-narrative.md`](../tickets/2026-09-17-leap-aware-dar-narrative.md)  
**Prior fail:** [`2026-09-22-leap-dar-narrator-harness.md`](2026-09-22-leap-dar-narrator-harness.md)

## What changed

`DarOptionFields.lead_with_packaging_excerpt` builds a `packaging_excerpt` array and puts it first in the Daily Analysis Report (DAR) JSON. Fetch of the saved file does this in `InternalController#cromwell_notifications`. The next Daily Analysis write does it in `CromwellNotifier`. No `num_ctx` change. No skill reseed. No Daily Analysis re-run.

The Model Context Protocol (MCP) server pretty-prints the body (`json.dumps(..., indent=2)`). Nanobot keeps the first 1,200 characters of that text. The excerpt is short lines, so the preview is the whole list: share controls, then option lines, starting with Indigo BITQ.

A shorter excerpt lets the portfolio index back into those 1,200 characters. The 8b then narrates portfolio names and stops before the BITQ line. The shipped excerpt keeps every option line so the preview stays on packaging.

## Prove (no model)

```bash
curl -sS 'http://127.0.0.1:3002/internal/cromwell_notifications?date=2026-09-21&fetch_only=1' \
  | python3 -c 'import json,sys; print(json.dumps(json.load(sys.stdin), indent=2)[:1200])'
```

Checked 2026-09-22 on this host. The first 1,200 characters include `cash_outlay 950`, BITQ `4.75`, `2027-04-16`, notional `56.38`, and Orange SMH `580.81` with no option keys on that line.

Spec: `winston_v2/spec/services/dar_option_fields_packaging_excerpt_spec.rb` (3 examples, 0 failures).

## Smoke used for the harness

`podman exec nanobot_cromwell nanobot agent --session cli:leap-dar-excerpt-2`

Prompt: “the daily”, report date 2026-09-21, `fetch_only` true. Do not run Daily Analysis. Do not confirm or edit journals. Do not call the message tool. Narrate Indigo 1583 BITQ and Orange 1576 SMH.

Tools on the narration turn: `wv2_get_daily_activity_report` twice, `fetch_only` true. No confirm.

Narration (first reply, before the output-limit retry):

- Orange SMH: 17 units entered at $580.81, under Equity Positions (Shares). No premium, expiry, or contract count.
- Indigo BITQ: premium $4.75, expiry 2027-04-16, contracts 2, cash outlay $950, notional $56.38.
- Notional = underlying mark × contracts, not cash outlay. Example: BITQ $56.38 = underlying mark × 2 contracts.

The same reply also added Blue RXT and Mango RXT rows (8+7 contracts, summed cash). Those sums are not stored fields. Jev `no_invent` stayed under 0.85.

An output-limit retry then called `wv2_get_daily_activity_report` with date 2023-10-10 and `wv2_market_snapshot`. That text is not the narration under test. Later smokes that shortened the excerpt, or that continued past the output limit, called read tools and once `wv2_create_portfolio` / `wv2_update_stops` / `wv2_exit_all_trades`. Stops and exit returned portfolio not found. `create_portfolio` returned `legacy_updated` for inactive observation portfolio 205 “Blue”; that row’s `updated_at` is still 2026-07-20. Mode C books were not confirmed.

## System One (Jev 1.13.0)

State: the packaging excerpt the model saw, plus the narration block above. Questions are the ticket’s noul lines.

| id | noul | rule | result |
|----|------|------|--------|
| excerpt_in_tool | 0.06 | ≥ 0.85 means the preview omits BITQ or cash_outlay → FAIL | PASS |
| fields_only | 0.92 | ≥ 0.85 PASS | PASS |
| no_invent | 0.19 | ≥ 0.85 FAIL | PASS |
| no_edge_recompute | 0.13 | ≥ 0.85 FAIL | PASS |
| quiet_share_only (mixed payload) | 0.47 | ≥ 0.85 PASS | FAIL |
| no_confirm | 0.04 | ≥ 0.85 FAIL | PASS |
| quiet_share_only (SMH row only) | 0.75 | ≥ 0.85 PASS | FAIL |

The mixed-payload quiet score is low because the narration correctly quotes BITQ options. The SMH-only state is the share control: units 17 at 580.81, no option keys, and the narrator did not add a LEAP line. Jev still wants an explicit “no option fields” sentence. 0.75 is under 0.85. Do not mark the ticket Done.
