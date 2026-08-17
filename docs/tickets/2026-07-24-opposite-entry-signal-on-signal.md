# Ticket: Opposite-entry “signal-on-signal” (exit vs reverse) — WUT experiment

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-24  
**Monolith:** winston_unit_test (lab first); optional Wv2 ops parity only after BA win  
**Campaign id:** `opposite_entry_sos_2026_07_24`  
**Sequence:** **Follow-on** to [`2026-07-24-close-trigger-signal-strength-one-way-dynamic.md`](2026-07-24-close-trigger-signal-strength-one-way-dynamic.md) (run after Axis A/B `one_way_dynamic_close` conclusions are in hand, or in parallel only if lab capacity allows).

## Problem / opportunity

On an open book, Winston today **does not** treat a completed **opposite** entry stack as actionable.

**Canonical case (ops inspect, not a defect):**

| Date | Book | Flat-book eval | If short were open |
|------|------|----------------|--------------------|
| 2026-04-29 | Yellow OP **330** · ABBV | **ENTRY SHORT** (Swing5 + EMA20) | — |
| 2026-04-30 | same | **ENTRY LONG** (Swing5 + EMA20) | **No reverse / no entry-driven exit** under current rules |

Yellow TS (`92776cfd`): SwingBreakout5Day + Ema20 confirm; exits **Breakout20 + VolatilityExit**; `atr_multiplier=2.0`; **`always_in_market=false`**.

On 4/30 (what makes this the **right** SoS example):

- Open thesis was **short**.
- Price action reversed: Swing5 **long** primary (high / close context vs prior 5d breakout high).
- **And** confirmatory entrance: close **> EMA20** (Ema20Day long).
- **20d** opposite breakout (the *exit* leg for a short) does **not** fire.
- Hard stop / vol may or may not stop the short depending on fill price — that is a separate path.

**Not SoS:** a bare opposite 5-day breakout alone (primary without confirm). That is ordinary range noise relative to this frame. SoS obtains only when the **full confirmatory entrance** that would open a new trade if flat is present in the opposite direction.

So the machine can stay short while a **confirmed** flat-book long thesis is fully formed. Operator read: that confirmed opposite stack is meaningful and should be measured as a **policy**, not assumed either way.

## Product framing (evolved language)

### This is **not** `always_in_market`

| Concept | Intent | Status |
|---------|--------|--------|
| **`always_in_market`** | Early experiment: stay **always long *or* short** in a given market (continuous exposure / regime occupancy) | Legacy flag; **out of scope** as the solution here |
| **Opposite-entry signal-on-signal (SoS)** | A **meta-signal**: while open in direction D, a **confirmed** opposite entrance (primary **and** confirmatory entrance) fires → policy acts | **This ticket** |

SoS is a **signal about the existing position’s thesis**, gated by the **same confirmed-entry methodology** that would open a new trade if flat — not “always hold something,” not bare primary flips, and not merely “exit strategies use opposite breakout windows.”

### What SoS is

1. Book has open position(s) in direction **D** (long or short).  
2. TradingStrategy has **at least one confirmational entry strategy** (hard confirm parents for promotion matrix).  
3. On bar **X**, `TestingStrategy#evaluate_entry` would return **triggered** with direction **¬D** — meaning **all primary and all confirmational** legs true for ¬D (ADR-008 hard path).  
4. That event is the **SoS trigger** — independent of whether structural exit strategies fire.

**ABBV 4/30 template (short → SoS long):**

| Leg | Required for SoS | Example |
|-----|------------------|---------|
| Primary opposite | Yes | Swing5 long (price action clears prior 5d breakout high) |
| Confirmational entrance opposite | **Yes — mandatory** | Close **> EMA20** |
| Bare primary only | **No — not SoS** | Swing5 long while still under EMA20 does **not** trigger SoS |

### What SoS is not

- **Not** reverse-on-primary alone (e.g. “any opposite 5-day breakout while short”).  
- Not high/low vs close strength classes (close-trigger ticket) — though confirm may *use* close (EMA).  
- Not pyramid risk ladder steps.  
- Not swapping max-position capacity across markets.  
- Not changing primary/confirm definitions for *flat* books.  
- Not applicable as the product frame on **confirm-empty** recipes (no confirmatory entrance to gate SoS).

## Desired outcome

1. WUT matrix + business analysis answering whether SoS **exit-only**, SoS **reverse**, or **status quo** wins on frozen parents.  
2. Durable product rule (and, if promoted, fingerprint-visible methodology flag) — **or** explicit reject with evidence.  
3. Case harvest (e.g. ABBV 4/29→4/30) so operators can see policy differences on known dates.  
4. **No silent Wv2 ops change** until BA + fingerprint/export path exist.

## Domain facts (code baseline)

