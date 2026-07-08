# Ticket: Vet Portfolio White trend strategies

**Status:** Proposed

**Date:** 2026-07-08

**Context:** Session [`2026-07-08-1744-portfolio-overlap-orange-white-eval-gates`](../session-reports/2026-07-08-1744-portfolio-overlap-orange-white-eval-gates.md). White membership built (CPER, 20 markets). Prefer after Orange vet for lab throughput.

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
