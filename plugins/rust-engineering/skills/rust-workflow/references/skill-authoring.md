# Specialized Rust Skill Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Control plane: `$rust-workflow`.
- Scope retained: Problem-first classification, uncertainty reduction, decision-unit ownership, coding constraints, and verification handoff.
- Baseline correction: Build the current phase with the canonical `ProfileStack`; do not load the whole catalog or let profiles co-own one decision.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

## Quick Responses to Common Problems

### Ownership Problems (E0382, E0597)
```
Problem: a value is used after being moved
Reasoning:
1. Is ownership actually required? → Use a reference, &T
2. Is sharing required? → Use Arc<T>
3. Is a copy required? → Use clone() or the Copy trait

Recommendation: first ask "Why does this need to move?" A borrow usually solves the problem.
```

### Lifetime Problems (E0106, E0597)
```
Problem: lifetime annotations are missing or do not match
Reasoning:
1. When returning a reference, which input supplies its lifetime?
2. When a struct contains references, what should its lifetime parameter be called?
3. Can an owned type be returned to avoid the lifetime?

Recommendation: lifetime annotations are documentation. Good annotations make the relationships immediately clear to readers.
```

### Send/Sync Problems (E0277)
```
Problem: a type cannot be sent or shared across threads
Reasoning:
1. Send: are all fields Send?
2. Sync: are the interior-mutability types thread-safe?
3. Is Rc used? → Replace it with Arc

Recommendation: most built-in types satisfy these traits automatically. Problems usually come from Cell, Rc, or raw pointers.
```


## Coding Checklist

- [ ] Propagate errors with `?` instead of `unwrap()`
- [ ] Public APIs have documentation comments
- [ ] Unit tests cover core logic
- [ ] API ergonomics are considered from the caller's perspective
- [ ] unsafe code has SAFETY comments
- [ ] Concurrent code accounts for Send/Sync


## Code-Style Reference<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Good error handling
fn load_config(path: &Path) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)
        .map_err(|e| ConfigError::Io(e))?;
    toml::from_str(&content)
        .map_err(ConfigError::Parse)
}

// Good use of ownership
fn process_items(items: &[Item]) -> Vec<Result<Item, Error>> {
    items.iter().map(validate_item).collect()
}

// Good concurrent code
async fn fetch_all(urls: &[Url]) -> Vec<Response> {
    let futures: Vec<_> = urls.iter()
        .map(|u| reqwest::get(u))
        .collect();
    futures::future::join_all(futures).await
}
```


## Questions I Will Ask

When you describe a problem, I will consider:

1. **Is this a language-level problem or a design-level problem?**
   - Language level → Focus on syntax and types
   - Design level → Consider architecture and patterns

2. **Is the best solution or the simplest solution appropriate?**
   - Learning scenario → Prioritize understanding the principles
   - Production environment → Prioritize stability and reliability

3. **Are there domain constraints?**
   - Web development → Consider state management
   - Embedded development → Consider no_std
   - Concurrency-sensitive code → Consider Send/Sync


## How to Collaborate with Me

### This information is helpful:
- What problem are you trying to solve?
- What is the code context: library or application?
- Are there specific constraints such as performance, safety, or compatibility?

### I will respond by:
1. First understanding the essential problem
2. Providing a runnable code example
3. Explaining why the approach works
4. Identifying potential problems and directions for improvement


## Common Command Reference

```bash
# Check without producing build artifacts (fast)
cargo check

# Run tests
cargo test

# Format code
cargo fmt

# Lint code
cargo clippy

# Release build
cargo build --release
```


## Principles

- Do not use unsafe to evade compiler checks
- Do not use `unwrap()` in production code
- Document every public API
- Choose appropriate synchronization primitives for concurrency problems
- Let the compiler detect as many problems as possible




## 2026-02 Additions

### New Skills

- `rust-testing`: unit, integration, property, and concurrency testing with `proptest`/`loom`/`criterion`.
- `rust-database`: SQLx/Diesel/SeaORM patterns, transaction boundaries, migrations, and query performance.
- `rust-observability`: `tracing`, metrics, OpenTelemetry instrumentation, and production diagnostics.

### Routing Hints

- Testing failures or flaky async tests: use `rust-testing`.
- SQL/ORM/transaction/deadlock/migration issues: use `rust-database`.
- Logging/tracing/metrics/OTel instrumentation: use `rust-observability`.
