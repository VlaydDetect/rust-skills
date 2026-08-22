# api-must-use

> Mark types and functions with `#[must_use]` when ignoring results is likely a bug

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-api-design; supporters=`rust-traits`, `rust-ownership`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Mark types and functions with `#[must_use]` when ignoring results is likely a bug.

## Apply When

Apply when a public or independently evolving caller contract needs an ownership, construction, extension, or compatibility decision, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the abstraction has only one local use or would expose implementation and dependency details without caller value. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Write representative caller examples, minimize public surface, and review ownership, errors, extension rights, and compatibility.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

More flexibility can improve call sites while increasing inference, monomorphization, compatibility, and maintenance obligations.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`futures`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Compile downstream-style examples and check docs, public paths, feature behavior, and the declared compatibility baseline.

## Why It Matters

Some return values should never be ignored—`Result`, locks, RAII guards, computed values that have no side effects. Without `#[must_use]`, silently discarding these values can introduce subtle bugs that are hard to detect. The attribute generates compiler warnings when the value is unused.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Result ignored - error silently dropped
fn send_email(to: &str, body: &str) -> Result<(), EmailError> { ... }

send_email("user@example.com", "Hello!");  // No warning if Result ignored!
// Email may have failed, but we don't know

// Computed value ignored - likely a bug
fn compute_checksum(data: &[u8]) -> u32 { ... }

let data = vec![1, 2, 3, 4];
compute_checksum(&data);  // Result discarded - pointless call
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
#[must_use = "this `Result` may be an `Err` that should be handled"]
fn send_email(to: &str, body: &str) -> Result<(), EmailError> { ... }

send_email("user@example.com", "Hello!");  
// Warning: unused `Result` that must be used

// Mark pure functions
#[must_use = "this returns a new value and does not modify the input"]
fn compute_checksum(data: &[u8]) -> u32 { ... }

compute_checksum(&data);
// Warning: unused return value of `compute_checksum` that must be used
```

## Apply to Types

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Apply to Types illustration -->
```rust
// Mark the type itself when it should always be used
#[must_use = "futures do nothing unless polled"]
struct MyFuture<T> { ... }

// Mark RAII guards
#[must_use = "if unused, the lock will be immediately released"]
struct MutexGuard<'a, T> { ... }

// Mark results/errors
#[must_use = "errors should be handled"]
enum AppError { ... }
```

## Standard Library Examples

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Standard Library Examples illustration -->
```rust
// Result and Option are #[must_use]
let v: Vec<i32> = vec![1, 2, 3];
v.first();  // Warning: unused Option

// Iterator adapters are #[must_use]
v.iter().map(|x| x * 2);  // Warning: iterators are lazy

// String methods that return new values
let s = "hello";
s.to_uppercase();  // Warning: unused String
```

## When to Apply

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When to Apply illustration -->
```rust
// ✅ Pure functions (no side effects)
#[must_use]
fn add(a: i32, b: i32) -> i32 { a + b }

// ✅ Builder methods returning Self
#[must_use = "builder methods return a new builder"]
fn with_timeout(self, t: Duration) -> Self { ... }

// ✅ Fallible operations
#[must_use]
fn try_parse(s: &str) -> Result<Data, ParseError> { ... }

// ✅ Iterators and futures (lazy)
#[must_use = "iterators are lazy and do nothing unless consumed"]
struct Map<I, F> { ... }

// ❌ Side-effecting functions where result is optional
fn log(msg: &str) -> Result<(), io::Error> { ... }  // Might be ok to ignore

// ❌ Methods with useful side effects
fn vec.push(item);  // Mutates vec, no return to use
```

## Custom Messages

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Custom Messages illustration -->
```rust
#[must_use = "creating a guard does nothing without assignment"]
struct ScopeGuard { ... }

#[must_use = "this returns the old value"]
fn replace(&mut self, new: T) -> T { ... }

#[must_use = "use `.await` to execute the future"]
async fn fetch() -> Data { ... }
```

## Clippy Lints

```toml
[lints.clippy]
must_use_candidate = "warn"      # Suggests where to add #[must_use]
unused_must_use = "deny"          # Built-in, treat warnings as errors
double_must_use = "warn"          # Redundant #[must_use]
```

## Related Rules
- [api-builder-must-use](./api-builder-must-use.md) - Builder pattern must_use
- [err-result-over-panic](./err-result-over-panic.md) - Result types require handling
- [lint-deny-correctness](./lint-deny-correctness.md) - Enabling useful lints
