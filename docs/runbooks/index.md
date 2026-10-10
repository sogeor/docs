# Runbooks

Platform-wide operational procedures that span several repositories. Procedures that concern one
repository live in that repository's `docs/operations.md`.

Every runbook follows the [runbook template](template.md): goal, prerequisites, numbered steps with exact
commands, expected result, verification, rollback.

| Runbook | Trigger | Status |
|---|---|---|
| Tear down and recreate a workload cluster | Cost saving, recovery | planned |
| Recover `mgmt` from Git and backups | Loss of the management cluster | planned |
| Tear down and recreate the whole platform | Full rebuild | planned |
| Unseal OpenBao | OpenBao restart | planned |
| Rotate external loop credentials | Schedule, suspected leak | planned |
| Monthly restore test | Schedule | planned |
| Migrate OpenTofu state to S3 | Leaving gitlab.com | planned |
| Move a cluster from `single` to `ha` | Growth | planned |

## Incident response

See [Incident response](incident-response/index.md).
