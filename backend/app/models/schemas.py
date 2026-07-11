from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    database: str


class DailyCostRow(BaseModel):
    date: date
    aws: float
    gcp: float
    azure: float
    vercel: float
    datadog: float
    requests: int
    billable_requests: int
    total_usd: float = 0
    total_display: float = 0
    cost_per_request_usd: float = 0


class CategoryBreakdown(BaseModel):
    name: str
    amount_usd: float
    percentage: float
    trend_pct: float = 0


class PlatformTrendPoint(BaseModel):
    date: date
    amount_usd: float
    amount_display: float


class WorkspaceCostRow(BaseModel):
    workspace_id: str
    workspace_name: str
    primary_provider: str
    requests: int
    total_cost_usd: float
    avg_latency_ms: float
    utilization_rate: float


class SummaryMetrics(BaseModel):
    currency_display: str = "EUR"
    total_spend_usd: float
    total_spend_display: float
    total_requests: int
    billable_requests: int
    avg_cost_per_request_usd: float
    avg_cost_per_billable_usd: float
    days_tracked: int
    fx_rate_usd_display: float
    as_of: datetime


class SyncLogEntry(BaseModel):
    id: str
    source: str
    status: str
    records_synced: int
    message: str
    api_endpoint: str | None = None
    ran_at: datetime


class IntegrationStatus(BaseModel):
    name: str
    enabled: bool
    description: str
    requires_key: bool = False
    last_status: str | None = None


class IntegrationsResponse(BaseModel):
    integrations: list[IntegrationStatus]
    fx_rates: dict[str, float] = Field(default_factory=dict)


class DateRangeFilter(BaseModel):
    date_from: date | None = None
    date_to: date | None = None
    platform: str | None = None
