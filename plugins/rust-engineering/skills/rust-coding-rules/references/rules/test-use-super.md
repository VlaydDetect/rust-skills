# test-use-super

> Use `use super::*;` in test modules to access parent module items

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-testing; supporters=`rust-verify`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `use super::*;` in test modules to access parent module items.

## Apply When

Apply when a concrete contract or risk needs the cheapest deterministic test that would fail for the defect, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the technique duplicates lower-cost coverage or adds a framework, snapshot, mock, sleep, or fuzz harness without unique risk coverage. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Map the contract to one test level and technique, isolate uncontrolled resources, and prove the assertion fails for the intended regression when practical.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Specialized test tools broaden state-space coverage but add dependencies, execution cost, maintenance, and false-stability risk.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`tempfile`, `mockall`, `proptest`) must already be accepted by the project or be approved before addition.

## Verification

Run the exact new test and its owning package or target, then record required features, runtime, seed, environment, and residual matrix.

## Why It Matters

The test module is a child of the module being tested. `use super::*` imports all items from the parent module, including private ones. This gives tests access to both public API and internal implementation details for thorough testing.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Verbose imports
#[cfg(test)]
mod tests {
    use crate::my_module::public_function;
    use crate::my_module::MyStruct;
    // Can't access private items this way!
    
    #[test]
    fn test_function() {
        let result = public_function();
        // ...
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// src/my_module.rs
pub struct PublicStruct { ... }
struct PrivateStruct { ... }  // Private

pub fn public_function() -> i32 { ... }
fn private_helper() -> i32 { ... }  // Private

#[cfg(test)]
mod tests {
    use super::*;  // Imports everything from parent
    
    #[test]
    fn test_public_struct() {
        let s = PublicStruct::new();
        // ...
    }
    
    #[test]
    fn test_private_struct() {
        let s = PrivateStruct::new();  // Can access private!
        // ...
    }
    
    #[test]
    fn test_private_helper() {
        assert_eq!(private_helper(), 42);  // Can test private!
    }
}
```

## Selective Imports

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Selective Imports illustration -->
```rust
#[cfg(test)]
mod tests {
    // When you want to be explicit
    use super::{parse, ParseError, Token};
    
    // Or import all plus test utilities
    use super::*;
    use std::fs;
    use tempfile::TempDir;
    
    #[test]
    fn test_parse() { ... }
}
```

## Nested Modules

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Nested Modules illustration -->
```rust
mod outer {
    pub fn outer_fn() -> i32 { 1 }
    
    mod inner {
        pub fn inner_fn() -> i32 { 2 }
        
        #[cfg(test)]
        mod tests {
            use super::*;           // Gets inner's items
            use super::super::*;    // Gets outer's items
            
            #[test]
            fn test_inner() {
                assert_eq!(inner_fn(), 2);
                assert_eq!(outer_fn(), 1);
            }
        }
    }
}
```

## With External Dependencies

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the With External Dependencies illustration -->
```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    // Test-only dependencies
    use proptest::prelude::*;
    use mockall::predicate::*;
    
    proptest! {
        #[test]
        fn test_property(s: String) {
            let result = process(&s);
            prop_assert!(result.is_ok());
        }
    }
}
```

## Related Rules
- [test-cfg-test-module](./test-cfg-test-module.md) - Test module structure
- [test-integration-dir](./test-integration-dir.md) - Integration tests
- [proj-pub-crate-internal](./proj-pub-crate-internal.md) - Visibility modifiers
