# 0021 DefectDojo for vulnerability management

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

Findings come from many scanners; they must be deduplicated, tracked against SLAs and enriched.

## Decision drivers

- One place for all findings.
- SLA tracking.
- Open source.

## Considered options

1. DefectDojo with Dependency-Track for SBOM
2. Scanner reports in CI only
3. GitHub code scanning only

## Decision outcome

Chosen option: "DefectDojo with Dependency-Track for SBOM".

- DefectDojo (profile `security-plus`) ingests Semgrep, gitleaks, Trivy, Grype, Checkov, ZAP, kube-bench, kubescape and OpenSCAP.
- SLA: Critical 7 days, High 30 days; enrichment with the FSTEC vulnerability database.

### Consequences

- Good: one view of risk.
- Bad: heavy; runs on demand or in the cloud.

## Pros and cons of the other options

### Scanner reports in CI only

- Bad: no deduplication or SLA tracking.

### GitHub code scanning only

- Bad: covers only GitHub-side scanners.
