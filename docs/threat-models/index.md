# Threat models

Threat models of platform components and flows, written with STRIDE per data flow and reviewed when the
architecture changes. Each model follows the [threat model template](template.md).

| Model | Scope | Status |
|---|---|---|
| External loop | GitHub Actions, gitlab.com state, Cloudflare, `edge` | planned |
| Management cluster | Argo CD, Cluster API, OpenBao, Keycloak, Harbor | planned |
| Supply chain | Source → build → sign → registry → admission | planned |
| Mesh and inbound traffic | Headscale, DERP, Cloudflare Tunnel, oauth2-proxy | planned |
| `store` application | Public web, payments, personal data | planned |
