# 0013 Cilium with ClusterMesh

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

Clusters need a CNI with network policies, encryption, observability and multi-cluster service discovery.

## Decision drivers

- Default-deny and FQDN policies.
- Transparent encryption.
- Multi-cluster.

## Considered options

1. Cilium with WireGuard, Hubble and ClusterMesh
2. Calico
3. Flannel

## Decision outcome

Chosen option: "Cilium with WireGuard, Hubble and ClusterMesh".

- Cilium is part of profile `core` in every cluster.
- Non-overlapping CIDRs per `cluster_id` enable ClusterMesh.

### Consequences

- Good: one CNI everywhere.
- Bad: eBPF requirements on kernels (checked per OS).

## Pros and cons of the other options

### Calico

- Bad: multi-cluster and L7 visibility require more components.

### Flannel

- Bad: no network policies.
