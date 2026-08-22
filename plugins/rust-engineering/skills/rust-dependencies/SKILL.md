---
name: rust-dependencies
description: Govern adopted Rust dependencies, versions, features, sources, duplication, security, licensing, updates, and removal. Use after a crate is selected or when an existing dependency graph needs policy and maintenance.
---

# Rust Dependency Governance

Own the lifecycle and risk of dependencies already in or approved for the project. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- An existing dependency needs an update, feature change, source change, deduplication, audit, license review, or removal.
- The graph contains unexpected versions, default features, native build inputs, git sources, or security advisories.
- Workspace policy must distinguish runtime, build, dev, optional, target, and public dependencies.

## Workflow

1. Identify the owning package and why the dependency exists, including which code path and configuration requires it.
2. Inspect resolved versions, reverse dependencies, feature edges, source, lockfile, target conditions, build scripts, licenses, and advisory evidence.
3. Classify public API exposure, runtime or build criticality, native or proc-macro code, maintenance risk, and replacement cost.
4. Choose the smallest policy change: disable defaults, narrow features, align versions, update, pin with reason, replace, or remove.
5. Review lockfile and transitive diffs separately from manifest intent; avoid opportunistic graph churn.
6. Validate affected feature and target configurations and record security or license evidence with dates and tool limitations.

## Decision Rules

- Do not add a dependency until `rust-crate-discovery` establishes need and suitability.
- Default features are part of the dependency request and should be inspected rather than accepted blindly.
- Avoid exact pins unless reproducibility or a known regression requires them and an update trigger is documented.
- Git dependencies need immutable revisions and an explicit supply or release rationale.
- A dependency exposed in public types can become a SemVer and version-coordination obligation.
- Duplicate versions are not automatically defects; act when cost, types, native linking, security, or build time is concrete.
- Security audit output is time-bound evidence and may be unavailable offline; never present it as timeless proof.
- Remove unused features and dependencies only after checking build scripts, cfg, examples, benches, docs, and generated paths.

## Boundaries and Hand-offs

- `rust-crate-discovery` owns evaluating a crate before adoption; this profile begins once a dependency exists or is approved.
- `rust-cargo-build` owns resolver mechanics while `rust-semver` owns downstream compatibility of public exposure.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Dependency Governance field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
