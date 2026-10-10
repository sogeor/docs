# Cluster constructor

A cluster is described by one YAML file. Two mechanisms (Cluster API and OpenTofu) accept the same
description and produce the same node contract.

```text
cluster   = distribution + kubernetes_version + topology + profiles + network
node pool = role + os + provider + size + (count | autoscale) + labels + taints
```

The distribution is set **per cluster** (nodes join with the control plane's tooling). The OS is set
**per pool**: kubeadm and k3s clusters may mix pools on different operating systems.

## Cluster description

```yaml
cluster: main                    # unique name
cluster_id: 2                    # 1–24, defines CIDRs (see Network)
distribution: kubeadm            # talos | kubeadm | k3s
kubernetes_version: "1.37.1"
topology: single                 # single | ha
profiles: [core, data]
mechanism: capi                  # capi | opentofu (default depends on the control plane provider)
allow_experimental: false
pools:
  cp:
    role: control-plane
    os: ubuntu-2404              # ubuntu-2404 | ubuntu-2604 | astra-18 | alpine | talos
    provider: selectel           # proxmox | selectel | vkcloud | yandex | timeweb | byo
    site: selectel-ru-9
    size: m
    count: 1
  workers:
    role: worker
    os: ubuntu-2404
    provider: selectel
    site: selectel-ru-9
    size: l
    autoscale: { min: 0, max: 3 }
    labels: {}
    taints: []
```

The JSON Schema lives in the `modules` repository (`schemas/cluster.schema.json`).

## Distributions

| `distribution` | Allowed pool OS | Bootstrap via CAPI | Bootstrap via OpenTofu | Status |
|---|---|---|---|---|
| `talos` | `talos` | Talos bootstrap and control plane providers | `siderolabs/talos` | stable |
| `kubeadm` | `ubuntu-2404`, `ubuntu-2604`, `astra-18`, `alpine` | kubeadm bootstrap and control plane | OpenTofu + Ansible (`k8s_kubeadm`) | stable |
| `k3s` | `ubuntu-2404`, `ubuntu-2604`, `astra-18`, `alpine` | k3s bootstrap and control plane (community) | OpenTofu + Ansible (`k8s_k3s`) | stable (community CAPI provider) |

## Operating systems

| `os` | Version | Status | Image | Notes |
|---|---|---|---|---|
| `ubuntu-2404` | Ubuntu Server 24.04 LTS | stable | `images` | Current reference |
| `ubuntu-2604` | Ubuntu Server 26.04 LTS | planned | `images` | Stable after verification; CIS report uses the nearest profile until SCAP Security Guide ships one |
| `astra-18` | Astra Linux SE 1.8 | planned | `images` (ISO supplied manually) | Russian track; in a cloud only if the provider offers an image |
| `alpine` | Alpine Linux, current stable 3.x | experimental | `images` | musl/OpenRC, no official Kubernetes support |
| `talos` | Talos Linux | stable | Talos Image Factory | No SSH, API only |

Several LTS releases are supported at the same time. A new LTS is a separate image (`ubuntu-2604-*`); the
old one is removed only after its standard support ends. Every (OS, provider) pair is a separate image.

## Providers

| `provider` | Mechanism | Autoscaling | Status |
|---|---|---|---|
| `proxmox` | OpenTofu (`bpg/proxmox`) for `mgmt`; CAPI (CAPMOX) for workload clusters | via CAPI | first |
| `selectel` | CAPI (CAPO, OpenStack) + OpenTofu for networks and projects | yes | primary cloud |
| `vkcloud` | CAPI (CAPO, OpenStack) | yes | later |
| `yandex` | CAPI (Yandex provider, maturity to be verified) or OpenTofu | yes / no | later |
| `timeweb` | OpenTofu | no | later |
| `byo` | OpenTofu (registration) + Ansible | no | existing servers over SSH |

A provider module appears together with its implementation; empty modules are not created.

## Two mechanisms, one interface

| Mechanism | When | What it creates |
|---|---|---|
| **Cluster API** (from `mgmt`) | Provider has an API and a CAPI provider | `Cluster`, `*ControlPlane`, `MachineDeployment`, `MachineHealthCheck`, Cluster Autoscaler annotations (min/max) |
| **OpenTofu + Ansible / Talos provider** | `mgmt` (the first cluster), `edge`, `byo`, providers without CAPI | VMs or node registration → inventory → Ansible roles or Talos machine config |

Manifests for CAPI are generated in `modules` and applied by Argo CD in `mgmt`.

## Topology

Every platform component and every CAPI template supports both values.

| Item | `single` | `ha` |
|---|---|---|
| Control plane nodes | 1 (pods allowed on the control plane) | 3 |
| Deployment / StatefulSet replicas | 1 | 2–3 |
| Anti-affinity | `preferred` only | `required` across nodes/zones |
| PodDisruptionBudget | not created (it blocks draining the only node) | `minAvailable: 1` |
| CloudNativePG | `instances: 1` | 3 |
| OpenBao | Raft, 1 node | Raft, 3 nodes |
| Storage | local-path (node disk) | cloud CSI or Longhorn (3 replicas) |
| GitLab | 1 replica each, external PostgreSQL/Redis/object storage | HPA, replicas |

## Sizes

| Size | vCPU | RAM | Disk |
|---|---|---|---|
| `xs` | 1 | 1 GB | 20 GB |
| `s` | 2 | 2 GB | 30 GB |
| `m` | 2 | 4 GB | 40 GB |
| `l` | 4 | 8 GB | 80 GB |
| `xl` | 8 | 16 GB | 160 GB |
| `2xl` | 8 | 32 GB | 200 GB |

Each provider module maps a size to its own flavor, preset or cores/memory.

## Validations

Checked before any resource is created:

- the pool OS is allowed for the cluster distribution, and an image exists for the (OS, provider) pair;
- all `control-plane` pools of a cluster are within 10 ms of each other (one `site` by default; multi-site needs an explicit flag);
- `topology: ha` requires an odd number of control plane nodes, at least 3;
- `talos` on `byo` only with `custom_image_supported: true`;
- `astra-18` in a cloud only if the provider offers an image;
- `alpine` only with `allow_experimental: true`;
- `autoscale.max` is always set (budget protection).

## Normalized node

Every mechanism outputs nodes in this shape; everything above it is provider-neutral.

```hcl
{
  name          = string        # hostname, unique in the organization
  fqdn          = string        # <name>.<internal-domain>
  cluster       = string
  distribution  = string        # talos | kubeadm | k3s
  role          = string        # control-plane | worker | edge | db | lb
  pool          = string
  provider      = string
  site          = string
  os            = string
  private_ip    = string
  public_ip     = string        # or null
  ssh_user      = string        # null for talos
  labels        = map(string)   # including topology.kubernetes.io/region|zone
  taints        = list(string)
  mesh_required = bool          # site is not the home site
}
```

## Inventory

Ansible inventory is produced with `ansible_host`/`ansible_group` resources of the `ansible/ansible`
provider and read by the `cloud.terraform.terraform_provider` plugin. Groups: `cluster_<name>`,
`distribution_<d>`, `role_<role>`, `site_<site>`, `os_<os>`, `mesh`, `internet`. Talos nodes are not
part of the inventory.

## Images

- Name: `<os>-<kind>-v<build>` (for example `ubuntu-2404-k8s-v20-1`).
- Proxmox tags: `packer;<os>;<kind>;[k8s-<major>-<minor>;]v<build>`; in clouds, image properties with the same values and the family `sogeor-<os>-<kind>`.
- The newest image is selected by tags or family; existing nodes are replaced by rolling replacement, not recreated in place.
- Talos: Image Factory schematic ID and version are input variables.

## Component profiles

| Profile | Components | When |
|---|---|---|
| `core` | Cilium, ingress-nginx, cert-manager, ESO, Kyverno, Falco, VictoriaMetrics, Grafana, Loki, Vector, local-path/CSI, Velero; in `mgmt` also Argo CD, CAPI, OpenBao, Keycloak, Harbor, SeaweedFS | always |
| `ci` | GitLab, GitLab Runner | `mgmt` |
| `data` | CloudNativePG, Strimzi | workload clusters running `store` |
| `security-plus` | DefectDojo, Dependency-Track, Tetragon, Trivy Operator, Wazuh | on demand |
| `observability-plus` | Tempo, OpenTelemetry Collector, Sloth, Hubble UI | on demand |
| `chaos` | Chaos Mesh | during experiments |
| `ru-track` | GOST TLS demo, integration stubs | optional |
