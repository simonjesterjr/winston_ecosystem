#!/usr/bin/env bash
# Host probe-before-promote + optional Jev System One state questions.
# Usage: ./ecosystem/scripts/probe_before_promote.sh 727 743 763 764
set -euo pipefail
ROOT="${SAWTOOTH_ROOT:-/home/johnkoisch/Documents/com/sawtooth}"
cd "$ROOT"
IDS=("$@")
[[ ${#IDS[@]} -gt 0 ]] || { echo "usage: $0 PBR_ID [PBR_ID…]" >&2; exit 2; }

export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
# shellcheck disable=SC1091
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
if [[ -z "${TYPESAFE_API_KEY:-}" && -f "$HOME/.config/jev/typesafe_api_key" ]]; then
  export TYPESAFE_API_KEY="$(cat "$HOME/.config/jev/typesafe_api_key")"
fi

OUT_JSON="$ROOT/ecosystem/docs/analysis/probe-before-promote-last.json"
PROBE_OUT="/ecosystem/docs/analysis/probe-before-promote-last.json"
export PROBE_OUT
set +e
./bin/compose exec -T -e PROBE_OUT="$PROBE_OUT" -e PROBE_STRICT=1 \
  winston_unit_test bin/rails runner /ecosystem/docs/analysis/probe_before_promote.rb "${IDS[@]}"
probe_ec=$?
set -e

echo "probe_exit=$probe_ec"

# Jev System One — three desk smells (noul yes/no on structured state)
if command -v jev >/dev/null 2>&1 && [[ -n "${TYPESAFE_API_KEY:-}" ]] && [[ -f "$OUT_JSON" ]]; then
  echo "=== Jev System One state questions ==="
  # Build a concatenated state from each row's jev_state
  STATE_FILE=$(mktemp)
  python3 - <<PY
import json
from pathlib import Path
rep = json.loads(Path("$OUT_JSON").read_text())
# One state blob listing each PBR facts for Jev
lines = ["Probe-before-promote facts for Winston Portfolio Backtest Runs:"]
for row in rep.get("rows", []):
    if not row.get("found"):
        lines.append(f"PBR {row.get('pbr_id')}: NOT FOUND")
        continue
    s = row.get("jev_state") or {}
    lines.append(
        f"PBR {s.get('pbr_id')}: heat_mode={s.get('heat_mode')!r}, heat_present={s.get('heat_present')}, "
        f"heat_enabled={s.get('heat_enabled')}, peak_open={s.get('peak_open')}, "
        f"max_positions_per_portfolio={s.get('max_positions_per_portfolio')}, "
        f"open_gt_cap_events={s.get('open_gt_cap_events')}, leap_fulfillment={s.get('leap_fulfillment')!r}, "
        f"prefers_option_packaging={s.get('prefers_option_packaging')}, share_units={s.get('share_units')}, "
        f"contracts_floor={s.get('contracts_floor')}, zero_contracts_smell={s.get('zero_contracts_smell')}, "
        f"stock_only_despite_leap_pref={s.get('stock_only_despite_leap_pref')}."
    )
Path("$STATE_FILE").write_text("\\n".join(lines))
print(Path("$STATE_FILE").read_text()[:1500])
PY
  set +e
  jev ask @"$STATE_FILE" -q \
    --noul heat_label_lie="For any listed PBR: is heat_mode turtle (or cell intends turtle) while heat hash is missing or heat_enabled is false?" \
    --noul cap_breach="For any listed PBR: did peak_open exceed max_positions_per_portfolio (or open_gt_cap_events > 0)?" \
    --noul zero_contracts="For any listed PBR: does packaging prefer LEAP/call while contracts_floor is 0, or stock_only_despite_leap_pref true?" \
    --json > "${OUT_JSON%.json}-jev.json" 2>"${OUT_JSON%.json}-jev.err"
  jev_ec=$?
  set -e
  echo "jev_ask_exit=$jev_ec"
  if [[ -s "${OUT_JSON%.json}-jev.json" ]]; then
    python3 - <<'PY'
import json
from pathlib import Path
p = Path("/home/johnkoisch/Documents/com/sawtooth/ecosystem/docs/analysis/probe-before-promote-last-jev.json")
try:
    d = json.loads(p.read_text())
except Exception as e:
    print("jev json parse error", e)
    raise SystemExit(0)
# Print compact answers
answers = d.get("answers") or d.get("questions") or d
print(json.dumps(answers, indent=2)[:2000])
PY
  else
    echo "jev ask produced no json; stderr:"
    head -20 "${OUT_JSON%.json}-jev.err" || true
  fi
  rm -f "$STATE_FILE"
else
  echo "Jev skipped (no jev binary or TYPESAFE_API_KEY)"
fi

exit "$probe_ec"
