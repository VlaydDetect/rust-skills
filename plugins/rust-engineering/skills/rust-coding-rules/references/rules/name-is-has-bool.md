# name-is-has-bool

> Use `is_`, `has_`, `can_`, `should_` prefixes for boolean-returning methods## Decision

Use this context-sensitive Rust decision when its premise is established: Use `is_`, `has_`, `can_`, `should_` prefixes for boolean-returning methods.

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

Boolean methods answer yes/no questions. Prefixes like `is_`, `has_`, `can_` make the question explicit, so code reads naturally: `if user.is_active()`, `if buffer.has_remaining()`. Without prefixes, boolean methods are ambiguous and require reading documentation.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
impl User {
    // Unclear: does this check or set?
    fn active(&self) -> bool { ... }
    
    // Unclear: does this delete or check?
    fn deleted(&self) -> bool { ... }
    
    // Unclear return type
    fn admin(&self) -> bool { ... }
}

// Reading code is confusing
if user.active() { ... }  // Is this checking or activating?
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
impl User {
    // Clear: answers "is the user active?"
    fn is_active(&self) -> bool { ... }
    
    // Clear: answers "is the user deleted?"
    fn is_deleted(&self) -> bool { ... }
    
    // Clear: answers "is the user an admin?"
    fn is_admin(&self) -> bool { ... }
    
    // Clear: answers "does the user have permission X?"
    fn has_permission(&self, perm: Permission) -> bool { ... }
    
    // Clear: answers "can the user edit?"
    fn can_edit(&self) -> bool { ... }
}

// Reads naturally
if user.is_active() && user.has_permission(Permission::Write) {
    // ...
}
```

## Common Prefixes

| Prefix | Use For | Example |
|--------|---------|---------|
| `is_` | State/property check | `is_empty()`, `is_valid()`, `is_some()` |
| `has_` | Possession/containment | `has_key()`, `has_children()`, `has_remaining()` |
| `can_` | Capability/permission | `can_read()`, `can_write()`, `can_execute()` |
| `should_` | Recommendation/policy | `should_retry()`, `should_cache()` |
| `needs_` | Requirement | `needs_update()`, `needs_auth()` |
| `will_` | Future action | `will_block()`, `will_overflow()` |

## Standard Library Examples

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Standard Library Examples illustration -->
```rust
// is_ prefix
vec.is_empty()
option.is_some()
option.is_none()
result.is_ok()
result.is_err()
char.is_alphabetic()
str.is_ascii()
path.is_file()
path.is_dir()

// has_ prefix (less common in std)
iterator.has_next()  // conceptual

// Checking methods
str.contains("foo")      // Not is_ because takes argument
str.starts_with("bar")   // Descriptive verb phrase
str.ends_with("baz")
```

## Negation

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Negation illustration -->
```rust
// Prefer positive form with caller negation
if !user.is_active() { ... }

// Rather than negative method
if user.is_inactive() { ... }  // Avoid double negatives: !is_inactive()

// Exception: when negative is the common case
fn is_empty(&self) -> bool { ... }     // Checking for empty is common
fn is_not_empty(&self) -> bool { ... } // Rarely needed, use !is_empty()
```

## Boolean Fields

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Boolean Fields illustration -->
```rust
struct Config {
    // Field names can omit prefix
    enabled: bool,
    verbose: bool,
    debug: bool,
}

impl Config {
    // But methods should have prefix
    fn is_enabled(&self) -> bool {
        self.enabled
    }
    
    fn is_verbose(&self) -> bool {
        self.verbose
    }
}
```

## Related Rules
- [name-no-get-prefix](./name-no-get-prefix.md) - Getter naming
- [name-funcs-snake](./name-funcs-snake.md) - Function naming
- [api-must-use](./api-must-use.md) - Boolean functions should be checked
