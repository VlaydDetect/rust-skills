# mem-reuse-collections

> Clear and reuse collections instead of creating new ones in loops## Decision

Consider this rule only after its prerequisites are satisfied: Clear and reuse collections instead of creating new ones in loops.

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
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Keep correctness tests green and record before/after allocations, type size, memory footprint, or representative benchmark evidence.

## Why It Matters

Creating new `Vec`, `String`, or `HashMap` instances in hot loops generates significant allocator pressure. Clearing a collection and reusing it keeps the existing capacity, avoiding repeated allocation/deallocation cycles. This is especially impactful for frequently-executed code paths.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
fn process_batches(batches: &[Batch]) -> Vec<Result> {
    let mut results = Vec::new();
    
    for batch in batches {
        let mut temp = Vec::new();  // Allocates every iteration
        
        for item in &batch.items {
            temp.push(transform(item));
        }
        
        results.push(aggregate(&temp));
        // temp dropped here, deallocation
    }
    
    results
}

fn format_lines(items: &[Item]) -> String {
    let mut output = String::new();
    
    for item in items {
        let line = format!("{}: {}", item.name, item.value);  // Allocates
        output.push_str(&line);
        output.push('\n');
    }
    
    output
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
fn process_batches(batches: &[Batch]) -> Vec<Result> {
    let mut results = Vec::with_capacity(batches.len());
    let mut temp = Vec::new();  // Allocate once outside loop
    
    for batch in batches {
        temp.clear();  // Reuse allocation, just reset length
        
        for item in &batch.items {
            temp.push(transform(item));
        }
        
        results.push(aggregate(&temp));
        // temp keeps its capacity for next iteration
    }
    
    results
}

fn format_lines(items: &[Item]) -> String {
    use std::fmt::Write;
    
    let mut output = String::new();
    let mut line = String::new();  // Reusable buffer
    
    for item in items {
        line.clear();
        write!(&mut line, "{}: {}", item.name, item.value).unwrap();
        output.push_str(&line);
        output.push('\n');
    }
    
    output
}
```

## Clear vs Drain vs New

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Clear vs Drain vs New illustration -->
```rust
let mut vec = vec![1, 2, 3, 4, 5];

// clear(): keeps capacity, O(n) for Drop types
vec.clear();
assert_eq!(vec.len(), 0);
assert!(vec.capacity() >= 5);

// drain(): returns iterator, clears after iteration
let drained: Vec<_> = vec.drain(..).collect();

// truncate(): keeps first n elements
vec.truncate(2);

// Creating new: loses all capacity
vec = Vec::new();  // Capacity gone
```

## HashMap Reuse

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the HashMap Reuse illustration -->
```rust
use std::collections::HashMap;

fn count_words_per_line(lines: &[&str]) -> Vec<HashMap<String, usize>> {
    let mut results = Vec::with_capacity(lines.len());
    let mut counts = HashMap::new();  // Reuse across iterations
    
    for line in lines {
        counts.clear();  // Keeps bucket allocation
        
        for word in line.split_whitespace() {
            *counts.entry(word.to_string()).or_insert(0) += 1;
        }
        
        results.push(counts.clone());
    }
    
    results
}
```

## BufWriter Pattern

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the BufWriter Pattern illustration -->
```rust
use std::io::{BufWriter, Write};

fn write_many_records(records: &[Record], mut output: impl Write) -> std::io::Result<()> {
    // BufWriter reuses its internal buffer
    let mut writer = BufWriter::with_capacity(8192, &mut output);
    let mut line = String::with_capacity(256);  // Reusable formatting buffer
    
    for record in records {
        line.clear();
        format_record(record, &mut line);
        writer.write_all(line.as_bytes())?;
        writer.write_all(b"\n")?;
    }
    
    writer.flush()
}
```

## When to Create Fresh

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When to Create Fresh illustration -->
```rust
// When ownership transfer is needed
fn produce_results() -> Vec<Vec<Item>> {
    let mut results = Vec::new();
    
    for batch in batches {
        let processed: Vec<Item> = batch.process();  // Ownership transferred
        results.push(processed);  // Moved into results
    }
    
    results  // Each inner Vec is independent
}

// When thread safety requires it
std::thread::scope(|s| {
    for _ in 0..4 {
        s.spawn(|| {
            let local_buffer = Vec::new();  // Thread-local, can't share
            // ...
        });
    }
});
```

## Related Rules
- [mem-with-capacity](./mem-with-capacity.md) - Pre-allocating capacity
- [mem-clone-from](./mem-clone-from.md) - Reusing allocations when cloning
- [mem-write-over-format](./mem-write-over-format.md) - Avoiding format! allocations
