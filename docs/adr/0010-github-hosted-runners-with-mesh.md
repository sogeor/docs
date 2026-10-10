# 0010 GitHub-hosted runners with mesh access

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

CI must reach home and cloud networks without exposing them, and self-hosted runners on public repositories are risky.

## Decision drivers

- No inbound ports.
- No persistent runners executing untrusted code.
- Least privilege network access.

## Considered options

1. GitHub-hosted runners joining the mesh with ephemeral keys
2. Self-hosted runners at home
3. Publishing APIs to the internet

## Decision outcome

Chosen option: "GitHub-hosted runners joining the mesh with ephemeral keys".

- Infrastructure jobs run on GitHub-hosted runners and join the mesh with an ephemeral key restricted by ACLs.
- Until Headscale exists, a temporary WireGuard hub is used for image builds.

### Consequences

- Good: ephemeral, isolated jobs.
- Bad: network setup adds time to each job.

## Pros and cons of the other options

### Self-hosted runners at home

- Bad: public repositories can run code on home hardware; persistent compromise risk.

### Publishing APIs to the internet

- Bad: violates the no-inbound rule.
