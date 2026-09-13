# Session Report — WUT Tailscale home loop, ADR-016, Blue C03 589–591

**Date:** 2026-09-13
**Time:** ~15:50–12:44 MDT (spanned 12 Sep evening into 13 Sep; wrap at 12:44)
**Duration:** ~cross-evening; wrap slice ~Tailscale fix + C03 eval
**Project:** Sawtooth / Winston ecosystem (WUT + Wv2 + contractor docs)
**Working directory:** /home/johnkoisch/Documents/com/sawtooth
**Branch:** `main` on `winston_unit_test`, `winston_v2`, `ecosystem` (each independent git)
**Model:** Grok 4.6
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Restore Winston Unit Test (WUT) MagicDNS home and Portfolio Backtest Run (PBR) assets; then evaluate PBR 589 / 590 / 591.

**Outcome:** Delivered (outage + ADR + C03 eval). Leftover dirty trees (Edge scoreboard, confirm-sync, Wv2 ops) **not** committed in this wrap.

**One-line summary:** `/wut/` was an infinite 302 because Rails redirected Serve-stripped `/` to `/wut/`; that redirect is gone, locked by spec + ADR-016. Blue C03 with hybrid fill is now a valid pair: EMA-20 confirm (PBR 590) beats no-confirm (PBR 591), but is GOOGL-concentrated and not trade-ready.

---

## 2. Work Completed

- Diagnosed MagicDNS `https://sawtooth-ai.tail944ffb.ts.net/wut/` as `302 Location: /wut/` loop; nested `/wut/portfolio_backtest_runs` stayed 200.
- Removed `TailscaleScriptName` root redirect in WUT and Winston v2 (Wv2). Serve-stripped `/` is home.
- Regression specs: `spec/lib/tailscale_script_name_spec.rb` in both monoliths (green).
- Restarted `winston_unit_test` and `winston_v2`. Live curl: `/wut/`, `/wut`, `/wv2/` all **200**. PBR index 19 CSS/JS assets 200; Finder `turbo/* 2.js` gone from importmap.
- Dated the landmine: 2026-07-06 WUT `1a91ef5` (localhost UX 302), copied to Wv2 2026-07-22 `740bbae`. Nested URLs hid it for two months.
- ADR-016 + hint `tailscale-serve-no-root-redirect.md`; struck “or is redirected” in the 2026-07-04 analysis.
- Evaluated PBR 589 / 590 / 591 as the first clean Blue C03 set after confirm-sync (see §15).

---

## 3. Code Delivered

### Files changed (this wrap’s accounted edits)

| File | Change | Notes |
|------|--------|-------|
| `winston_unit_test/lib/tailscale_script_name.rb` | modified | No `/` → `/wut/` 302; normalize empty PATH; exact-prefix strip |
| `winston_unit_test/config/initializers/relative_url_root.rb` | modified | Comment: do not redirect stripped home |
| `winston_unit_test/spec/lib/tailscale_script_name_spec.rb` | added | Serve-stripped `/` is 200 |
| `winston_unit_test/docs/issues/2026-09-12-wut-tailscale-home-redirect-loop.md` | added | resolved; dated to 2026-07-06 |
| `winston_v2/lib/tailscale_script_name.rb` | modified | Same as WUT for `/wv2/` |
| `winston_v2/config/initializers/relative_url_root.rb` | modified | Comment |
| `winston_v2/spec/lib/tailscale_script_name_spec.rb` | added | Same lock |
| `ecosystem/docs/adr/ADR-016-tailscale-serve-rails-subpath.md` | added | Accepted |
| `ecosystem/hints/tailscale-serve-no-root-redirect.md` | added | Session-start gotcha |
| `ecosystem/hints/README.md` | modified | Index the hint |
| `ecosystem/docs/analysis/2026-07-04-tailscale-serve-rails-subpath.md` | modified | Bare root must 200 |
| `ecosystem/docs/session-reports/2026-09-13-1244-wut-tailscale-home-and-blue-c03.md` | added | This report |

Scratch only (do not commit): `winston_unit_test/tmp/eval_pbr_589_591*.rb`.

### Not this wrap (dirty, leave for a later commit)

WUT still has Edge calculators, confirm-sync factory, Finder ` 2.js` deletions, PBR views. Wv2 has Edge + ops/WQ slate work. Ecosystem has ADR-015, measuring-edge docs, other tickets. See `git status` on each `main`.