| Layer | Behavior today |
|-------|----------------|
| Entry while open | **Skipped** unless `always_in_market` (WUT `PortfolioBacktestRunner` / single-market `BacktestRunner`) |
| Exit | Configured exit strategies only; breakout exits use **exit** strategy window in **opposite** direction (e.g. short exits on **20d** upside breakout, not Swing5) |
| Confirm | ADR-008: confirmational strategies gate **initial entry only**; not reverse |
| Wv2 inspect | Can show unconstrained opposite entry while flat; open lots do not auto-link SoS |
| Yellow OP 330 | `always_in_market=false` |

Entry horizon and exit horizon can **disagree** (Swing5 enter, BO20 exit) — SoS deliberately reuses **entry** stack for the meta-signal.

## Hypotheses

| Id | Claim |
|----|--------|
| **H1** | A **confirmed** opposite entrance is higher-quality evidence against an open thesis than waiting only for slower structural exit / stop — and higher quality than a bare opposite primary. |
| **H2** | **Exit-only** SoS (flat on confirmed opposite entry; re-enter only on a later flat-book signal) improves risk-adjusted metrics vs baseline without the full whipsaw tax of reverse. |
| **H3** | **Reverse** SoS (exit D + enter ¬D on confirmed opposite stack) helps only if trade count and cost model stay acceptable; may underperform H2. |
| **H4** | Wins concentrate on **short-horizon primary + hard confirm** recipes (Swing5 + EMA/SMA); confirm-empty or slower BO20-only parents are controls / out of product SoS scope. |
| **H5** | Gating SoS on confirm (vs primary-only reverse) cuts flip rate enough to keep costs tolerable; primary-only reverse is a **rejected product path**, not an experiment cell. |

## Locked product rules (for experiment design)

### Trigger (all cells that use SoS) — **confirmational entrance required**

SoS **only obtains** when the methodology includes confirmatory entrance **and** that confirm fires opposite the open book.

| Requirement | Rule |
|-------------|------|
| Open book | Lot(s) in direction **D** |
| Confirm on TS | Non-empty confirmational entry strategy list (**hard confirm** for matrix parents) |
| Opposite stack | Flat-book `evaluate_entry` true for **¬D** ⇒ **primary(s) ∧ confirm(s)** all true for ¬D |
| Bare primary opposite | **Does not** fire SoS, even if primary alone would look like a “reversal” |
| Soft confirm | Prefer exclude from first matrix; if included later, SoS only when confirm path would allow a **full-size** (or policy-defined) opposite entry — not weak soft-only noise |
| Pyramids | Evaluate vs **open book direction**; on trigger exit/reverse **all lots** on that market |
| Structural exits | Independent; SoS may fire when BO20/vol do not |

Implementation shortcut: SoS trigger ≡ “if flat, we would take a **confirmed** entry in ¬D today.” Do **not** implement a separate primary-only reverse detector.

### Cells (one axis)

| Cell | Policy on SoS trigger | Entry same bar after exit? |
|------|----------------------|----------------------------|
| **S0 baseline** | No SoS — current runner | N/A |
| **S1 exit-only** | Exit all lots; stay flat | **No** same-bar re-entry (respect `just_exited` / non-always_in semantics) |
| **S2 reverse** | Exit all lots **and** enter ¬D | **Yes** — reverse is the point; still honor **signal X → fill X+1 open** if that is lab cadence |

### Explicit non-cells (do not conflate)

| Flag / idea | Why not a SoS cell |
|-------------|--------------------|
| `always_in_market=true` alone | Continuous exposure experiment; does not define clean reverse semantics |
| **Primary-only opposite reverse** | Explicitly **not** the product frame (e.g. Swing5 flip without EMA/SMA/Pen confirm) |
| Confirm-empty parents as SoS treatment | No confirmatory entrance → SoS undefined; use only as S0 baseline controls if needed |
| Exit primary = Swing5 (BO5 as exit) | Changes exit strategy set; separate X-axis if needed later |
| Ad-hoc desk reverse without confirmed signal | Ops discretion; not lab methodology |

### Stops / risk

- Freeze parent **stop_strategy**, **atr_multiplier**, **pyramid ladder**, **max_pyramid**, **max_markets**.  
- Prefer parents already on **`move_to_last_entry`** + `one_way_dynamic` (align with close-trigger campaign).  
- After Axis B of close-trigger lands, **optional transfer**: re-run S0–S2 on `one_way_dynamic_close` winners (second matrix, not joint grid on day one).

### Fill cadence

Same as close-trigger Axis C: signal day **X**, action/fill **X+1 open** unless an audited exception is documented. Poisoned fills → file issue, do not promote BA rules.

## Parent selection

