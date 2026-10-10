# 0008 OpenTofu state on gitlab.com, portable

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

The external loop needs a remote state backend with locking before any platform storage exists.

## Decision drivers

- Free.
- Locking.
- Migration to S3 later without code changes.

## Considered options

1. gitlab.com managed state over the `http` backend
2. S3 bucket in a cloud
3. Local state

## Decision outcome

Chosen option: "gitlab.com managed state over the `http` backend".

- `backend "http" {}` with `TF_HTTP_*` variables; state names `bootstrap`, `edge`, `mgmt`, `dns`, `cloudflare`.
- Migration to S3 is `tofu init -migrate-state` and is documented.

### Consequences

- Good: zero cost, built-in locking.
- Bad: dependency on gitlab.com availability; daily state backups to object storage.

## Pros and cons of the other options

### S3 bucket in a cloud

- Bad: costs money and must exist before the platform; chicken-and-egg.

### Local state

- Bad: no locking, no CI.
