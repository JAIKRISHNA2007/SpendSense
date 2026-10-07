import React from 'react';

export default function AnomalyBadge({ level = 'Medium' }) {
  const isHigh = level === 'High';
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-[11px] font-semibold tracking-wide ${
        isHigh
          ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40 shadow-sm shadow-rose-950/50'
          : 'bg-amber-500/20 text-amber-300 border border-amber-500/40 shadow-sm shadow-amber-950/50'
      }`}
    >
      <span
        className={`w-1.5 h-1.5 rounded-full ${
          isHigh ? 'bg-rose-400 animate-pulse' : 'bg-amber-400'
        }`}
      />
      {level} Anomaly
    </span>
  );
}
