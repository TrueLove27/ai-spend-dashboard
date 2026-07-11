import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { api } from "../api/client";
import type { PlatformBreakdown } from "../types";

export default function Analytics() {
  const [platforms, setPlatforms] = useState<PlatformBreakdown[]>([]);
  const [weekly, setWeekly] = useState<{ week: string; spend_usd: number; requests: number }[]>([]);

  useEffect(() => {
    Promise.all([api.getPlatformBreakdown(), api.getWeeklyRollup()])
      .then(([p, w]) => { setPlatforms(p); setWeekly(w); });
  }, []);

  return (
    <>
      <h1 className="page-title">Advanced Analytics</h1>
      <p className="page-sub">Provider share analysis and weekly spend rollups</p>
      <div className="grid-2">
        <div className="panel">
          <h2>Provider Share (USD)</h2>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={platforms} layout="vertical">
              <XAxis type="number" stroke="#8fa3bf" fontSize={11} />
              <YAxis type="category" dataKey="platform" stroke="#8fa3bf" fontSize={11} width={90} />
              <Tooltip contentStyle={{ background: "#151d2e", border: "1px solid #2a3654" }} />
              <Bar dataKey="amount_usd" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="panel">
          <h2>Weekly Rollup</h2>
          <table>
            <thead><tr><th>Week</th><th>Spend USD</th><th>Requests</th></tr></thead>
            <tbody>
              {weekly.map((w) => (
                <tr key={w.week}><td>{w.week}</td><td>${Math.round(w.spend_usd).toLocaleString()}</td><td>{w.requests.toLocaleString()}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
