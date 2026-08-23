---
name: rust-pin
description: Design and review Rust pinning contracts, address-sensitive values, Pin and Unpin behavior, structural projection, self-referential state, Future polling, and pinned destruction. Use when moving a value could invalidate an internal invariant.
---

# Rust Pinning

Own the pinning contract: which value becomes address-sensitive, when that contract begins, which fields are structurally pinned, and how it remains valid through projection and destruction.

## Use This Skill When

- A type implements `Future`, stores self-references, exposes `Pin<P>`, or opts out of `Unpin`.
- Code uses `Pin::new_unchecked`, `get_unchecked_mut`, unsafe projection, `PhantomPinned`, or a projection crate.
- A move, replacement, drop, callback registration, intrusive link, or FFI handoff may invalidate an address-dependent invariant.

## Workflow

1. Name the address-sensitive invariant and the exact event after which the value must not move.
2. Identify the pointer owner and whether pinning the pointer actually prevents movement of the pointee.
3. Determine `Unpin` behavior, including generic parameters and any explicit negative opt-out through `PhantomPinned`.
4. Define which fields are structurally pinned and which may be safely replaced or moved.
5. Prefer safe construction and projection; isolate every unsafe operation with a local proof covering all later safe operations.
6. Check cancellation, panic, replacement, and `Drop` behavior before declaring the contract complete.

## Decision Rules

- `Pin` restricts access through a pointer; it does not freeze bytes, prevent interior mutation, or make a value thread-safe.
- Heap allocation alone is not a pinning proof, and pinning an `Unpin` value does not make moves observably unsafe.
- `Pin::new_unchecked` is justified only when the pointee cannot be moved until its pinning contract ends.
- Unsafe field projection must prove structural pinning and prevent later safe code from moving or replacing the field.
- A pinned value must be dropped before its storage is reused or invalidated; include the drop guarantee in intrusive and self-referential designs.
- Prefer stable `std::pin`, `std::pin::pin!`, `Box::pin`, and safe projection APIs before custom unsafe machinery.

## Boundaries and Hand-offs

- `rust-unsafe` owns the proof for unsafe construction or projection; this profile owns the pinning invariant being proved.
- `rust-concurrency` owns task cancellation and Future lifecycle; this profile owns address stability while the Future is pinned.
- `rust-ownership` owns ordinary borrow and owner relationships; pinning does not extend a reference lifetime.
- Use `rust-workflow` for repository changes and `rust-verify` for targeted tests, Miri, or compile-fail evidence.

## Detailed Reference

Read [Rust Pinning field guide](references/guide.md) before creating an unsafe pinning abstraction. For detailed algorithms and classified fragments, load only the [`rust-pin` Specialized Rust protocol](./references/pin.md).

## Specialized Rust protocols

For additional topic detail, read the [Profile reference index](./references/guide.md) and load only the matching family reference.

## Low-level protocols

For low-level debugging, profiling, build, sanitizer, cross-target, ABI, async-internal, security, or hardware detail, read the [Low-level reference index](references/low-level-index.md) and load only the matching family. Apply its official-evidence and command-safety gate before execution.
