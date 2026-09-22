# Ticket: Probe-before-promote checklist (v1+v2) + Jev System One state gates

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-09-21  
**Owner:** Sawtooth Ops (run); Chief of Staff (orchestrate); Forensics (consume)  
**DoD:** Script + wrapper live on sawtooth; specimen PBRs 727/743/763/764 probed; ticket indexed; promote screens must attach PASS output  
**Related:** [`../business-context/sawtooth-host-ops-dod.md`](../business-context/sawtooth-host-ops-dod.md); heat autopsy [`../analysis/2026-09-21-teal-heat-on-dd-autopsy-763-764.md`](../analysis/2026-09-21-teal-heat-on-dd-autopsy-763-764.md); packaging M-band [`2026-09-21-packaging-sub100-share-vs-option-m-band.md`](2026-09-21-packaging-sub100-share-vs-option-m-band.md)

## Goal

Before Mode C promote / “prefer this cell” language, run a **host** Portfolio Backtest Run (PBR) probe that fails closed on known lies:

### v1
1. **Heat intent vs reality** — `heat_mode: turtle` (or cell intends turtle) requires heat hash + `heat_enabled?` (#727 class)
2. **Position caps** — peak `open_positions` from `cash_events` ≤ `max_positions_per_portfolio`; count breaches (#763/#764 class)
3. **Packaging contracts** — LEAP/call preference with `floor(share_units/100)==0` or stock-only fills despite leap pref (#1984 class)
4. **Identity** — portfolio / Trading Strategy (TS) / risk / cadence printed

### v2
5. **Edge_R present** on completed non-barren runs  
6. **Open Analysis (OA) drawdown sanity** — heat-ON + OA DD ≥ 50% → FAIL smell  
7. **Runner SHA** — informational container git short SHA  

### Jev System One (typed yes/no)
Wrapper asks Jev three `noul` questions on the probe facts:
- heat label lie?
- cap breach?
- zero contracts / stock-only despite LEAP pref?

## How to run

```bash
cd /home/johnkoisch/Documents/com/sawtooth
./ecosystem/scripts/probe_before_promote.sh 727 743 763 764
```

Outputs:
- `ecosystem/docs/analysis/probe-before-promote-last.json`
- `ecosystem/docs/analysis/probe-before-promote-last.md`
- `ecosystem/docs/analysis/probe-before-promote-last-jev.json` (when TypeSafe key present)

Exit code 2 if any PBR FAIL (`PROBE_STRICT=1` default).

## Work items

- [x] v1+v2 ruby probe
- [x] shell wrapper + Jev asks
- [x] ticket + INDEX
- [ ] Required checkbox on promote-screen tickets (follow-up)
- [ ] Optional: Wv2 journal probe mode for #1984-class desk fills
