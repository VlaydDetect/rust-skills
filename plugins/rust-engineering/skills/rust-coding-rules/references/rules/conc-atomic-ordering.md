# conc-atomic-ordering

> Use the weakest correct memory `Ordering` for every atomic operation

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-concurrency; supporters=`rust-ownership`, `rust-testing`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use the weakest correct memory `Ordering` for every atomic operation.

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
- External crates referenced by the source (`loom`) must already be accepted by the project or be approved before addition.
- Runtime, task ownership, cancellation, capacity, blocking, and shutdown behavior must be known.

## Verification

Use deterministic protocol tests and add loom, stress, or benchmarks only for the schedules or throughput they can demonstrate.

## Why It Matters

Defaulting to `SeqCst` (sequentially consistent) on every atomic is a common correctness-first shortcut, but it carries real cost: on x86 the difference is small, but on ARM and RISC-V weaker orderings map to cheaper instructions while `SeqCst` requires full memory barriers. More importantly, choosing the wrong ordering — even a weaker one — is a correctness bug that causes data races the compiler won't catch. Understanding the four practical levels lets you write both correct and efficient concurrent code.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use std::sync::atomic::{AtomicU64, AtomicBool, Ordering};

static COUNTER: AtomicU64 = AtomicU64::new(0);
static READY: AtomicBool = AtomicBool::new(false);
static mut DATA: u64 = 0;

// SeqCst everywhere — correct, but unnecessarily expensive
fn increment() {
    COUNTER.fetch_add(1, Ordering::SeqCst);
}

fn producer() {
    unsafe { DATA = 42; }
    READY.store(true, Ordering::SeqCst); // overkill for a single flag
}

fn consumer() -> Option<u64> {
    if READY.load(Ordering::SeqCst) {
        Some(unsafe { DATA })
    } else {
        None
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::sync::atomic::{AtomicU64, AtomicBool, Ordering};

static COUNTER: AtomicU64 = AtomicU64::new(0);

// Relaxed: no ordering relative to other memory — fine for independent counters
fn increment() {
    COUNTER.fetch_add(1, Ordering::Relaxed);
}

fn total() -> u64 {
    COUNTER.load(Ordering::Relaxed)
}

// Acquire/Release: paired handoff — producer writes data THEN sets flag (Release);
// consumer loads flag (Acquire) and is guaranteed to see the preceding write.
static READY: AtomicBool = AtomicBool::new(false);
static VALUE: AtomicU64 = AtomicU64::new(0);

fn producer(value: u64) {
    VALUE.store(value, Ordering::Relaxed);   // write payload first
    READY.store(true, Ordering::Release);    // publish with Release
}

fn consumer() -> Option<u64> {
    if READY.load(Ordering::Acquire) {       // synchronize with Release store
        Some(VALUE.load(Ordering::Relaxed))  // payload visible after Acquire
    } else {
        None
    }
}

// SeqCst: only when you need a single total order across *multiple* atomics.
// Example: Dekker-style mutual exclusion involving two independent flags.
```

## Ordering Quick Reference

| Ordering | Use when |
|----------|----------|
| `Relaxed` | Operation is atomic but needs no ordering relative to other memory (counters, stats) |
| `Acquire` | Load that must see all stores preceding a matching `Release` on another thread |
| `Release` | Store that must be visible before a matching `Acquire` load on another thread |
| `AcqRel` | Read-modify-write (e.g. `compare_exchange`) acting as both Acquire and Release |
| `SeqCst` | Need a single global order observed by all threads across multiple atomic variables |

## Verification with loom

Use the `loom` crate to exhaustively verify ordering choices for small concurrent units — it explores all interleavings the C11 memory model permits:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Verification with loom illustration -->
```rust
#[cfg(loom)]
use loom::sync::atomic::{AtomicBool, Ordering};

#[cfg(loom)]
#[test]
fn test_handoff() {
    loom::model(|| {
        // ... spawn threads, assert invariants
    });
}
```

## Related Rules
- [own-mutex-interior](own-mutex-interior.md) - prefer `Mutex<T>` when lock-free isn't required
- [test-loom-concurrency](test-loom-concurrency.md) - exhaustively test concurrent code with loom
- [conc-scoped-threads](conc-scoped-threads.md) - safely share stack data across threads
