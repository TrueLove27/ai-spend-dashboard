import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { IntegrationsResponse } from "../types";

export default function Integrations() {
  const [data, setData] = useState<IntegrationsResponse | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.getIntegrations()
      .then(setData)
      .catch((e) => setError(String(e)));
  }, []);

  if (error) return <p className="error">{error}</p>;
  if (!data) return <p>Loading…</p>;

  return (
    <>
      <h1 className="page-title">API Integrations</h1>
      <p className="page-sub">Connected services and live exchange rates stored in SQLite</p>

      <div className="kpi-grid" style={{ marginBottom: "1.5rem" }}>
        {Object.entries(data.fx_rates).map(([currency, rate]) => (
          <div className="kpi" key={currency}>
            <div className="label">USD → {currency}</div>
            <div className="value">{rate.toFixed(4)}</div>
            <div className="sub">From Frankfurter API</div>
          </div>
        ))}
      </div>

      <div className="panel">
        <table>
          <thead>
            <tr><th>Integration</th><th>Status</th><th>Key Required</th><th>Description</th></tr>
          </thead>
          <tbody>
            {data.integrations.map((i) => (
              <tr key={i.name}>
                <td>{i.name}</td>
                <td><span className="badge">{i.enabled ? "active" : "inactive"}</span></td>
                <td>{i.requires_key ? "Yes" : "No"}</td>
                <td>{i.description}{i.last_status ? <><br /><small style={{ color: "#8fa3bf" }}>{i.last_status}</small></> : null}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
