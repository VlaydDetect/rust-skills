---
name: rust-ownership
description: Design and debug ownership, borrowing, lifetimes, moves, RAII, interior mutability, smart pointers, and resource lifecycle. Use when data ownership or reference validity is the controlling Rust problem.
---

# Rust Ownership

Own data and resource ownership, borrowing, reference lifetimes, pointer choice, and deterministic cleanup. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- The compiler reports moves, conflicting borrows, escaping references, lifetime mismatch, or ownership of captured values.
- An API must choose owned, borrowed, shared, mutable, copied, cloned, or cow data.
- Resource cleanup, cycles, self-reference, pinning, or interior mutability needs an explicit invariant.

## Workflow

1. Draw the ownership graph: creator, owners, borrowers, mutation points, thread boundaries, and drop order.
2. Identify the semantic lifetime required by the data rather than starting with lifetime annotations.
3. Prefer a single clear owner with short borrows; introduce shared ownership or interior mutability only for a real topology.
4. Reshape data or control flow to end borrows earlier before adding clones, reference counts, or unsafe code.
5. Choose pointer and mutability types by thread model, cycle risk, pinning need, and invariant enforcement.
6. Verify compiler behavior plus lifecycle effects such as drops, cancellation, file closure, or lock release.

## Decision Rules

- Lifetime parameters describe relationships; they do not extend the lifetime of a value.
- Return owned data when it is created inside the function and no longer has a valid external owner.
- Clone when duplication is semantically intended and measured or bounded, not merely to silence a borrow error.
- Use `Rc` or `RefCell` only in single-threaded ownership graphs and `Arc` with appropriate synchronization across threads.
- Avoid reference cycles or make weak edges and cycle-breaking ownership explicit.
- Use `Cow` when most inputs can remain borrowed and a minority require owned normalization.
- RAII guards must not be held across unrelated work or async suspension unless that scope is the invariant.
- Self-referential and pinned structures need a proven necessity and specialized design; do not improvise them with raw pointers.

## Boundaries and Hand-offs

- `rust-unsafe` owns manual validity and aliasing invariants once safe ownership tools are insufficient.
- `rust-concurrency` owns protocols across tasks or threads; this profile supplies the ownership foundation.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Ownership field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
