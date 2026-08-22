---
name: refactoring
description: Restructure Rust code while preserving an explicit behavioral, API, compatibility, and performance contract. Use for extraction, movement, simplification, dependency inversion, or staged structural change where behavior should remain stable.
---

# Rust Refactoring

Own behavior-preserving structural change and its migration sequence. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- Code must be moved, split, consolidated, renamed, or simplified without adding product behavior.
- A crate or module boundary must change while callers remain supported or receive a planned migration.
- Duplication or coupling has a demonstrated maintenance cost and an existing contract can anchor the change.

## Workflow

1. Name the preserved contract: observable behavior, public API, serialization, errors, ordering, timing envelope, and supported configurations.
2. Trace all callers, constructors, trait implementations, feature gates, tests, docs, and generated consumers of the changed surface.
3. Add or identify characterization evidence where the contract is not already executable.
4. Choose a sequence of compiling steps with one structural purpose each; introduce compatibility shims only when callers need a staged migration.
5. Remove superseded paths once all in-scope callers move; do not leave parallel abstractions without a stated transition need.
6. Compare before and after contracts, run targeted checks, and inspect the diff for accidental behavior or visibility changes.

## Decision Rules

- Do not combine a broad refactor with unrelated feature work unless separation is impossible and explained.
- Prefer moving existing behavior before rewriting it; movement gives a cleaner comparison point.
- Preserve public paths, feature behavior, error categories, and serialized forms unless the task authorizes a breaking change.
- An abstraction is justified by current variation or boundary ownership, not hypothetical reuse.
- Delete compatibility layers after the migration stage they exist for.
- Keep commits or logical steps buildable when practical so bisection remains useful.
- For performance-sensitive code, compare the same workload before and after; structural elegance is not evidence.
- Update documentation and examples when paths or concepts change even if runtime behavior does not.

## Boundaries and Hand-offs

- `rust-architecture` owns choosing system boundaries for new behavior; this profile owns changing structure under a preserved contract.
- `rust-semver` owns release compatibility classification for public library changes.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Refactoring field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
