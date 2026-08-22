# perf-ahash

> Use a faster hasher (`ahash` / `FxHashMap`) when DoS resistance is not needed

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-performance; supporters=`rust-stdlib`, `rust-cargo-build`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use a faster hasher (`ahash` / `FxHashMap`) when DoS resistance is not needed.

## Apply When

Apply when a controlled benchmark or profile identifies the operation and the proposed pattern preserves the correctness contract, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the change is based on source aesthetics, a synthetic non-representative workload, or an unapproved faster-but-weaker primitive. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Define metric and baseline, locate the bottleneck, test one pattern, compare repeated samples, and reject noise-level wins.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Lower runtime cost may increase code, dependency, memory, security, build-time, determinism, or maintenance cost.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`rustc-hash`, `ahash`) must already be accepted by the project or be approved before addition.
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Record exact workload, toolchain, target, features, profile, environment, before/after distributions, and functional equivalence.

## Why It Matters

Rust's default `HashMap` uses SipHash-1-3, which is DoS-resistant (hash flooding attacks on external input are not viable) but roughly 2–4× slower than non-cryptographic hashers on typical integer and short-string keys. For internal maps keyed by compiler-generated IDs, integer handles, or other trusted data, switching to a faster hasher can meaningfully reduce CPU time in hot map-heavy code. The wrong choice here is a security bug, not just a performance one — never use a non-DoS-resistant hasher for maps keyed by untrusted external input (user-supplied strings, network data, file paths from untrusted sources).

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use std::collections::HashMap;

// Using the default SipHash hasher for compiler-internal integer keys —
// DoS resistance is wasted cost here.
fn build_id_map(ids: &[(u32, String)]) -> HashMap<u32, String> {
    ids.iter().cloned().collect()
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// ahash: randomized seed per process, DoS-resistant, ~2x faster than SipHash.
// Good default replacement for most use cases.
use ahash::AHashMap;

fn build_id_map_ahash(ids: &[(u32, String)]) -> AHashMap<u32, String> {
    ids.iter().cloned().collect()
}

// FxHashMap (rustc-hash): fastest option, but uses a predictable hash function.
// Only for trusted integer or pointer keys where hash flooding is not a concern
// (e.g., compiler internals, in-process caches keyed by integer IDs).
use rustc_hash::FxHashMap;

type NodeMap<V> = FxHashMap<u32, V>;

fn build_node_map(nodes: &[(u32, String)]) -> NodeMap<String> {
    let mut map = NodeMap::with_capacity_and_hasher(
        nodes.len(),
        Default::default(),
    );
    map.extend(nodes.iter().cloned());
    map
}

// Convenient type aliases to avoid repeating the hasher parameter
use std::collections::HashMap;
use rustc_hash::FxBuildHasher;

type FastMap<K, V> = HashMap<K, V, FxBuildHasher>;

fn fast_map_example() -> FastMap<u32, u64> {
    FastMap::with_capacity_and_hasher(64, FxBuildHasher)
}
```

## Hasher Selection Guide

| Hasher | Crate | DoS-resistant | Speed | Use when |
|--------|-------|--------------|-------|----------|
| `SipHash-1-3` | std (default) | Yes | Baseline | Keys from untrusted external input |
| `ahash` | `ahash` | Yes (randomized) | ~2× faster | General-purpose replacement; safe default upgrade |
| `FxHash` | `rustc-hash` | No | Fastest | Trusted integer/pointer keys, compiler internals |
| `gxhash` | `gxhash` | Optional | Very fast (SIMD) | Throughput-critical, homogeneous key types |

## Key Points

- **Profile first**: switch hashers only after confirming map operations appear in profiler output.
- `ahash::AHashMap` is a drop-in replacement for `HashMap` and is the safest upgrade — it uses a random per-process seed.
- `FxHashMap` is what rustc uses internally; it is predictable, so never expose it to externally-supplied keys.
- Pass `with_capacity` when the final size is known — it applies regardless of hasher choice.

## Related Rules
- [perf-entry-api](perf-entry-api.md) - avoid redundant lookups with the entry API
- [perf-profile-first](perf-profile-first.md) - profile before optimizing
- [mem-with-capacity](mem-with-capacity.md) - pre-allocate collections when size is known
