# Session Report — Telegram rich_message Desktop Patch

**Date:** 2026-07-14  
**Time:** ~15:20–15:45 MDT  
**Duration:** ~25m  
**Project:** Sawtooth / Cromwell (nanobot Telegram gateway)  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `ecosystem` main (session report only — runtime `ai/nanobot` is outside any monolith git)  
**Model:** Grok  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Diagnose Telegram Desktop “This message is not supported by your version of Telegram…” while already on latest stable; then disable the offending send path.

**Outcome:** Delivered

**One-line summary:** Cromwell was sending Bot API 10.1 `sendRichMessage` (`rich_message`); we force-disabled that path in the nanobot image so replies use legacy HTML `send_message` that Desktop can render.

---

## 2. Work Completed

- Traced Telegram unsupported-message symptom to live `nanobot-ai==0.2.2` (not attic openclawd copy).
- Confirmed outbound path tries `sendRichMessage` first; API accepts it, so `_rich_send_disabled` never latched; Desktop stable cannot render `Message.rich_message`.
- Patched `ai/nanobot/Containerfile` to force `_rich_send_disabled = True` at build time.
- Rebuilt image `localhost/sawtooth_nanobot_cromwell:latest` and recreated `nanobot_cromwell`.
- Verified in running container: flag is True; bot connected (`@sawtooth_nanobot`); MCP winston connected.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `ai/nanobot/Containerfile` | modified | Build-time sed of `nanobot` telegram channel: `_rich_send_disabled=True` |
| `ecosystem/docs/session-reports/2026-07-14-1545-telegram-rich-message-desktop-patch.md` | added | This report |

### Commits

- _Filled at wrap after commit._

### Branch / PR state at sign-off

- Branch: `ecosystem` `main`
- Runtime patch path `ai/nanobot/Containerfile` is **outside every monolith git repo** (workspace root is not a git project). Only this session report is versioned under `ecosystem`.
- PR: not opened (docs-only on main)

---

## 4. Decisions Made

### Decision 1: Force-disable rich send at image build
- **Choice:** Patch installed `nanobot/channels/telegram.py` during `Containerfile` build so `_rich_send_disabled` starts `True`.
- **Why:** No config knob in nanobot schema; API does not fail for rich messages, so runtime auto-latch never fires. Clients lack renderer.
- **Alternatives considered:** (1) Downgrade nanobot-ai, (2) client-side only (use mobile/beta), (3) monkey-patch at container start.
- **Reversibility:** Easy — remove the RUN patch step and rebuild; or set flag back to False when Desktop/Web support rich messages.
- **Promote to ADR?** No — operational compatibility pin; document in Containerfile + this report.

### Decision 2: Do not change Wv2 PDF Telegram delivery
- **Choice:** Leave `TelegramReportDelivery` / `sendDocument` alone.
- **Why:** Documents are not the unsupported type; rich text messages are.
- **Alternatives considered:** N/A
- **Reversibility:** N/A
- **Promote to ADR?** No

---

## 5. Insights Surfaced

- Live Cromwell gateway is **pip package** `nanobot-ai==0.2.2` in a slim image — not the attic `openclawd-stack/nanobot` source tree (that older tree used `send_message_draft` for progress; current package uses stream edit + rich final).
- Bot API **10.1** (2026-06) added `sendRichMessage` / `rich_message`. Server accepts; many stable Desktop/Web clients still show the generic “feature not yet implemented” placeholder. Mobile often works.
- `_rich_send_disabled` only flips on *API capability errors*, not client render failures — classic server/client skew bug.
- Workspace `ai/` (compose build context for nanobot) is **not in git**; ecosystem `ai/` holds agent skills/personas only. Patch durability depends on disk + image layers, not a monolith repo unless later vendored.

---

## 6. Issues & Tickets

### Resolved this session
- Telegram Desktop “message not supported” for Cromwell prose replies — root cause `sendRichMessage`; mitigated by force legacy HTML path.

