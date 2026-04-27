import type { LaneCount } from "../types";

interface Props {
  lanes: LaneCount[];
}

export function TopLanesTable({ lanes }: Props) {
  if (lanes.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400 text-sm">
        No lane data yet
      </div>
    );
  }

  const maxCount = Math.max(...lanes.map((l) => l.count));

  return (
    <div className="space-y-3">
      {lanes.map((lane, idx) => (
        <div key={`${lane.origin}-${lane.destination}-${idx}`}>
          <div className="flex items-center justify-between text-sm mb-1">
            <span className="text-slate-700 font-medium">
              {lane.origin} <span className="text-slate-400">→</span> {lane.destination}
            </span>
            <span className="text-slate-500 tabular-nums">{lane.count}</span>
          </div>
          <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-blue-500 rounded-full"
              style={{ width: `${(lane.count / maxCount) * 100}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
