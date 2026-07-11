from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from app.models.schemas import DailyCostRow
from app.services.cost_service import CostService


class AnalyticsService:
    def __init__(self, db: Session) -> None:
        self.cost_service = CostService(db)

    def compare_periods(self, date_from: date, date_to: date) -> dict:
        rows = self.cost_service.get_daily_costs(date_from, date_to)
        if not rows:
            return {"period_spend_usd": 0, "avg_daily_usd": 0, "days": 0, "total_requests": 0}
        total = sum(r.total_usd for r in rows)
        return {
            "period_spend_usd": round(total, 2),
            "avg_daily_usd": round(total / len(rows), 2),
            "days": len(rows),
            "total_requests": sum(r.requests for r in rows),
        }

    def platform_breakdown(self, rows: list[DailyCostRow] | None = None) -> list[dict]:
        rows = rows or self.cost_service.get_daily_costs()
        totals = {p: 0.0 for p in self.cost_service.PLATFORMS}
        for r in rows:
            for p in self.cost_service.PLATFORMS:
                totals[p] += getattr(r, p)
        grand = sum(totals.values()) or 1
        return [
            {"platform": p.upper(), "amount_usd": round(v, 2), "share_pct": round(v / grand * 100, 1)}
            for p, v in sorted(totals.items(), key=lambda x: -x[1])
        ]

    def weekly_rollup(self) -> list[dict]:
        rows = self.cost_service.get_daily_costs()
        weeks: dict[str, dict] = {}
        for r in rows:
            week = r.date.isocalendar()
            key = f"{week.year}-W{week.week:02d}"
            if key not in weeks:
                weeks[key] = {"week": key, "spend_usd": 0, "requests": 0}
            weeks[key]["spend_usd"] += r.total_usd
            weeks[key]["requests"] += r.requests
        return list(weeks.values())


def get_analytics_service(db: Session) -> AnalyticsService:
    return AnalyticsService(db)
