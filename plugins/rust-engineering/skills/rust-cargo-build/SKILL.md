---
name: rust-cargo-build
description: Diagnose and design Cargo manifests, targets, features, build scripts, profiles, configuration, metadata, lockfiles, and build commands. Use when Cargo mechanics or effective build state controls the task.
---

# Cargo Build System

Own Cargo's effective package, target, feature, configuration, and build behavior. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A manifest, feature, target, profile, build script, Cargo config, lockfile, or command is being changed or debugged.
- Local and CI Cargo behavior differ because of package selection, target, features, environment, or configuration.
- The task needs the exact build graph rather than source-level architecture.

## Workflow

1. Locate the effective workspace root, package manifests, toolchain, `.cargo/config*`, lockfile, task runner, and CI command.
2. Inspect packages, targets, resolver, workspace inheritance, default members, dependencies, feature edges, target cfg, and profiles.
3. Reproduce with the narrowest exact Cargo invocation, preserving toolchain, package, target, features, environment, and locked or offline flags.
4. Change the owning manifest or config once; avoid compensating flags at every call site unless variability is intentional.
5. Check build-script rerun directives, generated outputs, links metadata, and host-versus-target compilation when applicable.
6. Validate the affected matrix and confirm that lockfile or metadata changes are intentional and reviewable.

## Decision Rules

- Cargo features are additive within a resolved package build and should describe capabilities, not mutually exclusive modes unless enforced.
- Distinguish host dependencies, target dependencies, build dependencies, dev dependencies, and proc-macro execution.
- Use resolver 2 or 3 according to workspace edition and policy; do not assume dev or target features unify the same way under every resolver.
- Build scripts must declare every file and environment input through `rerun-if-changed` or `rerun-if-env-changed`.
- Write generated artifacts to `OUT_DIR`, not the source tree, unless the repository intentionally checks generated code in.
- Preserve lockfile policy: applications commonly commit it; library policies vary and should be explicit.
- Target cfg expressions select dependencies or code; a feature named after a platform is not equivalent.
- Profiles are workspace-root controlled; package-level profile sections do not behave as independent package policy.

## Rulebook Overlay

After resolving effective Cargo state, select relevant build-boundary entries from [`proj-`](../rust-coding-rules/references/categories/proj.md) or measured profile entries from [`opt-`](../rust-coding-rules/references/categories/opt.md). Rulebook settings are not workspace defaults.

## Boundaries and Hand-offs

- `rust-workspace` owns crate boundaries and workspace governance; this profile owns Cargo execution semantics.
- `rust-dependencies` owns dependency policy and `rust-cargo-discovery` does not exist; use `rust-crate-discovery` before adopting a crate.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Cargo Build System field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
