# Huiali Ecosystem Protocol

> Product adaptation of `skills/rust-ecosystem/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-ecosystem`.
- Supporting profiles when needed: `$rust-crate-discovery`, `$rust-research`.
- Scope retained: Solution classes, ecosystem maturity, maintenance, portability, interoperability, and evidence-led crate selection.
- Baseline correction: Treat crate names and popularity as time-sensitive leads. Resolve project constraints and verify current upstream status before recommending or adding a dependency.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## Async Runtimes

| Runtime | Characteristics | Use Case |
|---------|----------------|----------|
| **tokio** | Most popular, feature-rich | General async applications |
| **async-std** | std-like API | Prefer std-style APIs |
| **smol** | Minimal, embeddable | Lightweight applications |
| **async-executors** | Unified interface | Need runtime portability |

```toml
# Web services
tokio = { version = "1", features = ["full"] }
axum = "0.7"

# Lightweight
async-std = "1"

# Minimal
smol = "2"
```


## Solution Patterns

### Pattern 1: Web Service Stack

```toml
[dependencies]
# Async runtime
tokio = { version = "1", features = ["full"] }

# Web framework
axum = "0.7"

# Database
sqlx = { version = "0.7", features = ["runtime-tokio", "postgres"] }

# Serialization
serde = { version = "1", features = ["derive"] }
serde_json = "1"

# Error handling
anyhow = "1"
thiserror = "1"

# Tracing
tracing = "0.1"
tracing-subscriber = "0.3"
```

### Pattern 2: CLI Tool Stack

```toml
[dependencies]
# Argument parsing
clap = { version = "4", features = ["derive"] }

# Error handling
anyhow = "1"

# Config
config = "0.13"
dotenvy = "0.15"

# Progress
indicatif = "0.17"

# Terminal colors
colored = "2"
```

### Pattern 3: Data Processing

```toml
[dependencies]
# Parallelism
rayon = "1"

# CSV
csv = "1"

# Serialization
serde = { version = "1", features = ["derive"] }
serde_json = "1"

# HTTP client
reqwest = { version = "0.11", features = ["json", "blocking"] }
```


## Web Frameworks

| Framework | Characteristics | Performance |
|-----------|----------------|-------------|
| **axum** | Tower middleware, type-safe | High |
| **actix-web** | Highest performance | Highest |
| **rocket** | Developer-friendly | Medium |
| **warp** | Compositional, filters | High |

<!-- huiali-source: skills/rust-ecosystem/SKILL.md#rust-block-1; sha256=015c0008d3cd3e5f7be86db7868da10b94694ec5acf1bdfef7518f38a9de4ac3 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// axum example
use axum::{Router, routing::get, Json};
use serde::Serialize;

#[derive(Serialize)]
struct User {
    id: u64,
    name: String,
}

async fn get_user() -> Json<User> {
    Json(User {
        id: 1,
        name: "Alice".to_string(),
    })
}

let app = Router::new()
    .route("/user", get(get_user));
```


## Serialization

| Library | Characteristics | Performance |
|---------|----------------|-------------|
| **serde** | Standard choice | High |
| **bincode** | Binary, compact | Highest |
| **postcard** | no_std, embedded | High |
| **ron** | Readable format | Medium |

<!-- huiali-source: skills/rust-ecosystem/SKILL.md#rust-block-2; sha256=df5cade92baee66effb3b17d4b56dc6a99c785ffacce6094d3100366ff1e4794 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct User {
    id: u64,
    name: String,
}

// JSON
let json = serde_json::to_string(&user)?;
let user: User = serde_json::from_str(&json)?;

// Binary (more efficient)
let bytes = bincode::serialize(&user)?;
let user: User = bincode::deserialize(&bytes)?;
```


## HTTP Clients

| Library | Characteristics |
|---------|----------------|
| **reqwest** | Most popular, easy to use |
| **ureq** | Sync, simple |
| **surf** | Async, modern |
| **hyper** | Low-level, flexible |

