# proj-lib-main-split

> Keep `main.rs` minimal, logic in `lib.rs`

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-module-layout; supporters=`rust-workspace`, `rust-cargo-build`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Keep `main.rs` minimal, logic in `lib.rs`.

## Apply When

Apply when a demonstrated module, crate, visibility, target, feature, MSRV, or build-script boundary needs clearer ownership, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the change is driven only by file size or speculative reuse and would add package, public API, build, or migration cost. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Map current owners and public paths, choose the cheapest boundary that enforces responsibility, and plan all callers and configurations.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Stronger boundaries improve ownership and isolation while adding navigation, build graph, feature, release, and migration overhead.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`anyhow`) must already be accepted by the project or be approved before addition.

## Verification

Inspect cargo metadata and public paths, then compile affected packages, features, targets, docs, tests, and generated boundaries.

## Why It Matters

Putting your logic in `lib.rs` makes it testable, reusable, and keeps `main.rs` as a thin entry point. Integration tests can only access your library crate, not binary code in `main.rs`.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// src/main.rs - everything here
fn main() {
    let args = parse_args();
    let config = load_config(&args.config_path).unwrap();
    let db = connect_database(&config.db_url).unwrap();
    
    // Hundreds of lines of application logic...
    // All untestable from integration tests!
}

fn parse_args() -> Args { /* ... */ }
fn load_config(path: &str) -> Result<Config, Error> { /* ... */ }
fn connect_database(url: &str) -> Result<Db, Error> { /* ... */ }
// ... more functions that can't be tested
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// src/main.rs - thin entry point
use my_app::{run, Config};

fn main() -> anyhow::Result<()> {
    let config = Config::from_env()?;
    run(config)
}

// src/lib.rs - all the logic
pub mod config;
pub mod database;
pub mod handlers;

pub use config::Config;

pub fn run(config: Config) -> anyhow::Result<()> {
    let db = database::connect(&config.db_url)?;
    let app = handlers::build_app(db);
    app.run()
}
```

## With CLI Arguments

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the With CLI Arguments illustration -->
```rust
// src/main.rs
use clap::Parser;
use my_app::{run, Args};

fn main() -> anyhow::Result<()> {
    let args = Args::parse();
    run(args)
}

// src/lib.rs
use clap::Parser;

#[derive(Parser, Debug)]
#[command(name = "myapp", version, about)]
pub struct Args {
    #[arg(short, long)]
    pub config: PathBuf,
    
    #[arg(short, long, default_value = "info")]
    pub log_level: String,
}

pub fn run(args: Args) -> anyhow::Result<()> {
    // All application logic here - testable!
}
```

## Project Structure

```
my_app/
├── Cargo.toml
├── src/
│   ├── main.rs       # Entry point only
│   ├── lib.rs        # Library root, re-exports
│   ├── config.rs     # Configuration
│   ├── database.rs   # Database connection
│   └── handlers/     # Request handlers
│       ├── mod.rs
│       └── users.rs
└── tests/
    └── integration.rs  # Can access lib.rs!
```

## Testing Benefits

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Testing Benefits illustration -->
```rust
// tests/integration.rs - can test everything!
use my_app::{Config, run, database};

#[test]
fn test_database_connection() {
    let config = Config::test_config();
    let db = database::connect(&config.db_url).unwrap();
    assert!(db.is_connected());
}

#[test]
fn test_full_workflow() {
    let config = Config::test_config();
    // Test the actual run function
    assert!(my_app::run(config).is_ok());
}
```

## Multiple Binaries

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Multiple Binaries illustration -->
```rust
// src/lib.rs - shared code
pub mod core;
pub mod utils;

// src/bin/server.rs
use my_app::core::Server;

fn main() -> anyhow::Result<()> {
    Server::new()?.run()
}

// src/bin/cli.rs
use my_app::core::Client;

fn main() -> anyhow::Result<()> {
    let client = Client::new()?;
    client.execute_command()
}
```

## Related Rules
- [proj-bin-dir](proj-bin-dir.md) - Put multiple binaries in src/bin/
- [proj-mod-by-feature](proj-mod-by-feature.md) - Organize modules by feature
- [test-integration-dir](test-integration-dir.md) - Integration tests in tests/
