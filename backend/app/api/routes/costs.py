from datetime import date

from fastapi import APIRouter, Query

from app.models.schemas import (
    AgentCostRow,
    CategoryBreakdown,
    DailyCostRow,
    PlatformTrendPoint,
    SummaryMetrics,
    SyncLogEntry,
)
from app.services.analytics_service import analytics_service
from app.services.cost_service import cost_service

router = APIRouter(prefix="/costs", tags=["costs"])


@router.get("/summary", response_model=SummaryMetrics)
def summary():
    return cost_service.get_summary()


@router.get("/daily", response_model=list[DailyCostRow])
def daily(
    date_from: date | None = Query(None, alias="from"),
    date_to: date | None = Query(None, alias="to"),
):
    return cost_service.get_daily_costs(date_from, date_to)


@router.get("/categories", response_model=list[CategoryBreakdown])
def categories():
    return cost_service.get_categories()


@router.get("/agents", response_model=list[AgentCostRow])
def agents():
    return cost_service.get_agents()


@router.get("/platforms/{platform}/trends", response_model=list[PlatformTrendPoint])
def platform_trends(platform: str):
    return cost_service.get_platform_trends(platform)


@router.get("/sync-logs", response_model=list[SyncLogEntry])
def sync_logs():
    return cost_service.get_sync_logs()


@router.post("/sync/{source}", response_model=SyncLogEntry)
def trigger_sync(source: str):
    return cost_service.trigger_sync(source)
