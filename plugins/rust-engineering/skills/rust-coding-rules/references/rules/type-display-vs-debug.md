# type-display-vs-debug

> Use `Display` for user-facing output and `Debug` for diagnostics; never swap them

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-traits; supporters=`rust-api-design`, `rust-ownership`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `Display` for user-facing output and `Debug` for diagnostics; never swap them.

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
- External crates referenced by the source (`anyhow`, `thiserror`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Use compile-pass, compile-fail, and runtime boundary cases to prove valid construction and rejection paths.

## Why It Matters

`Debug` (`{:?}`) is for developers: logs, panic messages, test assertions, and `dbg!()`. It should always be derived and reflects internal structure. `Display` (`{}`) is for end users: CLI output, error messages surfaced to humans, and log fields meant to be read in production. `std::error::Error` requires `Display` so that error chains read naturally. Routing `Debug` output to users leaks implementation details; routing `Display` output to log frameworks loses structural information.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
#[derive(Debug)]
struct ParseError {
    input: String,
    line: u32,
}

// Mistake 1: using Debug output in a user-facing message
fn report_error(e: &ParseError) {
    eprintln!("failed: {:?}", e); // leaks internal field names
}

// Mistake 2: implementing Display by calling debug
use std::fmt;
impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:?}", self) // wrong — duplicates Debug
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::fmt;

#[derive(Debug)] // derive Debug for free diagnostic output
struct ParseError {
    input: String,
    line: u32,
}

// Hand-write Display for a clean, human-readable message
impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "parse error on line {}: {:?}", self.line, self.input)
    }
}

impl std::error::Error for ParseError {}

fn main() {
    let e = ParseError { input: "foo bar".into(), line: 42 };

    // User-facing: clean sentence
    eprintln!("error: {e}");

    // Developer/log: structured dump
    eprintln!("debug: {e:?}");
}
```

## Guidelines

| Trait | Format | Audience | How to implement |
|-------|--------|----------|-----------------|
| `Debug` | `{:?}` / `{:#?}` | Developers, logs | `#[derive(Debug)]` (almost always) |
| `Display` | `{}` | End users, error messages | Hand-write to describe the condition clearly |

- Never derive `Display` — it must be intentionally written.
- `#[derive(Debug)]` on every public type (API Guidelines C-DEBUG).
- If your error type implements `std::error::Error`, its `Display` output becomes the human-readable error message that propagates through `anyhow::Context` and similar.
- The `{:#?}` pretty-print form is still `Debug`; use it in tests for readable assertion output, not in user-facing code.

## Related Rules
- [api-common-traits](api-common-traits.md) - implement `Debug`, `Clone`, `PartialEq` eagerly
- [err-thiserror-lib](err-thiserror-lib.md) - `thiserror` generates correct `Display` from `#[error("...")]`
- [type-numeric-fmt](type-numeric-fmt.md) - hex/octal/binary formatting for numeric newtypes
