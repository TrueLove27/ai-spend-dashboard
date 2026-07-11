"""AI Spend Dashboard — mock billing API for portfolio demo."""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DATA_PATH = Path(__file__).parent / "data" / "mock_costs.json"

app = FastAPI(title="AI Spend Dashboard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _load() -> dict:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


class CostEntry(BaseModel):
    date: str
    openai: float
    anthropic: float
    elevenlabs: float
    deepgram: float
    calls: int
    total: float


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "ai-spend-dashboard"}


@app.get("/api/summary")
def summary():
    data = _load()
    rows = data["daily_costs"]
    total_spend = sum(
        r["openai"] + r["anthropic"] + r["elevenlabs"] + r["deepgram"] for r in rows
    )
    total_calls = sum(r["calls"] for r in rows)
    avg_cpc = round(total_spend / total_calls, 4) if total_calls else 0
    return {
        "currency": data["currency"],
        "total_spend": round(total_spend, 2),
        "total_calls": total_calls,
        "avg_cost_per_call": avg_cpc,
        "days_tracked": len(rows),
        "platforms": data["platforms"],
    }


@app.get("/api/daily", response_model=list[CostEntry])
def daily_costs(
    from_date: date | None = Query(None, alias="from"),
    to_date: date | None = Query(None, alias="to"),
):
    data = _load()
    rows = data["daily_costs"]
    out: list[CostEntry] = []
    for r in rows:
        d = date.fromisoformat(r["date"])
        if from_date and d < from_date:
            continue
        if to_date and d > to_date:
            continue
        total = r["openai"] + r["anthropic"] + r["elevenlabs"] + r["deepgram"]
        out.append(CostEntry(**r, total=round(total, 2)))
    return out


@app.get("/api/categories")
def categories():
    return _load()["categories"]


@app.get("/api/platform-trends")
def platform_trends():
    data = _load()
    platforms = ["openai", "anthropic", "elevenlabs", "deepgram"]
    return {
        p: [{"date": r["date"], "amount": r[p]} for r in data["daily_costs"]]
        for p in platforms
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
