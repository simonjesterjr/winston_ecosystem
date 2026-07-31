# Business analysis

**Stakeholder- and operator-facing** evaluation of portfolios, strategies, and trading readiness — return, drawdown, survivability, correlation (PCS), capacity, and paper/live recommendations.

This is **not** the same as:

| Folder | Role |
|--------|------|
| `docs/analysis/` | Durable *technical* findings (how a subsystem works, litmus tests, engineering eval) |
| `docs/business-context/` | Domain *rules and explainers* (glossary-adjacent: what a gate *is*, lifecycle semantics) |
| **`business_analysis/`** | *What the lab evidence says we should do* — cohort ranking, promotion candidates, experiment outcomes |

## Naming

- Dated: `YYYY-MM-DD-short-kebab-slug.md`
- Prefer one primary narrative per decision theme; tickets link here rather than copy tables.

## Index

| Doc | Topic |
|-----|--------|
| [2026-07-13-pbr-return-dd-pcs-evaluation.md](./2026-07-13-pbr-return-dd-pcs-evaluation.md) | PBR return/DD/PCS; Blue 44/48 component attribution; passed signals; paper-first recommendation; Level 2 experiment log |
| [2026-07-18-confirmational-entry-experiment.md](./2026-07-18-confirmational-entry-experiment.md) | 20-cell confirm matrix on 62/71/72/57/55; C03 EMA20 winner; soft vs hard; transfer; one-way ladder note (ADR-008) |
| [2026-07-24-close-trigger-signal-strength.md](./2026-07-24-close-trigger-signal-strength.md) | Close vs high/low entry (H1); one_way_dynamic_close strength risk (H2); lab same-day open vs ops T+1 (H3); business rules |
| [2026-07-30-berlekamp-simons-winston-lessons.md](./2026-07-30-berlekamp-simons-winston-lessons.md) | Berlekamp/Simons × Winston: lessons, impact statement, CGT vs Kelly, perpendicular vs parallel strategy families; spawns Kelly + parallel-system tickets |

## Exposure

WUT UI link to this library is tracked in: `docs/tickets/2026-07-13-wut-expose-business-analysis-link.md`.
