---
name: rust-semver
description: Classify and plan Rust compatibility changes across public APIs, traits, types, features, MSRV, behavior, macros, and published packages. Use for release impact, deprecation, migration, and cargo-semver-checks interpretation.
---

# Rust SemVer

Own downstream compatibility classification and migration policy for released Rust contracts. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A published API, feature, MSRV, behavior, macro, trait, or package relationship is changing.
- A release needs major, minor, or patch classification and migration notes.
- SemVer tooling reports a change that needs contextual confirmation or misses a behavioral concern.

## Workflow

1. Identify the actual baseline release, supported branches, public feature set, MSRV, and documented stability policy.
2. Inventory changed public items, paths, trait contracts, bounds, auto traits, layouts, errors, macros, features, behavior, and dependencies exposed in types.
3. Classify source, binary or ABI where promised, behavioral, MSRV, and ecosystem compatibility separately.
4. Use configured SemVer tooling as evidence, then manually review dimensions it cannot model and false positives from intended policy.
5. Choose preserve, deprecate, shim, feature-gate, staged migration, or breaking release and write downstream examples.
6. Verify against the baseline artifact or tag with declared features and record tool limitations.

## Decision Rules

- Adding a public item is not always harmless when exhaustive enums, trait coherence, names, or feature behavior are involved.
- Removing or renaming public paths, required trait items, variants, fields, implementations, or supported features is normally breaking.
- New trait bounds, changed generic inference, auto-trait loss, panic behavior, ordering, or error classification can break callers without a signature deletion.
- Raising MSRV is a compatibility change and should follow the project's stated policy.
- `#[non_exhaustive]` changes what downstream code may construct or match and should be planned before release.
- Macro output and accepted syntax are public contracts when downstream crates invoke the macro.
- Pre-1.0 version policy may differ, but it must be explicit rather than assumed.
- Do not trust a clean automated report as proof of behavioral or all trait compatibility.

## Boundaries and Hand-offs

- `rust-api-design` owns the best current API shape; this profile owns compatibility with already released shapes.
- `rust-documentation` owns deprecation and migration prose once the compatibility decision is made.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust SemVer field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
