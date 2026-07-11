import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { SyncLogEntry } from "../types";

export default function SyncLogs() {
  const [logs, setLogs] = useState<SyncLogEntry[]>([]);
  const [syncing, setSyncing] = useState(false);

  const load = () => api.getSyncLogs().then(setLogs);

  useEffect(() => { load(); }, []);

  const trigger = async () => {
    setSyncing(true);
    await api.triggerSync("Manual — All Integrations");
    await load();
    setSyncing(false);
  };

  return (
    <>
      <h1 className="page-title">Data Sync Pipeline</h1>
      <p className="page-sub">Live ingestion from Frankfurter FX, provider status pages, and optional Stripe billing</p>
      <button className="btn" onClick={trigger} disabled={syncing} style={{ marginBottom: "1rem" }}>
        {syncing ? "Syncing…" : "Trigger Manual Sync"}
      </button>
      <div className="panel">
        <table>
          <thead>
            <tr><th>Time</th><th>Source</th><th>Status</th><th>Records</th><th>API</th><th>Message</th></tr>
          </thead>
          <tbody>
            {logs.map((l) => (
              <tr key={l.id}>
                <td>{new Date(l.ran_at).toLocaleString()}</td>
                <td>{l.source}</td>
                <td><span className="badge">{l.status}</span></td>
                <td>{l.records_synced}</td>
                <td><small>{l.api_endpoint ?? "—"}</small></td>
                <td>{l.message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
