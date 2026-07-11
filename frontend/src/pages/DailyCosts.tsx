import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { DailyCostRow } from "../types";

export default function DailyCosts() {
  const [rows, setRows] = useState<DailyCostRow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getDaily().then(setRows).finally(() => setLoading(false));
  }, []);

  return (
    <div className="page">
      <header className="page-header">
        <div>
          <h2>Daily breakdown</h2>
          <p>Per-day provider allocation, call volume, and cost-per-connected metrics.</p>
        </div>
        <a className="btn secondary" href="/api/v1/export/daily.csv">Download CSV</a>
      </header>
      <div className="panel table-wrap">
        {loading ? (
          <div className="page-state">Loading…</div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th className="num">OpenAI</th>
                <th className="num">Anthropic</th>
                <th className="num">ElevenLabs</th>
                <th className="num">Deepgram</th>
                <th className="num">Telephony</th>
                <th className="num">Calls</th>
                <th className="num">Connected</th>
                <th className="num">Total INR</th>
                <th className="num">CPC</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.date}>
                  <td>{r.date}</td>
                  <td className="num">${r.openai}</td>
                  <td className="num">${r.anthropic}</td>
                  <td className="num">${r.elevenlabs}</td>
                  <td className="num">${r.deepgram}</td>
                  <td className="num">${r.telephony}</td>
                  <td className="num">{r.calls}</td>
                  <td className="num">{r.connected_calls}</td>
                  <td className="num">₹{r.total_inr.toLocaleString()}</td>
                  <td className="num">₹{r.cost_per_call_inr}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
