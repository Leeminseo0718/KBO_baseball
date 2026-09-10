from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kbo_data.sources.naver import NaverSnapshot


@dataclass(frozen=True)
class SnapshotEnvelope:
    source: str
    entity_type: str
    source_key: str
    fetched_at: str
    source_url: str
    sha256: str
    payload: dict[str, Any]


def make_envelope(snapshot: NaverSnapshot) -> SnapshotEnvelope:
    raw = json.dumps(snapshot.payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return SnapshotEnvelope(
        source="naver_sports",
        entity_type=snapshot.entity_type,
        source_key=snapshot.source_key,
        fetched_at=datetime.now(timezone.utc).isoformat(),
        source_url=snapshot.url,
        sha256=hashlib.sha256(raw).hexdigest(),
        payload=snapshot.payload,
    )


def write_envelope(envelope: SnapshotEnvelope, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_key = envelope.source_key.replace(":", "-")
    path = output_dir / f"{envelope.entity_type}-{safe_key}-{envelope.sha256[:12]}.json"
    path.write_text(json.dumps(asdict(envelope), ensure_ascii=False, indent=2), encoding="utf-8")
    return path

