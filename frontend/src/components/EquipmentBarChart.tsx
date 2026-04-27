import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface Props {
  data: Record<string, number>;
}

const COLORS: Record<string, string> = {
  dry_van: "#3b82f6",
  reefer: "#06b6d4",
  flatbed: "#8b5cf6",
};

export function EquipmentBarChart({ data }: Props) {
  const entries = Object.entries(data).map(([name, value]) => ({
    name: name.replace(/_/g, " "),
    rawName: name,
    value,
    color: COLORS[name] || "#64748b",
  }));

  if (entries.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400 text-sm">
        No equipment data yet
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={entries}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis dataKey="name" tick={{ fontSize: 12 }} />
        <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
        <Tooltip />
        <Bar dataKey="value">
          {entries.map((entry) => (
            <Cell key={entry.rawName} fill={entry.color} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
