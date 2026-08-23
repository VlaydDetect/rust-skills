# own-refcell-interior

> Use `RefCell<T>` for interior mutability in single-threaded code## Decision

Consider this rule only after its prerequisites are satisfied: Use `RefCell<T>` for interior mutability in single-threaded code.

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
- Apply only after the rule-specific condition in the rule guidance is observed in the current repository.

## Verification

Compile the affected paths and test moves, early returns, mutation, and drop or cancellation behavior that the rule changes.

## Why It Matters

Rust's borrow checker enforces rules at compile time, but sometimes you need to mutate data through a shared reference. `RefCell<T>` moves borrow checking to runtime, allowing mutation through `&self`. This is essential for patterns like caches, lazy initialization, and observer patterns where compile-time borrowing is too restrictive.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
struct Cache {
    // Requires &mut self to update, breaking shared reference patterns
    data: HashMap<String, String>,
}

impl Cache {
    fn get_or_compute(&mut self, key: &str) -> &str {
        // Caller needs &mut Cache, can't share cache reference
        if !self.data.contains_key(key) {
            self.data.insert(key.to_string(), expensive_compute(key));
        }
        &self.data[key]
    }
}
```

This forces exclusive access even for logically shared operations.

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::cell::RefCell;
use std::collections::HashMap;

struct Cache {
    data: RefCell<HashMap<String, String>>,
}

impl Cache {
    fn get_or_compute(&self, key: &str) -> String {
        // Can mutate through &self
        let mut data = self.data.borrow_mut();
        if !data.contains_key(key) {
            data.insert(key.to_string(), expensive_compute(key));
        }
        data[key].clone()
    }
}

// Multiple references can coexist
let cache = Cache::new();
let ref1 = &cache;
let ref2 = &cache;
ref1.get_or_compute("key1");
ref2.get_or_compute("key2");
```

## Common Pattern: Rc<RefCell<T>>

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Common Pattern: Rc<RefCell<T>> illustration -->
```rust
use std::rc::Rc;
use std::cell::RefCell;

// Shared mutable state in single-threaded code
type SharedState = Rc<RefCell<AppState>>;

fn create_handlers(state: SharedState) -> Vec<Box<dyn Fn()>> {
    vec![
        Box::new({
            let state = state.clone();
            move || state.borrow_mut().increment()
        }),
        Box::new({
            let state = state.clone();
            move || state.borrow_mut().decrement()
        }),
    ]
}
```

## Runtime Panics

`RefCell` panics if you violate borrowing rules at runtime:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Runtime Panics illustration -->
```rust
let cell = RefCell::new(5);
let borrow1 = cell.borrow();
let borrow2 = cell.borrow_mut(); // PANIC: already borrowed
```

Use `try_borrow()` and `try_borrow_mut()` for fallible borrowing.

## Cell for Copy Types

For simple `Copy` values, `Cell<T>` is lighter than `RefCell<T>` — no runtime borrow flags, no panics. You `get()`/`set()`/`replace()` the value instead of borrowing it:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Cell for Copy Types illustration -->
```rust
use std::cell::Cell;

struct Counter {
    count: Cell<u32>,
}

impl Counter {
    fn bump(&self) {
        self.count.set(self.count.get() + 1); // mutate through &self, never panics
    }
}
```

## Related Rules
- [own-rc-single-thread](./own-rc-single-thread.md) - Combining with Rc for shared ownership
- [own-mutex-interior](./own-mutex-interior.md) - Thread-safe alternative
- [conc-thread-local](./conc-thread-local.md) - `thread_local!` with `Cell`/`RefCell` for per-thread state
