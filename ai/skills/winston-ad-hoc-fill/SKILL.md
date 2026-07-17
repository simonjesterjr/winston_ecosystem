---
name: winston-ad-hoc-fill
description: Book or exit a free-form paper fill on an Operational Portfolio without a Daily Analysis draft — human-authorized price (and units for enter) only.
---

# Winston Ad-Hoc Paper Fill (enter + exit)

## Triggers

**Enter / book**
- "I bought 54 shares of TSMC at 323.44 for portfolio Magenta"
- "book 45 GGG @ 58.87 on YGF"
- "paper fill long NVDA 10 @ 140 for portfolio 12"

**Exit**
- "I sold all AMZN on portfolio 12 at 250"
- "exit MSFT on Mango at 450"
- "close position 1 on Orange @ 240"
- "AMZN stopped out on Blue — book the exit" → `reason=external_stop`

If a **pending** enter/exit task already exists for that market, prefer skill `winston-confirmation-loop` (`wv2_confirm_journal`) instead of inventing a second journal.

## MCP Tools

| Tool | When |
|------|------|
| `wv2_book_trade` | Ad-hoc **enter** (open/pyramid) |
| `wv2_exit_trade` | Ad-hoc **exit** (close **one** open lot) |
| `wv2_exit_all_trades` | Flatten **all** open lots for a symbol on an OP |
| `wv2_update_stops` | Move stop on **all** open lots for a symbol |
| `wv2_list_portfolios` | Resolve OP id/name if ambiguous |
| `wv2_get_portfolio_status` | Optional verify after book/exit (only if user asks) |

## Enter — required inputs (never invent)

1. **Portfolio** — id or name (resolve “the portfolio” / Active focus only when unambiguous)
2. **Symbol** — must already be on the OP’s Books
3. **Units** — positive integer from the human
4. **Price** — fill price from the human
5. Optional: `direction` (default `long`), `trade_date`, `stop_price`, `notes`

**Do not call `wv2_book_trade` until the human has stated units and price** (or clearly confirmed a quoted fill). If missing, ask one short clarifying question.

## Exit — required inputs (never invent)

1. **Portfolio** — id or name
2. **Price** — exit fill price from the human
3. **Symbol** *or* **position_id** — enough to uniquely identify the open position
4. Optional: `trade_date`, `notes`, **`reason`** (`units` reserved; full exit only for now)

### Exit reason packaging

| Human speech | `reason` | Journal packaging |
|--------------|----------|-------------------|
| “AMZN stopped out — book exit, no Winston signal” | `external_stop` | `fulfillment_details.exit_reason=external_stop`, `winston_signal=false` |
| Discretionary close / I sold it | `discretionary` | same, reason discretionary |
| Generic desk exit | omit or `ad_hoc` | default |

Aliases: `stopped_out`, `broker_stop` → external_stop. Do **not** invent reason; if human only says “exit”, use default `ad_hoc`.

**Do not call `wv2_exit_trade` until the human has stated price and which position/symbol.** Full close of the matched open lot.

## Playbook — enter

1. Resolve portfolio (`portfolio_id_or_name`).
2. Confirm symbol is intended; if market_not_on_books, report and suggest add-market — do not force.
3. Call **only** `wv2_book_trade` with explicit args.
4. Reply: paste tool **`reply_text`** verbatim.
5. Stop. No activate/sync/daily-analysis menus.

## Playbook — exit

1. Resolve portfolio.
2. Prefer `position_id` when the human or desk named it; else `symbol` (latest open lot for that market).
3. Call **only** `wv2_exit_trade` with explicit args.
4. Reply: paste tool **`reply_text`** verbatim.
5. Stop.

## Playbook — exit all / bulk stops (multi-lot)

**Flatten all lots for a market** (human says “close all MSFT on Blue”, “flatten the pyramid”):

1. Resolve portfolio + symbol + price.
2. Call **`wv2_exit_all_trades`** (not loop of `wv2_exit_trade` unless user named one lot).
3. Paste **`reply_text`**.

**Move all stops** (human says “move MSFT stops to 395 on Orange”):

1. Resolve portfolio + symbol + stop price.
2. Call **`wv2_update_stops`**.
3. Paste **`reply_text`**.

Shell equivalents: `exit_all Blue MSFT price=420` · `stops Orange MSFT price=395`

## Examples

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

```
wv2_exit_trade {
  portfolio_id_or_name: "12",
  symbol: "AMZN",
  price: 250.0,
  notes: "desk exit"
}
```

```
wv2_exit_trade {
  portfolio_id_or_name: "12",
  symbol: "AMZN",
  price: 252.0,
  reason: "external_stop",
  notes: "broker stop hit"
}
```

```
wv2_exit_trade {
  portfolio_id_or_name: "12",
  position_id: 1,
  price: 240.0
}
```

## Reply contract

Prefer `reply_text` from the tool.

Enter pattern:
```
Booked long 45 GGG @ 58.87 — journal #N OP #11 “…”
stop=55.0, capital_base=…, active=…
```

Exit pattern:
```
Exited 5 AMZN @ 250.0 — journal #N OP #12 “…” position #1
reason=ad_hoc, capital_base=…, active=…, open=false
```

External stop pattern:
```
AMZN stopped out — book exit, no Winston signal (5 @ 252.0) — journal #N OP #12 “…”
reason=external_stop, capital_base=…, active=…, open=false
```

## Errors

| Code | Action |
|------|--------|
| `not_found` | Clarify portfolio, symbol, or open position |
| `market_not_on_books` | Symbol not on Books (enter only) — report; offer add-market only if user asks |
| `closed_refuse` | OP closed — use open series |
| `invalid_input` | Missing price (exit) or units/price (enter) |
| `invalid_state` | Position already closed |
| `book_failed` / `exit_failed` / `confirmation_failed` | Report message; do not invent a retry fill |

## Never Do

- Invent units, price, symbol, portfolio, or position
- Book or exit without explicit human authorization of the fill
- Use this path when user is **confirming a DAR draft** (use `wv2_confirm_journal`)
- Auto-chain sync / daily analysis after book/exit
- Partial exits within a lot (not supported — full lot only; multi-lot uses exit_all)
- LEAP/options mechanics (not supported — stock only for now)
- Claim single-lot exit when human asked to flatten multi-lot — use `wv2_exit_all_trades`
