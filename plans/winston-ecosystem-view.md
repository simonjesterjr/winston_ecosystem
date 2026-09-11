# Plan: Winston Ecosystem View (WEV)

| Field | Value |
|-------|--------|
| **Status** | In progress — tournament judged 2026-09-07 |
| **Date** | 2026-09-07 |
| **Type** | Cross-monolith operator console (spec + inventory + thin UI) |
| **Mode** | contractor + tournament |
| **Graph nodes** | `ecosystem/`, `winston_v2`, `data_manager`, `winston_unit_test`, `broker_gateway` |
| **Human gates** | No new compose service; no docker.sock; no Capital Activation chrome; no invented BookScore |
| **Contracts** | `ecosystem/interfaces/winston-ecosystem-view-v1.md` |
| **Task tracking** | [`winston-ecosystem-view.md.tasks.json`](winston-ecosystem-view.md.tasks.json) |
| **Poster** | `ecosystem/docs/poster/` |
| **Code** | `ecosystem/ecosystem_view/` |
| **Ops door** | Wv2 `GET /operations/ecosystem` |
| **Tournament** | `plans/winston-ecosystem-view-candidate-{a,b,c}.md` (record, not SoT) |

## Tournament verdict

Three isolated candidates. Scorecard: glossary, no invented services, four planes, inventory-first, code in `ecosystem/`, reactive/mobile, Pulse ≠ PnL, paper/real same schema, YAGNI, expression as TradingStrategy projection.

| Candidate | Thesis | Keep | Drop |
|-----------|--------|------|------|
| **A** | Inventory-first projector in `ecosystem/`; static HTML; Wv2 is one link | Ownership, contracts, UNKNOWN policy, Score Projection, no 5th app | “Wv2 is only a link” — Tailscale `/wv2` cannot see `:3001/:3000/:3003` or `podman` |
| **B** | Console hosted in ops-shell; ADR-005 first paint local-only | Human door, hang-risk rules, local Sidekiq `/2`, cheap OP SQL | docker.sock; aggregating four DBs on GET; claiming host Pulse from Puma |
| **C** | 2.5D CSS/SVG OP rack as primary economic view; DragonRuby rejected | World list, depth=attention band, table↔rack identity, tint=ops current DD, lab PBR as a different object | Game runtime; Pulse/code-health (yields to A) |

**Applied synthesis:** A ownership + B entry + C board math.

## Four planes (never collapse)

| Plane | Question | Views | Must not show |
|-------|----------|-------|----------------|
| **Poster** | How is Winston *supposed* to be wired? | VIEW-01 isometric topology | Live CPU; OP returns |
| **Monoliths** | What repos/desks exist, and what work touches them? | Cuboid catalog + work.json | Invented CodeCity ranks |
| **Code** | How is the estate connected in Graphify? | vis-network node–edge (estate first, drill to monolith) | Pulse health; live CPU |
| **Pulse** | Is work flowing? | VIEW-02 runtime, VIEW-03 queues, VIEW-04 cron, VIEW-05 watermarks, VIEW-06 traces | `return_pct`, Sharpe, PCS |
| **Book Board** | What is the economic reality of **Operational Portfolios**? | VIEW-08 rack+table, VIEW-09 detail, VIEW-10 scoreboard, VIEW-11 promotion | Queue depth as “book health”; WUT `paper_runs` mixed in |

VIEW-06 traces = **UNKNOWN** (no OpenTelemetry in Winston). VIEW-07 = static catalog later; not v1 chrome.

## Canonical short names

| Short | Repo | Host |
|-------|------|------|
| **wv2** | `winston_v2/` | :3002 |
| **wut** | `winston_unit_test/` | :3000 |
| **dm** | `data_manager/` | :3001 |
| **bg** | `broker_gateway/` | :3003 |

AI (`ollama`, `winston_mcp`, `nanobot_cromwell`, `open-webui`) is compose profile `ai`, not a fifth monolith. IBKR Client Portal Gateway is a **host process**, not a container.

## Book Board nouns

World = list of **Operational Portfolios** + Score Projection. A CONTEXT **Book** is membership (`markets[]`).

Depth: Active **real** near, Active **paper** mid, inactive/closed far (`Operations::AttentionBands`). `export_kind` is a mark, not a shelf.

Tint: ops-equity **current** drawdown when the series exists; else UNKNOWN (do not fake 0%). Size: Risk Capital when cheap; else min tile.

Toggle 2D table ↔ 2.5D rack: **same JSON, same numbers**.

## Score Projection (not a BookScore engine)

Project only stored/computed-elsewhere fields. Missing → `{status: "UNKNOWN", reason: ...}`. Never coerce to 0. Never average Pulse into PnL.

