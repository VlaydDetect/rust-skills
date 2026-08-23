# Huiali Performance Protocol

> Product adaptation of `skills/rust-performance/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-performance`.
- Supporting profiles when needed: `$debugging`, `$rust-observability`.
- Scope retained: Baselines, profiling, allocation, cache behavior, batching, contention, latency distributions, throughput, and regression evidence.
- Baseline correction: Profile the actual target and workload before optimizing. Dependency swaps and unsafe code require measured benefit and explicit new costs.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## Optimization Priority

```
1. Algorithm choice      (10x - 1000x)   ← Biggest impact
2. Data structure        (2x - 10x)
3. Reduce allocations    (2x - 5x)
4. Cache optimization    (1.5x - 3x)
5. SIMD/parallelism      (2x - 8x)
```

**Warning**: Premature optimization is the root of all evil. Make it work first, then optimize hot paths.


## Solution Patterns

### Pattern 1: Pre-allocation

<!-- huiali-source: skills/rust-performance/SKILL.md#rust-block-1; sha256=8c3485e5e27f03aaf5ba61ce6b2e337aed0451214518f24296b570b8af72f415 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: grows dynamically
let mut vec = Vec::new();
for i in 0..1000 {
    vec.push(i);
}

// ✅ Good: pre-allocate known size
let mut vec = Vec::with_capacity(1000);
for i in 0..1000 {
    vec.push(i);
}
```

### Pattern 2: Avoid Unnecessary Clones

<!-- huiali-source: skills/rust-performance/SKILL.md#rust-block-2; sha256=6a26bdc9018046907349a234d967e5e4e8a102d1765c154f59f1d7e832b72179 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: unnecessary clone
fn process(item: &Item) {
    let data = item.data.clone();
    // use data...
}

// ✅ Good: use reference
fn process(item: &Item) {
    let data = &item.data;
    // use data...
}
```

### Pattern 3: Batch Operations

<!-- huiali-source: skills/rust-performance/SKILL.md#rust-block-3; sha256=5150da2a276463e13c9ffaecb0631139c0250610b491bf369aab4c9d6c46cc4a -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: multiple database calls
for user_id in user_ids {
    db.update(user_id, status)?;
}

// ✅ Good: batch update
db.update_all(user_ids, status)?;
```

### Pattern 4: Small Object Optimization

<!-- huiali-source: skills/rust-performance/SKILL.md#rust-block-4; sha256=787eb5c3eb23f13d387da863bfd6e22d1654c7c4e44bd390acc2c40fc0aae2e3 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use smallvec::SmallVec;

// ✅ No heap allocation for ≤16 items
let mut vec: SmallVec<[u8; 16]> = SmallVec::new();
```

### Pattern 5: Parallel Processing

<!-- huiali-source: skills/rust-performance/SKILL.md#rust-block-5; sha256=5baa523ba142f1ba2bbf0b6dc6d950ac93584082a9d263c08252c9e9f185b534 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use rayon::prelude::*;

let sum: i32 = data
    .par_iter()
    .map(|x| expensive_computation(x))
    .sum();
```


## Profiling Tools

| Tool | Purpose |
|------|---------|
| `cargo bench` | Criterion benchmarks |
| `perf` / `flamegraph` | CPU flame graphs |
| `heaptrack` | Allocation tracking |
| `valgrind --tool=cachegrind` | Cache analysis |
| `dhat` | Heap allocation profiling |


## Common Optimizations

### Anti-Patterns to Fix

| Anti-Pattern | Why Bad | Correct Approach |
|--------------|---------|------------------|
| Clone to avoid lifetimes | Performance cost | Proper ownership design |
| Box everything | Indirection overhead | Prefer stack allocation |
| HashMap for small data | Hash overhead too high | Vec + linear search |
| String concatenation in loop | O(n²) | `with_capacity` or `format!` |
| LinkedList | Cache-unfriendly | `Vec` or `VecDeque` |


## Advanced: False Sharing

### Symptom

<!-- huiali-source: skills/rust-performance/SKILL.md#rust-block-6; sha256=3b821c79f98bdd7478834202e675c3b954e6fe906b7f5b4033d1f72f959b6832 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Problem: multiple AtomicU64 in one struct
struct ShardCounters {
    inflight: AtomicU64,
    completed: AtomicU64,
}
```

- One CPU core at 90%+
- High LLC miss rate in perf
- Many atomic RMW operations
- Adding threads makes it slower

### Diagnosis

