# Capacity

Resource needs depend on profiles and topology. Detailed per-component requests live in the `platform`
repository; this page gives planning numbers.

## Management cluster at home

| Item | Value |
|---|---|
| Hypervisor VM for Proxmox | 32 GB RAM, up to 48 GB if needed |
| `mgmt` topology | `single` |
| Profiles | `core` + `ci` |
| Headroom | Packer builds must fit next to `mgmt` |
| Heavy profiles | `security-plus`, `observability-plus` on demand or in the cloud |

## Workload clusters in the cloud

| Item | Rule |
|---|---|
| Worker pools | Autoscaled; `min: 0` where the workload allows |
| `autoscale.max` | Always set; it is the budget guard |
| Idle clusters | Torn down after a final backup, recreated from Git |
| `store` production | Always on, never scaled to zero; budgeted separately |
| Reference budget | About 10–15 thousand RUB per month, pay-as-you-go |

## Sizing guide

| Cluster | Topology | Control plane | Workers |
|---|---|---|---|
| `mgmt` | `single` | 1 × `2xl` (Proxmox) | — (pods on the control plane) |
| `main` | `single` | 1 × `m` | autoscale `l`, 0–3 |
| `talos` | `single` | 1 × `m` | autoscale `l`, 0–3 |
| any | `ha` | 3 × `m` or larger | autoscale, at least 2 per zone |

!!! note
    Numbers are refined as components land in `platform`; measured consumption replaces estimates.
