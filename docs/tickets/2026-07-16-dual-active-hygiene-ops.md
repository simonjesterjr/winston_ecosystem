# Ticket: Dual-Active hygiene after paper smokes

**Status:** Proposed  
**Date:** 2026-07-16  
**Source:** Session `2026-07-16-1529-paper-fill-desk-handoffs-wrap.md`  
**Domain:** ADR-006 Active mutex

## Problem

After transfer/activate/book smokes, multiple OPs may be Active (`#12` Blue, `#157` Blank, Orange, Rust). Daily Analysis and ops “focus” (lowest Active id) become noisy.

## Scope

1. Operator decide sole focus Active OP  
2. Deactivate extras via shell/MCP (`deactivate`)  
3. Optional: document preferred sole-Active paper hygiene  

## Acceptance

- [ ] Sole intended Active OP for paper desk  
- [ ] Ops focus panel matches operator intent  
