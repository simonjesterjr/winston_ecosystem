---
name: operator-prose
description: >
  Operator-facing communication: expand every acronym on first use in a
  discussion (e.g. Trend Following (TF), then TF; Compound Annual Growth Rate
  (CAGR), then CAGR). Use for all chat replies to the human operator, session
  recaps, score interpretations, and strategy discussion — not only formal
  stakeholder docs.
metadata:
  short-description: "Expand acronyms before using them with the operator"
---

# Operator prose — no bare acronyms

## When this applies

**Always** when writing to the human operator in this workspace:

- Normal chat answers and analysis
- Scorecards interpreted in prose
- Strategy / risk / portfolio discussion
- Session handoffs and “what we learned” summaries
- Ticket or analysis prose meant for the operator to read

Does **not** force expansion inside:

- Code identifiers, file paths, ENV keys, or API field names
- Tables that already expanded the term in a header or caption above
- Second and later uses **in the same reply** after a correct first expansion

## Rule

1. **First use in a reply (or distinct section):** full phrase, then acronym in parentheses.  
   Examples:
   - Trend Following (TF)
   - Compound Annual Growth Rate (CAGR)
   - Portfolio Backtest Run (PBR)
   - One-Way Dynamic (OWD)
   - Maximum drawdown (max DD) — or keep “maximum drawdown” if rare
   - Trading Strategy (TS)
   - Winston Unit Test (WUT)
   - data_manager (DM) — product name + short form

2. **Later in the same reply:** the short form is fine (TF, CAGR, PBR, …).

3. **New reply / new session:** expand again on first use. Do not assume the operator still has the expansion in working memory from yesterday.

4. **Stack of jargon:** expand each new acronym the first time it appears; do not open a paragraph with three bare acronyms.

5. **Prefer plain words when the acronym adds nothing:** e.g. “maximum drawdown” once is often clearer than “Max DD (MDD)” if you never need MDD again.

## Domain short forms (expand first, then use)

| Short | Expand first as |
|-------|-----------------|
| TF | Trend Following (TF) |
| CAGR | Compound Annual Growth Rate (CAGR) |
| PBR | Portfolio Backtest Run (PBR) |
| TS | Trading Strategy (TS) |
| OWD | One-Way Dynamic (OWD) |
| OWDC | One-Way Dynamic Close (OWDC) |
| ATR | Average True Range (ATR) |
| DD | drawdown (DD) or maximum drawdown |
| WUT | Winston Unit Test (WUT) |
| Wv2 / WV2 | Winston v2 (Wv2) |
| DM | data_manager (DM) |
| PCS | Portfolio Correlation Score (PCS) — or the project’s current full name from CONTEXT |
| DAR | Daily Analysis Report (DAR) if that is the local meaning |

If unsure of the local expansion, look up `ecosystem/CONTEXT.md` or write the concept in plain English without an acronym.

## Anti-patterns

- “S4 TF under NBO with OWD ladder A: CAGR 19%, DD 43%, Calmar …” with no expansions
- Using **Calmar**, **Sharpe**, **SoT**, **SoS** without saying what they are on first use
- Assuming UI labels (PBR, TS) are self-explanatory in a long strategy narrative

## Good pattern

> Under next-bar-open fills, the best Trend Following (TF) recipe on Mint was FastBO5. Compound Annual Growth Rate (CAGR) was about 19% per year with a 43% maximum drawdown. That CAGR is solid TF, not exceptional low-risk performance.

## Relation to other skills

- **`stakeholder`:** already requires introducing abbreviations; this skill applies the same discipline to **everyday operator chat**, not only outward emails.
- **Code / tickets / IDs:** keep `PBR 246`, `TS #48`, experiment keys as-is after the prose has expanded the concept once if needed.
