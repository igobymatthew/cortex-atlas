import React from "react";

type StateNode = {
  id: string;
  label: string;
  weight?: number;
};

type StateEdge = {
  from: string;
  to: string;
  probability?: number;
};

type StateMachineProps = {
  nodes: StateNode[];
  edges: StateEdge[];
};

export function StateMachine({ nodes, edges }: StateMachineProps) {
  return (
    <div>
      <h3>State Machine</h3>
      <ul>
        {nodes.map((node) => (
          <li key={node.id}>
            {node.label} {node.weight !== undefined ? `(${node.weight})` : ""}
          </li>
        ))}
      </ul>
      <ul>
        {edges.map((edge, index) => (
          <li key={`${edge.from}-${edge.to}-${index}`}>
            {edge.from} → {edge.to}
            {edge.probability !== undefined ? ` (${edge.probability})` : ""}
          </li>
        ))}
      </ul>
    </div>
  );
}
