# Nix Packaging for Rust Field Guide

This guide is the detailed policy for `nix-packaging`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- A Nix derivation is a declared build function over pinned sources, dependencies, tools, platform, environment, and phases.
- Rust builders differ mainly in dependency vendoring and caching workflow, workspace ergonomics, cross support, and customization surface.
- Fixed-output dependency hashes turn Cargo registry and git resolution into reproducible Nix inputs.
- Cross compilation distinguishes build-platform tools, host-platform build outputs in Nix terminology, and target libraries; Rust also distinguishes proc-macro or build-script host execution.
- Source filters improve cache keys but can silently omit build scripts, assets, migrations, schemas, or nested manifests.
- Package checks, passthru tests, apps, and runtime smoke tests cover different stages from compilation to usable artifact.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Repository already packages Rust | Extend existing builder | Avoids parallel hash and phase conventions |
| Simple single package | buildRustPackage | Native nixpkgs path is usually sufficient |
| Large workspace needing layered caching | Evaluate existing crane or naersk use | Only real build cost justifies extra machinery |
| Cross compile with native deps | Explicit platform-separated inputs | Host tools and target libraries differ |
| Runtime assets required | Install and smoke-test them | Compilation alone misses closure and lookup failures |

## Common Failure Modes

- Switching builders to avoid understanding one hash or source-filter failure.
- Letting Cargo fetch from the network during the sandbox build.
- Putting target libraries in native build inputs or host tools in propagated runtime inputs.
- Filtering source so aggressively that nested manifests, schemas, assets, or build inputs disappear.
- Installing the binary without required shared libraries, data, certificates, migrations, or plugins.

## Required Evidence

- Pinned source, lockfile, dependency hash, builder, features, profile, and platform inputs.
- A clean sandbox build without network or host impurity.
- Checks and installed-artifact inventory tied to package contract.
- Runtime or target smoke evidence plus closure and native-library inspection when applicable.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.
