from __future__ import annotations

from datetime import datetime, timezone

import httpx

from app.core.config import settings


class FrankfurterClient:
    """Live FX rates from https://api.frankfurter.app (free, no API key)."""

    def __init__(self) -> None:
        self.base_url = settings.frankfurter_base_url.rstrip("/")

    async def fetch_usd_rates(self, quotes: list[str]) -> dict[str, float]:
        symbols = ",".join(quotes)
        url = f"{self.base_url}/latest?from=USD&to={symbols}"
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            payload = response.json()
        rates = {k.upper(): float(v) for k, v in payload.get("rates", {}).items()}
        rates["USD"] = 1.0
        return rates

    @property
    def endpoint_label(self) -> str:
        return f"{self.base_url}/latest"


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
