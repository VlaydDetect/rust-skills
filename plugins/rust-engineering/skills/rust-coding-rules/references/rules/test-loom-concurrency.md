# test-loom-concurrency

> Use `loom` to exhaustively test lock-free and concurrent code## Decision

Consider this rule only after its prerequisites are satisfied: Use `loom` to exhaustively test lock-free and concurrent code.

## Apply When

Apply when a concrete contract or risk needs the cheapest deterministic test that would fail for the defect, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the technique duplicates lower-cost coverage or adds a framework, snapshot, mock, sleep, or fuzz harness without unique risk coverage. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Map the contract to one test level and technique, isolate uncontrolled resources, and prove the assertion fails for the intended regression when practical.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Specialized test tools broaden state-space coverage but add dependencies, execution cost, maintenance, and false-stability risk.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`tokio`, `criterion`, `loom`) must already be accepted by the project or be approved before addition.

## Verification

Run the exact new test and its owning package or target, then record required features, runtime, seed, environment, and residual matrix.

## Why It Matters

Probabilistic stress tests can run millions of iterations and still miss a race condition that only manifests under a specific thread interleaving. `loom` systematically explores every thread scheduling and memory-reordering permitted by the C11 memory model, turning "we ran it a lot and it seemed fine" into a proof of correctness for the interleavings that exist within the model bounds. Tokio uses loom to verify its internal synchronization primitives.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Stress test: might pass a billion times, still doesn't prove correctness
#[test]
fn stress_test_flag() {
    use std::sync::{Arc, atomic::{AtomicBool, Ordering}};
    let flag = Arc::new(AtomicBool::new(false));
    for _ in 0..1_000_000 {
        let flag = Arc::clone(&flag);
        std::thread::spawn(move || {
            flag.store(true, Ordering::Relaxed);
        });
    }
    // races may never surface under the OS scheduler used here
}
```

## Good

Gate concurrent primitives behind `#[cfg(loom)]` so the same code runs with loom's instrumented types during model checking and with std types in production:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// src/flag.rs
#[cfg(loom)]
use loom::sync::atomic::{AtomicBool, Ordering};
#[cfg(not(loom))]
use std::sync::atomic::{AtomicBool, Ordering};

pub struct Flag(AtomicBool);

impl Flag {
    pub const fn new() -> Self {
        Self(AtomicBool::new(false))
    }

    pub fn set(&self) {
        self.0.store(true, Ordering::Release);
    }

    pub fn is_set(&self) -> bool {
        self.0.load(Ordering::Acquire)
    }
}
```

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// tests/loom_flag.rs  (or inside a #[cfg(loom)] mod in the crate)
#[cfg(loom)]
mod tests {
    use loom::sync::Arc;
    use super::Flag;

    #[test]
    fn flag_set_visible_to_other_thread() {
        loom::model(|| {
            let flag = Arc::new(Flag::new());

            let flag2 = Arc::clone(&flag);
            let writer = loom::thread::spawn(move || {
                flag2.set();
            });

            // All interleavings: either writer runs first or reader does.
            // loom verifies the Acquire/Release pair holds in both cases.
            let seen = flag.is_set();
            writer.join().unwrap();

            // After join, writer must have completed; flag must be set.
            assert!(flag.is_set(), "flag must be set after join");
            // 'seen' may be false if reader ran before writer — that is valid.
            let _ = seen;
        });
    }
}
```

Run loom tests with the feature flag:

```bash
RUSTFLAGS="--cfg loom" cargo test --test loom_flag
```

## Key Points

- Keep loom model closures **small**: combinatorial explosion grows with the number of atomic operations and threads. Test one primitive or algorithm at a time.
- loom replaces `std::sync::atomic`, `std::sync::Mutex`, `std::thread`, and `std::cell` with instrumented equivalents — import from `loom::` under `#[cfg(loom)]`.
- Use `loom::model(|| { ... })` as the entry point; loom runs the closure repeatedly under different schedules.
- loom checks the C11 model — it does not detect logical bugs unrelated to concurrency.

## Related Rules
- [conc-atomic-ordering](conc-atomic-ordering.md) - choose correct memory orderings
- [test-criterion-bench](test-criterion-bench.md) - benchmark concurrent code after verifying correctness
