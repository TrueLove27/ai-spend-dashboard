# AI Spend Dashboard

Internal-style **cost control tower** for AI voice and LLM infrastructure. Aggregates spend across providers, tracks cost-per-connected-call, and surfaces agent-level economics — with a React dashboard and FastAPI backend.

## Highlights

- Multi-provider billing view (LLM, TTS, ASR, telephony)
- INR and USD reporting with configurable FX
- Daily breakdowns, category splits, and weekly rollups
- Agent cost analysis (calls, duration, booking rate)
- Sync pipeline for billing ingestion jobs
- CSV export for finance review

## Stack

| Layer | Tech |
|-------|------|
| Backend | Python, FastAPI, Pydantic, APScheduler |
| Frontend | React, TypeScript, Vite, Recharts |
| Data | JSON store (demo dataset included) |

## Getting started

**With Docker**

```bash
docker compose up --build
```

- App: http://localhost:5173  
- API docs: http://localhost:8000/docs  

**Local development**

```bash
# Backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend && npm install && npm run dev
```

## API overview

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/costs/summary` | Aggregate KPIs |
| `GET /api/v1/costs/daily` | Daily cost rows |
| `GET /api/v1/costs/agents` | Agent-level metrics |
| `GET /api/v1/analytics/platform-breakdown` | Provider share |
| `GET /api/v1/export/daily.csv` | CSV export |

Full reference: `/docs` when the backend is running.

## Architecture

Layered backend: **API → Service → Repository → Data**. The frontend is a multi-page SPA that talks to `/api/v1` via a typed client.

## License

MIT
