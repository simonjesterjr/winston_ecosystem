# Ticket: Telegram equity compare charts (“Blue vs Mango”)

**Status:** Done  
**Date:** 2026-07-17  
**Done:** 2026-07-17  
**Epic:** `2026-07-17-ops-daily-demo-epic.md`  
**Priority:** Medium (demo polish; not blocking desk loop)

## Problem

Equity series and PDF chart primitives exist, but there is no ad-hoc “show equity of Blue vs Mango” image delivery over Telegram.

## Scope

1. Service: multi-OP equity series → PNG/chart image (reuse PDF chart drawer or new renderer).  
2. MCP or report path that returns media path for Cromwell.  
3. Speech contract for Cromwell skill.  
4. Non-goal: interactive live charts in Telegram.

## Acceptance

- [x] Operator can request compare chart; Telegram receives image  
- [x] Labels match OP display names / short fingerprints  

## Implementation (2026-07-17)

### Design

- **Media format:** single-page **PDF** chart (same delivery path as DAR: `storage/reports` → nanobot `wv2_reports` volume). Telegram attaches via `media=[telegram_media_path]`. Not interactive PNG (no PNG gem; PDF matches proven report pipeline).
- **Series:** `PortfolioEquitySeries` per OP, date-aligned with forward-fill for multi-line overlay.
- **Labels:** display name (e.g. `Blue`) + short fingerprint when present (`Blue · ab12cd34`).
- **Optional** `normalize=true` rebases each series to 100 at start.

### Surfaces

| Surface | Path |
|---------|------|
| Domain | `Operations::EquityCompareChartService` |
| Chart drawer | `ReportPdfChartDrawer` legend for multi-series labels |
| Internal | `GET\|POST /internal/portfolios/equity_compare` |
| Shell | `equity_compare Blue Mango` · alias `equity` |
| MCP | `wv2_compare_equity` + `_meta.delivery` / `reply_text` |
| Skill | `ecosystem/ai/skills/winston-equity-compare/SKILL.md` |

### Example

```text
equity_compare Blue Mango
equity Blue Mango as_of=2026-07-16 normalize=true
```

```json
{
  "portfolios": ["Blue", "Mango"],
  "as_of": "2026-07-17"
}
```

Returns: metrics rows, `pdf_path`, `telegram_media_path`, `reply_text`.

### Specs

`spec/services/operations/equity_compare_chart_service_spec.rb`

## Related

- `PortfolioEquitySeries`, `ReportPdfChartDrawer`  
- Report delivery skill (media attach pattern)  
