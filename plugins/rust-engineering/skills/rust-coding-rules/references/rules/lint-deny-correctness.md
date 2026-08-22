# lint-deny-correctness

> `#![deny(clippy::correctness)]`

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-style-clippy; supporters=`rust-stable`, `rust-cargo-build`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: `#![deny(clippy::correctness)]`.

## Apply When

Apply when the repository needs a scoped formatting, lint, warning-level, cfg, or CI policy under its actual toolchain, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when a broad lint group or automatic fix would change API, MSRV, semantics, generated code, or unrelated dirty files. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Reproduce the exact lint, classify it, fix semantic causes individually, and use the narrowest documented allow for intentional exceptions.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Bad

Applying the headline as a universal rewrite without proving its premise, prerequisites, and caller-visible effects.

## Good

Apply the rule only to the demonstrated boundary, preserve the controlling contract, and retain evidence for the changed property.

## Trade-offs

Stricter lint policy catches defects earlier but increases toolchain churn, exception maintenance, and migration work.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.

## Verification

Run the configured format and Clippy gate with exact packages, targets, features, and toolchain; separate baseline failures.

## Why It Matters

Clippy's correctness lints catch code that is outright wrong - logic errors, undefined behavior, or code that doesn't do what you think. These should always be errors, not warnings.

## Setup

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Setup illustration -->
```rust
// At the top of lib.rs or main.rs
#![deny(clippy::correctness)]

// Or in Cargo.toml for workspace-wide
[lints.clippy]
correctness = "deny"
```

## What It Catches

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the What It Catches illustration -->
```rust
// Infinite loop (iter::repeat without take)
for x in std::iter::repeat(1) {  // ERROR: infinite iterator
    println!("{}", x);
}

// Comparison to NaN (always false)
if x == f64::NAN {  // ERROR: NaN != NaN always
    // This never executes
}

// Use after free patterns
let r;
{
    let x = 5;
    r = &x;  // ERROR: x dropped here
}
println!("{}", r);

// Wrong equality check
if x = 5 {  // ERROR: assignment in condition (should be ==)
}

// Useless comparisons
if x >= 0 && x < 0 {  // ERROR: impossible condition
}
```

## Important Correctness Lints

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Important Correctness Lints illustration -->
```rust
// approx_constant - using imprecise PI, E values
let pi = 3.14;  // Use std::f64::consts::PI

// invalid_regex - regex that won't compile
let re = Regex::new("[");  // Invalid regex

// iter_next_loop - using .next() in for loop incorrectly
for x in iter.next() {  // Should be: for x in iter

// never_loop - loop that never actually loops
loop {
    break;  // Always breaks immediately
}

// nonsensical_open_options - impossible file options
File::options().read(false).write(false).open("f");

// unit_cmp - comparing unit type ()
if foo() == bar() { }  // Both return (), always true
```

## Full Recommended Lints

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Full Recommended Lints illustration -->
```rust
#![deny(clippy::correctness)]
#![warn(clippy::suspicious)]
#![warn(clippy::style)]
#![warn(clippy::complexity)]
#![warn(clippy::perf)]

// For published crates
#![warn(missing_docs)]
#![warn(clippy::cargo)]
```

## Running Clippy

```bash
# Basic check
cargo clippy

# With all warnings as errors
cargo clippy -- -D warnings

# Check specific lint category
cargo clippy -- -W clippy::correctness

# In CI (fail on warnings)
cargo clippy -- -D warnings -D clippy::correctness
```

## Related Rules
- [lint-warn-suspicious](lint-warn-suspicious.md) - Warn on suspicious code
- [lint-warn-perf](lint-warn-perf.md) - Warn on performance issues
