# Specialized Rust Ebpf Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Primary owner: `$rust-systems-networking`.
- Supporting profiles when needed: `$rust-observability`, `$rust-unsafe`, `$rust-performance`.
- Scope retained: Verifier constraints, bounded control flow, maps, XDP and probe attachment, no_std code, kernel/user ABI, and observability boundaries.
- Baseline correction: Retain verifier and ABI reasoning, but verify every Aya API against the exact resolved release. Version-sensitive Aya examples from the source are rejected rather than presented as current code.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

## eBPF vs Kernel Modules

| Property | eBPF | Kernel modules |
|-----|------|---------|
| Safety verification | Verified before loading | Requires manual review |
| Stability | Stable API | API may change |
| Performance | Just-in-time compiled | High, but with greater risk |
| Crash risk | Limited | May crash the kernel |
| Language support | C, Rust | C, Rust |


## Aya Library

> Rejected Specialized Rust Rust block `14108e656683`: Version-sensitive Aya API was rejected; keep verifier/no_std/map/ABI reasoning and research the exact resolved Aya release.


## eBPF Map

> Rejected Specialized Rust Rust block `cc751062d9a8`: Version-sensitive Aya API was rejected; keep verifier/no_std/map/ABI reasoning and research the exact resolved Aya release.


## XDP Programs

> Rejected Specialized Rust Rust block `4c9a1623b04f`: Version-sensitive Aya API was rejected; keep verifier/no_std/map/ABI reasoning and research the exact resolved Aya release.


## Tracepoint

> Rejected Specialized Rust Rust block `f57130e7ae0b`: Version-sensitive Aya API was rejected; keep verifier/no_std/map/ABI reasoning and research the exact resolved Aya release.


## kprobe/kretprobe

> Rejected Specialized Rust Rust block `1b6e5347e57b`: Version-sensitive Aya API was rejected; keep verifier/no_std/map/ABI reasoning and research the exact resolved Aya release.


## User-Space Loader

> Rejected Specialized Rust Rust block `615d263b4141`: Version-sensitive Aya API was rejected; keep verifier/no_std/map/ABI reasoning and research the exact resolved Aya release.


## Tail Call

> Rejected Specialized Rust Rust block `3b2b7265adb2`: Version-sensitive Aya API was rejected; keep verifier/no_std/map/ABI reasoning and research the exact resolved Aya release.


## Performance Optimization

| Optimization target | Method |
|-------|------|
| Map access | Read in batches to reduce system calls |
| Tail calls | Bound chain length and avoid excessive jumps |
| Data structures | Use arrays instead of hash tables |
| Lock contention | Use PerCPU maps |


## Related Skills

```
rust-ebpf
    │
    ├─► rust-embedded → no_std and kernel interfaces
    ├─► rust-performance → performance analysis
    └─► rust-unsafe → low-level memory operations
```
