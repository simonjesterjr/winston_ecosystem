# Plan: Copper #1585 — service-path fingerprint adopt (PBR 794)

**Status:** Active  
**Date:** 2026-09-25  
**Tickets:** [`docs/tickets/2026-09-25-copper-1585-fingerprint-importer-adopt.md`](../docs/tickets/2026-09-25-copper-1585-fingerprint-importer-adopt.md) · parent [`docs/tickets/2026-09-24-mode-d-phase-2.md`](../docs/tickets/2026-09-24-mode-d-phase-2.md) · send still blocked [`docs/tickets/2026-09-24-mode-d-phase-2-paper-send.md`](../docs/tickets/2026-09-24-mode-d-phase-2-paper-send.md)  
**Lane:** A (plan + System One + Grok CLI)  
**Operator lock:** fingerprint `d627cd795b410360aff56706dec38759d48f7d32f7cfac4203a29523e2c7c666` (short `d627cd79…`) from Winston Unit Test (WUT) Portfolio Backtest Run (PBR) #794 capture (heat + Resting Stop Touch (RST) + window) — not yet a Winston v2 (Wv2) TradingStrategy (TS) selection.

## Goal

I want Operational Portfolio (OP) **#1585** (`Portfolio Copper · mode-d-from-wut-794`) to carry the Operator-named fingerprint **through the service path** — `Operations::PortfolioConfigImporter` via `POST /internal/portfolios` — so OP + a new/found fingerprinted TS share lineage, Mode D + DUT070450 bind stay intact, Mode C Copper **#1581** / shared null-fingerprint TS **#341** stay untouched, and only then can paper Send ungate on the paper-send ticket. No SQL fingerprint writes. No Desk Send in this plan.

## Problem

#1585 was minted with a rails runner `Portfolio.create!` cutover ([`docs/analysis/2026-09-24-copper-794-mode-d-cutover.rb`](../docs/analysis/2026-09-24-copper-794-mode-d-cutover.rb)), bypassing `Operations::PortfolioConfigImporter` / `POST /internal/portfolios`. Desk doctrine: never repeat that for OP/TS lineage. Consequence: OP and TS **#341** still have **null fingerprint**; #341 is shared with Mode C Copper **#1581**, so writing on #341 is forbidden. A leftover **TST** book (Mode D TestDesk residue) currently sits on #1585 and **will block adopt** (`find_adopt_candidate` requires exact book-symbol match against the import `markets` list).

## Approach

1. **Read-only preflight** on #1585 (journals=0 / not engaged, exact `seed_name`, Mode D + DUT bind snapshot, markets including whether TST is present). Snapshot #1581/#341.
2. **Clear the TST book** so Copper market membership matches the import JSON (destroy TST book when journals=0; do not leave TST in the adopted DNA).
3. **WUT export/capture** for PBR **794** (live export already carries the Operator fingerprint — assert equality), with **seed_name override** matching #1585 and `force_lab_uncapped: true` so 11 Copper markets are not paper-capped to 4.
4. **`POST /internal/portfolios`** (importer) expecting `action=adopted` on #1585 — lands **inactive**, creates/finds TS by fingerprint (not #341).
5. **Re-activate** #1585 with `force=true` (dual-active vs #1581 same markets is intentional).
6. **Verify** fingerprint on OP + new/found TS; Mode D + DUT bind intact; #1581/#341 unchanged; no Desk Send.

## Preflight (read-only — fail closed before any mutate)

Run against live Wv2 (host `:3002`). Record a JSON snapshot under `docs/analysis/` before any write.

| Check | Pass rule |
|-------|-----------|
| Journals | `Portfolio.find(1585).journals.count == 0` and `engaged? == false` |
| `seed_name` | Exact string on #1585 (cutover used the full display name as seed — typically `Portfolio Copper · mode-d-from-wut-794`). POST body must use this exact value; do **not** leave WUT default `Portfolio Copper`. |
| Mode D | `leap_fulfillment == "none"` and `fulfillment_mode == "mode_d"` (from `fulfillment_packaging_policy`) |
| DUT bind | `broker_binding_id == "bnd_3d6a5020d839c315583277d2"` and `fulfillment_adapter_key` for Interactive Brokers (IBKR) paper **DUT070450** |
| Markets | Expect Copper 11: `AMZN GLD GOOGL JNJ MSFT PG TSLA TSM WMT XLE XLV`. **Live glance 2026-09-25 also showed leftover `TST`.** |
| #1581 / #341 | Mode C, `leap_fulfillment=all`, TS #341, null fingerprint — must remain so after adopt |
| Fingerprint lock | Operator full hash below — no alternate hash |

