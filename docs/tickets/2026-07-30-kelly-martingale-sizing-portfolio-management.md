# Ticket: Kelly / Martingale sizing in Winston portfolio management (WUT lab → Wv2 daily managers)

**Status:** In progress — **meta risk-scale layer shipped** (WUT); **ADR-010 accepted** (2026-08-09); Wv2 import + PositionSizer port in flight  
**Priority:** P2  
**Date:** 2026-07-30 (updated 2026-08-09)  
**Scope:** Cross-monolith — **Winston Unit Test (WUT)** lab first for evidence; **Winston v2 (Wv2)** portfolio daily managers / Daily Analysis Report (DAR) risk path as operational consumer  
**Rationale source:** `ecosystem/business_analysis/2026-07-30-berlekamp-simons-winston-lessons.md`  
**Maps:**  
- Historical peer S/M/K: `docs/analysis/2026-07-30-sizing-kelly-martingale-pbr-map.md`  
- Meta layer design: `docs/analysis/2026-07-31-risk-scale-meta-layer.md`  
- Product ADR: `docs/adr/ADR-010-risk-scale-meta-layer.md`

---

## Problem

Winston sizes positions with **static risk percentage**, **One-Way Dynamic (OWD)** / **One-Way Dynamic Close (OWDC)** ladders, confirmational soft-mode reduced size (ADR-008), and portfolio/market heat caps. That is a coherent but **heuristic** bet-sizing stack.

Elwyn Berlekamp’s Medallion turnaround emphasized **Kelly-family** sizing: load up when edge is stronger, shrink when weak, maximize geometric growth of bankroll under uncertainty. Separately, operators sometimes conflate **Martingale** (increase size after losses to recover) with aggressive risk. Those are **not** the same family:

| Family | Idea | Risk posture |
|--------|------|----------------|
| **Kelly** | Size ∝ estimated edge / odds; maximize log-wealth | Growth-optimal *if* edge and costs are honest; fractional Kelly for estimation error |
| **Martingale** | Increase size after losses (classic double-to-recover) | **Anti-Kelly**; ruin risk under finite capital and fat tails |

We have never scored Kelly-family policies against current OWD/static controls on frozen entry recipes, nor defined how a winner would surface in **Wv2 daily portfolio managers** (task quantities, DAR risk commentary, journal drafts) without silent Engaged Operational Portfolio mutation.

---

## Desired outcome

1. **Inventory** of every place risk % / unit size is chosen in WUT backtests and Wv2 signal → task → journal paths (code pointers).  
2. **Lab comparison** of sparse sizing packs (static, OWD ladder A, Kelly-family proxies, Martingale baseline with hard caps).  
3. **Scored recommendation:** keep OWD / adopt a Kelly-family policy / reject Martingale (expected for classic form).  
4. If adopt: a thin follow-on for **Wv2 daily manager** wiring only (fingerprint / succession law respected).

---

## Important distinctions (do not blur)

- **OWD pyramid on strength** (size up into continuation) is closer to **anti-Martingale / confidence scaling**, not classic Martingale. Document overlap explicitly.  
- **Confirm soft mode** (reduced size when confirms fail) is already a primitive “edge weak → shrink” move — ADR-008.  
- **Kelly needs an edge estimate.** Proxies must be named (signal strength, inverse realized volatility, rolling hit-rate × payoff). No fictional precision.  
- **Costs and fill honesty matter.** Lab same-day open vs ops next-bar-open is a known variance; Kelly without costs is fiction.

---

## Scope of work

### 1. Inventory (read-only first)

Map:

| Surface | Questions |
|---------|-----------|
| WUT risk evaluators / PositionManager | How `risk_percentage`, OWD ladders, caps become units |
| TradingStrategy fingerprint fields | Which sizing knobs are identity-bearing |
| Wv2 Daily Analysis / signal evaluation | Does ops re-derive size or trust exported TS? |
| Task generator / journal drafts | Where human sees quantity; can daily manager recompute? |
| Portfolio heat / max markets | Interaction with Kelly fraction (global bankroll vs per-Book) |

Cite files; do not invent.

### 2. Candidate policies (lab)

Freeze entries (recommend S4 FastBO5 and/or Blue panel used in prior ladder science). Sparse packs only:

| Pack | Policy | Notes |
|------|--------|-------|
| **S** | Static risk % (control) | Current static baseline |
| **O** | OWD ladder A (control) | e.g. long 2→3→4→6; prior S4 freeze |
| **K1** | Size ∝ signal strength score | Needs strength definition from existing or close-trigger work |
| **K2** | Size ∝ 1 / realized vol (ATR-scaled Kelly-ish) | Bankroll × vol target |
| **K3** | Fractional Kelly from rolling edge estimate | Lab-only; document estimation window; half-Kelly default |
| **M** | Martingale: size up after consecutive losses | **Hard caps** mandatory; ruin metrics required |
| **M′** optional | Capped recovery Martingale | Only if M is educationally useful |

