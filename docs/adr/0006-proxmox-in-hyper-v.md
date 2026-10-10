# 0006 Proxmox VE nested in Hyper-V at home

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

The home host runs Windows. The platform needs an API-driven hypervisor for `mgmt`, image builds and Astra pools.

## Decision drivers

- Use existing hardware.
- An API supported by Packer, OpenTofu and Cluster API.
- No changes to the host OS.

## Considered options

1. Proxmox VE as a Hyper-V VM with nested virtualization
2. Hyper-V directly
3. Bare-metal Proxmox

## Decision outcome

Chosen option: "Proxmox VE as a Hyper-V VM with nested virtualization".

- Proxmox runs in a Hyper-V VM on a NAT network; no inbound ports.
- The VM is created idempotently by `bootstrap` scripts.

### Consequences

- Good: Packer, `bpg/proxmox` and CAPMOX work unchanged.
- Bad: nested virtualization costs performance.
- Bad: a single physical host; `mgmt` at home cannot be HA.

## Pros and cons of the other options

### Hyper-V directly

- Bad: weak OpenTofu and Cluster API support.

### Bare-metal Proxmox

- Bad: requires a dedicated machine.