<!-- huiali-source: skills/rust-ecosystem/SKILL.md#rust-block-3; sha256=11f62fb636ccba012c9b3de93e2630a01140d6cd0f036bf690af5cb3f6ff7346 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// reqwest - async
let response = reqwest::Client::new()
    .post("https://api.example.com")
    .json(&payload)
    .send()
    .await?
    .json::<Response>()
    .await?;

// ureq - sync (no async runtime needed)
let response: Response = ureq::post("https://api.example.com")
    .send_json(&payload)?
    .into_json()?;
```


## Databases

| Type | Library |
|------|---------|
| ORM | **sqlx**, diesel, sea-orm |
| Raw SQL | **sqlx**, tokio-postgres |
| NoSQL | mongodb, redis |
| Connection pool | **sqlx**, deadpool, r2d2 |

<!-- huiali-source: skills/rust-ecosystem/SKILL.md#rust-block-4; sha256=e6bff25341360a40cbcfc87749c98dea5ff72733be634550cd62344993ac2038 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// sqlx with compile-time checked queries
use sqlx::PgPool;

let pool = PgPool::connect(&database_url).await?;

let user = sqlx::query_as!(
    User,
    "SELECT id, name FROM users WHERE id = $1",
    user_id
)
.fetch_one(&pool)
.await?;
```


## Concurrency & Parallelism

| Scenario | Candidates to verify against the current project |
|----------|---------------|
| Data parallelism | **rayon** |
| Work stealing | Existing runtime or a currently maintained work-stealing implementation |
| Channels | Standard or resolved runtime/crate channel matching required semantics |
| Atomics | **std::sync::atomic** |

<!-- huiali-source: skills/rust-ecosystem/SKILL.md#rust-block-5; sha256=cb290fd629dec39742a495537ffc27f63b30d912a33e5e8292ddebc09ecf4787 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// rayon - easy parallelism
use rayon::prelude::*;

let sum: i32 = data
    .par_iter()
    .map(|x| expensive_computation(x))
    .sum();
```


## Error Handling

| Library | Use Case |
|---------|----------|
| **thiserror** | Library error types |
| **anyhow** | Application error propagation |
| **snafu** | Structured errors |

<!-- huiali-source: skills/rust-ecosystem/SKILL.md#rust-block-6; sha256=0e831166481cc40a7013504706bb74f3caef1093e5627d212bd4db7169bfad25 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// thiserror - for libraries
use thiserror::Error;

#[derive(Error, Debug)]
pub enum MyError {
    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Invalid data: {msg}")]
    Invalid { msg: String },
}

// anyhow - for applications
use anyhow::{Context, Result};

fn load_config() -> Result<Config> {
    let content = std::fs::read_to_string("config.toml")
        .context("failed to read config file")?;

    toml::from_str(&content)
        .context("failed to parse config")
}
```


## Common Tools

| Scenario | Library |
|----------|---------|
| CLI parsing | **clap** (v4), structopt |
| Logging | **tracing**, log |
| Config | **config**, dotenvy |
| Testing | **tempfile**, rstest, proptest |
| Time | **chrono**, time |
| Random | **rand** |
| Regex | **regex** |


## Crate Selection Principles

1. **Active maintenance**: Check GitHub activity, recent updates
2. **Download count**: Reference crates.io downloads
3. **MSRV**: Minimum Supported Rust Version compatibility
4. **Dependencies**: Number and security of dependencies
5. **Documentation**: Complete docs and examples
6. **License**: MIT/Apache2 compatibility

```bash
# Check crate info
cargo info <crate-name>

# Check dependencies
cargo tree

# Security audit
cargo audit

# License check
cargo deny check licenses
```


## Workflow

### Step 1: Identify Need

