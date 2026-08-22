# own-cow-conditional

> Use `Cow<'a, T>` for conditional ownership

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-ownership; supporters=`rust-stdlib`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `Cow<'a, T>` for conditional ownership.

## Apply When

Apply when ownership, borrowing, lifetime, pointer, mutation, or drop semantics control correctness, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when independent ownership is required, or the proposed borrowing shape would leak a guard or lifetime into unrelated callers. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Draw the owner/borrower/drop graph and choose the least complex ownership topology that enforces it.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Less cloning can increase lifetime coupling; shared ownership and interior mutability add runtime and liveness costs.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- Apply only after the rule-specific condition in the source guidance is observed in the current repository.

## Verification

Compile the affected paths and test moves, early returns, mutation, and drop or cancellation behavior that the rule changes.

## Why It Matters

`Cow` (Clone-on-Write) lets you avoid allocations when you *might* need to own data but usually don't. It holds either a borrowed reference or an owned value, cloning only when mutation is needed.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Always allocates, even when input doesn't need modification
fn normalize_path(path: &str) -> String {
    if path.contains("//") {
        path.replace("//", "/")  // Allocation needed
    } else {
        path.to_string()  // Unnecessary allocation!
    }
}

// Always clones the error message
fn format_error(code: u32) -> String {
    match code {
        404 => "Not Found".to_string(),      // Unnecessary!
        500 => "Internal Error".to_string(), // Unnecessary!
        _ => format!("Error {}", code),      // This one needs allocation
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::borrow::Cow;

// Only allocates when needed
fn normalize_path(path: &str) -> Cow<'_, str> {
    if path.contains("//") {
        Cow::Owned(path.replace("//", "/"))  // Allocate
    } else {
        Cow::Borrowed(path)  // Zero-cost borrow
    }
}

// Static strings stay borrowed
fn format_error(code: u32) -> Cow<'static, str> {
    match code {
        404 => Cow::Borrowed("Not Found"),      // No allocation
        500 => Cow::Borrowed("Internal Error"), // No allocation
        _ => Cow::Owned(format!("Error {}", code)), // Allocate only for unknown
    }
}
```

## Real-World Example from ripgrep

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Real-World Example from ripgrep illustration -->
```rust
// https://github.com/BurntSushi/ripgrep/blob/master/crates/globset/src/pathutil.rs
pub(crate) fn file_name<'a>(path: &Cow<'a, [u8]>) -> Option<Cow<'a, [u8]>> {
    let last_slash = path.rfind_byte(b'/').map(|i| i + 1).unwrap_or(0);
    match *path {
        Cow::Borrowed(path) => Some(Cow::Borrowed(&path[last_slash..])),
        Cow::Owned(ref path) => {
            let mut path = path.clone();
            path.drain_bytes(..last_slash);
            Some(Cow::Owned(path))
        }
    }
}
```

## Clone-on-Write Pattern

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Clone-on-Write Pattern illustration -->
```rust
use std::borrow::Cow;

fn process_text(text: Cow<'_, str>) -> Cow<'_, str> {
    if text.contains("bad_word") {
        // to_mut() clones if borrowed, returns &mut if owned
        let mut owned = text.into_owned();
        owned = owned.replace("bad_word", "***");
        Cow::Owned(owned)
    } else {
        text  // Pass through unchanged
    }
}

// Usage
let borrowed: Cow<str> = Cow::Borrowed("hello world");
let result = process_text(borrowed);  // No allocation!

let with_bad: Cow<str> = Cow::Borrowed("hello bad_word");
let result = process_text(with_bad);  // Allocates only here
```

## Cow with Collections

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Cow with Collections illustration -->
```rust
use std::borrow::Cow;

// Mixed borrowed/owned in a collection
fn collect_errors<'a>(
    static_errors: &[&'static str],
    dynamic_errors: Vec<String>,
) -> Vec<Cow<'a, str>> {
    let mut errors: Vec<Cow<str>> = Vec::new();
    
    // Static strings - no allocation
    for &e in static_errors {
        errors.push(Cow::Borrowed(e));
    }
    
    // Dynamic strings - take ownership
    for e in dynamic_errors {
        errors.push(Cow::Owned(e));
    }
    
    errors
}
```

## When to Use Cow

| Situation | Use Cow? |
|-----------|----------|
| Usually borrow, sometimes own | Yes |
| Always need owned data | No, just use owned type |
| Always borrow | No, just use reference |
| Hot path, avoiding all allocations | Yes |
| Returning static strings or formatted | Yes |

## Related Rules
- [own-borrow-over-clone](own-borrow-over-clone.md) - Prefer borrowing over cloning
- [mem-avoid-format](mem-avoid-format.md) - Avoid format! when possible
