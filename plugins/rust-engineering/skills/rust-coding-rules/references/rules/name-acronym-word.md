# name-acronym-word

> Treat acronyms as words in identifiers: `HttpServer`, not `HTTPServer`## Decision

Use this context-sensitive Rust decision when its premise is established: Treat acronyms as words in identifiers: `HttpServer`, not `HTTPServer`.

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

When acronyms are written in ALL CAPS within identifiers, word boundaries become unclear: is `HTTPSHandler` "HTTPS Handler" or "HTTP SHandler"? Treating acronyms as words (`HttpsHandler`) maintains clear word boundaries and follows Rust convention. The standard library uses this consistently.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// ALL CAPS acronyms - unclear word boundaries
struct HTTPServer { ... }      // HTTP + Server or H + TTP + Server?
struct TCPIPConnection { ... } // TCP + IP? Or other splits?
struct JSONParser { ... }
struct XMLHTTPRequest { ... }  // Very confusing

fn parseJSON(input: &str) { ... }
fn connectTCP(addr: &str) { ... }
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Acronyms as words - clear boundaries
struct HttpServer { ... }      // Http + Server
struct TcpIpConnection { ... } // Tcp + Ip + Connection
struct JsonParser { ... }
struct XmlHttpRequest { ... }

fn parse_json(input: &str) { ... }
fn connect_tcp(addr: &str) { ... }

// More examples
struct Uuid { ... }            // Not UUID
struct Uri { ... }             // Not URI
struct Url { ... }             // Not URL
struct Html { ... }            // Not HTML
struct Css { ... }             // Not CSS
struct Api { ... }             // Not API
```

## Standard Library Examples

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Standard Library Examples illustration -->
```rust
// std uses acronyms as words
std::net::TcpStream            // Not TCPStream
std::net::TcpListener          // Not TCPListener
std::net::UdpSocket            // Not UDPSocket
std::net::IpAddr               // Not IPAddr
std::io::IoError               // Not IOError (though Io is acceptable too)
```

## Two-Letter Acronyms

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Two-Letter Acronyms illustration -->
```rust
// Two-letter acronyms can go either way
struct Io { ... }    // or IO - both acceptable
struct Id { ... }    // or ID - both acceptable

// Preference: treat as word for consistency
struct IoHandler { ... }     // Preferred
struct IdGenerator { ... }   // Preferred
```

## In snake_case

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the In snakecase illustration -->
```rust
// Acronyms become lowercase in snake_case
fn parse_json() { ... }
fn connect_tcp() { ... }
fn generate_uuid() { ... }
fn fetch_http() { ... }
fn encode_url() { ... }

// Variables
let json_response = fetch_json();
let tcp_connection = connect_tcp();
let user_id = generate_uuid();
```

## Mixed Cases

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Mixed Cases illustration -->
```rust
// When acronym is part of compound
struct HttpsConnection { ... }   // Https (not HTTPS)
struct Utf8String { ... }        // Utf8 (not UTF8)
struct Base64Encoder { ... }     // Base64 as word

// Multiple acronyms
struct JsonApiClient { ... }     // Json + Api + Client
struct RestApiHandler { ... }    // Rest + Api + Handler
```

## Related Rules
- [name-types-camel](./name-types-camel.md) - Type naming conventions
- [name-funcs-snake](./name-funcs-snake.md) - Function naming conventions
- [name-consts-screaming](./name-consts-screaming.md) - Constant naming
