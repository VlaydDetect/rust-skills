# mem-avoid-format

> Avoid `format!()` when string literals work

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-performance; supporters=`rust-ownership`, `rust-stdlib`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Avoid `format!()` when string literals work.

## Apply When

Apply when a measured allocation, footprint, locality, move, or layout cost is material on the representative workload, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when there is no profile or size evidence, or the change would complicate ownership, portability, or correctness for a noise-level gain. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Measure allocation or layout first, change one representation or reuse decision, and compare the same workload.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Inline storage, boxing, arenas, compact types, and reuse exchange simplicity, code size, stack use, locality, or dependency cost.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`log`, `bytes`, `compact_str`) must already be accepted by the project or be approved before addition.
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Keep correctness tests green and record before/after allocations, type size, memory footprint, or representative benchmark evidence.

## Why It Matters

`format!()` always allocates a new String, even for constant text. In hot paths, these allocations add up. Use string literals, `write!()`, or pre-allocated buffers instead.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Allocates every time, even for static text
fn get_error_message() -> String {
    format!("An error occurred")  // Unnecessary allocation!
}

// Allocates in a loop
for item in items {
    log::info!("{}", format!("Processing item: {}", item));  // Double work!
}

// format! in hot path
fn classify(n: i32) -> String {
    if n > 0 {
        format!("positive")  // Allocates!
    } else if n < 0 {
        format!("negative")  // Allocates!
    } else {
        format!("zero")      // Allocates!
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Return &'static str for constants
fn get_error_message() -> &'static str {
    "An error occurred"  // No allocation
}

// Use format args directly
for item in items {
    log::info!("Processing item: {}", item);  // No intermediate String
}

// Return Cow for mixed static/dynamic
use std::borrow::Cow;

fn classify(n: i32) -> Cow<'static, str> {
    if n > 0 {
        Cow::Borrowed("positive")  // No allocation
    } else if n < 0 {
        Cow::Borrowed("negative")  // No allocation
    } else {
        Cow::Borrowed("zero")      // No allocation
    }
}

// Or just &'static str if always static
fn classify_str(n: i32) -> &'static str {
    if n > 0 { "positive" }
    else if n < 0 { "negative" }
    else { "zero" }
}
```

## Use write!() for Output

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Use write!() for Output illustration -->
```rust
use std::io::Write;

// Bad: Allocate then write
fn bad_log(writer: &mut impl Write, msg: &str, code: u32) {
    let formatted = format!("[ERROR {}] {}", code, msg);  // Allocation!
    writer.write_all(formatted.as_bytes()).unwrap();
}

// Good: Write directly
fn good_log(writer: &mut impl Write, msg: &str, code: u32) {
    write!(writer, "[ERROR {}] {}", code, msg).unwrap();  // No allocation!
}
```

## Pre-allocate for Multiple Appends

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pre-allocate for Multiple Appends illustration -->
```rust
// Bad: Multiple allocations
fn build_message(parts: &[&str]) -> String {
    let mut result = String::new();
    for part in parts {
        result = format!("{}{}\n", result, part);  // Allocates each iteration!
    }
    result
}

// Good: Pre-allocate
fn build_message(parts: &[&str]) -> String {
    let total_len: usize = parts.iter().map(|p| p.len() + 1).sum();
    let mut result = String::with_capacity(total_len);
    for part in parts {
        result.push_str(part);
        result.push('\n');
    }
    result
}

// Good: Use join
fn build_message(parts: &[&str]) -> String {
    parts.join("\n")
}
```

## CompactString for Small Strings

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the CompactString for Small Strings illustration -->
```rust
use compact_str::CompactString;

// Stack-allocated for strings <= 24 bytes
fn format_code(code: u32) -> CompactString {
    compact_str::format_compact!("ERR-{:04}", code)
    // Stack-allocated if result is small enough
}
```

## When format!() Is Fine

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When format!() Is Fine illustration -->
```rust
// Rare/cold paths - clarity over micro-optimization
fn log_startup_message() {
    println!("{}", format!("Starting {} v{}", APP_NAME, VERSION));
}

// When you need an owned String anyway
fn create_user_greeting(name: &str) -> String {
    format!("Hello, {}!", name)  // Need owned String
}

// Error messages (already on error path)
return Err(format!("Invalid value: {}", value).into());
```

## Related Rules
- [mem-write-over-format](mem-write-over-format.md) - Use write!() instead of format!()
- [mem-with-capacity](mem-with-capacity.md) - Pre-allocate strings
- [own-cow-conditional](own-cow-conditional.md) - Use Cow for mixed static/dynamic
