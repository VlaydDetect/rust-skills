# api-builder-pattern

> Use Builder pattern for complex construction

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-api-design; supporters=`rust-traits`, `rust-ownership`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use Builder pattern for complex construction.

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

When a type has many optional parameters or complex initialization, the Builder pattern provides a clear, flexible API. It avoids constructors with many parameters (which are error-prone) and makes the code self-documenting.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Constructor with many parameters - hard to read, easy to get wrong
let client = Client::new(
    "https://api.example.com",  // Which is which?
    30,                          // Timeout? Retries?
    true,                        // What does this mean?
    None,
    Some("auth_token"),
    false,
);

// Or many Option fields
struct Client {
    url: String,
    timeout: Option<Duration>,
    retries: Option<u32>,
    // ... 10 more optional fields
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
#[derive(Default)]
#[must_use = "builders do nothing unless you call build()"]
pub struct ClientBuilder {
    base_url: Option<String>,
    timeout: Option<Duration>,
    max_retries: u32,
    auth_token: Option<String>,
}

impl ClientBuilder {
    pub fn new() -> Self {
        Self::default()
    }
    
    /// Sets the base URL for all requests.
    pub fn base_url(mut self, url: impl Into<String>) -> Self {
        self.base_url = Some(url.into());
        self
    }
    
    /// Sets the request timeout. Default is 30 seconds.
    pub fn timeout(mut self, timeout: Duration) -> Self {
        self.timeout = Some(timeout);
        self
    }
    
    /// Sets the maximum number of retries. Default is 3.
    pub fn max_retries(mut self, n: u32) -> Self {
        self.max_retries = n;
        self
    }
    
    /// Sets the authentication token.
    pub fn auth_token(mut self, token: impl Into<String>) -> Self {
        self.auth_token = Some(token.into());
        self
    }
    
    /// Builds the client with the configured options.
    pub fn build(self) -> Result<Client, BuilderError> {
        let base_url = self.base_url
            .ok_or(BuilderError::MissingBaseUrl)?;
        
        Ok(Client {
            base_url,
            timeout: self.timeout.unwrap_or(Duration::from_secs(30)),
            max_retries: self.max_retries,
            auth_token: self.auth_token,
        })
    }
}

// Usage - clear and self-documenting
let client = ClientBuilder::new()
    .base_url("https://api.example.com")
    .timeout(Duration::from_secs(10))
    .max_retries(5)
    .auth_token("secret")
    .build()?;
```

## Builder Variations

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Builder Variations illustration -->
```rust
// 1. Infallible builder (build() returns T, not Result)
impl WidgetBuilder {
    pub fn build(self) -> Widget {
        Widget {
            color: self.color.unwrap_or(Color::Black),
            size: self.size.unwrap_or(Size::Medium),
        }
    }
}

// 2. Typestate builder (compile-time required field checking)
pub struct ClientBuilder<Url> {
    url: Url,
    timeout: Option<Duration>,
}

pub struct NoUrl;
pub struct HasUrl(String);

impl ClientBuilder<NoUrl> {
    pub fn new() -> Self {
        Self { url: NoUrl, timeout: None }
    }
    
    pub fn url(self, url: String) -> ClientBuilder<HasUrl> {
        ClientBuilder { url: HasUrl(url), timeout: self.timeout }
    }
}

impl ClientBuilder<HasUrl> {
    pub fn build(self) -> Client {
        // url is guaranteed to be set
        Client { url: self.url.0, timeout: self.timeout }
    }
}

// 3. Consuming vs borrowing (consuming is more common)
// Consuming (takes self)
pub fn timeout(mut self, t: Duration) -> Self { ... }

// Borrowing (takes &mut self, allows reuse)
pub fn timeout(&mut self, t: Duration) -> &mut Self { ... }
```

## Evidence from reqwest

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Evidence from reqwest illustration -->
```rust
// https://github.com/seanmonstar/reqwest/blob/master/src/async_impl/client.rs

#[must_use]
pub struct ClientBuilder {
    config: Config,
}

impl ClientBuilder {
    pub fn new() -> ClientBuilder {
        ClientBuilder {
            config: Config::default(),
        }
    }
    
    pub fn timeout(mut self, timeout: Duration) -> ClientBuilder {
        self.config.timeout = Some(timeout);
        self
    }
    
    pub fn build(self) -> Result<Client, Error> {
        // Validation and construction
    }
}
```

## Key Attributes

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Key Attributes illustration -->
```rust
#[derive(Default)]  // Enables MyBuilder::default()
#[must_use = "builders do nothing unless you call build()"]
pub struct MyBuilder { ... }

impl MyBuilder {
    #[must_use]  // Each method should have this
    pub fn option(mut self, value: T) -> Self { ... }
}
```

## Related Rules
- [api-builder-must-use](api-builder-must-use.md) - Add #[must_use] to builders
- [api-typestate](api-typestate.md) - Compile-time state machines
- [api-impl-into](api-impl-into.md) - Accept impl Into for flexibility
