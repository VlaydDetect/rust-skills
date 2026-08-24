---
name: rust-workspace
description: Design and maintain Rust workspace package boundaries, shared metadata, dependency inheritance, resolver policy, release groups, and repository topology. Use when the unit of change is crates and their relationships rather than modules within one crate.
---

# Rust Workspaces

Own workspace-level crate responsibilities, dependency direction, shared policy, and multi-package evolution. Apply this profile directly for focused advice or load it from `rust-workflow` in the role justified by the current decision unit.

## Use This Skill When

- A crate is being added, split, merged, moved, published, or made private within a workspace.
- Workspace dependency inheritance, default members, resolver, profiles, metadata, or shared lints need policy.
- Package boundaries produce cycles, excessive rebuilds, unclear ownership, or difficult release coordination.

## Workflow

1. Map workspace root, members, exclusions, default members, package targets, publish status, dependency edges, and release coupling.
2. Name each crate's responsibility and the concrete ownership, reuse, compilation, platform, or release reason for its boundary.
3. Check dependency direction, feature forwarding, public re-exports, workspace inheritance, and build or proc-macro host roles.
4. Choose the smallest topology change that improves a demonstrated boundary without creating a speculative framework crate.
5. Plan path, package-name, feature, API, documentation, CI, lockfile, and release migrations together.
6. Validate affected packages independently and through workspace consumers under relevant features and targets.

## Decision Rules

- Create a crate boundary for independent ownership, reuse, release, target, unsafe containment, proc-macro, or build isolation—not merely file count.
- Keep dependency direction aligned with semantic layers and avoid cyclic concepts even when Cargo prevents literal package cycles.
- Use `[workspace.dependencies]` to centralize compatible requirements, not to make every member depend on every shared crate.
- Forward features deliberately and document whether a root feature changes public behavior or only composition.
- Private workspace crates still have internal compatibility and build-cost consequences.
- Proc-macro crates, build helpers, and xtask tools should remain narrow because they compile or execute in special contexts.
- A workspace root may be virtual; never assume it has a root package target.
- Coordinate published crate versions and dependency requirements when public packages evolve together.

## Rulebook Overlay

After mapping package responsibilities and dependency direction, select only relevant workspace IDs from the [`proj-` index](../rust-coding-rules/references/categories/proj.md). Module-level entries remain owned by `rust-module-layout`.

## Boundaries and Hand-offs

- `rust-module-layout` owns organization inside one crate; use a crate boundary only when workspace-level costs and benefits justify it.
- `rust-cargo-build` owns command, feature-resolution, config, and build-script mechanics.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Workspaces field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
