# pat-exhaustive-enum

> Match owned enums exhaustively; avoid catch-all `_` that hides new variants

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-idioms; supporters=`rust-stable`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Match owned enums exhaustively; avoid catch-all `_` that hides new variants.

## Apply When

Apply when pattern syntax can make state extraction, exhaustiveness, guards, or early return clearer without changing behavior, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the syntax exceeds the declared MSRV or a catch-all would hide a meaningful future or current variant. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. List the states and binding needs, choose exhaustive matching or a deliberate fallback, and preserve evaluation and drop order.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Concise patterns can improve clarity, while dense nesting or broad catch-alls can obscure control flow and evolution.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.

## Verification

Compile under the declared toolchain and test every meaningful variant, guard boundary, and fallback behavior.

## Why It Matters

A `_ =>` wildcard arm silently absorbs any variant added to an enum you own, converting what should be a compile-time error into a silent runtime no-op. Exhaustive matches let the compiler act as a checklist: add a variant, get a build failure everywhere it is unhandled. Reserve `_` and `..` for **foreign** `#[non_exhaustive]` enums, where the language requires a catch-all, and document why it is necessary.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
#[derive(Debug)]
enum Status {
    Active,
    Pending,
    Closed,
}

fn describe(s: &Status) -> &'static str {
    match s {
        Status::Active => "active",
        _ => "inactive", // hides Status::Pending silently; adding a new variant goes unnoticed
    }
}
```

If `Status::Suspended` is later added, `describe` compiles and silently returns `"inactive"` for it — a logic bug the compiler never catches.

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
#[derive(Debug)]
enum Status {
    Active,
    Pending,
    Closed,
}

fn describe(s: &Status) -> &'static str {
    match s {
        Status::Active => "active",
        Status::Pending => "pending",
        Status::Closed => "closed",
        // Adding Status::Suspended now causes a compile error here — intended.
    }
}
```

## Grouping Variants with `|`

When several variants share the same handling, list them explicitly rather than falling back to `_`:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Grouping Variants with | illustration -->
```rust
fn is_terminal(s: &Status) -> bool {
    match s {
        Status::Closed | Status::Pending => true,
        Status::Active => false,
    }
}
```

## When `_` Is Required: Foreign `#[non_exhaustive]` Enums

External crates may mark enums `#[non_exhaustive]`, which means the compiler *forces* a wildcard. Document the intent:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When  Is Required: Foreign #[nonexhaustive] Enums illustration -->
```rust
// From a hypothetical external crate:
// #[non_exhaustive]
// pub enum TheirEvent { Click, Hover, /* ... future variants */ }

fn handle_event(event: &some_crate::TheirEvent) {
    match event {
        some_crate::TheirEvent::Click => { /* ... */ }
        some_crate::TheirEvent::Hover => { /* ... */ }
        // required by #[non_exhaustive]; intentionally a no-op for unknown variants
        _ => {}
    }
}
```

## Clippy Lint

`clippy::wildcard_enum_match_arm` (part of `clippy::restriction`) warns when a wildcard arm in a match on a non-`#[non_exhaustive]` enum could be replaced with explicit variants. Enabling it catches drift over time.

## Related Rules
- [api-non-exhaustive](api-non-exhaustive.md) - use `#[non_exhaustive]` for future-proof enums in public APIs
- [type-enum-states](type-enum-states.md) - use enums for mutually exclusive states
- [pat-matches-macro](pat-matches-macro.md) - boolean pattern tests with `matches!()`
