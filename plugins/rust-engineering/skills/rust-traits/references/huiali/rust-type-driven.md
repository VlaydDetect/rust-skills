# Huiali Type Driven Protocol

> Product adaptation of `skills/rust-type-driven/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-traits`.
- Supporting profiles when needed: `$rust-api-design`, `$rust-stable`.
- Scope retained: Newtypes, typestate, sealed states, capability types, trait bounds, associated types, and invalid-state elimination.
- Baseline correction: Use type-level states when they materially remove invalid runtime states; avoid type-state explosion and preserve diagnostics, semver, and compile-time cost.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## Solution Patterns

### Pattern 1: Newtype Pattern

<!-- huiali-source: skills/rust-type-driven/SKILL.md#rust-block-1; sha256=d347c14634132b1c6b7f2573e414a11563051f2381cd82cb8a3155b179319731 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Primitive types can be confused
fn process_user(id: u64) { ... }
fn process_order(id: u64) { ... }

// Easy to mix up:
process_order(user_id);  // Compiles but wrong!

// ✅ Type-safe newtypes
struct UserId(u64);
struct OrderId(u64);

fn process_user(id: UserId) { ... }
fn process_order(id: OrderId) { ... }

// Compiler prevents:
// process_order(user_id);  // Compile error!
```

**When to use:**
- Domain-specific identifiers
- Values with different semantics but same representation
- Adding type-level validation

### Pattern 2: Type State Pattern

<!-- huiali-source: skills/rust-type-driven/SKILL.md#rust-block-2; sha256=c905f1a8aafecebebdb365d7c1ea995feaefd3422f61ff5260f8a1c2efdfe88e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Encode states in types
struct Disconnected;
struct Connecting;
struct Connected;

struct Connection<State = Disconnected> {
    socket: TcpSocket,
    _state: PhantomData<State>,
}

impl Connection<Disconnected> {
    pub fn new() -> Self {
        Connection {
            socket: TcpSocket::new(),
            _state: PhantomData,
        }
    }

    pub fn connect(self) -> Connection<Connecting> {
        // Start connection...
        Connection {
            socket: self.socket,
            _state: PhantomData,
        }
    }
}

impl Connection<Connecting> {
    pub fn finish(self) -> Result<Connection<Connected>, Error> {
        // Complete connection...
        Ok(Connection {
            socket: self.socket,
            _state: PhantomData,
        })
    }
}

impl Connection<Connected> {
    pub fn send(&mut self, data: &[u8]) -> Result<(), Error> {
        // Only Connected state can send
        self.socket.write(data)
    }
}

// Type state prevents invalid operations:
let conn = Connection::new();
// conn.send(data);  // Compile error! Not connected yet
let conn = conn.connect();
let mut conn = conn.finish()?;
conn.send(data)?;  // OK!
```

### Pattern 3: PhantomData for Ownership

<!-- huiali-source: skills/rust-type-driven/SKILL.md#rust-block-3; sha256=c3d6c60a47d0883798683a42b97910d8996981daa6bdcb9dff73959db29a96fc -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::marker::PhantomData;

// PhantomData marks ownership and variance
struct MyIterator<'a, T> {
    ptr: *const T,
    end: *const T,
    _marker: PhantomData<&'a T>,  // Tells compiler: we borrow T
}

