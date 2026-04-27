import type { Call } from "../types";

interface Props {
  calls: Call[];
}

const OUTCOME_STYLES: Record<string, string> = {
  booked: "bg-emerald-100 text-emerald-700",
  negotiation_failed: "bg-amber-100 text-amber-700",
  not_eligible: "bg-red-100 text-red-700",
  no_matching_load: "bg-slate-100 text-slate-700",
  carrier_rejected_pitch: "bg-purple-100 text-purple-700",
};

const SENTIMENT_STYLES: Record<string, string> = {
  positive: "bg-emerald-100 text-emerald-700",
  neutral: "bg-slate-100 text-slate-700",
  negative: "bg-red-100 text-red-700",
  frustrated: "bg-orange-100 text-orange-700",
};

function Badge({ value, styles }: { value: string | null; styles: Record<string, string> }) {
  if (!value) return <span className="text-slate-400">—</span>;
  const style = styles[value] || "bg-slate-100 text-slate-700";
  return (
    <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${style}`}>
      {value.replace(/_/g, " ")}
    </span>
  );
}

function formatRate(value: number | null): string {
  if (value === null || value === undefined) return "—";
  return `$${value.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
}

function formatTime(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function CallsTable({ calls }: Props) {
  if (calls.length === 0) {
    return (
      <div className="bg-white rounded-lg border border-slate-200 p-8 text-center text-slate-400">
        No calls recorded yet. When the agent finishes a call, it'll appear here.
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 border-b border-slate-200 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-3 text-left font-medium">Time</th>
              <th className="px-4 py-3 text-left font-medium">MC #</th>
              <th className="px-4 py-3 text-left font-medium">Carrier</th>
              <th className="px-4 py-3 text-left font-medium">Load</th>
              <th className="px-4 py-3 text-right font-medium">Posted</th>
              <th className="px-4 py-3 text-right font-medium">Final</th>
              <th className="px-4 py-3 text-center font-medium">Rounds</th>
              <th className="px-4 py-3 text-left font-medium">Outcome</th>
              <th className="px-4 py-3 text-left font-medium">Sentiment</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {calls.map((call) => (
              <tr key={call.id} className="hover:bg-slate-50">
                <td className="px-4 py-3 text-slate-600 whitespace-nowrap">
                  {formatTime(call.timestamp)}
                </td>
                <td className="px-4 py-3 font-mono text-slate-700">{call.mc_number || "—"}</td>
                <td className="px-4 py-3 text-slate-700">{call.company_name || "—"}</td>
                <td className="px-4 py-3 font-mono text-slate-700">{call.load_id || "—"}</td>
                <td className="px-4 py-3 text-right text-slate-600">{formatRate(call.loadboard_rate)}</td>
                <td className="px-4 py-3 text-right font-medium text-slate-900">
                  {formatRate(call.final_agreed_rate)}
                </td>
                <td className="px-4 py-3 text-center text-slate-600">{call.negotiation_rounds}</td>
                <td className="px-4 py-3"><Badge value={call.outcome} styles={OUTCOME_STYLES} /></td>
                <td className="px-4 py-3"><Badge value={call.sentiment} styles={SENTIMENT_STYLES} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
