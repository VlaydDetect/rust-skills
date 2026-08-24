# Specialized Rust Skill Index Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Control plane: `$rust-workflow`.
- Scope retained: Precise symptom-to-profile lookup, negative routing, manual invocation, and escalation from mechanics to design or domain reasoning.
- Baseline correction: The product routing index is authoritative. Specialized Rust source names that were merged are reference families, not additional standalone skills.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

## Quick Navigation

| Category | Number of skills | Purpose |
|-----|---------|-----|
| Core skills | 7 | Essentials for daily development |
| Advanced skills | 10 | Deeper Rust understanding |
| Expert skills | 18 | Specialized difficult problems |
| **Total** | **38** | |


## Core Skills (Essential)

| Skill | File | Description |
|-----|------|------|
| **rust-skill** | `rust-skill/SKILL.md` | Rust programming overview and core concepts |
| **rust-ownership** | `rust-ownership/SKILL.md` | Ownership and lifetimes |
| **rust-mutability** | `rust-mutability/SKILL.md` | Mutability in depth |
| **rust-concurrency** | `rust-concurrency/SKILL.md` | Concurrency fundamentals |
| **rust-error** | `rust-error/SKILL.md` | Error-handling fundamentals |
| **rust-error-advanced** | `rust-error-advanced/SKILL.md` | Error handling in depth |
| **rust-coding** | `rust-coding/SKILL.md` | Coding conventions and best practices |


## Advanced Skills

| Skill | File | Description |
|-----|------|------|
| **rust-unsafe** | `rust-unsafe/SKILL.md` | unsafe Rust |
| **rust-anti-pattern** | `rust-anti-pattern/SKILL.md` | Identifying and avoiding anti-patterns |
| **rust-performance** | `rust-performance/SKILL.md` | Performance optimization, including advanced techniques |
| **rust-web** | `rust-web/SKILL.md` | Web-development guide |
| **rust-learner** | `rust-learner/SKILL.md` | Learning paths and resources |
| **rust-ecosystem** | `rust-ecosystem/SKILL.md` | Rust ecosystem and crate selection |
| **rust-cache** | `rust-cache/SKILL.md` | Redis cache management |
| **rust-auth** | `rust-auth/SKILL.md` | JWT and API-key authentication |
| **rust-middleware** | `rust-middleware/SKILL.md` | Middleware patterns |
| **rust-xacml** | `rust-xacml/SKILL.md` | Policy engines and RBAC |


## Expert Skills

| Skill | File | Description |
|-----|------|------|
| **rust-ffi** | `rust-ffi/SKILL.md` | FFI and C/C++ interoperability, including C++ exceptions |
| **rust-pin** | `rust-pin/SKILL.md` | Pin and Unpin in depth |
| **rust-macro** | `rust-macro/SKILL.md` | Macro programming in depth |
| **rust-async** | `rust-async/SKILL.md` | async/await in depth |
| **rust-async-pattern** | `rust-async-pattern/SKILL.md` | Asynchronous design patterns |
| **rust-const** | `rust-const/SKILL.md` | const fn and compile-time computation |
| **rust-embedded** | `rust-embedded/SKILL.md` | Embedded development, including WASM and RISC-V |
| **rust-lifetime-complex** | `rust-lifetime-complex/SKILL.md` | Complex lifetime scenarios |
| **rust-linear-type** | `rust-linear-type/SKILL.md` | Linear types and resource management |
| **rust-coroutine** | `rust-coroutine/SKILL.md` | Coroutines and green threads |
| **rust-ebpf** | `rust-ebpf/SKILL.md` | eBPF and kernel programming |
| **rust-gpu** | `rust-gpu/SKILL.md` | GPU memory and computation |
| **rust-skill-index** | `rust-skill-index/SKILL.md` | Skill index (this file) |


## Skill Classification

### By Difficulty

```
Beginner: rust-skill, rust-ownership, rust-concurrency, rust-error
Intermediate: rust-mutability, rust-unsafe, rust-coding, rust-performance
Advanced: rust-async, rust-pin, rust-macro, rust-ffi, rust-embedded
Expert: rust-ebpf, rust-gpu, rust-coroutine, rust-linear-type
```

### By Domain

```
Systems programming: rust-unsafe, rust-ffi, rust-embedded, rust-ebpf, rust-gpu
Web development: rust-web, rust-async, rust-middleware, rust-auth, rust-xacml
Concurrent programming: rust-concurrency, rust-async, rust-coroutine
Performance optimization: rust-performance, rust-embedded
Type system: rust-ownership, rust-pin, rust-macro, rust-const, rust-lifetime-complex
Error handling: rust-error, rust-error-advanced
Infrastructure: rust-cache, rust-auth, rust-middleware, rust-xacml
```


## Problem Lookup

Choose a skill based on the problem:

| Problem type | Recommended skill |
|---------|---------|
| Ownership/lifetime errors | rust-ownership |
| Borrow conflicts/mutability | rust-mutability |
| Send/Sync errors | rust-concurrency |
| Error-handling strategy | rust-error / rust-error-advanced |
| Asynchronous-code problems | rust-async |
| unsafe code review | rust-unsafe |
| FFI and C++ interoperability | rust-ffi |
| Performance optimization | rust-performance |
| no_std development | rust-embedded |
| eBPF kernel programming | rust-ebpf |
| GPU computation | rust-gpu |
| Coroutine implementation | rust-coroutine |
| Linear-type semantics | rust-linear-type |
| Crate selection | rust-ecosystem |
| Code style | rust-coding |
| Caching strategy | rust-cache |
| Authentication and authorization | rust-auth |
| Web middleware | rust-middleware |
| Policy engine | rust-xacml |



## Newly Added Skills

- `rust-testing` - unit/integration/property/concurrency testing
- `rust-database` - sqlx/diesel/sea-orm, transaction, migration
- `rust-observability` - tracing, metrics, OpenTelemetry
