import { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell,
} from "recharts";
import { api } from "../api/client";
import type { CategoryBreakdown, DailyCostRow, SummaryMetrics } from "../types";

const COLORS = ["#10b981", "#3b82f6", "#8b5cf6", "#f59e0b", "#64748b"];

export default function Dashboard() {
  const [summary, setSummary] = useState<SummaryMetrics | null>(null);
  const [daily, setDaily] = useState<DailyCostRow[]>([]);
  const [categories, setCategories] = useState<CategoryBreakdown[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([api.getSummary(), api.getDaily(), api.getCategories()])
      .then(([s, d, c]) => { setSummary(s); setDaily(d); setCategories(c); })
      .catch((e) => setError(String(e)));
  }, []);

  if (error) return <div className="page-state error">Could not load dashboard — is the API running on port 8000?</div>;
  if (!summary) return <div className="page-state">Loading spend data…</div>;

  const chartData = daily.map((r) => ({
    date: r.date.slice(5),
    OpenAI: r.openai,
    Anthropic: r.anthropic,
    ElevenLabs: r.elevenlabs,
    Deepgram: r.deepgram,
  }));

  return (
    <div className="page">
      <header className="page-header">
        <div>
          <h2>Cost overview</h2>
          <p>Multi-provider AI infrastructure spend with INR reporting and connected-call efficiency metrics.</p>
        </div>
        <div className="header-actions">
          <a className="btn secondary" href="/api/v1/export/daily.csv">Export CSV</a>
        </div>
      </header>

      <div className="metric-grid">
        <div className="metric-card">
          <div className="metric-label">Total spend</div>
          <div className="metric-value">₹{summary.total_spend_inr.toLocaleString()}</div>
          <div className="metric-hint">${summary.total_spend_usd.toLocaleString()} USD · {summary.days_tracked} days</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Connected calls</div>
          <div className="metric-value">{summary.connected_calls.toLocaleString()}</div>
          <div className="metric-hint">{summary.total_calls.toLocaleString()} total attempts</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Cost per connected</div>
          <div className="metric-value accent">₹{summary.avg_cost_per_connected_inr}</div>
          <div className="metric-hint">Target benchmark: ₹4.20</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">FX rate</div>
          <div className="metric-value">{summary.usd_to_inr_rate}</div>
          <div className="metric-hint">USD → INR conversion</div>
        </div>
      </div>

      <div className="chart-grid">
        <div className="panel">
          <div className="panel-heading">
            <h3>Daily spend by provider</h3>
            <span>USD · stacked</span>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <XAxis dataKey="date" stroke="#64748b" fontSize={11} tickLine={false} />
              <YAxis stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
              <Tooltip contentStyle={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 8 }} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="OpenAI" stackId="a" fill="#10b981" radius={[0, 0, 0, 0]} />
              <Bar dataKey="Anthropic" stackId="a" fill="#f59e0b" />
              <Bar dataKey="ElevenLabs" stackId="a" fill="#8b5cf6" />
              <Bar dataKey="Deepgram" stackId="a" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="panel">
          <div className="panel-heading">
            <h3>Category split</h3>
            <span>INR</span>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={categories} dataKey="amount_inr" nameKey="name" cx="50%" cy="50%" innerRadius={55} outerRadius={90} paddingAngle={2}>
                {categories.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip contentStyle={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 8 }} formatter={(v: number) => `₹${v.toLocaleString()}`} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
