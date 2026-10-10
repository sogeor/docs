# 0020 Falco and Tetragon for runtime security

- Status: proposed
- Date: 2026-10-11

## Context and problem statement

Runtime threats must be detected, and some must be blocked.

## Decision drivers

- Detection rules as code.
- Kernel-level enforcement where needed.

## Considered options

1. Falco for detection (profile `core`) and Tetragon for enforcement (profile `security-plus`)
2. Falco only
3. Tetragon only

## Decision outcome

Chosen option: "Falco for detection (profile `core`) and Tetragon for enforcement (profile `security-plus`)".

- Falco with Falcosidekick to Loki and alerts.
- Tetragon policies for high-risk behavior where enforcement is justified.

### Consequences

- Good: broad detection with optional enforcement.
- Bad: two rule languages to maintain.

## Pros and cons of the other options

### Falco only

- Bad: no in-kernel enforcement.

### Tetragon only

- Bad: smaller rule ecosystem.
