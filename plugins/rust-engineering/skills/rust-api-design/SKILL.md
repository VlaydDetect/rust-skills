---
name: rust-api-design
description: Design stable, idiomatic Rust APIs with explicit ownership, errors, extensibility, visibility, naming, and compatibility. Use for public crate surfaces, cross-module contracts, builders, traits, types, and downstream ergonomics.
---

# Rust API Design

Own the caller-visible Rust contract and its evolution surface. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A public type, function, trait, module, builder, error, or re-export is being added or changed.
- An internal boundary needs a durable contract between independently evolving modules or crates.
- The design must balance ergonomics, ownership, extensibility, documentation, and SemVer.

## Workflow

1. Identify users, use cases, supported toolchain, no-std or target constraints, and the minimum behavior the API must promise.
2. Design from caller examples first, including success, error, optional configuration, borrowing, and repeated use.
3. Choose ownership, visibility, naming, type representation, errors, generic bounds, and extension policy explicitly.
4. Minimize public surface and dependency types; keep constructors valid and invalid states unrepresentable where practical.
5. Review downstream compatibility, trait coherence, object safety, non-exhaustiveness, feature behavior, and documentation links.
6. Validate with compile-pass examples, compile-fail constraints when useful, rustdoc, and SemVer tooling already configured by the repository.

## Decision Rules

- Accept borrowed inputs when the function need not retain them; return owned values when ownership must outlive the call.
- Prefer concrete types until callers genuinely need abstraction; avoid generic parameters that only mirror one implementation.
- Keep fields private when construction or mutation must preserve invariants.
- Use `#[non_exhaustive]`, sealed traits, or private modules only with a stated downstream extension policy.
- Do not expose third-party types accidentally when they would bind the public contract to a dependency version.
- Name operations by domain behavior and Rust convention, not internal storage or transport details.
- Builders are appropriate for many optional or validated settings; a direct constructor is clearer for a few required fields.
- Public errors, feature flags, auto traits, Send or Sync behavior, and panic conditions are part of the API.

## Rulebook Overlay

After the caller contract is explicit, select at most eight IDs from [`api-`](../rust-coding-rules/references/categories/api.md), [`conv-`](../rust-coding-rules/references/categories/conv.md), [`serde-`](../rust-coding-rules/references/categories/serde.md), or semantic [`name-`](../rust-coding-rules/references/categories/name.md) rules. Public compatibility remains owned here.

## Boundaries and Hand-offs

- `rust-traits` owns detailed dispatch and coherence design; `rust-ownership` owns difficult lifetime and pointer choices.
- `rust-semver` owns classifying a released API change and `rust-documentation` owns the complete rustdoc experience.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust API Design field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.

## Specialized Rust protocols

For additional topic detail, read the [Profile reference index](./references/guide.md) and load only the matching family reference.
