# const-generics

> Parameterize over values with const generics `<const N: usize>`

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-stable; supporters=`rust-stdlib`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Parameterize over values with const generics `<const N: usize>`.

## Apply When

Apply when compile-time evaluation or value parameterization enforces a useful invariant within the declared MSRV, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the feature is unavailable at the MSRV or const complexity harms diagnostics and compile time without runtime value. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Confirm stabilization and const-evaluable operations, then keep the compile-time contract smaller than the runtime API it supports.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Const evaluation can move work and errors earlier while increasing compiler work, generic surface, and MSRV coupling.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.

## Verification

Compile on the declared MSRV and primary toolchain, including boundary values and intended compile-time rejection.

## Why It Matters

Const generics let a single type or function work for any array size — or other constant value — without macros, trait objects, or carrying a runtime length field. The compiler monomorphizes one copy per distinct value, so there is no indirection and no overhead compared to hand-writing the same code for each size. This is the idiomatic way to write generic array-based data structures and algorithms on stable Rust.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// works only for one fixed size — must be copy-pasted per size
fn sum_4(arr: [i32; 4]) -> i32 {
    arr.iter().sum()
}

fn sum_8(arr: [i32; 8]) -> i32 {
    arr.iter().sum()
}

// carries runtime length — extra field, heap allocation, no compile-time bounds
struct Buffer {
    data: Vec<u8>,
    capacity: usize,
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// one generic function works for any array size; N is inferred from the argument
fn sum<const N: usize>(arr: [i32; N]) -> i32 {
    arr.iter().sum()
}

let total = sum([1, 2, 3, 4]);       // N = 4, inferred
let total8 = sum([0i32; 8]);         // N = 8, inferred

// stack-allocated buffer parameterized by capacity — no heap, no runtime length
struct Buffer<const N: usize> {
    data: [u8; N],
    len: usize,
}

impl<const N: usize> Buffer<N> {
    const fn new() -> Self {
        Self { data: [0u8; N], len: 0 }
    }

    fn push(&mut self, byte: u8) -> bool {
        if self.len < N {
            self.data[self.len] = byte;
            self.len += 1;
            true
        } else {
            false
        }
    }

    fn as_slice(&self) -> &[u8] {
        &self.data[..self.len]
    }
}

// capacity is part of the type — mismatches caught at compile time
let mut small: Buffer<8> = Buffer::new();
let mut large: Buffer<1024> = Buffer::new();
small.push(42);
large.push(99);

// const generic used as an array length computed from another const
const BLOCK: usize = 16;
fn xor_block<const N: usize>(a: [u8; N], b: [u8; N]) -> [u8; N] {
    let mut out = [0u8; N];
    for i in 0..N {
        out[i] = a[i] ^ b[i];
    }
    out
}
let result = xor_block([0u8; BLOCK], [0xFF; BLOCK]);
```

## Notes

Rust 1.65+ stabilized const generic defaults (`struct Buf<const N: usize = 64>`), letting you provide a sensible default while still allowing callers to override it. Const generics currently support integer, bool, and char types; floating-point and custom types are not yet stable. Where N can be inferred from a function argument, you rarely need to write it explicitly.

## Related Rules
- [const-fn](const-fn.md) - mark functions `const fn` so they can be called in const contexts
- [mem-assert-type-size](mem-assert-type-size.md) - assert type sizes to catch layout regressions
