// Shared TypeScript types matching backend response shapes.

export interface Call {
  id: number;
  call_id: string;
  timestamp: string;
  duration_seconds: number | null;
  mc_number: string | null;
  company_name: string | null;
  carrier_eligible: boolean | null;
  load_id: string | null;
  loadboard_rate: number | null;
  final_agreed_rate: number | null;
  first_counter_offer: number | null;
  negotiation_rounds: number;
  deal_agreed: boolean;
  transfer_initiated: boolean;
  requested_origin: string | null;
  requested_destination: string | null;
  requested_equipment_type: string | null;
  outcome: string | null;
  sentiment: string | null;
  transcript: string | null;
}

export interface LaneCount {
  origin: string;
  destination: string;
  count: number;
}

export interface Metrics {
  total_calls: number;
  booked_calls: number;
  booking_rate: number;
  avg_negotiated_rate: number | null;
  avg_negotiation_rounds: number | null;
  avg_rate_uplift_pct: number | null;
  avg_first_counter_offer_pct: number | null;
  total_loads: number;
  available_loads: number;
  booked_loads: number;
  outcome_breakdown: Record<string, number>;
  sentiment_breakdown: Record<string, number>;
  top_requested_lanes: LaneCount[];
  top_requested_equipment: Record<string, number>;
}
