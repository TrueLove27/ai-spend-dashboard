from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from app.db.models import Category, DailyCost, FxRate, SyncLog, Workspace


class CostRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[DailyCost]:
        return self.db.query(DailyCost).order_by(DailyCost.cost_date).all()

    def filter_by_date(self, date_from: date | None, date_to: date | None) -> list[DailyCost]:
        query = self.db.query(DailyCost)
        if date_from:
            query = query.filter(DailyCost.cost_date >= date_from)
        if date_to:
            query = query.filter(DailyCost.cost_date <= date_to)
        return query.order_by(DailyCost.cost_date).all()

    def get_latest(self) -> DailyCost | None:
        return self.db.query(DailyCost).order_by(DailyCost.cost_date.desc()).first()

    def count(self) -> int:
        return self.db.query(DailyCost).count()


class WorkspaceRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Workspace]:
        return self.db.query(Workspace).order_by(Workspace.total_cost_usd.desc()).all()


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Category]:
        return self.db.query(Category).order_by(Category.percentage.desc()).all()


class SyncLogRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[SyncLog]:
        return self.db.query(SyncLog).order_by(SyncLog.ran_at.desc()).all()

    def append(self, entry: SyncLog) -> SyncLog:
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry


class FxRateRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def upsert_rates(self, rates: dict[str, float], source: str) -> list[FxRate]:
        now = datetime.now(timezone.utc)
        saved: list[FxRate] = []
        for quote, rate in rates.items():
            row = FxRate(
                base_currency="USD",
                quote_currency=quote,
                rate=rate,
                source=source,
                fetched_at=now,
            )
            self.db.add(row)
            saved.append(row)
        self.db.commit()
        return saved

    def latest_rates(self) -> dict[str, float]:
        rows = self.db.query(FxRate).order_by(FxRate.fetched_at.desc()).limit(10).all()
        out: dict[str, float] = {"USD": 1.0}
        for row in rows:
            out.setdefault(row.quote_currency, row.rate)
        return out
