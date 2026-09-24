# Ticket: \<short title\>

**Status:** Proposed  
**Priority:** P0 | P1 | P2 | P3 | unset  
**Date:** YYYY-MM-DD  
**Lane:** A (plan + System One harness + Grok CLI) | B (hotfix/small; short harness)  
**Implementer:** Grok CLI | Winston Dev (Lane B only) | …  
**DoD:** …

## Goal

One paragraph: what done looks like.

## Context / specimens

Links to journals, PBRs, analysis, parent plan/ADR.

## Work items

- [ ] …

## System One harness

Required for Lane A and non-trivial Lane B. Skip only for trivial renames/doc moves.  
Law: [`../business-context/jev-desk-guardrails.md`](../business-context/jev-desk-guardrails.md).

**State:** (facts Jev may see — paths to probe JSON, journal fields, autopsy excerpt; keep deterministic numbers here)

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| e.g. heat_label_lie | Noul | heat_mode claims turtle but heat hash absent | noul ≥ 0.85 → FAIL promote |
| e.g. route | Choice | options: ship, hold, escalate | choice=ship ∧ confidence ≥ 0.7 |

**Runner:** `jev ask …` / `./ecosystem/scripts/jev-desk-helpers.sh` / `probe_before_promote.sh`  
**Order:** deterministic code/probe first; Jev on residual semantic smells.  
**On fail:** stop · update ticket · do not promote / do not claim Done.

## CLI seed (when Grok CLI implements)

```
cwd: /home/johnkoisch/Documents/com/sawtooth
Lane <A|B>. <one paragraph goal>
Follow ticket <path>. System One harness above.
Tee every jev ask (state + questions + answers) into TUI + wrap.
Push main. In-band wrap.
```

### CLI seed — tee Jev System One (default)

At every System One checkpoint in this ticket/plan:

1. Print a clear TUI banner: `=== Jev System One ===`
2. Print the **state** blob (facts / probe JSON / autopsy excerpt) verbatim.
3. Print each question (Noul / Choice / Score) before calling `jev`.
4. Run `jev ask` (desk: `jevctl` / `ecosystem/scripts/jev-desk-helpers.sh`); do not silently skip when `TYPESAFE_API_KEY` is set.
5. Print the JSON answers (and confidence) in the TUI; append the same block to the in-band wrap / ticket Results.
6. Branch fail-closed on harness pass rules. Deterministic probes run first; Jev judges residual semantic smells only.

If Jev is unavailable, print `Jev skipped: <reason>` and continue only if the ticket allows probe-only; never pretend Jev passed. Prefer `jevctl` over the TypeSafe Python SDK.

## Non-goals

- …
