# ADR-001: Majestic Monoliths with Multi-Channel Coordination

**Status:** Accepted
**Date:** 2026-06-12
**Deciders:** Architecture (seeded from principles/00_majestic_monoliths_and_vision.md)
**Source:** `principles/00_majestic_monoliths_and_vision.md`, `principles/01_core_principles.md`

## Context

The Winston trading ecosystem spans data acquisition, backtesting, live operations, and agentic coordination. We needed an architecture that supports independent development and deployment of each concern while allowing clean composition.

Three approaches were considered:

- **Approach A: Single monolith** — one Rails app for everything
- **Approach B: Microservices** — many small services with shared nothing
- **Approach C: Majestic monoliths** — focused complete apps coordinated via narrow interfaces

## Decision

We chose **Approach C: Majestic monoliths** with four focused applications:

1. **data_manager (DM)** — data acquisition and parquet standard
2. **winston_unit_test (WUT)** — backtesting and daily ops lab
3. **winston_v2 (Wv2)** — live operational trading
4. **Cromwell** — agentic coordinator (runtime in `ai/`, not yet a standalone monolith)

Cross-monolith coordination uses:

- REST/JSON internal APIs (token-authenticated)
- Sidekiq jobs (within each monolith only)
- Webhooks (especially DM → Cromwell, Wv2 → Cromwell)
- File mounts (DM parquet tree, `portfolio_configs/` JSON exchange)
- MCP tools (Wv2/DM agent surface for Cromwell)

Podman compose at sawtooth root is the local runtime. AI layer is strictly optional via compose profiles.

## Rationale

### Why not a single monolith?

Data acquisition, backtesting, and live trading have different release cadences, scaling needs, and failure domains. A single app would couple EODHD outages to live trading evaluation and make the codebase unwieldy.

### Why not microservices?

The team size and domain complexity do not justify the operational overhead of many small services. Each monolith is already a complete Rails app with its own PG, Sidekiq, and deployment story — "majestic" means independently valuable, not fragmented.

### Why majestic monoliths?

- **Independent deployability** — DM can update parquet logic without redeploying Wv2
- **Clear ownership** — DM owns data; Wv2 owns live portfolios; WUT owns vetting
- **Narrow coordination** — webhooks, file mounts, and MCP prevent tight coupling
- **WUT as reference** — mature patterns exist; new work adapts rather than reinvents

## Consequences

### Positive

- Each monolith can be developed, tested, and deployed independently
- Cross-monolith contracts live in `ecosystem/interfaces/` as explicit artifacts
- Cromwell and MCP provide an auditable agent surface without duplicating business logic

### Negative

- Cross-monolith changes require coordination across repos and compose
- File-based handoffs (`portfolio_configs/`) need discipline to keep strategy names in sync

### Risks mitigated

- Tight coupling → prevented by narrow APIs and file-based data standard
- Knowledge loss → `ecosystem/` as general contractor knowledge base