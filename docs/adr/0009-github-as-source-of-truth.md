# 0009 GitHub as the source of truth

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

Code is public and needs community features, while the internal CI runs GitLab.

## Decision drivers

- Public visibility and contributions.
- One place for reviews.

## Considered options

1. All code on GitHub; internal loop repositories mirrored to GitLab
2. GitLab only
3. Both as equals

## Decision outcome

Chosen option: "All code on GitHub; internal loop repositories mirrored to GitLab".

- Pull requests, reviews and releases happen on GitHub.
- Mirroring to GitLab is one-way, by a reusable workflow.

### Consequences

- Good: one review flow.
- Bad: GitLab pipelines report status back to GitHub through an integration.

## Pros and cons of the other options

### GitLab only

- Bad: smaller open-source audience; GitLab in `mgmt` is not public.

### Both as equals

- Bad: split reviews and drift.
