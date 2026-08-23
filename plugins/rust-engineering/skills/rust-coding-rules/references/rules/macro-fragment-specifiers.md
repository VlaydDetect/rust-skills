# macro-fragment-specifiers

> Capture with precise fragment specifiers, not raw `:tt`, where you can## Decision

Use this context-sensitive Rust decision when its premise is established: Capture with precise fragment specifiers, not raw `:tt`, where you can.

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

Fragment specifiers tell the compiler — and readers — exactly what syntactic category a macro arm expects. They produce targeted error messages ("expected expression" instead of "no rules expected token"), enable better IDE tooling, and prevent ambiguous parses. Using raw `:tt` (token tree) forces you to re-parse or validate by hand and leaks implementation details into error messages.

Note the **follow-set restriction**: after `:expr`, `:ty`, `:pat`, and a few others, only a limited set of tokens may appear — most commonly `=>`, `,`, `;`, `|`, or another fragment. Plan your separator tokens accordingly.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Slurping everything as :tt, then trying to use $e as if it were an expression.
macro_rules! debug_val {
    ($($t:tt)*) => {
        println!("{} = {:?}", stringify!($($t)*), $($t)*);
        //                                          ^^^^^^^^ re-expanding :tt soup
    };
}

fn main() {
    debug_val!(1 + 2);      // works by accident
    debug_val!(let x = 1);  // accepted by the macro; blows up at expansion
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
macro_rules! debug_val {
    // :expr captures a single expression; the follow-set allows `=>` and `,` after it.
    ($e:expr) => {
        println!("{} = {:?}", stringify!($e), $e);
    };
}

fn main() {
    debug_val!(1 + 2);
    // debug_val!(let x = 1); // now correctly rejected at the macro call site
}
```

## Fragment Specifier Reference

| Specifier | Matches | Common uses |
|-----------|---------|-------------|
| `:expr` | An expression | Values, arithmetic, closures |
| `:ty` | A type | Generic helpers, type aliases |
| `:ident` | An identifier | Field names, variable names |
| `:pat` | A pattern | `match` arm patterns |
| `:pat_param` | A pattern (no `|` at top level) | Fn param patterns |
| `:path` | A path (`a::b::c`) | Trait bounds, type paths |
| `:literal` | A literal (`42`, `"hi"`) | Constant values |
| `:block` | A `{ ... }` block | Inline code injection |
| `:stmt` | A statement | Statement-level macros |
| `:meta` | A meta item | `#[derive(Clone)]` content |
| `:vis` | A visibility qualifier | `pub`, `pub(crate)` |
| `:lifetime` | A lifetime (`'a`) | Generic lifetime params |
| `:tt` | Any single token tree | Last resort; combinators |

## Trailing-Comma Pattern

Allow an optional trailing comma in repetitions without requiring a follow-set workaround:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Trailing-Comma Pattern illustration -->
```rust
macro_rules! my_vec {
    ($($e:expr),* $(,)?) => {
        // $(,)? consumes an optional trailing comma, which is legal after :expr
        // because it appears as a separator/terminator, not in follow position.
        vec![$($e),*]
    };
}

let v = my_vec![1, 2, 3,]; // trailing comma accepted
```

## Related Rules
- [macro-rules-hygiene](macro-rules-hygiene.md) - hygiene and `$crate` for declarative macros
- [macro-prefer-functions](macro-prefer-functions.md) - when a function is a better choice
