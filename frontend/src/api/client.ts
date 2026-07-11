const BASE = "/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, init);
  if (!res.ok) throw new Error(`API ${path} failed: ${res.status}`);
  return res.json();
}

export const api = {
  getSummary: () => request<import("../types").SummaryMetrics>("/costs/summary"),
  getDaily: () => request<import("../types").DailyCostRow[]>("/costs/daily"),
  getCategories: () => request<import("../types").CategoryBreakdown[]>("/costs/categories"),
  getWorkspaces: () => request<import("../types").WorkspaceCostRow[]>("/costs/workspaces"),
  getSyncLogs: () => request<import("../types").SyncLogEntry[]>("/costs/sync-logs"),
  getIntegrations: () => request<import("../types").IntegrationsResponse>("/integrations/status"),
  getPlatformBreakdown: () => request<import("../types").PlatformBreakdown[]>("/analytics/platform-breakdown"),
  getWeeklyRollup: () => request<{ week: string; spend_usd: number; requests: number }[]>("/analytics/weekly-rollup"),
  triggerSync: (source: string) =>
    request<import("../types").SyncLogEntry>(`/costs/sync/${encodeURIComponent(source)}`, { method: "POST" }),
};
