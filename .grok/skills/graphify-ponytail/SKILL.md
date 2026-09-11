---
name: graphify-ponytail
description: >
  Traverse the Winston estate via the Graphify Graph (query/path/explain, not
  grep-first), then Ponytail to simplify and collapse duplicates toward the
  owning monolith. Use when asking how code works, what calls X, tracing a
  flow, finding copies across DM/WUT/Wv2/BG, simplifying, deleting dead code,
  harmonizing helpers, or the user says /graphify-ponytail, "graphify then
  ponytail", "harmonize". Not for capital actions or Telegram broadcasts.
metadata:
  short-description: "Graphify map, then Ponytail collapse"
---

# Graphify then Ponytail

ADR-014. **Graphify Graph** is the map. Executing files are proof. **Ponytail** is the edit. Do not skip the map; do not treat the map as the runtime.

The full Graphify CLI lives in the user `graphify` skill (`/graphify`, `query`, `path`, `explain`, `update`). This overlay is the Sawtooth rule for *when* and *which graph*, plus how Ponytail uses the result.

## 1. Pick the graph

| Scope | File |
|-------|------|
| One monolith | `{repo}/graphify-out/graph.json` |
| Cross-monolith / “where else does this live?” | workspace `graphify-out/graph.json` (merged; nodes have `repo`) |

If the file is missing: say so and run `/graphify` on that path (Rails: `graphify extract --code-only` is enough). Do not silently rebuild the whole workspace for a one-file question.

Stale after a large code change: `graphify update <path>` (AST, no LLM). Full semantic rebuild only when docs/papers must change. **`/wrap` step 2** always refreshes existing graphs for repos this session touched and re-merges the workspace graph — do not skip that on wrap; do not full-rebuild during wrap.

## 2. Traverse (before grep)

1. Expand the question against that graph’s vocabulary (Graphify query skill — tokens must exist in the graph).
2. Run one of:
   - `graphify query "…" --graph <graph.json>` — BFS neighbors
   - `graphify query "…" --dfs --graph <graph.json>` — one chain
   - `graphify path "A" "B" --graph <graph.json>` — shortest path
   - `graphify explain "X" --graph <graph.json>` — one node
   - `graphify god-nodes --graph <graph.json>` — hubs (harmonize suspects)
3. Print the expansion. Answer only from the subgraph. Never invent an edge. AMBIGUOUS stays AMBIGUOUS.
4. **Then read** every cited `source_file` (and `source_location` when present). If the file contradicts the graph, believe the file and note the graph is stale.

Grep is a follow-up for a string the graph did not index (SQL, YAML keys, comments), not the first map.

## 3. Harmonize (Ponytail after the map)

Use when Graphify shows two (or more) implementations of one job, or a god node with parallel helpers.

1. Name the **owner** from ADRs/principles (DM derivatives, BG transport, Wv2 desk, WUT lab reference). The extra copy is the candidate to delete or wrap.
2. Climb the Ponytail ladder on the *mapped* surface: skip it → reuse owner → stdlib → shortest diff. Do not add a third helper.
3. `/ponytail-review` on the diff. `/ponytail-audit` only when the user asked for whole-repo bloat.
4. Do not Ponytail away trust-boundary checks, money-path validation, or an explicit request.

Pattern: `[map] → owner is X → skipped copy in Y, add when [evidence].`

## 4. Done

- Claims cite graph `source_location` **and** the file you read.
- Cross-monolith collapse names the contract (`ecosystem/interfaces/…` or ADR), not only two directories.
- Optional: `graphify save-result` with `--outcome useful|dead_end|corrected` so the next session prefers working nodes.
