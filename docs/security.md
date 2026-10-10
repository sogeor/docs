# Security

Security is a default, not a profile. This page summarizes what the platform guarantees on each layer;
threat models and incident response live in their own sections.

## Supply chain

Target: SLSA Build Level 3 where the tooling allows it.

- Ephemeral isolated jobs; provenance (in-toto/SLSA), SBOM (CycloneDX), scan results and VEX (OpenVEX) for container images, charts and, later, VM images.
- Signing with Cosign using a key in OpenBao Transit (`hashivault://`); GitHub artifact attestations for public artifacts.
- Kyverno `verifyImages` at admission: signature, provenance, SBOM, registry allowlist, digest.
- Harbor: proxy cache, built-in Trivy, blocks unsigned or vulnerable images.
- Dependency-Track: SBOM inventory, license and vulnerability policies.
- Renovate in every repository; OpenSSF Scorecard; signed commits; actions pinned by SHA; `zizmor`, `actionlint`, minimal `permissions`, `persist-credentials: false`.

## Policy as code

| Layer | Tool |
|---|---|
| IaC, static | Checkov, Trivy config, tflint |
| IaC, plan | Conftest/OPA on `tofu show -json` |
| Cluster descriptions | JSON Schema + Conftest (constructor validations) |
| Operating system | OpenSCAP (CIS), goss |
| Kubernetes admission | Kyverno (Audit → Enforce), Pod Security Admission `restricted` |
| Kubernetes posture | kube-bench, kubescape, Trivy Operator |
| Runtime | Falco + Falcosidekick, Tetragon |
| Network | Cilium NetworkPolicy default deny, FQDN egress |
| Code | Semgrep, gitleaks |

## Secrets and identities

- **OpenBao** in `mgmt`: KV v2, dynamic database credentials, PKI, Transit (Cosign, state encryption of the internal loop), SSH CA. Unseal with Shamir 3 of 5; keys are held by people. Cloud KMS auto-unseal is considered when moving to `ha`.
- **CI without static secrets:** GitLab `id_tokens` → OpenBao JWT; GitHub Actions → cloud OIDC where supported, otherwise Environment secrets restricted to `master`.
- External Secrets Operator authenticates to OpenBao with Kubernetes auth; database credentials are short-lived.
- Keycloak is the single sign-on for Argo CD, Grafana, GitLab, Harbor, OpenBao, the Kubernetes API (OIDC) and oauth2-proxy.
- OpenTofu state is encrypted: `pbkdf2` in the external loop, OpenBao Transit in the internal loop.
- Kubernetes Secrets are encrypted at rest in etcd; Talos disks are encrypted.

| Secret | Where | How it is delivered |
|---|---|---|
| Tokens for the external loop (hypervisor, clouds, Cloudflare, state backend) | GitHub Environments | job environment variables |
| State encryption passphrase | GitHub Environments + the operator's password manager | `TF_VAR_state_passphrase` |
| Provider credentials for CAPI | OpenBao → ESO → Secret in `mgmt` | rotated in OpenBao |
| Internal loop tokens | OpenBao (dynamic where possible) | OIDC → OpenBao |
| Cosign key | OpenBao Transit (non-exportable) | `hashivault://` |
| SSH | OpenBao SSH CA; a static key only for bootstrap | certificate per job or person |
| Talos machine secrets, talosconfig | encrypted state + copy in OpenBao | `siderolabs/talos` / CAPI |
| Break-glass kubeconfig | OpenBao | manual, audited |
| Application secrets | OpenBao → ESO | `ExternalSecret` |
| Bootstrap secrets before OpenBao | SOPS + age | `sops -d` |
| OpenBao unseal keys | key holders only | runbook |

## Human access

- SSH: OpenBao SSH CA certificates valid for at most 8 hours.
- Kubernetes API: OIDC, RBAC by group; break-glass kubeconfig only in OpenBao, with an alert on use.
- Network: Tailscale ACLs. Web: oauth2-proxy.
- Every action is logged.

## Detection and response

Sources: Kubernetes audit log, Falco, Tetragon, auditd, OpenBao, GitLab, Headscale, CrowdSec, oauth2-proxy,
cloudflared → Loki (Wazuh optional). Detection as code (Falco, Sigma) with tests and MITRE ATT&CK mapping.
Incident response runbooks, exercises and postmortems. Russian track: integration point for KUMA or
MaxPatrol SIEM over Syslog CEF.

## Vulnerability management

- DefectDojo aggregates Semgrep, gitleaks, Trivy, Grype, Checkov, ZAP, kube-bench, kubescape and OpenSCAP findings.
- SLA: Critical — 7 days, High — 30 days.
- Findings are enriched with the FSTEC vulnerability database (BDU).
- Images are rebuilt monthly.

## Application testing

SAST (Semgrep), gitleaks, SCA (Trivy/Grype + Dependency-Track), IaC (Checkov), containers (Trivy, hadolint),
DAST (ZAP), API fuzzing (Schemathesis), fuzzing (Jazzer), Spectral (OWASP ruleset). Templates for Russian
commercial tools are provided and disabled by default.
