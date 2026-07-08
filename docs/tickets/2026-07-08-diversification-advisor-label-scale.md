# Ticket: Fix PortfolioDiversificationAdvisor labels for low mean |r|

**Status:** Proposed

**Date:** 2026-07-08

**Context:** Session [`2026-07-08-1744-portfolio-overlap-orange-white-eval-gates`](../session-reports/2026-07-08-1744-portfolio-overlap-orange-white-eval-gates.md). Portfolio White mean |r| ≈ 0.105 was labeled **Weak Diversification**; Orange mean |r| ≈ 0.171 was **Strong Diversification**. Low pairwise correlation should usually mean *stronger* diversification.

## Problem

Rating scale/labels appear inverted or thresholded incorrectly for operator-facing sidecars.

## Scope

1. Read `PortfolioDiversificationAdvisor` thresholds and labels.
2. Align labels so lower mean |r| maps to stronger diversification (unless intentional inverse).
3. Specs for White/Orange-like mean values.
4. Re-emit sidecars optional.

## Acceptance

- Documented scale; White-like 0.10 not labeled “weak” if weak means poorly diversified

## Related

- `winston_unit_test/app/services/portfolio_diversification_advisor.rb`
- Orange/White sidecars
