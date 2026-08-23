# closure-impl-fn-return

> Return closures as `impl Fn`/`FnMut`/`FnOnce`, not `Box<dyn Fn>`## Decision

Use this context-sensitive Rust decision when its premise is established: Return closures as `impl Fn`/`FnMut`/`FnOnce`, not `Box<dyn Fn>`.

## Apply When

Apply when callback capture, call multiplicity, mutation, lifetime, storage, or dispatch semantics control the interface, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when a named function or concrete operation is clearer, or boxing and static bounds add constraints with no real storage need. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Determine capture ownership and whether the callback is Fn, FnMut, or FnOnce, then choose static or dynamic storage deliberately.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Generic closures optimize well but monomorphize; boxed callbacks erase types but add allocation and lifetime or auto-trait constraints.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.

## Verification

Compile representative captures, repeated calls, moves, thread or task transfer, and lifetime rejection cases.

## Why It Matters

`impl Fn` in return position names the closure's concrete (but unnameable) type and enables static dispatch with no heap allocation. `Box<dyn Fn>` adds an allocation and a virtual call every time the closure is invoked. The opaque `impl Trait` syntax was designed precisely for this use case. Reach for `Box<dyn Fn>` only when the function must return *different* closure types depending on runtime conditions, or when the closure must be stored in a struct field or collection.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Allocates on the heap for no benefit — single concrete closure type.
fn adder_bad(n: i32) -> Box<dyn Fn(i32) -> i32> {
    Box::new(move |x| x + n)
}

fn multiplier_bad(n: i32) -> Box<dyn Fn(i32) -> i32> {
    Box::new(move |x| x * n)
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Zero allocation, statically dispatched.
fn adder(n: i32) -> impl Fn(i32) -> i32 {
    move |x| x + n
}

fn multiplier(n: i32) -> impl Fn(i32) -> i32 {
    move |x| x * n
}

fn apply(f: impl Fn(i32) -> i32, value: i32) -> i32 {
    f(value)
}

fn demo() {
    let add5 = adder(5);
    let mul3 = multiplier(3);

    assert_eq!(apply(add5, 10), 15);
    assert_eq!(apply(mul3, 10), 30);
}
```

## Key Points

**When `Box<dyn Fn>` is required:**

Different `if`/`match` arms return distinct closure types, so `impl Fn` cannot unify them:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Key Points illustration -->
```rust
fn make_transform(double: bool) -> Box<dyn Fn(i32) -> i32> {
    if double {
        Box::new(|x| x * 2)   // one concrete type
    } else {
        Box::new(|x| x + 100) // different concrete type
    }
    // `impl Fn` would fail: "expected closure, found a different closure"
}

// Storing heterogeneous closures also requires boxing:
struct Pipeline {
    steps: Vec<Box<dyn Fn(i32) -> i32>>,
}

impl Pipeline {
    fn new() -> Self {
        Self { steps: Vec::new() }
    }

    fn add_step(&mut self, f: impl Fn(i32) -> i32 + 'static) {
        self.steps.push(Box::new(f));
    }

    fn run(&self, mut value: i32) -> i32 {
        for step in &self.steps {
            value = step(value);
        }
        value
    }
}

fn demo_pipeline() {
    let mut p = Pipeline::new();
    p.add_step(|x| x + 1);
    p.add_step(|x| x * 3);
    assert_eq!(p.run(4), 15);
}
```

**Returning `FnMut`:** The binding at the call site must be `mut`.

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Key Points illustration -->
```rust
fn counter(start: i32) -> impl FnMut() -> i32 {
    let mut n = start;
    move || {
        let current = n;
        n += 1;
        current
    }
}

fn demo_counter() {
    let mut next = counter(0);
    assert_eq!(next(), 0);
    assert_eq!(next(), 1);
}
```

## Related Rules
- [anti-type-erasure](anti-type-erasure.md) - avoid `Box<dyn Trait>` when `impl Trait` works
- [closure-static-vs-dyn](closure-static-vs-dyn.md) - static vs dynamic dispatch trade-offs for callbacks
