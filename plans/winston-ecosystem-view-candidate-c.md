# Winston Ecosystem View — Candidate C (2.5D OP rack)

> **Tournament record — not SoT.** Applied synthesis: `ecosystem/plans/winston-ecosystem-view.md`.

| Field | Value |
|-------|--------|
| **Status** | Tournament design — Candidate C |
| **Date** | 2026-09-07 |
| **Author** | Architecture (Grok; Candidate C) |
| **Type** | Cross-monolith design |
| **Mode** | compete (tournament) — implementation later under contractor |
| **Inventories (locked)** | `/tmp/wev-inventory-runtime.md`, `wev-inventory-queues-cron.md`, `wev-inventory-books-scores.md`, `wev-inventory-ui-obs.md` |
| **Contract** | `ecosystem/interfaces/winston-ecosystem-view-v1.md` |
| **Poster** | `ecosystem/docs/poster/winston-topology.dsl.md` |
| **Related** | ADR-001, ADR-005, ADR-006, ADR-007, ADR-009, ADR-012; `CONTEXT.md`; `plans/cromwell-staff-roster.md` |

This is **not a game**. No weather, banners, cities, terrain, particles, day/night, or fictional dressing. Spatial encoding exists in **one** place: the Operational Portfolio (OP) rack.

---

## 1. Thesis

The operator’s scarce resource is attention (Principle 12). The scarce *economic* object is the **Operational Portfolio** — paper and real — not a Book join row, not a WUT lab Portfolio Backtest Run (PBR), not a compose container.

**Candidate C:** a **2.5D CSS/SVG isometric OP rack** is the primary economic view (**VIEW-08 / VIEW-09 / VIEW-10 / VIEW-11** as one visual). World state is a **list of OPs + projected scores**. Projection = **render + pick**. A 2D table and the 2.5D rack **must show identical numbers**.

All other planes stay **structured**:

| Plane | Form | Spatial? |
|-------|------|----------|
| Runtime topology (VIEW-01) | Isometric **poster**, diagram-as-code | Layout only (compose graph) |
| Queues / cron (VIEW-02) | Tables | No |
| Pulse / health (VIEW-03) | Tables + one boolean | **Yield to A** |
| Traces (VIEW-04) | Placeholder | **UNKNOWN until OpenTelemetry (OTel) exists** |
| Code health (VIEW-05) | None in C | **Yield to A** |
| Data coverage (VIEW-06) | Tables | No |
| Lab objects (VIEW-07) | Optional typed rail | Separate object type, labeled `lab` |
| OP rack (VIEW-08…11) | 2.5D slabs | **Yes — only here** |

DragonRuby is **rejected** (YAGNI): zero matches in-repo, Winston operator UI is ERB + `ops_shell.css`, ADR-005 is a fluid 900px fold not a 1280×720 canvas. Introducing a game runtime to draw boxes of money is a new ops surface, a new deploy, and a glossary hazard. CSS/SVG isometric is the same stack as the ops-shell.

---

## 2. Locked glossary (do not “fix” the brief)

From `CONTEXT.md` + `/tmp/wev-inventory-books-scores.md`. Wrong nouns fail the design.

| Term | Meaning | Not |
|------|---------|-----|
| **Book** | Portfolio ↔ Market join (allocation slot) | A paper/real strategy slot; a slab |
| **Operational Portfolio (OP)** | Wv2 `portfolios` row used for Daily Analysis (DA) and desk tasking. **The slab.** | WUT lab `portfolios`; a Book |
| **Execution Mode** | `paper` \| `real` on the OP | `live`; derived from Active or `export_kind` |
| **Active** | Attention: included in DA + task surface | Live money; “the one OP” |
| **export_kind** | `observation` \| `trade_ready` (WUT provenance) | A depth plane |
| **WUT PBR** | Lab backtest score vector | An OP. If shown: `object_type=lab_pbr`, label `lab` |
| **WQ Shadow** | One **paper OP** on Quiver Tracking | A skim book; mix with TF slabs only as an OP (it is one) |
| **BookScore** | **Does not exist.** Do not invent | ret/vol/sharpe/max_dd/expectancy/current_dd/signal_idle/paper_live_hash_ok/expression_rev as a new engine |
| **current drawdown** | Derived from Wv2 `Operations::PortfolioEquitySeries` peak→last. **Not stored.** | PBR `max_drawdown`; a BookScore field |
| **Pulse** | Watchdog HTTP probes (DM `EcosystemHealthCheckJob`). No `last.json` today | Per-OP health score; OTel |
| **OTel / CodeCity / DragonRuby** | **Absent** | Do not fake |

