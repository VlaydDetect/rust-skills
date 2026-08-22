# own-mutex-interior

> Use `Mutex<T>` for interior mutability across threads

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-ownership; supporters=`rust-stdlib`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `Mutex<T>` for interior mutability across threads.

## Apply When

Apply when ownership, borrowing, lifetime, pointer, mutation, or drop semantics control correctness, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when independent ownership is required, or the proposed borrowing shape would leak a guard or lifetime into unrelated callers. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Draw the owner/borrower/drop graph and choose the least complex ownership topology that enforces it.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Less cloning can increase lifetime coupling; shared ownership and interior mutability add runtime and liveness costs.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`bytes`, `parking_lot`) must already be accepted by the project or be approved before addition.

## Verification

Compile the affected paths and test moves, early returns, mutation, and drop or cancellation behavior that the rule changes.

## Why It Matters

When you need shared mutable state across threads, `Mutex<T>` provides safe interior mutability with synchronization. Unlike `RefCell`, `Mutex` is `Send + Sync` and uses OS-level locking to ensure only one thread can access the data at a time.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use std::cell::RefCell;
use std::sync::Arc;

// RefCell is !Sync - this won't compile
let shared = Arc::new(RefCell::new(vec![]));

// ERROR: RefCell cannot be shared between threads safely
std::thread::spawn({
    let shared = shared.clone();
    move || shared.borrow_mut().push(1)
});
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::sync::{Arc, Mutex};

let shared = Arc::new(Mutex::new(vec![]));

let handles: Vec<_> = (0..10).map(|i| {
    let shared = shared.clone();
    std::thread::spawn(move || {
        let mut data = shared.lock().unwrap();
        data.push(i);
    })
}).collect();

for handle in handles {
    handle.join().unwrap();
}

println!("{:?}", shared.lock().unwrap()); // All values present
```

## Mutex Poisoning

If a thread panics while holding a lock, the mutex becomes "poisoned":

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Mutex Poisoning illustration -->
```rust
use std::sync::{Arc, Mutex};

let mutex = Arc::new(Mutex::new(0));

// Handle poisoning gracefully
match mutex.lock() {
    Ok(guard) => println!("Value: {}", *guard),
    Err(poisoned) => {
        // Recover the data anyway
        let guard = poisoned.into_inner();
        println!("Recovered value: {}", *guard);
    }
}

// Or ignore poisoning (use with caution)
let guard = mutex.lock().unwrap_or_else(|e| e.into_inner());
```

## Prefer parking_lot::Mutex

For better performance, consider `parking_lot::Mutex`:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Prefer parkinglot::Mutex illustration -->
```rust
use parking_lot::Mutex;
use std::sync::Arc;

let shared = Arc::new(Mutex::new(vec![]));

// No poisoning, no Result to unwrap
let mut data = shared.lock();
data.push(42);
// Lock automatically released when guard drops
```

Benefits of `parking_lot`:
- No poisoning (returns guard directly)
- Smaller size (1 byte vs 40+ bytes)
- Better performance under contention
- Fair locking option available

## When to Use What

| Type | Threading | Overhead | Use Case |
|------|-----------|----------|----------|
| `RefCell<T>` | Single | Minimal | Interior mutability, same thread |
| `Mutex<T>` | Multi | Locking | Shared mutable state across threads |
| `RwLock<T>` | Multi | Locking | Many readers, few writers |
| `parking_lot::Mutex` | Multi | Less | Drop-in std::Mutex replacement |

## Related Rules
- [own-rwlock-readers](./own-rwlock-readers.md) - When reads dominate writes
- [own-refcell-interior](./own-refcell-interior.md) - Single-threaded alternative
- [async-no-lock-await](./async-no-lock-await.md) - Avoiding locks across await points
- [conc-atomic-ordering](./conc-atomic-ordering.md) - Lock-free alternative for simple state
