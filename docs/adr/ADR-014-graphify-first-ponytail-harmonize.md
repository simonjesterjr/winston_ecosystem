# ADR-014: Graphify-first traversal; Ponytail to harmonize

**Status:** Accepted
**Date:** 2026-09-10
**Deciders:** Operator + Architecture
**Builds on:** ADR-001 (majestic monoliths), principle 8 (reuse WUT, abandon v1), principle 9 (preserve knowledge durably)
**Glossary:** `CONTEXT.md` — Graphify Graph, Ponytail, Work Graph
**Skill:** `graphify-ponytail`

## Context

The estate is several majestic monoliths plus contractor docs. Agents default to grep and ad-hoc file reads, then write a *new* helper next to an existing one. That multiplies ATR/load/journal/Sidekiq copies across Data Manager (DM), Winston Unit Test (WUT), Winston v2 (Wv2), and Broker Gateway (BG).

Three approaches:

- **A. Grep-first** — status quo. Fast locally; blind to god nodes, surprising bridges, and same-named symbols in two repos.
- **B. Trust Graphify as proof** — query `graph.json` and edit from labels alone. The graph goes stale; vendor JS and placeholder community names add noise; executing code is not the graph.
- **C. Graphify as the map, files as proof, Ponytail as the edit** — query/path/explain first; read cited `source_file` / `source_location`; then the Ponytail ladder (YAGNI, reuse, shortest working diff) so duplicates collapse toward the owning monolith.

## Decision

Choose **C**.

1. **Traverse with Graphify** when the question is “how does this work?”, “what calls X?”, “where is the other copy?”, or any cross-file / cross-monolith orientation. Prefer the existing graph:
   - one monolith → `{repo}/graphify-out/graph.json`
   - cross-monolith → workspace `graphify-out/graph.json` (merged)
2. **Never invent an edge.** Answer only from graph output, then confirm in the cited files. The executing branch is proof; the graph is the map.
3. **Simplify and harmonize with Ponytail after the map.** If Graphify shows two implementations of one job, do not add a third. Reuse the owner (ADRs/principles: DM owns derivatives, BG owns transport, Wv2 owns the desk, WUT is the lab reference). Delete or wrap the extra copy. `/ponytail-review` on the diff; `/ponytail-audit` only when asked for whole-repo bloat.
4. **Stale graph:** `graphify update` (code) on that path. Full `/graphify` rebuild only when the graph is missing or docs/semantic coverage must change. Do not rebuild 12k nodes as a side effect of a one-file fix. **`/wrap` step 2** runs `graphify update` on each touched repo that already has a graph, then re-merges the workspace graph. It does not silently full-rebuild, does not `git add graphify-out/`, and only flags Ponytail duplicates — it does not start a harmonize rewrite unless asked.
5. **Rebuild law is not execution proof.** Rails graphs are often `--code-only`. Ecosystem docs are semantic. Both can omit a live branch — read the file.

`graphify-out/` is a local working artifact (map + HTML + report). Do not treat it as source of truth in git unless we later decide to pin it.

## Rationale

- **Not A:** grep cannot rank god nodes or surface a Wv2 `Portfolio` that is a different node from a WUT `Portfolio`. Harmonize work starts from that confusion.
- **Not B:** Graphify honesty tags (EXTRACTED / INFERRED / AMBIGUOUS) exist because the map is lossy. Capital paths still need the executing method and a test.
- **C** matches how we already treat parquet vs PG: the map (coverage, graph) points; the artifact (parquet, `.rb`) proves.

## Consequences

### Positive

- Orientation uses one merged graph plus per-monolith graphs instead of re-walking trees.
- Duplicate helpers have a named ritual: map → owner → Ponytail collapse.
- Query results can be saved (`graphify save-result`) so later sessions prefer working nodes.

### Negative

- Graphs go stale after large refactors until `graphify update`.
- Merged HTML is community-aggregated above 5,000 nodes; symbol-level work still uses `graphify query` / `path` / `explain`.
- Ecosystem graph includes vendor IBKR demo JS (noisy god nodes). Ignore those communities for Winston work.

### Risks mitigated

- Copy-paste “harmonize” that actually adds a third ATR calculator.
- Grep that finds one monolith and misses the owner in another.
- Ponytail that deletes a trust-boundary check because it looked unused in one file.
