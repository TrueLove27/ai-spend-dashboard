from __future__ import annotations

from dataclasses import dataclass

import stripe

from app.core.config import settings


@dataclass
class StripeSyncResult:
    enabled: bool
    charge_count: int
    total_usd: float
    message: str


class StripeBillingClient:
    """Optional live billing pull from Stripe test/live account."""

    def __init__(self) -> None:
        self.enabled = settings.stripe_enabled
        if self.enabled:
            stripe.api_key = settings.stripe_secret_key

    def fetch_recent_charges(self, limit: int = 100) -> StripeSyncResult:
        if not self.enabled:
            return StripeSyncResult(
                enabled=False,
                charge_count=0,
                total_usd=0.0,
                message="Stripe not configured. Set STRIPE_SECRET_KEY in backend/.env to enable.",
            )

        charges = stripe.Charge.list(limit=limit)
        data = charges.get("data", [])
        total_cents = sum(int(c.get("amount") or 0) for c in data if c.get("paid"))
        total_usd = round(total_cents / 100, 2)
        return StripeSyncResult(
            enabled=True,
            charge_count=len(data),
            total_usd=total_usd,
            message=f"Stripe API: fetched {len(data)} charges totaling ${total_usd:,.2f} USD.",
        )

    @property
    def endpoint_label(self) -> str:
        return "https://api.stripe.com/v1/charges"
