---
name: rust-stdlib
description: Choose and use Rust standard-library types, collections, iterators, I/O, paths, time, synchronization, and platform facilities. Use when the main decision is which std primitive expresses the contract without an external dependency.
---

# Rust Standard Library

Own standard-library selection and the semantic trade-offs of its core primitives. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A collection, iterator, path, I/O, time, process, synchronization, conversion, or utility type is being selected.
- A dependency might be avoidable with a correct standard-library facility.
- Existing code misuses a std API through wrong ownership, ordering, blocking, or platform assumptions.

## Workflow

1. Name the required semantics: ownership, ordering, lookup, duplication, mutation, blocking, time basis, encoding, and platform behavior.
2. Inspect the repository MSRV and existing type conventions before selecting a recently stabilized API.
3. Choose the simplest std type that directly enforces the contract; compare complexity and allocation behavior only where relevant.
4. Account for fallible conversions, Unicode versus bytes, path versus string, wall versus monotonic time, and poisoning or cancellation behavior.
5. Keep platform-specific behavior behind a narrow boundary and avoid assuming Unix semantics from the host.
6. Demonstrate edge cases with a small example or targeted test and route performance claims to measurement.

## Decision Rules

- Prefer slices and iterators at read-only boundaries; allocate owned collections only when ownership or mutation requires them.
- Use `Path` and `OsStr` for filesystem interfaces, not UTF-8 `String` by default.
- Use `Instant` for elapsed time and deadlines; `SystemTime` represents wall-clock time and can move.
- Select `HashMap`, `BTreeMap`, `Vec`, sets, heaps, or deques by required operations and ordering, not habit.
- Do not hold blocking std locks across async suspension points.
- Handle poisoned locks according to invariant policy rather than unconditionally unwrapping or ignoring them.
- Distinguish bytes, scalar values, grapheme clusters, and display width before indexing or truncating text.
- Use checked, saturating, wrapping, or overflowing arithmetic deliberately where numeric limits are part of the contract.

## Rulebook Overlay

After required operations and guarantees are explicit, select only relevant IDs from the [`coll-` index](../rust-coding-rules/references/categories/coll.md). Use adjacent rule categories only when their owner profile is already selected.

## Boundaries and Hand-offs

- `rust-ownership` owns borrowing and pointer semantics; this profile chooses std types under those semantics.
- `rust-concurrency` owns protocol and liveness design; this profile covers the mechanics of std synchronization primitives.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Standard Library field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
