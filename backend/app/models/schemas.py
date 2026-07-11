from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class DailyCostRow(BaseModel):
    date: date
    openai: float
    anthropic: float
    elevenlabs: float
    deepgram: float
    telephony: float
    calls: int
    connected_calls: int
    total_usd: float = 0
    total_inr: float = 0
    cost_per_call_inr: float = 0


class CategoryBreakdown(BaseModel):
    name: str
    amount_inr: float
    percentage: float
    trend_pct: float = 0


class PlatformTrendPoint(BaseModel):
    date: date
    amount_usd: float
    amount_inr: float


class AgentCostRow(BaseModel):
    agent_id: str
    agent_name: str
    platform: str
    calls: int
    total_cost_inr: float
    avg_duration_sec: float
    booking_rate: float


class SummaryMetrics(BaseModel):
    currency_display: str = "INR"
    total_spend_inr: float
    total_spend_usd: float
    total_calls: int
    connected_calls: int
    avg_cost_per_call_inr: float
    avg_cost_per_connected_inr: float
    days_tracked: int
    usd_to_inr_rate: float
    as_of: datetime


class SyncLogEntry(BaseModel):
    id: str
    source: str
    status: str
    records_synced: int
    message: str
    ran_at: datetime


class DateRangeFilter(BaseModel):
    date_from: date | None = None
    date_to: date | None = None
    platform: str | None = None
