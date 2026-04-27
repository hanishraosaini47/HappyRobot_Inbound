import { useEffect, useState } from "react";
import { api } from "./api";
import { CallsTable } from "./components/CallsTable";
import { EquipmentBarChart } from "./components/EquipmentBarChart";
import { MetricCard } from "./components/MetricCard";
import { OutcomePieChart } from "./components/OutcomePieChart";
import { SentimentBarChart } from "./components/SentimentBarChart";
import { TopLanesTable } from "./components/TopLanesTable";
import type { Call, Metrics } from "./types";

function formatPercent(value: number | null): string {
  if (value === null || value === undefined) return "—";
  return `${(value * 100).toFixed(1)}%`;
}

function formatRate(value: number | null): string {
  if (value === null || value === undefined) return "—";
  return `$${value.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
}

function formatUplift(value: number | null): string {
  if (value === null || value === undefined) return "—";
  const sign = value >= 0 ? "+" : "";
  return `${sign}${value.toFixed(1)}%`;
}

export default function App() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [calls, setCalls] = useState<Call[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    try {
      setError(null);
      const [m, c] = await Promise.all([api.getMetrics(), api.getCalls(20)]);
      setMetrics(m);
      setCalls(c);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load data");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // Poll every 15s so new calls show up automatically during the demo
    const interval = setInterval(load, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen">
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-slate-900">
              Acme Logistics — Carrier Sales
            </h1>
            <p className="text-xs text-slate-500 mt-0.5">
              AI agent performance dashboard
            </p>
          </div>
          <button
            onClick={load}
            className="text-sm bg-slate-900 text-white px-4 py-2 rounded-md hover:bg-slate-700 transition"
          >
            Refresh
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {loading && !metrics ? (
          <div className="text-center text-slate-400 py-12">Loading…</div>
        ) : metrics ? (
          <>
            {/* Top metric cards */}
            <section>
              <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wide mb-3">
                Performance
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
                <MetricCard label="Total Calls" value={metrics.total_calls.toString()} />
                <MetricCard
                  label="Booking Rate"
                  value={formatPercent(metrics.booking_rate)}
                  hint={`${metrics.booked_calls} booked`}
                />
                <MetricCard
                  label="Avg Negotiated Rate"
                  value={formatRate(metrics.avg_negotiated_rate)}
                  hint="across booked deals"
                />
                <MetricCard
                  label="Avg Rate Uplift"
                  value={formatUplift(metrics.avg_rate_uplift_pct)}
                  hint="vs. loadboard rate"
                />
                <MetricCard
                  label="Avg First Counter"
                  value={formatUplift(metrics.avg_first_counter_offer_pct)}
                  hint="carrier opening ask"
                />
                <MetricCard
                  label="Loads Booked"
                  value={`${metrics.booked_loads} / ${metrics.total_loads}`}
                  hint={`${metrics.available_loads} available`}
                />
              </div>
            </section>

            {/* Charts row 1 */}
            <section className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-5">
                <h3 className="text-sm font-semibold text-slate-700 mb-3">
                  Call Outcomes
                </h3>
                <OutcomePieChart data={metrics.outcome_breakdown} />
              </div>
              <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-5">
                <h3 className="text-sm font-semibold text-slate-700 mb-3">
                  Carrier Sentiment
                </h3>
                <SentimentBarChart data={metrics.sentiment_breakdown} />
              </div>
            </section>

            {/* Charts row 2 — demand insights */}
            <section className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-5">
                <h3 className="text-sm font-semibold text-slate-700 mb-3">
                  Top Requested Lanes
                </h3>
                <p className="text-xs text-slate-500 mb-4">
                  What carriers are calling about — useful for sourcing decisions
                </p>
                <TopLanesTable lanes={metrics.top_requested_lanes} />
              </div>
              <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-5">
                <h3 className="text-sm font-semibold text-slate-700 mb-3">
                  Equipment Demand
                </h3>
                <EquipmentBarChart data={metrics.top_requested_equipment} />
              </div>
            </section>

            {/* Recent calls table */}
            <section>
              <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wide mb-3">
                Recent Calls
              </h2>
              <CallsTable calls={calls} />
            </section>
          </>
        ) : null}
      </main>

      <footer className="max-w-7xl mx-auto px-6 py-6 text-xs text-slate-400 text-center">
        Powered by HappyRobot · Auto-refreshes every 15s
      </footer>
    </div>
  );
}
