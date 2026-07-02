# Plan: Winston + LLM (Roadmap) — Native Secure Local Models, RAG, Agentic Orchestration

**Status**: Long-term vision and phased roadmap (2026-06-12). Companion to the immediate MCP and next-steps plans. Do **not** start implementation until the MCP access layer (immediate + next) is stable and the principals have used the Cromwell bot on Telegram for real daily flows. This document lives in ecosystem/ as the single source of truth for the "extend WUT and Wv2 to use downloaded/secure LLM natively" direction.

**Relationship to prior work**: The MCP layer (nanobot + ollama + winston_mcp tools) is the **bridge and forcing function**. It proves the value of agentic access, surfaces the exact operations that benefit from LLM augmentation, and gives us traces (tool calls, decisions, journal notes) that become training/ RAG data. The monoliths remain the source of truth and the durable compute; LLM is an accelerator and explainer inside them and in Cromwell, not a replacement for the rule-based risk/position discipline.

## Vision (Why This Direction)
Current Winston is deterministic and excellent at what it does: reliable trend-following signals from vetted strategies, strict risk (ATR, pyramiding, cash events, position limits), full audit via journals + passed_signals, data guarantees via DM parquet (raw + derivatives), async orchestration via Sidekiq, coordination via webhooks/APIs/files.

The opportunity: replace or augment **hard-coded components** (certain analysis heuristics, journal note generation, signal explanation / "why we passed", regime detection, report summarization, dynamic parameter suggestion, data anomaly flagging) with a **secure, local, downloadable LLM** (ollama models we control) so that:
- Analysis and reporting become higher-quality and more adaptive without losing the guardrails.
- The system reasons over its own history (journals, strategies, passed signals, equity curves) in context.
- Cromwell (the agentic coordinator) can orchestrate richer workflows using natural language + tools (MCP today, direct calls tomorrow).
- New capabilities (synthesis across portfolios, "what would the strategy have done in 2022 vol spike?", personalized risk commentary) appear without exploding the Ruby service count.
- Everything stays offline/private where it matters (local models + local data).

**Non-goals**: Do not make the core signal generation a black box. The deterministic strategies (Breakout*, VolatilityExit*, the four risk evaluators, stops) remain the decision engines. LLM augments, explains, drafts, selects among pre-approved options, or proposes config tweaks that a human (or Cromwell) then vets and promotes.

**Key constraints** (from principles):
- Downloaded/secure LLM only for the parts we choose (ollama or vllm-served models we pull and run locally in podman).
- Core monoliths (especially WUT for experimentation, Wv2 for live) can still run and produce correct results with the AI layer completely absent.
- Parquet (DM) + PG metadata/state + journals remain the durable source of truth.
- Async (Sidekiq), webhooks, narrow APIs/MCP surfaces, file exchange (portfolio_configs, reports) continue as the composition model.
- Majestic monoliths stay independently valuable.
- Update ecosystem/ on every material decision.

## Architectural Patterns (Emerging)
1. **LLM as a Service inside the monoliths (optional dependency)**:
   - Add a thin, swappable `LlmClient` (or `OllamaClient`) that talks to http://ollama:11434 (when the ai profile is up) or a configurable local/remote endpoint.
   - Feature-flag or presence-detect: if no ollama or env var `WINSTON_LLM_ENABLED=false`, fall back to the current deterministic paths (template notes, simple strings).
   - Use for: drafting journal notes ("Entry rationale: breakout above 20d with confirmation on ATR contraction..."), explaining passed signals in human language, generating daily report prose, suggesting "consider tightening pyramid on this symbol given recent vol", regime tagging of days, etc.
   - Keep prompts small, versioned (in app/prompts/ or as constants), with few-shot examples drawn from real journals.
   - Output is **always** post-processed + validated before it affects state (e.g. LLM proposes a note; it is stored in journal.notes_draft; human or Cromwell confirms before "executed").