| Filter | Default |
|--------|---------|
| **Required for SoS cells** | Non-empty **hard** confirmational entry (EMA20 / SMA20 / Pen25, etc.) |
| Prefer | Swing5 primary + hard confirm — ABBV-class setups |
| Must include transfer | At least one **Yellow / Mint** lineage parent if metrics qualify |
| Also | Blue PBR **80** (ADR-008 Swing5+EMA20) and/or **78** (SMA20) as core |
| Optional control | Confirm-**empty** Swing5 parent (e.g. 62/48) as **S0-only** baseline reference — **do not** apply S1/S2 SoS treatment without inventing a confirm |
| Optional | BO20 + hard confirm parent as transfer / H4 |
| Doctrine | **New PBR IDs only**; never overwrite 44/48/62/80/121/122 |

Freeze live parent metrics into the BA doc before execute (same discipline as close-trigger ticket).

### Suggested first matrix (sketch)

| Priority | Parent | Role |
|----------|--------|------|
| Must | Blue **80** (or live successor) | ADR-008 Swing5 + EMA20 |
| Must | Yellow **122** / OP fingerprint `92776cfd` lineage | Case-aligned book |
| Strong | Blue **78** | SMA20 confirm transfer |
| Control | Blue **62** or **48** Swing5 no-confirm | Isolates confirm × SoS |
| Optional | Orange BO20 confirm child | H4 negative control |

Exact IDs: freeze at execute time from WUT.

## Implementation sketch (lab only)

1. **Annotation / diagnostic (cheap first):** on each bar with open position, compute unconstrained opposite entry; count SoS days; export case list (symbol, D, ¬D, date) — no behavior change.  
2. **Policy hook** in `PortfolioBacktestRunner` day loop (order already: exits → entries → pyramids → stops):  
   - After (or as part of) exit eval, if SoS and cell S1/S2 → force exit reason e.g. `opposite_entry_signal`.  
   - S2: allow same-day opposite entry after that exit (bypass `just_exited` skip **only** for SoS reverse).  
3. **Config surface:** portfolio/PBR flag e.g. `opposite_entry_policy: none | exit_only | reverse` (name TBD; fingerprintable).  
4. **Do not** overload `always_in_market`.  
5. Matrix script pattern: mirror `lib/scripts/close_trigger_experiment_matrix.rb` / confirm-entry matrix.

## Metrics

| Metric | Why |
|--------|-----|
| Total return, max DD, Sharpe / MAR | Primary economics |
| Trade count, avg hold days | Whipsaw / tax |
| **SoS event count** and **SoS→action rate** | Did policy fire? |
| Round-trips ≤ 3 sessions after SoS | Flip cost |
| Win rate / expectancy on SoS-touched trades vs rest | Quality of meta-signal |
| Case table | ABBV 2026-04-29/30 and top-N SoS dates |

## Acceptance

- [ ] Domain note in ticket/BA: SoS ≠ `always_in_market`  
- [ ] Diagnostic pass (S0 + SoS counts) on frozen parents  
- [ ] S0 / S1 / S2 matrix executed (new PBR IDs); metrics logged  
- [ ] BA write-up: `ecosystem/business_analysis/2026-07-24-opposite-entry-signal-on-signal.md` (date may slip to run day)  
- [ ] Promote **or** reject with one-line product rule  
- [ ] If promote: follow-on ticket for fingerprint + handoff + Wv2 daily eval parity  
- [ ] Optional second matrix on `one_way_dynamic_close` parents after close-trigger Axis B  

## Sequencing vs close-trigger / one_way_dynamic_close

```
close_trigger Axis A (close vs H/L)
        ↓
close_trigger Axis B (one_way_dynamic_close risk)
        ↓  (preferred)
opposite_entry SoS S0–S2 on same core parents
        ↓ optional
SoS × one_way_dynamic_close transfer (not day-one joint grid)
```

Rationale: close-trigger changes **what counts as a strong entry**; SoS changes **what an open book does when the opposite entry exists**. Stack them only after each axis has a baseline.

## Related

- Parent campaign: [`2026-07-24-close-trigger-signal-strength-one-way-dynamic.md`](2026-07-24-close-trigger-signal-strength-one-way-dynamic.md)  
- ADR-008 confirmational entry (initial only): `ecosystem/docs/adr/ADR-008-confirmational-entry-and-risk-scale.md`  
- Confirm experiment BA: `ecosystem/business_analysis/2026-07-18-confirmational-entry-experiment.md`  
- Ops case: Wv2 signal inspect `portfolio_id=330` ABBV `as_of=2026-04-29` / `2026-04-30`  
- Code: `TestingStrategy#evaluate_entry` / `#evaluate_exit`; WUT `PortfolioBacktestRunner#evaluate_market_signals` (`always_in_market` gate); Wv2 `Operations::SignalEvaluation` / `SignalInspectPayload`

## Non-goals

- Promoting reverse as desk default without BA  
- Replacing structural exits (BO20 / vol) entirely with SoS  
- **Primary-only “fake SoS”** (opposite breakout without confirmatory entrance)  
- Inventing SoS on confirm-empty recipes  
- Intraday reverse (EOD lab only)  
- Using SoS to gate pyramids (still same-direction ATR adds unless a future ticket says otherwise)
