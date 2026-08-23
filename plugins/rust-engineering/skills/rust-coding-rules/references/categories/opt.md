# Compiler Optimization

Prefix: `opt-` · 12 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than eight rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when a reproducible profile or benchmark identifies a compiler, codegen, branch, cache, or target-specific bottleneck.
- Defer when the workload, deployment target, or portability contract is unknown, or the expected benefit is speculative.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`opt-bounds-check`](../rules/opt-bounds-check.md) | `conditional` | `rust-performance` | Use iterators and patterns that eliminate bounds checks in hot paths |
| [`opt-cache-friendly`](../rules/opt-cache-friendly.md) | `conditional` | `rust-performance` | Organize data for cache-efficient access patterns |
| [`opt-codegen-units`](../rules/opt-codegen-units.md) | `conditional` | `rust-performance` | Set `codegen-units = 1` for maximum optimization in release builds |
| [`opt-cold-unlikely`](../rules/opt-cold-unlikely.md) | `conditional` | `rust-performance` | Mark unlikely code paths with `#[cold]` to help compiler optimization |
| [`opt-inline-always-rare`](../rules/opt-inline-always-rare.md) | `conditional` | `rust-performance` | Use `#[inline(always)]` sparingly—only for critical hot paths proven by profiling |
| [`opt-inline-never-cold`](../rules/opt-inline-never-cold.md) | `conditional` | `rust-performance` | Use `#[inline(never)]` and `#[cold]` for error paths and rarely-executed code |
| [`opt-inline-small`](../rules/opt-inline-small.md) | `conditional` | `rust-performance` | Use `#[inline]` for small hot functions |
| [`opt-likely-hint`](../rules/opt-likely-hint.md) | `conditional` | `rust-performance` | Use code structure to hint at likely branches; use intrinsics on nightly |
| [`opt-lto-release`](../rules/opt-lto-release.md) | `conditional` | `rust-performance` | Enable LTO in release builds |
| [`opt-pgo-profile`](../rules/opt-pgo-profile.md) | `conditional` | `rust-performance` | Use Profile-Guided Optimization (PGO) for maximum performance |
| [`opt-simd-portable`](../rules/opt-simd-portable.md) | `conditional` | `rust-performance` | Use portable SIMD for vectorized operations across architectures |
| [`opt-target-cpu`](../rules/opt-target-cpu.md) | `conditional` | `rust-performance` | Use `target-cpu=native` for maximum performance on known deployment targets |

## Batch Audit

For a broad audit, evaluate this category in batches of at most eight rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
