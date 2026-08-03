# Ticket: Align WUT/Wv2 PortfolioColor fallback + from_name

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-03  
**Scope:** WUT + Wv2  
**Parent:** [`archive/2026-08-03-portfolio-preferred-color.md`](archive/2026-08-03-portfolio-preferred-color.md)  
**Session:** [`../session-reports/2026-08-03-1520-portfolio-preferred-color.md`](../session-reports/2026-08-03-1520-portfolio-preferred-color.md)

## Goal

Make `PortfolioColor` hash-fallback palette and name-token extraction identical (or intentionally versioned) across WUT and Wv2 so anonymous portfolios get the same chart color in lab and ops.

## Context

Majestic monoliths intentionally duplicate `PortfolioColor` (no shared gem). Canonical **TOKEN_HEX** matches. Residual divergence:

| Area | WUT | Wv2 |
|------|-----|-----|
| `FALLBACK_PALETTE` | slightly different set/order | slightly different set/order |
| `from_name` | word-scan (`scan(/[a-z]+/)`) | `\b` token match + optional `seed_name` |

Registry color names (Red/Blue/Green/…) already resolve identically. Only non-token names (e.g. “Builder AAL…”) can diverge.

## Acceptance

- [ ] Same `FALLBACK_PALETTE` order and membership in both monoliths
- [ ] Same `from_name` token rules (document seed_name as Wv2-only input to `preferred`)
- [ ] Spec table of anonymous names asserting equal hex in both suites (or shared fixture list copied)
- [ ] Comment in both services: “keep in sync with sibling monolith”

## Out of scope

- Shared gem extraction (ADR-001 still applies)
