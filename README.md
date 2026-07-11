# AI Spend Dashboard

A full-stack internal-style dashboard for tracking AI voice and LLM infrastructure costs across multiple providers. Built as a **portfolio project** with entirely synthetic data — no real API keys or production endpoints.

## Features

- **Summary KPIs** — total spend, call volume, average cost-per-call
- **Daily breakdown** — stacked bar chart by provider (OpenAI, Anthropic, ElevenLabs, Deepgram)
- **Category split** — LLM, TTS, ASR, telephony, analysis
- **REST API** — FastAPI backend with filterable date ranges

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11+, FastAPI, Pydantic |
| Frontend | HTML, CSS, Chart.js |
| Data | Local JSON mock dataset |

## Quick Start

```bash
# Terminal 1 — API
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend (any static server)
cd frontend
python -m http.server 5173
# Open http://localhost:5173
```

API docs: http://localhost:8000/docs

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/summary` | Aggregate KPIs |
| GET | `/api/daily` | Daily cost rows (`?from=YYYY-MM-DD&to=YYYY-MM-DD`) |
| GET | `/api/categories` | Spend by category |
| GET | `/api/platform-trends` | Per-platform time series |

## Skills Demonstrated

- Full-stack dashboard development
- Cost analytics & KPI design
- Multi-provider billing aggregation patterns
- REST API design with FastAPI

## License

MIT — portfolio use.
