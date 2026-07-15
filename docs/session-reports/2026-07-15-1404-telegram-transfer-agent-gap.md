# Session Report — Telegram transfer agent gap + Phase 3 runbook live

**Date:** 2026-07-15  
**Time:** ~prior evening 2026-07-14 into 14:04 MDT 2026-07-15  
**Duration:** multi-slice (~operator verification + Telegram debug + LLM reliability)  
**Project:** sawtooth Winston ecosystem (cross-monolith)  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `ecosystem` / `winston_unit_test` — `main`  
**Model:** Grok 4.5 (xAI)  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Walk Phase 3 operator runbook live; then import/transfer portfolio via Telegram; fix failures; wrap with tickets.

**Outcome:** Partially delivered (platform handoff works; agent reply quality still broken — tickets filed for next session **A**)

**One-line summary:** OP `#157` is the WUT run 57 handoff; Telegram “failure” was mostly LLM timeout + bad post-tool prose, not missing import code.

---

## 2. Work Completed

- Live walk of Phase 3 verification runbook A–H (pass; sole Active `#12`).  
- Operator walkthrough of same runbook for manual re-run.  
- Diagnosed Telegram privacy mode (`can_read_all_group_messages: false` → need @mention).  
- Diagnosed transfer tool null-arg validation + WUT `portfolio_config` accidentally private.  
- Fixed WUT actions public; MCP null-tolerant schema + int coercion (host MCP).  
- Smoke + Telegram transfer: `#157 Portfolio Blank (WUT run 57)`, paper, inactive.  
- Bumped Cromwell to `cromwell-qwen3:8b`, think off, longer LLM timeouts.  
- Explained agent-vs-machinery gap ELI18.  
- Filed tickets A–E for next session.

---

## 3. Code Delivered

### Files changed

| File | Change | Repo |
|------|--------|------|
| `winston_unit_test/app/controllers/internal_controller.rb` | `public` for portfolio_config / strategy_config / testing_strategies | `winston_unit_test` |
| `ai/mcp_winston/mcp_winston/server.py` | transfer null/int coerce; schema | host `ai/mcp_winston` (not ecosystem git) |
| `ai/mcp_winston/mcp_winston/tools_schema.py` | parent_correlation_id null-ok | host |
| `ai/data/cromwell-bot/config.json` | 8b, think false, reasoning_effort none | host local |
| `compose.yml` (root) | NANOBOT timeouts 600/900 | host local |
| `ecosystem/docs/tickets/2026-07-15-*.md` | A–E tickets | `ecosystem` |
| this session report | added | `ecosystem` |

### Commits

_Filled at commit time._

### Branch / PR state at sign-off

- Ecosystem + WUT commits pushed if wrap succeeds.  
- Host MCP/compose/config: operator must preserve or re-apply (see ticket D).

---

## 4. Decisions Made

### Decision 1: #157 is the transfer artifact
- **Choice:** Treat OP `#157` as WUT run 57 on Wv2; do not require second create.  
- **Why:** Transfer already succeeded (create then `legacy_updated`).  
- **Reversibility:** easy (destroy inactive OP if undesired).  

### Decision 2: Prefer agent quality over ops stopgap
- **Choice:** No desk/rake as primary handoff path; fix Cromwell reply + export + MCP summary.  
- **Why:** Operator wants Telegram path trustworthy.  

### Decision 3: 8b + think off on CPU
- **Choice:** `cromwell-qwen3:8b` with `think: false` and longer timeouts vs staying on 3b.  
- **Why:** 3b tool selection catastrophic; 8b timed out until think/timeouts fixed.  

### Decision 4: Next session starts at A
- **Choice:** Ticket A (reply contract) first.  

---

## 5. Insights Surfaced

- Telegram group privacy drops non-@mention messages silently.  
- Small models invent explanations for schema errors (`null` ≠ string).  
- Transfer tool was never the long-term gap; **post-tool narration** was.  
- WUT run export without fingerprint forces permanent `legacy_*` path.  
- Podman compose force-recreate cascades stop/rm and name conflicts.  
- Generic MCP `retry_guidance` (fetch_only / 4:30) pollutes unrelated 422s.  

