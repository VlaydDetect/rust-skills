# api-impl-asref

> Use `AsRef<T>` when you only need to borrow the inner data## Decision

Use this context-sensitive Rust decision when its premise is established: Use `AsRef<T>` when you only need to borrow the inner data.

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

`AsRef<T>` provides a cheap borrowed view of data without taking ownership or copying. Functions accepting `impl AsRef<T>` can work with multiple types that contain or represent `T`, making APIs flexible while avoiding unnecessary allocations. Use `AsRef` when you only need to read, `Into` when you need to own.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Forces callers to provide exact types
fn process_text(text: &str) { ... }
fn read_file(path: &Path) { ... }

// Can't call directly with owned types
let s = String::from("hello");
process_text(&s);  // Works but verbose

let p = PathBuf::from("/file");
read_file(&p);  // Works but verbose
read_file("/file");  // Error! &str != &Path
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Accept anything that can be viewed as the target type
fn process_text(text: impl AsRef<str>) {
    let s: &str = text.as_ref();
    println!("{}", s);
}

fn read_file(path: impl AsRef<Path>) -> io::Result<Vec<u8>> {
    std::fs::read(path.as_ref())
}

// All of these work:
process_text("literal");        // &str
process_text(String::from("owned"));  // String
process_text(Cow::from("cow")); // Cow<str>

read_file("/path/to/file");     // &str  
read_file(Path::new("/path"));  // &Path
read_file(PathBuf::from("/path")); // PathBuf
read_file(OsStr::new("/path")); // &OsStr
```

## AsRef vs Into vs Borrow

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the AsRef vs Into vs Borrow illustration -->
```rust
// AsRef<T>: cheap borrow, no ownership transfer
fn read(p: impl AsRef<Path>) {
    let path: &Path = p.as_ref();
}

// Into<T>: ownership transfer, may allocate
fn store(p: impl Into<PathBuf>) {
    let owned: PathBuf = p.into();
}

// Borrow<T>: like AsRef but with Eq/Hash consistency guarantee
use std::borrow::Borrow;
fn lookup<Q: ?Sized>(map: &HashMap<String, V>, key: &Q) -> Option<&V>
where
    String: Borrow<Q>,
    Q: Hash + Eq,
{
    map.get(key)
}
```

## Implement AsRef for Custom Types

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Implement AsRef for Custom Types illustration -->
```rust
struct Name(String);

impl AsRef<str> for Name {
    fn as_ref(&self) -> &str {
        &self.0
    }
}

impl AsRef<[u8]> for Name {
    fn as_ref(&self) -> &[u8] {
        self.0.as_bytes()
    }
}

// Now Name works with functions expecting AsRef<str>
fn greet(name: impl AsRef<str>) {
    println!("Hello, {}!", name.as_ref());
}

greet(Name("Alice".into()));
```

## Common AsRef Implementations

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Common AsRef Implementations illustration -->
```rust
// Standard library provides many
impl AsRef<str> for String { ... }
impl AsRef<str> for str { ... }
impl AsRef<[u8]> for str { ... }
impl AsRef<[u8]> for String { ... }
impl AsRef<[u8]> for Vec<u8> { ... }
impl AsRef<Path> for str { ... }
impl AsRef<Path> for String { ... }
impl AsRef<Path> for PathBuf { ... }
impl AsRef<Path> for OsStr { ... }
impl AsRef<OsStr> for str { ... }
```

## When to Use Which

| Trait | Use When |
|-------|----------|
| `&T` | Single type, simple API |
| `AsRef<T>` | Read-only access, multiple input types |
| `Into<T>` | Need to store/own the value |
| `Borrow<T>` | HashMap/HashSet keys, Eq/Hash needed |
| `Deref<Target=T>` | Smart pointer semantics |

## Pattern: Optional AsRef Bound

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Optional AsRef Bound illustration -->
```rust
// When T itself might be passed
fn process<T: AsRef<U>, U>(value: T) {
    let inner: &U = value.as_ref();
}

// More flexible: accept T or &T
fn process<T: AsRef<U> + ?Sized, U: ?Sized>(value: &T) {
    let inner: &U = value.as_ref();
}
```

## Related Rules
- [api-impl-into](./api-impl-into.md) - When to use Into instead
- [own-slice-over-vec](./own-slice-over-vec.md) - Using slices for flexibility
- [own-borrow-over-clone](./own-borrow-over-clone.md) - Preferring borrows
