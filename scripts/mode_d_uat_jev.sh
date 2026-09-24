#!/usr/bin/env bash
# System One read of a Mode D desk UAT state file.
# The Ruby walk (Operations::ModeD::TestDesk) writes the facts. This script
# does not send orders. Pass rule: each noul >= 0.85 (yes).
#
# Usage: ecosystem/scripts/mode_d_uat_jev.sh /path/to/state.txt
set -euo pipefail

STATE="${1:-}"
if [[ -z "$STATE" || ! -f "$STATE" ]]; then
  echo "usage: $0 STATE_FILE" >&2
  exit 2
fi

export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
# shellcheck disable=SC1091
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
if [[ -z "${TYPESAFE_API_KEY:-}" && -f "$HOME/.config/jev/typesafe_api_key" ]]; then
  TYPESAFE_API_KEY="$(cat "$HOME/.config/jev/typesafe_api_key")"
  export TYPESAFE_API_KEY
fi

if ! command -v jev >/dev/null 2>&1 || [[ -z "${TYPESAFE_API_KEY:-}" ]]; then
  echo "Jev skipped (no jev binary or TYPESAFE_API_KEY)" >&2
  exit 3
fi

OUT="${STATE%.txt}-jev.json"
set +e
jev ask @"$STATE" --json \
  --noul call_on_opt_in_only="Is every covered call in this walk attached to a long stock lot whose slate choice was opt_in, with no covered call on a short lot or on a long whose slate choice stayed opt_out?" \
  --noul not_on_entry="Was the covered call its own slate line after the long shares already existed, rather than part of the entry line?" \
  --noul paired_unwind="On the long exit, was the covered call bought to close before the stock lots were marked flat, and was no short call left open?" \
  --noul three_lots_each="Did the long side reach 3 stock lots before its exit, and did the short side reach 3 stock lots before its exit?" \
  --noul short_has_no_call="Did every short slate line offer no covered-call choice, and did the short book record no covered-call journal?" \
  >"$OUT" 2>"${OUT}.err"
jev_ec=$?
set -e
echo "jev_ask_exit=$jev_ec"
if [[ ! -s "$OUT" ]]; then
  echo "jev ask produced no json" >&2
  cat "${OUT}.err" >&2 || true
  exit 1
fi

python3 - "$OUT" <<'PY'
import json, sys
doc = json.loads(open(sys.argv[1]).read())
answers = doc.get("answers") or doc.get("nouls") or doc
if isinstance(answers, dict) and "answers" in answers:
    answers = answers["answers"]
print(json.dumps(answers, indent=2)[:4000])
# Accept either a list of {id, noul} or a dict of id -> noul / {noul:}.
rows = []
if isinstance(answers, list):
    rows = answers
elif isinstance(answers, dict):
    for key, value in answers.items():
        if isinstance(value, dict):
            rows.append({"id": key, **value})
        else:
            rows.append({"id": key, "noul": value})
failed = []
for row in rows:
    noul = row.get("noul", row.get("probability", row.get("yes")))
    if noul is None:
        continue
    if float(noul) < 0.85:
        failed.append((row.get("id") or row.get("question_id"), noul))
if failed:
    print("FAIL", failed)
    raise SystemExit(1)
print("PASS nouls>=")
PY
