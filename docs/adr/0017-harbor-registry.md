# 0017 Harbor as the container registry

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

Clusters need a registry with proxy cache, scanning, signature policies and OIDC.

## Decision drivers

- Self-hosted.
- Scanning and policy enforcement.
- OIDC through Keycloak.

## Considered options

1. Harbor in `mgmt`
2. Public registries only
3. Plain distribution registry

## Decision outcome

Chosen option: "Harbor in `mgmt`".

- Harbor runs in `mgmt` with built-in Trivy and proxy cache projects.
- Platform manifests reference images by digest only.

### Consequences

- Good: one place for supply-chain policy.
- Bad: another stateful service to back up.

## Pros and cons of the other options

### Public registries only

- Bad: rate limits, no internal policy.

### Plain distribution registry

- Bad: no scanning, policies or UI.
