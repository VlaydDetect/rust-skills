# name-iter-convention

> Use iter/iter_mut/into_iter for iterator methods

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-api-design; supporters=`rust-style-clippy`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Use iter/iter_mut/into_iter for iterator methods.

## Apply When

Apply when an identifier is part of a Rust caller contract or repository convention and its name communicates cost, ownership, state, or behavior, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when a rename would create compatibility churn without improving meaning or merely enforces taste already handled by tooling. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Classify the item and semantic operation, follow Rust convention and local vocabulary, then check public-path compatibility.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Good

Apply the rule only to the demonstrated boundary, preserve the controlling contract, and retain evidence for the changed property.

## Trade-offs

Conventional names improve discoverability but public renames can impose migration and deprecation costs.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Compile callers and docs, run configured naming lints, and perform compatibility analysis for public renames.

## Why It Matters

Rust has a standard convention for iterator method names that signals ownership semantics. Following this convention makes APIs predictable and enables the `for item in collection` syntax to work correctly.

## The Three Iterator Methods

| Method | Returns | Ownership |
|--------|---------|-----------|
| `iter()` | `impl Iterator<Item = &T>` | Borrows collection |
| `iter_mut()` | `impl Iterator<Item = &mut T>` | Mutably borrows |
| `into_iter()` | `impl Iterator<Item = T>` | Consumes collection |

## Implementation

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Implementation illustration -->
```rust
struct MyCollection<T> {
    items: Vec<T>,
}

impl<T> MyCollection<T> {
    /// Returns an iterator over references.
    fn iter(&self) -> impl Iterator<Item = &T> {
        self.items.iter()
    }
    
    /// Returns an iterator over mutable references.
    fn iter_mut(&mut self) -> impl Iterator<Item = &mut T> {
        self.items.iter_mut()
    }
}

// IntoIterator trait for into_iter()
impl<T> IntoIterator for MyCollection<T> {
    type Item = T;
    type IntoIter = std::vec::IntoIter<T>;
    
    fn into_iter(self) -> Self::IntoIter {
        self.items.into_iter()
    }
}

// Also implement for references
impl<'a, T> IntoIterator for &'a MyCollection<T> {
    type Item = &'a T;
    type IntoIter = std::slice::Iter<'a, T>;
    
    fn into_iter(self) -> Self::IntoIter {
        self.items.iter()
    }
}

impl<'a, T> IntoIterator for &'a mut MyCollection<T> {
    type Item = &'a mut T;
    type IntoIter = std::slice::IterMut<'a, T>;
    
    fn into_iter(self) -> Self::IntoIter {
        self.items.iter_mut()
    }
}
```

## Usage

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Usage illustration -->
```rust
let collection = MyCollection { items: vec![1, 2, 3] };

// Explicit methods
for x in collection.iter() { }     // Borrows
for x in collection.iter_mut() { } // Mutably borrows

// IntoIterator enables for loop syntax
for x in &collection { }      // Calls (&collection).into_iter()
for x in &mut collection { }  // Calls (&mut collection).into_iter()
for x in collection { }       // Consumes, calls collection.into_iter()
```

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
impl MyCollection<T> {
    // Non-standard names
    fn elements(&self) -> impl Iterator<Item = &T> { }      // Should be iter()
    fn get_items(&self) -> impl Iterator<Item = &T> { }     // Should be iter()
    fn iterate(&self) -> impl Iterator<Item = &T> { }       // Should be iter()
    fn as_iter(&self) -> impl Iterator<Item = &T> { }       // Should be iter()
}
```

## Additional Iterator Methods

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Additional Iterator Methods illustration -->
```rust
impl MyCollection<T> {
    // Filter by predicate
    fn iter_valid(&self) -> impl Iterator<Item = &T> {
        self.iter().filter(|x| x.is_valid())
    }
    
    // Specific slice
    fn iter_range(&self, start: usize, end: usize) -> impl Iterator<Item = &T> {
        self.items[start..end].iter()
    }
}
```

## Standard Library Examples

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Standard Library Examples illustration -->
```rust
// Vec, slice, arrays
vec.iter()      // &T
vec.iter_mut()  // &mut T
vec.into_iter() // T

// HashMap
map.iter()      // (&K, &V)
map.iter_mut()  // (&K, &mut V)
map.into_iter() // (K, V)
map.keys()      // &K
map.values()    // &V
```

## Related Rules
- [name-iter-type-match](./name-iter-type-match.md) - Iterator type naming
- [name-iter-method](./name-iter-method.md) - Iterator method names
- [perf-iter-over-index](./perf-iter-over-index.md) - Prefer iterators
