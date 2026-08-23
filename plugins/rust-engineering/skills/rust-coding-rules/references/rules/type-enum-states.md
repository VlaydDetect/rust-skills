# type-enum-states

> Use enums for mutually exclusive states## Decision

Consider this rule only after its prerequisites are satisfied: Use enums for mutually exclusive states.

## Apply When

Apply when a type can encode a real invariant, state, identity, representation, or output contract more reliably than convention, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the extra type machinery does not eliminate a meaningful invalid state or would make a local operation harder to use. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Name the invalid states, choose the smallest nominal or algebraic representation, and review construction and conversion boundaries.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Type-driven guarantees move failures earlier but can expand public surface, conversion code, generic complexity, and diagnostics.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`serde`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Use compile-pass, compile-fail, and runtime boundary cases to prove valid construction and rejection paths.

## Why It Matters

When a value can be in exactly one of several states, an enum makes invalid states unrepresentable. The compiler ensures all states are handled. Contrast with boolean flags or optional fields that can represent impossible combinations.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
struct Connection {
    is_connected: bool,
    is_authenticated: bool,
    is_disconnected: bool,  // Can all three be true? False?
    socket: Option<TcpStream>,
    credentials: Option<Credentials>,
}

// Possible invalid states:
// - is_connected && is_disconnected (contradiction)
// - is_authenticated && !is_connected (impossible)
// - socket is None but is_connected is true (inconsistent)
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
enum ConnectionState {
    Disconnected,
    Connecting { address: SocketAddr },
    Connected { socket: TcpStream },
    Authenticated { socket: TcpStream, session: Session },
    Failed { error: ConnectionError },
}

struct Connection {
    state: ConnectionState,
}

// Impossible states are unrepresentable
// Each state has exactly the data it needs
```

## Pattern Matching Ensures Completeness

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern Matching Ensures Completeness illustration -->
```rust
fn handle_connection(conn: &Connection) {
    match &conn.state {
        ConnectionState::Disconnected => {
            println!("Not connected");
        }
        ConnectionState::Connecting { address } => {
            println!("Connecting to {}", address);
        }
        ConnectionState::Connected { socket } => {
            println!("Connected, not authenticated");
        }
        ConnectionState::Authenticated { socket, session } => {
            println!("Authenticated as {}", session.user);
        }
        ConnectionState::Failed { error } => {
            println!("Failed: {}", error);
        }
    }
    // Compiler error if any state is missing
}
```

## State Transitions

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the State Transitions illustration -->
```rust
impl Connection {
    fn connect(&mut self, addr: SocketAddr) -> Result<(), Error> {
        match &self.state {
            ConnectionState::Disconnected => {
                self.state = ConnectionState::Connecting { address: addr };
                Ok(())
            }
            _ => Err(Error::AlreadyConnected),
        }
    }
    
    fn on_connected(&mut self, socket: TcpStream) {
        if let ConnectionState::Connecting { .. } = &self.state {
            self.state = ConnectionState::Connected { socket };
        }
    }
    
    fn authenticate(&mut self, creds: Credentials) -> Result<(), Error> {
        match std::mem::replace(&mut self.state, ConnectionState::Disconnected) {
            ConnectionState::Connected { socket } => {
                let session = perform_auth(&socket, creds)?;
                self.state = ConnectionState::Authenticated { socket, session };
                Ok(())
            }
            other => {
                self.state = other;
                Err(Error::NotConnected)
            }
        }
    }
}
```

## Result and Option as State Enums

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Result and Option as State Enums illustration -->
```rust
// Option<T> is an enum for "might not exist"
enum Option<T> {
    Some(T),
    None,
}

// Result<T, E> is an enum for "might have failed"
enum Result<T, E> {
    Ok(T),
    Err(E),
}

// Use these instead of nullable/sentinel values
fn find_user(id: u64) -> Option<User> { ... }
fn parse_config(s: &str) -> Result<Config, ParseError> { ... }
```

## Avoid Boolean Flags

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Avoid Boolean Flags illustration -->
```rust
// Bad: boolean flags
struct Task {
    is_running: bool,
    is_completed: bool,
    is_failed: bool,
    error: Option<Error>,
}

// Good: enum state
enum TaskState {
    Pending,
    Running { started_at: Instant },
    Completed { result: Output },
    Failed { error: Error },
}

struct Task {
    state: TaskState,
}
```

## Related Rules
- [api-typestate](./api-typestate.md) - Type-level state machines
- [api-non-exhaustive](./api-non-exhaustive.md) - Forward-compatible enums
- [type-option-nullable](./type-option-nullable.md) - Option for optional values
- [pat-exhaustive-enum](./pat-exhaustive-enum.md) - Match owned enums exhaustively
- [serde-enum-representation](./serde-enum-representation.md) - Choose enum wire tagging
