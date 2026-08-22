# Rust Documentation Field Guide

This guide is the detailed policy for `rust-documentation`. It synthesizes the full-stack documentation skill and its rustdoc, doctest, README, example, changelog, and migration references; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- Crate-level docs answer why the crate exists, how to start, which features and targets matter, and where to go next.
- Module docs explain responsibility and relationships; item docs explain contract, inputs, outputs, failures, invariants, and examples.
- Doctests are both documentation and tests, with feature, target, and environment limitations that must be understood.
- Intra-doc links preserve navigability through refactors better than raw paths when used correctly.
- Examples establish expected ergonomics and can reveal API design problems before prose does.
- Documentation debt is a correctness issue when users make unsafe, incompatible, or operationally wrong choices from stale claims.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Common public API | Runnable doctest | Keeps the main path accurate |
| Complex integration | Example crate or examples target | Supports setup beyond a compact item doc |
| Compiler rejection is the lesson | Compile-fail doctest | The diagnostic contract is intentional |
| Environment or network required | No-run example plus explicit prerequisites | Avoids false deterministic tests |
| Breaking migration | Dedicated guide with old and new calls | Users need actionable transition steps |

## Common Failure Modes

- Examples that compile only because hidden setup contradicts the visible code.
- Listing APIs without explaining ownership, errors, safety, blocking, or lifecycle.
- Duplicating feature or compatibility tables across files until they drift.
- Using `ignore` for doctests simply to make failures disappear.
- Documenting intended future behavior as if the current release implements it.

## Required Evidence

- Successful rustdoc link checking and doctests for intended feature or target configurations.
- A reader path from crate overview to a working common example and detailed contract sections.
- Safety, errors, panics, cancellation, blocking, and feature requirements where applicable.
- Synchronization of README, crate docs, examples, changelog, and migration material for changed user contracts.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-documentation/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.
