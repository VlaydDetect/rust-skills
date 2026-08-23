# Specialized Rust Ebpf Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Primary owner: `$rust-systems-networking`.
- Supporting profiles when needed: `$rust-observability`, `$rust-unsafe`, `$rust-performance`.
- Scope retained: Verifier constraints, bounded control flow, maps, XDP and probe attachment, no_std code, kernel/user ABI, and observability boundaries.
- Baseline correction: Retain verifier and ABI reasoning, but verify every Aya API against the exact resolved release. Version-sensitive Aya examples from the source are rejected rather than presented as current code.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

## eBPF vs 内核模块

| 特性 | eBPF | 内核模块 |
|-----|------|---------|
| 安全验证 | 编译时验证 | 需要手动审查 |
| 稳定性 | 稳定的 API | API 可能变化 |
| 性能 | 即时 JIT | 高但有风险 |
| 崩溃风险 | 有限 | 可能崩溃内核 |
| 语言支持 | C, Rust | C, Rust |


## Aya 库

> Rejected Specialized Rust Rust block `14108e656683`: Version-sensitive Aya API was rejected; keep verifier/no_std/map/ABI reasoning and research the exact resolved Aya release.


## eBPF Map

> Rejected Specialized Rust Rust block `cc751062d9a8`: Version-sensitive Aya API was rejected; keep verifier/no_std/map/ABI reasoning and research the exact resolved Aya release.


## XDP 程序

> Rejected Specialized Rust Rust block `4c9a1623b04f`: Version-sensitive Aya API was rejected; keep verifier/no_std/map/ABI reasoning and research the exact resolved Aya release.


## Tracepoint

> Rejected Specialized Rust Rust block `f57130e7ae0b`: Version-sensitive Aya API was rejected; keep verifier/no_std/map/ABI reasoning and research the exact resolved Aya release.


## kprobe/kretprobe

> Rejected Specialized Rust Rust block `1b6e5347e57b`: Version-sensitive Aya API was rejected; keep verifier/no_std/map/ABI reasoning and research the exact resolved Aya release.


## 用户态加载器

> Rejected Specialized Rust Rust block `615d263b4141`: Version-sensitive Aya API was rejected; keep verifier/no_std/map/ABI reasoning and research the exact resolved Aya release.


## Tail Call

> Rejected Specialized Rust Rust block `3b2b7265adb2`: Version-sensitive Aya API was rejected; keep verifier/no_std/map/ABI reasoning and research the exact resolved Aya release.


## 性能优化

| 优化点 | 方法 |
|-------|------|
| Map 访问 | 批量读取，减少系统调用 |
| 尾调用 | 控制链长度，避免过多跳转 |
| 数据结构 | 使用数组而非哈希表 |
| 锁竞争 | 使用 PerCPU map |


## 与其他技能关联

```
rust-ebpf
    │
    ├─► rust-embedded → no_std, 内核接口
    ├─► rust-performance → 性能分析
    └─► rust-unsafe → 底层内存操作
```
