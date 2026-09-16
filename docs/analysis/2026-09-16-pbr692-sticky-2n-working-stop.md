# PBR #692 Working Stop — sticky 2N vs sticky 20D_BO

**Banner:** report only — no pack promotion · no stamps · no production DB writes.  
**Date:** 2026-09-16 (America/Denver)  
**Cell:** `red_rst_turtle_r01_leap30k_ts75` · PBR **#692** · TS75 TurtleV1 **S1** Breakout20/10 · RST · leap_fulfillment=all · risk 1% · $30k · heat turtle  
**Question:** Is Working Stop on this LEAP RST path **sticky 2N** (high−2N / low+2N daily trail), or **sticky 20D_BO**?

---

## VERDICT

**No — not sticky daily high−2N; not sticky 20D_BO either.**

**Accurate label:** **pyramid `move_to_last_entry` 2N** (favorable sync on adds only) **+ separate S1 10-Day Breakout channel exits**. Dual doctrine: Working Stop pierce vs channel exit.

John’s continuous-trail hypothesis (*as high−2N moves above last pyramid stop, replace*) is **disproved** for TS75/`move_to_last_entry`. Desk lock **sticky 20D_BO** remains correct for **S2 only**; it must **not** be applied to this S1 LEAP cell.

---

## Code evidence (paths + quoted logic)

