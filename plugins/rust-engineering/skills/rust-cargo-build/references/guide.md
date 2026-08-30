# Cargo Build System Field Guide

This guide is the detailed policy for `rust-cargo-build`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Effective Cargo state combines manifests, workspace inheritance, config, environment, command flags, toolchain, target, and lockfile.
- Targets include libraries, binaries, examples, tests, benches, build scripts, and proc macros, each with different compilation roles.
- Features propagate along dependency feature edges and are unified for a package within the selected graph under resolver rules.
- Cross compilation builds build scripts and proc macros for the host while compiling normal dependencies for the target.
- `cargo metadata` and `cargo tree` expose resolved graph views, but source cfg and build-script behavior can still refine what executes.
- Reproducibility depends on locked resolution, registry or git sources, toolchain, config, environment, and native build inputs.

## Profiling Profile Contract

When a profiler needs release-like optimization plus readable symbols, define the custom profile once at the workspace root:

```toml
[profile.profiling]
inherits = "release"
debug = true
strip = "none"
```

- Build or benchmark with `--profile profiling` and resolve the output path from effective Cargo metadata/command output. A custom target directory means `target/profiling` is not a safe assumption.
- Keep this profile observational: do not add LTO, `panic = "abort"`, `codegen-units = 1`, target CPU flags, or an allocator. Each changes the workload and requires a separate measured experiment.
- Custom profiles require `inherits` and are workspace-root policy; do not place the profile in a member manifest or a global Cargo config.
- Frame pointers are a tool/target-specific codegen input, not a Cargo profile key. Apply `-C force-frame-pointers=yes` only to the scoped profiling command when required and record the flag.
- Do not compare Criterion baselines built with different profiles, targets, features, flags, allocators, or toolchains.

See the [Rust profiling protocol](../../rust-performance/references/low-level/rust-profiling.md) for profiler selection and the [Cargo profile reference](https://doc.rust-lang.org/cargo/reference/profiles.html) for current semantics.

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
