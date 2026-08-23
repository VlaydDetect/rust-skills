# Rust Style and Clippy Field Guide

This guide is the detailed policy for `rust-style-clippy`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Rustfmt provides deterministic formatting under a toolchain and configuration; its output may change between compiler versions.
- Clippy lints range from correctness signals through performance suggestions to subjective style; lint level does not replace context.
- Workspace lint inheritance centralizes policy while package and target scope still determine what is checked.
- `all-targets`, feature selection, target platform, and test or bench code materially change lint coverage.
- Narrow allows preserve global policy better than disabling a lint group for one intentional pattern.
- Baseline separation matters in dirty or legacy repositories so a local task does not claim ownership of unrelated diagnostics.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Pure formatting diff | rustfmt under pinned toolchain | The tool is the repository's canonical formatter |
| Correctness lint with valid premise | Fix root cause | Suppressing would retain a defect |
| Pedantic style lint harms clarity | Narrow allow with reason | Policy should serve maintainability |
| Generated code warning | Exclude or configure generator | Hand edits will be overwritten |
| Toolchain update adds warnings | Review policy and code together | New lint behavior may not imply regressions |

## Common Failure Modes

- Running automatic fixes over unrelated user changes.
- Accepting a Clippy suggestion that raises MSRV or changes public types silently.
- Using crate-wide allows for one localized intentional construct.
- Reporting a full-workspace baseline failure as caused by a narrow change without evidence.
- Treating lint-clean code as proof of correct concurrency, unsafe, API, or behavior.

## Required Evidence

- Exact toolchain, rustfmt and Clippy configuration, command scope, targets, and features.
- A classification for semantic lint changes and reasoned narrow suppressions.
- Diff inspection proving formatting did not rewrite unrelated files.
- Local versus pre-existing failure separation under the repository's declared CI gate.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-style-clippy/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-coding`](./coding.md) — primary; Readable Rust, naming, formatting, Clippy scope, documentation, control flow, API conventions, and reviewable diffs.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
