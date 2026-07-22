# Core Principles (Extracted & Growing)

(Seeded from user query + approved DM plan. Update this file on every major decision.)

1. **Majestic Monoliths** — Focused, complete Rails apps (DM, WUT, future Wv2, Cromwell) that are independently valuable and deployable, yet designed from the start to compose cleanly via APIs, webhooks, Sidekiq (internal), and files (parquet).

2. **Async + Webhooks + Agentic Coordination** — Sidekiq for real work inside a monolith. Webhooks (and simple APIs) for cross-monolith coordination, especially status from DM to Cromwell. Cromwell is the agentic "principal coordinator" (todos, reports, daily orchestration, telling DM when to run).

3. **Data as a First-Class Service with Guarantees** — DM is responsible for acquisition (EODHD), the 3+ year + latest trading data invariant, calculation of running derivatives (ATR + supported MAs), and producing the canonical Winston EOD Standard (parquet). Consumers pull or mount; DM verifies they have what they need.

4. **Parquet is the Winston Standard** — Raw OHLCV + derived columns live in parquet files under DM's `data/markets/...`. PG is metadata only (Market registry, coverage, DownloadRun/Task, consumers, status). This gives portability, analytical power (DuckDB), easy git/repo shipping of data sets (with reconciliation), and a clean handoff between monoliths.

5. **DM Owns Derivatives** — After downloading/filling data for a market, DM (re)computes ATR (17 simple, matching WUT) and the moving averages currently supported in the ecosystem and writes them into the parquet. Keeps them fresh on incremental updates.

6. **Reconciliation for Reality** — DM has a ReconciliationService that walks the on-disk parquet tree and ensures PG knows about every symbol, its actual date range, which indicators are present, etc. Run on boot, after downloads, explicitly via rake. Makes "clone repo + data files are here" or "someone updated an old parquet in place" work without full re-downloads or treating files as brand new.

7. **Single Upstream First (EODHD)** — Build the entire DM pipeline (parquet standard, 3y logic, reconciliation, provisioning, Cromwell notifications, WUT consumption) against EODHD only. Pluggable design is preserved but secondary. User provides the API key once the ecosystem config location is ready.

8. **Reuse WUT, Abandon v1** — `winston_unit_test/` (WUT) contains the mature, comprehensive approaches to data (DataDownloader patterns, adapters, DataSync/Reconciler, DatasetLoader, IndicatorCalculator, calculate_atr, Activity atr with config, Portfolio/Market/Book via joins, Sidekiq + daily ops orchestration, etc.). Use those as the model. `winston/` (v1) is legacy — do not model after it or copy its data logic.

9. **Preserve Knowledge Durably** — Everything important (vision, principles, plans, interfaces/contracts, deployment/podman, hints/cues) goes into `sawtooth/ecosystem/`. The AI (and humans) always read it first in a session. This eliminates re-explaining and hallucinations on a long-running project.

10. **Podman-Native Deployment** — Local (and target) runtime is podman. Root `compose.yml` orchestrates the monoliths + redis. Volumes for DM's parquet data tree (mountable by consumers). Each monolith has a minimal Containerfile.

11. **Observable & Idempotent by Default** — Structured logging, explicit DownloadRun/Task tracking with steps, Cromwell gets rich status (started, per-market, derivatives done, parquet written, verified, errors, completion). All major operations (download a symbol for a window, reconcile, provision) are idempotent.

12. **Human Attention Is the Most Valuable Commodity** — Operator attention is scarcer than compute, logs, or Telegram bandwidth. Every human-facing surface (Cromwell cron, Sawtooth Main posts, MCP reply text, ops dashboards, alerts) must earn the right to interrupt. Prefer silence or a one-line all-clear over exhaustive quiet-state dumps. Lead with what needs a decision or shows regime change (volatility, movers, breaches, failures); bury or omit uninteresting detail. Never pad with menus, offer-lists, or “would you like me to…” on scheduled broadcasts. Apply this when designing skills, cron messages, report copy, and agent recovery behavior — a correct but attention-wasting message is still a product failure.

13. **Evolving** — This list will grow. When we decide something (provisioning model, exact parquet columns, auth for internal APIs, etc.), document the decision + rationale here and in the relevant principles/ or plans/ file.

See the approved data download service plan (in `plans/`) for the concrete application of these principles to the first monolith (DM).
