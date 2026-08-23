# mem-write-over-format

> Use `write!()` into existing buffers instead of `format!()` allocations## Decision

Consider this rule only after its prerequisites are satisfied: Use `write!()` into existing buffers instead of `format!()` allocations.

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
- External crates referenced by the source (`log`, `criterion`) must already be accepted by the project or be approved before addition.
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Keep correctness tests green and record before/after allocations, type size, memory footprint, or representative benchmark evidence.

## Why It Matters

`format!()` always allocates a new `String`. In hot paths or loops, these allocations add up. `write!()` writes directly into an existing buffer, reusing its capacity. For high-frequency formatting operations, this can eliminate significant allocator overhead.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
fn log_event(event: &Event, output: &mut Vec<u8>) {
    // format! allocates a new String every call
    let line = format!(
        "[{}] {}: {}\n",
        event.timestamp,
        event.level,
        event.message
    );
    output.extend_from_slice(line.as_bytes());
}

fn build_response(items: &[Item]) -> String {
    let mut result = String::new();
    
    for item in items {
        // format! allocates for each item
        result.push_str(&format!("{}: {}\n", item.name, item.value));
    }
    
    result
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::fmt::Write;

fn log_event(event: &Event, output: &mut Vec<u8>) {
    use std::io::Write;
    // write! to Vec<u8> directly, no intermediate allocation
    write!(
        output,
        "[{}] {}: {}\n",
        event.timestamp,
        event.level,
        event.message
    ).unwrap();
}

fn build_response(items: &[Item]) -> String {
    use std::fmt::Write;
    
    let mut result = String::with_capacity(items.len() * 64);
    
    for item in items {
        // write! into existing String, reuses capacity
        write!(&mut result, "{}: {}\n", item.name, item.value).unwrap();
    }
    
    result
}
```

## Write Trait Varieties

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Write Trait Varieties illustration -->
```rust
// std::fmt::Write - for String, &mut String
use std::fmt::Write as FmtWrite;
let mut s = String::new();
write!(&mut s, "Hello {}", 42).unwrap();

// std::io::Write - for Vec<u8>, File, TcpStream, etc.
use std::io::Write as IoWrite;
let mut v: Vec<u8> = Vec::new();
write!(&mut v, "Hello {}", 42).unwrap();

// Both can fail in principle, but String/Vec never fail
// Still need .unwrap() due to Result return type
```

## Reusable Formatting Buffer

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Reusable Formatting Buffer illustration -->
```rust
use std::fmt::Write;

struct Formatter {
    buffer: String,
}

impl Formatter {
    fn new() -> Self {
        Self { buffer: String::with_capacity(1024) }
    }
    
    fn format_event(&mut self, event: &Event) -> &str {
        self.buffer.clear();  // Reuse allocation
        write!(
            &mut self.buffer, 
            "[{}] {}",
            event.timestamp, 
            event.message
        ).unwrap();
        &self.buffer
    }
}

// Usage
let mut formatter = Formatter::new();
for event in events {
    let formatted = formatter.format_event(event);
    send_log(formatted);
}
```

## writeln! for Lines

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the writeln! for Lines illustration -->
```rust
use std::fmt::Write;

let mut output = String::new();

// writeln! adds newline automatically
writeln!(&mut output, "Line 1: {}", value1).unwrap();
writeln!(&mut output, "Line 2: {}", value2).unwrap();

// Equivalent to
write!(&mut output, "Line 1: {}\n", value1).unwrap();
```

## When format! Is Fine

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When format! Is Fine illustration -->
```rust
// One-time formatting, not in loop
let message = format!("Starting server on port {}", port);
log::info!("{}", message);

// Return value (can't return reference to local buffer)
fn describe(item: &Item) -> String {
    format!("{}: {}", item.name, item.value)  // Must allocate
}

// Debug/error paths (not hot)
if condition {
    panic!("Unexpected: {}", format!("details: {:?}", debug_info));
}
```

## Benchmark Difference

Writing into a pre-allocated buffer avoids per-call heap allocation and is
consistently faster than `format!()` in tight loops. The exact difference
depends on string length, allocator, and hardware — measure with
[criterion](https://crates.io/crates/criterion) in your own workload.

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Benchmark Difference illustration -->
```rust
use std::fmt::Write; // brings the write! target trait into scope

// format! in loop: new heap allocation on every iteration
for i in 0..1000 {
    let s = format!("item-{}", i);
    process(&s);
}

// write! with reuse: no allocation after the first iteration
let mut buf = String::with_capacity(32);
for i in 0..1000 {
    buf.clear();
    write!(&mut buf, "item-{}", i).unwrap();
    process(&buf);
}
```

## Related Rules
- [mem-avoid-format](./mem-avoid-format.md) - General format! avoidance patterns
- [mem-reuse-collections](./mem-reuse-collections.md) - Reusing buffers in loops
- [mem-with-capacity](./mem-with-capacity.md) - Pre-allocating string capacity
