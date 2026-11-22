"""Optional talk to `bescientific_backend` (health + curriculum). Failures are silent."""
from __future__ import annotations

from typing import Any


def platform_health(base_url: str, get=None, timeout: float = 3.0) -> bool:
    try:
        if get is None:
            import requests
            get = requests.get
        r = get(f"{base_url.rstrip('/')}/health", timeout=timeout)
        return r.status_code == 200 and (r.json() or {}).get("status") == "ok"
    except Exception:
        return False


def fetch_curriculum(base_url: str, get=None, api_key: str | None = None,
                     timeout: float = 3.0) -> dict[str, Any] | None:
    try:
        if get is None:
            import requests
            get = requests.get
        headers = {"X-API-Key": api_key} if api_key else {}
        r = get(f"{base_url.rstrip('/')}/curriculum", headers=headers, timeout=timeout)
        if r.status_code == 200:
            data = r.json()
            return data if isinstance(data, dict) else None
    except Exception:
        pass
    return None
