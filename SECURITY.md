# Security Policy

## Reporting a vulnerability

Do not open a public issue. Use
[Private Vulnerability Reporting](https://github.com/sogeor/docs/security/advisories/new).

Reports are accepted in English or Russian. Initial response within 7 days.
Fix targets: Critical — 7 days, High — 30 days.

## Response process

1. Acknowledge the report within 7 days.
2. Confirm and assess severity (CVSS) privately in a draft security advisory.
3. Fix in a private fork of the advisory; rebuild and republish the site.
4. Publish the advisory and a CHANGELOG entry, crediting the reporter unless they ask for anonymity.
5. Request a CVE through GitHub when applicable.

Fix targets apply from confirmation.

## Scope

- documentation that would lead a reader to an insecure deployment (wrong commands, missing warnings, unsafe defaults);
- leaked secrets or personal values in the repository or on the published site;
- the site build: aggregation scripts, MkDocs configuration, GitHub Actions workflows.

Vulnerabilities in platform components are reported to the repository that owns them
(for example [`sogeor/images`](https://github.com/sogeor/images/security/advisories/new)).
