# name-funcs-snake

> Use `snake_case` for functions, methods, variables, and modules## Decision

Use this context-sensitive Rust decision when its premise is established: Use `snake_case` for functions, methods, variables, and modules.

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

Rust uses `snake_case` for "value-level" names—functions, methods, variables, modules. This convention is enforced by the compiler and distinguishes runtime entities from types. Consistent naming makes code scannable and predictable.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// CamelCase functions - compiler warns
fn calculateTotal() -> f64 { ... }  // warning: function `calculateTotal` should have a snake case name
fn getUserName() -> String { ... }  // warning

// Inconsistent naming
fn get_user() -> User { ... }
fn fetchOrder() -> Order { ... }  // Mixed conventions
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// snake_case for functions
fn calculate_total() -> f64 { ... }
fn get_user_name() -> String { ... }
fn fetch_order() -> Order { ... }

// snake_case for methods
impl User {
    fn full_name(&self) -> String { ... }
    fn is_active(&self) -> bool { ... }
    fn set_email(&mut self, email: &str) { ... }
}

// snake_case for variables
let user_count = 42;
let max_connections = 100;
let is_valid = true;

// snake_case for modules
mod user_service;
mod http_client;
mod json_parser;
```

## Acronyms in snake_case

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Acronyms in snakecase illustration -->
```rust
// Lowercase acronyms in snake_case
fn parse_json() -> Json { ... }   // Not parse_JSON
fn connect_tcp() -> TcpStream { ... }   // Not connect_TCP
fn generate_uuid() -> Uuid { ... }      // Not generate_UUID

let http_response = fetch();
let json_data = parse();
```

## Local Variables

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Local Variables illustration -->
```rust
fn process_data(input_data: &[u8]) -> Result<Output, Error> {
    let raw_bytes = input_data;
    let decoded_string = decode(raw_bytes)?;
    let parsed_value = parse(&decoded_string)?;
    let final_result = transform(parsed_value)?;
    
    Ok(final_result)
}
```

## Related Rules
- [name-types-camel](./name-types-camel.md) - Type naming
- [name-consts-screaming](./name-consts-screaming.md) - Constant naming
- [name-lifetime-short](./name-lifetime-short.md) - Lifetime naming
