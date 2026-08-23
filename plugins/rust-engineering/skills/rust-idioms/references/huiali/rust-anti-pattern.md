# Huiali Anti Pattern Protocol

> Product adaptation of `skills/rust-anti-pattern/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-idioms`.
- Supporting profiles when needed: `$rust-coding-rules`, `$rust-review`.
- Scope retained: Symptom-to-cause diagnosis for cloning, allocation, stringly APIs, panic, locking, abstraction, collection, and async mistakes.
- Baseline correction: Anti-patterns are contextual warning signs, not bans. Identify the violated invariant or measured cost before rewriting code.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## Top 5 Beginner Mistakes

| Rank | Mistake | Correct Approach |
|------|---------|------------------|
| 1 | Using `.clone()` to escape borrow checker | Use references |
| 2 | Using `.unwrap()` in production code | Use `?` or `with_context()` |
| 3 | Everything is `String` | Use `&str`, `Cow<str>` when needed |
| 4 | Index-based loops | Use iterators `.iter()`, `.enumerate()` |
| 5 | Fighting lifetimes | Redesign data structure |


## Common Anti-Patterns

### Anti-Pattern 1: Clone Everywhere

<!-- huiali-source: skills/rust-anti-pattern/SKILL.md#rust-block-1; sha256=161b67d203252336ed8ca49fbc2ec2cefba0aab6e8e1b03ee9c72d40c8e5f033 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: escaping borrow checker
fn process(user: User) {
    let name = user.name.clone();  // Why clone?
    // ...
}

// ✅ Good: use references
fn process(user: &User) {
    let name = &user.name;  // Just borrow
}
```

**When clone is actually needed:**
- Truly need independent copy
- API design requires owned value
- Data flow requirements

### Anti-Pattern 2: Unwrap in Production

<!-- huiali-source: skills/rust-anti-pattern/SKILL.md#rust-block-2; sha256=bde9b7b455b3f544ad0a2b46dbc1c4ab545959fb808d745d58f1c08bcf188eba -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: may panic
let config = File::open("config.json").unwrap();

// ✅ Good: propagate error
let config = File::open("config.json")?;

// ✅ Good: with context
let config = File::open("config.json")
    .context("failed to open config")?;
```

### Anti-Pattern 3: String Everywhere

<!-- huiali-source: skills/rust-anti-pattern/SKILL.md#rust-block-3; sha256=b0a6bc0550b9574323a65d889dcab3021e3623e8c270865844cc02545b5ff14f -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: unnecessary allocation
fn greet(name: String) {
    println!("Hello, {}", name);
}

// ✅ Good: borrow is enough
fn greet(name: &str) {
    println!("Hello, {}", name);
}

// When String is actually needed: ownership or mutation required
```

### Anti-Pattern 4: Index Loops

<!-- huiali-source: skills/rust-anti-pattern/SKILL.md#rust-block-4; sha256=663f56639ad72fcb81ffbb68fe30da01edd9fdadccfdee0a2bbdae63d80f64c3 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: error-prone, inefficient
for i in 0..items.len() {
    println!("{}: {}", i, items[i]);
}

// ✅ Good: direct iteration
for item in &items {
    println!("{}", item);
}

// ✅ Good: with index
for (i, item) in items.iter().enumerate() {
    println!("{}: {}", i, item);
}
```

### Anti-Pattern 5: Excessive Unsafe

<!-- huiali-source: skills/rust-anti-pattern/SKILL.md#rust-block-5; sha256=6aa148b9883a4e2f04b5d4417d184a5cf316607ca6fd660fcca1794db555b962 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: unsafe for convenience
unsafe {
    let ptr = data.as_mut_ptr();
    // ... complex memory operations
}

// ✅ Good: find safe abstractions
let mut data: Vec<u8> = vec![0; size];
// Vec handles memory management
```


## Solution Patterns

### Pattern 1: Avoiding Clone

<!-- huiali-source: skills/rust-anti-pattern/SKILL.md#rust-block-6; sha256=65f826599604aa9f6b86f1515e66ad2f73bc005e4b9b52014e682a226de855d0 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Anti-pattern: clone to satisfy borrow checker
fn process_data(data: &Data) -> String {
    let cloned = data.items.clone();
    cloned.into_iter().map(|x| x.to_string()).collect()
}

// ✅ Solution: use references properly
fn process_data(data: &Data) -> String {
    data.items.iter().map(|x| x.to_string()).collect()
}
```

