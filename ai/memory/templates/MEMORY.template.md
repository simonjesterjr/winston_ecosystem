# Winston / Cromwell Long-Term Memory

Runtime facts only. Workflows live in `skills/`; architecture in `ecosystem/principles/`.

Ecosystem AI version at last seed: see `ecosystem/ai/VERSION`.

## Principals

| Name | Role | Notes |
|------|------|-------|
| (fill in) | | |

## Active Portfolios

| Name | Status | Capital | Markets | Strategy |
|------|--------|---------|---------|----------|
| (agent or human updates after wv2_list_portfolios) | | | | |

## Standing Preferences

- Report delivery: PDF attachment via Telegram, not text links
- Timezone: America/Denver (4:30 PM MT = post-NY-close report cutoff)
- Risk commentary: include passed signals with reasons

## Principal Todos

(Agent maintains from chat + wv2_list_pending_actions)

## Promotion Candidates

(WUT runs under consideration for transfer to Wv2)

## Handoff reply pattern (few-shot)

When transfer succeeds, prefer tool `reply_text` verbatim. Else:

```
Transfer OK — Adopted fingerprint onto existing OP: #6 “Portfolio Orange · 6622b2eb” · 6622b2eb
active=false, execution_mode=paper
```

Never: markets inventory, capital_base list, or “Would you like to check status…”.

## Recurring Decisions

(Learned facts — e.g. fulfillment preferences, portfolio-specific notes)

## Do NOT Store Here

- Tool call sequences → `skills/`
- MCP schemas → `ecosystem/interfaces/`
- Architecture → `ecosystem/principles/`