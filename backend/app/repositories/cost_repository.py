from __future__ import annotations

from datetime import date

from app.core.database import JsonStore


class CostRepository:
    def __init__(self) -> None:
        self._store = JsonStore("daily_costs.json")

    def get_all(self) -> list[dict]:
        return self._store.read()

    def filter_by_date(self, date_from: date | None, date_to: date | None) -> list[dict]:
        rows = self.get_all()
        out = []
        for r in rows:
            d = date.fromisoformat(r["date"])
            if date_from and d < date_from:
                continue
            if date_to and d > date_to:
                continue
            out.append(r)
        return out


class AgentRepository:
    def __init__(self) -> None:
        self._store = JsonStore("agents.json")

    def get_all(self) -> list[dict]:
        return self._store.read()


class CategoryRepository:
    def __init__(self) -> None:
        self._store = JsonStore("categories.json")

    def get_all(self) -> list[dict]:
        return self._store.read()


class SyncLogRepository:
    def __init__(self) -> None:
        self._store = JsonStore("sync_logs.json")

    def get_all(self) -> list[dict]:
        return self._store.read()

    def append(self, entry: dict) -> dict:
        logs = self.get_all()
        logs.insert(0, entry)
        self._store.write(logs)
        return entry
