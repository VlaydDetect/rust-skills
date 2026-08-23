# conv-tryfrom-fallible

> Implement `TryFrom` for fallible conversions instead of ad-hoc conversion functions## Decision

Use this context-sensitive Rust decision when its premise is established: Implement `TryFrom` for fallible conversions instead of ad-hoc conversion functions.

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
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Test valid, invalid, boundary, round-trip, allocation, and error behavior and compile representative inference contexts.

## Why It Matters

`TryFrom`/`TryInto` is the standard trait pair for conversions that can fail. Implementing `TryFrom<T>` automatically provides `TryInto` for callers (API Guidelines C-CONV-TRAITS), enabling ergonomic `.try_into()?` at call sites. It integrates naturally with the `?` operator, ecosystem crates, and generic bounds that constrain `T: TryFrom<U>`. Ad-hoc conversion functions scatter the conversion surface and deprive callers of these benefits.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use std::io;

struct Port(u16);

// Bespoke function — callers must know its name, can't use `.try_into()`
fn port_from_u32(n: u32) -> Result<Port, String> {
    if n > u16::MAX as u32 {
        return Err(format!("port {} out of range", n));
    }
    Ok(Port(n as u16))
}

fn main() {
    let p = port_from_u32(8080).unwrap();
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::fmt;

#[derive(Debug)]
struct Port(u16);

#[derive(Debug)]
struct PortError(u32);

impl fmt::Display for PortError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "port {} is out of range (0–65535)", self.0)
    }
}

impl std::error::Error for PortError {}

impl TryFrom<u32> for Port {
    type Error = PortError;

    fn try_from(value: u32) -> Result<Self, Self::Error> {
        u16::try_from(value)
            .map(Port)
            .map_err(|_| PortError(value))
    }
}

fn accept_port(n: u32) -> Result<Port, PortError> {
    // Callers use the standard `.try_into()?` idiom
    n.try_into()
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let p: Port = 8080_u32.try_into()?;
    println!("port: {}", p.0);
    Ok(())
}
```

## Notes

- Implement `TryFrom`, not `TryInto`; the blanket impl provides `TryInto` automatically (mirrors the `From`/`Into` relationship).
- Use a concrete error type, not `String` or `Box<dyn Error>`, so callers can match on it.
- When the conversion is truly infallible, implement `From` instead.

## Related Rules
- [api-from-not-into](api-from-not-into.md) - implement `From`, not `Into`, for the same reason
- [conv-fromstr-parsing](conv-fromstr-parsing.md) - standard hook for string→type parsing
- [api-parse-dont-validate](api-parse-dont-validate.md) - parse into validated types at boundaries
