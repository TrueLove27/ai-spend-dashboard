import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { AgentCostRow } from "../types";

export default function Agents() {
  const [agents, setAgents] = useState<AgentCostRow[]>([]);

  useEffect(() => {
    api.getAgents().then(setAgents);
  }, []);

  return (
    <div className="page">
      <header className="page-header">
        <div>
          <h2>Agent economics</h2>
          <p>Voice agent spend, handle time, and booking conversion by platform.</p>
        </div>
      </header>
      <div className="panel table-wrap">
        <table>
          <thead>
            <tr>
              <th>Agent</th>
              <th>Platform</th>
              <th className="num">Calls</th>
              <th className="num">Spend (INR)</th>
              <th className="num">Avg duration</th>
              <th className="num">Booking rate</th>
            </tr>
          </thead>
          <tbody>
            {agents.map((a) => (
              <tr key={a.agent_id}>
                <td>
                  <strong>{a.agent_name}</strong>
                  <div style={{ color: "#64748b", fontSize: "0.78rem" }}>{a.agent_id}</div>
                </td>
                <td>{a.platform}</td>
                <td className="num">{a.calls.toLocaleString()}</td>
                <td className="num">₹{a.total_cost_inr.toLocaleString()}</td>
                <td className="num">{a.avg_duration_sec}s</td>
                <td className="num">{(a.booking_rate * 100).toFixed(0)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
