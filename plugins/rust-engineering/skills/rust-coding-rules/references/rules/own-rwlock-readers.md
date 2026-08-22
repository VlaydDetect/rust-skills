# own-rwlock-readers

> Use `RwLock<T>` when reads significantly outnumber writes

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-ownership; supporters=`rust-stdlib`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `RwLock<T>` when reads significantly outnumber writes.

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
- External crates referenced by the source (`parking_lot`) must already be accepted by the project or be approved before addition.
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Compile the affected paths and test moves, early returns, mutation, and drop or cancellation behavior that the rule changes.

## Why It Matters

`Mutex<T>` allows only one thread to access data at a time, even for reads. `RwLock<T>` allows multiple concurrent readers OR one exclusive writer. For read-heavy workloads, this dramatically improves throughput by eliminating unnecessary serialization of read operations.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use std::sync::{Arc, Mutex};

// Configuration rarely changes but is read constantly
let config = Arc::new(Mutex::new(Config::load()));

// Every read blocks other reads unnecessarily
fn get_setting(config: &Mutex<Config>, key: &str) -> String {
    let guard = config.lock().unwrap();
    guard.get(key).to_string()
}

// 100 threads reading = serialized, one at a time
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::sync::{Arc, RwLock};

// Multiple readers can proceed concurrently
let config = Arc::new(RwLock::new(Config::load()));

fn get_setting(config: &RwLock<Config>, key: &str) -> String {
    let guard = config.read().unwrap(); // Multiple threads can hold read lock
    guard.get(key).to_string()
}

fn update_setting(config: &RwLock<Config>, key: &str, value: &str) {
    let mut guard = config.write().unwrap(); // Exclusive access for writes
    guard.set(key, value);
}

// 100 threads reading = parallel execution
```

## parking_lot::RwLock

Prefer `parking_lot::RwLock` for better performance:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the parkinglot::RwLock illustration -->
```rust
use parking_lot::RwLock;
use std::sync::Arc;

let data = Arc::new(RwLock::new(HashMap::new()));

// Read - no unwrap needed
let value = data.read().get("key").cloned();

// Write
data.write().insert("key".to_string(), "value".to_string());

// Upgradeable read lock (unique to parking_lot)
let upgradeable = data.upgradable_read();
if upgradeable.get("key").is_none() {
    let mut write = parking_lot::RwLockUpgradableReadGuard::upgrade(upgradeable);
    write.insert("key".to_string(), "default".to_string());
}
```

## When RwLock Hurts

RwLock has overhead for tracking readers. It can be slower than Mutex when:

| Scenario | Better Choice |
|----------|---------------|
| Writes are frequent (>20% of operations) | `Mutex` |
| Lock held very briefly | `Mutex` |
| Single-threaded | `RefCell` |
| Reads dominate, lock held longer | `RwLock` |

## Write Starvation

Standard `RwLock` may starve writers if readers are continuous. `parking_lot::RwLock` is fair by default.

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Write Starvation illustration -->
```rust
// parking_lot is writer-fair, preventing starvation
use parking_lot::RwLock;

// Or use std with explicit fairness (nightly)
// #![feature(rwlock_downgrade)]
```

## Real-World Pattern: Cached Computation

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Real-World Pattern: Cached Computation illustration -->
```rust
use parking_lot::RwLock;
use std::sync::Arc;

struct CachedData {
    cache: RwLock<Option<ExpensiveResult>>,
}

impl CachedData {
    fn get(&self) -> ExpensiveResult {
        // Fast path: read lock
        if let Some(cached) = self.cache.read().as_ref() {
            return cached.clone();
        }
        
        // Slow path: compute and cache
        let result = compute_expensive();
        *self.cache.write() = Some(result.clone());
        result
    }
}
```

## Related Rules
- [own-mutex-interior](./own-mutex-interior.md) - When writes are frequent
- [async-no-lock-await](./async-no-lock-await.md) - RwLock in async contexts