```
What problem to solve?
  → Web service? Choose framework (axum/actix)
  → CLI tool? Use clap + anyhow
  → Data processing? Use rayon
  → Database access? Use sqlx
```

### Step 2: Evaluate Options

```
Check:
  → crates.io download count
  → GitHub stars and activity
  → Documentation quality
  → Recent releases
  → Community support
```

### Step 3: Verify Safety

```bash
# Security audit
cargo audit

# License compatibility
cargo deny check

# Dependency tree
cargo tree -i <crate>
```


## Deprecated Patterns → Modern

| Deprecated | Modern | Reason |
|-----------|--------|--------|
| `lazy_static` | `std::sync::OnceLock` | std built-in |
| `rand::thread_rng` | `rand::rng()` | New API |
| `failure` | `thiserror` + `anyhow` | More popular |
| `serde_derive` | `serde` (unified) | Simpler imports |


## Quick Reference

| Scenario | Recommended Stack |
|----------|------------------|
| Web service | axum + tokio + sqlx + serde |
| CLI tool | clap + anyhow + config |
| Serialization | serde + (json/bincode/postcard) |
| Parallel compute | rayon |
| Config management | config + dotenvy |
| Logging | tracing + tracing-subscriber |
| Testing | tempfile + rstest + proptest |
| Date/time | chrono or time |


## Review Checklist

When selecting crates:

- [ ] Crate is actively maintained (updated within 6 months)
- [ ] Good documentation and examples
- [ ] Reasonable dependency count
- [ ] No known security issues (cargo audit)
- [ ] Compatible license (MIT/Apache2)
- [ ] MSRV compatible with project
- [ ] High download count and community usage
- [ ] Stable API (1.0+ or widely used)


## Verification Commands

```bash
# Search crates
cargo search <keyword>

# Get crate info
cargo info <crate-name>

# Check dependencies
cargo tree

# Security audit
cargo audit

# License check
cargo deny check

# Check for updates
cargo outdated
```


## Common Pitfalls

### 1. Too Many Dependencies

**Symptom**: Long compile times, dependency conflicts

```toml
# ❌ Avoid: unnecessary dependencies
[dependencies]
# Don't need full tokio if only using channels
tokio = { version = "1", features = ["full"] }

# ✅ Better: minimal features
tokio = { version = "1", features = ["sync"] }
```

### 2. Unmaintained Crates

**Symptom**: Security vulnerabilities, incompatibilities

```bash
# Check last update
cargo info <crate-name>

# Check for alternatives
cargo search <similar-crate>
```

### 3. Version Conflicts

**Symptom**: Build failures, duplicate dependencies

```bash
# Diagnose conflicts
cargo tree -d

# Use same version across workspace
[workspace.dependencies]
serde = "1"
```


## Related Skills

- **rust-async** - Async runtime patterns
- **rust-web** - Web framework usage
- **rust-error** - Error handling libraries
- **rust-testing** - Testing libraries
- **rust-performance** - Performance-critical crates

## Additional unique source examples

These code-only deltas appeared in the condensed English or localized source. They remain fragments, not dependency or hardware claims.

### `SKILL_ZH.md` example 1

<!-- huiali-source: skills/rust-ecosystem/SKILL_ZH.md#rust-block-1; sha256=fb1fe2cf13b643c54895c7458e216b10c675c478570e358a10e17bad3939ac19 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct User {
    id: u64,
    name: String,
}

// JSON
let json = serde_json::to_string(&user)?;

// 二进制
let bytes = bincode::serialize(&user)?;
```

### `SKILL_ZH.md` example 2

<!-- huiali-source: skills/rust-ecosystem/SKILL_ZH.md#rust-block-2; sha256=ea0ca1362f10efc86054435806dfcf1affbadc028776cb84e5db58b8462d0028 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// reqwest
let response = reqwest::Client::new()
    .post("https://api.example.com")
    .json(&payload)
    .send()
    .await?;
```
