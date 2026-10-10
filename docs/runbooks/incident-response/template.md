# Incident response playbook template

Copy this page to `docs/runbooks/incident-response/<threat>.md`, replace every `CHANGE_ME` and add it to
the [playbook table](index.md#playbooks).

## Summary

| Item | Value |
|---|---|
| Threat | CHANGE_ME |
| MITRE ATT&CK | CHANGE_ME: technique ID and name |
| Default severity | CHANGE_ME: SEV1 / SEV2 / SEV3 |
| Detection sources | CHANGE_ME: rule names and log sources |

## Triage

1. CHANGE_ME: how to confirm the alert is a true positive.
2. Open an incident record and assign severity.

## Containment

1. CHANGE_ME: isolate (NetworkPolicy, cordon and drain, revoke token, mesh ACL).

## Eradication

1. CHANGE_ME: remove the cause (rotate secrets in OpenBao, recreate nodes from images).

## Recovery

1. CHANGE_ME: restore service and verify.

## Evidence

- CHANGE_ME: logs and artifacts to preserve before changes, and where to store them.

## Follow-up

- Write a [postmortem](../../postmortems/template.md).
- Add or tune a detection rule with a test.