Three independent axes (ADR-006) stay independent on the rack:

1. `export_kind` → text mark `obs` \| `tr` (not a depth).
2. **Active** + **Execution Mode** → **depth plane** (attention band).
3. Capital / utilization / current drawdown → **size / height / tint**.

---

## 3. Goals and non-goals

### Goals

- One glance: **every paper OP and every real OP** the operator actually has, stacked by promotion/attention, sized by capital, tinted by **current** drawdown.
- Toggle **table ↔ 2.5D** with a shared world-state JSON; labels are the same floats.
- Inventory scripts **before** any HTML.
- Board lives as a small ops-shell page (Wv2), linked from the existing header. Contracts + poster + projection scripts live in `ecosystem/`.
- Honest **UNKNOWN** (no series → no fake 0% drawdown; no OTel → no traces).

### Non-goals

- A city, a sim, a skybox, a “Winston World.”
- BookScore, `paper_live_hash_ok`, `expression_rev`, modular expression DAG on a Book.
- Promoting paper→real in place (Capital Activation is a new series; CA **service not shipped** — ticket still Proposed).
- Hosting the rack on WUT (lab down ≠ ops view) or DM `/status` (controller **missing**).
- Sidekiq Web, CodeScene, FossFLOW, Structurizr, DragonRuby, an OTel collector.
- Spatializing HTTP probes, queues, or git hotspots (that *is* a game).

---

## 4. View catalog (scorecard map)

| ID | Name | Candidate C form | Owner of truth |
|----|------|------------------|----------------|
| VIEW-01 | Runtime topology | Poster DSL → mermaid/SVG | Root `compose.yml` (canonical). Stale `ecosystem/deployment/compose.yml` is **not** topology |
| VIEW-02 | Queues / cron | Table: Redis DB, job class, schedule, watermark, last-ok **UNKNOWN** until Redis is read | Sidekiq-cron YAML + `ecosystem/ai/schedule/` (drift is a displayed fact) |
| VIEW-03 | Pulse | Boolean consumed from watchdog. **No pulse city.** | **Yield to A** (staff-roster `last.json` / DM `/status` when built) |
| VIEW-04 | Traces | Panel: `UNKNOWN — no OpenTelemetry in Winston` | Do not invent |
| VIEW-05 | Code health | Not in C | **Yield to A.** C refuses CodeCity |
| VIEW-06 | Parquet / DataCoverage | Table of latest vs Completed NY session | DM |
| VIEW-07 | Lab | Optional rail, `object_type=lab_pbr`, wireframe, default **hidden** | WUT `portfolio_backtest_runs` |
| VIEW-08 | OP identity rack | 2.5D slabs, one per Wv2 OP | Wv2 `portfolios` |
| VIEW-09 | Promotion / attention depth | Near = Active real; mid = Active paper; far = inactive/closed | `AttentionBands` + `closed_at` |
| VIEW-10 | Capital / utilization | Footprint ∝ Risk Capital; height ∝ utilization | `RiskEquity` snapshot |
| VIEW-11 | Drawdown + integrity | Tint = current DD; badge = boolean only | Equity series + pulse/integrity booleans |

VIEW-08…11 are **one projection** of one world list. They are not four pages.

---

## 5. World state

World state is a JSON array. Each element is an **object** with a discriminator. The renderer never infers type from name.

```json
{
  "schema": "winston-ecosystem-view-world/v1",
  "as_of": "2026-09-07",
  "pulse_ok": null,
  "objects": [ { "object_type": "operational_portfolio", "id": 11 } ]
}
```

