# Ticket: Copper #1585 — fingerprint adopt via PortfolioConfigImporter

**Status:** Blocked  
**Priority:** P1  
**Date:** 2026-09-25  
**Lane:** A  
**Implementer:** Grok CLI  
**Parent:** [Mode D phase 2](2026-09-24-mode-d-phase-2.md)  
**Blocks:** [Mode D phase 2 — paper send](2026-09-24-mode-d-phase-2-paper-send.md)  
**Plan:** [`../../plans/copper-1585-fingerprint-importer-adopt.md`](../../plans/copper-1585-fingerprint-importer-adopt.md)  
**DoD:** OP #1585 adopted via `POST /internal/portfolios` with Operator fingerprint `d627cd79…` on OP + linked TS (not #341); Mode D + DUT070450 bind intact; #1581/#341 untouched; re-activated with `force=true`; paper Send still not done.  
**Human gates:** Operator-named fingerprint lock below; no Desk Send in this ticket; no SQL fingerprint writes; no `TradingStrategy#341.update!`.

## Operator-named fingerprint (lock)

- Full: `d627cd795b410360aff56706dec38759d48f7d32f7cfac4203a29523e2c7c666`
- Short: `d627cd79…`
- Source: WUT PBR #794 capture (heat + RST + window) — live WUT export already emits this hash (2026-09-25 glance); not yet a Wv2 TS selection until adopt.

## Goal

I want #1585's null fingerprint fixed the desk-correct way: service-path adopt through `Operations::PortfolioConfigImporter`, not another rails `Portfolio.create!` / `update!` stamp. After adopt + re-activate, paper Send can clear its fingerprint gate on the paper-send ticket — Send itself stays Operator-only and out of this ticket.

## Context / specimens

- Mint root cause: [`../analysis/2026-09-24-copper-794-mode-d-cutover.rb`](../analysis/2026-09-24-copper-794-mode-d-cutover.rb) used `Portfolio.create!` and skipped the importer.
- Diagnosis note: [`../analysis/2026-09-25-copper-1585-null-fingerprint-importer-path.md`](../analysis/2026-09-25-copper-1585-null-fingerprint-importer-path.md)
- DUT bind: [`../analysis/2026-09-24-walnut-unbind-1585-dut-bind.json`](../analysis/2026-09-24-walnut-unbind-1585-dut-bind.json) — `bnd_3d6a5020d839c315583277d2` / DUT070450
- Live preflight risk (2026-09-25): #1585 markets include leftover **TST** (TestDesk residue) → must clear before POST or importer forks instead of adopts
- Live WUT export risk: `seed_name` is `Portfolio Copper` → must override to #1585's exact seed (`Portfolio Copper · mode-d-from-wut-794` expected)
- ADR-006 lineage; importer always lands inactive

## Work items

- [x] Read-only preflight snapshot: journals=0 / not engaged; exact `seed_name`; Mode D; DUT bind; markets (±TST); #1581/#341 baseline — clean at 15:44:18Z, then superseded (see Results)
- [ ] Clear leftover TST book on #1585 (journals=0 only); re-read markets = Copper 11 — **stopped**: journals became 1 before destroy
- [ ] Export WUT PBR 794; assert fingerprint == Operator lock; patch `seed_name` + `force_lab_uncapped: true` — export read and lock matched; body not patched or posted
- [ ] `POST /internal/portfolios` — expect `action=adopted`, portfolio id 1585, active false, TS id ≠ 341 — **not called**
- [ ] `POST /internal/portfolios/activate` with `force=true` — **not called**
- [ ] Verify fingerprint on OP + new/found TS; Mode D + bind intact; #1581/#341 unchanged; no Send — siblings untouched because no write; fingerprint still null
- [x] Record evidence on paper-send ticket; leave Send blocked until that ticket's remaining gates clear
- [x] System One harness (below) tee'd into TUI + wrap — `preflight_clear` failed closed

## System One harness

**State:** preflight JSON; patched adopt body (seed, fp, markets, force_lab_uncapped); POST response; post-activate snapshots of #1585 / new TS / #1581 / #341.

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| preflight_clear | Noul | journals=0, seed exact, TST absent, Mode D + DUT bind before POST | noul ≥ 0.85 |
| action_adopted | Noul | POST action=adopted on id 1585 (not forked/created) | noul ≥ 0.85 |
| fp_lock | Noul | OP + linked TS fingerprint equal full Operator lock; TS id ≠ 341 | noul ≥ 0.85 |
| mode_d_bind | Noul | After re-activate: mode_d, leap_fulfillment none, DUT bind unchanged | noul ≥ 0.85 |
| siblings_untouched | Noul | #1581 still Mode C on #341; #341 fingerprint still null | noul ≥ 0.85 |
| no_send | Noul | Did this work Desk-Send or SQL-stamp fingerprint? | noul ≥ 0.85 → FAIL |

