# Huiali Coding Protocol

> Product adaptation of `skills/rust-coding/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-style-clippy`.
- Supporting profiles when needed: `$rust-idioms`, `$rust-coding-rules`.
- Scope retained: Readable Rust, naming, formatting, Clippy scope, documentation, control flow, API conventions, and reviewable diffs.
- Baseline correction: Project policy and selected toolchain own formatting and lint levels. Avoid universal deny lists, mechanical rewrites, and preferences that conflict with the local contract.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## Naming Conventions (Rust-Specific)

| Rule | Correct | Incorrect |
|------|---------|-----------|
| No `get_` prefix for methods | `fn name(&self)` | `fn get_name(&self)` |
| Iterator methods | `iter()` / `iter_mut()` / `into_iter()` | `get_iter()` |
| Conversion naming | `as_` (cheap), `to_` (expensive), `into_` (ownership) | Mixed usage |
| `static` variables uppercase | `static CONFIG: Config` | `static config: Config` |
| `const` variables | `const BUFFER_SIZE: usize = 1024` | No restriction |

### General Naming

<!-- huiali-source: skills/rust-coding/SKILL.md#rust-block-1; sha256=4d53f06833dda685bb03305666e09b34fca5fc042d714c745c851d20d3b00a4f -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Variables and functions: snake_case
let max_connections = 100;
fn process_data() { ... }

// Types and traits: CamelCase
struct UserSession;
trait Cacheable {}

// Constants: SCREAMING_SNAKE_CASE
const MAX_CONNECTIONS: usize = 100;
static CONFIG: once_cell::sync::Lazy<Config> = ...
```


## Solution Patterns

### Pattern 1: Conversion Methods

<!-- huiali-source: skills/rust-coding/SKILL.md#rust-block-2; sha256=0475ea3214d7dd1d6f96fcee057953b47c9563969ab212998e7a53f84bea7ca4 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
impl Buffer {
    // as_ - cheap, view conversion
    pub fn as_slice(&self) -> &[u8] {
        &self.data
    }

    // to_ - expensive, allocating conversion
    pub fn to_vec(&self) -> Vec<u8> {
        self.data.clone()
    }

    // into_ - consuming, ownership transfer
    pub fn into_vec(self) -> Vec<u8> {
        self.data
    }
}
```

### Pattern 2: Newtype Pattern

<!-- huiali-source: skills/rust-coding/SKILL.md#rust-block-3; sha256=94b7a19fd4a3d087c767d2412c91ea04a4e9bd8be60d26bbf52f7c87aa31f8fe -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ Domain semantics with newtypes
struct Email(String);
struct UserId(u64);
struct Meters(f64);

impl Email {
    pub fn new(s: impl Into<String>) -> Result<Self, EmailError> {
        let email = s.into();
        if email.contains('@') {
            Ok(Self(email))
        } else {
            Err(EmailError::Invalid)
        }
    }
}
```

### Pattern 3: Error Handling

<!-- huiali-source: skills/rust-coding/SKILL.md#rust-block-4; sha256=f84816c79ca3ca7dae6a29bd588aa3d427d8aea5968cdfff655a0263632e14bc -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ Good: propagate errors
fn read_config() -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string("config.toml")
        .map_err(ConfigError::from)?;
    toml::from_str(&content)
        .map_err(ConfigError::Parse)
}

// ❌ Avoid: panic in library code
fn read_config() -> Config {
    std::fs::read_to_string("config.toml").unwrap()  // panic!
}

// ✅ Use expect when invariant guaranteed
fn get_user(&self) -> &User {
    self.user.as_ref()
        .expect("user always initialized in constructor")
}
```

### Pattern 4: String Handling

<!-- huiali-source: skills/rust-coding/SKILL.md#rust-block-5; sha256=73b5d40802ac40ba15e9533cb21a100f6f1185abef41f50bad1e39abce5af419 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ Accept &str in APIs
fn greet(name: &str) {
    println!("Hello, {}", name);
}

// ✅ Use Cow when might need owned
use std::borrow::Cow;

fn process(input: &str) -> Cow<str> {
    if input.contains("special") {
        Cow::Owned(input.replace("special", "normal"))
    } else {
        Cow::Borrowed(input)
    }
}

