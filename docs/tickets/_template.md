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
Follow ticket <path>. System One harness above. Push main. In-band wrap.
```

## Non-goals

- …
