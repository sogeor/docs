# 0023 Long-term direction: sogeor platform

- Status: proposed
- Date: 2026-10-15

## Context and problem statement

The base platform (Talos, Cluster API, OpenTofu and Ansible) builds clusters from one description, but each
workload cluster is tied to one infrastructure provider, and the node OS, autoscaling and data services come from
third-party projects. The long-term goal is a Platform as a Service for businesses and individuals, where pools of
one cluster run at any providers. Without a recorded direction, decisions made for the base platform could block
that goal, or the goal could be pursued before the base platform works.

## Decision drivers

- Finish and keep the base platform as the working reference.
- Keep the base platform's contracts (cluster description, normalized node) usable by future components.
- Deliver the long-term components one at a time.

## Considered options

1. Record the long-term direction in [Vision and roadmap](../vision.md) and pursue it only after the base platform.
2. Extend the base platform incrementally without a recorded direction.
3. Start the long-term components now, in parallel with the base platform.

## Decision outcome

Chosen option: "Record the long-term direction in Vision and roadmap and pursue it only after the base platform".

- [Vision and roadmap](../vision.md) is the public description of the direction: Sogeor operator (Go) instead of
  Cluster API, Sogeor agent (Rust), Sogeor Kubernetes OS, unified data services, backups and keys, hybrid
  post-quantum and GOST cryptography profiles, pluggable encrypted transport, multi-tenancy.
- Stage 1 of the roadmap is the base platform. Decisions in ADR 0002–0022 stay in force for it; ADR 0003
  (Talos for `mgmt`) and ADR 0004 (Cluster API) are expected to be superseded by later records when the
  corresponding stages start.
- Each later stage gets its own ADR before implementation.

### Consequences

- Good: the base platform is not delayed or changed by the long-term plan.
- Good: contributors see why provider-neutral contracts matter.
- Bad: the vision describes components that do not exist yet; the roadmap must be kept honest about status.

## Pros and cons of the other options

### Extend the base platform incrementally without a recorded direction

- Bad: decisions taken for the base platform may close off the long-term goal.

### Start the long-term components now, in parallel with the base platform

- Bad: splits a single maintainer's effort; neither the base platform nor the new components reach a working state.