```bash
# Perf analysis
perf stat -d your_program
# Look for LLC-load-misses and locked-instrs

# Flamegraph
cargo flamegraph
# Find atomic fetch_add hotspots
```

### Solution: Cache Line Padding

<!-- huiali-source: skills/rust-performance/SKILL.md#rust-block-7; sha256=101ab862a0a4f3053e74c3e0e2cbef7da20fc1ad80c7a5d15339fcb8de069b07 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ Each field in separate cache line
#[repr(align(64))]
struct PaddedAtomicU64(AtomicU64);

struct ShardCounters {
    inflight: PaddedAtomicU64,
    completed: PaddedAtomicU64,
}
```


## Lock Contention Optimization

### Symptom

<!-- huiali-source: skills/rust-performance/SKILL.md#rust-block-8; sha256=3395a2cf9698266e2f8542819c61185a7143cdadfb4fcd934387b2eb1f57ce05 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ All threads compete for single lock
let shared: Arc<Mutex<HashMap<String, usize>>> =
    Arc::new(Mutex::new(HashMap::new()));
```

- Most time spent in mutex lock/unlock
- Performance degrades with more threads
- High system time percentage

### Solution: Thread-Local Sharding

<!-- huiali-source: skills/rust-performance/SKILL.md#rust-block-9; sha256=1999f74c65bd9b8e948bde5c95fba9278f3154637db2d4487d32a3c9130ba899 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ Each thread has local HashMap, merge at end
pub fn parallel_count(data: &[String], num_threads: usize)
    -> HashMap<String, usize>
{
    let mut handles = Vec::new();

    for chunk in data.chunks(data.len() / num_threads) {
        handles.push(thread::spawn(move || {
            let mut local = HashMap::new();
            for key in chunk {
                *local.entry(key.clone()).or_insert(0) += 1;
            }
            local  // Return local counts
        }));
    }

    // Merge all local results
    let mut result = HashMap::new();
    for handle in handles {
        for (k, v) in handle.join().unwrap() {
            *result.entry(k).or_insert(0) += v;
        }
    }
    result
}
```


## NUMA Awareness

### Problem

<!-- huiali-source: skills/rust-performance/SKILL.md#rust-block-10; sha256=2826d318541928de746abac18652dec90684eb0fb30d201d45aceaaea14c4f6d -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Multi-socket server, memory allocated on remote NUMA node
let pool = ArenaPool::new(num_threads);
// Rayon work-stealing causes tasks to run on any thread
// Cross-NUMA access causes severe memory migration latency
```

### Solution

<!-- huiali-source: skills/rust-performance/SKILL.md#rust-block-11; sha256=171fc2666a76b48494b9957edc88925dd454ba16930f2c6626899c49a055dedb -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 1. NUMA node binding
let numa_node = detect_numa_node();
let pool = NumaAwarePool::new(numa_node);

// 2. Use unified allocator (jemalloc)
#[global_allocator]
static ALLOC: jemallocator::Jemalloc = jemallocator::Jemalloc;

// 3. Avoid cross-NUMA object clones
// Borrow directly, don't copy data
```

### Tools

```bash
# Check NUMA topology
numactl --hardware

# Bind to NUMA node
numactl --cpunodebind=0 --membind=0 ./my_program
```


## Data Structure Selection

| Scenario | Choice | Reason |
|----------|--------|--------|
| High-concurrency writes | DashMap or sharding | Reduces lock contention |
| Read-heavy, few writes | RwLock<HashMap> | Read locks don't block |
| Small dataset | Vec + linear search | HashMap overhead higher |
| Fixed keys | Enum + array | Zero hash overhead |

### Read-Heavy Example

<!-- huiali-source: skills/rust-performance/SKILL.md#rust-block-12; sha256=2f850333b7d38a8ad941c16d3a4c386bc934bf29a9b2ea4b8a001ec91673a5b1 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ Many reads, few updates
struct Config {
    map: RwLock<HashMap<String, ConfigValue>>,
}

impl Config {
    pub fn get(&self, key: &str) -> Option<ConfigValue> {
        self.map.read().unwrap().get(key).cloned()
    }

    pub fn update(&self, key: String, value: ConfigValue) {
        self.map.write().unwrap().insert(key, value);
    }
}
```


## Common Performance Traps

| Trap | Symptom | Solution |
|------|---------|----------|
| Adjacent atomic variables | False sharing | `#[repr(align(64))]` |
| Global Mutex | Lock contention | Thread-local + merge |
| Cross-NUMA allocation | Memory migration | NUMA-aware allocation |
| Frequent small allocations | Allocator pressure | Object pooling |
| Dynamic string keys | Extra allocations | Use integer IDs |


