from fastapi import APIRouter

from app.api.routes import analytics, costs, export, health, integrations

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(costs.router)
api_router.include_router(analytics.router)
api_router.include_router(export.router)
api_router.include_router(integrations.router)