### Pattern 2: Proper Error Handling

<!-- huiali-source: skills/rust-anti-pattern/SKILL.md#rust-block-7; sha256=a4e7d147b1c395d4249c6f76fa4f07c796a68508b64b30385724782643735544 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Anti-pattern: unwrap chain
fn load_config() -> Config {
    let content = std::fs::read_to_string("config.toml").unwrap();
    toml::from_str(&content).unwrap()
}

// ✅ Solution: Result propagation
fn load_config() -> Result<Config, Box<dyn Error>> {
    let content = std::fs::read_to_string("config.toml")?;
    Ok(toml::from_str(&content)?)
}

// ✅ Solution: with context (anyhow)
fn load_config() -> anyhow::Result<Config> {
    let content = std::fs::read_to_string("config.toml")
        .context("failed to read config file")?;
    toml::from_str(&content)
        .context("failed to parse config")
}
```

### Pattern 3: String vs &str

<!-- huiali-source: skills/rust-anti-pattern/SKILL.md#rust-block-8; sha256=5677c0873ad4c135758c77732cfd21695e1b81ebcb609669d62a1c72a03c2f9a -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Anti-pattern: String parameters everywhere
struct Config {
    host: String,
    port: String,
    path: String,
}

impl Config {
    fn new(host: String, port: String, path: String) -> Self {
        Self { host, port, path }
    }
}

// ✅ Solution: accept &str, store String
impl Config {
    fn new(host: impl Into<String>, port: u16, path: impl Into<String>) -> Self {
        Self {
            host: host.into(),
            port: port.to_string(),
            path: path.into(),
        }
    }
}
```

### Pattern 4: Iterator-Based Processing

<!-- huiali-source: skills/rust-anti-pattern/SKILL.md#rust-block-9; sha256=8a0a5a8e714505b952b1b47c78d4ba0b9501dad3431301006cc18f78ebccadef -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Anti-pattern: manual indexing
fn sum_even(nums: &[i32]) -> i32 {
    let mut sum = 0;
    for i in 0..nums.len() {
        if nums[i] % 2 == 0 {
            sum += nums[i];
        }
    }
    sum
}

// ✅ Solution: iterator chain
fn sum_even(nums: &[i32]) -> i32 {
    nums.iter()
        .filter(|&&n| n % 2 == 0)
        .sum()
}
```


## Code Smell Quick Reference

| Symptom | Indicates | Refactoring Direction |
|---------|-----------|----------------------|
| Many `.clone()` | Unclear ownership | Clarify data flow |
| Many `.unwrap()` | Missing error handling | Add Result handling |
| Many `pub` fields | Broken encapsulation | Private + accessors |
| Deep nesting | Complex logic | Extract methods |
| Long functions (>50 lines) | Too many responsibilities | Split responsibilities |
| Huge enums | Missing abstraction | Trait + types |


## Outdated → Modern Patterns

| Outdated | Modern |
|----------|--------|
| Index loop `.items[i]` | `.iter().enumerate()` |
| `collect::<Vec<_>>()` then iterate | Chain iterators |
| `lazy_static!` | `std::sync::OnceLock` |
| `mem::transmute` conversion | `as` or `TryFrom` |
| Custom linked list | `Vec` or `VecDeque` |
| Manual unsafe cell | `Cell`, `RefCell` |


## Workflow

### Step 1: Identify Anti-Patterns

```
Code review checklist:
  → Lots of .clone()? Check ownership design
  → .unwrap() in lib code? Need error handling
  → Index loops? Should use iterators
  → pub fields with invariants? Need encapsulation
  → >50 line functions? Should split
```

### Step 2: Ask Key Questions

```
1. Is this fighting Rust or working with Rust?
   Fighting → Redesign
   Working with → Continue

2. Is this clone necessary?
   Escaping borrow checker → Warning sign
   Actually need copy → Keep

3. Will this unwrap panic?
   Might panic → Use ?
   Never panics → expect("reason")

4. Is there a more idiomatic way?
   Check std library patterns
   Review other Rust code
```

### Step 3: Refactor

```
Identified anti-pattern?
  ↓
Understand the root cause
  ↓
Find idiomatic alternative
  ↓
Refactor incrementally
  ↓
