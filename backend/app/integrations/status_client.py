from __future__ import annotations

from datetime import datetime, timezone

import httpx

from app.core.config import settings


class StatusPageClient:
    """Fetches public provider status metadata (real HTTP, no API key)."""

    ENDPOINTS = {
        "aws": "https://status.aws.amazon.com/",
        "gcp": "https://status.cloud.google.com/",
        "azure": "https://azure.status.microsoft/",
        "vercel": "https://www.vercel-status.com/",
        "datadog": "https://status.datadoghq.com/",
    }

    async def check_provider(self, provider: str) -> dict:
        url = self.ENDPOINTS.get(provider)
        if not url:
            return {"provider": provider, "reachable": False, "status_code": None}

        async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
            response = await client.get(url)
            return {
                "provider": provider,
                "reachable": response.status_code < 500,
                "status_code": response.status_code,
                "checked_at": datetime.now(timezone.utc).isoformat(),
                "url": url,
            }

    async def check_all(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
            async def _check(provider: str, url: str) -> dict:
                try:
                    response = await client.get(url)
                    return {
                        "provider": provider,
                        "reachable": response.status_code < 500,
                        "status_code": response.status_code,
                        "checked_at": datetime.now(timezone.utc).isoformat(),
                        "url": url,
                    }
                except Exception:
                    return {"provider": provider, "reachable": False, "status_code": None, "url": url}

            import asyncio
            tasks = [_check(provider, url) for provider, url in self.ENDPOINTS.items()]
            return list(await asyncio.gather(*tasks))
