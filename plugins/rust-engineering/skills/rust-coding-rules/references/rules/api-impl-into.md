# api-impl-into

> Accept `impl Into<T>` for flexible APIs, implement `From<T>` for conversions

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-api-design; supporters=`rust-traits`, `rust-ownership`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Accept `impl Into<T>` for flexible APIs, implement `From<T>` for conversions.

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
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Compile downstream-style examples and check docs, public paths, feature behavior, and the declared compatibility baseline.

## Why It Matters

APIs that accept `impl Into<T>` are ergonomic—callers can pass the target type directly or any type that converts to it. This reduces boilerplate `.into()` calls at call sites. Implement `From<T>` rather than `Into<T>` because `From` implies `Into` through a blanket implementation.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Requires exact type - forces callers to convert
fn process_path(path: PathBuf) { ... }
fn set_name(name: String) { ... }

// Caller must convert explicitly
process_path(PathBuf::from("/path/to/file"));
process_path("/path/to/file".to_path_buf());  // Verbose
process_path("/path/to/file".into());          // Explicit

set_name(String::from("Alice"));
set_name("Alice".to_string());  // Verbose
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Accept anything that converts to the target type
fn process_path(path: impl Into<PathBuf>) {
    let path = path.into();  // Convert once inside
    // ...
}

fn set_name(name: impl Into<String>) {
    let name = name.into();
    // ...
}

// Callers are ergonomic
process_path("/path/to/file");    // &str converts automatically
process_path(PathBuf::from(".")); // PathBuf works too

set_name("Alice");                // &str
set_name(String::from("Alice"));  // String
set_name(format!("User-{}", id)); // String from format!
```

## Implement From, Not Into

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Implement From, Not Into illustration -->
```rust
struct UserId(u64);

// ✅ Implement From
impl From<u64> for UserId {
    fn from(id: u64) -> Self {
        UserId(id)
    }
}

// Into is automatically provided by blanket impl
let id: UserId = 42u64.into();  // Works!

// ❌ Don't implement Into directly
impl Into<UserId> for u64 {
    fn into(self) -> UserId {
        UserId(self)  // This works but is non-idiomatic
    }
}
```

## Common Conversions

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Common Conversions illustration -->
```rust
// String-like types
fn log_message(msg: impl Into<String>) { ... }
log_message("literal");           // &str
log_message(String::from("own")); // String
log_message(Cow::from("cow"));    // Cow<str>

// Path-like types  
fn read_file(path: impl AsRef<Path>) { ... }  // AsRef for borrowed access
fn write_file(path: impl Into<PathBuf>) { ... }  // Into when storing

// Duration
fn set_timeout(duration: impl Into<Duration>) { ... }
set_timeout(Duration::from_secs(5));
// Note: no blanket impl for integers, would need custom wrapper
```

## AsRef vs Into

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the AsRef vs Into illustration -->
```rust
// AsRef<T>: borrow as &T, no conversion cost
fn count_bytes(data: impl AsRef<[u8]>) -> usize {
    data.as_ref().len()  // Just borrows, no allocation
}
count_bytes("hello");  // &str -> &[u8]
count_bytes(b"hello"); // &[u8] -> &[u8]
count_bytes(vec![1, 2, 3]);  // &Vec<u8> -> &[u8]

// Into<T>: convert to owned T, may allocate
fn store_data(data: impl Into<Vec<u8>>) {
    let owned: Vec<u8> = data.into();  // Takes ownership
    // ...
}
```

## When NOT to Use impl Into

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When NOT to Use impl Into illustration -->
```rust
// ❌ Trait objects need Sized
fn process(handler: impl Into<Box<dyn Handler>>) { }
// Better: just take Box<dyn Handler> directly

// ❌ Recursive types
struct Node {
    children: Vec<impl Into<Node>>,  // Error: impl Trait not allowed here
}

// ❌ Performance-critical hot paths (minor overhead of trait dispatch)
fn hot_path(value: impl Into<u64>) {
    // Consider taking u64 directly if called billions of times
}

// ❌ When you need to name the type
fn returns_impl() -> impl Into<String> { }  // Opaque, hard to use
```

## Builder Pattern with Into

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Builder Pattern with Into illustration -->
```rust
struct Config {
    name: String,
    path: PathBuf,
}

impl Config {
    fn new(name: impl Into<String>) -> Self {
        Config {
            name: name.into(),
            path: PathBuf::new(),
        }
    }
    
    fn path(mut self, path: impl Into<PathBuf>) -> Self {
        self.path = path.into();
        self
    }
}

// Clean builder calls
let config = Config::new("myapp")
    .path("/etc/myapp");
```

## Related Rules
- [api-impl-asref](./api-impl-asref.md) - When to use AsRef instead
- [api-from-not-into](./api-from-not-into.md) - Why From is preferred
- [err-from-impl](./err-from-impl.md) - From for error conversion
