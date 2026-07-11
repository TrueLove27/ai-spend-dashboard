from __future__ import annotations

from datetime import date

from app.models.schemas import DailyCostRow
from app.services.cost_service import cost_service


class AnalyticsService:
    def compare_periods(self, date_from: date, date_to: date) -> dict:
        rows = cost_service.get_daily_costs(date_from, date_to)
        if not rows:
            return {"period_spend_inr": 0, "avg_daily_inr": 0, "days": 0, "total_calls": 0}
        total = sum(r.total_inr for r in rows)
        return {
            "period_spend_inr": round(total, 2),
            "avg_daily_inr": round(total / len(rows), 2),
            "days": len(rows),
            "total_calls": sum(r.calls for r in rows),
        }

    def platform_breakdown(self, rows: list[DailyCostRow] | None = None) -> list[dict]:
        rows = rows or cost_service.get_daily_costs()
        totals = {p: 0.0 for p in cost_service.PLATFORMS}
        for r in rows:
            for p in cost_service.PLATFORMS:
                totals[p] += getattr(r, p)
        grand = sum(totals.values()) or 1
        return [
            {"platform": p, "amount_usd": round(v, 2), "share_pct": round(v / grand * 100, 1)}
            for p, v in sorted(totals.items(), key=lambda x: -x[1])
        ]

    def weekly_rollup(self) -> list[dict]:
        rows = cost_service.get_daily_costs()
        weeks: dict[str, dict] = {}
        for r in rows:
            week = r.date.isocalendar()
            key = f"{week.year}-W{week.week:02d}"
            if key not in weeks:
                weeks[key] = {"week": key, "spend_inr": 0, "calls": 0}
            weeks[key]["spend_inr"] += r.total_inr
            weeks[key]["calls"] += r.calls
        return list(weeks.values())


analytics_service = AnalyticsService()