// Without PhantomData, compiler doesn't know about the 'a lifetime
```

### Pattern 4: Builder Pattern with Type State

<!-- huiali-source: skills/rust-type-driven/SKILL.md#rust-block-4; sha256=119179afbd4f259382e178b3d7d15bb8248a9de125b557b2f02ad05668aa86ce -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Type-safe builder that enforces required fields
struct HostSet;
struct HostUnset;
struct PortSet;
struct PortUnset;

struct ConfigBuilder<H, P> {
    host: Option<String>,
    port: Option<u16>,
    _host: PhantomData<H>,
    _port: PhantomData<P>,
}

impl ConfigBuilder<HostUnset, PortUnset> {
    pub fn new() -> Self {
        ConfigBuilder {
            host: None,
            port: None,
            _host: PhantomData,
            _port: PhantomData,
        }
    }
}

impl<P> ConfigBuilder<HostUnset, P> {
    pub fn host(self, host: impl Into<String>) -> ConfigBuilder<HostSet, P> {
        ConfigBuilder {
            host: Some(host.into()),
            port: self.port,
            _host: PhantomData,
            _port: PhantomData,
        }
    }
}

impl<H> ConfigBuilder<H, PortUnset> {
    pub fn port(self, port: u16) -> ConfigBuilder<H, PortSet> {
        ConfigBuilder {
            host: self.host,
            port: Some(port),
            _host: PhantomData,
            _port: PhantomData,
        }
    }
}

// Only works when both required fields are set
impl ConfigBuilder<HostSet, PortSet> {
    pub fn build(self) -> Config {
        Config {
            host: self.host.unwrap(),
            port: self.port.unwrap(),
        }
    }
}

// Usage:
let config = ConfigBuilder::new()
    .host("localhost")
    .port(8080)
    .build();  // OK

// Won't compile without required fields:
// ConfigBuilder::new().build();  // Error!
```


## Making Invalid States Unrepresentable

<!-- huiali-source: skills/rust-type-driven/SKILL.md#rust-block-5; sha256=0f9d25c706c34875cb84ab086ddbcb836c907be198078cd9ee200cd433b88cc0 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Easy to create invalid state
struct User {
    name: String,
    email: Option<String>,  // Might be empty
    age: u32,
}

// ✅ Email cannot be invalid
struct User {
    name: String,
    email: Email,  // Type guarantees validity
    age: u32,
}

struct Email(String);

