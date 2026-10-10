# 0007 OpenTofu with state encryption

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

Infrastructure is code. State contains sensitive data (Talos secrets, tokens).

## Decision drivers

- Open-source license.
- Client-side state encryption.
- Compatibility with existing providers.

## Considered options

1. OpenTofu with `encryption` blocks
2. Terraform
3. Pulumi

## Decision outcome

Chosen option: "OpenTofu with `encryption` blocks".

- OpenTofu ≥ 1.10 everywhere; state and plans encrypted.
- External loop uses `pbkdf2` with a passphrase; internal loop uses OpenBao Transit.

### Consequences

- Good: state leak does not leak secrets.
- Bad: losing the passphrase loses the state; it is kept in a password manager.

## Pros and cons of the other options

### Terraform

- Bad: BSL license; no native client-side state encryption.

### Pulumi

- Bad: smaller provider ecosystem for target clouds, different skills.
