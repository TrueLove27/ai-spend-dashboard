from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.db.seed import seed_if_empty
from app.db.session import SessionLocal, init_db
from app.services.sync_service import SyncService


def _scheduled_sync():
    db = SessionLocal()
    try:
        import asyncio
        asyncio.run(SyncService(db).run_full_sync("Scheduled Job — All Integrations"))
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()

    scheduler = None
    if settings.scheduler_enabled:
        scheduler = BackgroundScheduler()
        scheduler.add_job(_scheduled_sync, "interval", hours=24, id="daily_sync")
        scheduler.start()
    yield
    if scheduler:
        scheduler.shutdown(wait=False)


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="3.0.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix=settings.api_prefix)
    return app


app = create_app()
