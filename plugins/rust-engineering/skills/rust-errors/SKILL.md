---
name: rust-errors
description: Design Rust error boundaries, types, context, recovery, propagation, panic policy, diagnostics, and application or library reporting. Use when failure semantics and caller action are the primary concern.
---

# Rust Error Design

Own recoverable failure contracts from low-level cause to caller action and final reporting. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A library or application needs error types, variants, context, conversion, retry, or diagnostic policy.
- Existing `unwrap`, boxed error, string error, or broad conversion hides actionable failure distinctions.
- A boundary must decide which failures are recoverable, retryable, user-facing, or invariant violations.

## Workflow

1. List failure modes at the boundary and the actions callers can reasonably take for each.
2. Separate domain failures, input rejection, transient infrastructure, cancellation, programmer bugs, and violated invariants.
3. Choose a typed or erased representation based on library stability and application composition needs.
4. Add context at ownership boundaries without duplicating or discarding the causal source chain.
5. Define conversion, redaction, retry, logging, status, and panic policy at the correct layer.
6. Test variant classification, sources, display constraints, and recovery paths rather than only success.

## Decision Rules

- Library errors should expose stable actionable categories without leaking private dependency types accidentally.
- Applications may erase heterogeneous internal errors near the top, but domain decisions should remain typed until then.
- Panic only for violated internal invariants or explicitly unrecoverable startup policy, not routine input or I/O failure.
- Preserve `source()` chains when wrapping causes; avoid converting everything to strings early.
- Error display is for humans, variants or structured fields are for program decisions.
- Classify cancellation separately from failure when callers need to suppress retries or user alarms.
- Retry policy needs idempotency, bounds, backoff, and error classification; an error type alone does not make retries safe.
- Redact secrets, credentials, raw payloads, and sensitive paths before errors cross trust boundaries.

## Rulebook Overlay

After defining caller actions and failure boundaries, select only relevant IDs from the [`err-` index](../rust-coding-rules/references/categories/err.md). Dependency-specific rules remain conditional and do not replace this profile's taxonomy.

## Boundaries and Hand-offs

- `rust-observability` owns when and where errors are logged or emitted as telemetry.
- `rust-api-design` and `rust-semver` own public compatibility of exported error types and variants.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Error Design field guide](references/guide.md) before making a consequential design choice. Use the [Actionbook error protocol](references/actionbook-index.md) when failure must be traced across mechanical, API, and domain layers. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.

## Huiali protocols

For source-derived detail relevant to this profile, read the [Huiali integration index](references/huiali-index.md) and load only the matching family reference.
