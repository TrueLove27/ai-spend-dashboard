export interface SummaryMetrics {
  currency_display: string;
  total_spend_inr: number;
  total_spend_usd: number;
  total_calls: number;
  connected_calls: number;
  avg_cost_per_call_inr: number;
  avg_cost_per_connected_inr: number;
  days_tracked: number;
  usd_to_inr_rate: number;
  as_of: string;
}

export interface DailyCostRow {
  date: string;
  openai: number;
  anthropic: number;
  elevenlabs: number;
  deepgram: number;
  telephony: number;
  calls: number;
  connected_calls: number;
  total_usd: number;
  total_inr: number;
  cost_per_call_inr: number;
}

export interface CategoryBreakdown {
  name: string;
  amount_inr: number;
  percentage: number;
  trend_pct: number;
}

export interface AgentCostRow {
  agent_id: string;
  agent_name: string;
  platform: string;
  calls: number;
  total_cost_inr: number;
  avg_duration_sec: number;
  booking_rate: number;
}

export interface SyncLogEntry {
  id: string;
  source: string;
  status: string;
  records_synced: number;
  message: string;
  ran_at: string;
}

export interface PlatformBreakdown {
  platform: string;
  amount_usd: number;
  share_pct: number;
}
