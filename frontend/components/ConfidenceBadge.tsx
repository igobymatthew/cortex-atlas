import React from "react";

type ConfidenceBadgeProps = {
  value: number;
  label?: string;
};

function formatConfidence(value: number) {
  return `${Math.round(value * 100)}%`;
}

export function ConfidenceBadge({ value, label = "Confidence" }: ConfidenceBadgeProps) {
  const displayValue = Number.isFinite(value) ? Math.max(0, Math.min(1, value)) : 0;
  return (
    <div>
      <strong>{label}:</strong> {formatConfidence(displayValue)}
    </div>
  );
}
