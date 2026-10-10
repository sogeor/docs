# 0011 Headscale mesh with an AmneziaWG fallback

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

Sites (home, clouds, CI) need private connectivity; plain WireGuard may be blocked in some networks.

## Decision drivers

- Self-hosted control plane.
- ACLs as code.
- Survive WireGuard blocking.

## Considered options

1. Headscale + DERP on a small VDS, Tailscale clients; AmneziaWG as plan B
2. Tailscale SaaS
3. Manual WireGuard

## Decision outcome

Chosen option: "Headscale + DERP on a small VDS, Tailscale clients; AmneziaWG as plan B".

- Headscale and DERP run on `edge`; ACLs live in `management`.
- DERP over HTTPS is the first fallback; AmneziaWG is planned if needed.

### Consequences

- Good: one mesh for nodes, CI and admins.
- Bad: `edge` is a dependency for cross-site traffic.

## Pros and cons of the other options

### Tailscale SaaS

- Bad: external dependency and account limits.

### Manual WireGuard

- Bad: manual key management, no ACLs, no NAT traversal.