**Runner:** rails/curl probes first; `jev ask` / `ecosystem/scripts/jev-desk-helpers.sh` on residual.  
**Order:** deterministic first; Jev on residual smells.  
**On fail:** stop · update ticket · do not Send · do not `update!` #341.

## CLI seed (Grok CLI)

```
cwd: /home/johnkoisch/Documents/com/sawtooth
Lane A. Adopt Operator fingerprint d627cd79… onto Wv2 OP #1585 via POST /internal/portfolios (PortfolioConfigImporter). Clear TST leftover first. Patch WUT PBR 794 export seed_name to exact #1585 seed + force_lab_uncapped true. Expect action=adopted on 1585; re-activate force=true; verify Mode D + DUT070450 bind; leave #1581/#341 untouched. No SQL fingerprint writes. No Desk Send.
Follow ticket ecosystem/docs/tickets/2026-09-25-copper-1585-fingerprint-importer-adopt.md and plan ecosystem/plans/copper-1585-fingerprint-importer-adopt.md.
System One harness on the ticket. Tee every jev ask (state + questions + answers) into TUI + wrap.
Push ecosystem main. In-band wrap.
```

### CLI seed — tee Jev System One (default)

At every System One checkpoint in this ticket/plan:

1. Print a clear TUI banner: `=== Jev System One ===`
2. Print the **state** blob (facts / probe JSON / autopsy excerpt) verbatim.
3. Print each question (Noul / Choice / Score) before calling `jev`.
4. Run `jev ask` (desk: `jevctl` / `ecosystem/scripts/jev-desk-helpers.sh`); do not silently skip when `TYPESAFE_API_KEY` is set.
5. Print the JSON answers (and confidence) in the TUI; append the same block to the in-band wrap / ticket Results.
6. Branch fail-closed on harness pass rules. Deterministic probes run first; Jev judges residual semantic smells only.

If Jev is unavailable, print `Jev skipped: <reason>` and continue only if the ticket allows probe-only; never pretend Jev passed. Prefer `jevctl` over the TypeSafe Python SDK.

## Results (2026-09-25)

Adopt **did not run**. `POST /internal/portfolios` was not called. No fingerprint write. No Desk Send. TST book **2010** is still on #1585. #1581 and Trading Strategy #341 were not written.

Clean snapshot at `2026-09-25T15:44:18Z` (`docs/analysis/2026-09-25-copper-1585-fingerprint-adopt-preflight.json`): journals 0, not engaged, seed `Portfolio Copper · mode-d-from-wut-794`, Mode D, bind `bnd_3d6a5020d839c315583277d2`, markets included TST.

Thirteen seconds later `Operations::TaskGenerator#create_draft_journal` inserted journal **2105** (MSFT, status `draft`, notes `UAT fake enter`, not executed) and pending task **1918**. Re-read at `2026-09-25T15:50:01Z`: journals 1, `engaged?` true. The TST destroy script aborted on `journals=1` before `destroy!`. Stop evidence: `docs/analysis/2026-09-25-copper-1585-fingerprint-adopt-engaged-stop.json`.

Winston Unit Test `GET /internal/portfolio_config?run_id=794` returned fingerprint `d627cd795b410360aff56706dec38759d48f7d32f7cfac4203a29523e2c7c666` (matches the lock) and seed `Portfolio Copper`. That body was not patched and not posted.

### Jev System One

```
=== Jev System One ===
checkpoint: preflight_clear + no_send
```

State: the stop JSON above (journals 1, TST present, POST not attempted, no SQL fingerprint write).

Questions:

- `preflight_clear` (Noul): Before any portfolio import POST, does this state show journal count 0, seed_name exactly Portfolio Copper · mode-d-from-wut-794, TST absent from markets, fulfillment_mode mode_d, leap_fulfillment none, and broker_binding_id bnd_3d6a5020d839c315583277d2?
- `no_send` (Noul): Did this work Desk-Send an order or SQL-stamp a fingerprint onto a portfolio or trading strategy?

Answers (`jev-1.13.0`):

```json
{
  "preflight_clear": { "type": "noul", "noul": 0.04 },
  "no_send": { "type": "noul", "noul": 0.04 }
}
```

`preflight_clear` 0.04 is below 0.85, so the gate fails and the adopt stays stopped. `no_send` 0.04 is below 0.85, so the inverted fail rule does not trip.

Later checkpoints (`action_adopted`, `fp_lock`, `mode_d_bind`, `siblings_untouched`) were not asked. There is no POST result to judge.

**Resume:** Operator decides whether draft journal 2105 and task 1918 may be removed. Only a journals=0 book can clear TST and adopt. Do not SQL-stamp the fingerprint.

## Non-goals

- Desk Send / `place_order`
- SQL or console fingerprint `update!` on OP or TS #341
- Mutating Mode C Copper #1581
- Repeating `Portfolio.create!` cutover for lineage
- IBKR permission changes