Sources: live greps/dumps captured on sawtooth-ai in prior desk sessions (CoS / forensics transcripts). Line numbers as of those dumps (main after PR #36 restore sticky B3 / 20D_BO).

### 1) Day loop always calls trailing then S2 applicator

`portfolio_backtest_runner.rb` — `update_stops_and_check_hits`:

```ruby
evaluator[:position_manager].update_trailing_stops(activity, positions)
apply_s2_20d_working_stop!(evaluator, positions, activity, market_id)
```

Stop-outs use Working Stop pierce on **underlying**, then option mark (LEAP path).

### 2) Trailing ratchet is sticky-favorable — but gated off for this chassis

`position_manager.rb` ~473–497:

```ruby
def update_trailing_stops(activity, positions)
  return if positions.empty?
  return if scale_in_only_stop_strategy?

  direction = positions.first.direction
  current_risk = risk(activity)
  new_stop = calculate_stop(current_risk, activity, direction.to_sym)

  positions.each do |pos|
    if direction == "long"
      pos.update(updated_stop: [pos.updated_stop, new_stop].compact.max)
    else
      pos.update(updated_stop: [pos.updated_stop, new_stop].compact.min)
    end
  end
  # ... at max_pyramid, sync all lots to best_stop ...
end
```

Long: only raise stop (`max`); short: only lower (`min`) — never loosen. **However:**

Lab law (`wut-s2-working-stop-lab.md`):  
> `PositionManager#update_trailing_stops` does **not** daily-trail under `move_to_last_entry` (correct).

Domain law (`turtle-s2-pyramid-and-working-stop.md`):  
> **Not** a daily ATR trail. `move_to_last_entry` only on a **pyramid fill**; 20-day only after **max lots**.

TS75 fingerprint: `stop_strategy="move_to_last_entry"` (same as TS77). So daily high−2N trail **does not run** on #692.

### 3) Sticky 20D_BO path is S2-gated — S1 never enters

`portfolio_backtest_runner.rb` ~1876–1907:

```ruby
def apply_s2_20d_working_stop!(evaluator, positions, activity, market_id)
  return unless resting_stop_touch?
  return unless turtle_s2_recipe?(evaluator)   # Breakout55 + Breakout20 + move_to_last_entry
  # ... only after max pyramid ...
  # take when 20d has passed last-entry 2N; then write_working_stop!(p, level) nightly
end
```

Lab recipe gate: **System 1 (S1) 20/10 is out** — 10-day stays in play while adding; no 20d→WS supersession.

### 4) Pierce path (both systems)

`working_stop_pierce` uses `position.updated_stop || position.original_stop` on underlying OHLC (touch / gap-open under RST). LEAP exits mark option premium after underlying stop/channel decision.

---

## #692 facts (verified aggregates; lot IDs need live machine)

Quoted known panel facts (cross-checked in 2026-09-15 TS75 audit stdout):

| Fact | Value |
|------|--------|
| cell_key | `red_rst_turtle_r01_leap30k_ts75` |
| closes n | 422 (audit) / user: 427 positions all `is_option` |
| exit mix | user: **250 stop** + **172 10d channel**; 0 share closes |
| updated_stop ≠ original_stop | user: **277/427** (consistent with pyramid move-together, not 20d width) |
| underlying stop distance median | user: **~$0.92** ATR-scale (**not** 20-day channel width) |
| edge_r | stored ~886.9; **signal-path recalculated 9.4183 / audit 9.42** |

**Lot tape:** This executor was **box-scoped** (no `ListMachines` / machine Shell). Live Position IDs / per-engagement ratchet sequences for #692 were **not** re-queried this turn. Do not invent IDs.

**Mechanistic expectation for S1 pyramids (to confirm on re-query):**  
On each pyramid fill, all open lots’ `updated_stop` → newest lot’s underlying 2N (`move_to_last_entry`). Never loosen. Between fills, stop flat (no high−2N). Channel exits fire as **10-Day Breakout** independently of WS.

Contrast (S2 Red #672, not #692) — maxed stack shared `updated_stop=111.70` while newest `original_stop≈109.52` shows **20d above last 2N** (sticky 20D_BO). That pattern must **not** appear on #692 if S1 gating holds.

---

## Exit mix implication

| Exit class | Mechanism | #692 |
|------------|-----------|------|
| Stop-out | `working_stop_pierce` on underlying WS (`updated_stop`\|\|`original_stop`), then option mark | ~250 |
| Channel | S1 **Breakout10** (`exit_strategy_ids=[25]`), **not** suppressed under max | ~172 |
| Share closes | — | 0 |

This is **dual doctrine**: WS (2N / last-entry) vs **10d channel exit** — not “WS became the channel.”

---

## Desk-law amendment (precise wording)

**Do not** replace sticky 20D_BO with sticky 2N globally.

**Add (LEAP RST S1 path):**

> **S1 (Breakout20/10) LEAP RST + `move_to_last_entry`:** Working Stop is **last-entry ±2N**, updated **only on pyramid fills** (move-together; never loosen). There is **no** daily high−2N trail and **no** sticky 20D_BO Working Stop (`apply_s2_20d_working_stop!` is S2-gated). The **10-day Donchian remains a channel exit** while adding and after max. Scoreboard language: dual doctrine — **WS pierce** vs **10d channel exit**. Sticky **20D_BO** remains desk lock **only for Turtle S2** (55/20) after max when 20d has passed 2N.

---


---

## Live re-verify on sawtooth-ai (2026-09-16 afternoon)

### Confirmed knobs
- TS75 / PBR #692 `stop_strategy` = **`move_to_last_entry`**
- `leap_fulfillment=all`, `pyramid_atr_multiplier=0.5`, `leap_atr_offset=0.0`

### Code (current main line numbers)
- `position_manager.rb:403-430` — `calculate_stop` = entry/open ± `atr_multiplier × ATR` (2N when multiplier=2)
- `position_manager.rb:470-507` — `update_trailing_stops` early-returns on `scale_in_only_stop_strategy?` which includes `MoveToLastEntryStopStrategy`
- `position_manager.rb:509-515` — `apply_scale_in_stops!` only on new lot
- `portfolio_backtest_runner.rb:1854-1866` — `turtle_s2_recipe?` requires Breakout55 + Breakout20 (+ move_to_last_entry)
- `portfolio_backtest_runner.rb:1877-1907` — `apply_s2_20d_working_stop!` gated by `turtle_s2_recipe?` → **S1 never enters**
- `portfolio_backtest_runner.rb:2249-2250` — day loop still calls both; S1 trailing is no-op; S2 applicator no-op
- `portfolio_backtest_runner.rb:1927+` — pierce on `updated_stop || original_stop`

### Lot tape (#692)
- `moved updated_stop≠original_stop`: **277/427**
- Global never-loosen vs own original: longs **1/422**, shorts **0/5**
- Lone loosen: position **314675** (long 2025-10-22): `orig=16.6888` → `upd=16.6331` after peer **314676** (2025-10-23) booked with wider ATR so last-entry 2N (`16.6331`) sat **below** prior lot’s 2N. Classic `move_to_last_entry` replace — **not** a daily high−2N trail. True “never loosen” would be `max(current, last_entry_2n)` for longs; current strategy does not do that.

Example pyramid wave (market_id 176 / PHYMF-ish stack, Jan 2023):
| id | bar | order | orig_stop | final_upd |
|----|-----|-------|-----------|-----------|
| 314154 | 2023-01-03 | 35.648 | 35.278 | 36.257 |
| 314158 | 2023-01-06 | 35.922 | 35.521 | 36.257 |
| 314162 | 2023-01-09 | 36.324 | 35.910 | 36.257 |
| 314164 | 2023-01-10 | 36.647 | 36.257 | 36.257 |

Stops sync to newest entry’s 2N on adds; no continuous high−2N ratchet between fills.

### Desk-law recommendation (unchanged)
Do **not** rename sticky 20D_BO → sticky 2N globally. **Add S1 LEAP RST clause:** WS = last-entry ±2N on pyramid fills only (`move_to_last_entry`); no daily high−2N; no sticky 20D_BO; 10-day remains channel exit. Optional follow-up: if John wants hard never-loosen, change move-together to favorable-only `max`/`min` vs last-entry 2N (rare ATR-expand case like 314675).


---

## Desk-law lock (John, 2026-09-16)

**Universal desk law is not sticky 20D_BO.**

It is:
1. Every recipe must have an **exit strategy**
2. Positions must have **protective stops**

TS75 obeys: `exit_strategy_ids=[25]` (10-Day Breakout) + `stop_strategy=move_to_last_entry` with `atr_multiplier=2`.

Sticky **20D_BO** remains **Turtle S2 Working Stop methodology only** (after max when 20d has passed last-entry 2N). Do not treat it as the global desk rule.

**Filed:** [`../business-context/exit-and-protective-stop-desk-law.md`](../business-context/exit-and-protective-stop-desk-law.md) · wrap [`../session-reports/2026-09-16-1447-pbr692-working-stop-autopsy.md`](../session-reports/2026-09-16-1447-pbr692-working-stop-autopsy.md)
