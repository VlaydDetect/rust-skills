# Rust Coding Guidelines (50 Core Rules)

> Each item is a candidate mapped through the canonical rulebook or owner profile; project contracts override generic style guidance.

## Naming (Rust-Specific)

| Rule | Guideline |
|------|-----------|
| No `get_` prefix | `fn name()` not `fn get_name()` |
| Iterator convention | `iter()` / `iter_mut()` / `into_iter()` |
| Conversion naming | `as_` (cheap &), `to_` (expensive), `into_` (ownership) |
| Static naming | Follow Rust and project naming; do not impose a universal `G_` prefix |

## Data Types

| Rule | Guideline |
|------|-----------|
| Use newtypes | `struct Email(String)` for domain semantics |
| Prefer slice patterns | `if let [first, .., last] = slice` |
| Pre-allocate | `Vec::with_capacity()`, `String::with_capacity()` |
| Avoid Vec abuse | Use arrays for fixed sizes |

## Strings

| Rule | Guideline |
|------|-----------|
| Prefer bytes for proven byte protocols | `s.bytes()` only when ASCII/byte semantics are established |
| Use `Cow<str>` | When might modify borrowed data |
| Build strings deliberately | Choose `format!`, `write!`, push operations, or reuse from readability and allocation needs |
| Measure repeated search | Algorithm and preprocessing depend on pattern count and workload |

## Error Handling

| Rule | Guideline |
|------|-----------|
| Use `?` propagation | Not `try!()` macro |
| Document bug invariants | `expect()` only for a proven invariant; it is not universally preferred over `unwrap()` |
| Validate at the boundary | Choose errors, `assert!`, or `debug_assert!` from trust and failure policy |

## Memory

| Rule | Guideline |
|------|-----------|
| Lifetime names communicate relationships | Short conventional names are fine when the relationship is simple |
| Choose `borrow` or `try_borrow` from failure policy | Runtime borrow failure may be a bug or a recoverable condition |
| Shadowing for transformation | `let x = x.parse()?` |

## Concurrency

| Rule | Guideline |
|------|-----------|
| Identify lock ordering | Prevent deadlocks |
| Atomics for simple proven protocols | A primitive type alone does not make a lock unnecessary |
| Choose memory order carefully | Relaxed/Acquire/Release/SeqCst |

## Async

| Rule | Guideline |
|------|-----------|
| Keep CPU work off async executors | Use direct work, threads, a pool, or runtime blocking facilities from topology |
| Don't hold locks across await | Use scoped guards |

## Macros

| Rule | Guideline |
|------|-----------|
| Avoid unless necessary | Prefer functions/generics |
| Follow Rust syntax | Macro input should look like Rust |

## Deprecated → Better

| Deprecated | Better | Since |
|------------|--------|-------|
| `lazy_static!` | `std::sync::OnceLock` | 1.70 |
| `once_cell::Lazy` | `std::sync::LazyLock` | 1.80 |
| `std::sync::mpsc` | Select std, crossbeam, or runtime channels by topology/backpressure/dependency policy | context-dependent |
| `std::sync::Mutex` | Select std, parking_lot, async locks, or another protocol by poisoning/fairness/runtime needs | context-dependent |
| `failure`/`error-chain` | Migrate when needed; choose custom errors, thiserror, or anyhow by public contract and dependency policy | context-dependent |
| `try!()` | `?` operator | 2018 |

## Quick Reference

```
Naming: snake_case (fn/var), CamelCase (type), SCREAMING_CASE (const)
Format: rustfmt (just use it)
Docs: /// for public items, //! for module docs
Lint: preserve project policy; select additional lint groups deliberately
```

Claude knows Rust conventions well. These are the non-obvious Rust-specific rules.
