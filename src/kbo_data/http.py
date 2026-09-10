from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any


class HttpClient:
    def __init__(self, interval_seconds: float = 1.2, timeout_seconds: int = 20) -> None:
        self.interval_seconds = interval_seconds
        self.timeout_seconds = timeout_seconds
        self._last_request_at = 0.0

    def _wait(self) -> None:
        remaining = self.interval_seconds - (time.monotonic() - self._last_request_at)
        if remaining > 0:
            time.sleep(remaining)

    def get_bytes(self, url: str, *, accept: str = "application/json,text/html") -> bytes:
        self._wait()
        request = urllib.request.Request(
            url,
            headers={
                "Accept": accept,
                "User-Agent": "KBODataRoom/0.1 (personal research; rate-limited)",
            },
        )
        error: Exception | None = None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    self._last_request_at = time.monotonic()
                    return response.read()
            except (urllib.error.URLError, TimeoutError) as exc:
                error = exc
                time.sleep(2 ** attempt)
        raise RuntimeError(f"GET failed after retries: {url}") from error

    def get_json(self, url: str) -> dict[str, Any]:
        payload = json.loads(self.get_bytes(url).decode("utf-8"))
        if not payload.get("success", False):
            raise RuntimeError(f"Source returned an error: {payload}")
        return payload

