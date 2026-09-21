# Loop B evidence — PCS vs OA/cash (Mint / Yellow / Walnut vs Mode C)

**Date:** 2026-09-20 (America/Denver)  
**From:** Forensics (Operator ask via CoS)  
**Seed:** `2026-09-20-loop-eng-dimension-b-portfolio-design-spike.md`  
**Scope:** Evidence only. **No auto re-weight.**  
**Source:** Live WUT `portfolio_correlation_snapshots` + completed `portfolio_backtest_runs` (2026-09-20).

---

## Verdict (short)

| Hypothesis | Read |
|------------|------|
| (1) high PCS ≠ Turtle alpha | **Supported.** Walnut PCS **79.1** (true diversifier) has **no usable LEAP OA panel**; share PBRs are thin/insolvent. Mid-band Mode C (PCS ~61–72) prints large OA/cash. Low-PCS Orange (~25) still prints huge LEAP OA (#683). |
| (2) “non-corr” lore mixed mean\|r\| vs max\|r\|-PCS | **Supported.** Mint/Yellow were narrated as diversifiers but live PCS is **44 / 39** (max\|r\| **0.89 / 1.0**, high_pairs=1). Their **mean\|r\|** (~0.17) looks “low,” matching Orange mean (~0.24) — but corr_v2 is **max\|r\|-first**. Walnut is the only true high-PCS sleeve in that trio. |
| (3) test regime favors trending clusters | **Partially.** Mid-band max\|r\| books (Red/Blue/Indigo/Teal/Copper/Slate) dominate LEAP OA. Extreme high_pairs Orange can still compound on LEAP cash. High max\|r\| **Mint/Yellow** fail (insolvent LEAP). So “cluster = alpha” is too crude — **mid-band geometry + liquid LEAP book** wins; barren/insolvent sleeves fail regardless of lore. |

**PCS scoring vs testing:** **Both.** Lore mis-labeled Mint/Yellow as high-diversifiers (**scoring/narrative error**). Separately, even true high-PCS Walnut **under-tested / underperforms** on available PBRs vs Mode C mid-band (**testing + alpha gap**).

---

## Live PCS (WUT, 2026-09-20)

| Book | pid | PCS | mean\|r\| | max\|r\| | high_pairs |
|------|-----|-----|----------|---------|------------|
| Walnut | 223 | **79.10** | 0.083 | 0.393 | 0 |
| Indigo | 411 | 72.29 | 0.221 | 0.488 | 0 |
| Red | 6 | 71.48 | 0.251 | 0.495 | 0 |
| Blue | 7 | 66.41 | 0.174 | 0.619 | 0 |
| Teal | 412 | 64.86 | 0.190 | 0.627 | 0 |
| Mango | 65 | 64.15 | 0.217 | 0.652 | 0 |
| Copper | 413 | 60.90 | 0.287 | 0.696 | 0 |
| Slate | 414 | 60.83 | 0.292 | 0.696 | 0 |
| Mint | 110 | **44.01** | 0.169 | **0.894** | 1 |
| Yellow | 111 | **38.71** | 0.176 | **0.998** | 1 |
| Orange | 35 | 24.87 | 0.235 | 0.919 | 3 |
| Rust | 66 | 22.99 | 0.221 | 0.974 | 3 |

corr_v2 reminder (ADR-007): score = 100 × (0.50×(1−max\|r\|) + 0.25×high_pair_term + 0.15×(1−mean\|r\|) + 0.10×quality). **Max\|r\| dominates.**

---

## Best LEAP OA scoreboard (prefer `leap_fulfillment=all`, rank by OA)

| Book | Best PBR | risk | OA % | OA DD % | final_cash | Notes |
|------|----------|------|------|---------|------------|-------|
| Teal | **#743** | 2% | **+19992** | 1.9 | ~$6.0M | heat=legacy; Mode C evolved |
| Copper | #710 | 2% | +15931 | 9.0 | ~$4.8M | Mode C |
| Slate | #713 | 2% | +15749 | 9.0 | ~$4.7M | Mode C |
| Blue | #685 | 2% | +11875 | 3.7 | ~$3.6M | Mode C mid |
| Orange | #683 | 2% | +10374 | 12.2 | ~$3.1M | **low PCS**; trust cash/OA (journal short-entry bug) |
| Indigo | #704 | 2% | +8979 | 5.4 | ~$2.7M | pre-evolve; evolved #723 r01 OA +7454 |
| Red | #693 | 2% | +8109 | 5.4 | ~$2.5M | Mode C mid |
| Mango | #686 | 1% | +2795 | 49.4 | ~$0.86M | r02 #687 insolvent |
| Mint | #689 | 2% | **−263** | 180 | −$49k | LEAP insolvent |
| Yellow | #690 | 1% | **−286** | 167 | −$56k | LEAP insolvent (#691 r02 worse) |
| Rust | #697 | 2% | −311 | 150 | −$63k | LEAP insolvent (share/turtle #663 still held elsewhere) |
| Walnut | — | — | **no LEAP OA** | — | — | Only share #498 cash −$236 / #496 cash ~$1k |

Share-only Walnut: **#496** (TS77 1%) cash ~$1068, legacy ret +90%; **#498** (TS75 1%) cash −$236, ret −102%. Not a Mode-C-class compounder on available evidence.

---

## Read for Operator / CoS

1. **Stop grouping Mint/Yellow with Walnut as “non-corr.”** Only Walnut is high-PCS. Mint/Yellow fail the Mode C PCS∈[60,90] gate today.
2. **High PCS is neither necessary nor sufficient** for LEAP Turtle alpha in this panel: Orange wins with PCS~25; Walnut loses/absent with PCS~79.
3. **Mode C mid-band (PCS 60–72) is where the LEAP OA mass lives** in current stamps — consistent with the compile gate, not with “maximize PCS.”
4. **60d forward labels:** not available in this pull (no labeled forward-return table attached to these snapshots). Gap for Dimension B spike — do **not** invent.
5. **No auto re-weight** from this pack. Promote/design still human.

Raw rows: `ecosystem/docs/analysis/2026-09-20-loop-b-pcs-vs-oa-rows.json`

---

## Gaps / next (optional, not started)

- Stamp Walnut LEAP TS75 r01/r02 so Walnut has an apples-to-apples OA cell.
- Attach 60d forward sleeve returns to snapshot dates if Quiver/daily_job history allows.
- Keep Rust promote hold (#663) separate from this PCS lore question.
