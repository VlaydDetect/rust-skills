# pat-let-else

> Use `let ... else` for early-return pattern extraction## Decision

Consider this rule only after its prerequisites are satisfied: Use `let ... else` for early-return pattern extraction.

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
- External crates referenced by the source (`anyhow`) must already be accepted by the project or be approved before addition.

## Verification

Compile under the declared toolchain and test every meaningful variant, guard boundary, and fallback behavior.

## Why It Matters

`let ... else` (stable since Rust 1.65) binds a pattern in the success path or diverges in the `else` branch. It keeps the happy path at the top indentation level and eliminates rightward drift that accumulates when nesting multiple `if let` blocks. The `else` block must diverge via `return`, `continue`, `break`, or a macro like `panic!` or `bail!`.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
fn process(input: Option<String>) -> Option<u32> {
    if let Some(s) = input {
        if let Ok(n) = s.trim().parse::<u32>() {
            if n > 0 {
                return Some(n * 2);
            } else {
                return None;
            }
        } else {
            return None;
        }
    } else {
        return None;
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
fn process(input: Option<String>) -> Option<u32> {
    let Some(s) = input else { return None; };
    let Ok(n) = s.trim().parse::<u32>() else { return None; };
    if n == 0 {
        return None;
    }
    Some(n * 2)
}
```

Multiple extractions stay flat, each guarding against one failure mode before the next line runs.

## Using with `anyhow` / `bail!`

The `else` block can use any diverging expression, including macros:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Using with anyhow / bail! illustration -->
```rust
use anyhow::{bail, Result};

fn get_id(map: &std::collections::HashMap<String, u64>, key: &str) -> Result<u64> {
    let Some(&id) = map.get(key) else {
        bail!("key '{}' not found", key);
    };
    Ok(id)
}
```

## Notes

- The bound variable is in scope **after** the `let` statement, not inside the `else` block.
- Prefer `?` when the `else` branch would just propagate an error; `let ... else` shines when the divergence is a `return`, `continue`, or `break`.
- Clippy lint `clippy::manual_let_else` flags patterns that can be converted.

## Related Rules
- [err-question-mark](err-question-mark.md) - use `?` for error propagation
- [anti-unwrap-abuse](anti-unwrap-abuse.md) - avoid `.unwrap()` in production code
- [pat-exhaustive-enum](pat-exhaustive-enum.md) - match enums exhaustively
