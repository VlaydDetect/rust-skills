# Rust Workspaces Field Guide

This guide is the detailed policy for `rust-workspace`. It synthesizes the full-stack workspace skill and its topology, manifest, dependency, publishing, and migration references; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- A workspace shares a lockfile, target directory, root configuration, profiles, and optional inherited package or dependency metadata.
- Crates are compilation, visibility, feature, dependency, and release units; modules are cheaper namespace and privacy units.
- Package names, crate names, public paths, and filesystem paths can differ and all may affect migrations.
- Workspace dependencies simplify version alignment but do not replace dependency ownership or feature discipline.
- Default members affect unqualified root commands and therefore developer and CI behavior.
- Published path dependencies need version requirements and release sequencing that local workspace builds may not reveal.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Only privacy or navigation changes | Module boundary | Avoids new package and release cost |
| Independent target or platform | Separate crate | Cargo can select and compile the boundary independently |
| Unsafe subsystem | Potential narrow crate | A crate can concentrate audit and safe public surface |
| One implementation used once | Keep in owner crate | A utilities crate would obscure responsibility |
| Published packages evolve together | Explicit release group and requirements | Local path resolution can hide registry constraints |

## Common Failure Modes

- Creating `common`, `core`, or `utils` crates that become dependency magnets without a cohesive domain.
- Splitting a crate to improve folder size while increasing public API and release coordination.
- Centralizing dependency declarations and assuming feature behavior is now uniform.
- Testing only the workspace root and missing packages excluded from default members.
- Moving a package without updating CI paths, docs, publish metadata, examples, and lockfile consumers.

## Required Evidence

- A current and proposed package graph with responsibility and dependency direction.
- The concrete boundary benefit and added build, API, feature, and release costs.
- Migration coverage for package names, paths, public re-exports, CI, docs, and publication.
- Independent and consumer compilation for affected packages across required configurations.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-workspace/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.
