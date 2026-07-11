from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.schemas import IntegrationStatus, IntegrationsResponse
from app.repositories.cost_repository import FxRateRepository, SyncLogRepository

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.get("/status", response_model=IntegrationsResponse)
def integration_status(db: Session = Depends(get_db)):
    fx_repo = FxRateRepository(db)
    logs = SyncLogRepository(db).get_all()
    last_sync = logs[0].message if logs else None

    integrations = [
        IntegrationStatus(
            name="Frankfurter FX",
            enabled=True,
            description="Live USD exchange rates from api.frankfurter.app (no API key required).",
            requires_key=False,
            last_status=last_sync,
        ),
        IntegrationStatus(
            name="Provider Status Pages",
            enabled=True,
            description="HTTP health checks against public AWS/GCP/Azure/Vercel/Datadog status pages.",
            requires_key=False,
            last_status=last_sync,
        ),
        IntegrationStatus(
            name="Stripe Billing",
            enabled=settings.stripe_enabled,
            description="Pulls recent charges from your Stripe account when STRIPE_SECRET_KEY is set.",
            requires_key=True,
            last_status="Configured" if settings.stripe_enabled else "Not configured — add STRIPE_SECRET_KEY to .env",
        ),
        IntegrationStatus(
            name="SQLite Database",
            enabled=True,
            description=f"Persistent storage at {settings.database_url}",
            requires_key=False,
            last_status="Connected",
        ),
    ]
    return IntegrationsResponse(integrations=integrations, fx_rates=fx_repo.latest_rates())
