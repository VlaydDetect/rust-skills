# const-block

> Use inline `const { }` blocks for compile-time evaluation and assertions

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-stable; supporters=`rust-stdlib`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Use inline `const { }` blocks for compile-time evaluation and assertions.

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

A `const { }` block (stabilized in Rust 1.79) forces the enclosed expression to be evaluated at compile time, even inside a regular function. This has three practical uses: compile-time assertions that fail the build rather than panicking at runtime; precomputed values inlined at the exact call site without a named `const` item; and initializing arrays of non-`Copy` types that require a per-element constant expression. Catching invariant violations at compile time gives a clearer error message and zero runtime cost.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
const SIZE: usize = 64;

fn process(buf: &[u8]) {
    // runtime panic — error surface is deferred until execution
    assert!(SIZE.is_power_of_two(), "SIZE must be a power of two");
    assert!(buf.len() <= SIZE);
}

// repeated magic number — easy to get out of sync
fn header() -> [u8; 4] {
    [0u8; 4]
}

// initializing array of non-Copy type requires unsafe or a workaround without const blocks
// std::array::from_fn is fine, but const blocks make the intent clearer for const values
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
const SIZE: usize = 64;

fn process(buf: &[u8]) {
    // compile-time assertion — build fails immediately if SIZE changes to a bad value
    const { assert!(SIZE.is_power_of_two(), "SIZE must be a power of two") };

    // runtime assertion for dynamic data still makes sense here
    assert!(buf.len() <= SIZE);
}

// inline const block used as a value — evaluated once, inlined at each use
fn magic_header() -> u32 {
    const { 0xDEAD_BEEFu32.swap_bytes() }
}

// compile-time bounds check on a type-level relationship
struct Packet<const HDR: usize, const BODY: usize>;

impl<const HDR: usize, const BODY: usize> Packet<HDR, BODY> {
    fn new() -> Self {
        // fails at compile time if the relationship is violated, not at runtime
        const { assert!(HDR + BODY <= 1500, "packet exceeds ethernet MTU") };
        Packet
    }
}

// array of non-Copy type using a const block per element
// (each element is its own const expression — legal since 1.79)
fn make_table() -> [u64; 4] {
    [
        const { u64::MAX / 1 },
        const { u64::MAX / 2 },
        const { u64::MAX / 3 },
        const { u64::MAX / 4 },
    ]
}
```

## Notes

`const { expr }` is an expression, so it can appear anywhere an expression is valid: in function bodies, match arms, array initializers, and as default values. It is distinct from a named `const ITEM: T = expr;` declaration — a `const` block is anonymous and scoped to its enclosing expression. For long-lived or widely shared values, prefer a named `const`; reach for `const { }` when you want a one-off compile-time guarantee or value inline.

## Related Rules
- [const-fn](const-fn.md) - write functions callable in const contexts
- [mem-assert-type-size](mem-assert-type-size.md) - assert hot type sizes to prevent layout regressions