2. **RAG / Memory Layer (local only)**:
   - Journals, passed_signals, operations_tasks, TradingStrategy definitions, Cromwell notifications, and (later) equity series summaries become the corpus.
   - Local embeddings (via ollama or a small dedicated embedding model) + a lightweight store (pgvector extension on the existing PGs, or a separate tiny vector container, or even simple file-based + DuckDB for starters).
   - Retrieval for: "similar past situations for this market", "how did we size risk the last time ATR was this high?", "what notes did we write on successful pyramiding in Portfolio A?".
   - WUT (lab) can have heavier RAG experimentation; Wv2 keeps it lighter and read-only for live decisions.
   - No external vector DBs in v1 of this roadmap (keep it podman-contained and offline).

3. **MCP + Tools as the Agent Contract (already started)**:
   - The immediate/next MCP server (winston_mcp) is the first "orchestration surface".
   - Cromwell (our agent) will be the primary consumer: it receives daily webhooks, maintains todos, decides sequences ("first sync data if needed, then run analysis for the two active portfolios, then prepare the briefing for the 4pm channel"), calls the tools, incorporates LLM-generated explanations into the Telegram messages.
   - Over time, some tool implementations inside the monoliths can themselves call the local LLM (e.g. the report builder asks LLM for the narrative summary section).
   - MCP remains useful even after native calls: it gives external agents (future Cursor, other bots, human operators via a CLI MCP client) the same safe surface.