## Review Checklist

When optimizing performance:

- [ ] Profiled to identify bottleneck
- [ ] Bottleneck confirmed with measurements
- [ ] Algorithm is optimal for use case
- [ ] Data structure appropriate
- [ ] Unnecessary allocations removed
- [ ] Parallelism exploited where beneficial
- [ ] Cache-friendly data layout
- [ ] Lock contention minimized
- [ ] Benchmarks show improvement
- [ ] Code still readable and maintainable


## Verification Commands

```bash
# Benchmark
cargo bench

# Profile with perf
perf stat -d ./target/release/your_program

# Generate flamegraph
cargo flamegraph --release

# Heap profiling
valgrind --tool=dhat ./target/release/your_program

# Cache analysis
valgrind --tool=cachegrind ./target/release/your_program

# NUMA topology
numactl --hardware
```


## Common Pitfalls

### 1. Premature Optimization

**Symptom**: Optimizing before profiling

**Fix**: Profile first, optimize hot paths only

### 2. Micro-optimizing Cold Paths

**Symptom**: Spending time on code that rarely runs

**Fix**: Focus on hot loops (90% of time in 10% of code)

### 3. Trading Readability for Minimal Gains

**Symptom**: Complex code for <5% improvement

**Fix**: Only optimize if gain is significant (>20%)


## Performance Diagnostic Workflow

```
1. Identify symptom (slow, high CPU, high memory)
   ↓
2. Profile with appropriate tool
   - CPU → perf/flamegraph
   - Memory → heaptrack/dhat
   - Cache → cachegrind
   ↓
3. Find hotspot (function/line)
   ↓
4. Understand why it's slow
   - Algorithm? Data structure? Allocation?
   ↓
5. Apply targeted optimization
   ↓
6. Benchmark to confirm improvement
   ↓
7. Repeat if not fast enough
```


## Related Skills

- **rust-concurrency** - Parallel processing patterns
- **rust-async** - Async performance optimization
- **rust-unsafe** - Zero-cost abstractions with unsafe
- **rust-coding** - Writing performant idiomatic code
- **rust-anti-pattern** - Performance anti-patterns to avoid

## Additional unique source examples

These code-only deltas appeared in the condensed English or localized source. They remain fragments, not dependency or hardware claims.

### `SKILL_ZH.md` example 1

<!-- huiali-source: skills/rust-performance/SKILL_ZH.md#rust-block-1; sha256=9e485f165b5a873352ff0cf75444735c477fc3d747a3976027cc69d2e403f191 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ 每次增长都分配
let mut vec = Vec::new();
for i in 0..1000 {
    vec.push(i);
}

// ✅ 预分配已知大小
let mut vec = Vec::with_capacity(1000);
for i in 0..1000 {
    vec.push(i);
}
```

### `SKILL_ZH.md` example 2

<!-- huiali-source: skills/rust-performance/SKILL_ZH.md#rust-block-2; sha256=2ab62483bfaeb974c4ea6e12d0e18ae406132b2d24a83e19945d05523023d214 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ 不必要的 clone
fn process(item: &Item) {
    let data = item.data.clone();
    // ...
}

// ✅ 使用引用
fn process(item: &Item) {
    let data = &item.data;
    // ...
}
```

### `SKILL_ZH.md` example 3

<!-- huiali-source: skills/rust-performance/SKILL_ZH.md#rust-block-3; sha256=0ccfbf0c30214377898497eff87c5235f3b1b1a60c472b529d67b3eaf5fbcad6 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ 多次数据库调用
for user_id in user_ids {
    db.update(user_id, status)?;
}

// ✅ 批量更新
db.update_all(user_ids, status)?;
```

### `SKILL_ZH.md` example 4

<!-- huiali-source: skills/rust-performance/SKILL_ZH.md#rust-block-4; sha256=20ffb703e9db7d79f3d6a7fd644da0f99da021a551cc2724d6a02431d32cd50e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 常用小集合用 SmallVec
use smallvec::SmallVec;
let mut vec: SmallVec<[u8; 16]> = SmallVec::new();
// 16 个以内不分配堆内存
```

### `SKILL_ZH.md` example 5

<!-- huiali-source: skills/rust-performance/SKILL_ZH.md#rust-block-5; sha256=4d31c222adb85712b3cca6b4307e02da29f3a7dddd6d07658a7cb6308c84e950 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use rayon::prelude::*;
let sum: i32 = data
    .par_iter()
    .map(|x| expensive(x))
    .sum();
