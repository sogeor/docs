# 0016 Artifact signing with OpenBao Transit

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

Images and charts must be signed with a key that cannot be exfiltrated.

## Decision drivers

- Non-exportable keys.
- Audit of every signature.
- No dependency on public transparency logs for internal artifacts.

## Considered options

1. Cosign with `hashivault://` keys in OpenBao Transit; GitHub artifact attestations for public artifacts
2. Cosign key files in CI secrets
3. Keyless Sigstore only

## Decision outcome

Chosen option: "Cosign with `hashivault://` keys in OpenBao Transit; GitHub artifact attestations for public artifacts".

- One Transit key per project: `transit/keys/cosign-<project>`.
- Public keys are stored in the policies repository for Kyverno verification.

### Consequences

- Good: key never leaves OpenBao.
- Bad: signing depends on OpenBao availability.

## Pros and cons of the other options

### Cosign key files in CI secrets

- Bad: exportable keys.

### Keyless Sigstore only

- Bad: internal artifacts and air-gapped verification need an internal root.
