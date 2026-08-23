---
name: rust-unsafe
description: Review and design internal unsafe Rust, raw pointers, aliasing, initialization, layout, interior mutability, pinning, and sound safe abstractions. Use when memory validity or unsafe invariants are involved; use rust-unsafe-ffi for external ABI boundaries.
---

# Unsafe Rust

Own internal unsafe operations and the soundness boundary of safe Rust abstractions. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- Code contains or proposes `unsafe`, raw pointers, unions, `MaybeUninit`, `UnsafeCell`, manual allocation, pin projections, or layout assumptions.
- A safe API wraps unsafe internals and its validity, aliasing, thread-safety, or drop invariant needs proof.
- Miri, sanitizer, or undefined-behavior findings need interpretation.

## Workflow

1. Challenge the need for unsafe and identify a safe standard-library or crate alternative before proceeding.
2. Define the safe public contract and list every caller obligation the wrapper must enforce rather than merely document.
3. For each unsafe operation, state pointer provenance, alignment, initialization, validity, aliasing, bounds, lifetime, layout, thread, panic, and drop assumptions that apply.
4. Minimize the unsafe block and keep invariant-establishing checks adjacent to it; avoid unsafe functions when callers should not carry the obligation.
5. Audit all constructors, mutation paths, auto traits, panics, partial initialization, and destruction, including zero-sized and empty cases.
6. Run targeted tests and Miri or sanitizers where applicable, then document tool coverage limits and remaining manual proof obligations.

## Decision Rules

- Every unsafe block needs a `SAFETY` explanation that proves the exact operation's preconditions from local facts.
- A safe function must not rely on undocumented caller behavior to avoid undefined behavior.
- Do not use `transmute` when explicit conversions, pointer casts, byte APIs, or layout-aware operations express the contract.
- `MaybeUninit` does not make uninitialized values valid; track initialization and drop exactly once.
- `UnsafeCell` permits interior mutation but does not supply synchronization or arbitrary aliasing.
- Do not implement `Send` or `Sync` manually without a full concurrency and ownership proof.
- Panic or early-return paths must preserve initialization and ownership invariants.
- Miri success is supporting evidence, not proof for all platforms, optimizations, foreign code, or concurrency schedules.

## Rulebook Overlay

After writing the operation-by-operation safety proof, select only relevant IDs from the [`unsafe-` index](../rust-coding-rules/references/categories/unsafe.md). The rules supplement local invariant evidence and never justify introducing unsafe code.

Then use the [Actionbook internal unsafe index](references/actionbook-checks/index.md)
as an adversarial checklist. Load individual retained rules, not the whole
corpus, and apply the product note at the top of each file. Report one finding
under the canonical product rule when the two rulebooks overlap.

## Boundaries and Hand-offs

- `rust-unsafe-ffi` owns ABI, foreign ownership, callbacks, unwinding, and exported symbol contracts.
- `rust-performance` must supply measurements before unsafe is justified primarily as an optimization.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Unsafe Rust field guide](references/guide.md) before making a consequential design choice. For a new or reviewed unsafe boundary, also read the [Actionbook review protocol](references/actionbook-checks/overview.md) and select the relevant detailed rules from its [29-rule index](references/actionbook-checks/index.md). Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.

## Huiali protocols

For source-derived detail relevant to this profile, read the [Huiali integration index](references/huiali-index.md) and load only the matching family reference.

## Low-level protocols

For source-derived debugging, profiling, build, sanitizer, cross-target, ABI, async-internal, security, or hardware detail relevant to this profile, read the [Low-level integration index](references/low-level-index.md) and load only the matching family. Apply its official-evidence and command-safety gate before execution.
