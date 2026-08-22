# name-lifetime-short

> Use short, conventional lifetime names: `'a`, `'b`, `'de`, `'src`

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-style-clippy; supporters=`rust-api-design`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use short, conventional lifetime names: `'a`, `'b`, `'de`, `'src`.

## Apply When

Apply when an identifier is part of a Rust caller contract or repository convention and its name communicates cost, ownership, state, or behavior, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when a rename would create compatibility churn without improving meaning or merely enforces taste already handled by tooling. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Classify the item and semantic operation, follow Rust convention and local vocabulary, then check public-path compatibility.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Conventional names improve discoverability but public renames can impose migration and deprecation costs.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`serde`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Compile callers and docs, run configured naming lints, and perform compatibility analysis for public renames.

## Why It Matters

Lifetime parameters are ubiquitous in Rust signatures. Short names like `'a` keep signatures readable. For domain-specific lifetimes, descriptive but short names like `'src` or `'de` communicate intent without clutter. The Rust community has established conventions that aid recognition.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Overly verbose lifetimes
fn parse<'input_lifetime, 'output_lifetime>(
    input: &'input_lifetime str
) -> Result<&'output_lifetime str, Error> { ... }

// Meaningless long names
struct Parser<'parser_instance_lifetime> {
    source: &'parser_instance_lifetime str,
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Standard short lifetimes
fn parse<'a>(input: &'a str) -> Result<&'a str, Error> { ... }

struct Parser<'a> {
    source: &'a str,
}

// Multiple lifetimes: 'a, 'b, 'c
fn merge<'a, 'b>(first: &'a str, second: &'b str) -> String { ... }

// Descriptive when clarity helps
fn deserialize<'de>(input: &'de [u8]) -> Result<Value<'de>, Error> { ... }
```

## Common Lifetime Conventions

| Lifetime | Convention | Example |
|----------|------------|---------|
| `'a` | Generic, first lifetime | `fn foo<'a>(x: &'a str)` |
| `'b` | Generic, second lifetime | `fn bar<'a, 'b>(x: &'a T, y: &'b U)` |
| `'de` | Deserialization | serde's `Deserialize<'de>` |
| `'src` | Source code/input | `struct Lexer<'src>` |
| `'ctx` | Context | `struct Query<'ctx>` |
| `'input` | Input data | `struct Parser<'input>` |
| `'static` | Static lifetime | `&'static str` |

## Elision Preferred

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Elision Preferred illustration -->
```rust
// Let elision work when possible
fn first_word(s: &str) -> &str {  // Not fn first_word<'a>(s: &'a str) -> &'a str
    s.split_whitespace().next().unwrap_or("")
}

impl User {
    fn name(&self) -> &str {  // Elision handles this
        &self.name
    }
}
```

## Serde Convention

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Serde Convention illustration -->
```rust
use serde::{Deserialize, Serialize};

// 'de is the standard serde lifetime for borrowed data
#[derive(Deserialize)]
struct Request<'de> {
    #[serde(borrow)]
    name: &'de str,
    #[serde(borrow)]
    tags: Vec<&'de str>,
}
```

## Related Rules
- [own-lifetime-elision](./own-lifetime-elision.md) - When to omit lifetimes
- [name-type-param-single](./name-type-param-single.md) - Type parameter naming
- [own-borrow-over-clone](./own-borrow-over-clone.md) - Borrowing patterns
