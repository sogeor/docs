# sogeor platform

An open-source reference DevSecOps platform. Anyone can deploy it from this documentation; every decision is
recorded and every component is code.

- **Cluster constructor.** Clusters are assembled from independent axes: distribution, OS per pool, provider,
  size, topology and component profiles. A new combination is a new description file, not new code.
- **Provider-neutral.** Everything above node creation works with a normalized node contract.
- **GitOps.** State lives in Git; Argo CD converges every cluster to it.
- **Secure by default.** Least privilege, no static secrets in CI, signed and verified artifacts, policies on every layer.
- **Cheap now, highly available later.** Everything runs as `single`; switching to `ha` is a configuration change.
- **Compliance tracks.** International (CIS, NIST SSDF, SLSA, OWASP) and Russian (FSTEC orders, GOST R 56939-2024).

!!! info "Primary scenario"
    The guides lead to a cloud deployment (Selectel or any OpenStack). A home Proxmox host is one of the
    providers, not a requirement.

## Where to start

| You want to | Read |
|---|---|
| Understand what the platform is | [Platform overview](platform-overview.md), [Principles](principles.md) |
| Describe a cluster | [Cluster constructor](constructor.md) |
| Deploy the platform | [Deploy everything](deploy-everything.md) |
| Plan addresses and access | [Network](network.md) |
| Review security and compliance | [Security](security.md), [Compliance](compliance.md) |
| Size the hardware or budget | [Capacity](capacity.md) |
| See why things are the way they are | [Decisions](adr/index.md) |
| Work with a single repository | **Repositories** section of this site |

## Repositories

| Repository | Purpose | Status |
|---|---|---|
| [`.github`](https://github.com/sogeor/.github) | Organization profile, community health files | ready |
| [`docs`](https://github.com/sogeor/docs) | This site: cross-cutting pages, ADRs, runbooks | in progress |
| `bootstrap` | Layer 0: hypervisor, cloud accounts, buckets, SOPS/age | planned |
| `workflows` | Reusable GitHub Actions workflows | planned |
| [`images`](https://github.com/sogeor/images) | VM images for every (OS, provider) pair | ready (Ubuntu 24.04 on Proxmox) |
| `modules` | OpenTofu modules, cluster description schema, CAPI generator | planned |
| `management` | External loop: `edge`, `mgmt`, DNS, Cloudflare | planned |
| `platform` | GitOps for all clusters | planned |
| `ansible` | OS, distribution and hardening roles | planned |
| `ci-templates` | GitLab CI templates | planned |
| `charts` | Helm chart `service` | planned |
| `store` | Online store, the reference workload | planned |
| `policies` | Kyverno, Falco, Tetragon, Sigma, Semgrep, Conftest | planned |
| `compliance` | Control matrix, mappings, BDU enrichment | planned |
