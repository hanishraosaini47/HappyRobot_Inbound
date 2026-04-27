import {
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

interface Props {
  data: Record<string, number>;
}

const COLORS: Record<string, string> = {
  booked: "#10b981",
  negotiation_failed: "#f59e0b",
  not_eligible: "#ef4444",
  no_matching_load: "#6b7280",
  carrier_rejected_pitch: "#a855f7",
};

const FALLBACK_COLORS = ["#3b82f6", "#ec4899", "#14b8a6", "#f97316"];

export function OutcomePieChart({ data }: Props) {
  const entries = Object.entries(data).map(([name, value], idx) => ({
    name,
    value,
    color: COLORS[name] || FALLBACK_COLORS[idx % FALLBACK_COLORS.length],
  }));

  if (entries.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400 text-sm">
        No call data yet
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={260}>
      <PieChart>
        <Pie
          data={entries}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={80}
          label={(entry) => `${entry.value}`}
        >
          {entries.map((entry) => (
            <Cell key={entry.name} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}