### Deferred
- Re-enable rich messages when Desktop/Web support is confirmed; gate on client capability or nanobot config if upstream adds one.
- Consider vendoring or tracking `ai/nanobot/Containerfile` in a real git home so rebuilds are reproducible across clones.
- After `nanobot-ai` bump: re-validate patch string still matches (build asserts or fails).

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Containerfile patch string | Build step printed `patched ... ->_rich_send_disabled=True` | ✅ |
| Running image | `podman exec` inspect of `TelegramChannel.__init__` | ✅ `_rich_send_disabled: bool = True` |
| Gateway health | `podman logs nanobot_cromwell` | ✅ bot connected, MCP winston, cron jobs |
| End-to-end Telegram Desktop | Manual ping after deploy | ⚠️ Operator should confirm next live reply renders |

**Test command(s):**

```bash
podman exec nanobot_cromwell python -c "import inspect, nanobot.channels.telegram as t; print([l for l in inspect.getsource(t.TelegramChannel.__init__).splitlines() if 'rich_send' in l])"
podman logs --tail 30 nanobot_cromwell
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** Still `nanobot-ai==0.2.2` (no version bump); build-time source patch only.
- **Services:** Rebuilt/recreated `nanobot_cromwell`; compose `--force-recreate` briefly churned dependent AI/core containers (redis/postgres/etc. recovered; all were running after).
- **Migrations:** None

---

## 9. Risks & Technical Debt

- **Untracked Containerfile:** `ai/nanobot/Containerfile` is not in any monolith git repo — easy to lose on clean machine unless image/cache remains.
- **Brittle pin:** Patch matches exact upstream comment string; fails build if nanobot-ai renames the flag (good fail-closed).
- **Compose recreate blast radius:** `./bin/compose --profile ai up -d --force-recreate nanobot_cromwell` stopped a wide dependency set; prefer targeted rebuild + `podman restart` / recreate single container when possible.

---

## 10. Open Questions

- **When does Telegram Desktop stable render `rich_message`?** — needs client release notes; blocks safe removal of the force-disable.
- **Should workspace-root `ai/` + `compose.yml` gain a git home?** — ops durability; does not block current fix.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Image rebuilt, `nanobot_cromwell` running with rich send forced off; awaiting human Desktop smoke test.
- **Next concrete step:** Send a short message to Cromwell in Telegram Desktop and confirm the reply is readable (not the unsupported placeholder). Old unsupported bubbles remain historical.
- **Files to read first:**
  1. `ai/nanobot/Containerfile` (patch RUN step)
  2. This session report
  3. Live package (in container): `nanobot/channels/telegram.py` (`_try_send_rich`, `send`, `send_delta`)

---

## 12. Stakeholder Communications

- _None required unless Desktop still fails after a fresh bot reply._

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report
- **What worked well:** Inspecting the *running* package via `podman exec` + `inspect.getsource` (attic source would have misled).
- **Friction points:** Dockerfile heredocs break older podman/buildah parsers — used one-line `python -c` patch instead. Compose force-recreate wider than intended.
- **Subagent usage:** None

---

## 14. Follow-up Actions

- [ ] Confirm one fresh Cromwell reply on Telegram Desktop — owner: operator — due: next session
- [ ] On next `nanobot-ai` bump, re-check rich-send patch still applies — owner: whoever bumps Containerfile pin
- [ ] Optional: track `ai/nanobot/Containerfile` in a git-backed path — owner: ecosystem/ops

---

## 15. Appendix (optional)

### Symptom (user)
> This message is not supported by your version of Telegram. Please update to the latest version in Settings > Advanced, or install it from https://desktop.telegram.org. If you are already using the latest version, this message might depend on a feature that is not yet implemented.

### Culprit API (live nanobot)
```text
do_api_request("sendRichMessage", {
  "chat_id": ...,
  "rich_message": { "markdown": "<reply>" }
})
```

### Patch effect
```python
# before
self._rich_send_disabled: bool = False  # Latch off if Bot API < 10.1
# after (forced)
self._rich_send_disabled: bool = True  # Forced off: Desktop/Web lack rich_message support
```

### Rebuild commands used
```bash
podman build -f ./ai/nanobot/Containerfile -t localhost/sawtooth_nanobot_cromwell:latest ./ai/nanobot
./bin/compose --profile ai up -d --force-recreate nanobot_cromwell
```
