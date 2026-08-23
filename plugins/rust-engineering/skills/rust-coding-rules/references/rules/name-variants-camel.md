# name-variants-camel

> Use `UpperCamelCase` for enum variants## Decision

Use this context-sensitive Rust decision when its premise is established: Use `UpperCamelCase` for enum variants.

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
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Compile callers and docs, run configured naming lints, and perform compatibility analysis for public renames.

## Why It Matters

Enum variants follow the same naming convention as types—`UpperCamelCase`. This distinguishes them from fields, variables, and functions. The compiler warns on violations, and consistent naming helps readers instantly recognize variant names.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
enum Status {
    pending,       // warning: variant `pending` should have an upper camel case name
    in_progress,   // warning
    COMPLETED,     // Not idiomatic
}

enum Color {
    RED,           // Screaming case - not Rust style
    GREEN,
    BLUE,
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
enum Status {
    Pending,
    InProgress,
    Completed,
    Failed,
}

enum Color {
    Red,
    Green,
    Blue,
    Custom(u8, u8, u8),
}

enum HttpMethod {
    Get,
    Post,
    Put,
    Delete,
    Patch,
}
```

## Variants with Data

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Variants with Data illustration -->
```rust
enum Message {
    // Unit variant
    Quit,
    
    // Tuple variant
    Move(i32, i32),
    
    // Struct variant
    Write { text: String },
    
    // Named fields
    ChangeColor {
        red: u8,
        green: u8,
        blue: u8,
    },
}
```

## Variant Naming Tips

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Variant Naming Tips illustration -->
```rust
// Be specific
enum Error {
    NotFound,           // Good: specific
    PermissionDenied,   // Good: specific
    Error,              // Bad: vague
}

// Avoid redundant type name in variant
enum ConnectionState {
    Connected,          // Good
    Disconnected,       // Good
    ConnectionError,    // Bad: redundant "Connection"
}

// Use None/Some pattern for Option-like enums
enum MaybeValue<T> {
    Some(T),
    None,
}
```

## Related Rules
- [name-types-camel](./name-types-camel.md) - Type naming
- [api-non-exhaustive](./api-non-exhaustive.md) - Forward-compatible enums
- [type-enum-states](./type-enum-states.md) - State machine enums
