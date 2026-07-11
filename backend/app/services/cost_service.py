from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import DailyCost
from app.models.schemas import (
    CategoryBreakdown,
    DailyCostRow,
    PlatformTrendPoint,
    SummaryMetrics,
    SyncLogEntry,
    WorkspaceCostRow,
)
from app.repositories.cost_repository import (
    CategoryRepository,
    CostRepository,
    FxRateRepository,
    SyncLogRepository,
    WorkspaceRepository,
)
from app.services.sync_service import SyncService


class CostService:
    PLATFORMS = ("aws", "gcp", "azure", "vercel", "datadog")

    def __init__(self, db: Session) -> None:
        self.db = db
        self.costs = CostRepository(db)
        self.workspaces = WorkspaceRepository(db)
        self.categories = CategoryRepository(db)
        self.sync_logs = SyncLogRepository(db)
        self.fx_rates = FxRateRepository(db)

    def _display_rate(self) -> float:
        rates = self.fx_rates.latest_rates()
        return rates.get(settings.display_currency, 1.0)

    def _row_total_usd(self, row: DailyCost) -> float:
        return sum(getattr(row, p) for p in self.PLATFORMS)

    def _enrich_row(self, row: DailyCost) -> DailyCostRow:
        total_usd = self._row_total_usd(row)
        rate = self._display_rate()
        total_display = round(total_usd * rate, 2)
        billable = row.billable_requests or row.requests
        cpr = round(total_usd / billable, 6) if billable else 0
        return DailyCostRow(
            date=row.cost_date,
            aws=row.aws,
            gcp=row.gcp,
            azure=row.azure,
            vercel=row.vercel,
            datadog=row.datadog,
            requests=row.requests,
            billable_requests=billable,
            total_usd=round(total_usd, 2),
            total_display=total_display,
            cost_per_request_usd=cpr,
        )

    def get_daily_costs(self, date_from: date | None = None, date_to: date | None = None) -> list[DailyCostRow]:
        rows = self.costs.filter_by_date(date_from, date_to)
        return [self._enrich_row(r) for r in rows]

    def get_summary(self) -> SummaryMetrics:
        rows = self.get_daily_costs()
        total_usd = sum(r.total_usd for r in rows)
        rate = self._display_rate()
        total_display = round(total_usd * rate, 2)
        total_requests = sum(r.requests for r in rows)
        billable = sum(r.billable_requests for r in rows)
        return SummaryMetrics(
            currency_display=settings.display_currency,
            total_spend_usd=round(total_usd, 2),
            total_spend_display=total_display,
            total_requests=total_requests,
            billable_requests=billable,
            avg_cost_per_request_usd=round(total_usd / total_requests, 6) if total_requests else 0,
            avg_cost_per_billable_usd=round(total_usd / billable, 6) if billable else 0,
            days_tracked=len(rows),
            fx_rate_usd_display=rate,
            as_of=datetime.now(timezone.utc),
        )

    def get_categories(self) -> list[CategoryBreakdown]:
        return [CategoryBreakdown.model_validate(c, from_attributes=True) for c in self.categories.get_all()]

    def get_workspaces(self) -> list[WorkspaceCostRow]:
        return [WorkspaceCostRow.model_validate(w, from_attributes=True) for w in self.workspaces.get_all()]

    def get_platform_trends(self, platform: str) -> list[PlatformTrendPoint]:
        if platform not in self.PLATFORMS:
            return []
        rate = self._display_rate()
        rows = self.get_daily_costs()
        return [
            PlatformTrendPoint(
                date=r.date,
                amount_usd=getattr(r, platform),
                amount_display=round(getattr(r, platform) * rate, 2),
            )
            for r in rows
        ]

    def get_sync_logs(self) -> list[SyncLogEntry]:
        return [SyncLogEntry.model_validate(log, from_attributes=True) for log in self.sync_logs.get_all()]

    async def trigger_sync(self, source: str) -> SyncLogEntry:
        entry = await SyncService(self.db).run_full_sync(source)
        return SyncLogEntry(
            id=entry.id,
            source=entry.source,
            status=entry.status,
            records_synced=entry.records_synced,
            message=entry.message,
            api_endpoint=entry.api_endpoint,
            ran_at=entry.ran_at,
        )


def get_cost_service(db: Session) -> CostService:
    return CostService(db)
