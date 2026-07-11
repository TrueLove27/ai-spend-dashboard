from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.schemas import (
    CategoryBreakdown,
    DailyCostRow,
    PlatformTrendPoint,
    SummaryMetrics,
    SyncLogEntry,
    WorkspaceCostRow,
)
from app.services.cost_service import get_cost_service

router = APIRouter(prefix="/costs", tags=["costs"])


@router.get("/summary", response_model=SummaryMetrics)
def summary(db: Session = Depends(get_db)):
    return get_cost_service(db).get_summary()


@router.get("/daily", response_model=list[DailyCostRow])
def daily(
    date_from: date | None = Query(None, alias="from"),
    date_to: date | None = Query(None, alias="to"),
    db: Session = Depends(get_db),
):
    return get_cost_service(db).get_daily_costs(date_from, date_to)


@router.get("/categories", response_model=list[CategoryBreakdown])
def categories(db: Session = Depends(get_db)):
    return get_cost_service(db).get_categories()


@router.get("/workspaces", response_model=list[WorkspaceCostRow])
def workspaces(db: Session = Depends(get_db)):
    return get_cost_service(db).get_workspaces()


@router.get("/platforms/{platform}/trends", response_model=list[PlatformTrendPoint])
def platform_trends(platform: str, db: Session = Depends(get_db)):
    return get_cost_service(db).get_platform_trends(platform)


@router.get("/sync-logs", response_model=list[SyncLogEntry])
def sync_logs(db: Session = Depends(get_db)):
    return get_cost_service(db).get_sync_logs()


@router.post("/sync/{source}", response_model=SyncLogEntry)
async def trigger_sync(source: str, db: Session = Depends(get_db)):
    return await get_cost_service(db).trigger_sync(source)
