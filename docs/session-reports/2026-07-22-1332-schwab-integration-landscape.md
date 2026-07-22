# Session Report — Schwab / ToS Access Landscape + Extra-Modal Fulfillment

**Date:** 2026-07-22  
**Time:** ~session morning–13:32 local  
**Duration:** ~multi-turn research + docs (estimate ~1–2h wall)  
**Project:** sawtooth Winston ecosystem  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `main` (ecosystem)  
**Model:** Grok 4.5 (xAI)  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Research best ways to integrate with Schwab (API, email, webhooks, automation including trade execution); expand discovery for full automation without implementing; tie to existing grill/analysis; later deepen landscape for thinkorswim systematic access; capture **extra-modal fulfillment** (signal market vs LEAP/futures/CLETF packaging).

**Outcome:** Delivered (analysis + glossary; no implementation; grill started but not completed)

**One-line summary:** Filed pre-design Schwab/ToS access landscape and Winston-scoped discovery (API-primary intake, L0–L4 automation ladder), crystallized **Extra-Modal Fulfillment** in CONTEXT, and cross-linked parent broker-intake ticket + fulfillment grill tee.

---

## 2. Work Completed

- Researched Schwab Trader API (Individual): OAuth lifetimes, REST accounts/orders/transactions, streamer `ACCT_ACTIVITY`, rate limits, paperMoney gap, futures write limits, no retail fill webhook.
- Clarified thinkorswim vs API: thinkScript/conditionals are not a full autotrader; systematic access = Schwab API + optional streamer; ToS = human UI.
- Wrote landscape analysis with issue register and dual-spine / extra-modal constraints.
- Wrote Winston-scoped Schwab integration discovery (channel recommendation, BrokerFillEvent draft, L0–L4 ladder).
- Updated parent ticket `2026-07-21-broker-confirmation-email-api-intake` with draft acceptance answers and automation expansion.
- Updated fulfillment ownership analysis (grill tee) for API-primary + second grill block + extra-modal.
- Glossary: **Extra-Modal Fulfillment**; broadened **Fulfillment Packaging**; relationships + dialogue examples.
- Domain BC `human-gated-desk-and-fulfillment.md`: extra-modal paragraph.
- Opened grill Q1 (post-confirm amend) but user continued research rather than answering grill.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/docs/analysis/2026-07-22-schwab-thinkorswim-access-landscape.md` | added | Pre-design landscape + §2a extra-modal |
| `ecosystem/docs/analysis/2026-07-22-schwab-integration-discovery.md` | added | Winston-scoped API vs email + L0–L4 |
| `ecosystem/docs/analysis/2026-07-22-winston-fulfillment-ownership-and-broker-intake.md` | modified | Channel table, grill outcomes, extra-modal, cross-links |
| `ecosystem/docs/tickets/2026-07-21-broker-confirmation-email-api-intake.md` | modified | Draft answers, automation checkbox, extra-modal note |
| `ecosystem/docs/business-context/human-gated-desk-and-fulfillment.md` | modified | Extra-modal dual-spine paragraph |
| `ecosystem/CONTEXT.md` | modified | Extra-Modal Fulfillment; packaging; relationships; dialogue |
| `ecosystem/docs/session-reports/2026-07-22-1332-schwab-integration-landscape.md` | added | This report |

### Commits

- _Pending at report write — wrap will commit._

### Branch / PR state at sign-off

- Branch: `main` (ecosystem) — dirty until wrap commit  
- Pushed: pending wrap  
- PR: not opened (docs on main)

**Monoliths with code changes:** none (ecosystem docs only)

---

## 4. Decisions Made

### Decision 1: API primary for confirmation intake
- **Choice:** Schwab Trader API read (orders + transactions poll) primary; email fallback  
- **Why:** Structure, order/txn ids, partials, unblocks L3 later; email brittle  
- **Alternatives considered:** Email-first, hybrid equal weight  
- **Reversibility:** easy until implementation  
- **Promote to ADR?** No — ticket acceptance + optional note in BC after grill lock

### Decision 2: No retail fill webhook as v1 design center
- **Choice:** Poll + optional streamer; not “Schwab POSTs to us”  
- **Why:** Not a first-class retail product  
- **Alternatives considered:** DIY email-as-push  
- **Reversibility:** easy  
- **Promote to ADR?** No

### Decision 3: Automation ladder L0–L4 outside DA
- **Choice:** L1–L2 near-term; L3/L4 separate component + ADR; never DA place_order  
- **Why:** ADR-009 already; OAuth/token ops; capital risk  
- **Alternatives considered:** Autotrader inside Wv2 DA  
- **Reversibility:** costly if wrong (capital)  
- **Promote to ADR?** L3/L4 only when building write path

### Decision 4: Extra-Modal Fulfillment is normal
- **Choice:** Signal Market stays for DA; cash/returns on packaging (LEAP, futures, CLETF, …); mandatory signal↔fulfillment link; matcher ≠ symbol equality  
- **Why:** Operator product model; already partial as Fulfillment Packaging  
- **Alternatives considered:** Force stock-only fills; re-point Books to fill symbols  
- **Reversibility:** easy in docs; costly if code assumes symbol equality  
- **Promote to ADR?** Optional later if implementation choices hard; glossary + BC sufficient for now

### Decision 5: Do not implement this session
- **Choice:** Analysis only  
- **Why:** User request  
- **Alternatives considered:** Spike OAuth  
- **Reversibility:** n/a  
- **Promote to ADR?** No

---

## 5. Insights Surfaced

- Access token ~30m / refresh ~7d makes unattended L4 hostile without human token hygiene.
- API widely reported **live-only** — no clean paperMoney place_order; Winston paper should stay Winston paper.
- Streamer `ACCT_ACTIVITY` is near-real-time acceleration; REST poll remains catch-up SoT.
- Extra-modal breaks naive `fill.symbol == Book.symbol` matching — design-critical for broker intake.
- Futures may fill via ToS UI for commodity packaging while retail API place_order may not support futures.

---

## 6. Issues & Tickets

### Resolved this session
- _None (no defects)._ Discovery content advanced on existing ticket `2026-07-21-broker-confirmation-email-api-intake`.

### Deferred
- Parent discovery ticket acceptance checkboxes still open (draft answers only) — close after grill. **(report only — skip promote)**  
- Full `/grill-with-docs` on fulfillment ownership + Schwab docs (Q1 posed: post-confirm amend mode). **→ ticket:** [`docs/tickets/2026-07-22-grill-fulfillment-schwab-extra-modal.md`](../tickets/2026-07-22-grill-fulfillment-schwab-extra-modal.md)  
- Single-fulfillment invariant + post-confirm amend (sibling ticket may exist). **(report only — skip promote)**  
- L1 implementation (ingest pipeline) after discovery acceptance. **(report only — skip promote)**  
- L3 “send to broker” ADR/spike — only if product wants horizon. **(report only — skip promote)**  
- Live Schwab spike: OAuth, fixtures for equity/option/txn/stream, futures place probe, email vs API latency. **(report only — skip promote)**

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Schwab public portal docs | web_fetch | ⚠️ Auth-walled / access denied from agent |
| Capability map | Community clients + secondary sources | ⚠️ Medium confidence; spike required |
| CONTEXT / analysis consistency | Manual cross-read | ✅ Docs aligned |
| Code / tests | n/a | _None_ |

**Test command(s):** _None._

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None  
- **Services:** None  
- **Migrations:** None  

---

## 9. Risks & Technical Debt

- Discovery answers are **recommended** not grill-locked — risk of implementing symbol-equality matcher.
- Unofficial API docs drift; production code needs redacted fixtures from a real account.
- Extra-modal risk sizing (ATR share story vs option notional) still under-specified for capital_base.

---

## 10. Open Questions

- **Post-confirm amend mode (A rewrite / B append / C close+reopen)?** — grill Q1; blocks fulfillment identity product law.  
- **Trade-then-book vs intent-first default for real desk?** — product default.  
- **Where does broker adapter live (host worker vs Wv2 vs new monolith)?** — L1/L3 design.  
- **When may BrokerFillEvent auto-confirm paper or real?** — ADR-009 impact.  
- **Does retail API place futures for this account?** — spike.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Docs complete for landscape + extra-modal; grill not finished; no code.  
- **Next concrete step:** `/grill-with-docs` against fulfillment ownership + Schwab discovery (start with amend semantics, then channel lock, then extra-modal match rules).  
- **Files to read first:**  
  1. `ecosystem/docs/analysis/2026-07-22-schwab-thinkorswim-access-landscape.md`  
  2. `ecosystem/docs/analysis/2026-07-22-schwab-integration-discovery.md`  
  3. `ecosystem/docs/analysis/2026-07-22-winston-fulfillment-ownership-and-broker-intake.md`  
  4. `ecosystem/CONTEXT.md` (Extra-Modal Fulfillment, dual spines)  
  5. `ecosystem/docs/tickets/2026-07-21-broker-confirmation-email-api-intake.md`  

---

## 12. Stakeholder Communications

- _None required unless operator wants a non-technical summary of “we researched Schwab, no trading automation built.”_

---

## 13. Tools & Workflow Notes

- **Skills used:** grill-with-docs (partial), session-report, wrap (in progress); web_search / web_fetch for Schwab research  
- **What worked well:** Separating landscape (platform facts) vs discovery (Winston recommendation) vs grill tee (product process)  
- **Friction points:** Official Schwab portal blocked from agent environment  
- **Subagent usage:** None  

---

## 14. Follow-up Actions

- [ ] Complete grill-with-docs on fulfillment + Schwab channel + extra-modal — owner: operator + agent — due: next design session — **See:** [`docs/tickets/2026-07-22-grill-fulfillment-schwab-extra-modal.md`](../tickets/2026-07-22-grill-fulfillment-schwab-extra-modal.md)  
- [ ] Lock parent discovery ticket acceptance (API primary, human confirm, event shape) — owner: after grill — *left in report only*  
- [ ] Ensure single-fulfillment / post-confirm amend ticket is ready before L1 build — *left in report only*  
- [ ] Optional: Schwab OAuth + redacted fixture spike (host, not git PII) — *left in report only*  
- [ ] Optional: L3 adapter ADR only if write-path appetite confirmed — *left in report only*  
- [ ] Risk product rule: methodology risk % vs booked option/future notional for capital sizing — *left in report only*  

### Promotion summary (wrap)

| Item | Action |
|------|--------|
| 1 Grill-with-docs | **Ticket created** `2026-07-22-grill-fulfillment-schwab-extra-modal.md` |
| 2–6 | **Skipped** (session report only) |

---

## 15. Appendix (optional)

**Key external refs (non-normative):**  
- https://developer.schwab.com/  
- schwab-py client + streaming docs  
- Community reports: paperMoney not via developer API; ~7-day refresh token  

**Related series:** `adr-009-desk-fulfillment`
