# name-no-get-prefix

> Omit get_ prefix for simple getters## Decision

Use this context-sensitive Rust decision when its premise is established: Omit get_ prefix for simple getters.

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

Rust convention omits the `get_` prefix for simple field access. Methods like `len()`, `name()`, `value()` are cleaner than `get_len()`, `get_name()`, `get_value()`. This follows the principle of making the common case concise.

The `get` prefix is reserved for methods that DO something beyond simple field access.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
struct User {
    name: String,
    age: u32,
}

impl User {
    fn get_name(&self) -> &str {      // Verbose
        &self.name
    }
    
    fn get_age(&self) -> u32 {         // Verbose
        self.age
    }
    
    fn get_is_adult(&self) -> bool {   // Doubly verbose
        self.age >= 18
    }
}

let name = user.get_name();
let age = user.get_age();
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
struct User {
    name: String,
    age: u32,
}

impl User {
    fn name(&self) -> &str {           // Clean
        &self.name
    }
    
    fn age(&self) -> u32 {             // Clean
        self.age
    }
    
    fn is_adult(&self) -> bool {       // Boolean uses is_ prefix
        self.age >= 18
    }
}

let name = user.name();
let age = user.age();
```

## When get_ IS Appropriate

Use `get` when the method does more than simple access:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When get IS Appropriate illustration -->
```rust
impl HashMap<K, V> {
    // Returns Option - not just field access
    fn get(&self, key: &K) -> Option<&V> { }
    
    // Mutable variant
    fn get_mut(&mut self, key: &K) -> Option<&mut V> { }
}

impl Vec<T> {
    // Returns Option - bounds checked
    fn get(&self, index: usize) -> Option<&T> { }
}

impl Context {
    // Does computation/lookup, not just field access
    fn get_config(&self) -> Config {
        self.configs.get(&self.current_env).cloned().unwrap_or_default()
    }
}
```

## Standard Library Examples

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Standard Library Examples illustration -->
```rust
// No get_ prefix
String::len()
Vec::len()
Vec::capacity()
Vec::is_empty()
Path::file_name()
Option::is_some()
Result::is_ok()

// With get - returns Option or does lookup
Vec::get(index)
HashMap::get(key)
BTreeMap::get(key)
```

## Pattern: Getter/Setter Pairs

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Getter/Setter Pairs illustration -->
```rust
impl Config {
    // Getter: no prefix
    fn timeout(&self) -> Duration {
        self.timeout
    }
    
    // Setter: use set_ prefix
    fn set_timeout(&mut self, timeout: Duration) {
        self.timeout = timeout;
    }
}
```

## Pattern: Builder Methods

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Builder Methods illustration -->
```rust
impl ConfigBuilder {
    // Builder methods: no get_, no set_
    fn timeout(mut self, timeout: Duration) -> Self {
        self.timeout = timeout;
        self
    }
    
    fn retries(mut self, retries: u32) -> Self {
        self.retries = retries;
        self
    }
}
```

## Decision Guide

| Pattern | Naming |
|---------|--------|
| Simple field access | `name()`, `value()`, `len()` |
| Boolean property | `is_valid()`, `has_items()` |
| Fallible access | `get()`, `get_mut()` |
| Setter | `set_name()`, `set_value()` |
| Builder | `name()`, `value()` (consuming self) |

## Related Rules
- [name-is-has-bool](./name-is-has-bool.md) - Boolean naming
- [name-is-has-bool](./name-is-has-bool.md) - Boolean naming
- [api-builder-pattern](./api-builder-pattern.md) - Builder pattern