Test thoroughly
```


## Review Checklist

When reviewing code:

- [ ] No unreasonable `.clone()`
- [ ] Library code has no `.unwrap()`
- [ ] No `pub` fields with invariants
- [ ] No index loops when iterators available
- [ ] Using `&str` instead of `String` when sufficient
- [ ] Not ignoring `#[must_use]` warnings
- [ ] `unsafe` has SAFETY comments
- [ ] No giant functions (>50 lines)
- [ ] Error handling uses Result not panic
- [ ] No premature optimization


## Verification Commands

```bash
# Check for common issues
cargo clippy

# Specific anti-pattern lints
cargo clippy -- -W clippy::clone_on_copy \
                -W clippy::unwrap_used \
                -W clippy::expect_used

# Check for complexity
cargo clippy -- -W clippy::cognitive_complexity

# Find todos and fixmes
rg "TODO|FIXME|XXX|HACK" --type rust
```


## Common Pitfalls

### 1. Clone to Compile

**Symptom**: Lots of `.clone()` calls

<!-- huiali-source: skills/rust-anti-pattern/SKILL.md#rust-block-10; sha256=49ea2c3f1bdd59495e10ebbe92cbcdf538867700762378480639101449bad30e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: cloning to satisfy compiler
fn process(items: &Vec<Item>) -> Vec<String> {
    let items_clone = items.clone();
    items_clone.into_iter().map(|i| i.name).collect()
}

// ✅ Good: proper borrowing
fn process(items: &[Item]) -> Vec<String> {
    items.iter().map(|i| i.name.clone()).collect()
}

// ✅ Better: no clone at all
fn process(items: &[Item]) -> Vec<&str> {
    items.iter().map(|i| i.name.as_str()).collect()
}
```

### 2. Error Handling Shortcuts

**Symptom**: Unwrap/expect in production code

<!-- huiali-source: skills/rust-anti-pattern/SKILL.md#rust-block-11; sha256=613e15405e2765d81ee2f03abc62305ba0ee227db3d89a8a691b72251f30fca0 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: panic on error
let data = fetch_data().unwrap();
let parsed: Config = serde_json::from_str(&data).expect("bad JSON");

// ✅ Good: proper error propagation
fn load_data() -> Result<Config, Box<dyn Error>> {
    let data = fetch_data()?;
    let parsed = serde_json::from_str(&data)?;
    Ok(parsed)
}
```

### 3. String Allocation Waste

**Symptom**: Unnecessary String allocations

<!-- huiali-source: skills/rust-anti-pattern/SKILL.md#rust-block-12; sha256=f13f5e7cd264e2d2a73dfd817edb5a7e13672309a5cd8397c2091b8092399a9f -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: allocating for no reason
fn log_message(level: String, msg: String) {
    println!("[{}] {}", level, msg);
}

// ✅ Good: borrow when possible
fn log_message(level: &str, msg: &str) {
    println!("[{}] {}", level, msg);
}
```


## Self-Check Questions

### 1. Is this code fighting Rust?

- Fighting → Redesign approach
- Working with → Continue

### 2. Is this clone necessary?

- To escape borrow checker → Warning sign
- Actually need independent copy → OK

### 3. Will this unwrap panic?

- Might panic → Use `?`
- Never panics → `expect("reason")`

### 4. Is there a more idiomatic way?

- Reference other Rust codebases
- Check std library APIs


## Related Skills

- **rust-coding** - Idiomatic patterns to follow
- **rust-ownership** - Understanding borrowing to avoid clones
- **rust-error** - Proper error handling patterns
- **rust-performance** - When optimization matters
- **rust-refactoring** - Systematic code improvement

## Additional unique source examples

These code-only deltas appeared in the condensed English or localized source. They remain fragments, not dependency or hardware claims.

### `SKILL_EN.md` example 1

<!-- huiali-source: skills/rust-anti-pattern/SKILL_EN.md#rust-block-1; sha256=5d3732fb34352d2a09875e06b4ab0cff8b920c67b47c77100c6bb69f70de2462 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Bad: clone used as an escape hatch
fn process(user: User) {
    let name = user.name.clone();
    // ...
}

// Better: borrow instead
fn process(user: &User) {
    let name = &user.name;
}
```

### `SKILL_EN.md` example 2

<!-- huiali-source: skills/rust-anti-pattern/SKILL_EN.md#rust-block-2; sha256=8e0a22b182faa38a4f1ec02fe8b27790e51bba2b48a8a6684d7e1c70bd287deb -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Bad
let config = std::fs::read_to_string("config.json").unwrap();

