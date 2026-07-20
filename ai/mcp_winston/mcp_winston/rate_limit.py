"""In-memory rate limits for expensive MCP tools (task 8)."""

from __future__ import annotations

import os
import time
from collections import defaultdict, deque

EXPENSIVE_TOOLS: frozenset[str] = frozenset(
    t.strip()
    for t in os.getenv(
        "MCP_RATE_LIMIT_TOOLS",
        "wv2_perform_daily_analysis,wv2_get_daily_activity_report,wv2_sync_data,wut_run_daily_operations,dm_request_full_sync",
    ).split(",")
    if t.strip()
)

WINDOW_SEC = int(os.getenv("MCP_RATE_LIMIT_WINDOW_SEC", "120"))
MAX_CALLS = int(os.getenv("MCP_RATE_LIMIT_MAX", "4"))

_recent: dict[str, deque[float]] = defaultdict(deque)


def check_rate_limit(tool: str) -> tuple[bool, int]:
    """Return (limited, retry_after_seconds)."""
    if tool not in EXPENSIVE_TOOLS or MAX_CALLS <= 0:
        return False, 0
    now = time.time()
    window_start = now - WINDOW_SEC
    q = _recent[tool]
    while q and q[0] < window_start:
        q.popleft()
    if len(q) >= MAX_CALLS:
        retry = max(1, int(WINDOW_SEC - (now - q[0])))
        return True, retry
    q.append(now)
    return False, 0