# api-impl-fromiterator

> Implement `FromIterator` and `Extend` for collection types, and `IntoIterator` for all three reference forms

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-api-design; supporters=`rust-traits`, `rust-ownership`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Implement `FromIterator` and `Extend` for collection types, and `IntoIterator` for all three reference forms.

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
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Compile downstream-style examples and check docs, public paths, feature behavior, and the declared compatibility baseline.

## Why It Matters

The Rust API Guidelines (C-COLLECT) require that collection types implement `FromIterator<T>` so that `iter.collect::<MyCollection<T>>()` works. Pairing it with `Extend<T>` enables efficient batch insertion — the standard library uses `Extend` internally in `collect` when extending an existing collection. Implementing `IntoIterator` for the type itself, for `&Type`, and for `&mut Type` rounds out the contract and lets the collection participate in `for` loops and iterator adapter chains. Skipping these traits forces callers into awkward manual loops and breaks generic code.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
struct Bag<T>(Vec<T>);

impl<T> Bag<T> {
    fn new() -> Self { Bag(Vec::new()) }

    fn push(&mut self, item: T) { self.0.push(item); }
}

fn main() {
    // Callers must loop manually — no collect(), no extend(), no for loop
    let mut b = Bag::new();
    for x in [1, 2, 3] {
        b.push(x);
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
struct Bag<T>(Vec<T>);

impl<T> Bag<T> {
    fn new() -> Self { Bag(Vec::new()) }

    fn push(&mut self, item: T) { self.0.push(item); }

    fn len(&self) -> usize { self.0.len() }

    fn is_empty(&self) -> bool { self.0.is_empty() }
}

// 1. FromIterator — enables .collect::<Bag<T>>()
impl<T> FromIterator<T> for Bag<T> {
    fn from_iter<I: IntoIterator<Item = T>>(iter: I) -> Self {
        Bag(iter.into_iter().collect())
    }
}

// 2. Extend — enables .extend(iter) and is used internally by collect
impl<T> Extend<T> for Bag<T> {
    fn extend<I: IntoIterator<Item = T>>(&mut self, iter: I) {
        self.0.extend(iter);
    }
}

// 3a. IntoIterator for owned Bag (consuming)
impl<T> IntoIterator for Bag<T> {
    type Item = T;
    type IntoIter = std::vec::IntoIter<T>;

    fn into_iter(self) -> Self::IntoIter {
        self.0.into_iter()
    }
}

// 3b. IntoIterator for &Bag (borrowing)
impl<'a, T> IntoIterator for &'a Bag<T> {
    type Item = &'a T;
    type IntoIter = std::slice::Iter<'a, T>;

    fn into_iter(self) -> Self::IntoIter {
        self.0.iter()
    }
}

// 3c. IntoIterator for &mut Bag (mutable borrowing)
impl<'a, T> IntoIterator for &'a mut Bag<T> {
    type Item = &'a mut T;
    type IntoIter = std::slice::IterMut<'a, T>;

    fn into_iter(self) -> Self::IntoIter {
        self.0.iter_mut()
    }
}

fn main() {
    // collect works
    let b: Bag<i32> = [1, 2, 3].into_iter().collect();
    assert_eq!(b.len(), 3);

    // extend works
    let mut b2 = Bag::new();
    b2.extend([4, 5, 6]);
    assert_eq!(b2.len(), 3);

    // for loop works on &Bag
    for x in &b {
        let _ = x;
    }

    // map/filter chains work via IntoIterator
    let doubled: Bag<i32> = b.into_iter().map(|x| x * 2).collect();
    assert_eq!(doubled.len(), 3);
}
```

## Notes

- If your collection wraps an existing standard container, delegate `from_iter` and `extend` to the inner container's own implementations for maximum efficiency.
- `FromIterator` + `Extend` enable `collect` to call `extend` on a pre-allocated collection when possible, avoiding extra allocations.

## Related Rules
- [name-iter-convention](name-iter-convention.md) - `iter`/`iter_mut`/`into_iter` method naming
- [perf-collect-once](perf-collect-once.md) - avoid collecting intermediate iterators
- [api-common-traits](api-common-traits.md) - implement `Debug`, `Clone`, `PartialEq` eagerly
