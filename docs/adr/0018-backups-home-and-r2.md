# 0018 Backups at home and in Cloudflare R2

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

Data must survive the loss of the home host or a cloud cluster, at minimal cost.

## Decision drivers

- Off-site copy.
- Low cost.
- Automatic restore.

## Considered options

1. SeaweedFS in `mgmt` as primary, copies in Cloudflare R2
2. Cloud provider object storage only
3. Home only

## Decision outcome

Chosen option: "SeaweedFS in `mgmt` as primary, copies in Cloudflare R2".

- CloudNativePG (barman cloud), Velero, OpenBao Raft snapshots and OpenTofu state go to SeaweedFS and R2.
- Clusters bootstrap from the latest backup; monthly restore tests record RTO and RPO.

### Consequences

- Good: losing `mgmt` is recoverable from R2.
- Bad: R2 has no versioning; date prefixes are used.

## Pros and cons of the other options

### Cloud provider object storage only

- Bad: egress and storage costs; tied to one provider.

### Home only

- Bad: no off-site copy.
