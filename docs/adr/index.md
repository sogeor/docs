# Architecture decision records

Platform-wide decisions in [MADR](https://adr.github.io/madr/) format. Decisions that affect a single
repository are recorded in that repository.

| Status | Meaning |
|---|---|
| `proposed` | Drafted, awaiting maintainer review |
| `accepted` | In force |
| `superseded` | Replaced by a later record (linked) |

| Number | Title | Status |
|---|---|---|
| [0001](0001-aggregate-repository-docs-via-ci-copy.md) | Aggregate repository docs via CI copy | proposed |
| [0002](0002-cluster-constructor.md) | Cluster constructor | proposed |
| [0003](0003-talos-for-mgmt.md) | Talos Linux for the management cluster | proposed |
| [0004](0004-capi-and-autoscaling-for-workload-clusters.md) | Cluster API and autoscaling for workload clusters | proposed |
| [0005](0005-single-and-ha-topology.md) | Topology `single` and `ha` | proposed |
| [0006](0006-proxmox-in-hyper-v.md) | Proxmox VE nested in Hyper-V at home | proposed |
| [0007](0007-opentofu-with-state-encryption.md) | OpenTofu with state encryption | proposed |
| [0008](0008-state-on-gitlab-com.md) | OpenTofu state on gitlab.com, portable | proposed |
| [0009](0009-github-as-source-of-truth.md) | GitHub as the source of truth | proposed |
| [0010](0010-github-hosted-runners-with-mesh.md) | GitHub-hosted runners with mesh access | proposed |
| [0011](0011-headscale-mesh-with-amneziawg-fallback.md) | Headscale mesh with an AmneziaWG fallback | proposed |
| [0012](0012-cloudflare-tunnel-for-ingress.md) | Cloudflare Tunnel for inbound traffic | proposed |
| [0013](0013-cilium-and-clustermesh.md) | Cilium with ClusterMesh | proposed |
| [0014](0014-gitlab-in-mgmt.md) | GitLab in the management cluster | proposed |
| [0015](0015-oidc-to-openbao.md) | CI authentication through OIDC to OpenBao | proposed |
| [0016](0016-signing-with-openbao-transit.md) | Artifact signing with OpenBao Transit | proposed |
| [0017](0017-harbor-registry.md) | Harbor as the container registry | proposed |
| [0018](0018-backups-home-and-r2.md) | Backups at home and in Cloudflare R2 | proposed |
| [0019](0019-kyverno-admission.md) | Kyverno for admission control | proposed |
| [0020](0020-falco-and-tetragon.md) | Falco and Tetragon for runtime security | proposed |
| [0021](0021-defectdojo.md) | DefectDojo for vulnerability management | proposed |
| [0022](0022-compliance-tracks.md) | International and Russian compliance tracks | proposed |
