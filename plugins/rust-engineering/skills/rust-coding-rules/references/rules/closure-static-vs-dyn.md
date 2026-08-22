# closure-static-vs-dyn

> Accept `impl Fn` (generic) for hot callbacks; use `&dyn Fn`/`Box<dyn Fn>` to cut code size or to store them

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-traits; supporters=`rust-ownership`, `rust-api-design`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Accept `impl Fn` (generic) for hot callbacks; use `&dyn Fn`/`Box<dyn Fn>` to cut code size or to store them.

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

A generic parameter `F: Fn(…) -> …` (or `impl Fn`) monomorphizes at each call site: the compiler emits a specialized copy of the function, enabling inlining and zero-cost dispatch. The trade-off is binary bloat when many different closure types are substituted. `&dyn Fn`/`Box<dyn Fn>` share a single compiled copy via a vtable, which reduces code size and is the only option for storing heterogeneous closures (e.g. an event handler registry). Choose by profiling requirements, not habit.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Storing closures generically in a struct is impossible — the struct
// would need a type parameter per handler, making it unusable.
struct BadRegistry<F: Fn(&str)> {
    // Can only hold ONE concrete closure type — defeats the purpose.
    handler: F,
}

// Equally, using Box<dyn Fn> on a hot, single-call-site inner loop
// pays a vtable cost for no benefit.
fn transform_slow(xs: &[i32], f: &dyn Fn(i32) -> i32) -> Vec<i32> {
    xs.iter().map(|&x| f(x)).collect()
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Generic / static dispatch: preferred for hot paths — inlinable, zero allocation.
fn transform<F: Fn(i32) -> i32>(xs: &[i32], f: F) -> Vec<i32> {
    xs.iter().map(|&x| f(x)).collect()
}

// Dynamic dispatch: required when storing heterogeneous closures.
struct Registry {
    handlers: Vec<Box<dyn Fn(&str)>>,
}

impl Registry {
    fn new() -> Self {
        Self { handlers: Vec::new() }
    }

    fn register(&mut self, handler: impl Fn(&str) + 'static) {
        self.handlers.push(Box::new(handler));
    }

    fn dispatch(&self, event: &str) {
        for handler in &self.handlers {
            handler(event);
        }
    }
}

fn demo() {
    // Static dispatch — the compiler may inline the closure entirely.
    let doubled = transform(&[1, 2, 3], |x| x * 2);
    assert_eq!(doubled, vec![2, 4, 6]);

    // Dynamic dispatch — one compiled copy, heterogeneous handlers.
    let mut reg = Registry::new();
    reg.register(|e| println!("logger: {e}"));
    reg.register(|e| println!("metrics: {e}"));
    reg.dispatch("user_signup");
}
```

## Decision Table

| Situation | Use |
|-----------|-----|
| Hot inner loop, single call site | `impl Fn` / generic `F: Fn` |
| Callback stored in a struct field | `Box<dyn Fn>` |
| Collection of mixed closures | `Vec<Box<dyn Fn(…)>>` |
| Pass-through, one level deep, not stored | `&dyn Fn` (avoids allocation) |
| Called across an `await` point | `Box<dyn Fn + Send>` |

**Note:** `&dyn Fn` is useful to avoid an allocation when you only need to borrow the closure for one call and do not store it. Pass `&closure` (reference to a stack-allocated closure) rather than boxing.

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Decision Table illustration -->
```rust
fn call_once_dyn(f: &dyn Fn() -> i32) -> i32 {
    f()
}

fn demo_ref() {
    let x = 7;
    let result = call_once_dyn(&|| x + 1);
    assert_eq!(result, 8);
}
```

## Related Rules
- [anti-type-erasure](anti-type-erasure.md) - prefer `impl Trait` over `Box<dyn Trait>` when possible
- [type-generic-bounds](type-generic-bounds.md) - add trait bounds only where needed
- [closure-fn-trait-bounds](closure-fn-trait-bounds.md) - choose the weakest `Fn` trait
