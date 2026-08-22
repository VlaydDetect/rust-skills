# mem-arrayvec

> Use `ArrayVec<T, N>` for fixed-capacity collections that never heap-allocate

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-performance; supporters=`rust-ownership`, `rust-stdlib`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `ArrayVec<T, N>` for fixed-capacity collections that never heap-allocate.

## Apply When

Apply when a measured allocation, footprint, locality, move, or layout cost is material on the representative workload, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when there is no profile or size evidence, or the change would complicate ownership, portability, or correctness for a noise-level gain. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Measure allocation or layout first, change one representation or reuse decision, and compare the same workload.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Inline storage, boxing, arenas, compact types, and reuse exchange simplicity, code size, stack use, locality, or dependency cost.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`smallvec`, `arrayvec`) must already be accepted by the project or be approved before addition.
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Keep correctness tests green and record before/after allocations, type size, memory footprint, or representative benchmark evidence.

## Why It Matters

`ArrayVec` from the `arrayvec` crate provides Vec-like API with a compile-time maximum capacity, storing all elements inline on the stack. Unlike `SmallVec` which can spill to heap, `ArrayVec` guarantees no heap allocation—if you exceed capacity, it returns an error or panics. This is ideal for embedded systems, real-time code, or when you have a hard upper bound.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Vec always heap-allocates, even for small collections
fn parse_options(input: &str) -> Vec<Option> {
    let mut options = Vec::new();  // Heap allocation
    for part in input.split(',').take(8) {  // Know we never exceed 8
        options.push(parse_option(part));
    }
    options
}

// Or SmallVec when you truly can't exceed capacity
use smallvec::SmallVec;
fn get_flags() -> SmallVec<[Flag; 4]> {
    // SmallVec CAN heap-allocate if pushed beyond 4
    // That might be unexpected in no-alloc contexts
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use arrayvec::ArrayVec;

// Guaranteed no heap allocation
fn parse_options(input: &str) -> ArrayVec<Option<u32>, 8> {
    let mut options = ArrayVec::new();
    for part in input.split(',') {
        if options.try_push(parse_option(part)).is_err() {
            break;  // Capacity reached, stop
        }
    }
    options
}

// For embedded/no_std contexts
#[no_std]
fn collect_readings() -> ArrayVec<SensorReading, 16> {
    let mut readings = ArrayVec::new();
    for sensor in SENSORS.iter() {
        readings.push(sensor.read());  // Panics if > 16
    }
    readings
}
```

## ArrayVec vs SmallVec vs Vec

| Type | Stack | Heap | Use When |
|------|-------|------|----------|
| `Vec<T>` | Never | Always | Unknown size, may grow indefinitely |
| `SmallVec<[T; N]>` | Up to N | Beyond N | Usually small, occasionally large |
| `ArrayVec<T, N>` | Always | Never | Hard limit, no heap allowed |

## API Patterns

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the API Patterns illustration -->
```rust
use arrayvec::ArrayVec;

let mut arr: ArrayVec<i32, 4> = ArrayVec::new();

// Push with potential panic (like Vec)
arr.push(1);
arr.push(2);

// Safe push - returns Err if full
match arr.try_push(3) {
    Ok(()) => println!("Added"),
    Err(err) => println!("Full, couldn't add {}", err.element()),
}

// Check capacity
assert!(arr.len() < arr.capacity());

// Remaining capacity
let remaining = arr.remaining_capacity();

// Is it full?
if arr.is_full() {
    arr.pop();
}

// From iterator with limit
let arr: ArrayVec<_, 10> = (0..100)
    .filter(|x| x % 2 == 0)
    .take(10)  // Important: don't exceed capacity
    .collect();
```

## ArrayString for Stack Strings

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the ArrayString for Stack Strings illustration -->
```rust
use arrayvec::ArrayString;
use std::fmt::Write; // brings the write! target trait into scope

// Stack-allocated string with max capacity
let mut s: ArrayString<64> = ArrayString::new();
s.push_str("Hello, ");
s.push_str("world!");

// No heap allocation for small strings
fn format_code(code: u32) -> ArrayString<16> {
    let mut s = ArrayString::new();
    write!(&mut s, "CODE-{:04}", code).unwrap();
    s
}
```

## When NOT to Use ArrayVec

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When NOT to Use ArrayVec illustration -->
```rust
// ❌ When size varies widely
fn parse_json_array(json: &str) -> ArrayVec<Value, ???> {
    // What capacity? JSON arrays can be any size
}

// ❌ When capacity is very large
let big: ArrayVec<u8, 1_000_000> = ArrayVec::new();  // 1MB on stack = bad

// ✅ Use SmallVec or Vec instead for these cases
```

## Cargo.toml

```toml
[dependencies]
arrayvec = "0.7"
```

## Related Rules
- [mem-smallvec](./mem-smallvec.md) - When heap fallback is acceptable
- [mem-with-capacity](./mem-with-capacity.md) - Pre-allocating Vec capacity
- [own-move-large](./own-move-large.md) - Large stack types considerations
