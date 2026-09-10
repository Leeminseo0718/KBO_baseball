from __future__ import annotations

import html
import re
from dataclasses import dataclass

from kbo_data.http import HttpClient


@dataclass(frozen=True)
class PlayerVerification:
    player_id: str
    expected_name: str
    official_name: str | None
    matched: bool
    source_url: str


class KboOfficialClient:
    NAME_PATTERN = re.compile(r'id="[^"]*playerProfile_lblName"[^>]*>([^<]+)<')

    def __init__(self, http: HttpClient, base_url: str = "https://www.koreabaseball.com") -> None:
        self.http = http
        self.base_url = base_url.rstrip("/")

    def verify_player(self, player_id: str, expected_name: str) -> PlayerVerification:
        paths = (
            "/Record/Player/PitcherDetail/Basic.aspx",
            "/Record/Player/HitterDetail/Basic.aspx",
        )
        official_name: str | None = None
        source_url = ""
        for path in paths:
            source_url = f"{self.base_url}{path}?playerId={player_id}"
            body = self.http.get_bytes(source_url, accept="text/html").decode("utf-8", errors="replace")
            match = self.NAME_PATTERN.search(body)
            if match:
                official_name = html.unescape(match.group(1)).strip()
                break
        return PlayerVerification(player_id, expected_name, official_name, official_name == expected_name, source_url)

