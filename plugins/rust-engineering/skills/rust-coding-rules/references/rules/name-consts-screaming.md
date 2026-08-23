# name-consts-screaming

> Use `SCREAMING_SNAKE_CASE` for constants and statics## Decision

Use this context-sensitive Rust decision when its premise is established: Use `SCREAMING_SNAKE_CASE` for constants and statics.

## Apply When

Apply when an identifier is part of a Rust caller contract or repository convention and its name communicates cost, ownership, state, or behavior, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when a rename would create compatibility churn without improving meaning or merely enforces taste already handled by tooling. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Classify the item and semantic operation, follow Rust convention and local vocabulary, then check public-path compatibility.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Conventional names improve discoverability but public renames can impose migration and deprecation costs.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Compile callers and docs, run configured naming lints, and perform compatibility analysis for public renames.

## Why It Matters

Constants and statics are special—they're known at compile time and have program-wide lifetime. `SCREAMING_SNAKE_CASE` makes them visually distinct from runtime variables. This convention is enforced by the compiler and universally expected.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// lowercase/camelCase constants - compiler warns
const maxConnections: u32 = 100;  // warning
const default_timeout: u64 = 30;  // warning
static globalCounter: AtomicU64 = AtomicU64::new(0);  // warning
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// SCREAMING_SNAKE_CASE for constants
const MAX_CONNECTIONS: u32 = 100;
const DEFAULT_TIMEOUT: Duration = Duration::from_secs(30);
const BUFFER_SIZE: usize = 4096;

// SCREAMING_SNAKE_CASE for statics
static GLOBAL_COUNTER: AtomicU64 = AtomicU64::new(0);
static CONFIG: OnceLock<Config> = OnceLock::new();

// Type-level constants in impl blocks
impl Buffer {
    const INITIAL_CAPACITY: usize = 1024;
    const MAX_CAPACITY: usize = 1024 * 1024;
}
```

## Associated Constants

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Associated Constants illustration -->
```rust
trait Limit {
    const MAX: usize;
    const MIN: usize;
}

impl Limit for SmallBuffer {
    const MAX: usize = 256;
    const MIN: usize = 16;
}

// Generic associated constants
struct Container<T> {
    data: Vec<T>,
}

impl<T> Container<T> {
    const EMPTY: Self = Self { data: Vec::new() };
}
```

## Environment and Config

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Environment and Config illustration -->
```rust
// Environment variable names
const ENV_DATABASE_URL: &str = "DATABASE_URL";
const ENV_LOG_LEVEL: &str = "LOG_LEVEL";

// Configuration keys
const CONFIG_TIMEOUT_SECONDS: &str = "timeout_seconds";
const CONFIG_MAX_RETRIES: &str = "max_retries";
```

## Lazy Static / OnceLock

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Lazy Static / OnceLock illustration -->
```rust
use std::sync::OnceLock;

// Global configuration
static CONFIG: OnceLock<AppConfig> = OnceLock::new();

// Compiled regex
static EMAIL_REGEX: OnceLock<Regex> = OnceLock::new();

fn get_email_regex() -> &'static Regex {
    EMAIL_REGEX.get_or_init(|| {
        Regex::new(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$").unwrap()
    })
}
```

## Related Rules
- [name-funcs-snake](./name-funcs-snake.md) - Function/variable naming
- [name-types-camel](./name-types-camel.md) - Type naming
- [type-newtype-ids](./type-newtype-ids.md) - Type-safe constants
