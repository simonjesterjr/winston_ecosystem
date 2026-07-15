# Session Report — Cromwell reply contract, fingerprint export, Tier 0 isolation

**Date:** 2026-07-15  
**Time:** ~15:00–17:22 MDT  
**Duration:** ~2h 20m  
**Project:** sawtooth Winston ecosystem (cross-monolith)  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `ecosystem` `main`; `winston_unit_test` `main`  
**Model:** Grok 4.5 (xAI)  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Execute ticket A (Cromwell transfer reply contract); then B (fingerprint export); record concurrency tiers; implement Tier 0 session isolation; unblock A smoke.

**Outcome:** Partially delivered — A docs+MCP levers landed but **live Telegram quality still fails acceptance**; B done and smokes green; Tier 0 isolation deployed; concurrency tickets filed.

**One-line summary:** Transfer machinery works; agent prose and shared-session cron were the real gaps — skills alone insufficient; fingerprint export and isolated cron sessions are the structural fixes.

---

## 2. Work Completed

- Ticket A: hardened `winston-wut-to-wv2` skill, always-on AGENTS HARD RULES, channels/tools guidance, MEMORY few-shot; seeded Cromwell; restarted bot.
- Live smoke: transfer run 57 OK (`legacy_updated` #157) but reply still menu-heavy; “activate the portfolio” lost #157 context; activate API succeeded while LLM hung.
- Partial ticket C: MCP `_attach_agent_summary` + `reply_hint` for transfer/activate/deactivate (host `ai/mcp_winston`, image rebuilt).
- Filed Tier 0/1/2 concurrency tickets; linked from ticket D.
- Restarted nanobot to free stuck agent lock; confirmed #157 active=true (dual Active with #12).
- Ticket B: `PortfolioConfigExporter`; `portfolio_config?run_id=` includes fingerprint/seed_name/export_kind; specs green; live re-import `adopted` #10.
- Tier 0: all Cromwell cron jobs `sessionKey: cron:<job-id>` (origin still Sawtooth Main); README + AGENTS; seeded + nanobot restart.
- Operator guidance: Telegram phrasing for transfer PBR 41 (Orange) then activate by id.

---

## 3. Code Delivered

### Files changed

| File | Change | Repo |
|------|--------|------|
| `ecosystem/ai/skills/winston-wut-to-wv2/SKILL.md` | Success template; forbid auto-chain menus | ecosystem |
| `ecosystem/ai/skills/winston-portfolio-lifecycle/SKILL.md` | Activate playbook; resolve “the portfolio” | ecosystem |
| `ecosystem/ai/skills/winston-wut-portfolio-lifecycle/SKILL.md` | Transfer stops at reply contract | ecosystem |
| `ecosystem/ai/personas/cromwell-agents.md` | HARD RULES; concurrency truth | ecosystem |
| `ecosystem/ai/personas/cromwell-channels.md` | Handoff no-menus | ecosystem |
| `ecosystem/ai/personas/cromwell-tools.md` | Lead with mutating tool result | ecosystem |
| `ecosystem/ai/memory/templates/MEMORY.template.md` | Handoff few-shot | ecosystem |
| `ecosystem/ai/schedule/cromwell-cron.json` | Isolated `cron:<job-id>` sessionKeys | ecosystem |
| `ecosystem/ai/schedule/README.md` | Tier 0 + busy-ack gap docs | ecosystem |
| `ecosystem/ai/VERSION` | 1.4.0 → 1.4.3 | ecosystem |
| `ecosystem/interfaces/winston-mcp-tools.md` | Transfer notes + summary field | ecosystem |
| `ecosystem/docs/tickets/2026-07-15-*.md` | A/B/C/D updates + Tier 0/1/2 new | ecosystem |
| `winston_unit_test/app/services/portfolio_config_exporter.rb` | **added** ADR-006 export builder | WUT |
| `winston_unit_test/app/controllers/internal_controller.rb` | portfolio_config → exporter | WUT |
| `winston_unit_test/lib/tasks/portfolio_configs.rake` | Thin wrapper | WUT |
| `winston_unit_test/spec/services/portfolio_config_exporter_spec.rb` | **added** 3 examples | WUT |
| `ai/mcp_winston/mcp_winston/server.py` | `_attach_agent_summary` | host (not git) |
| `bin/seed-cromwell-workspace` | Help text for cron merge | workspace root (may be outside git) |

### Commits

_Filled at commit time._

### Branch / PR state at sign-off

- `ecosystem` `main` — commit+push in wrap  
- `winston_unit_test` `main` — commit+push in wrap  
- Host MCP image rebuilt with summary; not in a tracked repo  

---

## 4. Decisions Made

### Decision 1: Skills alone insufficient for A
- **Choice:** Put reply contract in always-on `AGENTS.md` HARD RULES + MCP `summary`/`reply_hint`.  
- **Why:** 8b rarely `read_file`s skills; live smoke still menu’d after skill-only land.  
- **Reversibility:** easy.  
- **Promote to ADR?** no  

### Decision 2: Cron sessionKey isolation (Tier 0)
- **Choice:** `sessionKey: cron:<job-id>` with `originChatId` for Sawtooth Main delivery.  
- **Why:** Shared group session caused auto-compact + pending-queue during user handoffs.  
- **Alternatives:** dual nanobot, raise concurrency (deferred Tier 1).  
- **Reversibility:** easy (revert JSON + seed).  

### Decision 3: Shared PortfolioConfigExporter for B
- **Choice:** One service for rake + internal API.  
- **Why:** MCP transfer was permanently `legacy_*` while file export had fingerprints.  
- **Reversibility:** easy.  

### Decision 4: Do not auto-destroy #157
- **Choice:** Leave legacy #157; fingerprinted re-import adopted #10.  
- **Why:** Operator hygiene, not silent cleanup.  

---

## 5. Insights Surfaced

- Double choke: `NANOBOT_MAX_CONCURRENT_REQUESTS=1` + `OLLAMA_NUM_PARALLEL=1` + shared session was worse than serial LLM alone.  
- `podman-compose up --no-deps` still cascades dependency stop/rm name conflicts — use `podman restart` / stop-rm-up carefully.  
- Transfer tool JSON already had full portfolio block; model ignored it.  
- Activate completed in 40ms; multi-minute “failure” was post-tool LLM + extra `get_portfolio_status` + Flood Control.  
- Run 41 Orange exports fingerprinted observation; ready for A re-smoke after Tier 0.  

---

## 6. Issues & Tickets

### Resolved this session
- B fingerprint export (code + smoke)  
- Tier 0 session isolation (deployed)  
- Partial C summary field on MCP  
- Concurrency design captured as tickets  

### Deferred
- A acceptance (Telegram first-two-lines quality) — still open  
- Busy-ack (nanobot product gap) — documented only  
- Dual-Active hygiene (#12 + #157)  
- Thin cron / dual runtime (Tier 2 / Tier 1 tickets)  
- Host MCP git-home (existing ticket)  
- `bin/seed-cromwell-workspace` if not in a git root  

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| A skill/personas seed | seed + restart | ✅ |
| A live Telegram reply quality | operator smoke | ❌ menus / context loss |
| Activate #157 | Wv2 API + audit | ✅ active=true |
| MCP summary helper | in rebuilt image | ✅ |
| B exporter specs | rspec 3 examples | ✅ |
| B live run 57 export | curl fingerprint | ✅ |
| B re-import | action=adopted #10 | ✅ |
| Tier 0 jobs.json | all `cron:<id>` | ✅ |
| Nanobot after restart | MCP connected | ✅ |

**Test command(s):**

```bash
curl -sS "http://localhost:3000/internal/portfolio_config?run_id=57" | jq '{seed_name,fingerprint,export_kind}'
podman exec winston_unit_test bundle exec rspec spec/services/portfolio_config_exporter_spec.rb
python3 -c "import json;j=json.load(open('ai/data/cromwell-bot/workspace/cron/jobs.json'));print([ (x['id'],x['payload']['sessionKey']) for x in j['jobs']])"
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new  
- **Services:** nanobot_cromwell, winston_mcp rebuilt/restarted; compose cascade briefly disrupted stack (recovered)  
- **Migrations:** None  
- **Runtime seed:** ecosystem/ai VERSION 1.4.3  

---

## 9. Risks & Technical Debt

- A still red on live model behavior — structural levers in place but unproven.  
- Dual Active #12 + #157 may confuse Daily Analysis focus.  
- Legacy #157 vs fingerprinted #10 naming/seed divergence.  
- MCP summary only on host image until git-home lands.  
- Busy-ack still absent — silent wait under global lock.  

---

## 10. Open Questions

- **Should #157 be deactivated/closed after fingerprinted Orange/Blank work?** — operator  
- **Is observation export_kind correct for paper activate of PBR 41?** — business; gates say observation  
- **Nanobot patch for busy-ack?** — product vs ops  

---

## 11. Handoff & Resume Notes

- **Where I left off:** Tier 0 deployed; A smoke not re-run; operator asked for Telegram phrasing for PBR 41.  
- **Next concrete step:** Telegram `@sawtooth_nanobot transfer WUT run 41 to Wv2` then activate by returned `#id`; judge A acceptance on first two lines.  
- **Files to read first:**  
  1. `ecosystem/docs/tickets/2026-07-15-cromwell-transfer-reply-contract.md`  
  2. `ecosystem/docs/tickets/2026-07-15-cromwell-cron-session-isolation-busy-ack.md`  
  3. `ecosystem/ai/skills/winston-wut-to-wv2/SKILL.md`  
  4. `winston_unit_test/app/services/portfolio_config_exporter.rb`  

---

## 12. Stakeholder Communications

- _None formal._ Operator has Telegram phrasing for Orange PBR 41.  

---

## 13. Tools & Workflow Notes

- **Skills used:** record, wrap, session-report  
- **What worked well:** shared exporter for B; live curl + Wv2 import smoke  
- **Friction points:** compose recreate cascade; 8b multi-minute turns; skills not auto-injected  
- **Subagent usage:** none  

---

## 14. Follow-up Actions

- [ ] Re-smoke A: transfer run 41 (or 57) after Tier 0; confirm first two lines have action + #id, no menus  
- [ ] Dual-Active hygiene: decide Active set (#12 / #157 / new Orange OP)  
- [ ] Host: commit MCP summary into tracked mcp-winston home when available  
- [ ] Tier 2 thin cron when ready  
- [ ] Commit bin/seed-cromwell-workspace if it lives outside ecosystem git  

---

## 15. Appendix

### Telegram phrasing (PBR 41 Orange)

```text
@sawtooth_nanobot transfer WUT run 41 to Wv2
@sawtooth_nanobot activate portfolio <id from reply>
```

### Run 41 export snapshot

- seed_name: Portfolio Orange  
- fingerprint: present (6622b2eb…)  
- export_kind: observation  
- wut_trading_strategy_id: 11  
