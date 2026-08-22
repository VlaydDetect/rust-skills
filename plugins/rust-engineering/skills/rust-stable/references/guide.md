# Stable Rust Field Guide

This guide is the detailed policy for `rust-stable`. It synthesizes the full-stack stable Rust specialization and its edition, toolchain, and language references; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- The effective toolchain comes from pin files, CI, environment, and Cargo policy together.
- MSRV means the oldest compiler promised to consumers; it needs both metadata and a real verification job.
- Editions are per-package and interoperable within a dependency graph, so workspace migrations can be staged.
- Nightly feature gates can affect language syntax, library APIs, targets, documentation, and reproducibility.
- Stable alternatives include older APIs, small local implementations, build-time cfg, or an explicit MSRV raise; each has maintenance cost.
- Language advice should preserve clarity around inference, moves, drops, panics, and platform data layout rather than relying on folklore.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Feature is stable within MSRV | Use it directly | The repository already promises the required compiler |
| Feature stabilized after MSRV | Fallback or explicit MSRV decision | Silent adoption breaks supported consumers |
| Nightly-only feature is convenience | Stay stable | Toolchain churn is not justified by shorter syntax |
| Nightly-only feature is product-critical | Pin and isolate it | Contain churn and make the policy explicit |
| Edition migration | Stage per package with migration review | Interoperability allows controlled rollout |

## Common Failure Modes

- Answering with the newest Rust syntax without checking the declared compiler floor.
- Treating edition 2024 as equivalent to a specific minimum rustc without verifying stabilization details.
- Enabling nightly globally for one isolated capability.
- Raising MSRV as an incidental result of a dependency or formatting change.
- Providing generic language guidance when a specialized ownership, traits, unsafe, or Cargo profile controls the decision.

## Required Evidence

- Observed toolchain files, package editions, `rust-version`, CI versions, and any mismatch among them.
- The stabilization or edition requirement for each proposed feature relative to the actual support floor.
- A migration or fallback decision with affected packages and consumer impact.
- Compilation and tests on the declared minimum and primary toolchains when policy changes.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-stable/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.
