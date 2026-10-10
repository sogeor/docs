# 0014 GitLab in the management cluster

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

Internal CI needs access to OpenBao, Harbor and clusters through the mesh, with OIDC-based secrets.

## Decision drivers

- Self-hosted, close to the internal services.
- OIDC id tokens for OpenBao.

## Considered options

1. GitLab CE from the Helm chart with GitLab Runner (Kubernetes executor) in `mgmt`
2. GitHub Actions for everything
3. Omnibus GitLab on a VM

## Decision outcome

Chosen option: "GitLab CE from the Helm chart with GitLab Runner (Kubernetes executor) in `mgmt`".

- Profile `ci`; external PostgreSQL (CloudNativePG), Redis and object storage (SeaweedFS).
- GitLab manages workload clusters, never `mgmt`.

### Consequences

- Good: backups and topology follow platform rules.
- Bad: significant memory use on the home host.

## Pros and cons of the other options

### GitHub Actions for everything

- Bad: internal services must not be reachable from public runners.

### Omnibus GitLab on a VM

- Bad: outside GitOps; separate backup path.