`pulse_ok: null` means UNKNOWN (watchdog snapshot not persisted — true as of 2026-09-07).

### 5.1 Operational Portfolio object (the slab)

Projected scores are **existing** fields or one-line derivations. No new score engine.

| Field | Source | First paint? |
|-------|--------|--------------|
| `object_type` | constant `operational_portfolio` | yes |
| `id`, `name`, `short_fingerprint` | `portfolios` | yes |
| `execution_mode` | `paper` \| `real` | yes |
| `active`, `closed_at` | columns | yes |
| `export_kind` | `observation` \| `trade_ready` | yes |
| `attention_band` | `Operations::AttentionBands.band_for` → `real` \| `paper` \| `inactive` | yes |
| `depth_plane` | see §6.1 | yes |
| `recipe` | TF / `quiver_tracking` / congress copy | yes |
| `fulfillment_label` | Adapter nickname if bound; omit for dummy_sim/manual | yes |
| `free_cash` | `RiskEquity` / `capital_base` | yes (ledger) |
| `risk_equity`, `long_mv`, `short_mv` | `RiskEquity.snapshot` | progressive (parquet marks) |
| `utilization` | `(long_mv + short_mv) / risk_equity` if `risk_equity > 0` else `null` | progressive |
| `over_deployed` | existing boolean (`free_cash / risk_equity < 0.25`) | progressive |
| `return_pct`, `max_drawdown_pct`, `end_equity`, `initial_capital` | `PortfolioEquitySeries` metrics **or** last Daily Activity Report (DAR) chapter cache | progressive |
| `current_dd_pct` | **derived** §7.3 | progressive; `null` if no series |
| `cagr_pct`, `calmar` | `Operations::CagrCalmar.from_window` (same as series) | progressive |
| `pcs_score` | Wv2 PCS copy if present (Books key); **not** a performance rank | optional |
| `integrity_ok` | boolean §7.4 | progressive |
| `cash_exposure_disagree` | `RiskEquity` | progressive |
| `last_dar_status` | `scored` \| `not_scored` \| `null` (inactive) | if DAR exists |
| `eval_path` | `/operations/portfolios/:id` | yes |

**Not on the object:** Book rows, expectancy, vol column, `signal_idle_bars`, `paper_live_hash_ok`, `expression_rev`, PBR `practical_sharpe_ratio` (lab), Mid-month Scoreboard (MMS) 0–100 operating score (different product).

### 5.2 Lab object (not a slab)

```json
{ "object_type": "lab_pbr", "id": 57, "label": "lab", "portfolio_name": "Mango", "total_return": 1.2, "max_drawdown": 22.0 }
```

Default: **not in the world list**. Operator toggle `include_lab=1` appends a far rail. Geometry is a **wireframe** (stroke, no fill). Mixing a lab PBR into `operational_portfolio` is a contract violation.

WUT `paper_runs` are also not OPs.

### 5.3 Inventory scripts first (delivery order)

No board until these emit JSON that matches the contract.

| Order | Script (to add under `ecosystem/scripts/`) | Reads |
|-------|--------------------------------------------|-------|
| 1 | Keep the four `/tmp/wev-inventory-*.md` as frozen evidence | compose, jobs, models, UI |
| 2 | `wev-world-ops` — `winston_v2` rails runner | OP list + cheap columns |
| 3 | `wev-world-ops-scores` — progressive scores | `RiskEquity` + series or last DAR chapters |
| 4 | `wev-world-lab` — optional | WUT PBRs as `lab_pbr` |
| 5 | `wev-project` — **pure** world JSON → screen JSON | no DB, no browser |
| 6 | `wev-assert-iso-table` — every numeric label on a slab equals the table cell | fixture + live dump |

`wev-project` is the test oracle. The browser must implement the **same** formulas (interface §4). A golden fixture in `ecosystem/interfaces/fixtures/ecosystem-view/` locks the worked example in §6.4.

---

## 6. 2.5D projection math (world list → screen)

