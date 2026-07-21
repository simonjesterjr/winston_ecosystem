---
name: winston-ad-hoc-fill
description: Book or exit a fill on an Operational Portfolio. Enter requires Signaled Entry Rule (signal link or force+notes); exit may be unsignaled.
---

# Winston Ad-Hoc Paper Fill (enter + exit)

## ADR-009 policy

- **Enter/pyramid:** **Signaled Entry Rule** — link `signal_task_id` or `signal_journal_id` (DA draft/task), **or** `force=true` + explicit `notes` audit. Prefer **`wv2_confirm_journal`** when a draft already exists.
- **Exit:** **Unsignaled Exit Allowance** — stop-outs and discretionary exits OK without a Winston signal.

## Triggers

**Enter / book**
- "honor the MSFT enter with LEAPs instead of stock" → link `signal_task_id` / confirm journal
- "I bought 54 shares of TSMC at 323.44 for Magenta" → **force=true** + notes (no DA signal) **or** confirm draft if one exists
- "book 45 GGG @ 58.87 on YGF" (naked) → force + notes
- "IBM signaled breakout — buy 2 Jan 2028 150 LEAP calls @ 12.50 on Blue" → `signal_task_id`

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
2. **Symbol** — signal **underlying**; must already be on the OP’s Books
3. **Units** — positive integer from the human (shares **or** contracts for LEAP/option)
4. **Price** — fill price from the human (stock $ **or** option **premium** per share)
5. Optional: `direction` (default `long`), `trade_date`, `stop_price`, `notes`
6. **Signal link (required unless force):** `signal_task_id` and/or `signal_journal_id`
7. **Force override:** `force=true` **and** non-empty `notes` (audit why policy was overridden)
8. **Related instrument** (when not stock):
   - `fulfillment_type`: `leap` | `option` | `proxy` | `option_strategy`
   - LEAP/option **require**: `strike`, `expiry` (YYYY-MM-DD); optional `option_type` (`call` default), `contract_multiplier` (default **100**)
   - Proxy optional: `instrument_symbol` (filled ticker if different)

### Capital / flow (do not invent multiplier)

| Type | Cash impact (enter) |
|------|---------------------|
| stock / proxy | −units × price |
| leap / option | −units × price × multiplier (default 100) |

**Do not call `wv2_book_trade` until the human has stated units and price** (and strike+expiry for LEAP/option). If missing, ask one short clarifying question.

## Exit — required inputs (never invent)

1. **Portfolio** — id or name
2. **Price** — exit fill price from the human
3. **Symbol** *or* **position_id** — enough to uniquely identify the open position
4. Optional: `trade_date`, `notes`, **`reason`** (`units` reserved; full exit only for now)

### Exit reason packaging

| Human speech | `reason` | Journal packaging |
|--------------|----------|-------------------|
| “AMZN stopped out — book exit, no Winston signal” | `external_stop` | `exit_reason=external_stop`, `winston_signal=false`, **Stop-Out Reconciliation** snapshot |
| Discretionary close / I sold it | `discretionary` | same, reason discretionary |
| Generic desk exit | omit or `ad_hoc` | default |

Aliases: `stopped_out`, `broker_stop` → external_stop. Do **not** invent reason; if human only says “exit”, use default `ad_hoc`.

**Stop-Out Reconciliation (ADR-009):** prefer `position_id` when multiple lots; unique symbol OK. Tool stamps `working_stop_at_exit`, `stop_fill_gap`; **warn** (not block) if fill diverges from Working Stop. Multi-lot same symbol without `position_id` → `ambiguous_position` (use `position_id` or `exit_all`).

**Do not call `wv2_exit_trade` until the human has stated price and which position/symbol.** Full close of the matched open lot.

## Playbook — enter

1. If a **pending DAR draft/task** exists for that market → skill `winston-confirmation-loop` (`wv2_confirm_journal`), not book.
2. Resolve portfolio (`portfolio_id_or_name`).
3. Confirm symbol is intended; if market_not_on_books, report and suggest add-market — do not force.
4. Set `signal_task_id` / `signal_journal_id` when human names the signal; else ask once; only use `force=true` + notes if human authorizes override.
5. Call **only** `wv2_book_trade` with explicit args.
6. Reply: paste tool **`reply_text`** verbatim.
7. Stop. No activate/sync/daily-analysis menus.

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
  force: true,
  notes: "desk paper fill — force override no DA draft"
}
```

```
wv2_book_trade {
  portfolio_id_or_name: "Blue",
  symbol: "IBM",
  units: 2,
  price: 12.50,
  fulfillment_type: "leap",
  strike: 150,
  expiry: "2028-01-21",
  option_type: "call",
  signal_task_id: 44,
  notes: "honor breakout with 2028 LEAPs"
}
```

Shell: `enter Blue IBM units=2 price=12.50 type=leap strike=150 expiry=2028-01-21 option_type=call signal_task=44`

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

LEAP pattern:
```
Booked long 2 LEAP IBM 2028-01-21 150 C @ 12.5 type=leap — journal #N OP #… “…”
multiplier=100, cash_impact=-2500.0, capital_base=…, active=…, signal_task=44
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
| `signaled_entry_required` | Need signal_task/journal or force+notes; prefer confirm draft |
| `force_requires_notes` | force=true without notes — ask why |
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
- Invent strike, expiry, or multiplier for LEAP/option fills
- Claim single-lot exit when human asked to flatten multi-lot — use `wv2_exit_all_trades`
- Treat option premium as stock share price for risk sizing (cash uses multiplier)
