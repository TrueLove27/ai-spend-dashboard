from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return HealthResponse(
        status="ok",
        service="cloud-spend-dashboard",
        version="3.0.0",
        database=settings.database_url.split("://", 1)[0],
    )