// ✅ Pre-allocate when size known
let mut s = String::with_capacity(100);
```


## Data Type Guidelines

| Rule | Description | Example |
|------|-------------|---------|
| Use newtype | Domain semantics | `struct Email(String)` |
| Use slice patterns | Pattern matching | `if let [first, .., last] = slice` |
| Pre-allocate | Avoid reallocations | `Vec::with_capacity()` |
| Avoid Vec abuse | Fixed size → array | `let arr: [u8; 256]` |

### String Guidelines

| Rule | Description |
|------|-------------|
| ASCII data use `bytes()` | `s.bytes()` faster than `s.chars()` |
| Might modify → `Cow<str>` | Borrow or owned |
| Use `format!` for concat | Better than `+` operator |
| Avoid nested `contains()` | O(n*m) complexity |


## Error Handling Guidelines

| Rule | Description |
|------|-------------|
| Use `?` to propagate | Don't use `try!()` macro |
| `expect()` over `unwrap()` | When value guaranteed |
| Use `assert!` for invariants | At function entry |


## Memory and Lifetimes

| Rule | Description |
|------|-------------|
| Meaningful lifetime names | `'src`, `'ctx` not just `'a` |
| `RefCell` use `try_borrow` | Avoid panics |
| Use shadowing for conversions | `let x = x.parse()?` |


## Concurrency Guidelines

| Rule | Description |
|------|-------------|
| Define lock ordering | Prevent deadlocks |
| Atomics for primitives | Not `Mutex<bool>` |
| Choose memory ordering carefully | Relaxed/Acquire/Release/SeqCst |


## Async Guidelines

| Rule | Description |
|------|-------------|
| CPU-bound → sync | Async for I/O |
| Don't hold locks across await | Use scoped guards |


## Macro Guidelines

| Rule | Description |
|------|-------------|
| Avoid macros (unless necessary) | Prefer functions/generics |
| Macro input like Rust | Readability first |


## Deprecated Patterns → Modern

| Deprecated | Modern | Version |
|-----------|---------|---------|
| `lazy_static!` | `std::sync::OnceLock` | 1.70 |
| `once_cell::Lazy` | `std::sync::LazyLock` | 1.80 |
| `std::sync::mpsc` | Keep or replace only when required semantics and measurements justify it | project-specific |
| `std::sync::Mutex` | Keep or replace only when lock semantics and measurements justify it | project-specific |
| `failure`/`error-chain` | `thiserror`/`anyhow` | - |
| `try!()` | `?` operator | 2018 |


## Clippy Configuration

```toml
[package]
edition = "2024"
# rust-version = "<project MSRV>"

[lints.rust]
unsafe_code = "warn"

[lints.clippy]
all = "warn"
# Enable selected pedantic lints individually when the project benefits.
```

### Common Clippy Lints

| Lint | Description |
|------|-------------|
| `clippy::all` | Enable all warnings |
| `clippy::pedantic` | Stricter checks |
| `clippy::unwrap_used` | Avoid unwrap |
| `clippy::expect_used` | Review `expect` at invariant boundaries; it is not preferred universally |
| `clippy::clone_on_ref_ptr` | Avoid cloning Arc |


## Formatting (rustfmt)

```bash
# Use default config
rustfmt src/lib.rs

# Check formatting
rustfmt --check src/lib.rs

# Config file: .rustfmt.toml
max_width = 100
tab_spaces = 4
edition = "2024"
```


## Documentation Guidelines

<!-- huiali-source: skills/rust-coding/SKILL.md#rust-block-6; sha256=890317b88f0f88b2e0a396007260ba29dc61d671b2ea515e163e46739aa25195 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
/// Module documentation
//! This module handles user authentication...

/// Struct documentation
///
/// # Examples
/// ```
/// let user = User::new("name");
/// ```
pub struct User { ... }

/// Method documentation
///
/// # Arguments
///
/// * `name` - User name
///
/// # Returns
///
/// Initialized user instance
///
/// # Panics
///
/// Panics when name is empty
pub fn new(name: &str) -> Self { ... }
```


## Workflow

### Step 1: Name Things Properly

```
Choosing a name?
  → Function/variable? snake_case
  → Type/trait? CamelCase
  → Constant? SCREAMING_SNAKE_CASE
  → Conversion method?
    - Cheap view? as_foo()
    - Expensive? to_foo()
    - Consuming? into_foo()
```

### Step 2: Format Code

```bash
# Run rustfmt
cargo fmt

# Check formatting in CI
cargo fmt --check

# Fix clippy warnings
cargo clippy --fix
```

### Step 3: Review Idioms

```
Check:
  → No unnecessary clone()
  → Use ? not unwrap()
  → &str in function parameters
  → Iterator methods not index loops
  → Meaningful error types
```


## Quick Reference

```
Naming: snake_case (fn/var), CamelCase (type), SCREAMING_SNAKE_CASE (const)
Format: rustfmt (just use it)
Docs: /// for public items, //! for module docs
Lint: #![warn(clippy::all)]
```


## Review Checklist

When reviewing code:

- [ ] Naming follows Rust conventions
- [ ] Using `?` instead of `unwrap()`
- [ ] Avoiding unnecessary `clone()`
- [ ] `unsafe` blocks have SAFETY comments
- [ ] Public APIs have doc comments
- [ ] Ran `cargo clippy`
- [ ] Ran `cargo fmt`
- [ ] No `get_` prefix on accessor methods
- [ ] Conversion methods named correctly (as/to/into)
- [ ] String parameters use `&str` when possible


## Verification Commands

```bash
# Format check
cargo fmt --check

