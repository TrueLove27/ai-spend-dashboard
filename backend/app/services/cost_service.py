from __future__ import annotations

from datetime import date, datetime, timezone

from app.core.config import settings
from app.models.schemas import (
    AgentCostRow,
    CategoryBreakdown,
    DailyCostRow,
    PlatformTrendPoint,
    SummaryMetrics,
    SyncLogEntry,
)
from app.repositories.cost_repository import (
    AgentRepository,
    CategoryRepository,
    CostRepository,
    SyncLogRepository,
)


class CostService:
    PLATFORMS = ("openai", "anthropic", "elevenlabs", "deepgram", "telephony")

    def __init__(self) -> None:
        self.costs = CostRepository()
        self.agents = AgentRepository()
        self.categories = CategoryRepository()
        self.sync_logs = SyncLogRepository()

    def _row_total_usd(self, row: dict) -> float:
        return sum(row[p] for p in self.PLATFORMS)

    def _enrich_row(self, row: dict) -> DailyCostRow:
        total_usd = self._row_total_usd(row)
        total_inr = round(total_usd * settings.usd_to_inr, 2)
        connected = row.get("connected_calls") or row["calls"]
        cpc = round(total_inr / connected, 4) if connected else 0
        return DailyCostRow(
            date=date.fromisoformat(row["date"]),
            openai=row["openai"],
            anthropic=row["anthropic"],
            elevenlabs=row["elevenlabs"],
            deepgram=row["deepgram"],
            telephony=row["telephony"],
            calls=row["calls"],
            connected_calls=connected,
            total_usd=round(total_usd, 2),
            total_inr=total_inr,
            cost_per_call_inr=cpc,
        )

    def get_daily_costs(self, date_from: date | None = None, date_to: date | None = None) -> list[DailyCostRow]:
        rows = self.costs.filter_by_date(date_from, date_to)
        return [self._enrich_row(r) for r in rows]

    def get_summary(self) -> SummaryMetrics:
        rows = self.get_daily_costs()
        total_usd = sum(r.total_usd for r in rows)
        total_inr = sum(r.total_inr for r in rows)
        total_calls = sum(r.calls for r in rows)
        connected = sum(r.connected_calls for r in rows)
        return SummaryMetrics(
            total_spend_inr=round(total_inr, 2),
            total_spend_usd=round(total_usd, 2),
            total_calls=total_calls,
            connected_calls=connected,
            avg_cost_per_call_inr=round(total_inr / total_calls, 4) if total_calls else 0,
            avg_cost_per_connected_inr=round(total_inr / connected, 4) if connected else 0,
            days_tracked=len(rows),
            usd_to_inr_rate=settings.usd_to_inr,
            as_of=datetime.now(timezone.utc),
        )

    def get_categories(self) -> list[CategoryBreakdown]:
        return [CategoryBreakdown(**c) for c in self.categories.get_all()]

    def get_agents(self) -> list[AgentCostRow]:
        return [AgentCostRow(**a) for a in self.agents.get_all()]

    def get_platform_trends(self, platform: str) -> list[PlatformTrendPoint]:
        if platform not in self.PLATFORMS:
            return []
        rows = self.get_daily_costs()
        return [
            PlatformTrendPoint(
                date=r.date,
                amount_usd=getattr(r, platform),
                amount_inr=round(getattr(r, platform) * settings.usd_to_inr, 2),
            )
            for r in rows
        ]

    def get_sync_logs(self) -> list[SyncLogEntry]:
        return [SyncLogEntry(**log) for log in self.sync_logs.get_all()]

    def trigger_sync(self, source: str) -> SyncLogEntry:
        entry = SyncLogEntry(
            id=f"sync-{int(datetime.now().timestamp())}",
            source=source,
            status="success",
            records_synced=len(self.costs.get_all()),
            message=f"Manual sync triggered for {source}",
            ran_at=datetime.now(timezone.utc),
        )
        self.sync_logs.append(entry.model_dump(mode="json"))
        return entry


cost_service = CostService()
