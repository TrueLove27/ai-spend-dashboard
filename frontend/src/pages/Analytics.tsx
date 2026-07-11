import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { api } from "../api/client";
import type { PlatformBreakdown } from "../types";

export default function Analytics() {
  const [platforms, setPlatforms] = useState<PlatformBreakdown[]>([]);
  const [weekly, setWeekly] = useState<{ week: string; spend_inr: number; calls: number }[]>([]);

  useEffect(() => {
    Promise.all([api.getPlatformBreakdown(), api.getWeeklyRollup()])
      .then(([p, w]) => { setPlatforms(p); setWeekly(w); });
  }, []);

  return (
    <div className="page">
      <header className="page-header">
        <div>
          <h2>Advanced analytics</h2>
          <p>Provider share analysis and weekly spend rollups for finance review.</p>
        </div>
      </header>
      <div className="chart-grid">
        <div className="panel">
          <div className="panel-heading"><h3>Platform share</h3><span>USD total</span></div>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={platforms} layout="vertical" margin={{ left: 20 }}>
              <XAxis type="number" stroke="#64748b" fontSize={11} />
              <YAxis type="category" dataKey="platform" stroke="#64748b" fontSize={11} width={88} />
              <Tooltip contentStyle={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 8 }} />
              <Bar dataKey="amount_usd" fill="#10b981" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="panel table-wrap">
          <div className="panel-heading"><h3>Weekly rollup</h3></div>
          <table>
            <thead><tr><th>Week</th><th className="num">Spend INR</th><th className="num">Calls</th></tr></thead>
            <tbody>
              {weekly.map((w) => (
                <tr key={w.week}>
                  <td>{w.week}</td>
                  <td className="num">₹{Math.round(w.spend_inr).toLocaleString()}</td>
                  <td className="num">{w.calls}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
