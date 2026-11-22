"""Asynchronous, delay-tolerant synchronisation.

Only lightweight JSON (students, answered-question events, BKT state) is sent -
never media. Failures are normal on a flaky network: nothing is lost because
rows stay flagged `synced=0` until the server confirms receipt, and the server
de-duplicates events by UUID, so retrying is always safe.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass

from .db import Database


@dataclass
class SyncResult:
    ok: bool
    sent: int = 0
    error: str | None = None


class SyncClient:
    """`post` is injectable (defaults to `requests.post`) so tests need no network."""

    def __init__(self, db: Database, base_url: str, api_key: str | None = None,
                 post=None, timeout: float = 8.0):
        self.db, self.base_url, self.api_key, self.timeout = db, base_url.rstrip("/"), api_key, timeout
        if post is None:
            import requests  # imported lazily: keeps the module importable without it
            post = requests.post
        self._post = post

    def sync_once(self) -> SyncResult:
        batch = self.db.unsynced_batch()
        n = len(batch["students"]) + len(batch["events"]) + len(batch["mastery"])
        if n == 0:
            return SyncResult(True, 0)
        headers = {"X-API-Key": self.api_key} if self.api_key else {}
        try:
            resp = self._post(f"{self.base_url}/v1/sync", json={"device_id": self.db.device_id(), **batch},
                              headers=headers, timeout=self.timeout)
        except Exception as exc:  # no connectivity, DNS, timeout, ...
            return SyncResult(False, 0, f"{type(exc).__name__}: {exc}")
        if resp.status_code != 200:
            return SyncResult(False, 0, f"HTTP {resp.status_code}")
        self.db.mark_synced(batch)
        return SyncResult(True, n)

    def sync_all(self, max_rounds: int = 20) -> SyncResult:
        """Drain the queue in batches; stops at the first failure."""
        total = 0
        for _ in range(max_rounds):
            r = self.sync_once()
            if not r.ok:
                return SyncResult(False, total, r.error)
            if r.sent == 0:
                break
            total += r.sent
        return SyncResult(True, total)


class SyncWorker(threading.Thread):
    """Background thread: try to sync every `interval` seconds, back off on failure."""

    def __init__(self, client: SyncClient, interval: float = 60.0, on_result=None):
        super().__init__(daemon=True)
        self.client, self.interval, self.on_result = client, interval, on_result
        self._stop_evt, self._wake = threading.Event(), threading.Event()

    def trigger(self) -> None:
        self._wake.set()

    def stop(self) -> None:
        self._stop_evt.set()
        self._wake.set()

    def run(self) -> None:
        wait = self.interval
        while not self._stop_evt.is_set():
            self._wake.wait(timeout=wait)
            self._wake.clear()
            if self._stop_evt.is_set():
                break
            result = self.client.sync_all()
            # normal cadence after success; exponential back-off (max 15 min) after a failure
            wait = self.interval if result.ok else min(wait * 2, 15 * 60)
            if self.on_result:
                try:
                    self.on_result(result)
                except Exception:
                    pass
