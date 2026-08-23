# closure-disjoint-capture

> Capture only what you use; lean on edition-2021 disjoint closure captures## Decision

Use this context-sensitive Rust decision when its premise is established: Capture only what you use; lean on edition-2021 disjoint closure captures.

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

Before the 2021 edition, a closure captured entire variables — using `config.threshold` pulled in the whole `config` struct, preventing other code from using any other field of `config` concurrently. Since Rust 2021, closures capture individual fields (`config.threshold` only), so sibling fields remain independently accessible. Take advantage of this: write closures that reference only the specific fields or values they need, and add `move` only when ownership is genuinely required. When you do need to `move` a single field, bind it to a local first so the rest of the struct stays usable.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
struct Config {
    threshold: i32,
    label: String,
}

fn demo_bad() {
    let config = Config { threshold: 10, label: String::from("demo") };

    // In pre-2021 editions the whole `config` is captured, blocking access
    // to `config.label` below. In 2021 this compiles, but the pattern of
    // capturing the whole struct via `move` is the real footgun:
    let threshold = config.threshold; // copy out the field first
    let check = move || threshold > 0; // now `config` is NOT fully moved

    // If instead you wrote: let check = move || config.threshold > 0;
    // `config` would be moved in, making `config.label` inaccessible afterwards.
    // Demonstrate the problematic pattern (commented out to allow compilation):
    // let check2 = move || config.threshold > 0;
    // println!("{}", config.label); // error: use of moved value

    println!("label still accessible: {}", config.label);
    assert!(check());
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
struct Config {
    threshold: i32,
    label: String,
}

fn demo_good() {
    let config = Config { threshold: 10, label: String::from("active") };

    // Edition 2021: the closure captures only `config.threshold` (a Copy field).
    // `config.label` is NOT captured, so it remains accessible.
    let check = || config.threshold > 0;

    // Both are usable simultaneously.
    println!("label: {}", config.label);  // fine — not captured by `check`
    assert!(check());
}

// When you need `move` for one field, bind it first.
fn make_checker(config: Config) -> (impl Fn() -> bool, String) {
    // Bind the field to a local, then move only that local into the closure.
    let threshold = config.threshold;
    let checker = move || threshold > 0; // moves `threshold` (i32, Copy), not `config`

    // `config.label` is still available here.
    (checker, config.label)
}

fn demo_bind_first() {
    let cfg = Config { threshold: 5, label: String::from("info") };
    let (check, label) = make_checker(cfg);
    println!("label returned: {label}");
    assert!(check());
}
```

## Key Points

- **Edition 2021 rule:** closures capture the *minimal* path used — `foo.bar` rather than `foo`. This reduces spurious borrow conflicts.
- **`move` captures the whole named place.** Writing `move || self.field` inside a method moves `*self`, not just `self.field`. Bind to a local to narrow the capture.
- **Copy types** (integers, booleans) are copied into the closure rather than moved, so the original remains valid even with `move`.
- **Borrow by reference first:** only escalate to `move` when the closure must outlive the scope (see [closure-move-capture](closure-move-capture.md)).

## Related Rules
- [own-borrow-over-clone](own-borrow-over-clone.md) - prefer borrowing over cloning
- [closure-move-capture](closure-move-capture.md) - when to use `move` and how to clone selectively
