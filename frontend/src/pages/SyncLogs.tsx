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
    await api.triggerSync("Manual — All Sources");
    await load();
    setSyncing(false);
  };

  return (
    <div className="page">
      <header className="page-header">
        <div>
          <h2>Sync pipeline</h2>
          <p>Billing ingestion jobs from BigQuery, provider APIs, and call-store connectors.</p>
        </div>
        <button className="btn" onClick={trigger} disabled={syncing}>
          {syncing ? "Running sync…" : "Run manual sync"}
        </button>
      </header>
      <div className="panel table-wrap">
        <table>
          <thead>
            <tr><th>Timestamp</th><th>Source</th><th>Status</th><th className="num">Records</th><th>Message</th></tr>
          </thead>
          <tbody>
            {logs.map((l) => (
              <tr key={l.id}>
                <td>{new Date(l.ran_at).toLocaleString()}</td>
                <td>{l.source}</td>
                <td><span className="badge">{l.status}</span></td>
                <td className="num">{l.records_synced}</td>
                <td>{l.message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
