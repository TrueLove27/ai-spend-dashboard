import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { WorkspaceCostRow } from "../types";

export default function Workspaces() {
  const [workspaces, setWorkspaces] = useState<WorkspaceCostRow[]>([]);

  useEffect(() => {
    api.getWorkspaces().then(setWorkspaces);
  }, []);

  return (
    <>
      <h1 className="page-title">Workspace Cost Analysis</h1>
      <p className="page-sub">Per-team spend, request volume, latency, and utilization</p>
      <div className="panel">
        <table>
          <thead>
            <tr>
              <th>Workspace</th><th>Provider</th><th>Requests</th>
              <th>Cost (USD)</th><th>Avg Latency</th><th>Utilization</th>
            </tr>
          </thead>
          <tbody>
            {workspaces.map((w) => (
              <tr key={w.workspace_id}>
                <td>{w.workspace_name}<br /><small style={{ color: "#8fa3bf" }}>{w.workspace_id}</small></td>
                <td>{w.primary_provider}</td>
                <td>{w.requests.toLocaleString()}</td>
                <td>${w.total_cost_usd.toLocaleString()}</td>
                <td>{w.avg_latency_ms}ms</td>
                <td>{(w.utilization_rate * 100).toFixed(0)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