// Better
let config = std::fs::read_to_string("config.json")?;

// Better with context
let config = std::fs::read_to_string("config.json")
    .map_err(|e| format!("failed to read config.json: {e}"))?;
```

### `SKILL_EN.md` example 3

<!-- huiali-source: skills/rust-anti-pattern/SKILL_EN.md#rust-block-3; sha256=8c63c430572e5741de275625c24e55aff264d63cc7aab894bddb607587e9709b -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Bad: unnecessary allocation at call site
fn greet(name: String) {
    println!("Hello, {name}");
}

// Better
fn greet(name: &str) {
    println!("Hello, {name}");
}
```

### `SKILL_EN.md` example 4

<!-- huiali-source: skills/rust-anti-pattern/SKILL_EN.md#rust-block-4; sha256=ac2fee2173fa8932ec45c3c56dc285d715372fc940486369cf78f0bc29c0c08a -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Bad
for i in 0..items.len() {
    println!("{}: {}", i, items[i]);
}

// Better
for item in &items {
    println!("{item}");
}

// Better with index
for (i, item) in items.iter().enumerate() {
    println!("{}: {}", i, item);
}
```

### `SKILL_EN.md` example 5

<!-- huiali-source: skills/rust-anti-pattern/SKILL_EN.md#rust-block-5; sha256=f1ed4f1061c3e78458d91ae9471a82afa1d934f0765180b38a179d71a2e0c730 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Bad: unsafe used where safe abstractions exist
unsafe {
    let ptr = data.as_mut_ptr();
    // pointer manipulation
}

// Better: prefer safe container operations
let data = vec![0u8; size];
```

### `SKILL_ZH.md` example 1

<!-- huiali-source: skills/rust-anti-pattern/SKILL_ZH.md#rust-block-1; sha256=1ccadf27ab171b0eb33ef9c57e171c19408800604dcaead1372dfdc16862363e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ 不好：躲避借用检查
fn process(user: User) {
    let name = user.name.clone();  // 为什么需要 clone？
    // ...
}

// ✅ 好：直接使用引用
fn process(user: &User) {
    let name = &user.name;  // 借用即可
}
```

### `SKILL_ZH.md` example 2

<!-- huiali-source: skills/rust-anti-pattern/SKILL_ZH.md#rust-block-2; sha256=542d08ac762b1e7048dbff33bfee19432c50ec2732f14956c0e41da79350bb30 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ 不好：可能 panic
let config = File::open("config.json").unwrap();

// ✅ 好：传播错误
let config = File::open("config.json")?;

// ✅ 好：带上下文
let config = File::open("config.json")
    .context("failed to open config")?;
```

### `SKILL_ZH.md` example 3

<!-- huiali-source: skills/rust-anti-pattern/SKILL_ZH.md#rust-block-3; sha256=64349cc97ab8134559fc5c1b18dc2b0ee83c53c748769be4310d598135dbc10b -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ 不好：不必要的分配
fn greet(name: String) {
    println!("Hello, {}", name);
}

// ✅ 好：借用即可
fn greet(name: &str) {
    println!("Hello, {}", name);
}

// 确实需要 String 的场景：需要持有或修改
```

### `SKILL_ZH.md` example 4

<!-- huiali-source: skills/rust-anti-pattern/SKILL_ZH.md#rust-block-4; sha256=b2f75e70d1e5092e46c5edb8d8749c60fefe05698f7109b2dd2bc003db378e90 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ 不好：容易出错，效率低
for i in 0..items.len() {
    println!("{}: {}", i, items[i]);
}

// ✅ 好：直接迭代
for item in &items {
    println!("{}", item);
}

// ✅ 好：需要索引
for (i, item) in items.iter().enumerate() {
    println!("{}: {}", i, item);
}
```

### `SKILL_ZH.md` example 5

<!-- huiali-source: skills/rust-anti-pattern/SKILL_ZH.md#rust-block-5; sha256=6aa2aec9400a4884e268f1b09df2eee30c01417716310f144421600bee46148d -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ 不好：为了省事用 unsafe
unsafe {
    let ptr = data.as_mut_ptr();
    // ... 复杂的内存操作
}

// ✅ 好：寻找安全的抽象
let mut data: Vec<u8> = vec![0; size];
// Vec 已经处理了内存管理
```
