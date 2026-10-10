# 0002 Cluster constructor

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

Clusters differ by distribution, operating system, provider, size and topology. Writing code per cluster multiplies modules and drifts between environments.

## Decision drivers

- Adding a cluster must not require new code.
- Invalid combinations must be rejected before any resource is created.
- The same description must work for Cluster API and OpenTofu.

## Considered options

1. A declarative cluster description with independent axes, validated by JSON Schema and Conftest
2. One OpenTofu root module per cluster
3. A managed Kubernetes service per cloud

## Decision outcome

Chosen option: "A declarative cluster description with independent axes, validated by JSON Schema and Conftest".

- A cluster is `distribution + kubernetes_version + topology + profiles + network`; a pool is `role + os + provider + size + count|autoscale + labels + taints`.
- The distribution is set per cluster, the OS per pool.
- Both mechanisms output the normalized node contract.

### Consequences

- Good: new combinations are data, reviewed as YAML.
- Good: validations encode compatibility rules once.
- Bad: the schema and the compatibility matrix must be maintained together with providers.

## Pros and cons of the other options

### One OpenTofu root module per cluster

- Bad: code duplication; every new combination is new code.

### A managed Kubernetes service per cloud

- Bad: provider lock-in; no Talos, Astra or home sites; different APIs per cloud.
