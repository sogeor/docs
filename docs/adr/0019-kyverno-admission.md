# 0019 Kyverno for admission control

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

Clusters must enforce security, supply-chain and convention policies at admission.

## Decision drivers

- Policies as Kubernetes YAML.
- Image verification.
- Testable policies.

## Considered options

1. Kyverno, Audit first then Enforce
2. OPA Gatekeeper
3. Pod Security Admission only

## Decision outcome

Chosen option: "Kyverno, Audit first then Enforce".

- Kyverno in profile `core`; `verifyImages` for signatures, provenance and SBOM.
- Exceptions are `PolicyException` objects with an expiry and a reason.

### Consequences

- Good: one engine for validation, mutation and verification.
- Bad: webhook availability affects admission.

## Pros and cons of the other options

### OPA Gatekeeper

- Bad: Rego for every policy; image verification needs extra tooling.

### Pod Security Admission only

- Bad: covers pod security only.
