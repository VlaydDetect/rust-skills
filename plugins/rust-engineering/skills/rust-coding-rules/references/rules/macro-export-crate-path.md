# macro-export-crate-path

> Export declarative macros with `#[macro_export]` and a clean import path## Decision

Use this context-sensitive Rust decision when its premise is established: Export declarative macros with `#[macro_export]` and a clean import path.

## Apply When

Apply when ordinary functions, traits, generics, derives, or build-time generation cannot express required Rust syntax or repetition cleanly, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when a normal language abstraction is sufficient or the proposed DSL adds more grammar and diagnostics than value. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Specify valid and invalid invocations, expansion, hygiene, evaluation count, visibility, and diagnostics before implementation.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Macros remove repetition but add expansion, hygiene, diagnostics, navigation, public surface, and compile-time costs.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.

## Verification

Use compile-pass and compile-fail cases, expansion inspection, crate-renaming and cross-crate tests, and compile-time measurement when broad.

## Why It Matters

`#[macro_export]` lifts a macro to the crate root, making it importable like any other item. Combined with `$crate::` paths (see `macro-rules-hygiene`), the macro works regardless of how callers import it. Since Rust 2018, callers can use ordinary path imports (`use mycrate::my_macro;`) rather than the legacy `#[macro_use] extern crate mycrate;`, which polluted the global namespace and depended on item ordering.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// lib.rs — legacy style
// Requires callers to write `#[macro_use] extern crate mylib;`
// and dumps all macros into the caller's global scope.
macro_rules! greet {
    ($name:expr) => {
        println!("hello, {}", $name);
    };
}
```

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// consumer/src/main.rs — legacy
#[macro_use]
extern crate mylib; // order-sensitive; pollutes namespace

fn main() {
    greet!("world");
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// lib.rs — modern style
#[macro_export]
macro_rules! greet {
    ($name:expr) => {
        $crate::__private::print_greeting($name);
    };
}

// Re-export so `use mylib::greet;` resolves through the crate's public path.
// (The re-export is implicit when using #[macro_export]; this is just for clarity
// or when you want to place it under a module path.)
pub use greet;
```

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// consumer/src/main.rs — modern
use mylib::greet;

fn main() {
    greet!("world");
}
```

## Placing Macros in Modules

`#[macro_export]` always places the macro at the crate root regardless of where the `macro_rules!` definition appears. To expose it under a module path, use a `pub use` re-export:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Placing Macros in Modules illustration -->
```rust
// lib.rs
pub mod macros {
    // The macro is defined at crate root by #[macro_export], but we
    // also re-export it here so `use mycrate::macros::greet;` works.
    pub use crate::greet;
}

#[macro_export]
macro_rules! greet {
    ($name:expr) => { println!("hello, {}", $name); };
}
```

## Key Points

- Prefer `use mycrate::my_macro;` — it is explicit and plays well with `rustfmt` and IDEs.
- Avoid `#[macro_use]` in new code; it is required only when supporting pre-2018 edition consumers.
- If the macro calls internal helpers, pair `#[macro_export]` with `$crate::__private::...` paths.
- Document macros with `///` just like any other public item.

## Related Rules
- [macro-rules-hygiene](macro-rules-hygiene.md) - using `$crate` for correct item resolution
- [macro-private-helpers](macro-private-helpers.md) - hiding helpers used by exported macros
- [proj-workspace-deps](proj-workspace-deps.md) - workspace dependency inheritance
