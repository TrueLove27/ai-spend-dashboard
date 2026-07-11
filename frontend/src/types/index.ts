export interface SummaryMetrics {
  currency_display: string;
  total_spend_usd: number;
  total_spend_display: number;
  total_requests: number;
  billable_requests: number;
  avg_cost_per_request_usd: number;
  avg_cost_per_billable_usd: number;
  days_tracked: number;
  fx_rate_usd_display: number;
  as_of: string;
}

export interface DailyCostRow {
  date: string;
  aws: number;
  gcp: number;
  azure: number;
  vercel: number;
  datadog: number;
  requests: number;
  billable_requests: number;
  total_usd: number;
  total_display: number;
  cost_per_request_usd: number;
}

export interface CategoryBreakdown {
  name: string;
  amount_usd: number;
  percentage: number;
  trend_pct: number;
}

export interface WorkspaceCostRow {
  workspace_id: string;
  workspace_name: string;
  primary_provider: string;
  requests: number;
  total_cost_usd: number;
  avg_latency_ms: number;
  utilization_rate: number;
}

export interface SyncLogEntry {
  id: string;
  source: string;
  status: string;
  records_synced: number;
  message: string;
  api_endpoint?: string | null;
  ran_at: string;
}

export interface PlatformBreakdown {
  platform: string;
  amount_usd: number;
  share_pct: number;
}

export interface IntegrationStatus {
  name: string;
  enabled: boolean;
  description: string;
  requires_key: boolean;
  last_status: string | null;
}

export interface IntegrationsResponse {
  integrations: IntegrationStatus[];
  fx_rates: Record<string, number>;
}
