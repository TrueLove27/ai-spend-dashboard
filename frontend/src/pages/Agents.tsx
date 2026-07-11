import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { AgentCostRow } from "../types";

export default function Agents() {
  const [agents, setAgents] = useState<AgentCostRow[]>([]);

  useEffect(() => {
    api.getAgents().then(setAgents);
  }, []);

  return (
    <>
      <h1 className="page-title">Agent Cost Analysis</h1>
      <p className="page-sub">Per-agent spend, call volume, duration, and booking conversion</p>
      <div className="panel">
        <table>
          <thead>
            <tr>
              <th>Agent</th><th>Platform</th><th>Calls</th>
              <th>Cost (INR)</th><th>Avg Duration</th><th>Booking Rate</th>
            </tr>
          </thead>
          <tbody>
            {agents.map((a) => (
              <tr key={a.agent_id}>
                <td>{a.agent_name}<br /><small style={{ color: "#8fa3bf" }}>{a.agent_id}</small></td>
                <td>{a.platform}</td>
                <td>{a.calls}</td>
                <td>₹{a.total_cost_inr.toLocaleString()}</td>
                <td>{a.avg_duration_sec}s</td>
                <td>{(a.booking_rate * 100).toFixed(0)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
