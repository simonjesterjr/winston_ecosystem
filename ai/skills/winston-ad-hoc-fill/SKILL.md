---
name: winston-ad-hoc-fill
description: Book a free-form paper fill on an Operational Portfolio without a Daily Analysis draft — human-authorized units and price only.
---

# Winston Ad-Hoc Paper Fill

## Triggers

- "I bought 54 shares of TSMC at 323.44 for portfolio Magenta"
- "book 45 GGG @ 58.87 on YGF"
- "paper fill long NVDA 10 @ 140 for portfolio 12"
- Free-form buy/sell when **no** pending DAR draft exists

If a **pending** enter task already exists for that market, prefer skill `winston-confirmation-loop` (`wv2_confirm_journal`) instead of inventing a second journal.

## MCP Tools

| Tool | When |
|------|------|
| `wv2_book_trade` | **Primary** — ad-hoc book |
| `wv2_list_portfolios` | Resolve OP id/name if ambiguous |
| `wv2_get_portfolio_status` | Optional verify after book (only if user asks or needed to report capital) |

## Required inputs (never invent)

1. **Portfolio** — id or name (resolve “the portfolio” / Active focus only when unambiguous)
2. **Symbol** — must already be on the OP’s Books
3. **Units** — positive integer from the human
4. **Price** — fill price from the human
5. Optional: `direction` (default `long`), `trade_date`, `stop_price`, `notes`

**Do not call `wv2_book_trade` until the human has stated units and price** (or clearly confirmed a quoted fill). If missing, ask one short clarifying question.

## Playbook

1. Resolve portfolio (`portfolio_id_or_name`).
2. Confirm symbol is intended; if market_not_on_books, report and suggest add-market — do not force.
3. Call **only** `wv2_book_trade` with explicit args.
4. Reply: paste tool **`reply_text`** verbatim (or lead with journal id, units, symbol, price, capital_base).
5. Stop. No activate/sync/daily-analysis menus.

## Example

```
wv2_book_trade {
  portfolio_id_or_name: "11",
  symbol: "GGG",
  units: 45,
  price: 58.87,
  direction: "long",
  stop_price: 55.0,
  notes: "desk paper fill"
}
```

## Reply contract

Prefer `reply_text` from the tool. Pattern:

```
Booked long 45 GGG @ 58.87 — journal #N OP #11 “…”
stop=55.0, capital_base=…, active=…
```

## Errors

| Code | Action |
|------|--------|
| `not_found` | Clarify portfolio or symbol |
| `market_not_on_books` | Symbol not on Books — report; offer add-market only if user asks |
| `closed_refuse` | OP closed — book on open series |
| `invalid_input` | Missing units/price/direction |
| `book_failed` / `confirmation_failed` | Report message; do not invent a retry fill |

## Never Do

- Invent units, price, symbol, or portfolio
- Book without explicit human authorization of the fill
- Use this path when user is **confirming a DAR draft** (use `wv2_confirm_journal`)
- Auto-chain sync / daily analysis after book
- LEAP/options mechanics (not supported — stock only for now)