Canonical, testable, independent of CSS. Implementation draws SVG polygons from these numbers. **Do not** use CSS `rotateX/rotateZ` as the source of coordinates — it fights pick-hit and the table identity test. CSS 3D may visually mimic; **math in the interface is SoT**.

### 6.1 World frame

Right-handed: **+x** right along a shelf, **+z** away from the operator (depth), **+y** up.

```
depth_plane(op):
  if closed or not active:  2   # far  — archive / closed
  else if execution_mode == "real": 0   # near — Active real (capital)
  else: 1   # mid — Active paper (learning / observation-in-the-attention-sense)
```

`export_kind=observation` does **not** move an Active real OP to mid. That would collapse ADR-006 axes. Observation is a mark on the slab.

Shelf z-origins (world units):

```
Z0 = 0.0    # near
Z1 = 4.0    # mid
Z2 = 8.0    # far
Z_LAB = 12.0  # only if include_lab
```

Within a plane, order = `AttentionBands.sort_key` (real→paper→inactive, then `id`). Pack:

```
GAP = 1.6
wx_i = i * GAP     # i = 0..n-1 in that plane
wz   = Z[depth_plane]
wy   = 0           # slab sits on the shelf; height grows +y
```

Closed OPs sort after open inactive, still plane 2. Opacity 0.55.

### 6.2 Size (VIEW-10)

**Footprint** encodes **Risk Capital** (`risk_equity` at `as_of`). Log scale so a $5k paper OP and a $200k real OP coexist.

```
eq = max(risk_equity, 0)
if eq == 0 or risk_equity is null:
  sx = sz = 0.55          # unfunded / UNKNOWN capital — min tile, not a lie
else:
  # $1k → 0.55, $10k → 0.80, $100k → 1.05, $1M → 1.30
  sx = sz = clamp(0.55 + 0.25 * log10(eq / 1000.0), 0.55, 1.60)
```

**Height** encodes **utilization**:

```
gross = long_mv + short_mv
util  = gross / risk_equity     if risk_equity > 0 else null
cap   = max_leverage or 2.0     # Leverage Guardrail default (CONTEXT)
sy    = 0.12                    if util is null
      = clamp(0.12 + 0.88 * min(util / cap, 1.0), 0.12, 1.00)
```

Over-deployed does **not** change size (size would then encode two things). It is a table column + a 1px slab outline using `--ops-user`.

WQ Shadow is sized like any other OP (it has Risk Capital). Recipe mark `WQ` on the top face.

### 6.3 Isometric 2:1 (dimetric)

```
TILE_W = 72          # px, x/z footprint of 1 world unit
TILE_H = 36          # px, half of TILE_W (classic 2:1)
ELEV   = 36          # px per 1 world-y
OX, OY = origin      # rack origin, default (520, 72) on a 1100×640 viewBox
```

World → screen:

```
sx(x, y, z) = OX + (x - z) * (TILE_W / 2)
sy(x, y, z) = OY + (x + z) * (TILE_H / 2) - y * ELEV
```

A slab is the axis-aligned box `[wx, wx+sx] × [0, sy] × [wz, wz+sz]`. Three visible faces (viewer looks from −z, −x, +y):

| Face | World corners (x,y,z) order |
|------|-----------------------------|
| **Top** | `(wx, sy, wz)`, `(wx+sx, sy, wz)`, `(wx+sx, sy, wz+sz)`, `(wx, sy, wz+sz)` |
| **Left** (west) | `(wx, 0, wz)`, `(wx, sy, wz)`, `(wx, sy, wz+sz)`, `(wx, 0, wz+sz)` |
| **Right** (south) | `(wx, 0, wz+sz)`, `(wx+sx, 0, wz+sz)`, `(wx+sx, sy, wz+sz)`, `(wx, sy, wz+sz)` |

Project each corner with `sx,sy`. Emit SVG `<polygon points="…">`.

**Painter’s order:** sort objects by `(wx + wz) descending`, then `id`. Draw far first.

**Pick:** point-in-polygon on the three faces, front-to-back (reverse painter). Hit `object_type + id` selects the table row with the same key. Inverse of the ground plane (y=0) is:

