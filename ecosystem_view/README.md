# Winston Ecosystem View

Four-plane operator console. Spec: `ecosystem/plans/winston-ecosystem-view.md`. Contracts: `ecosystem/interfaces/winston-ecosystem-view-v1.md`.

## Inventory (before chrome)

From sawtooth root:

```
python3 ecosystem/ecosystem_view/bin/inventory --pretty
python3 ecosystem/ecosystem_view/bin/inventory queues --pretty
python3 ecosystem/ecosystem_view/bin/inventory -o ecosystem/ecosystem_view/snapshots/latest.json --pretty
```

## Poster

`ecosystem/docs/poster/index.html` — intended topology, not live metrics.

## Operator door

Winston v2 ops-shell → **Ecosystem** (`/operations/ecosystem`, Tailscale `/wv2/operations/ecosystem`).

Static copy: `ecosystem/ecosystem_view/app/index.html` (loads snapshot JSON if present).

Slabs are **Operational Portfolios**. CONTEXT **Book** is the market join. Mode is `paper|real`. Pulse is not PnL.
