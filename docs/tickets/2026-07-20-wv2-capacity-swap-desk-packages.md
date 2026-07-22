# Ticket: Wv2 capacity swap → ordered Desk Handoff packages

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-20  
**Series:** `adr-009-desk-fulfillment` **#5**  
**Domain:** ADR-009  
**Glossary:** Desk Handoff, Passed Signal, Signal Spine

## Problem

At max markets / pyramid contests, **algorithm** must emit one deterministic package (e.g. exit weak ABC + enter XYZ) or algorithmic **Passed Signal** — not multi-choice ER menus. WUT has `PositionSwapEvaluator`; Wv2 DA does not yet emit ordered multi-leg **Desk Handoffs** with out-of-order **warn**.

## Scope (Wv2; may port WUT patterns)

1. Port or reimplement capacity/swap ranking into DA / TaskGenerator path.  
2. Emit one logical handoff id with N linked draft journals/tasks, **ordered** (exit before enter).  
3. Confirm enter while exit open → **warn** (refuse when capacity still full).  
4. Algorithmic pass reason when no valid swap (`max_markets_no_swap`, etc.).  
5. DAR next_steps list package as a unit.  
6. Specs with fixture portfolio at cap.

## Non-goals

- Human multi-choice ER menu as default  
- Auto-execute package without Desk Action  

## Acceptance

- [ ] At-capacity better signal produces ordered exit+enter drafts or algorithmic pass  
- [ ] Out-of-order confirm warns  
- [ ] Package visible as one Desk Handoff in DAR  
- [ ] No open-ended “pick which signal” UI  

## Related

- ADR-009, series #1–#2  
- WUT `PortfolioBacktest::PositionSwapEvaluator`  
- v1 interim: algorithmic pass only until this ships  
