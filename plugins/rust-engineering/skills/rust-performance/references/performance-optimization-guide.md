# Rust Benchmarking and Optimization Guide

> Commands are conditional examples. Resolve versions and artifact paths from the project and use external tools only when already present or explicitly authorized.

## Criterion: Maintained Benchmark Default

Use Criterion when a benchmark will support regression tracking, baseline comparison, or an optimization claim.

At the workspace/package manifest that owns the bench target:

```toml
[dev-dependencies]
criterion = "<resolved-compatible-version>"

[[bench]]
name = "parse"
harness = false
```

Keep setup outside the timed section, identify input size, and report throughput when it has product meaning:

<!-- rust-example: fragment; missing: parse_in_place implementation, representative corpus, project Criterion version, and benchmark target -->
```rust
use criterion::{
    black_box, criterion_group, criterion_main, BatchSize, BenchmarkId, Criterion, Throughput,
};

fn parse_inputs(c: &mut Criterion) {
    let mut group = c.benchmark_group("parse");

    for size in [1_024_usize, 16_384, 262_144] {
        let source = representative_input(size);
        group.throughput(Throughput::Bytes(source.len() as u64));
        group.bench_with_input(BenchmarkId::from_parameter(size), &source, |b, source| {
            b.iter_batched_ref(
                || source.clone(),
                |input| black_box(parse_in_place(black_box(input))),
                BatchSize::SmallInput,
            );
        });
    }

    group.finish();
}

criterion_group!(benches, parse_inputs);
criterion_main!(benches);
```

Use `iter` when one immutable input can be shared. Use `iter_batched` or `iter_batched_ref` only when per-iteration mutable setup must be excluded; choose `SmallInput` by default and move to `LargeInput` when retained batches are too large. Avoid `PerIteration` unless a resource or input size makes batching impossible, because its measurement overhead is materially higher.

Record whether output destruction is part of the operation. Returning a value with `Drop` can include destruction in `iter`; select a timing loop deliberately rather than hiding the cost.

### Commands and Baselines

```text
cargo test --benches
cargo bench --bench parse -- --save-baseline <baseline>
cargo bench --bench parse -- --baseline <baseline>
cargo bench --profile profiling --bench parse -- --profile-time <seconds>
```

- `cargo test --benches` proves that bench targets start; it does not establish performance.
- Save and compare baselines only under the same toolchain, profile, target, features, flags, allocator, workload, and runner class.
- `--profile-time` repeats the selected benchmark without Criterion's normal analysis or result saving, so external or in-process profiler overhead is easier to isolate.
- When running a Criterion executable directly under a profiler, pass the Criterion-required `--bench` argument and use the resolved executable path rather than assuming Cargo's internal layout.

### Async Benchmarks

Use the same executor family and relevant configuration as production when executor behavior is part of the metric. Prefer a synchronous benchmark when measuring a synchronous operation; otherwise the runtime, wakeups, timers, and scheduling become part of the result. Record runtime version, worker count, current-thread versus multi-thread mode, and whether setup occurs outside the timed future.

## Divan: Minimal Exploratory Alternative

Use Divan when the goal is a small local benchmark with low ceremony and no established Criterion baseline or profiler hook contract.

```toml
[dev-dependencies]
divan = "<resolved-compatible-version>"

[[bench]]
name = "scan"
harness = false
```

<!-- rust-example: fragment; missing: scan implementation, representative inputs, and project Divan version -->
```rust
fn main() {
    divan::main();
}

#[divan::bench(args = [64_usize, 1_024, 16_384])]
fn scan(size: usize) -> usize {
    let input = representative_input(size);
    divan::black_box(scan_bytes(divan::black_box(&input)))
}
```

Divan output can guide exploration, but move to Criterion before making a durable regression or optimization claim that needs baseline management, Criterion's analysis contract, or `pprof-rs` Criterion integration. Resolve Divan's current MSRV before adoption.

## Benchmark Validity Checklist

- Representative success, boundary, adversarial, and size-scaling inputs are defined.
- Setup, cloning, allocation, I/O, and destruction are either intentionally timed or explicitly excluded.
- `black_box` protects inputs/outputs where optimization could erase the work.
- Throughput units match the actual work rather than an arbitrary byte count.
- Warmup, sample, measurement time, and significance settings stay at framework defaults unless noise evidence justifies a change.
- Baseline names, raw results, environment, and runner identity are retained.
- A service or concurrent result also has an end-to-end workload covering queueing, contention, I/O, and tail latency.

## Optimization Loop

1. Profile the representative workload using the [cross-platform profiling protocol](./low-level/rust-profiling.md).
2. Turn the dominant call path or resource cost into a focused Criterion benchmark when one does not exist.
3. State one hypothesis and the correctness behavior that must remain unchanged.
4. Apply the smallest candidate change.
5. Run functional verification and the same before/after benchmark.
6. Reject noise-level wins and record new memory, startup, build-time, portability, maintenance, or soundness costs.

No collection, allocator, parallel runtime, layout attribute, unsafe block, LTO setting, codegen-unit count, panic strategy, or stripping policy is a universal optimization. These are measured experiment variables owned by their respective profiles.

## Primary Evidence

- [Criterion book](https://bheisler.github.io/criterion.rs/book/)
- [Criterion input groups and throughput](https://bheisler.github.io/criterion.rs/book/user_guide/benchmarking_with_inputs.html)
- [Criterion timing loops](https://bheisler.github.io/criterion.rs/book/user_guide/timing_loops.html)
- [Criterion profiling mode](https://bheisler.github.io/criterion.rs/book/user_guide/profiling.html)
- [Divan documentation](https://docs.rs/divan/latest/divan/)
