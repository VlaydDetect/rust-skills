# name-into-ownership

> Use `into_` prefix for ownership-consuming conversions

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-api-design; supporters=`rust-style-clippy`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `into_` prefix for ownership-consuming conversions.

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
- External crates referenced by the source (`bytes`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Compile callers and docs, run configured naming lints, and perform compatibility analysis for public renames.

## Why It Matters

The `into_` prefix signals "this method consumes self and returns something else." The original value is moved and no longer usable. This ownership transfer is usually cheap (no allocation), but the caller loses access to the original. Clear naming prevents "use after move" confusion.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
impl Wrapper {
    // Misleading: doesn't indicate ownership transfer
    fn get_inner(self) -> Inner {  
        self.inner
    }
    
    // Misleading: suggests borrowing
    fn as_inner(self) -> Inner {  // Takes self by value!
        self.inner
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
impl Wrapper {
    // into_ clearly shows ownership transfer
    fn into_inner(self) -> Inner {
        self.inner
    }
}

// Usage is clear
let wrapper = Wrapper::new(inner);
let inner = wrapper.into_inner();  // wrapper is consumed
// wrapper.foo();  // Error: use of moved value
```

## Standard Library Examples

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Standard Library Examples illustration -->
```rust
// All consume self and return owned data
let string: String = "hello".to_string();
let bytes: Vec<u8> = string.into_bytes();  // String consumed

let path = PathBuf::from("/foo");
let os_string: OsString = path.into_os_string();  // PathBuf consumed

let boxed: Box<[i32]> = vec![1, 2, 3].into_boxed_slice();  // Vec consumed

let vec: Vec<u8> = boxed.into_vec();  // Box consumed
```

## into_iter() Pattern

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the intoiter() Pattern illustration -->
```rust
let vec = vec![1, 2, 3];

// into_iter consumes the collection
for item in vec.into_iter() {  // or just: for item in vec
    // item is i32, not &i32
}
// vec is consumed, can't use anymore

// Contrast with iter() which borrows
let vec = vec![1, 2, 3];
for item in vec.iter() {
    // item is &i32
}
// vec still usable
```

## IntoIterator Trait

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the IntoIterator Trait illustration -->
```rust
impl IntoIterator for MyCollection {
    type Item = Element;
    type IntoIter = std::vec::IntoIter<Element>;
    
    fn into_iter(self) -> Self::IntoIter {
        self.elements.into_iter()  // Consumes self
    }
}
```

## Conversion Prefix Summary

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Conversion Prefix Summary illustration -->
```rust
struct Buffer {
    data: Vec<u8>,
    name: String,
}

impl Buffer {
    // as_ : free borrow, returns reference
    fn as_slice(&self) -> &[u8] {
        &self.data
    }
    
    // to_ : allocates, creates new value
    fn to_vec(&self) -> Vec<u8> {
        self.data.clone()
    }
    
    // into_ : consumes self, usually cheap
    fn into_inner(self) -> Vec<u8> {
        self.data
    }
    
    // into_ : can destructure into parts
    fn into_parts(self) -> (Vec<u8>, String) {
        (self.data, self.name)
    }
}
```

## Related Rules
- [name-as-free](./name-as-free.md) - Borrowing conversions
- [name-to-expensive](./name-to-expensive.md) - Allocating conversions
- [api-from-not-into](./api-from-not-into.md) - From trait implementation