```
x' = sx - OX;  y' = sy - OY
x  = x' / TILE_W + y' / TILE_H
z  = y' / TILE_H - x' / TILE_W
```

Use inverse only for empty-shelf clicks; object pick is polygon.

### 6.4 Worked example (golden)

`OX=520, OY=72`, Mint: `wx=0, wz=0, sx=sz=0.95, sy=0.64` (`risk_equity≈48200`, `util≈0.64`).

```
sx(x,y,z) = 520 + (x-z)*36
sy(x,y,z) =  72 + (x+z)*18 - y*36
```

| Corner | World | Screen |
|--------|-------|--------|
| top-N | (0.00, 0.64, 0.00) | (520.0, 49.0) |
| top-E | (0.95, 0.64, 0.00) | (554.2, 66.1) |
| top-S | (0.95, 0.64, 0.95) | (520.0, 83.2) |
| top-W | (0.00, 0.64, 0.95) | (485.8, 66.1) |

`current_dd_pct=4.2` → tint `--dd-watch` (see §7.3). Label on top face (same strings as table):

```
Mint · a1b2c3d4
real  $48,200  DD 4.2%
```

A second Active real at `i=1` has `wx=1.6`. First Active paper sits at `wz=4.0`, visually a full shelf back (`4 * 36 = 144px` of isometric depth).

### 6.5 Screen layout constants

| Token | Value |
|-------|-------|
| SVG `viewBox` | `0 0 1100 640` |
| Shelf labels | world `x = -2.1`, `z = Zk + 0.2`, text: `ACTIVE REAL` / `ACTIVE PAPER` / `INACTIVE / CLOSED` |
| Ground diamonds | unfilled, `--ops-panel-border`, one per plane, width = `max(n, 3) * GAP` |
| Min desktop | 1100px — below **900px** (ops-shell fold) **table is primary**, rack hidden or `overflow:auto` thumbnail. Identity of numbers still holds |
| Motion | none. No interpolate-on-refresh beyond replacing polygons |

---

## 7. Tint, badge, labels (VIEW-11)

### 7.1 What the operator should see in <2s

1. How many **Active real** slabs are near, and whether any are **red** (current DD).
2. How many **Active paper** sit behind them (learning band), including WQ Shadow if Active.
3. Whether archive (far) is a junk pile (too many inactive) — hygiene, not daily capital work.
4. Whether the **pulse** disk in the header is filled (ecosystem probes) — not a per-slab color.

### 7.2 Tint scale (current drawdown)

`current_dd_pct` is **not** `max_drawdown_pct`.

```
peak    = max(equity over series points)
current = last equity
current_dd_pct = (peak - current) / peak * 100   if peak > 0
               = null                            if series empty or peak <= 0
```

Series = `Operations::PortfolioEquitySeries` (`equity = free_cash + long MV − short MV`). Prefer last DAR `portfolio_chapters[].equity_series` when `as_of` equals the production report date (cheap). Otherwise compute async. **Never** substitute `max_drawdown_pct` for current DD (a recovered OP would stay red).

| `current_dd_pct` | Token | Hex (ops-shell family) | Meaning |
|------------------|-------|------------------------|---------|
| `null` | `--ops-muted` | `#8b9bb0` | UNKNOWN — no series. **Not green** |
| `= 0` | `--ops-ok` | `#3d9a6a` | At peak |
| `(0, 5]` | `--dd-ok` | `#3d9a6a` | Noise |
| `(5, 10]` | `--dd-watch` | `#c9a84c` | Watch (`--ops-user`) |
| `(10, 20]` | `--dd-alert` | `#c47a3d` | Attention |
| `> 20` | `--ops-err` | `#c45c5c` | Capital attention |
| `≥ 50` | `--ops-err` + 40% hatch | `#c45c5c` | Viability-class **current** DD (lab gate is PBR max DD ≤ 50; this is ops *now*) |

Top face = tint at 100%. Left/right faces = same hue, 70% / 55% luminance (read as a box, not a billboard).

### 7.3 Badge = boolean only

