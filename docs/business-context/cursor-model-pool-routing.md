# Cursor model-pool routing

**Status:** Active operator desk law  
**Date:** 2026-09-25  
**Owner:** Operator / CoS  
**Related:** [`winston-bot-cli-ai-dlc-contract.md`](winston-bot-cli-ai-dlc-contract.md), [`jev-desk-guardrails.md`](jev-desk-guardrails.md), [`llm-model-pins-and-eval-registry.md`](llm-model-pins-and-eval-registry.md)

## Business context

Cursor usage has two billing/model pools. The last cycle showed **1,732% Other Models vs 1% Cursor Models**; the cycle reset on 2026-09-24. This policy protects the included Cursor pool and prevents an execution convenience from silently becoming an Other Models burn.

The two pools are deliberately separate:

1. **Cursor Models** — the default pool for Cursor cloud agents, including Cursor Grok 4.6 / the included Cursor pool.
2. **Other Models** — Anthropic, OpenAI, or another explicitly named non-Cursor model. Use only when the Operator names that model/provider.

This is a stacked routing rule, not an either/or preference: choose the execution surface first, then keep the model pool inside this policy.

## Routing law

| Work shape | Preferred route | Model-pool rule |
|---|---|---|
| No sawtooth host, compose, container, DUT/IBKR, or watchable-TUI requirement | **Cursor cloud agent** | Default to **Cursor Models**. Do not silently select Claude or another Other Model. |
| Host-bound or watchable work: compose, Rails runner in containers, DUT/IBKR on host, or a session the Operator must watch | **Shared Grok CLI on sawtooth** | Winston **Lane A remains Grok CLI**; do not substitute a cloud agent for host access or a watchable TUI. |
| Any route where a non-Cursor model is genuinely needed | The route above, unless the Operator says otherwise | Escalate to **Other Models only after the Operator names the exact model/provider**. |

The CoS may mention this policy during the weekly LLM scan and glance at pool usage when easy. The scan may propose; it does not authorize an Other Models selection or a new pull/pin.

## Mental model and handoff

The ecosystem process remains: **bots act / CLI codes / AI-DLC remembers / Jev judges**. The route changes which coding surface is used; it does not change ticketing, plans, durable records, Jev checkpoints, or host verification. Link this note whenever a task seed or agent handoff chooses between Cursor cloud and Grok CLI.

When the work is host-bound, use the existing shared, watchable Grok CLI Lane A contract. When it is not host-bound, prefer a Cursor cloud agent and leave the model selector at Cursor Models. Never open a Claude or other Other Models cloud agent merely for convenience.
