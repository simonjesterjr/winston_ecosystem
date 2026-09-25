# Exit strategy + protective stops — universal desk law

**Type:** Domain / desk law  
**Applies to:** Every Trading Strategy (TS) / recipe on the Winston desk (WUT, Wv2 DA, live, paper)  
**Locked by:** John · **2026-09-16**  
**ADR:** none (CoS may elevate later)  
**Evidence:** [`../analysis/2026-09-16-pbr692-sticky-2n-working-stop.md`](../analysis/2026-09-16-pbr692-sticky-2n-working-stop.md) · wrap [`../session-reports/2026-09-16-1447-pbr692-working-stop-autopsy.md`](../session-reports/2026-09-16-1447-pbr692-working-stop-autopsy.md)

## Universal desk law (not sticky 20D_BO)

**Universal desk law is not sticky 20D_BO.**

It is:

1. Every recipe must have an **exit strategy**
2. Positions must have **protective stops**

Sticky **20D_BO** is **Turtle System 2 Working Stop methodology only** — see [`turtle-s2-pyramid-and-working-stop.md`](turtle-s2-pyramid-and-working-stop.md) and lab [`wut-s2-working-stop-lab.md`](wut-s2-working-stop-lab.md). Do not treat sticky 20D_BO as the global desk rule.

## How recipes obey

| Layer | Obligation |
|-------|------------|
| Exit strategy | TS must name at least one exit (channel / signal / time) that can close the trade without relying on stop alone |
| Protective stop | Every open lot has a Working Stop (underlying for extra-modal LEAPs); naked lots are a fail |

The **shape** of the Working Stop and when channel exits are evaluated is **recipe-specific** (S1 vs S2 vs other). Universal law only requires that both layers exist.

## Exemplar — TS75 / PBR #692 (S1 LEAP RST)

Obeys universal law via:

- **Exit strategy:** 10-Day Breakout (`exit_strategy_ids=[25]`) — stays in play while adding and after max
- **Protective stops:** `stop_strategy=move_to_last_entry` with `atr_multiplier=2` (last-entry ±2N; move-together on pyramid fills only; no daily high−2N trail; no sticky 20D_BO)

Dual doctrine on the scoreboard: **WS pierce** vs **10d channel exit**.

## What this is not

- **Not** a mandate that every recipe use sticky 20D_BO
- **Not** a mandate that every recipe use daily high−2N / low+2N trails
- **Not** permission to run without an exit strategy if stops exist, or without stops if an exit strategy exists

## Mode D user acceptance (2026-09-25)

A covered call on an open long does not satisfy the protective-stop obligation. The lot stays naked until a Good Till Canceled (GTC) stop is working at the broker. If the broker cancels that stop, Winston must drop `working` on the journal. Detail: [`mode-d-ops-shell-uat.md`](mode-d-ops-shell-uat.md).

## Related

- Turtle S2 methodology (sticky 20D_BO after max): [`turtle-s2-pyramid-and-working-stop.md`](turtle-s2-pyramid-and-working-stop.md)
- WUT S2 lab phases B1–B4: [`wut-s2-working-stop-lab.md`](wut-s2-working-stop-lab.md)
- LEAP extra-modal (stop on underlying): [`leap-extra-modal-proxy.md`](leap-extra-modal-proxy.md)