---

## 6. Issues & Tickets

### Resolved this session
- Phase 3 runbook A–H operator-verified (prior slice + this).  
- WUT `portfolio_config` ActionNotFound (private methods) fixed.  
- Transfer path end-to-end proven (`#157`).  

### Filed this wrap

| Ticket | Bucket | Role |
|--------|--------|------|
| `2026-07-15-cromwell-transfer-reply-contract.md` | **A** next | Skill/persona success template |
| `2026-07-15-wut-portfolio-config-fingerprint-export.md` | **B** | Fingerprint/seed on run export |
| `2026-07-15-mcp-transfer-summary-and-error-guidance.md` | **C** | summary field + clean errors |
| `2026-07-15-cromwell-llm-cpu-reliability.md` | **D** | timeouts/think/cron docs |
| `2026-07-15-telegram-handoff-non-goals.md` | **E** | anti-scope |

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Phase 3 runbook A–H | live rails runner | ✅ |
| Lifecycle specs (optional G) | 41 examples | ✅ |
| WUT portfolio_config run 57 | HTTP 200 from mcp net | ✅ |
| Transfer → #157 | MCP + Telegram tool audit | ✅ `legacy_updated` |
| Cromwell reply quality | Telegram | ❌ menus / ignored action |
| 8b + think false latency | api/chat ~1.6s warm | ✅ ops |

**Test command(s):** see Phase 3 wrap report §15; transfer audit `mcp_audit_*.jsonl` tool `wv2_transfer_portfolio_from_wut`.

---

## 8. Environment, Dependencies, Data

- **Services:** compose + `--profile ai` (ollama, winston_mcp, nanobot).  
- **Live OPs:** `#12` sole Active (Blue · PBR62); `#157` inactive Blank run 57.  
- **Config:** Cromwell model 8b; think false; timeouts 600/900 on root compose.  

---

## 9. Risks & Technical Debt

- MCP source not in ecosystem git (existing ticket).  
- Root compose vs `ecosystem/deployment/compose.yml` divergence.  
- Cron + user DM share one Ollama parallel slot.  
- Agent still free-forms after correct tools.  

---

## 10. Open Questions

- **Should re-transfer of run 57 keep human name `Portfolio Blank (WUT run 57)` or seed from lab Blank?** — product; ticket B.  
- **GPU ever on this host?** — if yes, 8b thinking optional.  

---

## 11. Handoff & Resume Notes

- **Where I left off:** Tickets A–E filed; transfer works; reply contract is next.  
- **Next concrete step:** Open ticket A → edit `winston-wut-to-wv2` skill + persona; re-seed workspace; Telegram smoke.  
- **Files to read first:**  
  1. `docs/tickets/2026-07-15-cromwell-transfer-reply-contract.md`  
  2. `ai/skills/winston-wut-to-wv2/SKILL.md`  
  3. Session transcript tool results for transfer `legacy_updated`  
  4. Live: `Portfolio.find(157)`  

---

## 12. Stakeholder Communications

- _None required beyond operator handoff._  

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report, record (tickets).  
- **What worked well:** reading session JSONL for exact tool calls.  
- **Friction:** podman-compose recreate; 8b thinking; silent Telegram privacy.  

---

## 14. Follow-up Actions

- [ ] **Next session: Ticket A** — reply contract  
- [ ] Then B → C → remaining D  
- [ ] Preserve host MCP patch / rebuild image when git-home exists  
- [ ] Optional destroy `#157` only if operator wants clean re-demo  

---

## 15. Appendix

### Transfer tool result (Telegram success)

```json
{
  "status": "ok",
  "action": "legacy_updated",
  "warnings": [
    "legacy_no_fingerprint: bare-name path (ADR-006 transition); re-export with fingerprint when possible",
    "paper_caps:max_markets normalized to 4 (was nil)",
    "paper_caps:max_leverage normalized to 1.0 (was nil)"
  ]
}
```

Portfolio id **157**, name **Portfolio Blank (WUT run 57)**, active **false**.

### Mental model

Tech did the homework; bot wrote a book report about the wrong chapter.
