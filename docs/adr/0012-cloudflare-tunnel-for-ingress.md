# 0012 Cloudflare Tunnel for inbound traffic

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

Services must be reachable from the internet without public ports at home or public load balancers.

## Decision drivers

- No inbound ports.
- Free tier.
- Works for home and clouds.

## Considered options

1. Cloudflare Tunnel (`cloudflared` in each cluster) and Cloudflare DNS
2. Public LoadBalancer services
3. Port forwarding at home

## Decision outcome

Chosen option: "Cloudflare Tunnel (`cloudflared` in each cluster) and Cloudflare DNS".

- Only Tunnel public hostnames and DNS are used.
- Zero Trust, WAF and paid features are not used; web apps use oauth2-proxy with Keycloak.

### Consequences

- Good: no exposed IP addresses.
- Bad: dependency on Cloudflare for public traffic.

## Pros and cons of the other options

### Public LoadBalancer services

- Bad: cost and exposed endpoints.

### Port forwarding at home

- Bad: exposes the home network.