**Operator-named fingerprint (lock):**

```
d627cd795b410360aff56706dec38759d48f7d32f7cfac4203a29523e2c7c666
```

## TST book handling

`Operations::PortfolioConfigImporter#find_adopt_candidate` only adopts a null-fingerprint open series when `seed_name`/`name` matches **and** `books_symbols_match?` (sorted trading symbols equal the JSON `markets` array). Leftover **TST** makes symbols unequal → importer **forks** a new OP instead of adopting #1585.

**Required before POST:**

1. Confirm journals still 0.
2. Destroy the TST `Book` on #1585 only (or equivalent ops helper). Do not delete Copper books.
3. Re-read markets; must equal the 11 Copper symbols (sorted) with **no TST**.
4. If journals > 0 or TST cannot be cleared safely → **stop**; escalate to Operator (engaged refuse / close-successor path). Do not SQL-stamp fingerprint.

After a successful adopt, `sync_books!` would also drop symbols absent from JSON — but adopt never runs if TST is still present, so clearing **before** POST is mandatory.

## WUT export / capture (PBR 794)

Canonical builder: WUT `PortfolioConfigExporter` (also `GET /internal/portfolio_config?run_id=794` on WUT host `:3000`).

**Live read-only glance (2026-09-25, this filing):** `GET http://127.0.0.1:3000/internal/portfolio_config?run_id=794` already returns:

