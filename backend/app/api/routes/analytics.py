from fastapi import APIRouter

from app.services.analytics_service import analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/platform-breakdown")
def platform_breakdown():
    return analytics_service.platform_breakdown()


@router.get("/weekly-rollup")
def weekly_rollup():
    return analytics_service.weekly_rollup()
