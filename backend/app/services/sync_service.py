from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.integrations.fx_client import FrankfurterClient
from app.integrations.status_client import StatusPageClient
from app.integrations.stripe_client import StripeBillingClient
from app.repositories.cost_repository import CostRepository, FxRateRepository, SyncLogRepository
from app.db.models import SyncLog


class SyncService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.costs = CostRepository(db)
        self.fx_rates = FxRateRepository(db)
        self.sync_logs = SyncLogRepository(db)
        self.fx_client = FrankfurterClient()
        self.stripe_client = StripeBillingClient()
        self.status_client = StatusPageClient()

    async def run_full_sync(self, source: str) -> SyncLog:
        messages: list[str] = []
        api_endpoints: list[str] = []
        records = 0
        status = "success"

        try:
            rates = await self.fx_client.fetch_usd_rates(["EUR", "GBP"])
            self.fx_rates.upsert_rates(rates, self.fx_client.endpoint_label)
            records += len(rates)
            eur = rates.get("EUR", 0)
            messages.append(f"Frankfurter FX: USD->EUR={eur:.4f}, USD->GBP={rates.get('GBP', 0):.4f}")
            api_endpoints.append(self.fx_client.endpoint_label)
        except Exception as exc:
            status = "partial"
            messages.append(f"Frankfurter FX failed: {exc}")

        try:
            stripe_result = self.stripe_client.fetch_recent_charges()
            messages.append(stripe_result.message)
            if stripe_result.enabled:
                api_endpoints.append(self.stripe_client.endpoint_label)
                records += stripe_result.charge_count
        except Exception as exc:
            status = "partial"
            messages.append(f"Stripe sync failed: {exc}")

        try:
            statuses = await self.status_client.check_all()
            reachable = sum(1 for s in statuses if s["reachable"])
            messages.append(f"Provider status pages: {reachable}/{len(statuses)} reachable.")
            records += reachable
            api_endpoints.extend(s["url"] for s in statuses if s.get("url"))
        except Exception as exc:
            status = "partial"
            messages.append(f"Status page checks failed: {exc}")

        records += self.costs.count()
        entry = SyncLog(
            id=f"sync-{int(datetime.now().timestamp())}",
            source=source,
            status=status,
            records_synced=records,
            message=" | ".join(messages),
            api_endpoint=", ".join(api_endpoints[:3]) + ("..." if len(api_endpoints) > 3 else ""),
            ran_at=datetime.now(timezone.utc),
        )
        return self.sync_logs.append(entry)
