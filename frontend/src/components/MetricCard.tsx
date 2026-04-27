interface Props {
  label: string;
  value: string;
  hint?: string;
}

export function MetricCard({ label, value, hint }: Props) {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-5">
      <div className="text-sm font-medium text-slate-500 uppercase tracking-wide">
        {label}
      </div>
      <div className="mt-2 text-3xl font-bold text-slate-900">{value}</div>
      {hint && <div className="mt-1 text-xs text-slate-400">{hint}</div>}
    </div>
  );
}