No 0–100 integrity score. No traffic-light enum pretending to be a boolean.

| Location | Boolean | True | False | UNKNOWN |
|----------|---------|------|-------|---------|
| Header disk | `pulse_ok` | filled `--ops-ok` | filled `--ops-err` | hollow `--ops-muted` |
| Slab corner | `integrity_ok` | small filled square | small empty square | no square |

```
integrity_ok =
  pulse_ok is not false
  AND cash_exposure_disagree is not true
  AND (if active and last_dar_status present: last_dar_status != "not_scored")
```

If `pulse_ok is false`, numbers are still shown (ledger does not need HTTP) but badges go empty — operator should not trust *freshness*. If pulse is UNKNOWN (today: no `last.json`), header is hollow; slab integrity uses only `cash_exposure_disagree` + DAR scored.

**Not** in the badge: PCS, utilization, over-deployed, export_kind, IBKR tickle, queue depth.

### 7.4 Labels (must match table)

Visible on the top face at ≥1.0 scale; truncated with title tooltip:

```
{name} · {short_fingerprint}
{execution_mode}  ${risk_equity as 82,200}  DD {current_dd_pct or "—"}%
```

Table columns (same numbers, same `as_of`):

`id | name | fp | mode | band | export | risk_eq | util | ret% | curDD% | maxDD% | over_dep | integ | path`

Toggle does not recompute. It re-renders.

---

## 8. Wireframe (ASCII)

Desktop ops-shell page `GET /wv2/operations/ecosystem` — same chrome as DARs (`ops-shell ops-dars-page`).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ← Ops shell     ECOSYSTEM VIEW                         [2.5D] [table]     │
│  as_of 2026-09-07   pulse ○ UNKNOWN   lab off                               │
│  Active real 2    Active paper 3    inactive 8    closed 2                  │
├──────────────────────────────────────────────┬──────────────────────────────┤
│                                              │ SELECTED  #11 Mint · a1b2c3  │
│           far  INACTIVE / CLOSED             │ mode     real                │
│         ╱─────────────────────────────╱      │ band     Active              │
│        ╱  ▢ Walnut·closed   ▢ obs    ╱       │ export   trade_ready         │
│       ╱─────────────────────────────╱        │ risk_eq  48200               │
│                                              │ util     0.64                │
│        mid  ACTIVE PAPER                     │ ret%     12.10               │
│      ╱───────────────────────────────╱       │ curDD%   4.20                │
│     ╱  ▣ Mango $22k  ▣ WQ Shadow     ╱        │ maxDD%   11.00               │
│    ╱───────────────────────────────╱         │ integ    true                │
│                                              │                              │
│   near  ACTIVE REAL  ← operator              │ [open portfolio] [journals]  │
│  ╱──────────────────────────────────╱        │                              │
│ ╱  ▣ Mint $48k DD 4.2%   ▣ Rust     ╱         │                              │
│╱──────────────────────────────────╱          │                              │
│                                              │                              │
│  tint: green=at peak  gold=5–10  red=>20     │                              │
│  size: footprint=Risk Capital  height=util   │                              │
└──────────────────────────────────────────────┴──────────────────────────────┘

Table mode (same JSON — numbers must not move):

 id  name   fp       mode  band      risk_eq   util  ret%  curDD  maxDD  integ
 11  Mint   a1b2c3d4 real  real      48200     0.64  12.1  4.2    11.0   true
 14  Rust   …        real  real      …         …     …     …      …      …
  7  Mango  …        paper paper     22100     …     …     …      …      …
  9  WQ Sh. qtrack   paper paper     …         …     …     —      …      …
  3  Walnut …        paper inactive  …         …     …     …      …      closed
