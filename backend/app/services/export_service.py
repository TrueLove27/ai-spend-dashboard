from __future__ import annotations

import csv
import io

from app.services.cost_service import cost_service


class ExportService:
    def daily_costs_csv(self) -> str:
        rows = cost_service.get_daily_costs()
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow([
            "date", "openai", "anthropic", "elevenlabs", "deepgram", "telephony",
            "calls", "connected_calls", "total_usd", "total_inr", "cpc_inr",
        ])
        for r in rows:
            writer.writerow([
                r.date, r.openai, r.anthropic, r.elevenlabs, r.deepgram, r.telephony,
                r.calls, r.connected_calls, r.total_usd, r.total_inr, r.cost_per_call_inr,
            ])
        return buf.getvalue()


export_service = ExportService()
