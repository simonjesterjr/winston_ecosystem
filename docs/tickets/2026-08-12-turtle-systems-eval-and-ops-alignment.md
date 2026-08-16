# Ticket: Turtle systems eval + heat + capital + ops voice

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-08-12  
**Monoliths:** winston_unit_test, winston_v2, ecosystem  
**BA:** `ecosystem/business_analysis/2026-08-12-turtle-systems-and-heat.md`  
**Heat:** `2026-07-25-ts-portfolio-heat-unit-limits.md`  
**Telegram issue:** `docs/issues/2026-07-28-telegram-operator-interface-wrong-chatbot-tone.md`

---

## Goal

Re-ground Winston lab and ops in Faith-style Turtle systems:

1. Lab matrix: S1 (20/10 ± skip-after-winner) and S2 (55/20), **0.5N** pyramids, **no vol exit**
2. Required books include **Blue** and **Mango** (window-fit hypothesis)
3. Portfolio discovery for another Mint-class exclusive book
4. Multi-level heat (L1–L4) on TS + PBR
5. DAR / PositionSizer: size on **risk_equity**, report free cash separately
6. Ops shell layout polish + Telegram operator voice

---

## Workstreams (checklist)

### 0 — Spec freeze

- [x] BA chassis + unit + heat + capital decisions
- [x] Classic Faith S1/S2 used (share unreadable)

### A — Lab knobs + matrix

- [x] `Breakout10DayStrategy` (S1 exit) — WUT + Wv2 registry/lookback
- [x] `skip_next_after_winner` in WUT PBR runner + unit specs
- [x] Matrix setup + scorecard; **24 PBRs #424–447** hybrid price-level fill
- [x] Score + window-fit — BA `business_analysis/2026-08-12-turtle-hybrid-price-scorecard.md`
- [x] Promote: **TS#77 Mint S2**, **TS#75 Yellow S1**; reject Blue; skip not global — TS descriptions updated

### B — Portfolio discovery

- [ ] **Portfolio Walnut** exclusive Mint-class (PCS ~90+) — agent thread in progress

### C — Heat L1–L4

- [x] TS `risk.heat` + fingerprint — Phase 1 2026-08-14 (`PortfolioHeatConfig`, export, capture, TS/PBR forms)
- [x] Correlation groups — Phase 2 2026-08-14 (`PortfolioHeatClusterResolver`, pairwise \|ρ\|)
- [x] PBR enforcement + pass reasons — Phase 3 2026-08-14 (`HeatCapacityGate`; heat_* pass reasons)
- [x] Wv2 desk gate — Phase 4 2026-08-14 (`DeskHeatGate` on DA enter/pyramid drafts)

### D — Wv2 promote

- [x] Handoff winners; recipe audit; no silent Engaged mutation
  (#797 Mint S2 `85730621` force-Active vs #384; #798 Yellow S1 `7aa73357` Active; #383 closed path B)

### E — Capital / DAR

- [x] `risk_equity` helper; PositionSizer; DAR dual metrics; specs
  (2026-08-12: `Operations::RiskEquity`; sizer uses risk_equity; DAR payload/MD/PDF show free cash + risk equity + over-deployed flag at 25% / negative cash)

### F — Ops shell + Telegram

- [ ] Layout fixes (operator-listed) — list still unwritten; walk `/operations` next UI session  
  See: [`2026-08-12-1541-dar-risk-equity-desk-stop.md`](../session-reports/2026-08-12-1541-dar-risk-equity-desk-stop.md) §14
- [ ] Persona / skill / reply_text hardening; live observe

---

## Matrix cells (A)

| Cell | System | Skip-winner | Portfolios |
|------|--------|-------------|------------|
| A1 | S1 | off | Blue, Mango, Mint, Yellow, Orange, Red, Green, Rust |
| A2 | S1 | on | same |
| B1 | S2 | off | same |
| Control | S4 FastBO5 | n/a | Blue, Mango (± Mint/Yellow) |

---

## Acceptance (program)

- BA frozen; S1/S2 fingerprints exist
- Scorecard with Blue/Mango window table
- Heat enforceable in lab when Phase C done
- Sizing uses risk_equity; DAR shows free_cash + risk_equity
- Telegram stays directed operator voice

## Commands (as landed)

```bash
# Setup Turtle matrix PBRs (idempotent)
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/turtle_systems_v1_setup.rb

# Score (after runs complete)
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/turtle_systems_v1_scorecard.rb WRITE=1
```
