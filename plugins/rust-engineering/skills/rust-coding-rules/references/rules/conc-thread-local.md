# conc-thread-local

> Prefer `thread_local!` with `Cell`/`RefCell` over `static mut`## Decision

Use this context-sensitive Rust decision when its premise is established: Prefer `thread_local!` with `Cell`/`RefCell` over `static mut`.

## Apply When

Apply when correctness or liveness spans threads, tasks, locks, channels, atomics, ordering, or shutdown, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when one owner and sequential execution satisfy the workload, or the proposed parallelism has no measured benefit. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Write the state machine, owners, capacities, lock order, memory ordering, failure, cancellation, and join policy.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Parallelism may improve throughput while increasing contention, scheduling variance, state-space, and shutdown complexity.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- Runtime, task ownership, cancellation, capacity, blocking, and shutdown behavior must be known.

## Verification

Use deterministic protocol tests and add loom, stress, or benchmarks only for the schedules or throughput they can demonstrate.

## Why It Matters

`static mut` requires `unsafe` at every access and is undefined behavior if any two threads touch it simultaneously — the compiler cannot rule that out. In Rust 2024, taking a shared or mutable reference to a `static mut` is a hard error (`static_mut_refs`). `thread_local!` gives each thread its own independent copy of the value, accessed through safe APIs via `Cell` (for `Copy` types) or `RefCell` (for anything else), with no synchronization overhead and no unsafe code needed.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Rust 2024: referencing static mut is a hard error (static_mut_refs lint)
static mut BUFFER: Vec<u8> = Vec::new();

fn append_to_buffer(data: &[u8]) {
    // UB if called from multiple threads; hard error in 2024 edition
    unsafe {
        BUFFER.extend_from_slice(data);
    }
}

fn flush_buffer() -> Vec<u8> {
    unsafe {
        std::mem::take(&mut BUFFER) // still requires unsafe
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::cell::RefCell;

thread_local! {
    static BUFFER: RefCell<Vec<u8>> = RefCell::new(Vec::with_capacity(4096));
}

fn append_to_buffer(data: &[u8]) {
    BUFFER.with_borrow_mut(|buf| buf.extend_from_slice(data));
}

fn flush_buffer() -> Vec<u8> {
    BUFFER.with_borrow_mut(|buf| std::mem::take(buf))
}
```

For `Copy` types, `Cell` is simpler (no borrow overhead):

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::cell::Cell;

thread_local! {
    static CALL_COUNT: Cell<u32> = Cell::new(0);
}

fn record_call() {
    CALL_COUNT.with(|c| c.set(c.get() + 1));
}

fn get_call_count() -> u32 {
    CALL_COUNT.with(|c| c.get())
}
```

## Key Points

- `with_borrow` / `with_borrow_mut` are stable convenience methods (since 1.73) on `LocalKey<RefCell<T>>` — prefer them over the longer `with(|v| v.borrow_mut())` form.
- Thread-local destructors run when the thread exits, so cleanup happens automatically.
- Avoid storing thread-locals in types that are sent across threads; the value is strictly per-thread and is not visible to other threads.
- For read-only global constants shared across threads, use `static` with an immutable type instead.

## When to Use

- Scratch buffers, caches, or accumulators that are logically per-thread and don't need to be shared
- Reusing allocations across calls within a single thread (e.g., formatting buffers, temporary vecs)
- Replacing `unsafe static mut` with a safe alternative

## Related Rules
- [own-refcell-interior](own-refcell-interior.md) - interior mutability for single-threaded code
- [own-mutex-interior](own-mutex-interior.md) - shared mutable state across threads requires `Mutex`
