# Huiali Error Protocol

> Product adaptation of `skills/rust-error/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-errors`.
- Supporting profiles when needed: `$rust-api-design`.
- Scope retained: Result propagation, error boundaries, context, recoverability, domain errors, panic policy, and source chains.
- Baseline correction: Evaluate unwrap and expect at the boundary and against the invariant. Neither is universally preferred or forbidden; public and recoverable paths need deliberate error contracts.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## Solution Patterns

### Pattern 1: Option for Normal Absence

<!-- huiali-source: skills/rust-error/SKILL.md#rust-block-1; sha256=ffaf7cb4a8d661719e97e552ac46d4e3e0874996f5516f29ec0ee12ea2785d67 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Lookup operations where "not found" is normal
fn find_user(id: u32) -> Option<User> {
    users.get(&id)
}

// Usage patterns
match find_user(123) {
    Some(user) => println!("Found: {}", user.name),
    None => println!("User not found"),
}

// Or convert to Result for propagation
let user = find_user(123).ok_or(UserNotFoundError)?;
```

**When to use**: Queries, lookups, optional configuration values.

**Key insight**: `None` carries no information, just absence.

### Pattern 2: Result for Expected Failures

<!-- huiali-source: skills/rust-error/SKILL.md#rust-block-2; sha256=1b08395532d289e6d5c983e7c2887f6b5f003f24be44714c1988e7fffbc4e59d -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// File might not exist (expected failure)
fn read_config(path: &Path) -> Result<String, io::Error> {
    std::fs::read_to_string(path)
}

// Network request might timeout
fn fetch(url: &str) -> Result<Response, reqwest::Error> {
    reqwest::blocking::get(url)
}
```

**When to use**: I/O operations, parsing, validation, network calls.

**Key insight**: Error type carries information about *why* it failed.

### Pattern 3: Custom Error Types (thiserror)