Fingerprint: any policy that changes methodology identity must mint a new TradingStrategy fingerprint when promoted — never mutate Engaged OPs.

### 3. Scorecard

Per pack: total return, max drawdown, Compound Annual Growth Rate (CAGR), Calmar, Sharpe (if available), trade count, worst loss streak, approximate ruin proxy (e.g. equity path min, time under water). Compare to pack **O** and **S**.

Experiment key suggestion: `sizing_kelly_martingale_v1`.  
PBR map: `docs/analysis/YYYY-MM-DD-sizing-kelly-martingale-pbr-map.md` (or business_analysis if capital ranking is the main product).

### 4. Ops fit (Wv2 daily managers)

If a Kelly-family pack wins lab gates:

- How does **portfolio daily management** expose size? (DAR line items, task packages, MCP confirm quantities)  
- Is size **purely** a function of imported TradingStrategy (preferred) or a daily overlay?  
- Overlay without succession = defect risk (fingerprint law / ADR-006).  
- Martingale must not ship to real Execution Mode without principal + ruin analysis (expected: never).

---

## Non-goals

- Live capital on Martingale  
- High-frequency / sub-minute Kelly  
- Replacing human-gated confirm (ADR-009)  
- Joint re-search of entry × exit × risk on full sample (anti-overfit)  
- Implementing production code before lab score and principal review  

---

## Lab progress (2026-07-30)

### Plumbing shipped (WUT)

- Portfolio `@trade_history` on close; passed into entry estimate + `PositionManager`.  
- `KellyRiskEvaluation` added; martingale hardened; defaults static-safe when history empty.  
- `risk_evaluation_strategy` remains PBR + TradingStrategy field (`static` / `martingale` / `kelly` / OWD / …).  
- Optional `risk_evaluation_config` on TS/export (max_multiplier, fractional_kelly, …) — empty ⇒ class defaults.  
- Entry ceiling uses `max_risk_fraction` so M/K are not forced back to base %.

### Yellow three-cell matrix (`sizing_kelly_martingale_v1`)

| Pack | PBR | Ret % | Max DD % | Sharpe | Note |
|------|-----|-------|----------|--------|------|
| S static | 341 | −0.8 | 40.9 | 0.12 | Fair control (not historical 340) |
| M martingale | 342 | +75.7 | **98.8** | 0.84 | Return mirage / ruin DD |
| K kelly | 343 | +44.5 | 39.6 | 0.33 | Best of three quality |

**Scored call (this panel):** reject Martingale; Kelly interesting vs static; more panels before ops.

### Still open

- [x] Full inventory + Wv2 daily manager path (ADR-010; PositionSizer + RiskScaleRecomputer).  
- [x] Multi-book Kelly hybrid panel (`kelly_hybrid_price_level_v1` — Mint/Mango/Yellow).  
- [x] Wv2 wiring: import, scale engine, PositionSizer, Daily Analysis recompute, exit close hook, DAR visibility.  
- [ ] Explain 340 vs 341 absolute drift (same market configs; different trade count) — optional archaeology.  
- [ ] Optional second DNA (Blue) if promoting a specific Kelly fingerprint.

## Acceptance

- [x] Lab experiment key + PBR map filed; packs **S / M / K** scored on Yellow.  
- [x] Explicit recommendation (this panel): **reject Martingale**; **Kelly > static** on return/DD; not yet promote to ops.  
- [x] Inventory written with code pointers (WUT + Wv2) — ADR-010 + handoff + gap plan 2026-08-09.  
- [x] Wv2 daily manager wiring: meta scale on TS.parameters; runtime state on Portfolio; recompute on DA + exit.  
- [x] Hybrid Kelly scorecard: **host-specific** — Mango/Mint favor Winston calendar (wk66); Yellow prefers none. Confirms not global default.  
- [ ] Cross-link results into Berlekamp business analysis §1 (lessons) as evidence update — residual doc polish.

---

## Related

- `ecosystem/business_analysis/2026-07-30-berlekamp-simons-winston-lessons.md`  
- `docs/tickets/2026-07-26-s4-phase2-ladder-mildness.md`  
- `docs/tickets/2026-07-25-owdc-owd-four-cell-matrix.md`  
- `docs/tickets/2026-07-25-ts-portfolio-heat-unit-limits.md`  
- `docs/adr/ADR-008-confirmational-entry-and-risk-scale.md`  
- `docs/adr/ADR-006-operational-portfolio-lineage-and-lifecycle.md`  
- `docs/tickets/2026-07-30-parallel-trading-system-swing-options-intraday.md` (shared risk module candidate for parallel band)  
