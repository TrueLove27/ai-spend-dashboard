"""JSON-backed persistence layer (portfolio demo)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.core.config import settings


class JsonStore:
    def __init__(self, filename: str) -> None:
        self.path = Path(settings.data_dir) / filename
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def read(self) -> Any:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def write(self, data: Any) -> None:
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")
