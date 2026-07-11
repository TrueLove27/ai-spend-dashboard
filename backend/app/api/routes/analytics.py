from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.analytics_service import get_analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/platform-breakdown")
def platform_breakdown(db: Session = Depends(get_db)):
    return get_analytics_service(db).platform_breakdown()


@router.get("/weekly-rollup")
def weekly_rollup(db: Session = Depends(get_db)):
    return get_analytics_service(db).weekly_rollup()
