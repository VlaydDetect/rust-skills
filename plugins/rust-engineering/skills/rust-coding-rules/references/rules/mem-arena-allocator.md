# mem-arena-allocator

> Use arena allocators for batch allocations

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-performance; supporters=`rust-ownership`, `rust-stdlib`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use arena allocators for batch allocations.

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
- External crates referenced by the source (`bumpalo`, `criterion`) must already be accepted by the project or be approved before addition.
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Keep correctness tests green and record before/after allocations, type size, memory footprint, or representative benchmark evidence.

## Why It Matters

Arena allocators (bump allocators) allocate memory from a contiguous region, making allocation extremely fast (just bump a pointer). All allocations are freed at once when the arena is dropped. Perfect for request-scoped or parse-tree allocations.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Many small allocations during parsing
fn parse(input: &str) -> Vec<Node> {
    let mut nodes = Vec::new();
    for token in tokenize(input) {
        nodes.push(Box::new(Node::new(token)));  // Heap alloc per node!
    }
    nodes
}

// Per-request allocations add up
fn handle_request(req: Request) -> Response {
    let headers = parse_headers(&req);      // Allocates
    let body = parse_body(&req);            // Allocates
    let response = generate_response();     // Allocates
    // All freed individually at end
    response
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use bumpalo::Bump;

// All nodes allocated from same arena
fn parse<'a>(input: &str, arena: &'a Bump) -> Vec<&'a Node> {
    let mut nodes = Vec::new();
    for token in tokenize(input) {
        let node = arena.alloc(Node::new(token));  // Fast bump!
        nodes.push(node);
    }
    nodes
}  // Arena freed all at once

// Per-request arena
fn handle_request(req: Request) -> Response {
    let arena = Bump::new();
    
    let headers = parse_headers(&req, &arena);
    let body = parse_body(&req, &arena);
    let response = generate_response(&arena);
    
    // Convert to owned response before arena drops
    response.to_owned()
}  // All request memory freed instantly
```

## Thread-Local Scratch Arena Pattern

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Thread-Local Scratch Arena Pattern illustration -->
```rust
use bumpalo::Bump;
use std::cell::RefCell;

thread_local! {
    static SCRATCH: RefCell<Bump> = RefCell::new(Bump::with_capacity(4 * 1024));
}

fn with_scratch<T>(f: impl FnOnce(&Bump) -> T) -> T {
    SCRATCH.with(|scratch| {
        let arena = scratch.borrow();
        let result = f(&arena);
        result
    })
}

fn reset_scratch() {
    SCRATCH.with(|scratch| {
        scratch.borrow_mut().reset();
    });
}

// Usage
fn process_batch(items: &[Item]) -> Vec<Output> {
    with_scratch(|arena| {
        let temp_data: Vec<&TempData> = items
            .iter()
            .map(|item| arena.alloc(compute_temp(item)))
            .collect();
        
        // Use temp_data...
        let result = finalize(&temp_data);
        
        reset_scratch();  // Reuse arena memory
        result
    })
}
```

## Evidence from ROC Compiler

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Evidence from ROC Compiler illustration -->
```rust
// https://github.com/roc-lang/roc/blob/main/crates/compiler/solve/src/to_var.rs
std::thread_local! {
    static SCRATCHPAD: RefCell<Option<bumpalo::Bump>> = 
        RefCell::new(Some(bumpalo::Bump::with_capacity(4 * 1024)));
}

fn take_scratchpad() -> bumpalo::Bump {
    SCRATCHPAD.with(|f| f.take().unwrap())
}

fn put_scratchpad(scratchpad: bumpalo::Bump) {
    SCRATCHPAD.with(|f| {
        f.replace(Some(scratchpad));
    });
}
```

## Bumpalo Collections

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bumpalo Collections illustration -->
```rust
use bumpalo::Bump;
use bumpalo::collections::{Vec, String};

fn process<'a>(arena: &'a Bump, input: &str) -> Vec<'a, String<'a>> {
    let mut results = Vec::new_in(arena);
    
    for word in input.split_whitespace() {
        let mut s = String::new_in(arena);
        s.push_str(word);
        s.push_str("_processed");
        results.push(s);
    }
    
    results  // All allocated in arena
}
```

## When to Use Arenas

| Situation | Use Arena? |
|-----------|-----------|
| Parsing (AST nodes) | Yes |
| Request handling | Yes |
| Batch processing | Yes |
| Long-lived data | No |
| Data escaping scope | No (or copy out) |
| Simple programs | Overkill |

## Performance Impact

Arena/bump allocation removes per-allocation metadata overhead and can be
substantially faster than the global allocator — often an order of magnitude in
microbenchmarks — but the actual speedup depends on the allocator, workload,
and allocation size. Arena reset is O(1) regardless of how many allocations
were made. Measure with [criterion](https://crates.io/crates/criterion) to
confirm the benefit in your specific use case.

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Performance Impact illustration -->
```rust
// Memory trade-off:
// - Arena wastes some memory (unused capacity at the end)
// - But eliminates per-allocation metadata overhead
// - Frees everything in O(1) with a single bump reset
```

## Related Rules
- [mem-with-capacity](mem-with-capacity.md) - Pre-allocate when size is known
- [mem-reuse-collections](mem-reuse-collections.md) - Reuse collections with clear()
- [opt-profile-first](perf-profile-first.md) - Profile to verify benefit
