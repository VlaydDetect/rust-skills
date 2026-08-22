# closure-fn-trait-bounds

> Require the least restrictive `Fn` trait a callback needs (`FnOnce` ⊇ `FnMut` ⊇ `Fn`)

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-traits; supporters=`rust-ownership`, `rust-api-design`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Require the least restrictive `Fn` trait a callback needs (`FnOnce` ⊇ `FnMut` ⊇ `Fn`).

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

`FnOnce` is implemented by every closure — it may consume its captures and can only be called once. `FnMut` is implemented by closures that mutate captures, and implies `FnOnce`. `Fn` is the strictest: it only reads captures and can be called any number of times concurrently. Bounding a parameter with the weakest trait the body actually requires accepts the widest set of callers. Requiring `Fn` when you only call the closure once needlessly rejects move-consuming closures.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// F: Fn is too strict — the closure is only called once,
// so move-consuming closures are unnecessarily rejected.
fn run_once_bad<F: Fn() -> String>(f: F) -> String {
    f()
}

fn demo_bad() {
    let s = String::from("hello");
    // This closure consumes `s`, so it only implements FnOnce, not Fn.
    // run_once_bad(move || s) // compile error: `s` moved in closure
    let _ = run_once_bad(|| String::from("ok")); // forced to use non-consuming closure
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Use FnOnce when you call the closure exactly once.
fn run_once<F: FnOnce() -> String>(f: F) -> String {
    f()
}

// Use FnMut when you call the closure multiple times and it may mutate state.
fn retry<F: FnMut() -> bool>(mut f: F, attempts: usize) -> bool {
    for _ in 0..attempts {
        if f() {
            return true;
        }
    }
    false
}

// Use Fn when you call the closure multiple times and need it shareable/re-entrant.
fn for_each<T, F: Fn(&T)>(items: &[T], f: F) {
    for item in items {
        f(item);
    }
}

fn demo() {
    // FnOnce: move-consuming closure is accepted
    let s = String::from("hello");
    let result = run_once(move || s.to_uppercase());
    assert_eq!(result, "HELLO");

    // FnMut: closure mutates a counter
    let mut count = 0usize;
    let found = retry(
        || {
            count += 1;
            count == 3
        },
        5,
    );
    assert!(found);

    // Fn: read-only closure, called once per element
    let nums = vec![1, 2, 3];
    for_each(&nums, |n| println!("{n}"));
}
```

## Key Points

| Trait | Captures | Calls | Accepts |
|-------|----------|-------|---------|
| `FnOnce` | may consume | exactly once | all closures |
| `FnMut` | may mutate | multiple | non-consuming |
| `Fn` | read-only | multiple / shared | pure closures |

- `FnMut` requires `mut f` at the call site (the parameter or binding must be `mut`).
- `Fn: FnMut: FnOnce` — a `Fn` closure satisfies an `FnOnce` bound, not the other way around.
- Standard library examples: `Iterator::map` uses `FnMut`; `thread::spawn` uses `FnOnce + Send + 'static`.

## Related Rules
- [closure-static-vs-dyn](closure-static-vs-dyn.md) - generic vs dynamic dispatch for callbacks
- [closure-move-capture](closure-move-capture.md) - when and how to use `move` closures