impl Email {
    pub fn new(s: impl Into<String>) -> Result<Self, EmailError> {
        let s = s.into();
        if s.contains('@') && s.len() > 3 {
            Ok(Email(s))
        } else {
            Err(EmailError::Invalid)
        }
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}
```


## Marker Traits

<!-- huiali-source: skills/rust-type-driven/SKILL.md#rust-block-6; sha256=b1d59caa82802cf561254c2d61337a66fac0546cf0221dab0845dcd4c220bc52 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Use marker traits to signal capabilities
trait Sendable: Send + 'static {}

// Sealed trait pattern (prevent external implementation)
mod sealed {
    pub trait Sealed {}
}

pub trait MyTrait: sealed::Sealed {
    fn method(&self);
}

// Only types we define can implement MyTrait
struct MyType;
impl sealed::Sealed for MyType {}
impl MyTrait for MyType {
    fn method(&self) { ... }
}
```


## Zero-Sized Types (ZST)

<!-- huiali-source: skills/rust-type-driven/SKILL.md#rust-block-7; sha256=d3e0f372bd90046277ae7c196433a8692dc77b2d94b0671c2f40b127d38227b3 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Use ZST for compile-time markers (no runtime cost)
struct DebugOnly;
struct Always;

struct Logger<Mode = Always> {
    _marker: PhantomData<Mode>,
}

impl Logger<DebugOnly> {
    pub fn log(&self, msg: &str) {
        #[cfg(debug_assertions)]
        println!("[DEBUG] {}", msg);
    }
}

impl Logger<Always> {
    pub fn log(&self, msg: &str) {
        println!("[LOG] {}", msg);
    }
}

// ZST has zero runtime cost:
assert_eq!(std::mem::size_of::<Logger<DebugOnly>>(), 0);
```


## Workflow

### Step 1: Identify Domain Invariants

```
What can go wrong?
  → IDs mixed up? Use newtype
  → Invalid state transitions? Use type state
  → Optional fields always present? Remove Option
  → Values need validation? Validate in constructor
```

### Step 2: Choose Type Pattern

```
Need to:
  → Prevent ID confusion? Newtype pattern
  → Encode state machine? Type state pattern
  → Enforce required fields? Builder with type state
  → Mark variance/ownership? PhantomData
  → Zero-cost abstraction? ZST
```

### Step 3: Validate at Construction

<!-- huiali-source: skills/rust-type-driven/SKILL.md#rust-block-8; sha256=f9e562e7ab60d3b6334965b90683f07ea3805e5bf6893525151c282139ab5554 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ Validation at construction
impl Email {
    pub fn new(s: &str) -> Result<Self, Error> {
        validate(s)?;  // Validate once
        Ok(Email(s.to_string()))
    }
}

// Now Email is always valid
fn send_email(to: Email) {
    // No need to re-validate
}
```


## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `is_valid` flag | Runtime checking | Use type states |
| Many `Option`s | Nullable everywhere | Redesign types |
| Primitive types everywhere | Type confusion | Newtype pattern |
| Runtime validation | Late error discovery | Constructor validation |
| Boolean parameters | Unclear meaning | Use enum or builder |


## Validation Timing

| Validation Type | Best Time | Example |
|-----------------|-----------|---------|
| Range validation | Construction | `Email::new()` returns `Result` |
| State transitions | Type boundaries | `Connection<Connected>` |
| Reference validity | Lifetimes | `&'a T` |
| Thread safety | `Send + Sync` | Compiler checks |


## Review Checklist

When reviewing type design:

- [ ] Invalid states are unrepresentable
- [ ] Newtypes used for domain concepts
- [ ] Validation happens at construction
- [ ] Type states prevent invalid operations
- [ ] No boolean blindness (use enums)
- [ ] PhantomData correctly marks ownership
- [ ] Builder enforces required fields
- [ ] Marker traits document capabilities
- [ ] ZSTs used for zero-cost abstractions


## Verification Commands

```bash
# Check type sizes
cargo build --release
nm target/release/myapp | grep MyType

# Ensure ZST optimization
objdump -d target/release/myapp | grep -A 10 my_function

# Test type-level guarantees
cargo test --lib
```


## Common Pitfalls

### 1. Boolean Blindness

**Symptom**: Unclear what true/false means

<!-- huiali-source: skills/rust-type-driven/SKILL.md#rust-block-9; sha256=6ee6bef270378ab1fbca7776f9037c2f1d4f5f467eabb87b52748c8612a90b78 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: what does true mean?
fn connect(hostname: &str, secure: bool) { ... }

// ✅ Good: explicit type
enum ConnectionMode {
    Secure,
    Insecure,
}

fn connect(hostname: &str, mode: ConnectionMode) { ... }
```

### 2. Optional Fields That Shouldn't Be

**Symptom**: Lots of `Option` everywhere

<!-- huiali-source: skills/rust-type-driven/SKILL.md#rust-block-10; sha256=9d92f745d1b4e28553358700c86ed4bdc447f4d650c90e6c8e500e6a73246c05 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: user email should always exist
struct User {
    name: String,
    email: Option<String>,
}

// ✅ Good: validate at construction
struct User {
    name: String,
    email: Email,  // Always valid
}
```

### 3. Missing Newtype

**Symptom**: Mixing up IDs

<!-- huiali-source: skills/rust-type-driven/SKILL.md#rust-block-11; sha256=6039b2d2f15e806ca7fc0cf626a887da9b10fa88306c830d8a0d5eb69732384e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: easy to confuse
fn transfer_money(from: u64, to: u64, amount: u64) { ... }

// transfer_money(amount, to, from);  // Oops!

// ✅ Good: type safety
fn transfer_money(from: AccountId, to: AccountId, amount: Money) { ... }
```


## Related Skills

- **rust-ownership** - Lifetime and borrowing fundamentals
- **rust-trait** - Advanced trait patterns
- **rust-pattern** - Design pattern implementations
- **rust-zero-cost** - Zero-cost abstractions
- **rust-linear-type** - Linear types and session types

## Additional unique source examples

These code-only deltas appeared in the condensed English or localized source. They remain fragments, not dependency or hardware claims.

### `SKILL_ZH.md` example 1

<!-- huiali-source: skills/rust-type-driven/SKILL_ZH.md#rust-block-1; sha256=80b42c089af2bd05bbf798ef628f27f77f182c479a1e00b84231e2a08fde5de0 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ 原始类型容易被混淆
struct UserId(u64);
struct OrderId(u64);

// ✅ 类型安全：无法混用
fn get_user(user_id: UserId) { ... }
fn get_order(order_id: OrderId) { ... }

// 编译器会阻止：
// get_order(user_id);  // 编译错误！
```

### `SKILL_ZH.md` example 2

<!-- huiali-source: skills/rust-type-driven/SKILL_ZH.md#rust-block-2; sha256=692ee8cdf4049a25632e78ff295d845aee50949ba66e21c7294e99527795abf5 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 用类型编码状态
struct Disconnected;
struct Connecting;
struct Connected;

struct Connection<State = Disconnected> {
    socket: TcpSocket,
    _state: PhantomData<State>,
}

impl Connection<Disconnected> {
    fn connect(self) -> Connection<Connecting> {
        // ...
        Connection { socket: self.socket, _state: PhantomData }
    }
}

impl Connection<Connected> {
    fn send(&mut self, data: &[u8]) {
        // 只有 Connected 状态可以发送
    }
}
```

### `SKILL_ZH.md` example 3

<!-- huiali-source: skills/rust-type-driven/SKILL_ZH.md#rust-block-3; sha256=905bc9a77f02e124bcf1bc7124d96804f4123b8c3ef69f742b5a124f324380d9 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 用 PhantomData 标记所有权和方差
struct MyIterator<'a, T> {
    _marker: PhantomData<&'a T>,
}

// 告诉编译器：我们借用了一个 T 的生命周期
```

### `SKILL_ZH.md` example 4

<!-- huiali-source: skills/rust-type-driven/SKILL_ZH.md#rust-block-4; sha256=98199379d14b0e291c9a8aae8c3b1c67199990a60b7cfd2905ca934cad1fc840 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ 容易创建无效状态
struct User {
    name: String,
    email: Option<String>,  // 可能为空
    age: u32,
}

// ✅ email 不可能为空
struct User {
    name: String,
    email: Email,  // 类型保证有效
    age: u32,
}

struct Email(String);

impl Email {
    fn new(s: &str) -> Option<Self> {
        if s.contains('@') {
            Some(Email(s.to_string()))
        } else {
            None
        }
    }
}
```

### `SKILL_ZH.md` example 5

<!-- huiali-source: skills/rust-type-driven/SKILL_ZH.md#rust-block-5; sha256=3b73f41a29eee19d98455849055d2b803e62a50b5e12d9833b9649df33fac034 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
struct ConfigBuilder {
    host: String,
    port: u16,
    timeout: u64,
    retries: u32,
}

impl ConfigBuilder {
    fn new() -> Self {
        Self {
            host: "localhost".to_string(),
            port: 8080,
            timeout: 30,
            retries: 3,
        }
    }

    fn host(mut self, host: impl Into<String>) -> Self {
        self.host = host.into();
        self
    }

    fn port(mut self, port: u16) -> Self {
        self.port = port;
        self
    }

    fn build(self) -> Config {
        // 可以在这里做最终验证
        Config {
            host: self.host,
            port: self.port,
        }
    }
}
```

### `SKILL_ZH.md` example 6

<!-- huiali-source: skills/rust-type-driven/SKILL_ZH.md#rust-block-6; sha256=67fe006e1c12e635cdf611db44922f4eea9bdd67b88ce119b9296b1a3120af90 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 用 marker trait 标记能力
trait Sendable: Send + 'static {}

// 或用 marker 做类型约束
struct Cache<T: Cacheable> {
    data: T,
}

trait Cacheable: Send + Sync {}
```

### `SKILL_ZH.md` example 7

<!-- huiali-source: skills/rust-type-driven/SKILL_ZH.md#rust-block-7; sha256=82a2ff539e2081d5284ca0eed1fc19a3e4415b40819b2dc895f0fc8b7c193d13 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 用 ZST 做标记
struct DebugOnly;
struct Always;

// 只在 debug 模式执行的代码
struct DebugLogger<Mode = Always> {
    _marker: PhantomData<Mode>,
}

impl DebugLogger<DebugOnly> {
    fn log(&self, msg: &str) {
        println!("[DEBUG] {}", msg);
    }
}
```