4. **Orchestration Evolution**:
   - Short term: nanobot (LLM + tools via MCP) + our prompts/skills = "Cromwell bot".
   - Medium: dedicated Cromwell monolith or service (Rails or lightweight) that owns state (todos, run logs, principal preferences), drives via Sidekiq jobs + MCP tool calls + webhooks, and uses the local LLM for planning/reasoning/summarization.
   - It can have its own PG for coordination state (separate from Wv2's journals).
   - Explicit graphs (simple state machine or a small langgraph-style in Python if we add a sidecar) or just well-structured prompts + tool choice.
   - WUT can simulate full agent days for backtesting the orchestration itself (new "agent run" concept?).

5. **Data & Derivative Implications**:
   - DM may later compute additional LLM-friendly features (embeddings of recent regime? volatility regime labels) or simply expose richer parquet sidecars.
   - Reconciliation and coverage remain unchanged.
   - Wv2/WUT will store LLM outputs as jsonb or text columns (drafts, explanations) alongside the deterministic fields — never as the sole decision record.

6. **Deployment & Optionality**:
   - ollama (and optional embedding/vector sidecars) live in the `ai` profile or compose.ai.yml exactly like the immediate plan.
   - Monolith Containerfiles get **optional** stages or runtime detection for LLM client libs (no heavy deps pulled unless the ai profile is built).
   - Local models are pulled explicitly by the operator (`podman compose --profile ai exec ollama ollama pull qwen2.5:14b` or whatever is vetted) and documented.
   - Graceful degradation is mandatory: "AI features disabled (no ollama reachable)" must be a clean log state, not a crash.

## Phased Roadmap (Rough Order — Adjust Based on Real Usage of the MCP Bot)

**Phase 0 (Immediate / Next — foundation)**: MCP tools + nanobot Cromwell bot + ollama container optional. Use the local model inside nanobot for reasoning over tool outputs and phrasing the Telegram reports. Traces collected. Real daily analysis ported. No changes inside WUT/Wv2 services yet.

**Phase 1 — Lightweight Augmentation Inside Monoliths**:
- Add OllamaClient + prompt templates to Wv2 (and parallel experimental area in WUT).
- Use for journal note drafting and passed-signal human explanations (stored separately from the rule-based reason codes).
- Simple RAG over the last N journals for a market when generating the note ("similar to the 2025-03-12 entry on AAPL...").
- Daily report prose generation (the "narrative" part of the Cromwell payload) gets an LLM section.
- WUT gains an "LLM explain this backtest day" button or rake for lab use.
- All gated; default off or no-op when no ollama.

**Phase 2 — Deeper Reasoning & Selection**:
- LLM-assisted signal vetting / ranking (e.g. "given the last 5 passed signals on this symbol and the current regime, should we still take the primary breakout?").
- Dynamic but safe config suggestion: LLM proposes a pyramid multiplier tweak or an extra confirmational strategy from the approved list; human/Cromwell promotes it into a TradingStrategy record (JSON flow preserved).
- Cross-portfolio synthesis for the daily briefing ("Portfolio A and B both see energy names; consider concentration").
- Better "why we passed" that combines the hard rule (e.g. "portfolio max positions") with LLM color ("recent similar setups had 60% follow-through but high drawdown risk").
- RAG index grows to include strategy definitions + historical performance summaries (exported from WUT runs).

**Phase 3 — Agentic Orchestration (Cromwell as first-class)**:
- Cromwell monolith/service appears.
- It owns the daily loop as an explicit workflow: detect trading day, ensure data via MCP/tool or direct, run analyses, collect outputs, ask LLM for high-level commentary and todo prioritization, emit rich multi-recipient notifications (Telegram via nanobot bridge or direct, email stubs, etc.), accept confirmations back via MCP or webhooks.
- Memory: Cromwell has its own long-term store (journals + its own action log + RAG over everything).
- Experiment in WUT: "agent backtests" that replay history with the orchestration layer making tool calls against simulated Wv2 state.
- Possible new sidecars only if justified (light vector DB, a small Python orchestration runtime that still delegates all state changes to the Rails monoliths via MCP).

**Phase 4 — Advanced / Research**:
- Multi-model routing inside the local cluster (fast cheap model for classification/triage, stronger model for final drafting).
- Self-improvement loops: Cromwell proposes new primitive strategies or risk rules; they are implemented as code, backtested in WUT, promoted only after human vetting (the majestic monolith discipline stays).
- Fine-tuning or continued pre-training on our private traces (journals + tool decisions) — only on air-gapped or carefully controlled infra.
- Optional external tools via MCP (carefully firewalled) for news/sentiment that then feed into regime or filter logic (still gated by our risk rules).
- Alternative stores (if PG + parquet + simple RAG hit limits): DuckDB on the side for analytical queries, or a time-series extension, but only after proving need.

## Technical Choices (Guiding, Subject to Validation in Phase 1)
- **LLM runtime**: ollama (already in the stack we evaluated) as the default local server. Models chosen for tool-use / reasoning strength + context length that fits our histories (journals are not enormous). Prefer quantized models that run well on the dev hardware.
- **Client**: lightweight HTTP (httpx in Python sidecars, or a small pure-Ruby or faraday client in Rails). No giant langchain unless it stays optional and slim.
- **Embeddings**: same ollama (nomic-embed or the model's native) or a dedicated small model. Store in pgvector on the monolith's own DB (Wv2 gets a journals_embedding table or jsonb + external index) or a shared tiny vector service in the ai profile.
- **Prompt management**: versioned files or structured constants. Include the Winston principles + current portfolio rules as system context (but keep tokens reasonable; retrieval helps).
- **Safety rails**: every LLM output that can affect money or state is a draft + requires explicit confirmation path (the same one used for deterministic signals). Hard limits on what the model is allowed to output (JSON schema enforcement where possible).
- **Fallbacks everywhere**: the existing deterministic path is always the "safe" one.
- **Observability**: every LLM call logs prompt hash (or truncated), model, latency, token counts, and the correlation id that ties to the journal/task/Cromwell notification.
- **Cost/usage (even local)**: track usage; surface in reports ("LLM assisted 14 notes today").
- **MCP evolution**: the winston_mcp server can grow a `llm_explain` or `rag_query` tool, or the monoliths can expose internal LLM endpoints that the MCP server proxies. Native calls inside services are preferred for latency once stable.

## Risks & Mitigations
- **Drift / loss of determinism**: Mitigation — LLM never mutates positions or risk parameters without an explicit human/Cromwell-approved TradingStrategy or journal record. All core sizing still uses the Ruby risk/position managers.
- **Hallucination in financial advice**: Mitigation — grounding in retrieved real journals + parquet facts + the approved strategy list. Output is commentary, not a trade order.
- **Model availability / size**: Mitigation — document small capable models; make everything degrade. Operator explicitly pulls models.
- **Performance in daily path**: Mitigation — LLM calls are async (Sidekiq jobs) or best-effort for notes; the signal decision itself stays fast and synchronous.
- **Security of local model serving**: ollama in the hardened container from the stack is a good start; we add network isolation (only reachable from winston_mcp, Wv2, Cromwell, nanobot on the compose network).
- **Complexity explosion**: Mitigation — small slices, constant return to "does the core still run cleanly without any of this?".
- **Data leakage**: All local. Prompts never sent to external unless operator explicitly configures a remote provider (and even then, only non-sensitive synthesized context).

## Integration Points with Existing Architecture
- **DM**: Later, may expose "recent regime features" or allow LLM-augmented gap/anomaly detection in acquisition. Notifications to Cromwell get richer.
- **WUT**: Primary lab for LLM experiments (new services under an llm/ namespace, backtest runs can store "LLM commentary" for later RAG). The 65-line rule still applies to Ruby; Python side experiments are fine in a dedicated research area.
- **Wv2**: Conservative consumer of the capabilities. DailyAnalysisJob and ReportBuilder get LLM hooks. CashEvents + journals + positions stay the capital and truth.
- **Cromwell (future)**: The big winner — it becomes the place where LLM planning + MCP tool use + webhook consumption + human chat (via nanobot or direct) all meet. It can maintain the principals' todo list across days.
- **Sidekiq + webhooks**: Unchanged. LLM work is just more jobs or steps inside existing flows.
- **Parquet / volumes**: Unchanged. LLM reads facts from them via the same DuckDB paths or via services.
- **ecosystem/**: This plan lives here. New interfaces (LLM prompt contracts, RAG corpus schemas, Cromwell orchestration events) go here. Principles updated when we lock a pattern (e.g. "LLM outputs are always drafts or commentary until explicitly confirmed").

## Verification Philosophy for This Roadmap
- Every phase must have a "no-LLM" regression test that the previous deterministic behavior is identical.
- End-to-end agent days (via the Cromwell bot or simulated) must be reproducible and auditable (the JSON notifications + journals are the record).
- WUT remains the place where we can safely try wilder ideas (RAG over 10 years of hypothetical journals, agent-orchestrated parameter search) before anything touches live Wv2 money.
- Metrics: quality of notes (human review), reduction in manual explanation work, correctness of signals (still measured against the rule engines), latency impact, token / model usage.

## Open Questions (To Be Resolved in Phase 1 Usage)
- Which exact model(s) give the best quality/size/speed tradeoff for our journal + report style?
- How much context (last 30 journals per symbol? full portfolio history? strategy definitions?) is useful before we need clever retrieval?
- Should the primary RAG store live in Wv2's PG (pgvector) or a shared Cromwell memory service?
- Do we ever want the LLM to propose entirely new primitive strategy code, or only compose from the existing registry?
- How do we version and review the prompts themselves (they are now part of the "strategy" surface)?
- When (if ever) do we introduce a small dedicated orchestration runtime (Python) vs. keeping everything inside the Rails monoliths + Sidekiq + MCP?

This roadmap is deliberately placed after the MCP access layer because the best way to discover what LLM augmentation is actually valuable — and where the hard guardrails must stay — is to have real principals using the Telegram Cromwell bot to drive the existing deterministic system every day. The traces and pain points from that usage will drive the prioritization inside this document.

The majestic monoliths, the parquet standard, the async + webhook model, and the "core runs without the AI" invariant are non-negotiable throughout.

(End of Winston + LLM roadmap)