<!-- huiali-source: skills/rust-error/SKILL.md#rust-block-3; sha256=94d983568736130181f00877716bd878ff96d3382fbe3263db25479372759a2e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ParseError {
    #[error("invalid format: {0}")]
    InvalidFormat(String),

    #[error("missing required field: {0}")]
    MissingField(&'static str),

    #[error("IO error")]
    Io(#[from] io::Error),

    #[error("parse error: {0}")]
    Parse(#[from] serde_json::Error),
}

// Use in library code
pub fn parse_config(input: &str) -> Result<Config, ParseError> {
    let raw: RawConfig = serde_json::from_str(input)?;  // Auto-converts
    validate_config(raw)
}
```

**When to use**: Library code, public APIs, need type-safe error handling.

**Trade-offs**: More boilerplate, but precise error types.

### Pattern 4: Flexible Errors (anyhow)

<!-- huiali-source: skills/rust-error/SKILL.md#rust-block-4; sha256=e401463848ec4828ea8b869e49114a9aee1225b7d42995e8a8e725c82a69a526 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use anyhow::{Context, Result, bail};

fn process_request() -> Result<Response> {
    let config = std::fs::read_to_string("config.json")
        .context("failed to read config file")?;

    let parsed: Config = serde_json::from_str(&config)
        .context("failed to parse config as JSON")?;

    if !parsed.is_valid() {
        bail!("invalid configuration: missing API key");
    }

    Ok(build_response(parsed))
}
```

**When to use**: Application code, rapid development, error context matters more than types.

**Trade-offs**: Loses type information, but gains flexibility and context.


## Workflow

### Step 1: Classify the Failure

```
Is absence normal?
  → Option<T>

Is failure expected and recoverable?
  → Result<T, E>

Is this a bug or invariant violation?
  → panic!() or assert!()
```

### Step 2: Choose Error Representation

```
Library code (public API)?
  → thiserror (typed errors)

Application code (internal)?
  → anyhow (flexible errors)

Need error conversions?
  → Implement From traits
```

### Step 3: Propagate or Handle

```
Can caller handle this?
  → Return Result, use ?

Need to add context?
  → .context("why it failed")?

Must handle here?
  → match / if let / unwrap_or
```


## Error Propagation Best Practices

### ✅ Good Patterns

<!-- huiali-source: skills/rust-error/SKILL.md#rust-block-5; sha256=20bb87b72a1aae370249356d58a44c881d69c7ef36b9220285b963a309c7765d -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Clear error types
fn validate() -> Result<(), ValidationError> {
    if name.is_empty() {
        return Err(ValidationError::EmptyName);
    }
    Ok(())
}

// Add context during propagation
let config = File::open("config.json")
    .context("failed to open config.json")?;

// Use ? operator
let data = read_file(&path)?;

// Provide defaults
let timeout = config.timeout.unwrap_or(Duration::from_secs(30));

// Pattern match for complex handling
match parse_input(input) {
    Ok(value) => process(value),
    Err(ParseError::InvalidFormat(msg)) => log_and_retry(msg),
    Err(e) => return Err(e),
}
```

### ❌ Anti-Patterns

<!-- huiali-source: skills/rust-error/SKILL.md#rust-block-6; sha256=d3af8c27d273029d955131c5d860072ce675618df5aacdb893661613fe580863 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ unwrap() on operations that can fail
let content = std::fs::read_to_string("config.json").unwrap();

// ❌ Silently ignore errors
let _ = some_fallible_operation();

// ❌ Generic error messages
Err(anyhow!("error"))  // Too vague

// ❌ Converting all errors to strings
.map_err(|e| e.to_string())?  // Loses type info

// ❌ Panic for expected failures
let num: i32 = input.parse().expect("parse failed");  // User input!
```


## When to Panic

### ✅ Acceptable Panic Scenarios

| Scenario | Example | Reasoning |
|----------|---------|-----------|
| Invariant violation | Array index out of bounds | Programming bug |
| Initialization checks | `env::var("HOME").expect(...)` | Required for program to run |
| Test assertions | `assert_eq!(result, expected)` | Verify assumptions |
| Unrecoverable state | OOM, corrupted data structures | Can't continue safely |

<!-- huiali-source: skills/rust-error/SKILL.md#rust-block-7; sha256=f070bc6380a0fc3f9df9d9ff5c95e34e3f9de898b9fd68999321bdc32242fa7e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ Acceptable: initialization check
let api_key = std::env::var("API_KEY")
    .expect("API_KEY environment variable must be set");

// ✅ Acceptable: test assertion
#[test]
fn test_user_creation() {
    let user = create_user("Alice");
    assert_eq!(user.name, "Alice");
}

// ✅ Acceptable: invariant violation
let first = queue.pop().expect("queue should never be empty at this point");
```

### ❌ Unacceptable Panic Scenarios

<!-- huiali-source: skills/rust-error/SKILL.md#rust-block-8; sha256=4889b20c1a13ffcec893563c309e40f6b40dfa5af97b73c43b8a5b91cd476d57 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ User input validation
let num: i32 = input.parse().unwrap();  // Use Result instead

// ❌ Network operations
let response = reqwest::blocking::get(url).unwrap();  // Use Result

// ❌ File operations
let config = std::fs::read_to_string("config.json").unwrap();  // Use Result
```


## Error Type Design

### Enum for Multiple Error Cases

<!-- huiali-source: skills/rust-error/SKILL.md#rust-block-9; sha256=bf3c05abc0f8ccd78273d438555da820aed180388eb0464357f9042b74774f47 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
#[derive(Error, Debug)]
pub enum ConfigError {
    #[error("file not found at {path}")]
    FileNotFound { path: String },

    #[error("invalid syntax at line {line}: {message}")]
    InvalidSyntax { line: usize, message: String },

    #[error("missing required field: {0}")]
    MissingField(String),

    #[error(transparent)]
    Io(#[from] io::Error),

    #[error(transparent)]
    Parse(#[from] serde_json::Error),
}
```

### Nested Errors with Context

<!-- huiali-source: skills/rust-error/SKILL.md#rust-block-10; sha256=36a1b9d0529cc4d05361e4fc6c61d2cb09c1f120b229d190c4619b0e3beec4ca -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
#[derive(Error, Debug)]
pub enum AppError {
    #[error("configuration error")]
    Config(#[from] ConfigError),

    #[error("database error")]
    Database(#[from] DatabaseError),

    #[error("authentication failed: {0}")]
    Auth(String),
}
```


## Common Pitfalls

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| `.unwrap()` everywhere | Production panics | Use `?` or `.with_context()` |
| `Box<dyn Error>` | Loses type information | Use thiserror enums |
| Silent error ignoring | Bugs go unnoticed | Handle or propagate |
| Deep error hierarchies | Over-engineering | Design as needed |
| Panic for control flow | Abusing panic | Use normal control flow |
| String errors | No pattern matching | Use typed errors |


## Quick Reference

| Scenario | Choice | Tool |
|----------|--------|------|
| Library returns custom errors | `Result<T, CustomEnum>` | thiserror |
| Application rapid development | `Result<T, anyhow::Error>` | anyhow |
| Absence is normal | `Option<T>` | `None` / `Some(x)` |
| Intentional panic | `panic!()` / `assert!()` | Special cases only |
| Error conversion | `.map_err()` / `.context()` | Add context |
| Fallback values | `.unwrap_or()` / `.unwrap_or_else()` | Safe defaults |
| Early return | `?` operator | Propagate errors |


## Review Checklist

When reviewing error handling code:

- [ ] All fallible operations return `Result` or `Option`
- [ ] Error types are meaningful (not just `String`)
- [ ] Error context is preserved through propagation
- [ ] `unwrap()` used only with justification (comments)
- [ ] `panic!()` used only for bugs or unrecoverable states
- [ ] Library code uses typed errors (thiserror)
- [ ] Application code adds context (anyhow `.context()`)
- [ ] Error messages are actionable for users/operators
- [ ] No silent error swallowing (`let _ = ...`)
- [ ] Tests cover error paths, not just happy paths


## Verification Commands

```bash
# Check for unwrap/expect usage
cargo clippy -- -W clippy::unwrap_used -W clippy::expect_used

# Check for panic in production code
cargo clippy -- -W clippy::panic

# Run tests including error paths
cargo test

# Check for unused Results
cargo clippy -- -D unused_must_use

# Verify error types implement Error trait
cargo check
```


## Conversion Patterns

### Option ↔ Result

<!-- huiali-source: skills/rust-error/SKILL.md#rust-block-11; sha256=6ea8e1e8ba1b496c88ad4fbf6260ca5f44def39740b90c3e0cb5eaa0f9ef56c0 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Option → Result
let result: Result<T, E> = option.ok_or(error_value)?;
let result: Result<T, E> = option.ok_or_else(|| compute_error())?;

// Result → Option
let option: Option<T> = result.ok();

// Result<Option<T>, E> → Result<T, E>
result.and_then(|opt| opt.ok_or(error))?;
```

### Error Type Conversions

<!-- huiali-source: skills/rust-error/SKILL.md#rust-block-12; sha256=e985f7ed15fb3d639e03b1a0146c1b17a7af24f5557a56d55cacbdac671daa8e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Manual conversion
.map_err(|e| MyError::from(e))?;

// Automatic with #[from]
// Requires: #[derive(Error, Debug)] with #[from] attribute
result?;  // Auto-converts if From impl exists

// Add context
.map_err(|e| MyError::Wrapped(e.to_string()))?;

// Use anyhow for flexibility
.context("operation failed")?;
```


## Advanced: Error Source Chains

<!-- huiali-source: skills/rust-error/SKILL.md#rust-block-13; sha256=7a317f96296221fcc1da6876c18dedeb4c7b48d3f067118a2b3edf04184e0f52 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::error::Error;

fn print_error_chain(e: &dyn Error) {
    eprintln!("Error: {}", e);

    let mut source = e.source();
    while let Some(e) = source {
        eprintln!("  Caused by: {}", e);
        source = e.source();
    }
}

// Usage
if let Err(e) = dangerous_operation() {
    print_error_chain(&e);
}
```


## Related Skills

- **rust-error-advanced** - Advanced error patterns (thiserror, anyhow, error chains)
- **rust-anti-pattern** - Error handling anti-patterns to avoid
- **rust-coding** - Error handling coding standards
- **rust-web** - Error handling in web contexts
- **rust-async** - Error handling in async code

## Additional unique source examples

These code-only deltas appeared in the condensed English or localized source. They remain fragments, not dependency or hardware claims.

### `SKILL_ZH.md` example 1

<!-- huiali-source: skills/rust-error/SKILL_ZH.md#rust-block-1; sha256=890bee34fda4590abea5230363347d138ff61f559d911e9ad78aa6baac47060a -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 查找操作，找不到是正常情况
fn find_user(id: u32) -> Option<User> {
    users.get(&id)
}

// 使用
let user = find_user(123);
if let Some(u) = user {
    println!("Found: {}", u.name);
}

// 或者用 ? 传播（但要包装成 Result）
let user = find_user(123).ok_or(UserNotFound)?;
```

### `SKILL_ZH.md` example 2

<!-- huiali-source: skills/rust-error/SKILL_ZH.md#rust-block-2; sha256=e4334443d8fd3189584cb0ec151ded5ec76af18f9558159ced055b5876dc1e3c -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 文件可能不存在
fn read_file(path: &Path) -> Result<String, io::Error> {
    std::fs::read_to_string(path)
}

// 网络请求可能超时
fn fetch(url: &str) -> Result<Response, reqwest::Error> {
    reqwest::blocking::get(url)?
}
```

### `SKILL_ZH.md` example 3

<!-- huiali-source: skills/rust-error/SKILL_ZH.md#rust-block-3; sha256=f92817a433d5dea20c1d01cea9c3e07c8898d0a788336abc7c40ab2d5aecd01e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ParseError {
    #[error("invalid format: {0}")]
    InvalidFormat(String),

    #[error("missing field: {0}")]
    MissingField(&'static str),

    #[error("IO error: {source}")]
    Io {
        #[from]
        source: io::Error,
    },
}
```

### `SKILL_ZH.md` example 4

<!-- huiali-source: skills/rust-error/SKILL_ZH.md#rust-block-4; sha256=ae615017fa1b4dc4ba8332d92add473c20b4b44b5c0b1674019ff0b1d25964f4 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use anyhow::{Context, Result, bail};

fn process_config() -> Result<Config> {
    let content = std::fs::read_to_string("config.json")
        .context("failed to read config file")?;

    let config: Config = serde_json::from_str(&content)
        .context("failed to parse config")?;

    Ok(config)
}
```

### `SKILL_ZH.md` example 5

<!-- huiali-source: skills/rust-error/SKILL_ZH.md#rust-block-5; sha256=7cdebc01d7314f98e92dc4a9637002df9f3c1a940f86b0ebbff7263dc57afb3f -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ 好：明确区分错误类型
fn validate() -> Result<(), ValidationError> {
    if name.is_empty() {
        return Err(ValidationError::EmptyName);
    }
    Ok(())
}

// ✅ 好：传播时添加上下文
let config = File::open("config.json")
    .map_err(|e| ConfigError::with_context("config", e))?;

// ✅ 好：使用 ? 运算符
let data = read_file(&path)?;

// ❌ 差：unwrap() 在可能失败的操作上
let content = std::fs::read_to_string("config.json").unwrap();

// ❌ 差：静默忽略错误
let _ = some_fallible_function();
```

### `SKILL_ZH.md` example 6

<!-- huiali-source: skills/rust-error/SKILL_ZH.md#rust-block-6; sha256=fafeaffffa6ec83eea8db4669c4a6dbb9e5a16f53d2ce74aa78d45d45b840eae -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ 可接受：初始化检查
let home = std::env::var("HOME")
    .expect("HOME environment variable must be set");

// ✅ 可接受：测试断言
assert!(!users.is_empty(), "should have at least one user");

// ❌ 不可接受：用户输入验证失败
let num: i32 = input.parse().unwrap();
```
