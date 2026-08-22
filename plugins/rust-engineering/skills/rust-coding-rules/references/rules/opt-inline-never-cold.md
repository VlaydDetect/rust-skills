# opt-inline-never-cold

> Use `#[inline(never)]` and `#[cold]` for error paths and rarely-executed code

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-performance; supporters=`rust-cargo-build`, `rust-stable`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `#[inline(never)]` and `#[cold]` for error paths and rarely-executed code.

## Apply When

Apply when a reproducible profile or benchmark identifies a compiler, codegen, branch, cache, or target-specific bottleneck, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the workload, deployment target, or portability contract is unknown, or the expected benefit is speculative. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Hold toolchain, target, profile, features, inputs, and hardware constant; test one optimization hypothesis at a time.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

LTO, codegen, inlining, PGO, SIMD, and target tuning can trade build time, size, portability, debuggability, and determinism.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`log`) must already be accepted by the project or be approved before addition.
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Compare repeated release-like measurements and artifact or codegen evidence while preserving functional behavior and fallback targets.

## Why It Matters

Inlining error handling code into hot paths wastes instruction cache space and can prevent other optimizations. `#[inline(never)]` keeps cold code out of the hot path. `#[cold]` tells the compiler this branch is unlikely, enabling better branch prediction hints and code layout.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
fn process_data(data: &[u8]) -> Result<Output, Error> {
    if data.is_empty() {
        // Error path inlined into hot function
        return Err(Error::Empty {
            context: format!("Expected data, got empty slice"),
            suggestions: vec!["Check input", "Validate before calling"],
        });
    }
    
    // Hot path - now polluted with error construction code
    do_processing(data)
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
fn process_data(data: &[u8]) -> Result<Output, Error> {
    if data.is_empty() {
        return Err(empty_data_error());  // Cold path stays small
    }
    
    do_processing(data)
}

#[cold]
#[inline(never)]
fn empty_data_error() -> Error {
    Error::Empty {
        context: format!("Expected data, got empty slice"),
        suggestions: vec!["Check input", "Validate before calling"],
    }
}
```

## #[cold] for Unlikely Branches

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the #[cold] for Unlikely Branches illustration -->
```rust
fn parse_value(input: &str) -> Result<i32, ParseError> {
    match input.parse() {
        Ok(n) => Ok(n),
        Err(e) => cold_parse_error(input, e),
    }
}

#[cold]
fn cold_parse_error(input: &str, e: std::num::ParseIntError) -> Result<i32, ParseError> {
    Err(ParseError {
        input: input.to_string(),
        source: e,
    })
}
```

## Panic Paths

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Panic Paths illustration -->
```rust
fn get_index(&self, idx: usize) -> &T {
    if idx >= self.len {
        cold_out_of_bounds(idx, self.len);
    }
    unsafe { self.ptr.add(idx).as_ref().unwrap() }
}

#[cold]
#[inline(never)]
fn cold_out_of_bounds(idx: usize, len: usize) -> ! {
    panic!("index {} out of bounds for length {}", idx, len);
}
```

## Error Construction Functions

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Error Construction Functions illustration -->
```rust
// Keep error construction out of hot path
impl MyError {
    #[cold]
    pub fn io_error(source: std::io::Error, path: &Path) -> Self {
        MyError::Io {
            source,
            path: path.to_path_buf(),
            context: get_context(),
        }
    }
    
    #[cold]
    pub fn validation_error(msg: &str, field: &str) -> Self {
        MyError::Validation {
            message: msg.to_string(),
            field: field.to_string(),
        }
    }
}

fn read_config(path: &Path) -> Result<Config, MyError> {
    std::fs::read_to_string(path)
        .map_err(|e| MyError::io_error(e, path))?
        .parse()
        .map_err(|e| MyError::parse_error(e))
}
```

## likely/unlikely Hints

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the likely/unlikely Hints illustration -->
```rust
// Nightly: std::hint likely/unlikely branch hints (still unstable as of Rust 1.96)
// (std::hint::cold_path() is stable since 1.95 for marking the rare branch)
#![feature(likely_unlikely)]
use std::hint::{likely, unlikely};

fn process(data: Option<&Data>) -> Result<Output, Error> {
    if unlikely(data.is_none()) {
        return cold_none_error();
    }
    
    let data = data.unwrap();
    
    if likely(data.is_valid()) {
        fast_process(data)
    } else {
        slow_validate_and_process(data)
    }
}

// Stable alternative: structure code so hot path is "fall through"
fn process(data: Option<&Data>) -> Result<Output, Error> {
    let data = match data {
        Some(d) => d,
        None => return cold_none_error(),  // Early return = unlikely hint
    };
    
    // Compiler assumes code after early returns is "hot"
    fast_process(data)
}
```

## Pattern: Extract Cold Code

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Extract Cold Code illustration -->
```rust
// Before: cold code inline
fn hot_function(x: i32) -> i32 {
    if x < 0 {
        log::error!("Negative value: {}", x);
        eprintln!("Debug info: {:?}", std::backtrace::Backtrace::capture());
        return 0;
    }
    x * 2
}

// After: cold code extracted
fn hot_function(x: i32) -> i32 {
    if x < 0 {
        return handle_negative(x);
    }
    x * 2
}

#[cold]
#[inline(never)]
fn handle_negative(x: i32) -> i32 {
    log::error!("Negative value: {}", x);
    eprintln!("Debug info: {:?}", std::backtrace::Backtrace::capture());
    0
}
```

## Related Rules
- [opt-inline-small](./opt-inline-small.md) - Inlining for hot code
- [opt-inline-always-rare](./opt-inline-always-rare.md) - Forced inlining
- [err-result-over-panic](./err-result-over-panic.md) - Error handling patterns
