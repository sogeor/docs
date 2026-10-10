# 0005 Topology `single` and `ha`

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

Budget allows one node per cluster today, while the reference must show highly available operation.

## Decision drivers

- Minimum cost now.
- Moving to HA without rewriting code.

## Considered options

1. A `topology` switch that every component and template honors
2. HA only
3. Single only

## Decision outcome

Chosen option: "A `topology` switch that every component and template honors".

- `single`: one control plane node, one replica, no PodDisruptionBudget, local-path storage.
- `ha`: three control plane nodes, 2–3 replicas, required anti-affinity, PDBs, replicated storage.

### Consequences

- Good: one code path, two cost profiles.
- Bad: every component must be tested in both modes.
- Bad: `single` is honestly not HA; failure model documents the limits.

## Pros and cons of the other options

### HA only

- Bad: triples cost; impossible on one home host.

### Single only

- Bad: does not demonstrate production patterns; a later rewrite.
