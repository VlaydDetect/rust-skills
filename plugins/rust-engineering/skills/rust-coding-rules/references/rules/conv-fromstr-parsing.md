# conv-fromstr-parsing

> Implement `FromStr` to enable `str::parse` for string-to-type conversions## Decision

Consider this rule only after its prerequisites are satisfied: Implement `FromStr` to enable `str::parse` for string-to-type conversions.

## Apply When

Apply when a conversion has stable ownership, validation, loss, or error semantics worth expressing through standard traits, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the conversion is ambiguous, lossy without an explicit name, or broad generic acceptance would hide cost or meaning. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Classify the conversion as borrowed, infallible, fallible, parsing, or lossy, then select the narrowest standard trait or named method.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Standard conversion traits improve composition but become broad API commitments and can create surprising inference or allocation.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`serde`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Test valid, invalid, boundary, round-trip, allocation, and error behavior and compile representative inference contexts.

## Why It Matters

`FromStr` is the single standard hook for parsing a `&str` into a typed value. Implementing it unlocks the idiomatic `.parse::<T>()` call, integrates with CLI argument parsers (clap, argh), and is the expected interface for serde string-deserializable types. A bespoke `fn parse_foo(s: &str)` forces callers to learn a private name and breaks generic code that constrains `T: FromStr`.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
#[derive(Debug)]
enum Color { Red, Green, Blue }

// Callers must know this private name; no `.parse()` support
fn parse_color(s: &str) -> Result<Color, String> {
    match s {
        "red"   => Ok(Color::Red),
        "green" => Ok(Color::Green),
        "blue"  => Ok(Color::Blue),
        other   => Err(format!("unknown color: {other}")),
    }
}

fn main() {
    let c = parse_color("red").unwrap();
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::str::FromStr;
use std::fmt;

#[derive(Debug, PartialEq)]
enum Color { Red, Green, Blue }

#[derive(Debug)]
struct ParseColorError(String);

impl fmt::Display for ParseColorError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "unknown color: {}", self.0)
    }
}

impl std::error::Error for ParseColorError {}

impl FromStr for Color {
    type Err = ParseColorError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "red"   => Ok(Color::Red),
            "green" => Ok(Color::Green),
            "blue"  => Ok(Color::Blue),
            other   => Err(ParseColorError(other.to_owned())),
        }
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Standard idiom — works with clap, config parsers, etc.
    let c: Color = "green".parse()?;
    assert_eq!(c, Color::Green);
    Ok(())
}
```

## Notes

- Use a concrete `Err` type, not `String`, so callers can pattern-match on parse failures.
- `FromStr` pairs naturally with `Display`: if you can parse it in, you should be able to print it out.
- For infallible string conversions (e.g., wrapping a `String` in a newtype), consider `From<&str>` or `From<String>` instead.
- CLI crates like `clap` detect `FromStr` automatically via the `value_parser` attribute macro.

## Related Rules
- [conv-tryfrom-fallible](conv-tryfrom-fallible.md) - `TryFrom` for fallible non-string conversions
- [type-newtype-validated](type-newtype-validated.md) - newtypes for validated data like `Email`, `Url`
- [api-parse-dont-validate](api-parse-dont-validate.md) - parse into validated types at boundaries
