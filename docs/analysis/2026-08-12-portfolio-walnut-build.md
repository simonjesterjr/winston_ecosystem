# Portfolio Walnut build — exclusive Mint-class book

**Date:** 2026-08-12  
**Monolith:** WUT (`winston_unit_test`)  
**Methodology:** `corr_v2` · quality gates on · fixed window `WINDOW_START=2019-05-08`

## Outcome

| Field | Value |
|-------|--------|
| Portfolio | **Portfolio Walnut** |
| Portfolio id | **223** |
| Seed | **DBC** (Invesco DB Commodity Index Tracking Fund) |
| Markets (10) | BDRY, CVNA, DBC, DD, GE, KR, MRK, ONDS, POET, SCHZ |
| PCS | **91.86** (Mint-class; Mint reference ~91–92) |
| max \|r\| | **0.156** (BDRY/DBC) |
| mean \|r\| | **0.023** |
| high pairs (\|r\| > 0.70) | **0** |
| rating | strong |
| trading days | 1456 (window ~2019-06-06 → 2026-07-21; ONDS trims start slightly) |
| preferred_color | `#78350f` |
| Exclusive | **yes** — zero shared symbols with Red/Blue/Orange/White/Green/Pink/Mango/Rust/Mint/Yellow |

## Seed choice

Tried and discarded for first-pass theme pools:

| Seed | Why not final |
|------|----------------|
| DBC (first theme rake) | Theme-first exclusive pool → PCS ~78 (mid-corr leftovers) |
| TIP / TAIL / WOOD / SIL / NEAR / KMLM | Probes with curated pools maxed ~80–87 |
| Softs (JO/NIB/BAL/COW) | Stale bars through ~2023 — artificial low \|r\|, rejected |
| Levered/inverse (PSQ/SPXS/SQQQ/TMF/UVXY…) | Reverse splits corrupt long-window Pearson → false PCS ~97; denylisted |

**DBC kept** as seed: free (not a prior registry seed), quality-pass, liquid broad commodity basket, thematic fit for “Walnut” real-asset diversifier. Final membership used **rank_vs_seed** over free quality symbols after exclusive peer strip + levered/inverse deny.

## Membership rationale

| Symbol | Role |
|--------|------|
| **DBC** | Seed — broad commodity beta |
| **SCHZ** | Aggregate bond sleeve (cash/bond diversifier; SHY already taken by Mint) |
| **BDRY** | Dry-bulk / shipping — commodity-adjacent, modest \|r\| with DBC |
| **GE, DD** | Industrial single names — low pairwise with book |
| **KR, MRK** | Defensive consumer / healthcare |
| **CVNA, ONDS, POET** | Idiosyncratic satellites (Mint-style leftover quality: cf. APLD/ASTS) |

Largest pair: BDRY/DBC ~0.16 — well under build cap 0.55. No high pairs.

## Artifacts

| Path | Notes |
|------|--------|
| `portfolio_configs/registry.json` | Walnut registered, seed=DBC |
| `portfolio_configs/portfolio-walnut-sidecar.json` | Full corr_v2 sidecar + matrix |
| WUT PG `portfolios.id=223` + 10 books | Snapshot source=`builder` as_of 2026-08-12 |
| `winston_unit_test/lib/tasks/portfolio_cohort_build.rake` | Walnut cohort + `rank_vs_seed` exclusive path |
| `winston_unit_test/app/services/portfolio_overlap_policy.rb` | Seed `DBC` → Portfolio Walnut |
| `winston_unit_test/app/services/portfolio_color.rb` | Token `walnut` → `#78350f` |

## Rebuild

```bash
bin/compose exec -T winston_unit_test bin/rails portfolios:build_new_cohorts[walnut]
```

Exclusive cohorts with `rank_vs_seed: true` (Walnut) expand free quality, strip peers + levered/inverse, rank candidates by avg \|r\| vs seed, then greedy-build under max-pairwise 0.55.

## Blockers / caveats

- **Not committed** — leave for operator review.
- ONDS has fewer bars (~1457) → intersection starts 2019-06-06 rather than 2019-05-08.
- Speculative satellites (ONDS, POET, CVNA) pass quality gates but are thin vs mega-cap liquidity; same pattern as Mint’s APLD/ASTS.
- Turtle PBR matrix **not** run this session.
- Re-running without `rank_vs_seed` / levered deny regresses to ~PCS 78 or inflated levered PCS — do not drop those guards for exclusive books.
