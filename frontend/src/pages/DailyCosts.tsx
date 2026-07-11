import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { DailyCostRow } from "../types";

export default function DailyCosts() {
  const [rows, setRows] = useState<DailyCostRow[]>([]);

  useEffect(() => {
    api.getDaily().then(setRows);
  }, []);

  return (
    <>
      <h1 className="page-title">Daily Cost Breakdown</h1>
      <p className="page-sub">Per-day provider split with request volume and cost-per-request metrics</p>
      <div className="panel">
        <table>
          <thead>
            <tr>
              <th>Date</th><th>AWS</th><th>GCP</th><th>Azure</th>
              <th>Vercel</th><th>Datadog</th><th>Requests</th><th>Billable</th>
              <th>Total USD</th><th>$/Request</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.date}>
                <td>{r.date}</td>
                <td>${r.aws}</td><td>${r.gcp}</td><td>${r.azure}</td>
                <td>${r.vercel}</td><td>${r.datadog}</td>
                <td>{r.requests.toLocaleString()}</td><td>{r.billable_requests.toLocaleString()}</td>
                <td>${r.total_usd.toLocaleString()}</td>
                <td>${r.cost_per_request_usd}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <a className="btn" href="/api/v1/export/daily.csv">Export CSV</a>
    </>
  );
}
