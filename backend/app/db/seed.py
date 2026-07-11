from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from app.db.models import Category, DailyCost, SyncLog, Workspace

DAILY_COSTS = [
    {"cost_date": date(2026, 7, 1), "aws": 142.5, "gcp": 88.2, "azure": 61.0, "vercel": 24.4, "datadog": 38.5, "requests": 189000, "billable_requests": 151200},
    {"cost_date": date(2026, 7, 2), "aws": 138.1, "gcp": 92.7, "azure": 58.5, "vercel": 22.9, "datadog": 37.8, "requests": 176400, "billable_requests": 140800},
    {"cost_date": date(2026, 7, 3), "aws": 151.3, "gcp": 79.8, "azure": 65.2, "vercel": 26.1, "datadog": 41.2, "requests": 194500, "billable_requests": 158100},
    {"cost_date": date(2026, 7, 4), "aws": 145.0, "gcp": 84.1, "azure": 59.8, "vercel": 25.0, "datadog": 39.1, "requests": 182200, "billable_requests": 144000},
    {"cost_date": date(2026, 7, 5), "aws": 123.6, "gcp": 75.4, "azure": 52.1, "vercel": 19.8, "datadog": 34.5, "requests": 158700, "billable_requests": 122400},
    {"cost_date": date(2026, 7, 6), "aws": 119.2, "gcp": 72.9, "azure": 49.5, "vercel": 18.5, "datadog": 32.9, "requests": 149200, "billable_requests": 118800},
    {"cost_date": date(2026, 7, 7), "aws": 147.8, "gcp": 91.3, "azure": 63.4, "vercel": 24.7, "datadog": 40.8, "requests": 191800, "billable_requests": 155500},
    {"cost_date": date(2026, 7, 8), "aws": 152.1, "gcp": 96.0, "azure": 66.9, "vercel": 27.2, "datadog": 43.1, "requests": 198600, "billable_requests": 162000},
    {"cost_date": date(2026, 7, 9), "aws": 144.4, "gcp": 90.5, "azure": 60.1, "vercel": 23.0, "datadog": 38.0, "requests": 185500, "billable_requests": 147200},
    {"cost_date": date(2026, 7, 10), "aws": 149.6, "gcp": 93.8, "azure": 64.0, "vercel": 25.8, "datadog": 41.5, "requests": 192400, "billable_requests": 156000},
    {"cost_date": date(2026, 7, 11), "aws": 141.2, "gcp": 87.6, "azure": 57.3, "vercel": 22.1, "datadog": 37.2, "requests": 180800, "billable_requests": 143600},
]

WORKSPACES = [
    {"workspace_id": "ws-001", "workspace_name": "Core API", "primary_provider": "AWS", "requests": 4200000, "total_cost_usd": 4820, "avg_latency_ms": 85, "utilization_rate": 0.78},
    {"workspace_id": "ws-002", "workspace_name": "Analytics Pipeline", "primary_provider": "GCP", "requests": 2100000, "total_cost_usd": 3150, "avg_latency_ms": 142, "utilization_rate": 0.62},
    {"workspace_id": "ws-003", "workspace_name": "Marketing Site", "primary_provider": "Vercel", "requests": 890000, "total_cost_usd": 1280, "avg_latency_ms": 48, "utilization_rate": 0.91},
    {"workspace_id": "ws-004", "workspace_name": "Legacy Monolith", "primary_provider": "Azure", "requests": 640000, "total_cost_usd": 1890, "avg_latency_ms": 210, "utilization_rate": 0.45},
    {"workspace_id": "ws-005", "workspace_name": "Observability Stack", "primary_provider": "Datadog", "requests": 1560000, "total_cost_usd": 960, "avg_latency_ms": 12, "utilization_rate": 0.88},
]

CATEGORIES = [
    {"name": "Compute", "amount_usd": 8420, "percentage": 38.2, "trend_pct": 4.1},
    {"name": "Storage", "amount_usd": 4210, "percentage": 19.1, "trend_pct": -1.2},
    {"name": "CDN / Edge", "amount_usd": 2180, "percentage": 9.9, "trend_pct": 6.8},
    {"name": "Observability", "amount_usd": 3560, "percentage": 16.1, "trend_pct": 2.4},
    {"name": "Networking", "amount_usd": 3740, "percentage": 16.7, "trend_pct": 0.9},
]


def seed_if_empty(db: Session) -> None:
    if db.query(DailyCost).count() > 0:
        return

    db.add_all(DailyCost(**row) for row in DAILY_COSTS)
    db.add_all(Workspace(**row) for row in WORKSPACES)
    db.add_all(Category(**row) for row in CATEGORIES)
    db.add(
        SyncLog(
            id="sync-bootstrap",
            source="database-seed",
            status="success",
            records_synced=len(DAILY_COSTS),
            message="Initial dataset loaded into SQLite from application seed.",
            api_endpoint=None,
            ran_at=datetime.now(timezone.utc),
        )
    )
    db.commit()