```

Mobile (<900px): table only; toggle still exists but 2.5D is a horizontally scrollable SVG, not the first paint.

Click slab = click row = `eval_path`. No modal city; the existing portfolio page is the drill-in.

---

## 9. Other planes (structured)

### 9.1 Poster (VIEW-01) — not the rack

`ecosystem/docs/poster/winston-topology.dsl.md` is diagram-as-code for **compose + host extras**. Isometric *layout* of services (near = host-published ports, far = AI profile / host IBKR Client Portal Gateway (CPGW)). It is a poster, not an OP. Rendering: mermaid now; optional SVG later. **No** FossFLOW/Structurizr (absent).

### 9.2 Queues / cron (VIEW-02)

A table on the same page **below the fold** (or a `#queues` fragment). Columns from the queues inventory. Cells that were not probed stay `UNKNOWN` (live Redis depths, Sidekiq last-ok). Catalog drift is a row, not a toast.

### 9.3 Pulse (VIEW-03) — yield to A

C consumes `pulse_ok`. C does **not** design `last.json`, DM `StatusController`, probe expansion (BG/Schwab/Quiver), or Telegram copy. Those are staff-roster + Candidate A’s home turf. Until A’s snapshot exists, header disk is hollow.

### 9.4 Traces (VIEW-04)

Static copy: “Traces: UNKNOWN — no OpenTelemetry collector or SDK in Winston monoliths.” Do not draw spans from Sidekiq logs.

### 9.5 Code health (VIEW-05) — yield to A

C will not spatialize git churn, hotspots, or “buildings per class.” CodeCity is forbidden by locked facts. If A proposes Rubycritic/CodeScene tables, C defers.

---

## 10. Where it lives

| Piece | Path | Why |
|-------|------|-----|
| Contract | `ecosystem/interfaces/winston-ecosystem-view-v1.md` | Cross-monolith SoT |
| Poster | `ecosystem/docs/poster/winston-topology.dsl.md` | Diagram-as-code |
| Scripts | `ecosystem/scripts/wev-*` | Inventory-first; projection oracle |
| Board HTML | Wv2 `Operations::EcosystemController` + ERB | Only HTML operator chrome that exists (inventory §1) |
| CSS | `ops_shell.css` tokens + `.op-rack` | No new design system |
| JSON | `GET /operations/ecosystem.json` | World list; ADR-005 first paint = shell + counts |
| Link injection | ops-shell home header `ops-btn ghost` **and** `renderPanels()` JS (ERB-only links die on Refresh) | Inventory checklist |
| Not | WUT sidebar, DM `/status`, BG JSON root, a new compose service | Wrong hosts |

Wv2 UI stack: **ERB + Sprockets + page-local JS** (Turbo unused). Follow that. Do not introduce importmaps for the rack.

First paint (ADR-005): counts by band + empty shelves + table headers. Progressive fetch of scores. Do **not** run `PortfolioEquitySeries` for every closed OP on the request.

---

## 11. Why C beats a table-only v1

A table is the **number SoT**. It is not the **attention SoT**.

ADR-006 already ordered the desk: Active real → Active paper → inactive hygiene. DAR and ops-shell panels still present that as **lists**. Lists do not make capital *mass* or *current* pain visible:

- Two Active real OPs, one $8k and one $180k, look like two rows. On the rack the $180k slab is the thing you can hit with your eye.
- A paper band of five observation recipes behind them is the learning shelf — you see the pile, not a scroll.
- Current DD as tint answers “who is hurting *now*” without opening equity compare. `max_drawdown_pct` in a column is history; red *now* is the interrupt.
- Far-plane clutter is the inactive-hygiene problem the soft norms (~1–3 real, ~1–7 paper) were written for — a wall of far tiles is the warning, without a hard cap.

Table-only v1 also invites the wrong compression: one “focus” OP (already rejected: `OpsShellPanels.focus` is nil). The rack cannot point at a single hero tile without lying about multi-Active.

C keeps the table. The rack is a **projection** of it. The identity test (`wev-assert-iso-table`) is what stops 2.5D from becoming a game.

DragonRuby-table hybrids lose: they add a runtime without adding a number.

---

## 12. Where C must yield to A (pulse / code-health)

A is an inventory-first **thin projector** with a first-class **Pulse plane** (`ComponentStatus.health`, `QueueSnapshot`, `CronSnapshot`, `DataWatermark`) that must never merge into PnL. That is the correct home for “is work moving?” C’s rack is the correct home for “where is capital?” Mixing them is the false dashboard both candidates forbid.

