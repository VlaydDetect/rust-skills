# type-phantom-marker

> Use `PhantomData` to express type relationships without runtime cost

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-traits; supporters=`rust-api-design`, `rust-ownership`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Use `PhantomData` to express type relationships without runtime cost.

## Apply When

Apply when a type can encode a real invariant, state, identity, representation, or output contract more reliably than convention, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the extra type machinery does not eliminate a meaningful invalid state or would make a local operation harder to use. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Name the invalid states, choose the smallest nominal or algebraic representation, and review construction and conversion boundaries.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Type-driven guarantees move failures earlier but can expand public surface, conversion code, generic complexity, and diagnostics.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Use compile-pass, compile-fail, and runtime boundary cases to prove valid construction and rejection paths.

## Why It Matters

Sometimes your type needs to be parameterized by a type that doesn't appear in any field—for variance, drop order, or semantic purposes. `PhantomData<T>` tells the compiler your type is "associated with" `T` without storing any `T` data. It has zero runtime cost.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Type parameter unused - compiler error
struct Handle<T> {
    id: u64,
    // Error: parameter `T` is never used
}

// Workaround with unnecessary storage
struct Handle<T> {
    id: u64,
    _type: Option<T>,  // Wastes memory, requires T: Default
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::marker::PhantomData;

struct Handle<T> {
    id: u64,
    _marker: PhantomData<T>,  // Zero-size, tells compiler about T
}

impl<T> Handle<T> {
    fn new(id: u64) -> Self {
        Handle {
            id,
            _marker: PhantomData,
        }
    }
}

// Different Handle types are incompatible
struct User;
struct Order;

fn process_user(h: Handle<User>) { ... }

let user_handle = Handle::<User>::new(1);
let order_handle = Handle::<Order>::new(2);

process_user(user_handle);   // OK
process_user(order_handle);  // Error: expected Handle<User>, found Handle<Order>
```

## Expressing Ownership

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Expressing Ownership illustration -->
```rust
use std::marker::PhantomData;

// Owns T conceptually (like Box<T>)
struct Container<T> {
    ptr: *mut T,
    _marker: PhantomData<T>,  // Acts like we own a T
}

// Drop will be called on T when Container drops
impl<T> Drop for Container<T> {
    fn drop(&mut self) {
        unsafe {
            std::ptr::drop_in_place(self.ptr);
        }
    }
}
```

## Expressing Borrowing

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Expressing Borrowing illustration -->
```rust
use std::marker::PhantomData;

// Borrows T for lifetime 'a
struct Ref<'a, T> {
    ptr: *const T,
    _marker: PhantomData<&'a T>,  // Acts like &'a T
}

// Compiler tracks lifetime correctly
impl<'a, T> Ref<'a, T> {
    fn get(&self) -> &'a T {
        unsafe { &*self.ptr }
    }
}
```

## Type-Level State Machine

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Type-Level State Machine illustration -->
```rust
use std::marker::PhantomData;

// States as zero-size types
struct Unlocked;
struct Locked;

struct Door<State> {
    _state: PhantomData<State>,
}

impl Door<Unlocked> {
    fn lock(self) -> Door<Locked> {
        println!("Locking...");
        Door { _state: PhantomData }
    }
    
    fn open(&self) {
        println!("Opening...");
    }
}

impl Door<Locked> {
    fn unlock(self) -> Door<Unlocked> {
        println!("Unlocking...");
        Door { _state: PhantomData }
    }
    
    // Can't call open() on Locked door - method doesn't exist
}

fn example() {
    let door: Door<Unlocked> = Door { _state: PhantomData };
    door.open();           // OK
    let locked = door.lock();
    // locked.open();      // Error: no method `open` for Door<Locked>
    let unlocked = locked.unlock();
    unlocked.open();       // OK
}
```

## Variance Control

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Variance Control illustration -->
```rust
use std::marker::PhantomData;

// Covariant in T (PhantomData<T>)
struct Producer<T> {
    _marker: PhantomData<T>,  // Covariant
}

// Contravariant in T (PhantomData<fn(T)>)
struct Consumer<T> {
    _marker: PhantomData<fn(T)>,  // Contravariant
}

// Invariant in T (PhantomData<fn(T) -> T>)
struct Both<T> {
    _marker: PhantomData<fn(T) -> T>,  // Invariant
}
```

## Common Uses

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Common Uses illustration -->
```rust
// 1. FFI handles with type safety
struct FileHandle<T: FileType> {
    fd: i32,
    _marker: PhantomData<T>,
}

// 2. Generic iterators
struct Iter<'a, T> {
    ptr: *const T,
    end: *const T,
    _marker: PhantomData<&'a T>,
}

// 3. Allocator-aware types
struct Vec<T, A: Allocator = Global> {
    buf: RawVec<T, A>,
    len: usize,
}
```

## Related Rules
- [api-typestate](./api-typestate.md) - State machine pattern
- [api-newtype-safety](./api-newtype-safety.md) - Type-safe wrappers
- [type-newtype-ids](./type-newtype-ids.md) - ID types
