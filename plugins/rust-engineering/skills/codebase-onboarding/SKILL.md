---
name: codebase-onboarding
description: Build an evidence-backed map of an unfamiliar Rust repository, its purpose, packages, entry points, boundaries, commands, and risks. Use before consequential work in an unknown codebase or when repository topology is unclear.
---

# Codebase Onboarding

Own first-pass understanding of an unfamiliar repository without changing it. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- The repository is new to the agent or the requested area has not been inspected.
- Package ownership, runtime entry points, data flow, or repository-native commands are unclear.
- The user asks for an architectural tour, onboarding guide, or impact map before implementation.

## Workflow

1. Read path-scoped instructions and dirty state, then identify the workspace root without assuming the current directory is it.
2. Inventory manifests, members, targets, toolchain files, task runners, CI, documentation, examples, tests, and generated-code boundaries.
3. Trace one representative path from public or executable entry point through core logic to I/O, persistence, or external adapters.
4. Map package and module responsibilities, dependency direction, feature and target gates, and the owners of public contracts.
5. Run only cheap read-only discovery commands already supported by the repository; record unknowns instead of installing tools.
6. Return a concise project map, safe starting commands, likely change surfaces, and questions whose answers materially affect the task.

## Decision Rules

- Treat effective Cargo metadata and opened source as stronger evidence than stale prose.
- Separate workspace packages, in-crate modules, runtime processes, and deployment artifacts; they are different maps.
- Do not read the entire tree linearly; follow entry points and dependency edges first.
- Name generated, vendored, fixture, and build-output directories so later agents do not edit them accidentally.
- Record repository-native commands exactly, including package, feature, target, and toolchain qualifiers.
- Distinguish observed facts, reasonable inferences, and unresolved questions.
- If documentation disagrees with code, report the conflict and its likely freshness rather than choosing silently.
- Stop discovery when the task's affected path and evidence requirements are clear; onboarding is not an exhaustive audit.

## Boundaries and Hand-offs

- `rust-navigation` owns fast symbol and call-path lookup after the initial project map exists.
- `rust-architecture-review` owns judging structural quality; onboarding describes structure without grading it.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Codebase Onboarding field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
