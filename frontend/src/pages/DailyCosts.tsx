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
      <p className="page-sub">Per-day provider split with CPC and connected call metrics</p>
      <div className="panel">
        <table>
          <thead>
            <tr>
              <th>Date</th><th>OpenAI</th><th>Anthropic</th><th>ElevenLabs</th>
              <th>Deepgram</th><th>Telephony</th><th>Calls</th><th>Connected</th>
              <th>Total INR</th><th>CPC INR</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.date}>
                <td>{r.date}</td>
                <td>${r.openai}</td><td>${r.anthropic}</td><td>${r.elevenlabs}</td>
                <td>${r.deepgram}</td><td>${r.telephony}</td>
                <td>{r.calls}</td><td>{r.connected_calls}</td>
                <td>₹{r.total_inr.toLocaleString()}</td>
                <td>₹{r.cost_per_call_inr}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <a className="btn" href="/api/v1/export/daily.csv">Export CSV</a>
    </>
  );
}
