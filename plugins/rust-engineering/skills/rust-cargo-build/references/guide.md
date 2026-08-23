# Cargo Build System Field Guide

This guide is the detailed policy for `rust-cargo-build`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Effective Cargo state combines manifests, workspace inheritance, config, environment, command flags, toolchain, target, and lockfile.
- Targets include libraries, binaries, examples, tests, benches, build scripts, and proc macros, each with different compilation roles.
- Features propagate along dependency feature edges and are unified for a package within the selected graph under resolver rules.
- Cross compilation builds build scripts and proc macros for the host while compiling normal dependencies for the target.
- `cargo metadata` and `cargo tree` expose resolved graph views, but source cfg and build-script behavior can still refine what executes.
- Reproducibility depends on locked resolution, registry or git sources, toolchain, config, environment, and native build inputs.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| One affected package | `-p` or manifest-scoped command | Keeps diagnosis and evidence narrow |
| Feature-specific behavior | Explicit no-default and feature matrix | Defaults alone do not prove optional configurations |
| Cross target | Separate host and target reasoning | Build scripts and proc macros execute on the host |
| Generated native bindings | Build script with declared inputs and OUT_DIR | Supports deterministic rebuilds |
| Release reproduction | Locked toolchain, resolution, target, and profile | Unqualified `cargo build` is incomplete evidence |

## Common Failure Modes

- Adding a feature flag to hide mutually exclusive global modes without compile-time conflict handling.
- Forgetting that root configuration and profiles control member builds.
- Using a build script that scans undeclared files or performs network access.
- Updating Cargo.lock incidentally while diagnosing an unrelated source failure.
- Claiming a target works because dependencies resolve without compiling the actual target and native inputs.

## Required Evidence

- The exact effective Cargo command and relevant manifest, config, toolchain, target, and environment inputs.
- Resolved package and feature edges for any graph-related conclusion.
- Intentional lockfile and metadata diffs separated from source changes.
- Targeted checks for affected targets, feature combinations, build scripts, and cross host or target roles.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-cargo-build/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.
