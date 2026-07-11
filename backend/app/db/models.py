from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class DailyCost(Base):
    __tablename__ = "daily_costs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cost_date: Mapped[date] = mapped_column(Date, unique=True, index=True)
    aws: Mapped[float] = mapped_column(Float, default=0)
    gcp: Mapped[float] = mapped_column(Float, default=0)
    azure: Mapped[float] = mapped_column(Float, default=0)
    vercel: Mapped[float] = mapped_column(Float, default=0)
    datadog: Mapped[float] = mapped_column(Float, default=0)
    requests: Mapped[int] = mapped_column(Integer, default=0)
    billable_requests: Mapped[int] = mapped_column(Integer, default=0)


class Workspace(Base):
    __tablename__ = "workspaces"

    workspace_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    workspace_name: Mapped[str] = mapped_column(String(128))
    primary_provider: Mapped[str] = mapped_column(String(64))
    requests: Mapped[int] = mapped_column(Integer, default=0)
    total_cost_usd: Mapped[float] = mapped_column(Float, default=0)
    avg_latency_ms: Mapped[float] = mapped_column(Float, default=0)
    utilization_rate: Mapped[float] = mapped_column(Float, default=0)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64))
    amount_usd: Mapped[float] = mapped_column(Float, default=0)
    percentage: Mapped[float] = mapped_column(Float, default=0)
    trend_pct: Mapped[float] = mapped_column(Float, default=0)


class SyncLog(Base):
    __tablename__ = "sync_logs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(32))
    records_synced: Mapped[int] = mapped_column(Integer, default=0)
    message: Mapped[str] = mapped_column(Text)
    api_endpoint: Mapped[str | None] = mapped_column(String(256), nullable=True)
    ran_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class FxRate(Base):
    __tablename__ = "fx_rates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_currency: Mapped[str] = mapped_column(String(8), default="USD")
    quote_currency: Mapped[str] = mapped_column(String(8))
    rate: Mapped[float] = mapped_column(Float)
    source: Mapped[str] = mapped_column(String(128))
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
