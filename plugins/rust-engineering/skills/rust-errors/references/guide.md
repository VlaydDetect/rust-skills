# Rust Error Design Field Guide

This guide is the detailed policy for `rust-errors`. It synthesizes the craft error design and recovery guides plus full-stack stable, API, observability, and documentation guidance; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- An error taxonomy should correspond to caller actions such as retry, correct input, choose another resource, abort operation, or report a bug.
- `Result` propagates recoverable outcomes; `Option` is appropriate only when absence is the complete information callers need.
- Concrete enums work well for library contracts; context-oriented wrappers or erased reports work well at application composition boundaries.
- `From` conversions should be semantically lossless enough for their layer; overly broad conversions collapse distinct decisions.
- Error context should name the attempted operation and safe identifiers, not restate the lower-level message.
- Recovery includes compensation, fallback, retry, cancellation, and partial-success semantics, all of which need explicit ownership.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Public library boundary | Stable typed enum or structured type | Callers need matchable recovery categories |
| Application top level | Context-rich erased report | Composition matters more than downstream matching |
| Expected absence | Option | No additional cause or recovery category is needed |
| Invalid external input | Recoverable validation error | The caller can correct or reject the request |
| Impossible internal state | Invariant error or panic by policy | Distinguish bugs from routine operations |

## Common Failure Modes

- Using strings as the only error contract and forcing callers to parse display text.
- Logging an error at every propagation layer and producing duplicate noisy events.
- Hiding the original source or backtrace when adding high-level context.
- Retrying all errors, including invalid input, cancellation, permission denial, or non-idempotent operations.
- Publishing dependency error types and unintentionally coupling SemVer to that dependency.

## Required Evidence

- A failure taxonomy mapped to caller action, retryability, reporting, and redaction.
- Tests for important variants, causal chains, conversions, and negative recovery behavior.
- Public compatibility analysis for exported errors and non-exhaustive policy.
- A clear ownership boundary for logging so propagation does not duplicate telemetry.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.