Sources: WUT PBR (`total_return`, `max_drawdown`, `practical_sharpe_ratio`); WUT PCS SoT keyed by **books_key** (ADR-007); Wv2 `PortfolioEquitySeries`; Mid-month Scoreboard process scores; DAR `scored` \| `not_scored`.

## Expression Projection

TradingStrategy + fingerprint drawn as brief stages (universe=Books membership, features=Winston EOD parquet, signal=registry classes, filter=Confirmational Entry, sizer/risk=TS+PositionSizer, execution=Desk/BG, ledger=CashEvent+Journal). No `expression_rev` field. No new engine.

## Pulse v1 (honest split)

Adversary correction: `podman ps` and Redis DB indexes are **not** the same constraint. docker.sock is required for containers. Shared Redis `LLEN`/`ZCARD` on `/0../3` is allowed from Wv2 with 0.2s timeouts.

| Fact | Where it can be true |
|------|----------------------|
| `podman ps`, compose drift, image tags | Host CLI only. Tailscale: UNKNOWN |
| Queue depths / retry / dead on Redis `/0../3` | Wv2 GET may peek sibling DBs (0.2s). Also CLI |
| Wv2 Sidekiq `/2` | Wv2 request |
| HTTP reachability of DM/WUT/BG | Short-timeout probes **after** first paint only. Never 20s clients |
| DataCoverage / CompletedNySession | DM rails runner (CLI); Wv2 local `dm_coverages` metadata only |

**Live Pulse finding (2026-09-07):** WUT `expected_returns` depth **227000** (producer-only graveyard: no worker `-q`, `discard_on StandardError` — these jobs do **not** become the dead set). WUT `default` retry **54**, dead **139**. Show on Pulse with retry+dead. Do not paint on the OP rack.

Queue SLOs: **none documented**. Inventory may **flag** depth≥100 / dead≥10. That flag is not `health: degraded` and not a product SLO.

## Architecture

```
ecosystem/ecosystem_view/     catalog, inventory CLI, static console, snapshots
ecosystem/docs/poster/        DSL + isometric HTML
ecosystem/interfaces/         JSON contracts
winston_v2 /operations/ecosystem   ADR-005 first paint: OP metadata + poster + table/rack
```

No new compose service. No docker.sock. No DragonRuby. No OTel collector.

**First paint (Wv2 GET):** `portfolios` columns + `markets` pluck + `trading_strategies.name`. Zero outbound HTTP. Zero parquet. Zero `includes(:journals, :positions)`.

## Backlog (inventory before chrome)

1. Inventory CLI (containers, queues, cron, OPs, watermarks) — **started**.
2. Contracts + poster DSL + this plan.
3. Static console + isometric poster (mobile, dark).
4. Wv2 route + ops-shell header link.
5. Later: code-health catalog, OTel if a collector exists, Capital Activation gate when the service ships, `last.json` if watchdog writes it.

## Adversary (applied)

VERDICT was `broken` on the slogan. Corrections taken: split podman vs Redis; sibling `LLEN` from Wv2; no Pulse on slabs; queue flags ≠ SLOs; v1 rack is attention-band shelves (not RiskEquity isometric — that path hits parquet); first paint still zero parquet. Plane remains named **Book Board** because the operator brief named it; every heading says Operational Portfolios. Expression stays a projection, not a fifth painted plane in v1.

## Key decisions

1. Glossary wins over the user brief’s “book / live / BookScore engine.”
2. Four planes never share a widget.
3. UI projects; engines stay in owner monoliths (ADR-007 for PCS).
4. Host Pulse stays on the CLI until a snapshot file is copied; Tailscale must not lie.
5. 2.5D is CSS/SVG isometric of the OP list, not a game world.
6. Pulse reuses the Poster isometric map. Edges animate only from Redis/Sidekiq busy, named Pulse Work, or DM `/internal/pulse` running symbols (e.g. IBM). Tablets poll every 3s. Book Board is the same cuboid language on attention-band floors. Codebase cuboids are TradingStrategy projection placeholders until a real hotspot tool exists.
7. Named Pulse Work is a Redis HASH on the **owner’s** DB (`wev:pulse:work`) plus `PUBLISH wev:pulse`. The Pulse Work Record is the contract; poll and a later Cable subscriber are both readers. Do not parse sibling Sidekiq args to invent titles. Tickle / health / expected_returns stay silent.

## UNKNOWN (do not paper over)

OTel, CodeCity, FossFLOW, DragonRuby, HDF5, S3, parquet `asof` column, roll calendar, Capital Activation service, `paper_live_hash_ok`, `expression_rev`, `signal_idle_bars`, queue age SLOs, Sidekiq last-error class, IBKR CPGW liveness from compose, DM `GET /status` controller (routed, missing).
