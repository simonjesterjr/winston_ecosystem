# Ticket: Portfolio color edit UI (WUT + Wv2)

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-03  
**Scope:** WUT + Wv2  
**Parent:** [`archive/2026-08-03-portfolio-preferred-color.md`](archive/2026-08-03-portfolio-preferred-color.md) (Done)  
**Session:** [`../session-reports/2026-08-03-1520-portfolio-preferred-color.md`](../session-reports/2026-08-03-1520-portfolio-preferred-color.md)

## Goal

Add an optional preferred-color field on portfolio create/edit forms so operators can set or override chart line color without editing JSON or SQL.

## Context

Preferred color (`portfolios.color`, CSS hex) already ships end-to-end: name-token defaults, WUT PCS Plotly, WUT→Wv2 export/import, DAR PDF and equity-compare charts. Operators currently set color via:

1. Name tokens (e.g. “Portfolio Green” → `#16a34a`)
2. Top-level `"color"` in handoff JSON
3. Direct column update

## Acceptance

- [ ] WUT portfolio new/edit form: optional color input (hex or token); validates via `PortfolioColor.normalize`
- [ ] Wv2 portfolio edit (ops shell if present): same optional field
- [ ] Blank field leaves column null (name/seed resolution still applies)
- [ ] Show swatch preview of `preferred_color` on portfolio show / correlation ranking row (nice-to-have)

## Out of scope

- Changing fingerprint or methodology export shape
- Registry rewrite
