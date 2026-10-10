# Principles

Every decision on the platform must satisfy these principles. A change that breaks one needs an ADR.

| Principle | In practice |
|---|---|
| **Minimum cost now, HA later** | Everything works in topology `single` (one node, one replica). Moving to `ha` is a configuration change, not a rewrite. |
| **Constructor** | A cluster is assembled from independent axes: distribution, pool OS, provider, size, topology, profiles. A new combination is a new description file. |
| **Provider neutrality** | Nothing above the node-creation layer knows the provider; it works with the [normalized node](constructor.md#normalized-node). |
| **Everything as code, GitOps** | State lives in Git; Argo CD converges clusters to it. Manual actions are limited to bootstrap and secrets, and they are documented. |
| **Self-healing** | Nodes are cattle: recreated from their description. Data is restored from backups automatically. A cluster can be torn down and recreated in one operation. |
| **Pay-as-you-go** | Cloud workload clusters scale automatically, down to zero worker nodes, and are torn down when not needed. |
| **Secure by default** | Least privilege, no static secrets in CI, verified signatures and hashes, policies on every layer. |
| **No personal values in code** | Addresses, domains, project IDs and host names are variables with `*.example` files. The reference must deploy for anyone. |
| **Cloud first for adopters** | Guides lead to a cloud deployment. A home Proxmox host is one provider among others. |
| **Latest stable versions and choice** | Several supported OS versions are available; new LTS releases are added, old ones removed only after end of support. |
| **Documentation is part of the product** | Every repository is documented from "what is this" to every option and every action. |

## Rules derived from the principles

- Versions are pinned exactly: providers, plugins, charts, images and actions (actions by full SHA). No `latest`.
- No `curl | bash` without a checksum.
- Secrets never reach Git in any form; examples use `CHANGE_ME`.
- Every component declares `requests/limits` and supports both topologies.
- Every manual step is written down: generic instructions in the repository's `docs/setup.md`.

## Repository conventions

| Topic | Convention |
|---|---|
| Language | Everything in repositories is in English |
| Default branch | `master`, protected by a ruleset (signed commits, pull requests, required checks) |
| Commits | Conventional Commits, squash merge |
| Versions | SemVer tags `vX.Y.Z` (`modules-vX.Y.Z`, `roles-vX.Y.Z` where several artifacts share a repository) |
| Decisions | MADR records in `docs/adr/` |
| Dependencies | Renovate, never auto-merged |
| License | Apache-2.0 |
