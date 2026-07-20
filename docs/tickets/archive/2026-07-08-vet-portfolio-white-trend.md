# Ticket: Vet Portfolio White trend strategies

**Status:** Done (2026-07-09)

**Date:** 2026-07-08

**Last updated:** 2026-07-09 — opt#36 / PBR 40; export observation

**Context:** Session [`2026-07-08-1744-portfolio-overlap-orange-white-eval-gates`](../session-reports/2026-07-08-1744-portfolio-overlap-orange-white-eval-gates.md). White membership built (CPER, 20 markets). Prefer after Orange vet for lab throughput.

**Result:** [`2026-07-09-1308-orange-white-vet-trend`](../session-reports/2026-07-09-1308-orange-white-vet-trend.md) — winner `Breakout50DayStrategy` + `VolatilityExitStrategy`; return +7.3%, max DD 94.1%, trades 738; `portfolio-white.json` `export_kind=observation`.

## Membership (20)

CIZ, CMDT, COPR, CPER, DBE, GOOGL, IWF, OILK, PHYMF, PPLT, PTF, ROKU, SOXX, TAGS, TESL, TILL, WMT, XLB, YOLO, ZROZ

## Scope

1. Run detached:  
   `env PORTFOLIO="Portfolio White" EXPORT=/portfolio_configs/portfolio-white.json bin/rails portfolios:vet_trend`
2. Winner PBR + export with viability gates.
3. Note multi-market (20) wall-clock may exceed Red/Orange.

## Acceptance

- Export + log complete
- `export_kind` set correctly
- Overlap peers unchanged by vet (membership-only vet)

## Related

- Plan task #6
- Orange vet ticket: `2026-07-08-vet-portfolio-orange-trend.md`
