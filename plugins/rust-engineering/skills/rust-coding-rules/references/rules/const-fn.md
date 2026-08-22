# const-fn

> Make functions `const fn` when they can run at compile time

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-stable; supporters=`rust-stdlib`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Make functions `const fn` when they can run at compile time.

## Apply When

Apply when compile-time evaluation or value parameterization enforces a useful invariant within the declared MSRV, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the feature is unavailable at the MSRV or const complexity harms diagnostics and compile time without runtime value. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Confirm stabilization and const-evaluable operations, then keep the compile-time contract smaller than the runtime API it supports.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Const evaluation can move work and errors earlier while increasing compiler work, generic surface, and MSRV coupling.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.

## Verification

Compile on the declared MSRV and primary toolchain, including boundary values and intended compile-time rejection.

## Why It Matters

A `const fn` can be called in const contexts — array lengths, `const`/`static` initializers, const-generic arguments — as well as at runtime, so marking a pure, simple function `const` widens where it can be used at zero cost. The compiler evaluates calls in const contexts during compilation, eliminating the work entirely from the binary. Current stable Rust supports most arithmetic, bitwise ops, conditionals, and slice operations in `const fn`; the main restrictions are heap allocation and most trait method calls.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// not const — cannot use result as an array length or const initializer
fn header_len() -> usize {
    4
}

fn magic_mask() -> u32 {
    0xFF00_FF00
}

fn make_buf() -> [u8; 8] {
    // runtime call — compiler cannot inline the length into the type
    [0u8; header_len()]  // error: `header_len` is not a `const fn`
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
const fn header_len() -> usize {
    4
}

const fn magic_mask() -> u32 {
    0xFF00_FF00
}

// usable as an array length — evaluated at compile time
let buf = [0u8; header_len()];

// usable in a const initializer
const MASK: u32 = magic_mask();

// usable in a static
static HEADER: [u8; header_len()] = [0u8; header_len()];

// const fn with logic — still fine on stable
const fn align_up(n: usize, align: usize) -> usize {
    (n + align - 1) & !(align - 1)
}

const ALIGNED: usize = align_up(13, 8); // 16, computed at compile time
```

## Notes

Adding `const` to a function is a backwards-compatible, non-breaking change for library authors. Start with `const fn` for any pure function without heap allocation or dynamic dispatch; you can always remove it if you later need a capability that is not yet `const`-stable. Avoid `const fn` for functions that call unstable `const` features not yet stabilized on the channel you target.

## Related Rules
- [const-block](const-block.md) - force compile-time evaluation and assertions inline
- [const-generics](const-generics.md) - parameterize types and functions over const values
- [opt-inline-small](opt-inline-small.md) - inline small hot functions