### Commits

- _(pending wrap Step 4 — only the table above)_

### Branch / PR state at sign-off

- Branch: `main` on all three — dirty beyond this wrap’s files
- Pushed: pending wrap Step 5
- PR: not opened

---

## 4. Decisions Made

### Decision 1: Never 302 Serve-stripped `/` to the prefix
- **Choice:** SCRIPT_NAME + prefix strip only (2026-07-04 model). Delete the 2026-07-06 root redirect.
- **Why:** Tailscale Serve `--set-path=/wut` strips; redirecting `/` to `/wut/` cannot converge.
- **Alternatives considered:** Host / X-Forwarded sniffing (rejected 2026-07-06 and again now); keep localhost-only redirect (Host is `127.0.0.1` through Serve, so it still loops).
- **Reversibility:** easy
- **Promote to ADR?** Yes — ADR-016 Accepted

### Decision 2: ADR + hint, not a Business Rule
- **Choice:** Access topology lives in ADR-016 and `ecosystem/hints/`. Not `business-context/`.
- **Why:** Not fills, risk, or journals.
- **Reversibility:** easy

### Decision 3: PBR 590 is interesting, not trade-ready
- **Choice:** EMA-20 confirm helps Blue under hybrid fill (590 vs 591). Do not promote. Next cell: freeze 590 knobs, drop One-Way Dynamic (OWD) or cap pyramids at 2.
- **Why:** GOOGL ~80% of 590’s Edge; n≈100 thin; E50 1.11 not ~1.2; 41% drawdown; OWD still on.
- **Reversibility:** lab-only
- **Promote to ADR?** No

---

## 5. Insights Surfaced

- Nested MagicDNS URLs can stay 200 while home loops. Logo `root_path` is `/wut/` — that is the detonator.
- 2026-07-06 session verified the 302 only in a Ruby mock and left “test Tailscale browser flow” unchecked.
- Confirm-sync fix worked: 589/590 market confirm `[8]`; 591 empty. 583/584 were not a C03 pair.
- Max-markets 4 vs nil is a different recipe (583 +196% uncapped vs 589 +77% capped), not noise.
- L3+ pyramids are negative on 589–591. 589→590 (max lots/symbol 5→4) is most of the return jump.
- PBR 80 (+2,356% / 27% DD, 1,382 trades, unstamped fill) is not a sibling of these hybrid runs.

---

## 6. Issues & Tickets

### Resolved this session
- WUT `/wut/` Tailscale home redirect loop — `winston_unit_test/docs/issues/2026-09-12-wut-tailscale-home-redirect-loop.md` (status resolved). Same defect in Wv2 `/wv2/`.

### Deferred
- Leftover dirty trees (Edge scoreboard, PBR confirm-sync, Finder ` 2.js`, Wv2 ops) — not in this wrap’s commit set.
- Next Blue cell: freeze PBR 590 knobs; static 2% or max pyramid 2 (not another confirm tweak).
- Hard-refresh instruction for PBR index if a cached importmap still looks unstyled.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| WUT TailscaleScriptName | `bundle exec rspec spec/lib/tailscale_script_name_spec.rb` | ✅ 6 examples |
| Wv2 TailscaleScriptName | same path in Wv2 | ✅ 4 examples |
| MagicDNS `/wut/` `/wut` | curl after compose restart | ✅ HTTP/2 200, dashboard HTML |
| MagicDNS `/wv2/` | curl | ✅ HTTP/2 200 |
| PBR index + 19 assets | curl | ✅ 200, no ` 2.js` in importmap |
| Browser click-through | no browser MCP | ⚠️ curl/HTML only |
| PBR 589–591 | Rails runner on live WUT PG | ✅ |

