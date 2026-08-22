# Rust by Example Field Guide

This guide is the detailed policy for `rust-by-example`. It synthesizes the full-stack Rust-by-example golden cases and the specialized language profiles they illustrate; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- A useful Rust example is complete enough to compile, small enough to inspect, and explicit about its observable result.
- Contrast examples can show owned versus borrowed input, static versus dynamic dispatch, or recoverable versus unrecoverable errors.
- Compile-fail examples are valuable when the compiler guarantee is the behavior being taught.
- Edition, MSRV, target, and dependency versions are part of reproducibility.
- Examples should isolate a rule; production code must additionally address logging, cancellation, configuration, security, and integration contracts.
- A minimal example can become a regression fixture only after it is connected to the repository's actual failure path.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Language ownership concept | Std-only executable snippet | Minimizes unrelated setup |
| Compiler prohibition | Labeled compile-fail example | The diagnostic is the observable result |
| External crate API | Minimal Cargo package with pinned requirement | Imports and runtime setup must be reproducible |
| Two valid designs | Side-by-side examples with the same input | A controlled contrast exposes trade-offs |
| Repository bug | First isolate, then add repository regression test | Isolation explains cause; integration proves the fix |

## Common Failure Modes

- Providing a fragment that omits the trait import or runtime attribute required to compile.
- Teaching error handling with unconditional panics without identifying that simplification.
- Adding a large framework to demonstrate a standard-language behavior.
- Claiming performance from a toy example without representative measurement.
- Copying a pattern into production without checking repository MSRV, features, and invariants.

## Required Evidence

- A complete snippet or crate with declared edition, toolchain assumptions, and dependencies.
- Observed compiler result or deterministic output matching the explanation.
- A statement of the one concept proved and the production concerns omitted.
- For contrasts, equivalent inputs and an explanation tied to type or runtime semantics.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-by-example/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.