- `fingerprint` = `d627cd795b410360aff56706dec38759d48f7d32f7cfac4203a29523e2c7c666` (**matches Operator lock** — do not invent another hash)
- `seed_name` / `name` = `Portfolio Copper` (**wrong for adopt** — must override to #1585 exact seed)
- `markets` = Copper 11 (no TST) — good
- `risk_percentage` = 1.0, `max_leverage` = 3.0, no `force_lab_uncapped` — **must add** `force_lab_uncapped: true` before POST or paper caps will normalize markets→4 / leverage→1.0
- Top-level methodology fields plus nested `trading_strategy` (`primary_entry_strategy`, `exit_strategy_names`, `heat`, `stop_strategy`, `wut_backtest_run_id`, …)

Capture + patch (implementer; not this filing):

```bash
curl -sS 'http://127.0.0.1:3000/internal/portfolio_config?run_id=794' \
  -o /tmp/copper-pbr794-export.json
# Patch seed_name to exact #1585 seed; set force_lab_uncapped true;
# assert fingerprint == Operator lock; assert TST not in markets.
# Write /tmp/copper-pbr794-adopt-body.json
```

Optional rake inside WUT container — still patch seed + `force_lab_uncapped` afterward; do **not** set `PAPER_CAPS=1`:

```bash
SEED_NAME='Portfolio Copper' \
  bin/rails 'wut:portfolios:export_config[794,/portfolio_configs/copper-pbr794-mode-d-adopt.json]'
```

If a future export fingerprint **differs** from the Operator lock → **do not POST that hash**. Stop and escalate.

## POST /internal/portfolios (document only — do not execute here)

Wv2 route: `POST /internal/portfolios` → `InternalController#create_portfolio` → `Operations::PortfolioConfigImporter.call(data:, source:)`.

Body is the patched WUT handoff JSON (same shape as `/portfolio_configs` files and the live export). Required adopt patches:

| Field | Value |
|-------|-------|
| `seed_name` | Exact #1585 `seed_name` from preflight (expect `Portfolio Copper · mode-d-from-wut-794`) |
| `fingerprint` | `d627cd795b410360aff56706dec38759d48f7d32f7cfac4203a29523e2c7c666` (already on live export — assert equality) |
| `force_lab_uncapped` | `true` (or `paper_ops_policy.force_lab_uncapped`) |
| `markets` | Copper 11 from export — **no TST** |

Documented curl shape (implementer runs; **this filing does not**):

```bash
curl -sS -X POST 'http://127.0.0.1:3002/internal/portfolios' \
  -H 'Content-Type: application/json' \
  --data-binary @/tmp/copper-pbr794-adopt-body.json
```

**Expect:** HTTP 200, `status=ok`, `action=adopted`, `portfolio.id=1585`, `portfolio.fingerprint` = full lock, `portfolio.active=false`, `trading_strategy.id` **≠ 341**, `trading_strategy.fingerprint` = full lock.

**Refuse / stop if:** `action=forked` (seed/books mismatch — usually TST or wrong seed_name), `engaged_refuse`, `closed_refuse`, or portfolio id ≠ 1585.

Importer `apply_portfolio_attributes!` does **not** assign `leap_fulfillment`, `fulfillment_packaging_policy`, `broker_binding_id`, or `fulfillment_adapter_key` — those must survive. Still verify explicitly after POST.

Display name becomes ADR-006 form: `seed · d627cd79`.

## Post: re-activate + verify

1. `POST /internal/portfolios/activate` with `{"id": 1585, "force": true}` (dual-active vs #1581 same markets is expected; without `force` activation 422s).
2. Verify #1585: fingerprint full lock; active true; Mode D; DUT bind unchanged; TS id is the new/found fingerprinted TS; markets = Copper 11, no TST; journals still 0.
3. Verify new/found TS: fingerprint full lock; methodology/heat from import.
4. Verify #341: still null fingerprint; name `TurtleV1 S1 Breakout20/10`; **no update!**.
5. Verify #1581: still on #341, Mode C, markets unchanged, fingerprint null.
6. **Do not Desk Send.** Paper-send ticket stays Blocked until this adopt + re-activate evidence is on the ticket.

## Grill notes

- Mint root cause: rails `Portfolio.create!` cutover skipped importer lineage — do not "fix" with another runner stamp of `fingerprint=`.
- Never `TradingStrategy.find(341).update!(fingerprint: ...)` — shared with Mode C #1581.
- `force_lab_uncapped: true` is mandatory for this 11-name lab book; default paper caps would warn and set max_markets=4.
- Seed mismatch with raw WUT `Portfolio Copper` → fork, not adopt.
- ADR-006: fingerprint adopt/fork/engaged refuse; import always inactive.

## System One harness

**State:** preflight JSON (journals, seed_name, markets±TST, Mode D, bind); export JSON fingerprint; POST response (`action`, ids, warnings); post-activate snapshots of #1585 / new TS / #1581 / #341.

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| preflight_clear | Noul | journals=0, seed_name exact, TST absent (or cleared), Mode D + DUT bind present before POST | noul ≥ 0.85 |
| action_adopted | Noul | POST result action is adopted on portfolio id 1585 (not forked/created) | noul ≥ 0.85 |
| fp_lock | Noul | OP and linked TS fingerprint equal full Operator lock; TS id ≠ 341 | noul ≥ 0.85 |
| mode_d_bind | Noul | After re-activate: fulfillment_mode mode_d, leap_fulfillment none, DUT bind unchanged | noul ≥ 0.85 |
| siblings_untouched | Noul | #1581 still Mode C on TS #341; #341 fingerprint still null | noul ≥ 0.85 |
| no_send | Noul | Did this work Desk-Send or SQL-stamp fingerprint? | noul ≥ 0.85 → FAIL |

**Runner:** deterministic rails/curl probes first; `jev ask` / desk helpers on residual.  
**Tee:** every `jev ask` (state + questions + answers) into TUI + wrap — see ticket CLI seed.  
**On fail:** stop; do not Send; do not write fingerprint via SQL/`update!` on #341.

## Implementation phases

1. Preflight snapshot + TST clear (journals=0 only) → harness `preflight_clear`
2. WUT export PBR 794 + seed/fingerprint assert/`force_lab_uncapped` patch
3. Checkpoint → dry-read body; Operator confirms lock hash still desired
4. POST adopt → harness `action_adopted` + `fp_lock`
5. Re-activate force → harness `mode_d_bind` + `siblings_untouched` + `no_send`
6. Update paper-send ticket evidence; in-band wrap

## Out of scope / non-goals

- SQL or console `update!` of fingerprint on OP or TS #341
- Mutating Mode C Copper #1581
- Desk Send / `place_order` / paper covered-call
- IBKR permission changes
- Repeating `Portfolio.create!` cutover for lineage
- Claiming heat improved Edge_R
