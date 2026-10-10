# 0015 CI authentication through OIDC to OpenBao

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

CI jobs need secrets; static tokens leak and are hard to rotate.

## Decision drivers

- No static secrets in CI.
- Short-lived, scoped credentials.

## Considered options

1. GitLab `id_tokens` (JWT) → OpenBao JWT auth; GitHub Actions → cloud OIDC or restricted Environments
2. CI variables with static tokens

## Decision outcome

Chosen option: "GitLab `id_tokens` (JWT) → OpenBao JWT auth; GitHub Actions → cloud OIDC or restricted Environments".

- Every job with secrets authenticates with an OIDC token bound to project and branch.
- OpenBao issues dynamic credentials where possible.

### Consequences

- Good: nothing to rotate in CI.
- Bad: OpenBao must be available for internal CI.

## Pros and cons of the other options

### CI variables with static tokens

- Bad: long-lived secrets in CI settings.
