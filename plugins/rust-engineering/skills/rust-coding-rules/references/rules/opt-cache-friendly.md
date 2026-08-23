# opt-cache-friendly

> Organize data for cache-efficient access patterns## Decision

Consider this rule only after its prerequisites are satisfied: Organize data for cache-efficient access patterns.

## Apply When

Apply when a reproducible profile or benchmark identifies a compiler, codegen, branch, cache, or target-specific bottleneck, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the workload, deployment target, or portability contract is unknown, or the expected benefit is speculative. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Hold toolchain, target, profile, features, inputs, and hardware constant; test one optimization hypothesis at a time.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

LTO, codegen, inlining, PGO, SIMD, and target tuning can trade build time, size, portability, debuggability, and determinism.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`bytes`) must already be accepted by the project or be approved before addition.
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Compare repeated release-like measurements and artifact or codegen evidence while preserving functional behavior and fallback targets.

## Why It Matters

Cache misses are expensive—a L3 cache miss costs ~100+ cycles vs ~4 cycles for L1 hit. Data layout and access patterns determine cache efficiency. Arrays of structs (AoS) vs structs of arrays (SoA), memory locality, and access patterns can make order-of-magnitude performance differences.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Array of Structs (AoS) - poor cache use when accessing one field
struct Particle {
    position: [f32; 3],  // 12 bytes
    velocity: [f32; 3],  // 12 bytes
    mass: f32,           // 4 bytes
    id: u64,             // 8 bytes
    flags: u8,           // 1 byte + padding
    // Total: 40 bytes per particle
}

fn update_positions(particles: &mut [Particle], dt: f32) {
    for p in particles {
        // Access position and velocity - 24 bytes
        // But loads 40-byte struct per particle
        // 16 bytes wasted per cache line load
        p.position[0] += p.velocity[0] * dt;
        p.position[1] += p.velocity[1] * dt;
        p.position[2] += p.velocity[2] * dt;
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Struct of Arrays (SoA) - cache-efficient for field access
struct Particles {
    positions_x: Vec<f32>,
    positions_y: Vec<f32>,
    positions_z: Vec<f32>,
    velocities_x: Vec<f32>,
    velocities_y: Vec<f32>,
    velocities_z: Vec<f32>,
    masses: Vec<f32>,
    ids: Vec<u64>,
    flags: Vec<u8>,
}

fn update_positions(p: &mut Particles, dt: f32) {
    // Access contiguous memory - perfect cache utilization
    for (px, vx) in p.positions_x.iter_mut().zip(&p.velocities_x) {
        *px += vx * dt;
    }
    for (py, vy) in p.positions_y.iter_mut().zip(&p.velocities_y) {
        *py += vy * dt;
    }
    for (pz, vz) in p.positions_z.iter_mut().zip(&p.velocities_z) {
        *pz += vz * dt;
    }
}
```

## Hot/Cold Splitting

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Hot/Cold Splitting illustration -->
```rust
// Separate frequently and rarely accessed fields
struct EntityHot {
    position: [f32; 3],
    velocity: [f32; 3],
    // Hot data - accessed every frame
}

struct EntityCold {
    name: String,
    creation_time: Instant,
    metadata: HashMap<String, Value>,
    // Cold data - rarely accessed
}

struct Entities {
    hot: Vec<EntityHot>,
    cold: Vec<EntityCold>,
}

// Hot loop touches only hot data
fn update(entities: &mut Entities, dt: f32) {
    for e in &mut entities.hot {
        e.position[0] += e.velocity[0] * dt;
        // Cold data stays out of cache
    }
}
```

## Prefetching

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Prefetching illustration -->
```rust
// Process in cache-line-sized chunks
const CACHE_LINE: usize = 64;

fn process_with_prefetch(data: &mut [u8]) {
    for chunk in data.chunks_mut(CACHE_LINE) {
        // Prefetch next chunk while processing current
        // (automatic in many cases, manual for complex patterns)
        process_chunk(chunk);
    }
}

// Matrix multiplication - block for cache
fn matmul_blocked(a: &[f64], b: &[f64], c: &mut [f64], n: usize) {
    const BLOCK: usize = 32;  // Fits in L1 cache
    
    for i0 in (0..n).step_by(BLOCK) {
        for j0 in (0..n).step_by(BLOCK) {
            for k0 in (0..n).step_by(BLOCK) {
                // Process BLOCK x BLOCK tile
                for i in i0..min(i0 + BLOCK, n) {
                    for j in j0..min(j0 + BLOCK, n) {
                        // Inner loop operates on cached data
                    }
                }
            }
        }
    }
}
```

## Avoid Pointer Chasing

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Avoid Pointer Chasing illustration -->
```rust
// Bad: linked list - random memory access
struct Node {
    value: i32,
    next: Option<Box<Node>>,
}

fn sum_linked(head: &Node) -> i32 {
    // Each node is a cache miss
}

// Good: contiguous vector
fn sum_vector(data: &[i32]) -> i32 {
    data.iter().sum()  // Sequential access, prefetcher happy
}

// Good: if graph needed, use indices
struct Graph {
    values: Vec<i32>,
    edges: Vec<usize>,  // Indices into values
}
```

## Memory Layout Attributes

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Memory Layout Attributes illustration -->
```rust
// Ensure cache-line alignment
#[repr(C, align(64))]
struct CacheAligned {
    data: [u8; 64],
}

// Prevent false sharing in concurrent code
#[repr(C, align(64))]
struct PaddedCounter {
    value: AtomicU64,
    _pad: [u8; 56],
}
```

## Measuring Cache Performance

```bash
# Linux perf
perf stat -e cache-references,cache-misses ./my_program

# Detailed cache analysis
perf stat -e L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses ./my_program

# Cachegrind
valgrind --tool=cachegrind ./my_program
```

## Related Rules
- [mem-smaller-integers](./mem-smaller-integers.md) - Smaller data fits more in cache
- [mem-box-large-variant](./mem-box-large-variant.md) - Keep enum sizes small
- [opt-bounds-check](./opt-bounds-check.md) - Sequential access patterns
