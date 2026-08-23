# name-types-camel

> Use `UpperCamelCase` for types, traits, and enum names## Decision

Use this context-sensitive Rust decision when its premise is established: Use `UpperCamelCase` for types, traits, and enum names.

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

Rust's naming conventions are enforced by the compiler and linter. Consistent naming makes code immediately recognizable—you know `HttpClient` is a type, `send_request` is a function. Violating conventions triggers warnings and makes code harder to read.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Lowercase types - compiler warns
struct http_client { ... }  // warning: type `http_client` should have an upper camel case name
trait serializable { ... }  // warning
enum response_type { ... }  // warning

// Screaming case for types
struct HTTP_CLIENT { ... }  // Not idiomatic
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// UpperCamelCase for all types
struct HttpClient { ... }
trait Serializable { ... }
enum ResponseType { ... }

// Compound words
struct TcpConnection { ... }
struct IoError { ... }
struct FileReader { ... }

// Generic types
struct HashMap<K, V> { ... }
struct Result<T, E> { ... }
```

## Acronyms

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Acronyms illustration -->
```rust
// Treat acronyms as words (capitalize first letter only)
struct HttpServer { ... }      // Not HTTPServer
struct JsonParser { ... }      // Not JSONParser
struct Uuid { ... }            // Not UUID
struct TcpStream { ... }       // Not TCPStream

// Exception: Two-letter acronyms can be all caps
struct IOError { ... }         // Acceptable
struct IoError { ... }         // Also acceptable (preferred)
```

## Type Aliases

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Type Aliases illustration -->
```rust
// Type aliases also use UpperCamelCase
type Result<T> = std::result::Result<T, Error>;
type BoxedFuture<'a, T> = Pin<Box<dyn Future<Output = T> + Send + 'a>>;
```

## Related Rules
- [name-variants-camel](./name-variants-camel.md) - Enum variant naming
- [name-funcs-snake](./name-funcs-snake.md) - Function naming
- [name-acronym-word](./name-acronym-word.md) - Acronym handling
