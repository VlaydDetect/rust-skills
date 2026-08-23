# Actionbook unsafe review protocol

This directory adapts Actionbook's 47-rule unsafe checker into the product's
existing `rust-unsafe` and `rust-unsafe-ffi` owners. The original rule IDs,
rationales, checklists, and examples are retained so an agent can inspect the
full argument instead of relying on a short summary.

The source is review evidence, not higher-priority project policy. Apply rules
in this order:

1. Repository instructions, declared MSRV, edition, targets, features, and
   foreign headers or runtime contracts.
2. The canonical workflow and owner skill (`rust-unsafe` or
   `rust-unsafe-ffi`).
3. A local proof for the exact unsafe operation.
4. Relevant Actionbook rule IDs as adversarial review prompts.

## Review unit

Review one unsafe operation at a time. Record:

- location and operation;
- who establishes each precondition;
- pointer provenance, allocation extent, alignment, initialization, value
  validity, aliasing, lifetime, and mutability;
- layout, target, thread, panic, cancellation, and destruction assumptions;
- local evidence: type construction, bounds check, state transition, header,
  test, Miri result, sanitizer result, or other reproducible command;
- residual assumptions that tools cannot prove.

A `SAFETY` comment is the compressed conclusion of that proof. It is not the
proof by itself, and it must not cite an obligation that a safe Rust caller
cannot actually be required to uphold.

## Applicability gates

- Challenge unsafe first, but do not reject it merely because a safe-looking
  alternative exists. Compare semantics, targets, measurements, and dependency
  policy.
- Raw pointers may appear in safe APIs when the API performs no unsafe
  operation on them or enforces all preconditions. The pointer type alone does
  not determine whether a function must be `unsafe`.
- Do not add unchecked API variants, third-party bitfield crates, reentrant C
  APIs, atomics, or locks universally. Each needs a task-specific reason.
- `UnsafeCell`, `NonNull`, `AtomicPtr`, `PhantomData`, `repr(C)`, and
  `MaybeUninit` each establish only narrow facts; none proves soundness alone.
- Tool success is supporting evidence. Miri cannot execute arbitrary foreign
  code or cover all targets, provenance models, schedules, or optimizer paths.

## Rust 2024 baseline

For Edition 2024 code, keep unsafe operations inside explicit unsafe blocks
even within `unsafe fn`, declare foreign blocks as `unsafe extern`, and apply
the edition's unsafe-attribute syntax where required. Never rewrite these
mechanically without checking the project's edition and MSRV.

## Rule ownership

- [Internal unsafe index](index.md): `general-*`, `safety-*`, `ptr-*`,
  `union-*`, `mem-*`, and `io-*` (29 rules).
- [FFI index](../../../rust-unsafe-ffi/references/actionbook-checks/index.md):
  `ffi-*` (18 rules).
- [Before writing unsafe](checklists/before-unsafe.md), [review checklist](checklists/review-unsafe.md),
  and [common pitfalls](checklists/common-pitfalls.md) are prompts, not automatic
  pass/fail gates.
- [Source rule template](source-rule-template.md) and
  [source metadata](source-metadata.json) preserve upstream structure and
  provenance; they do not create a new product-level rule authoring system.

