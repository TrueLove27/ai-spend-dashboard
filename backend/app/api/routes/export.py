from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.services.export_service import export_service

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/daily.csv", response_class=PlainTextResponse)
def export_daily_csv():
    return PlainTextResponse(export_service.daily_costs_csv(), media_type="text/csv")
