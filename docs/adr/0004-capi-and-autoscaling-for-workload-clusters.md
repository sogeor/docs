# 0004 Cluster API and autoscaling for workload clusters

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

Workload clusters run in clouds and must be created, scaled, repaired and torn down cheaply and automatically.

## Decision drivers

- Pay-as-you-go: scale workers to zero.
- Self-healing nodes.
- One declarative interface for several providers.

## Considered options

1. Cluster API with provider plugins and Cluster Autoscaler (`clusterapi`)
2. OpenTofu per workload cluster
3. Managed Kubernetes per provider

## Decision outcome

Chosen option: "Cluster API with provider plugins and Cluster Autoscaler (`clusterapi`)".

- Workload clusters are `Cluster` objects in Git, applied by Argo CD in `mgmt`.
- `MachineHealthCheck` replaces failed nodes; Cluster Autoscaler annotations set `min`/`max` per pool.

### Consequences

- Good: tear down and recreate through Git.
- Good: rolling replacement for image updates.
- Bad: `mgmt` must be available for changes; workload clusters keep running without it.

## Pros and cons of the other options

### OpenTofu per workload cluster

- Bad: no reconciliation, no health checks, no autoscaling.

### Managed Kubernetes per provider

- Bad: different APIs, no Talos, less control over hardening.