```

### `SKILL_ZH.md` example 6

<!-- huiali-source: skills/rust-performance/SKILL_ZH.md#rust-block-6; sha256=e164237877b7ff978c3787ca1dd19851287f029a94fde590dc038c1182d4fee0 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 问题代码：多个 AtomicU64 挤在一个 struct 里
struct ShardCounters {
    inflight: AtomicU64,
    completed: AtomicU64,
}
```

### `SKILL_ZH.md` example 7

<!-- huiali-source: skills/rust-performance/SKILL_ZH.md#rust-block-7; sha256=e15df7117a4cac888ac1e530c33da48ea8d2273509ede8849047cf86cbacf10a -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 每个字段独立一个 cache line
#[repr(align(64))]
struct PaddedAtomicU64(AtomicU64);

struct ShardCounters {
    inflight: PaddedAtomicU64,
    completed: PaddedAtomicU64,
}
```

### `SKILL_ZH.md` example 8

<!-- huiali-source: skills/rust-performance/SKILL_ZH.md#rust-block-8; sha256=ec40b96d71b1a0da6c917b50537285dee5af13e61289183b1de991e79dc5f537 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Benchmark 对比
fn bench_naive() { /* 多个 AtomicU64 */ }
fn bench_padded() { /* 独立 cache line */ }
```

### `SKILL_ZH.md` example 9

<!-- huiali-source: skills/rust-performance/SKILL_ZH.md#rust-block-9; sha256=95c4414ea108c13f1b8b14a472b5bce58d337e3310937aac1075c5fee36f6734 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 全局共享 HashMap，所有线程竞争同一把锁
let shared: Arc<Mutex<HashMap<String, usize>>> = Arc::new(Mutex::new(HashMap::new()));
```

### `SKILL_ZH.md` example 10

<!-- huiali-source: skills/rust-performance/SKILL_ZH.md#rust-block-10; sha256=f3406c53566449708a5dc0d50cc6e249e5f3c9fa16e0ce1b85ca6db489c2780f -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 每个线程本地 HashMap，最后合并
pub fn parallel_count(data: &[String], num_threads: usize) -> HashMap<String, usize> {
    let mut handles = Vec::new();

    for chunk in data.chunks(/*...*/) {
        handles.push(thread::spawn(move || {
            let mut local = HashMap::new();
            for key in chunk {
                *local.entry(key).or_insert(0) += 1;
            }
            local  // 返回本地计数
        }));
    }

    // 合并所有本地结果
    let mut result = HashMap::new();
    for handle in handles {
        for (k, v) in handle.join().unwrap() {
            *result.entry(k).or_insert(0) += v;
        }
    }
    result
}
```

### `SKILL_ZH.md` example 11

<!-- huiali-source: skills/rust-performance/SKILL_ZH.md#rust-block-11; sha256=45bfa6f629f1b92fe65852a859ea0ce5afdae276b7a0235346c17a8fdebcb6b6 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 多 socket 服务器，内存分配在远端 NUMA node
let pool = ArenaPool::new(num_threads);
// Rayon work-stealing 让任务在任意线程执行
// 跨 NUMA 访问导致严重的内存迁移延迟
```

### `SKILL_ZH.md` example 12

<!-- huiali-source: skills/rust-performance/SKILL_ZH.md#rust-block-12; sha256=a76287501db0192ebbd885157fac0b287645cd4cdf5520107f2754cbd559776d -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 1. NUMA 节点绑定
let numa_node = detect_numa_node();
let pool = NumaAwarePool::new(numa_node);

// 2. 统一 allocator（jemalloc）
#[global_allocator]
static ALLOC: jemallocator::Jemalloc = jemallocator::Jemalloc;

// 3. 避免跨 NUMA 的对象 clone
// 直接借用，不做数据拷贝
```

### `SKILL_ZH.md` example 13

<!-- huiali-source: skills/rust-performance/SKILL_ZH.md#rust-block-13; sha256=362c34cf6b9da8c6e8b538e1812d76f6852e026e7a40e45041b32bb81c5bd53a -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 大量读取，少量更新
struct Config {
    map: RwLock<HashMap<String, ConfigValue>>,
}

impl Config {
    pub fn get(&self, key: &str) -> Option<ConfigValue> {
        self.map.read().get(key).cloned()
    }

    pub fn update(&self, key: String, value: ConfigValue) {
        self.map.write().insert(key, value);
    }
}
```
