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
  getAgents: () => request<import("../types").AgentCostRow[]>("/costs/agents"),
  getSyncLogs: () => request<import("../types").SyncLogEntry[]>("/costs/sync-logs"),
  getPlatformBreakdown: () => request<import("../types").PlatformBreakdown[]>("/analytics/platform-breakdown"),
  getWeeklyRollup: () => request<{ week: string; spend_inr: number; calls: number }[]>("/analytics/weekly-rollup"),
  triggerSync: (source: string) =>
    request<import("../types").SyncLogEntry>(`/costs/sync/${encodeURIComponent(source)}`, { method: "POST" }),
};
