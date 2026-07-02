# Heartbeat Tasks

<!--
Authoritative schedule: ecosystem/ai/schedule/ (manifest.yaml + cromwell-cron.json).
Gateway heartbeat is DISABLED — Cromwell cron drives periodic Telegram posts.
This file is a pointer only; do not add Active Tasks that duplicate cron jobs.
-->

See [`ecosystem/ai/schedule/README.md`](../../schedule/README.md) for the full M-F timeline.

**NYSE session snapshots:** 7:30 AM–2:00 PM Mountain Time (9:30 AM–4:00 PM Eastern), via Cromwell cron.

**EOD delivery:** 4:35 PM MT — fetch_only report (Wv2 Sidekiq builds at 4:30 PM MT).