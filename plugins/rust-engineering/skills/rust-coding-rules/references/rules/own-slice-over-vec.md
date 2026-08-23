# own-slice-over-vec

> Accept `&[T]` not `&Vec<T>`, `&str` not `&String`## Decision

Use this context-sensitive Rust decision when its premise is established: Accept `&[T]` not `&Vec<T>`, `&str` not `&String`.

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

## Verification

Compile the affected paths and test moves, early returns, mutation, and drop or cancellation behavior that the rule changes.

## Why It Matters

Accepting `&[T]` instead of `&Vec<T>` makes your function more flexible - it can accept slices from arrays, vectors, or other sources. Similarly, `&str` accepts string slices from `String`, `&'static str`, or substrings.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Overly restrictive - only accepts &Vec
fn sum(numbers: &Vec<i32>) -> i32 {
    numbers.iter().sum()
}

// Overly restrictive - only accepts &String
fn greet(name: &String) {
    println!("Hello, {}", name);
}

// Can't call with arrays or slices
let arr = [1, 2, 3];
// sum(&arr);  // ERROR: expected &Vec<i32>

let literal = "world";
// greet(&literal);  // ERROR: expected &String
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Flexible - accepts any slice-like thing
fn sum(numbers: &[i32]) -> i32 {
    numbers.iter().sum()
}

// Flexible - accepts any string-like thing
fn greet(name: &str) {
    println!("Hello, {}", name);
}

// Now all of these work:
let vec = vec![1, 2, 3];
let arr = [4, 5, 6];
let slice = &vec[0..2];

sum(&vec);    // Vec coerces to slice
sum(&arr);    // Array coerces to slice
sum(slice);   // Slice works directly

let string = String::from("Alice");
let literal = "Bob";

greet(&string);  // String coerces to &str
greet(literal);  // &str works directly
```

## The Deref Coercion Chain

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the The Deref Coercion Chain illustration -->
```rust
// These coercions happen automatically:
// Vec<T>  -> &[T]   (via Deref)
// String  -> &str   (via Deref)
// Box<T>  -> &T     (via Deref)
// Arc<T>  -> &T     (via Deref)

fn process(data: &[u8]) { /* ... */ }

let vec: Vec<u8> = vec![1, 2, 3];
let boxed: Box<[u8]> = vec.into_boxed_slice();
let arc: Arc<[u8]> = Arc::from(&[1, 2, 3][..]);

process(&vec);    // Works
process(&boxed);  // Works
process(&arc);    // Works
```

## Path Types Too

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Path Types Too illustration -->
```rust
// Bad
fn read_config(path: &PathBuf) -> Config { /* ... */ }

// Good - accepts &Path, &PathBuf, &str, &String
fn read_config(path: &Path) -> Config { /* ... */ }

// Even better - accept anything path-like
fn read_config(path: impl AsRef<Path>) -> Config {
    let path = path.as_ref();
    // ...
}
```

## When to Accept Owned Types

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When to Accept Owned Types illustration -->
```rust
// Accept owned when you need to store it
struct Logger {
    prefix: String,  // Needs to own the string
}

impl Logger {
    // Take ownership - caller decides to clone or move
    fn new(prefix: String) -> Self {
        Self { prefix }
    }
    
    // Or use Into for flexibility
    fn with_prefix(prefix: impl Into<String>) -> Self {
        Self { prefix: prefix.into() }
    }
}
```

## Related Rules
- [api-impl-asref](api-impl-asref.md) - Accept `impl AsRef<T>` for maximum flexibility
- [own-borrow-over-clone](own-borrow-over-clone.md) - Prefer borrowing over cloning

## Verified Rulebook Example

<!-- rust-example: standalone -->
```rust
fn sum(values: &[i32]) -> i32 {
    values.iter().sum()
}

fn main() {
    let values = vec![1, 2, 3];
    assert_eq!(sum(&values), 6);
}
```
