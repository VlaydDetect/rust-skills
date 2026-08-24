# Specialized Rust Type Driven Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Primary owner: `$rust-traits`.
- Supporting profiles when needed: `$rust-api-design`, `$rust-stable`.
- Scope retained: Newtypes, typestate, sealed states, capability types, trait bounds, associated types, and invalid-state elimination.
- Baseline correction: Use type-level states when they materially remove invalid runtime states; avoid type-state explosion and preserve diagnostics, semver, and compile-time cost.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

## Solution Patterns

### Pattern 1: Newtype Pattern<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
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

### Pattern 2: Type State Pattern<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
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

### Pattern 3: PhantomData for Ownership<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
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

### Pattern 4: Builder Pattern with Type State<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
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


## Making Invalid States Unrepresentable<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
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


## Marker Traits<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
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


## Zero-Sized Types (ZST)<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
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

### Step 3: Validate at Construction<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
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

**Symptom**: Unclear what true/false means<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
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

**Symptom**: Lots of `Option` everywhere<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
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

**Symptom**: Mixing up IDs<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
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

### `SKILL_ZH.md` example 1<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Primitive types are easy to mix up
struct UserId(u64);
struct OrderId(u64);

// ✅ Type-safe: the values cannot be mixed up
fn get_user(user_id: UserId) { ... }
fn get_order(order_id: OrderId) { ... }

// The compiler rejects this:
// get_order(user_id);  // Compile error!
```

### `SKILL_ZH.md` example 2<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Encode state in types
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
        // Only the Connected state can send
    }
}
```

### `SKILL_ZH.md` example 3<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Use PhantomData to represent ownership and variance
struct MyIterator<'a, T> {
    _marker: PhantomData<&'a T>,
}

// Tell the compiler that we borrow a T for this lifetime
```

### `SKILL_ZH.md` example 4<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Invalid states are easy to construct
struct User {
    name: String,
    email: Option<String>,  // May be absent
    age: u32,
}

// ✅ email cannot be absent
struct User {
    name: String,
    email: Email,  // The type guarantees validity
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

### `SKILL_ZH.md` example 5<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
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
        // Final validation can happen here
        Config {
            host: self.host,
            port: self.port,
        }
    }
}
```

### `SKILL_ZH.md` example 6<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Use a marker trait to represent a capability
trait Sendable: Send + 'static {}

// Or use a marker as a type constraint
struct Cache<T: Cacheable> {
    data: T,
}

trait Cacheable: Send + Sync {}
```

### `SKILL_ZH.md` example 7<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Use a ZST as a marker
struct DebugOnly;
struct Always;

// Code that runs only in debug mode
struct DebugLogger<Mode = Always> {
    _marker: PhantomData<Mode>,
}

impl DebugLogger<DebugOnly> {
    fn log(&self, msg: &str) {
        println!("[DEBUG] {}", msg);
    }
}
```
