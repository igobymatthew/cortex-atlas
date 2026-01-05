import React from "react";

type HeatmapProps = {
  rows: string[];
  columns: string[];
  values: number[][];
};

export function Heatmap({ rows, columns, values }: HeatmapProps) {
  return (
    <table>
      <thead>
        <tr>
          <th />
          {columns.map((column) => (
            <th key={column}>{column}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row, rowIndex) => (
          <tr key={row}>
            <td>{row}</td>
            {columns.map((column, columnIndex) => (
              <td key={`${row}-${column}`}>{values[rowIndex]?.[columnIndex] ?? 0}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
