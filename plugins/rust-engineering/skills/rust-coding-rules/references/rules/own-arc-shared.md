# own-arc-shared

> Use `Arc<T>` for thread-safe shared ownership

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-ownership; supporters=`rust-stdlib`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `Arc<T>` for thread-safe shared ownership.

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
- Apply only after the rule-specific condition in the source guidance is observed in the current repository.

## Verification

Compile the affected paths and test moves, early returns, mutation, and drop or cancellation behavior that the rule changes.

## Why It Matters

`Arc` (Atomic Reference Counted) provides shared ownership across threads. Unlike `Rc`, its reference count is updated atomically, making it safe for concurrent access. Use it when multiple threads need to read the same data.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use std::rc::Rc;
use std::thread;

let data = Rc::new(vec![1, 2, 3]);
let data_clone = Rc::clone(&data);

// ERROR: Rc cannot be sent between threads safely
thread::spawn(move || {
    println!("{:?}", data_clone);
});
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::sync::Arc;
use std::thread;

let data = Arc::new(vec![1, 2, 3]);
let data_clone = Arc::clone(&data);

thread::spawn(move || {
    println!("{:?}", data_clone);  // Safe!
});

println!("{:?}", data);  // Original still accessible
```

## Arc with Mutex for Mutable Shared State

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Arc with Mutex for Mutable Shared State illustration -->
```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    let handle = thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}

println!("Result: {}", *counter.lock().unwrap());
```

## Arc vs Rc Decision Tree

```
Need shared ownership?
├── No → Use owned value or references
└── Yes → Will it cross thread boundaries?
    ├── No → Use Rc<T> (cheaper, no atomic ops)
    └── Yes → Use Arc<T>
        └── Need mutation?
            ├── No → Arc<T> is enough
            └── Yes → Arc<Mutex<T>> or Arc<RwLock<T>>
```

## Common Patterns

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Common Patterns illustration -->
```rust
use std::sync::Arc;

// Shared configuration (read-only)
struct AppConfig {
    database_url: String,
    max_connections: u32,
}

fn setup_workers(config: Arc<AppConfig>) {
    for i in 0..4 {
        let config = Arc::clone(&config);
        std::thread::spawn(move || {
            println!("Worker {} using db: {}", i, config.database_url);
        });
    }
}

// Shared cache with interior mutability
use std::sync::RwLock;
use std::collections::HashMap;

type Cache = Arc<RwLock<HashMap<String, String>>>;

fn get_cached(cache: &Cache, key: &str) -> Option<String> {
    cache.read().unwrap().get(key).cloned()
}

fn set_cached(cache: &Cache, key: String, value: String) {
    cache.write().unwrap().insert(key, value);
}
```

## Performance Considerations

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Performance Considerations illustration -->
```rust
// Arc::clone is cheap - just increments atomic counter
let a = Arc::new(large_data);
let b = Arc::clone(&a);  // Fast! No data copied

// But atomic operations have overhead vs Rc
// Use Rc in single-threaded contexts for better performance

// Avoid cloning Arc in hot loops if possible
// Bad:
for item in items {
    let arc = Arc::clone(&shared);  // Atomic op each iteration
    process(arc, item);
}

// Better: Clone once outside loop if possible
let arc = Arc::clone(&shared);
for item in items {
    process(&arc, item);  // Pass reference
}
```

## Related Rules
- [own-rc-single-thread](own-rc-single-thread.md) - Use Rc for single-threaded sharing
- [own-mutex-interior](own-mutex-interior.md) - Use Mutex for interior mutability
- [async-clone-before-await](async-clone-before-await.md) - Clone Arc before await points
- [conc-scoped-threads](conc-scoped-threads.md) - Borrow stack data instead of Arc
- [unsafe-send-sync-manual](unsafe-send-sync-manual.md) - Document manual Send/Sync impls
