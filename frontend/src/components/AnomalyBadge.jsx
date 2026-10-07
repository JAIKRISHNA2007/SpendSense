import React from 'react';

export default function AnomalyBadge({ level = 'Medium' }) {
  const isHigh = level === 'High';
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold ${
        isHigh
          ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
          : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
      }`}
    >
      {level} Anomaly
    </span>
  );
}
