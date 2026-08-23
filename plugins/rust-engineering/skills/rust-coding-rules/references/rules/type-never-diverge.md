# type-never-diverge

> Use `!` (never type) for functions that never return## Decision

Use this context-sensitive Rust decision when its premise is established: Use `!` (never type) for functions that never return.

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

The never type `!` indicates a function will never return normally—it either loops forever, panics, or exits the process. This helps the compiler understand control flow and enables `!` to coerce to any type, making it useful in match arms and expressions.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Return type doesn't indicate non-returning
fn infinite_loop() {
    loop {
        process_events();
    }
    // Implicit () return type, but never returns
}

// Using Option when it always panics
fn unreachable_code() -> Option<()> {
    panic!("This should never be called");
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// ! indicates function never returns
fn infinite_loop() -> ! {
    loop {
        process_events();
    }
}

fn abort_with_error(msg: &str) -> ! {
    eprintln!("Fatal error: {}", msg);
    std::process::exit(1);
}

fn panic_handler() -> ! {
    panic!("Unexpected state");
}
```

## Coercion to Any Type

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Coercion to Any Type illustration -->
```rust
// ! coerces to any type
fn get_value(opt: Option<i32>) -> i32 {
    match opt {
        Some(v) => v,
        None => panic!("No value"),  // panic! returns !, coerces to i32
    }
}

// Useful in Result handling
fn must_get_config() -> Config {
    match load_config() {
        Ok(c) => c,
        Err(e) => {
            log_error(&e);
            std::process::exit(1)  // Returns !, coerces to Config
        }
    }
}
```

## Standard Library Examples

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Standard Library Examples illustration -->
```rust
// std::process::exit
pub fn exit(code: i32) -> !

// panic! macro
// Expands to an expression of type !

// std::hint::unreachable_unchecked
pub unsafe fn unreachable_unchecked() -> !

// loop {} with no break
fn forever() -> ! {
    loop {}
}
```

## In Match Expressions

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the In Match Expressions illustration -->
```rust
enum State {
    Running,
    Stopped,
    Error,
}

fn get_status(state: &State) -> &str {
    match state {
        State::Running => "running",
        State::Stopped => "stopped",
        State::Error => unreachable!(),  // ! coerces to &str
    }
}

// With Result
fn process(r: Result<Data, Error>) -> Data {
    match r {
        Ok(d) => d,
        Err(e) => panic!("Unexpected error: {}", e),  // ! coerces to Data
    }
}
```

## Diverging Closures

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Diverging Closures illustration -->
```rust
// Closures that never return
let handler: fn() -> ! = || {
    panic!("Handler called");
};

// In thread spawn
std::thread::spawn(|| -> ! {
    loop {
        process_work();
    }
});
```

## Stability Notes

`fn f() -> !` (never type as a return type) has been **stable since Rust 1.41** — no feature gate needed.

Using `!` as an *arbitrary type argument* (e.g. `Result<(), !>`) still requires the nightly feature gate:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Stability Notes illustration -->
```rust
// Nightly only — using ! as a type argument
#![feature(never_type)]

type NeverResult = Result<(), !>;  // Can never be Err
```

On stable Rust, use `std::convert::Infallible` as the conventional substitute:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Stability Notes illustration -->
```rust
// Stable: Infallible is the standard stand-in for !
type StableNeverResult = Result<(), std::convert::Infallible>;
```

## Related Rules
- [err-result-over-panic](./err-result-over-panic.md) - When to panic vs return Result
- [type-result-fallible](./type-result-fallible.md) - Result for errors
- [opt-cold-unlikely](./opt-cold-unlikely.md) - Marking unlikely paths
