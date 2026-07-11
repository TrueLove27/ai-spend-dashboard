from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.export_service import ExportService

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/daily.csv", response_class=PlainTextResponse)
def export_daily_csv(db: Session = Depends(get_db)):
    return PlainTextResponse(ExportService().daily_costs_csv(db), media_type="text/csv")