| Topic | Why A wins | What C does |
|-------|------------|-------------|
| Pulse plane | A already specifies health cards + Redis `LLEN`/`ZCARD` on `/0..3` + Sidekiq-cron + Cromwell `jobs.json` + DataCoverage watermarks + `not_probed` for BG | Consume `pulse_ok` (and optionally a link to A’s console). **No** pulse city, no queue-as-slab-height |
| `last.json` / DM `GET /status` | Staff-roster + A: WEV prefers the watchdog snapshot when written; `/status` is Pulse-only and **not built** | Do not hijack `/status` for the OP rack; header disk stays hollow until a snapshot exists |
| Probe gaps (BG, Schwab, Quiver) | A’s `extension_probes` / `not_probed` is the honest encoding | Badge stays boolean; no per-vendor buildings |
| Catalog drift (manifest vs YAML) | A treats drift as a Pulse finding | VIEW-02 may show a row; C does not invent a clock UI |
| Code health / CodeCity / hotspots | A **rejects** CodeCity as v1 fiction (absent tooling). Any future static `code_health.json` belongs on A’s projector, not on C’s isometric capital language | Zero code-health UI. Spatializing LOC is a game |
| OTel traces | A: not in inventory, adding is fiction. C agrees | VIEW-04 string: `UNKNOWN — no OpenTelemetry` |
| Pulse ⇏ PnL | A’s plane discipline: Pulse `degraded` while an Active real OP is green on return is **correct** | Tint is **current DD only**. A red slab is not “Wv2 is down” |

If A ships the pulse table, the rack header disk is a **subscriber**, not a competitor. C still beats A on the **economic** glance (VIEW-08…11): A’s book plane is table-first with 2.5D as later density polish; C’s rack *is* v1, with the table as the identity proof.

---

## 13. Implementation slices (after tournament)

1. **Scripts + fixture** — world dump (cheap fields) + `wev-project` + golden screen JSON from §6.4.
2. **Contract freeze** — this plan’s interface file; no BookScore fields.
3. **Wv2 JSON endpoint** — metadata first; scores from last DAR chapters when `as_of` matches.
4. **Page + table** — ships value even if SVG is late (table-only is a *fallback*, not the thesis).
5. **SVG rack** — polygons from `wev-project` math; pick ↔ row.
6. **Header link** — ops-shell home + `renderPanels()` duplicate.
7. **Optional lab rail** — off by default.

Human gate: none of this books trades, mutates Engaged OPs, or calls Capital Activation (still unshipped). Read-only.

---

## 14. Risks

| Risk | Mitigation |
|------|------------|
| Equity series on many closed OPs blows first paint | ADR-005: cheap list; scores for Active only on first fetch; closed on demand |
| Operators read tint as “max DD” | Legend + table column `curDD%` vs `maxDD%`; never reuse max for tint |
| WQ Shadow looks like a TF OP | Recipe mark `WQ`; still a paper OP (correct) |
| Lab PBRs get mixed in | Discriminator + default hidden + wireframe |
| CSS 3D drift vs table numbers | Math SoT in `wev-project`; SVG from numbers |
| Pulse disk always hollow | Accept until A/`last.json`; do not scrape Telegram |

---

## 15. Decision log (Candidate C)

1. **OP is the slab. Book is a join.** Spatial only on the OP rack.
2. **CSS/SVG isometric, not DragonRuby.** YAGNI + existing ops-shell.
3. **Depth = attention band** (Active real / Active paper / inactive+closed), not `export_kind`.
4. **Size = log Risk Capital; height = utilization vs leverage cap.**
5. **Tint = current DD from ops equity series; documented bins; UNKNOWN is muted.**
6. **Badge = boolean** (pulse header, integrity slab). No BookScore.
7. **Table ↔ 2.5D identity** is a test, not a slogan.
8. **Yield pulse and code-health to A.** Do not spatialize them.
9. **Traces stay UNKNOWN** until OTel exists.
10. **Inventory scripts first.** Board is a projection of a file.