# Lint check
cargo clippy -- -D warnings

# Documentation check
cargo doc --no-deps --open

# Run tests
cargo test

# Check naming conventions
cargo clippy -- -W clippy::wrong_self_convention
```


## Common Pitfalls

### 1. Wrong Method Naming

**Symptom**: Clippy warning `wrong_self_convention`

<!-- huiali-source: skills/rust-coding/SKILL.md#rust-block-7; sha256=644089c4d49f8fe61d8d12601ad1f97917825f8e0b8195c0653fe0ceee07d6b9 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: unnecessary get_ prefix
impl User {
    fn get_name(&self) -> &str { &self.name }
}

// ✅ Good: direct accessor
impl User {
    fn name(&self) -> &str { &self.name }
}
```

### 2. String Type Misuse

**Symptom**: Unnecessary allocations

<!-- huiali-source: skills/rust-coding/SKILL.md#rust-block-8; sha256=34955d15f6f0247fc00cc96125ddb45a16aa97f323adcd62cec097c4e6571a1e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: forces allocation
fn greet(name: String) {
    println!("Hello, {}", name);
}

// ✅ Good: accepts borrowed or owned
fn greet(name: &str) {
    println!("Hello, {}", name);
}

// Both work now:
greet("Alice");  // &str
greet(&owned_string);  // &String → &str
```

### 3. Index Loops

**Symptom**: Less idiomatic, error-prone

<!-- huiali-source: skills/rust-coding/SKILL.md#rust-block-9; sha256=202d84e96c6d2d0acce230273f3bf6dfc41b9810a8c5a3a610e6a1e54888cbca -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: manual indexing
for i in 0..items.len() {
    println!("{}: {}", i, items[i]);
}

// ✅ Good: iterator
for item in &items {
    println!("{}", item);
}

// ✅ Good: with index
for (i, item) in items.iter().enumerate() {
    println!("{}: {}", i, item);
}
```


## Related Skills

- **rust-anti-pattern** - What not to do
- **rust-error** - Error handling patterns
- **rust-performance** - Performance idioms
- **rust-async** - Async conventions
- **rust-unsafe** - SAFETY comment style

## Additional unique source examples

These code-only deltas appeared in the condensed English or localized source. They remain fragments, not dependency or hardware claims.

### `SKILL_EN.md` example 1

<!-- huiali-source: skills/rust-coding/SKILL_EN.md#rust-block-1; sha256=063ae383aefa63bff6a0e097b2de5d560ede6d6e5c03fe4ffb1976301fe3f5bc -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
pub struct UserId(String);

impl UserId {
    pub fn parse(value: &str) -> Result<Self, &'static str> {
        if value.is_empty() { return Err("empty user id"); }
        Ok(Self(value.to_owned()))
    }
}
```

### `SKILL_ZH.md` example 1

<!-- huiali-source: skills/rust-coding/SKILL_ZH.md#rust-block-1; sha256=f766d106ecefb750bc9edd2f81743ceb0fb86bc25670a99b35d9abe5c0e0124e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 变量和函数：snake_case
let max_connections = 100;
fn process_data() { ... }

// 类型和 trait：CamelCase
struct UserSession;
trait Cacheable {}

// 常量：SCREAMING_SAME_CASE
const MAX_CONNECTIONS: usize = 100;
static CONFIG:once_cell::sync::Lazy<Config> = ...
```

### `SKILL_ZH.md` example 2

<!-- huiali-source: skills/rust-coding/SKILL_ZH.md#rust-block-2; sha256=e34b40e5b2f7ced23dc273f098b42027e10374482434a8eb30e5e4074d99b67f -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ 好的错误处理
fn read_config() -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string("config.toml")
        .map_err(ConfigError::from)?;
    toml::from_str(&content)
        .map_err(ConfigError::parse)
}

// ❌ 避免
fn read_config() -> Config {
    std::fs::read_to_string("config.toml").unwrap()  // panic!
}
```

### `SKILL_ZH.md` example 3

<!-- huiali-source: skills/rust-coding/SKILL_ZH.md#rust-block-3; sha256=75a7f58c56d778a6c0af9c97a4ffa4d51770aa18f39554c4492ed1790a19ac9b -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
/// 模块文档
//! 本模块处理用户认证...

/// 结构体文档
///
/// # Examples
/// ```
/// let user = User::new("name");
/// ```
pub struct User { ... }

/// 方法文档
///
/// # Arguments
///
/// * `name` - 用户名
///
/// # Returns
///
/// 初始化后的用户实例
///
/// # Panics
///
/// 当用户名为空时 panic
pub fn new(name: &str) -> Self { ... }
```
