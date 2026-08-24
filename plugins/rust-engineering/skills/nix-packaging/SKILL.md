---
name: nix-packaging
description: Package Rust software with Nix derivations, fixed source and Cargo dependency hashes, native inputs, cross compilation, install phases, tests, outputs, and reproducibility. Use for build artifacts and deployment packages rather than interactive shells.
---

# Nix Packaging for Rust

Own isolated derivations that build, test, and install Rust artifacts reproducibly. Apply this profile directly for focused advice or load it from `rust-workflow` in the role justified by the current decision unit.

## Use This Skill When

- A Rust package needs `buildRustPackage`, crane, naersk, a custom derivation, or flake package output.
- Cargo dependency hashes, native inputs, vendoring, install layout, tests, cross compilation, or reproducibility fail.
- The build works in a dev shell but not in the Nix sandbox or target package.

## Workflow

1. Identify package targets, source filtering, Cargo workspace members, lockfile, features, profile, native dependencies, tests, and installed artifacts.
2. Use the repository's existing Nix Rust builder; choose a different builder only for a demonstrated caching, workspace, or cross-build need.
3. Pin source and dependency inputs with the builder's expected hash model and keep network access out of build phases.
4. Declare native build tools separately from target libraries and account for host, build, and target platforms.
5. Define checks and install phase around actual outputs, preserving licenses, completions, assets, configuration examples, or libraries as required.
6. Build in a clean sandbox, inspect closure and artifacts, then test execution or linkage on the supported target.

## Decision Rules

- Reuse the existing builder and package style before introducing crane, naersk, or custom phase infrastructure.
- Nix builds must not depend on network access, mutable Cargo registries, undeclared environment, or host tools.
- Source filtering must include every manifest, lockfile, build script, generated input, asset, and workspace member needed by the build.
- Changing Cargo dependencies normally changes the fixed dependency hash; update it as an intentional reviewed artifact.
- Separate native build tools from target libraries so cross compilation resolves them for the correct platform.
- Do not disable tests merely because the sandbox exposes an implicit assumption; classify and fix or explicitly justify the unavailable environment.
- Install only intended runtime artifacts and resources rather than copying the whole target directory.
- A successful derivation build is not enough when the artifact needs runtime libraries, plugins, data, or target execution.

## Boundaries and Hand-offs

- `nix-dev-env` owns interactive convenience and extra developer tools.
- `rust-cargo-build` owns Cargo semantics inside the derivation; `nix-flakes` owns exposing the package output.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Nix Packaging for Rust field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
