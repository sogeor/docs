# 0003 Talos Linux for the management cluster

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

The management cluster holds GitOps, Cluster API, secrets, the registry and CI. It must be small, secure and recreatable from code.

## Decision drivers

- Minimal attack surface.
- Declarative, reproducible configuration.
- Low memory footprint on a home host.

## Considered options

1. Talos Linux with the `siderolabs/talos` OpenTofu provider
2. kubeadm on Ubuntu configured by Ansible
3. k3s

## Decision outcome

Chosen option: "Talos Linux with the `siderolabs/talos` OpenTofu provider".

- `mgmt` runs Talos, created by OpenTofu from the external loop.
- No SSH; administration only through the Talos API.

### Consequences

- Good: immutable, API-only nodes; machine config is code.
- Good: KubeSpan for a future multi-site `ha`.
- Bad: operators must learn `talosctl`; debugging without a shell is harder.

## Pros and cons of the other options

### kubeadm on Ubuntu configured by Ansible

- Bad: mutable OS, SSH, more patching and drift.

### k3s

- Bad: still a general-purpose OS underneath; fewer guarantees on immutability.
