from __future__ import annotations

import csv
import io

from sqlalchemy.orm import Session

from app.services.cost_service import get_cost_service


class ExportService:
    def daily_costs_csv(self, db: Session) -> str:
        rows = get_cost_service(db).get_daily_costs()
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow([
            "date", "aws", "gcp", "azure", "vercel", "datadog",
            "requests", "billable_requests", "total_usd", "total_display", "cost_per_request_usd",
        ])
        for r in rows:
            writer.writerow([
                r.date, r.aws, r.gcp, r.azure, r.vercel, r.datadog,
                r.requests, r.billable_requests, r.total_usd, r.total_display, r.cost_per_request_usd,
            ])
        return buf.getvalue()
