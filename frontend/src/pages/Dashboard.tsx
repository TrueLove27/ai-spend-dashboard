import { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell,
} from "recharts";
import { api } from "../api/client";
import type { CategoryBreakdown, DailyCostRow, SummaryMetrics } from "../types";

const COLORS = ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444"];

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

  if (error) return <p className="error">{error}</p>;
  if (!summary) return <p>Loading…</p>;

  const chartData = daily.map((r) => ({
    date: r.date.slice(5),
    AWS: r.aws,
    GCP: r.gcp,
    Azure: r.azure,
    Vercel: r.vercel,
    Datadog: r.datadog,
  }));

  const sym = summary.currency_display === "EUR" ? "€" : summary.currency_display === "GBP" ? "£" : "$";

  return (
    <>
      <h1 className="page-title">Cost Overview</h1>
      <p className="page-sub">Multi-cloud SaaS spend · SQLite database · live FX via Frankfurter API</p>

      <div className="kpi-grid">
        <div className="kpi"><div className="label">Total Spend ({summary.currency_display})</div><div className="value">{sym}{summary.total_spend_display.toLocaleString()}</div><div className="sub">${summary.total_spend_usd.toLocaleString()} USD</div></div>
        <div className="kpi"><div className="label">Billable Requests</div><div className="value">{summary.billable_requests.toLocaleString()}</div><div className="sub">{summary.total_requests.toLocaleString()} total</div></div>
        <div className="kpi"><div className="label">Cost / Request</div><div className="value">${summary.avg_cost_per_request_usd.toFixed(6)}</div></div>
        <div className="kpi"><div className="label">FX Rate</div><div className="value">{summary.fx_rate_usd_display.toFixed(4)}</div><div className="sub">USD → {summary.currency_display}</div></div>
      </div>

      <div className="grid-2">
        <div className="panel">
          <h2>Daily Spend by Provider (USD)</h2>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={chartData}>
              <XAxis dataKey="date" stroke="#8fa3bf" fontSize={11} />
              <YAxis stroke="#8fa3bf" fontSize={11} />
              <Tooltip contentStyle={{ background: "#151d2e", border: "1px solid #2a3654" }} />
              <Legend />
              <Bar dataKey="AWS" stackId="a" fill="#f59e0b" />
              <Bar dataKey="GCP" stackId="a" fill="#3b82f6" />
              <Bar dataKey="Azure" stackId="a" fill="#10b981" />
              <Bar dataKey="Vercel" stackId="a" fill="#8b5cf6" />
              <Bar dataKey="Datadog" stackId="a" fill="#ef4444" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="panel">
          <h2>Spend by Category (USD)</h2>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={categories} dataKey="amount_usd" nameKey="name" cx="50%" cy="50%" outerRadius={90} label>
                {categories.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip contentStyle={{ background: "#151d2e", border: "1px solid #2a3654" }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </>
  );
}
