# Rust Performance Compatibility Guide

`rust-performance` remains the public entrypoint for older prompts and links. Its work is implemented through focused decision owners; it is not an additional layer of performance policy.

## Resolve the Task

| Need | Read |
|---|---|
| Benchmark validity, statistics, CPU/heap profiles, counters, timelines, build or size evidence | [Rust Profiling guide](../../rust-profiling/references/guide.md) |
| Change selection, preserved invariants, representation, algorithms and component trade-offs | [Rust Optimization guide](../../rust-optimization/references/guide.md) |
| Unexplained regression or wrong behavior | [Debugging guide](../../debugging/references/guide.md) |
| Unsafe validity and dynamic-tool coverage | [Unsafe guide](../../rust-unsafe/references/guide.md) |

Preserve the user's metric, workload, environment, raw artifacts and correctness contract across the handoff. Evidence about one isolated function does not establish a service or fleet result. If evidence is missing, obtain a discriminating observation rather than choosing a fashionable container, allocator, runtime or compiler setting.

## Retained Reference Map

The existing reference paths stay stable so downstream skills do not break. Their content identifies the actual decision owner:

- [Measurement decision map](performance-overview.md)
- [Benchmark implementation](performance-optimization-guide.md)
- [Specialized performance routing](performance.md)
- [CPU, heap and timeline tool matrix](low-level/rust-profiling.md)
- [Windows vendor and OS profilers](low-level/intel-vtune-amd-uprof.md)
- [PGO and BOLT](low-level/pgo.md)
- [Other hardware/tool families](low-level-index.md)

`rust-cargo-build` still owns effective Cargo profiles, target selection, flags and linker configuration. `rust-data` owns data architecture; `rust-concurrency` owns synchronization and cancellation; `rust-observability` owns span and metric semantics. Performance evidence supports their decisions without creating duplicate ownership.

## Compiling Example

The [golden fixture](../examples/golden/) is dependency-free and retains its original iterator/loop example. It also compares a safe prefix sum against a release-validated unchecked loop using wrapping arithmetic. Tests cover all valid prefixes, empty input, invalid and overflowing requested lengths, and fixed-length boxed storage whose elements remain mutable.

The example proves parity for the tested contract, not faster execution. Run it with `cargo test --manifest-path skills/rust-performance/examples/golden/Cargo.toml` from the plugin root. Optional Miri checks support the local safety proof; they do not establish a native speedup or cover arbitrary future changes.

## Completion Boundary

Record the resolved owner, hypothesis, comparable evidence, trade-offs and remaining gaps. The compatibility entrypoint must not occupy another `ProfileStack` role beside the selected profiling/optimization owner for the same decision. Keep experimental data local to the requested work; no new runtime dependency, tool installation, symbol download, GUI launch or trace upload is implied by routing.