**Test command(s):**
```bash
cd winston_unit_test && bundle exec rspec spec/lib/tailscale_script_name_spec.rb
cd winston_v2 && bundle exec rspec spec/lib/tailscale_script_name_spec.rb
curl -sI https://sawtooth-ai.tail944ffb.ts.net/wut/ | grep -E 'HTTP/|location:'
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None added
- **Services:** `bin/compose restart winston_unit_test winston_v2` (Puma pick-up of middleware)
- **Migrations:** none in this wrap’s file set (Edge migration exists uncommitted in WUT)

---

## 9. Risks & Technical Debt

- Two `TailscaleScriptName` copies (WUT + Wv2) by design; ADR-016 says copy the **spec** with the middleware. DM has no copy yet.
- WUT/Wv2/ecosystem `main` remain dirty with other session work; a naive `git add .` would mix secrets-adjacent vendor and unrelated ops diffs.
- 590’s Edge is GOOGL-path concentrated — easy to overfit in the next cell.

---

## 10. Open Questions

- **Commit leftover Edge / confirm-sync / Wv2 ops in a second wrap?** — operator; blocks a clean `main`.
- **Next Blue cell: static 2% vs pyramid cap 2?** — operator; does not block Tailscale.

---

## 11. Handoff & Resume Notes

- **Where I left off:** `/wut/` live 200; ADR-016 written; C03 eval given; wrap waiting on follow-up promotion then commit of the table in §3 only.
- **Next concrete step:** Operator shortcut on §14; then commit/push those files. After that, optional Blue cell (590 knobs, drop OWD or cap L3+).
- **Files to read first:**
  1. `ecosystem/docs/adr/ADR-016-tailscale-serve-rails-subpath.md`
  2. `winston_unit_test/lib/tailscale_script_name.rb`
  3. This report §15 (C03 numbers)

---

## 12. Stakeholder Communications

- _None._ Lab UI outage + lab C03 eval; no capital or Telegram.

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report, operator-prose, graphify-ponytail (wrap step 2)
- **Graphify Graph:** updated `ecosystem/`, `winston_unit_test/`, `winston_v2/` via `graphify update` (AST). Merged 6 graphs → workspace `graphify-out/graph.json` (24098 nodes, 32600 edges). Not staged.
- **Ponytail flags:** `TailscaleScriptName` still lives as two monolith copies (`winston_unit_test/lib/tailscale_script_name.rb` L16 and Wv2 twin). Fixed both; did not extract a shared gem. ADR-016: copy the spec with the middleware. No new helper that already existed on the graph.
- **What worked well:** curl of MagicDNS vs localhost isolated Serve strip vs Rails 302; dating the landmine in `git log -p` on one file.
- **Friction points:** Compaction hid earlier Edge/confirm work; wrap must not scoop the whole dirty tree. No browser tools for UI verify.
- **Subagent usage:** None

---

## 14. Follow-up Actions

Wrap Step 3: operator chose **`skip all`** — items subsumed elsewhere; not filed as tickets/tasks.

- [x] ~~Commit leftover WUT Edge + confirm-sync + Finder ` 2.js`~~ — skipped (subsumed)
- [x] ~~Commit leftover Wv2 Edge / ops dirty tree~~ — skipped (subsumed)
- [x] ~~Next Blue PBR freeze 590 knobs~~ — skipped (subsumed)
- [x] ~~Hard-refresh PBR index~~ — skipped (subsumed)

---

## 15. Appendix (optional)

### Tailscale landmine

- 2026-07-04 `ee23c3b` — SCRIPT_NAME only (correct)
- 2026-07-06 `1a91ef5` — 302 `/` → `/wut/` inside a trend-vetting commit
- 2026-07-22 `740bbae` — same middleware copied to Wv2
- Live: Serve `/wut` → `127.0.0.1:3000` strips prefix; Puma saw `GET /`

### Blue C03 (hybrid fill, OWD, max 4 markets, 2020-08-05–2026-09-11)

| PBR | TS | Confirm | lots/sym | Return | DD | Edge | PF | E50 vs rand | Notes |
|-----|----|---------|----------|--------|-----|------|----|-------------|-------|
| 589 | #24 | EMA-20 | 5 | +77% | 39% still in it 198d | +0.16R n=164 | 1.06 | 1.10 / 1.19 worse | L4/L5 toxic |
| 590 | #24 | EMA-20 | 4 | +307% | 41% recovered; 128d new DD | +0.90R n=99 thin | 2.82 | 1.11 / 0.92 beats | GOOGL ~80% of Edge |
| 591 | #23 | none | 4 | +71% | 45% still in it 168d | +0.40R n=96 thin | 1.41 | 0.80 / 0.96 worse | valid no-confirm control |

Turtle bar (+0.3R–+0.7R **and** PF 1.6–2.2 **and** E50 ~1.2): 590 clears Edge and PF, misses E50 ~1.2. Not trade-ready.
