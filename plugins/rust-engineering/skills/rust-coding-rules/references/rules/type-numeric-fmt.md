# type-numeric-fmt

> Implement `LowerHex`, `UpperHex`, `Octal`, and `Binary` for numeric newtypes

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-traits; supporters=`rust-api-design`, `rust-ownership`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Implement `LowerHex`, `UpperHex`, `Octal`, and `Binary` for numeric newtypes.

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

Rust's API Guidelines (C-NUM-FMT) state that numeric types should support `{:x}`, `{:X}`, `{:o}`, and `{:b}` wherever the underlying integer type does. A numeric newtype that silently drops these format specifiers is an ergonomic regression — callers who reach for `{:x}` to debug a bitmask or address will hit a compile error instead. The fix is a one-liner per trait that forwards to the inner value's formatter.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use std::fmt;

struct Mask(u32);

impl fmt::Display for Mask {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

fn main() {
    let m = Mask(0xDEAD_BEEF);
    println!("{}", m);   // ok
    // println!("{:x}", m); // compile error: Mask doesn't implement LowerHex
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct Mask(u32);

impl fmt::Display for Mask {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Display::fmt(&self.0, f)
    }
}

impl fmt::LowerHex for Mask {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::LowerHex::fmt(&self.0, f)
    }
}

impl fmt::UpperHex for Mask {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::UpperHex::fmt(&self.0, f)
    }
}

impl fmt::Octal for Mask {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Octal::fmt(&self.0, f)
    }
}

impl fmt::Binary for Mask {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Binary::fmt(&self.0, f)
    }
}

fn main() {
    let m = Mask(0xDEAD_BEEF);
    println!("{m}");          // 3735928559
    println!("{m:x}");        // deadbeef
    println!("{m:X}");        // DEADBEEF
    println!("{m:#010x}");    // 0xdeadbeef
    println!("{m:o}");        // 33653337357
    println!("{m:b}");        // 11011110101011011011111011101111
}
```

## Notes

- Forward through the inner type's trait implementation (e.g., `fmt::LowerHex::fmt(&self.0, f)`) so that format flags like `#`, `0`, and width are handled correctly by the inner type.
- Apply this to any newtype whose inner type is a primitive integer (`u8`–`u128`, `i8`–`i128`, `usize`, `isize`).
- Skip `Octal`/`Binary` if there is genuinely no domain reason to print the value in those bases (e.g., a purely decimal `Count` newtype), but always implement `LowerHex`/`UpperHex` for any mask, address, or identifier type.

## Related Rules
- [type-newtype-ids](type-newtype-ids.md) - wrapping IDs and numeric values in newtypes
- [type-display-vs-debug](type-display-vs-debug.md) - choosing between `Display` and `Debug`
