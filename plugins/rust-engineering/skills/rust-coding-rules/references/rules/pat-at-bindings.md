# pat-at-bindings

> Use `@` bindings to capture a value while matching it against a pattern

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-idioms; supporters=`rust-stable`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `@` bindings to capture a value while matching it against a pattern.

## Apply When

Apply when pattern syntax can make state extraction, exhaustiveness, guards, or early return clearer without changing behavior, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the syntax exceeds the declared MSRV or a catch-all would hide a meaningful future or current variant. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. List the states and binding needs, choose exhaustive matching or a deliberate fallback, and preserve evaluation and drop order.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Concise patterns can improve clarity, while dense nesting or broad catch-alls can obscure control flow and evolution.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`bytes`) must already be accepted by the project or be approved before addition.

## Verification

Compile under the declared toolchain and test every meaningful variant, guard boundary, and fallback behavior.

## Why It Matters

The `name @ pattern` syntax binds the matched value to `name` and simultaneously tests it against `pattern` in a single arm. Without `@`, you either re-access the original expression (verbose) or add a guard that repeats the condition and re-extracts the value (redundant). `@` bindings make the constraint and the binding a single, readable unit.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
fn classify(n: u32) -> String {
    match n {
        1..=9 => format!("single digit: {n}"), // fine here — n is Copy and in scope
        10..=99 => {
            let tens = n; // no real benefit; contrived but shows the pattern
            format!("two digits: {tens}")
        }
        _ => String::from("large"),
    }
}

// More revealing: nested struct field — must re-access after matching range
#[derive(Debug)]
enum Command {
    Move { x: i32, y: i32 },
}

fn validate_move(cmd: &Command) {
    match cmd {
        Command::Move { x, y } if *x >= 0 && *x <= 100 => {
            // x is already bound, so this is fine, but the guard duplicates the range
            println!("valid move to x={x}, y={y}");
        }
        _ => println!("invalid command"),
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
fn classify(n: u32) -> String {
    match n {
        id @ 1..=9 => format!("single digit: {id}"),
        id @ 10..=99 => format!("two digits: {id}"),
        _ => String::from("large"),
    }
}

// Nested struct field with @ binding
#[derive(Debug)]
enum Command {
    Move { x: i32, y: i32 },
}

fn validate_move(cmd: &Command) {
    match cmd {
        Command::Move { x: x_pos @ 0..=100, y } => {
            println!("valid move to x={x_pos}, y={y}");
        }
        _ => println!("invalid command"),
    }
}
```

`x: x_pos @ 0..=100` destructures the `x` field, checks that it falls in `0..=100`, and binds the value to `x_pos` — all in one expression.

## Binding an Enum Variant While Inspecting Its Payload

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Binding an Enum Variant While Inspecting Its Payload illustration -->
```rust
#[derive(Debug, Clone)]
enum Packet {
    Data(Vec<u8>),
    Control(u8),
}

fn log_data(packet: &Packet) {
    match packet {
        whole @ Packet::Data(bytes) if !bytes.is_empty() => {
            println!("non-empty packet: {whole:?}");
        }
        Packet::Data(_) => println!("empty data packet"),
        Packet::Control(code) => println!("control: {code}"),
    }
}
```

`whole` captures the entire `Packet::Data(...)` value while the guard checks the payload — no need to reconstruct the variant for logging.

## Notes

- `@` bindings work in all pattern positions: `match`, `if let`, `while let`, `let ... else`, and function parameters.
- Clippy lint `clippy::bind_instead_of_map` is unrelated but similarly reduces redundant re-access patterns.

## Related Rules
- [pat-exhaustive-enum](pat-exhaustive-enum.md) - match enums exhaustively to catch new variants
- [type-enum-states](type-enum-states.md) - use enums for mutually exclusive states
