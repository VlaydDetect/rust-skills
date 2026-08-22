# Rust Ownership Field Guide

This guide is the detailed policy for `rust-ownership`. It synthesizes the craft ownership, borrowing, lifetimes, lifecycle, and pointer guides plus full-stack stable Rust ownership coverage; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- Ownership determines who may drop a value; borrowing grants temporary access without transferring that responsibility.
- Mutable access must be exclusive for the duration used, while shared references forbid mutation except through sound interior-mutability mechanisms.
- Non-lexical lifetimes can end a borrow at last use, so control-flow reshaping often solves conflicts without extra allocation.
- Drop order is reverse declaration order within a scope and can affect locks, transactions, files, spans, and foreign resources.
- `Box` gives unique heap ownership, `Rc` shared single-thread ownership, `Arc` shared thread-safe ownership; neither reference-counted pointer alone makes inner mutation safe.
- Common diagnostics E0382, E0499, E0502, E0505, E0507, and E0597 point to different ownership-graph contradictions.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Caller retains data | Borrowed slice, str, or reference | Avoids transfer and allocation |
| Callee must retain independent data | Owned value | Borrow duration should not leak into unrelated callers |
| Single-thread shared graph | Rc with Cell or RefCell if needed | Matches non-Send topology with runtime borrow checks |
| Cross-thread shared graph | Arc plus lock or atomic invariant | Reference counting and mutation are separate concerns |
| Borrowed fast path with occasional edit | Cow | Makes conditional ownership explicit |

## Common Failure Modes

- Adding `'static` to satisfy the compiler when the data is not actually process-long or owned.
- Cloning every value at API boundaries and obscuring who owns state.
- Wrapping everything in `Arc<Mutex<_>>` without a concurrency protocol.
- Returning references to local temporaries or data protected by a dropped guard.
- Creating `Rc` or `Arc` cycles that keep resources alive indefinitely.

## Required Evidence

- An ownership and drop-order map for affected resources and references.
- The specific compiler rule or lifecycle invariant addressed by the chosen type.
- Tests or examples covering mutation, early return, error, cancellation, and cleanup paths as applicable.
- Allocation or contention measurements before selecting cloning or shared locking for performance reasons.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.
