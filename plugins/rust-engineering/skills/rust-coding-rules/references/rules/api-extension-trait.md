# api-extension-trait

> Use extension traits to add methods to external types## Decision

Consider this rule only after its prerequisites are satisfied: Use extension traits to add methods to external types.

## Apply When

Apply when a public or independently evolving caller contract needs an ownership, construction, extension, or compatibility decision, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the abstraction has only one local use or would expose implementation and dependency details without caller value. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Write representative caller examples, minimize public surface, and review ownership, errors, extension rights, and compatibility.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

More flexibility can improve call sites while increasing inference, monomorphization, compatibility, and maintenance obligations.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`tokio`, `futures`, `anyhow`, `log`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Compile downstream-style examples and check docs, public paths, feature behavior, and the declared compatibility baseline.

## Why It Matters

Rust's orphan rules prevent implementing external traits on external types. Extension traits provide a workaround: define a new trait with your methods, then implement it for the external type. This pattern is used extensively in the ecosystem (e.g., `itertools::Itertools`, `tokio::AsyncReadExt`).

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Can't add methods directly to external types
impl Vec<u8> {
    fn as_hex(&self) -> String {
        // Error: cannot define inherent impl for a type outside this crate
    }
}

// Can't implement external trait for external type
impl SomeExternalTrait for Vec<u8> {
    // Error: orphan rules violation
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Define an extension trait
pub trait ByteSliceExt {
    fn as_hex(&self) -> String;
    fn is_ascii_printable(&self) -> bool;
}

// Implement for the external type
impl ByteSliceExt for [u8] {
    fn as_hex(&self) -> String {
        self.iter()
            .map(|b| format!("{:02x}", b))
            .collect()
    }
    
    fn is_ascii_printable(&self) -> bool {
        self.iter().all(|b| b.is_ascii_graphic() || b.is_ascii_whitespace())
    }
}

// Usage: import the trait to use the methods
use my_crate::ByteSliceExt;

let data: &[u8] = b"hello";
println!("{}", data.as_hex());  // "68656c6c6f"
```

## Convention: Ext Suffix

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Convention: Ext Suffix illustration -->
```rust
// Standard naming: TypeExt for extending Type
pub trait OptionExt<T> {
    fn unwrap_or_log(self, msg: &str) -> Option<T>;
}

impl<T> OptionExt<T> for Option<T> {
    fn unwrap_or_log(self, msg: &str) -> Option<T> {
        if self.is_none() {
            log::warn!("{}", msg);
        }
        self
    }
}

// For generic extensions
pub trait ResultExt<T, E> {
    fn log_err(self) -> Self;
}

impl<T, E: std::fmt::Display> ResultExt<T, E> for Result<T, E> {
    fn log_err(self) -> Self {
        if let Err(ref e) = self {
            log::error!("{}", e);
        }
        self
    }
}
```

## Ecosystem Examples

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Ecosystem Examples illustration -->
```rust
// itertools::Itertools
use itertools::Itertools;
let groups = vec![1, 1, 2, 2, 3].into_iter().group_by(|x| *x);

// futures::StreamExt
use futures::StreamExt;
let next = stream.next().await;

// tokio::io::AsyncReadExt
use tokio::io::AsyncReadExt;
let mut buf = [0u8; 1024];
reader.read(&mut buf).await?;

// anyhow::Context
use anyhow::Context;
let content = std::fs::read_to_string(path)
    .with_context(|| format!("failed to read {}", path))?;
```

## Scoped Extensions

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Scoped Extensions illustration -->
```rust
// Extension only visible where imported
mod string_utils {
    pub trait StringExt {
        fn truncate_ellipsis(&self, max_len: usize) -> String;
    }
    
    impl StringExt for str {
        fn truncate_ellipsis(&self, max_len: usize) -> String {
            if self.len() <= max_len {
                self.to_string()
            } else {
                format!("{}...", &self[..max_len.saturating_sub(3)])
            }
        }
    }
}

// Only available when explicitly imported
use string_utils::StringExt;
let short = "very long string".truncate_ellipsis(10);
```

## Generic Extensions with Bounds

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Generic Extensions with Bounds illustration -->
```rust
pub trait VecExt<T> {
    fn push_if_unique(&mut self, item: T)
    where
        T: PartialEq;
}

impl<T> VecExt<T> for Vec<T> {
    fn push_if_unique(&mut self, item: T)
    where
        T: PartialEq,
    {
        if !self.contains(&item) {
            self.push(item);
        }
    }
}

// Works with any T: PartialEq
let mut v = vec![1, 2, 3];
v.push_if_unique(2);  // No-op
v.push_if_unique(4);  // Adds 4
```

## Related Rules
- [api-sealed-trait](./api-sealed-trait.md) - Controlling trait implementations
- [api-impl-into](./api-impl-into.md) - Using standard conversion traits
- [name-as-free](./name-as-free.md) - Naming conventions for conversions
- [trait-blanket-impl](./trait-blanket-impl.md) - Blanket impls for extension traits
