#!/usr/bin/env python3
"""Stage reviewed low-level source families and maintain their pinned ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from collections import Counter
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1]
REPOSITORY = PLUGIN.parents[1]
SOURCE = REPOSITORY / "references" / "low-level-dev-skills"
LEDGER = PLUGIN / "provenance" / "low-level-dev-coverage.json"
STAGING = PLUGIN / "provenance" / ".low-level-staging"
STATUSES = {"pending", "in_progress", "adapted", "merged", "duplicate", "excluded"}
BLOCK_STATUSES = {"pending", "retained", "corrected", "fragment", "rejected"}
FENCE = re.compile(r"^```([^\n`]*)\n(.*?)^```[ \t]*$", re.MULTILINE | re.DOTALL)
HEADING = re.compile(r"^#{2,4}\s+(.*)$", re.MULTILINE)


def family(
    owner: str,
    supporting: list[str],
    group: str,
    focus: str,
    correction: str,
    evidence: list[str],
) -> dict:
    return {
        "owner": owner,
        "supporting": supporting,
        "group": group,
        "focus": focus,
        "correction": correction,
        "evidence": evidence,
    }


FAMILY_CONFIG = {
    "cargo-workflows": family("rust-cargo-build", ["rust-dependencies", "rust-verify"], "cargo", "Workspace, feature, build-script, lockfile, cache, CI, and Cargo tool workflows.", "Resolver, build-script directive, external-tool, audit-policy, and lockfile behavior comes from the effective project and current Cargo/tool documentation; source defaults are not policy.", ["cargo-metadata", "cargo-config", "cargo-build-scripts", "cargo-resolver"]),
    "rust-async-internals": family("rust-concurrency", ["rust-pin", "debugging"], "concurrency", "Future polling, Waker replacement, task scheduling, pinning, cancellation, blocking boundaries, and async diagnostics.", "A Future may be polled repeatedly and must arrange a wake after returning Pending. Do not spawn work on every poll, assume a runtime, or treat stack pinning as inherently unsafe.", ["async-future", "async-pinning"]),
    "rust-build-times": family("rust-performance", ["rust-cargo-build", "rust-research"], "performance", "Clean and incremental build measurement, Cargo timings, invalidation, monomorphization, caching, codegen backends, and linking.", "Derive report and artifact locations from Cargo metadata. Cranelift, linker swaps, crate splitting, cache services, and profile changes are experiments, never universal speedups.", ["cargo-timings", "cargo-metadata", "cargo-build-cache", "cargo-build-performance", "cargo-unstable", "sccache-rust"]),
    "rust-cross": family("rust-cargo-build", ["rust-stable", "rust-unsafe-ffi"], "cargo", "Host/target separation, target support tiers, linker and runner configuration, native libraries, containers, emulators, and deployment validation.", "Installing a Rust target does not install a linker, sysroot, native libraries, emulator, or hardware. Resolve current target names and support guarantees instead of retaining a static catalog.", ["rustup-cross", "rustc-platform-support", "cargo-config", "cargo-build-cache"]),
    "rust-debugging": family("debugging", ["rust-cargo-build", "rust-observability"], "debug", "Debug-profile selection, Rust-aware GDB/LLDB, backtraces, panics, structured instrumentation, and async task inspection.", "Use the actual Cargo profile and artifact path. Panic symbol names, pretty printers, tracing stacks, and async consoles are toolchain- or dependency-specific leads, not defaults.", ["cargo-profiles", "cargo-metadata"]),
    "rust-ffi": family("rust-unsafe-ffi", ["rust-unsafe", "rust-cargo-build"], "ffi", "Manual and generated bindings, sys-crate layering, safe wrappers, exported C APIs, linking, ownership transfer, and error translation.", "Pointer non-null and length checks do not prove validity, alignment, initialization, lifetime, allocator pairing, or exclusivity. Verify the exact ABI and target.", ["rustc-codegen", "cargo-build-scripts"]),
    "rust-no-std": family("rust-architecture", ["rust-cargo-build", "rust-unsafe"], "architecture", "core/alloc/std capability boundaries, allocator and panic ownership, portable libraries, target configuration, and host-side testing.", "Do not infer absence of allocation, a panic strategy, allocator, HAL, executor, or target layout merely from no_std. Separate library portability from final binary runtime requirements.", ["rustc-platform-support", "cargo-config"]),
    "rust-profiling": family("rust-performance", ["debugging", "rust-cargo-build"], "performance", "Representative workload profiling, symbols, perf/flamegraphs, allocation analysis, Criterion, binary size, and monomorphization evidence.", "Do not install tools, change host security, assume artifact paths, or pin arbitrary dependency versions. A flamegraph selects a hypothesis; a comparable benchmark establishes improvement.", ["perf-record", "perf-security", "cargo-flamegraph", "criterion", "cargo-bloat", "cargo-llvm-lines"]),
    "rust-sanitizers-miri": family("rust-unsafe", ["rust-verify", "debugging"], "safety", "Miri and Rust sanitizer selection, execution scope, report interpretation, unsafe-code validation, and residual proof obligations.", "Rust does not expose an `undefined` sanitizer mode. Miri interprets concrete executions and neither Miri nor a sanitizer proves soundness across all inputs, targets, optimizations, FFI, or schedules.", ["rust-sanitizers", "miri"]),
    "rust-security": family("rust-architecture", ["rust-dependencies", "rust-unsafe"], "architecture", "Threat boundaries, dependency advisories and policy, FFI, fuzzing, unsafe validation, supply-chain inputs, and release hardening.", "Split security ownership across architecture, dependencies, unsafe/FFI, testing, and verification. Advisory and license policies are project decisions, not copied allow/deny lists.", ["cargo-audit", "cargo-deny", "miri", "rust-sanitizers"]),
    "rust-unsafe": family("rust-unsafe", ["rust-testing", "rust-verify"], "safety", "Unsafe operations, raw pointers, traits, safe wrappers, transmute, UnsafeCell, provenance, aliasing, initialization, and drop.", "Each operation needs a local proof of its exact preconditions. Tool success supports but never replaces the proof, and unsafe is not a default optimization technique.", ["miri", "rust-sanitizers"]),
    "rustc-basics": family("rust-cargo-build", ["rust-performance", "rust-research"], "cargo", "Cargo profiles, rustflags precedence, target inspection, MIR/LLVM/assembly evidence, monomorphization, size, and diagnostic triage.", "Do not apply target-cpu=native, target features, LTO, panic, stripping, UPX, or direct rustc invocations universally. Preserve Cargo context and verify the deployment target.", ["cargo-config", "cargo-profiles", "rustc-codegen", "cargo-build-cache"]),
    "concurrency-debugging": family("debugging", ["rust-concurrency", "rust-unsafe"], "debug", "Race, deadlock, lock-order, atomic-ordering, happens-before, and thread-state diagnosis.", "A race detector covers executed schedules and supported code. Combine a minimized reproducer with protocol invariants; do not transplant C/C++ atomic examples into Rust without proving the Rust model.", ["rust-sanitizers", "miri"]),
    "core-dumps": family("debugging", ["rust-cargo-build", "rust-verify"], "debug", "Core/minidump acquisition, build identity, symbols, debugger loading, thread triage, and missing-symbol recovery.", "Core generation paths, retention, privilege, systemd integration, and symbol servers are host policy. Never change them automatically; first locate an existing dump and matching binary.", ["cargo-build-cache"]),
    "debug-optimized-builds": family("debugging", ["rust-cargo-build", "rust-performance"], "debug", "Inlined frames, optimized-out values, line-table drift, scheduler locking, split debug information, and profile trade-offs.", "Optimized debugging is approximate: source order and variables may not survive. Rebuild only when authorized and keep the failing optimization-sensitive behavior reproducible.", ["cargo-profiles", "rustc-codegen"]),
    "dwarf-debug-format": family("debugging", ["rust-cargo-build", "rust-performance"], "debug", "DWARF sections and DIEs, line and unwind data, split DWARF, debuginfod, LTO interactions, stripping, and separate symbols.", "DWARF version, section names, split-debug layout, and tool support vary by target and linker. Match symbols by build identity instead of assumed filenames.", ["cargo-profiles", "rustc-codegen"]),
    "gdb": family("debugging", ["rust-cargo-build", "rust-verify"], "debug", "GDB startup, breakpoints, watchpoints, state and thread inspection, reverse and remote debugging, scripting, and common symbol failures.", "Use repository and toolchain-provided Rust helpers when present. Do not edit global gdbinit, start remote servers, or assume command support without user authorization and local evidence.", ["cargo-profiles"]),
    "lldb": family("debugging", ["rust-cargo-build", "rust-verify"], "debug", "LLDB startup, breakpoints, expressions, watchpoints, threads, Apple behavior, IDE integration, and scripting.", "LLDB command and Rust formatter availability depend on the installed distribution. Keep IDE and user-level configuration out of automatic workflows.", ["cargo-profiles"]),
    "flamegraphs": family("rust-performance", ["debugging", "rust-cargo-build"], "performance", "Sampling-stack capture, folded stacks, differential views, callgrind and alternate inputs, graph interpretation, and follow-up measurement.", "Box width is sample proportion, the x-axis is not time, and color is normally not semantic. Preserve raw samples and use a benchmark or counter comparison for the claimed win.", ["cargo-flamegraph", "perf-record", "perf-security"]),
    "hardware-counters": family("rust-performance", ["debugging", "rust-research"], "performance", "PMU event selection, perf stat/record, derived metrics, raw events, source attribution, PAPI/PCM, multiplexing, and counter limitations.", "Event names, availability, privilege, skid, multiplexing, and useful thresholds are CPU- and kernel-specific. Prefer ratios tied to a hypothesis, not universal threshold tables.", ["perf-record", "perf-security"]),
    "heaptrack": family("rust-performance", ["debugging", "rust-cargo-build"], "performance", "Allocation capture, symbol quality, retained versus peak memory, call-stack attribution, filtering, run comparison, and Rust allocator visibility.", "Verify that the selected allocator and workload are observable by the tool. Tool output paths and GUI availability are environment-specific.", ["cargo-profiles"]),
    "intel-vtune-amd-uprof": family("rust-performance", ["debugging", "rust-research"], "performance", "Vendor profiler selection, hotspots, microarchitecture, memory access, pipeline stalls, and roofline reasoning.", "Availability, permissions, event semantics, and hardware support are vendor/version-specific. Do not install drivers or claim portability from a different CPU.", ["rustc-codegen"]),
    "linux-perf": family("rust-performance", ["debugging", "rust-cargo-build"], "performance", "perf stat, sampling, reporting, annotation, live analysis, events, stack collection, and failure diagnosis.", "Select frame-pointer, DWARF, or LBR call graphs from the binary and CPU. perf_event_paranoid is a security boundary and must never be weakened automatically.", ["perf-record", "perf-security"]),
    "strace-ltrace": family("debugging", ["rust-observability", "rust-performance"], "debug", "System-call and dynamic-library tracing, filtering, errno diagnosis, timing, attachment, seccomp investigation, and bounded capture.", "Tracing can expose secrets, alter timing, require privilege, and generate large output. Scope PID, events, duration, and output handling before running.", ["perf-security"]),
    "valgrind": family("rust-performance", ["debugging", "rust-unsafe"], "performance", "Memcheck, leak categories, suppressions, Cachegrind, Callgrind, Massif, overhead, and native-code coverage.", "Valgrind support and semantics are target-specific and do not replace Miri or Rust sanitizers. Validate allocator, JIT, FFI, and optimized-code visibility.", ["miri", "rust-sanitizers"]),
    "build-acceleration": family("rust-performance", ["rust-cargo-build", "rust-research"], "performance", "Bottleneck diagnosis, compiler caches, distributed compilation, debug information, invalidation, hit-rate analysis, and cache correctness.", "For Rust, prefer the existing Cargo/sccache path. Cache credentials, remote backends, C/C++ PCH/unity, and distcc are conditional and never automatic product defaults.", ["cargo-build-performance", "cargo-build-cache", "sccache-rust"]),
    "linkers-lto": family("rust-cargo-build", ["rust-performance", "rust-unsafe-ffi"], "cargo", "Linker selection, argument ordering, LTO modes, dead-code elimination, visibility, map files, and link-failure diagnosis.", "Compiler driver, linker flavor, arguments, target ABI, native libraries, and current platform defaults must be observed. Change one measured variable and preserve symbol/debug requirements.", ["rustc-codegen", "cargo-profiles", "cargo-config"]),
    "elf-inspection": family("debugging", ["rust-unsafe-ffi", "rust-performance"], "debug", "ELF identity, sections, symbols, dynamic dependencies, disassembly, hardening properties, size, and build IDs.", "Do not use ldd on an untrusted binary. Tool output and section conventions are ELF-specific; dispatch Mach-O and PE artifacts to appropriate native tools.", ["rustc-codegen"]),
    "dynamic-linking": family("rust-cargo-build", ["rust-unsafe-ffi", "debugging"], "cargo", "Shared-library identity, SONAME, RPATH/RUNPATH, loader search, plugins, interposition, visibility, and loader errors.", "Loader order and path semantics are OS-specific and security-sensitive. Do not set global loader variables or assume a GNU layout for macOS or Windows.", ["rustc-codegen", "cargo-config"]),
    "binutils": family("debugging", ["rust-cargo-build", "rust-unsafe-ffi"], "debug", "Archive, strip, objcopy, address translation, demangling, strings, headers, disassembly, and cross-tool selection.", "Select tools by object format and target. Never strip or rewrite the only artifact; work from a copy and preserve build identity and separate symbols.", ["rustc-codegen"]),
    "pgo": family("rust-performance", ["rust-cargo-build", "rust-research"], "performance", "Instrumentation or sample profile collection, workload representativeness, profile merge/use, post-link optimization, and impact verification.", "Source commands are compiler-specific. Rust PGO and BOLT require current rustc/LLVM guidance, matching binaries, representative profiles, and before/after correctness and performance evidence.", ["rustc-codegen", "cargo-build-performance"]),
    "code-generation-and-backends": family("rust-performance", ["rust-cargo-build", "rust-research"], "performance", "Compiler pipeline, LLVM lowering, target triples, calling-convention lowering, backend selection, and new-target feasibility.", "LLVM utilities and target-backend authoring are not Cargo workflows. Cranelift and alternative backends remain toolchain- and target-gated experiments.", ["rustc-codegen", "cargo-unstable", "cargo-build-performance"]),
    "compiler-optimizations-deep": family("rust-performance", ["rust-cargo-build", "rust-research"], "performance", "Optimization pipeline, vectorization diagnostics, register pressure, loop transforms, PGO, BOLT, and generated-code evidence.", "Do not infer LLVM pass behavior or vectorization from source shape. Inspect the actual compiler output and benchmark the supported target.", ["rustc-codegen", "cargo-build-performance"]),
    "sanitizers": family("rust-unsafe", ["rust-verify", "rust-unsafe-ffi"], "safety", "ASan, TSan, MSan, hardware-assisted modes, suppression and report concepts, and native dependency instrumentation.", "The source is primarily C/C++. For Rust, use only modes and targets documented by rustc; reject UBSan-as-Rust instructions and do not combine flags by analogy.", ["rust-sanitizers"]),
    "fuzzing": family("rust-testing", ["rust-unsafe", "rust-verify"], "testing", "Target design, corpus, dictionary, crash reproduction, minimization, sanitizer composition, structure-aware inputs, and bounded CI campaigns.", "Use the project's existing fuzz harness and pinned tooling. Installation, long-running campaigns, corpus upload, OSS-Fuzz onboarding, and network actions require explicit authorization.", ["rust-sanitizers", "miri"]),
    "binary-hardening": family("rust-cargo-build", ["rust-architecture", "rust-unsafe-ffi"], "cargo", "Hardening-property inspection, compiler/linker mitigation families, control-flow integrity, platform mechanisms, and residual attack surface.", "Hardening flags depend on object format, linker, target, runtime, deployment, and threat model. Verify the final artifact; never copy C flags into rustflags without rustc/linker evidence.", ["rustc-codegen", "cargo-config"]),
    "abi-and-calling-conventions": family("rust-unsafe-ffi", ["rust-cargo-build", "rust-unsafe"], "ffi", "System V, AAPCS, RISC-V, stack frames, registers, variadics, unwind, and compiler-output verification.", "Calling conventions are target ABI contracts, not architecture-only folklore. Confirm target triple, data layout, symbol ABI, variadic rules, unwind, and foreign compiler settings.", ["rustc-codegen", "rustc-platform-support"]),
    "memory-hierarchy-and-caches": family("rust-performance", ["rust-architecture", "rust-research"], "performance", "Cache hierarchy, lines, associativity, coherence, false sharing, locality, prefetching, and measurement.", "Cache sizes, line widths, topology, and penalties are hardware facts. Treat common numbers as examples and query or measure the deployment CPU.", ["perf-record"]),
    "cpu-pipelines-and-hazards": family("rust-performance", ["debugging", "rust-research"], "performance", "Pipeline dependencies, control and structural hazards, execution ports, instruction-level parallelism, and uop evidence.", "Classic pipelines are mental models, not a description of a modern CPU. Use target-specific counters and assembly before changing code.", ["perf-record", "rustc-codegen"]),
    "branch-prediction-and-speculation": family("rust-performance", ["rust-architecture", "rust-research"], "performance", "Predictability, branch layout, misprediction measurement, speculation, and side-channel constraints.", "Compiler hints and branchless rewrites are conditional. Security-sensitive constant-time behavior and runtime performance require separate, target-specific evidence.", ["perf-record", "rustc-codegen"]),
    "virtual-memory-paging-and-tlb": family("rust-performance", ["rust-architecture", "rust-research"], "performance", "Page translation, faults, TLB pressure, huge pages, mapping evidence, and embedded contrasts.", "Page-table shape, page size, huge-page policy, counters, and kernel interfaces are target/OS facts. Do not request huge pages or host configuration automatically.", ["perf-record", "perf-security"]),
    "memory-model": family("rust-concurrency", ["rust-unsafe", "rust-research"], "concurrency", "Atomic ordering, happens-before, release sequences, fences, publication, lock-free state machines, and common ordering failures.", "C++ examples are comparative evidence, not Rust proof. Write the Rust state machine and justify each ordering with the Rust memory model and primitive documentation.", ["miri"]),
    "cpu-cache-opt": family("rust-performance", ["rust-architecture", "rust-research"], "performance", "Counter-led cache diagnosis, data layout, traversal, false sharing, prefetch, blocking, and cache-aware algorithm choices.", "AoS/SoA, padding, prefetch, and blocking are workload- and hardware-dependent. Preserve semantics and compare representative measurements.", ["perf-record"]),
    "simd-intrinsics": family("rust-performance", ["rust-unsafe", "rust-stable"], "performance", "Auto-vectorization, runtime feature detection, x86 and ARM intrinsics, alignment, dispatch, scalar fallbacks, and generated assembly.", "Intrinsics require supported target features and local unsafe proofs. Never compile a baseline binary for target-cpu=native when it must run on different CPUs.", ["rustc-codegen", "rustc-platform-support"]),
    "custom-allocators": family("rust-unsafe", ["rust-performance", "rust-architecture"], "safety", "Pool, arena, global and system allocators, ownership, alignment, fragmentation, concurrency, teardown, and benchmarking.", "Do not adopt an allocator from generic benchmark claims. Prove layout and deallocation invariants, workload fit, OOM behavior, observability, and platform support.", ["miri", "rust-sanitizers"]),
    "numa-programming": family("rust-performance", ["rust-architecture", "rust-research"], "performance", "Topology discovery, memory placement, affinity, first touch, remote-access diagnosis, measurement, and fallback behavior.", "NUMA topology, container visibility, cpusets, allocator policy, and privilege are deployment facts. Never hard-code nodes or cores from source examples.", ["perf-record", "perf-security"]),
    "io-uring": family("rust-concurrency", ["rust-unsafe-ffi", "rust-performance"], "concurrency", "Submission/completion ownership, operation lifetimes, registered resources, multishot operations, cancellation, zero-copy, and fallback I/O.", "Kernel version, opcode support, library/runtime API, security restrictions, and buffer lifetime must be verified. Never retain a buffer until only submission rather than completion.", ["rustc-platform-support"]),
    "af-xdp": family("rust-systems-networking", ["rust-unsafe", "rust-performance"], "systems", "UMEM ownership, fill/completion and RX/TX rings, XDP redirect, copy/zero-copy modes, queue binding, and packet lifecycle.", "Kernel, libbpf/binding, NIC, driver, queue, privilege, and zero-copy support are required evidence. Preserve a bounded owner transition for every frame.", ["rustc-platform-support", "perf-record"]),
    "dpdk": family("rust-systems-networking", ["rust-unsafe", "rust-performance"], "systems", "EAL, huge pages, PMDs, mempools/mbufs, RX/TX bursts, rings, RSS, NUMA, affinity, and pipeline topology.", "Merge only concepts not already owned by the Huiali protocol. Binding APIs, device arguments, huge pages, queue counts, and core maps are target-specific and require exact evidence.", ["rustc-platform-support", "perf-record"]),
    "ebpf-rust": family("rust-systems-networking", ["rust-unsafe", "rust-observability"], "systems", "Kernel/user split, verifier constraints, program and map types, BTF/CO-RE, attachment, event transport, and load-failure diagnosis.", "Merge verifier and ABI concepts only. Aya APIs and kernel bindings must be checked against the resolved crate and target kernel; no source snippet is current by default.", ["rustc-platform-support"]),
    "embedded-rust": family("rust-architecture", ["rust-cargo-build", "rust-unsafe"], "architecture", "Target and memory layout, no_std entry/panic, flashing/debugging, compact telemetry, interrupts, concurrency models, and HAL ownership.", "MCU, target, linker script, HAL/runtime versions, probe, panic path, clock and memory budget are required evidence. Do not install targets or tools automatically.", ["rustup-cross", "rustc-platform-support", "cargo-config"]),
    "linker-scripts": family("rust-cargo-build", ["rust-architecture", "rust-unsafe-ffi"], "cargo", "Memory regions, sections, VMA/LMA, startup initialization, placement, KEEP/ALIGN/PROVIDE, symbols, and map-based verification.", "A linker script is target firmware policy. Verify the selected linker grammar, memory map, startup code, retained sections, alignment, stack/heap boundaries, and final map file.", ["rustc-codegen", "cargo-config"]),
}

FAMILY_ORDER = list(FAMILY_CONFIG)


EVIDENCE = {
    "cargo-timings": ("official-rust", "stable", "Cargo timings output and interpretation", "https://doc.rust-lang.org/stable/cargo/reference/timings.html"),
    "cargo-build-cache": ("official-rust", "stable", "Cargo target/build directories and artifact layout", "https://doc.rust-lang.org/cargo/reference/build-cache.html"),
    "cargo-metadata": ("official-rust", "stable-format-v1", "Machine-readable workspace, target directory, and resolved packages", "https://doc.rust-lang.org/nightly/cargo/commands/cargo-metadata.html"),
    "cargo-config": ("official-rust", "stable", "Cargo configuration hierarchy, target linker/runner, wrappers, and rustflags", "https://doc.rust-lang.org/cargo/reference/config.html"),
    "cargo-build-scripts": ("official-rust", "stable", "Build-script inputs, outputs, directives, and host/target behavior", "https://doc.rust-lang.org/cargo/reference/build-scripts.html"),
    "cargo-resolver": ("official-rust", "stable", "Dependency and feature resolution", "https://doc.rust-lang.org/cargo/reference/resolver.html"),
    "cargo-profiles": ("official-rust", "stable", "Cargo profile keys and inheritance", "https://doc.rust-lang.org/cargo/reference/profiles.html"),
    "cargo-build-performance": ("official-rust", "stable", "Measured Rust build-performance guidance", "https://doc.rust-lang.org/cargo/guide/build-performance.html"),
    "cargo-unstable": ("official-rust", "nightly", "Cargo unstable feature gates including codegen backends", "https://doc.rust-lang.org/cargo/reference/unstable.html"),
    "rustc-codegen": ("official-rust", "toolchain-specific", "rustc code-generation options", "https://doc.rust-lang.org/rustc/codegen-options/index.html"),
    "rust-sanitizers": ("official-rust", "nightly-target-specific", "Supported rustc sanitizer modes and target matrix", "https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html"),
    "miri": ("official-tool-owner", "nightly-version-sensitive", "Miri setup, coverage, limitations, and flags", "https://github.com/rust-lang/miri/"),
    "rustup-cross": ("official-rust", "current-rustup", "rustup cross-compilation responsibilities", "https://rust-lang.github.io/rustup/cross-compilation.html"),
    "rustc-platform-support": ("official-rust", "current-beta", "Rust target support tiers and target-specific notes", "https://doc.rust-lang.org/beta/rustc/platform-support.html"),
    "async-future": ("official-rust", "current", "Future poll and wake contract", "https://rust-lang.github.io/async-book/02_execution/02_future.html"),
    "async-pinning": ("official-rust", "current", "Pinning and async state-machine constraints", "https://rust-lang.github.io/async-book/part-reference/pinning.html"),
    "perf-record": ("official-tool-doc-mirror", "installed-perf-specific", "perf record events and call-graph modes", "https://man7.org/linux/man-pages/man1/perf-record.1.html"),
    "perf-security": ("official-linux-kernel", "kernel-specific", "perf privilege and data-exposure boundary", "https://docs.kernel.org/admin-guide/perf-security.html"),
    "cargo-flamegraph": ("tool-owner", "resolved-version", "cargo-flamegraph backends and command surface", "https://github.com/flamegraph-rs/flamegraph"),
    "criterion": ("tool-owner", "resolved-version", "Criterion benchmark methodology and APIs", "https://bheisler.github.io/criterion.rs/book/"),
    "cargo-bloat": ("tool-owner", "resolved-version", "cargo-bloat formats and attribution limits", "https://github.com/RazrFalcon/cargo-bloat"),
    "cargo-llvm-lines": ("tool-owner", "resolved-version", "Unoptimized LLVM IR line-count semantics", "https://github.com/dtolnay/cargo-llvm-lines"),
    "sccache-rust": ("tool-owner", "resolved-version", "Rust compiler-wrapper caching and limitations", "https://github.com/mozilla/sccache/blob/main/docs/Rust.md"),
    "cargo-audit": ("tool-owner", "resolved-version", "RustSec advisory scanning", "https://github.com/rustsec/rustsec/blob/main/cargo-audit/README.md"),
    "cargo-deny": ("tool-owner", "resolved-version", "Dependency license, advisory, source, and ban policy", "https://github.com/EmbarkStudios/cargo-deny"),
}


GROUP_PROTOCOLS = {
    "cargo": {
        "context": ["workspace root and selected package", "rust-toolchain/MSRV/Edition", "effective Cargo configuration", "host and target triples", "profile, features, lockfile policy, and native inputs"],
        "steps": ["Resolve effective state with repository files and cargo metadata before proposing flags.", "Separate host tools/build scripts/proc macros from target artifacts and runtime dependencies.", "State the exact artifact or behavior being changed and derive paths from Cargo output, not folklore.", "Change the owning manifest/config once; keep environment-only experiments local and reversible.", "Validate the affected package/target/profile matrix and review lockfile or artifact changes separately."],
        "pitfalls": ["Static target, linker, runner, and artifact-path catalogs drift.", "RUSTFLAGS can affect host invocations unless an explicit --target separates them.", "A faster link or smaller binary is not automatically a valid deployment artifact."],
    },
    "debug": {
        "context": ["exact failing command and environment", "matching executable, target and profile", "build ID and symbols", "input and process/thread state", "debugger/tracer version and privilege boundary"],
        "steps": ["Reproduce and preserve the original failure before changing build settings.", "Identify object format, optimization and symbol availability; match external symbols by build identity.", "Choose the narrowest observation: backtrace, breakpoint/watchpoint, core, syscall trace, or thread snapshot.", "Form one falsifiable hypothesis and collect only the state that distinguishes it.", "Record debugger limitations caused by inlining, optimization, missing frames, unsupported format, or timing perturbation."],
        "pitfalls": ["Debuggers can evaluate code and change process state.", "Optimized source lines and variables are not a faithful execution transcript.", "Tracing, cores and memory inspection may expose secrets."],
    },
    "performance": {
        "context": ["metric and correctness contract", "representative workload and data", "target/profile/features/toolchain", "hardware, kernel and load controls", "baseline distribution and retained raw evidence"],
        "steps": ["Classify CPU, allocation, I/O, contention, binary-size, or build-time cost before choosing a tool.", "Capture a comparable baseline and preserve raw samples, counters, reports, or build timings.", "Use one profiler or counter set to locate a bottleneck; treat attribution as a hypothesis with tool limitations.", "Change one variable and rerun the same workload and correctness checks.", "Reject noise-level wins and report unmeasured targets, cold/warm state, tail behavior, and new complexity."],
        "pitfalls": ["Flamegraph width is sample proportion, not an optimization measurement.", "Hardware events and thresholds are CPU/kernel-specific.", "Compile-time, binary-size and runtime improvements can trade against one another."],
    },
    "safety": {
        "context": ["unsafe operation and safe caller contract", "target and toolchain", "executed input/schedule", "FFI/native coverage", "remaining manual invariants"],
        "steps": ["Write provenance, alignment, initialization, validity, aliasing, lifetime, layout, thread, panic and drop obligations.", "Select Miri for supported MIR execution or a documented rustc sanitizer for a supported target and failure class.", "Use the repository-pinned nightly when present; otherwise report the required evidence as unavailable instead of installing.", "Minimize the reproducer and interpret the first causally relevant diagnostic.", "Record what the run did not cover and keep the local safety proof authoritative."],
        "pitfalls": ["Miri explores concrete executions, not all inputs or schedules.", "Sanitizer support is mode- and target-specific and normally nightly.", "C/C++ UBSan recipes are not a Rust sanitizer mode."],
    },
    "concurrency": {
        "context": ["state owner and task/thread topology", "wake or notification edges", "queue and resource bounds", "cancellation and shutdown", "ordering and memory-model invariants"],
        "steps": ["Draw the state machine, ownership transfers, suspension/completion points, and failure paths.", "For Future code, pair every Pending result with a path that can wake the latest Waker.", "Keep buffers, permits and operations alive until the documented completion/cancellation point.", "Bound work, queues, retries and spawned tasks; define who closes, drains and joins.", "Use schedule/race tools only after the invariant and minimized reproducer are explicit."],
        "pitfalls": ["A wake is a request to poll, not proof that progress occurred.", "Cancellation may occur at every suspension point.", "Lock-free code requires a state-machine and ordering proof, not only passing stress tests."],
    },
    "ffi": {
        "context": ["target ABI and object format", "type layout and calling convention", "ownership/allocator pairing", "pointer validity and lifetimes", "panic/unwind, callbacks and thread rules"],
        "steps": ["Write the foreign contract independently of Rust syntax and identify each allocation and destruction owner.", "Represent ABI-safe values and opaque handles; validate all lengths, alignments, encodings and nullability.", "Keep raw declarations separate from the safe wrapper and expose unsafe obligations only where callers can satisfy them.", "Contain panics/unwind and translate errors without borrowing temporary foreign storage.", "Verify symbols/layout with the actual target toolchain and at least one real foreign consumer."],
        "pitfalls": ["repr(C) does not prove semantic compatibility.", "A non-null pointer may still be invalid, unaligned, stale or aliased.", "Foreign allocators and callbacks carry independent lifecycle/thread contracts."],
    },
    "architecture": {
        "context": ["deployment and trust boundary", "target capabilities", "resource and failure budget", "external effects and supply inputs", "required portability and maintenance policy"],
        "steps": ["Start from the threat, resource, platform or portability constraint rather than a named tool.", "Separate domain policy from build, target, telemetry, security and hardware adapters.", "Identify unavailable std/platform capabilities and assign explicit owners for allocation, panic, time, I/O and cleanup.", "Route dependency policy, unsafe proof, fuzzing and artifact hardening to their existing owners.", "Prove one target-specific vertical slice and document what host-only evidence cannot establish."],
        "pitfalls": ["no_std does not imply no allocation or bare metal.", "A copied security allow/deny list is not a threat model.", "Hardware and deployment assumptions must remain configurable and evidenced."],
    },
    "testing": {
        "context": ["input boundary and invariant", "existing harness and engine version", "corpus/dictionary/seeds", "time and resource budget", "crash artifact handling"],
        "steps": ["Choose a narrow target that converts bytes into a meaningful operation without hiding panics or hangs.", "Seed valid structure, preserve and minimize crashes, and add each confirmed defect as a deterministic regression.", "Compose sanitizers only where the current Rust/target documentation permits it.", "Bound campaign time, memory, artifact retention and CI scope.", "Treat coverage growth as guidance; assert the actual safety or behavior contract separately."],
        "pitfalls": ["Random input without invariants produces weak signal.", "Fuzz engines, flags and corpus formats are version-specific.", "Long-running or uploaded campaigns require explicit authorization."],
    },
    "systems": {
        "context": ["kernel/NIC/driver/CPU/NUMA", "privileges and deployment", "resolved binding/library version", "queue/ring/buffer topology", "overload, shutdown and cleanup"],
        "steps": ["Select the kernel-verifier, AF_XDP, or DPDK execution model before applying rules.", "Draw every buffer/frame/map/event ownership transition through receive, queue, drop, transmit and detach.", "Record ring capacities, queue/core placement, batching and backpressure/drop behavior.", "Prove FFI layout, alignment, lifetime and thread-affinity at the binding boundary.", "Measure on the real target; classify host-only or hardware-free examples as fragments."],
        "pitfalls": ["Zero-copy still has ownership, synchronization and cleanup transitions.", "Queue/core/NUMA constants are not portable.", "Crate compilation does not prove verifier, driver or device acceptance."],
    },
}


WRONG_COMMAND = re.compile(
    r"-Z\s*sanitizer\s*=\s*undefined|build/cargo-timings|cargo\s+tree\s+--graph|"
    r"wasm32-wasi\b|/zld\b|:[ ]*main\b",
    re.IGNORECASE,
)
SIDE_EFFECT_COMMAND = re.compile(
    r"\bcargo\s+(?:install|update|upgrade|fetch)\b|\brustup\s+(?:toolchain\s+install|component\s+add|target\s+add)\b|"
    r"\b(?:sudo|apt-get|apt\s+install|brew\s+install|dnf\s+install|pacman|curl|wget|git\s+clone|sysctl)\b|"
    r"perf_event_paranoid|AWS_SECRET_ACCESS_KEY|AWS_ACCESS_KEY_ID",
    re.IGNORECASE,
)
COMMAND_LANGUAGES = {"bash", "cmd", "cmake", "console", "dockerfile", "gdb", "lldb", "powershell", "sh", "shell", "zsh"}
TOOL_PATTERNS = {
    "cargo": r"\bcargo\b",
    "rustc": r"\brustc\b",
    "rustup": r"\brustup\b",
    "miri": r"\bmiri\b",
    "perf": r"\bperf\b",
    "cargo-flamegraph": r"\bcargo(?:-|\s+)flamegraph\b",
    "cargo-bloat": r"\bcargo(?:-|\s+)bloat\b",
    "cargo-llvm-lines": r"\bcargo(?:-|\s+)llvm-lines\b",
    "criterion": r"\bcriterion\b",
    "sccache": r"\bsccache\b",
    "gdb": r"\b(?:rust-)?gdb\b",
    "lldb": r"\b(?:rust-)?lldb\b",
    "strace": r"\bstrace\b",
    "ltrace": r"\bltrace\b",
    "valgrind": r"\bvalgrind\b",
    "heaptrack": r"\bheaptrack\b",
    "readelf": r"\breadelf\b",
    "objdump": r"\bobjdump\b",
    "nm": r"(?:^|\s)nm(?:\s|$)",
    "ldd": r"\bldd\b",
    "cmake": r"\bcmake\b",
    "make": r"(?:^|\s)make(?:\s|$)",
    "ninja": r"\bninja\b",
    "cross": r"\bcross\b",
    "docker": r"\bdocker\b",
    "sysctl": r"\bsysctl\b",
    "curl": r"\bcurl\b",
    "wget": r"\bwget\b",
    "git": r"\bgit\b",
    "apt": r"\b(?:apt|apt-get)\b",
    "brew": r"\bbrew\b",
    "dnf": r"\bdnf\b",
    "pacman": r"\bpacman\b",
    "addr2line": r"\baddr2line\b",
}


def source_files() -> list[Path]:
    return sorted(
        path
        for path in SOURCE.rglob("*")
        if path.is_file()
        and ".git" not in path.relative_to(SOURCE).parts
        and "graphify-out" not in path.relative_to(SOURCE).parts
    )


def skill_roots() -> dict[str, Path]:
    roots: dict[str, Path] = {}
    for path in (SOURCE / "skills").rglob("SKILL.md"):
        name = path.parent.name
        if name in FAMILY_CONFIG:
            if name in roots:
                raise AssertionError(f"duplicate source family: {name}")
            roots[name] = path.parent
    if set(roots) != set(FAMILY_CONFIG):
        raise AssertionError(f"source family mismatch: {sorted(set(roots) ^ set(FAMILY_CONFIG))}")
    return roots


def family_markdown(name: str) -> list[Path]:
    return sorted(skill_roots()[name].rglob("*.md"))


def selected_markdown() -> list[Path]:
    return sorted({path for name in FAMILY_ORDER for path in family_markdown(name)})


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_count(path: Path) -> int | None:
    try:
        return len(path.read_text(encoding="utf-8").splitlines())
    except UnicodeDecodeError:
        return None


def normalize_block(body: str) -> str:
    return body.replace("\r\n", "\n").rstrip()


def block_digest(body: str) -> str:
    return hashlib.sha256(normalize_block(body).encode()).hexdigest()


def command_tools(body: str) -> list[str]:
    return sorted(name for name, pattern in TOOL_PATTERNS.items() if re.search(pattern, body, re.IGNORECASE | re.MULTILINE))


def command_contract(body: str, language: str, config: dict, status: str, evidence_ids: list[str]) -> dict | None:
    tools = command_tools(body)
    if language not in COMMAND_LANGUAGES and not tools:
        return None

    resolved_tools = tools or [language]
    nightly = bool(re.search(r"(?:^|\s)(?:\+nightly|-Z\b)|\bcargo\s+miri\b", body, re.IGNORECASE))
    core_tools = {"cargo", "rustc", "rustup"}
    channel = "nightly" if nightly else ("external" if set(resolved_tools) - core_tools else "stable")
    version = {
        "nightly": "project-pinned nightly; exact flag support rechecked",
        "external": "already-installed or project-resolved tool version",
        "stable": "project-selected Rust/Cargo toolchain",
    }[channel]

    effects: set[str] = set()
    if re.search(r"\bcargo\s+install\b|\b(?:apt|apt-get|brew|dnf|pacman)\b", body, re.IGNORECASE):
        effects.add("install")
    if re.search(r"\b(?:curl|wget|git\s+clone)\b|\bcargo\s+(?:install|update|fetch)\b|\brustup\s+(?:toolchain\s+install|component\s+add|target\s+add)\b", body, re.IGNORECASE):
        effects.add("network")
    if re.search(r"\brustup\s+(?:toolchain\s+install|component\s+add|target\s+add)\b", body, re.IGNORECASE):
        effects.update({"install", "toolchain-mutation"})
    if re.search(r"\bcargo\s+update\b", body, re.IGNORECASE):
        effects.add("lockfile-mutation")
    if re.search(r"\bsudo\b", body, re.IGNORECASE):
        effects.add("privilege")
    if re.search(r"\bsysctl\b|perf_event_paranoid", body, re.IGNORECASE):
        effects.add("global-host-config")
    if re.search(r"\bcargo\s+(?:build|check|test|run|bench)\b|\brustc\b|\b(?:cmake|make|ninja)\b", body, re.IGNORECASE):
        effects.add("build-artifacts")
    if set(tools) & {"perf", "cargo-flamegraph", "cargo-bloat", "cargo-llvm-lines", "criterion", "valgrind", "heaptrack"}:
        effects.add("profiler-output")
    if not effects:
        effects.add("read-only-host")

    linux_tools = {"perf", "strace", "ltrace", "readelf", "ldd"}
    hardware_tools = {"perf", "cargo-flamegraph", "valgrind", "heaptrack"}
    family = config["group"]
    components = [f"preinstalled `{tool}` at a resolved version" for tool in resolved_tools if tool not in core_tools]
    if "miri" in tools:
        components.append("Miri component for the project-pinned nightly")
    if re.search(r"sanitizer", body, re.IGNORECASE):
        components.append("documented sanitizer runtime for the selected target")

    return {
        "tools": resolved_tools,
        "applicable_version": version,
        "status": channel,
        "os_constraints": ["linux"] if set(tools) & linux_tools else ["resolve from project and installed tool"],
        "target_constraints": ["resolve host and target triples"] if family in {"cargo", "ffi", "systems"} else ["resolve active target"],
        "hardware_constraints": ["resolve CPU, kernel, or device capabilities"] if set(tools) & hardware_tools or family == "systems" else [],
        "required_components_and_dependencies": sorted(set(components)),
        "side_effects": sorted(effects),
        "evidence_ids": evidence_ids,
        "decision": status,
        "reason": "The source command is individually classified but not shipped; re-resolve exact syntax and prerequisites before any authorized execution.",
    }


def refresh_command_contracts(data: dict) -> None:
    bodies: dict[tuple[str, int], str] = {}
    for path in selected_markdown():
        for index, match in enumerate(FENCE.finditer(path.read_text(encoding="utf-8")), start=1):
            bodies[(relative(path), index)] = normalize_block(match.group(2))
    for block in data["blocks"]:
        occurrence = block["occurrences"][0]
        config = FAMILY_CONFIG[occurrence["family"]]
        contract = command_contract(
            bodies[(occurrence["source_path"], occurrence["block_index"])],
            block["language"],
            config,
            block["status"],
            block["evidence_ids"],
        )
        if contract:
            block["command_contract"] = contract
        else:
            block.pop("command_contract", None)
        if block["language"] == "rust":
            block["rust_example"] = "fragment" if block["status"] == "fragment" else None
        else:
            block.pop("rust_example", None)


def relative(path: Path) -> str:
    return path.relative_to(SOURCE).as_posix()


def target_for_family(name: str) -> str:
    return f"skills/{FAMILY_CONFIG[name]['owner']}/references/low-level/{name}.md"


def refresh_summary(data: dict) -> None:
    counts = Counter(entry["status"] for entry in data["entries"])
    block_counts = Counter(block["status"] for block in data["blocks"])
    data["summary"] = {
        "source_files": len(data["entries"]),
        **{status: counts[status] for status in sorted(STATUSES)},
        "block_decisions": {status: block_counts[status] for status in sorted(BLOCK_STATUSES)},
        "command_blocks": sum("command_contract" in block for block in data["blocks"]),
        "rust_blocks": sum(block["language"] == "rust" for block in data["blocks"]),
    }


def save(data: dict) -> None:
    refresh_summary(data)
    LEDGER.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def initialize(force: bool) -> None:
    if LEDGER.exists() and not force:
        raise SystemExit(f"ledger already exists: {LEDGER}")
    roots = skill_roots()
    selected = selected_markdown()
    selected_set = set(selected)
    entries = []
    for path in source_files():
        entries.append(
            {
                "source_path": relative(path),
                "source_sha256": digest(path),
                "source_bytes": path.stat().st_size,
                "source_lines": line_count(path),
                "status": "pending",
                "target_paths": [],
                "reason": "Awaiting sequential low-level source review.",
                "selected": path in selected_set or path.name == "LICENSE",
            }
        )

    blocks: dict[str, dict] = {}
    occurrences = 0
    for path in selected:
        name = next(name for name, root in roots.items() if path == root or root in path.parents)
        for index, match in enumerate(FENCE.finditer(path.read_text(encoding="utf-8")), start=1):
            occurrences += 1
            sha = block_digest(match.group(2))
            record = blocks.setdefault(
                sha,
                {
                    "source_sha256": sha,
                    "language": (match.group(1).strip().split() or ["plain"])[0].lower(),
                    "status": "pending",
                    "target_paths": [],
                    "reason": "Awaiting sequential source-family classification.",
                    "evidence_ids": [],
                    "occurrences": [],
                },
            )
            record["occurrences"].append(
                {"source_path": relative(path), "block_index": index, "family": name}
            )

    metrics = {
        "all_markdown_files": sum(path.suffix.lower() == ".md" for path in source_files()),
        "all_skill_files": sum(path.name == "SKILL.md" for path in source_files()),
        "selected_markdown_files": len(selected),
        "selected_markdown_lines": sum(line_count(path) or 0 for path in selected),
        "source_blocks": occurrences,
        "unique_source_blocks": len(blocks),
        "source_block_aliases": occurrences - len(blocks),
    }
    assert len(entries) == 213
    assert metrics == {
        "all_markdown_files": 205,
        "all_skill_files": 142,
        "selected_markdown_files": 84,
        "selected_markdown_lines": 16211,
        "source_blocks": 740,
        "unique_source_blocks": 738,
        "source_block_aliases": 2,
    }
    data = {
        "schema_version": 1,
        "source": {
            "name": "mohitmishra786/low-level-dev-skills",
            "relative_path": "references/low-level-dev-skills",
            "revision": "bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608",
            "commit_date": "2026-06-27T17:34:03+05:30",
            "license": "MIT",
            "copyright": "Copyright (c) 2026 chessMan",
        },
        "reviewed_on": "2026-08-23",
        "statuses": sorted(STATUSES),
        "block_statuses": sorted(BLOCK_STATUSES),
        "family_order": FAMILY_ORDER,
        "source_metrics": metrics,
        "evidence": {
            key: {
                "authority": value[0],
                "channel": value[1],
                "subject": value[2],
                "url": value[3],
                "reviewed_on": "2026-08-23",
            }
            for key, value in EVIDENCE.items()
        },
        "summary": {},
        "entries": entries,
        "blocks": [blocks[key] for key in sorted(blocks)],
    }
    save(data)


def load() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def entries_by_path(data: dict) -> dict[str, dict]:
    return {entry["source_path"]: entry for entry in data["entries"]}


def blocks_by_hash(data: dict) -> dict[str, dict]:
    return {block["source_sha256"]: block for block in data["blocks"]}


def classify_block(body: str, evidence_ids: list[str]) -> tuple[str, str, list[str]]:
    normalized = normalize_block(body)
    if WRONG_COMMAND.search(normalized):
        return "rejected", "Rejected: contains an obsolete or incorrect concrete command, target name, path, or unpinned image reference.", evidence_ids
    if SIDE_EFFECT_COMMAND.search(normalized):
        return "rejected", "Rejected from runtime guidance: installs tools/components, uses network or privilege, mutates host policy, updates resolution, or exposes credential-shaped configuration.", evidence_ids
    return "fragment", "Reviewed as source evidence only; useful concepts were rewritten into the family protocol, but the block is not shipped as an executable or compilable product claim.", evidence_ids


def stage_family(name: str) -> None:
    data = load()
    if name not in FAMILY_CONFIG:
        raise SystemExit(f"unknown family: {name}")
    in_progress = [entry for entry in data["entries"] if entry["status"] == "in_progress"]
    if in_progress:
        active = sorted({Path(entry["source_path"]).parent.name for entry in in_progress})
        raise SystemExit(f"finish the active family first: {active}")
    entries = entries_by_path(data)
    root = skill_roots()[name]
    source = root / "SKILL.md"
    source_entry = entries[relative(source)]
    if source_entry["status"] != "pending":
        raise SystemExit(f"family already staged or finalized: {name}")
    target = target_for_family(name)
    for path in family_markdown(name):
        entries[relative(path)].update(
            status="in_progress",
            target_paths=[target],
            reason=f"Sequential review of {name} is in progress.",
        )
    STAGING.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, STAGING / f"{name}.md")
    save(data)
    print(f"staged {name}: {relative(source)}")


def source_topics(name: str) -> list[tuple[str, str]]:
    generic = {"purpose", "triggers", "when to use", "workflow", "examples", "common problems", "related skills", "references"}
    topics: list[tuple[str, str]] = []
    for path in family_markdown(name):
        for heading in HEADING.findall(path.read_text(encoding="utf-8")):
            clean = re.sub(r"^\d+\.\s*", "", heading.strip()).strip("`")
            if clean.lower() in generic:
                continue
            pair = (relative(path), clean)
            if pair not in topics:
                topics.append(pair)
    return topics


def render_family(name: str, data: dict) -> str:
    config = FAMILY_CONFIG[name]
    protocol = GROUP_PROTOCOLS[config["group"]]
    root = skill_roots()[name]
    canonical = entries_by_path(data)[relative(root / "SKILL.md")]
    source_paths = [relative(root / "SKILL.md"), *[
        relative(path) for path in family_markdown(name) if path != root / "SKILL.md"
    ]]
    related_blocks = {
        block["source_sha256"]: block
        for block in data["blocks"]
        if any(item["family"] == name for item in block["occurrences"])
    }
    block_counts = Counter(block["status"] for block in related_blocks.values())
    title = name.replace("-", " ").title()
    lines = [
        f"# Low-level {title} protocol",
        "",
        f"<!-- low-level-source-family: {name}; source={canonical['source_path']}; sha256={canonical['source_sha256']}; revision={data['source']['revision']} -->",
        "",
        f"> Reviewed adaptation of `{source_paths[0]}` and {len(source_paths) - 1} supporting Markdown file(s). The source is evidence, not executable product policy.",
        "",
        "## Routing and retained scope",
        "",
        f"- Primary owner: `${config['owner']}`.",
        f"- Supporting profiles: {', '.join(f'`${item}`' for item in config['supporting']) or 'none'}.",
        f"- Retained scope: {config['focus']}",
        f"- Baseline correction: {config['correction']}",
        "- Project toolchain, MSRV, Edition, target, resolved dependencies, CI, hardware, operating system, and explicit user contract override this reference.",
        "",
        "## Required context",
        "",
        *[f"- {item}." for item in protocol["context"]],
        "",
        "## Decision protocol",
        "",
        *[f"{index}. {item}" for index, item in enumerate(protocol["steps"], start=1)],
        "",
        "## Source-derived knowledge map",
        "",
        "The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.",
        "",
    ]
    for path, topic in source_topics(name):
        lines.append(f"- `{topic}` — inspect when relevant; source `{path}`.")
    lines += [
        "",
        "## Failure modes and guardrails",
        "",
        *[f"- {item}" for item in protocol["pitfalls"]],
        "- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.",
        "- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.",
        "",
        "## Source example disposition",
        "",
        f"This family contains {sum(block_counts.values())} unique source block bodies: "
        + ", ".join(f"{block_counts[key]} `{key}`" for key in sorted(block_counts) if block_counts[key])
        + ". Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.",
        "",
        "## Evidence gate",
        "",
    ]
    for evidence_id in config["evidence"]:
        item = data["evidence"][evidence_id]
        lines.append(f"- [`{evidence_id}`]({item['url']}) — {item['subject']}; `{item['channel']}`, reviewed {item['reviewed_on']}.")
    lines += [
        "",
        "Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.",
        "",
    ]
    return "\n".join(lines)


def finalize_family(name: str) -> None:
    data = load()
    entries = entries_by_path(data)
    blocks = blocks_by_hash(data)
    root = skill_roots()[name]
    staged = STAGING / f"{name}.md"
    if not staged.is_file():
        raise SystemExit(f"family is not staged: {name}")
    target = target_for_family(name)
    evidence_ids = FAMILY_CONFIG[name]["evidence"]
    seen: set[str] = set()
    for path in family_markdown(name):
        for match in FENCE.finditer(path.read_text(encoding="utf-8")):
            sha = block_digest(match.group(2))
            if sha in seen:
                continue
            seen.add(sha)
            status, reason, evidence = classify_block(match.group(2), evidence_ids)
            record = blocks[sha]
            if record["status"] not in {"pending", status}:
                raise AssertionError(f"conflicting decision for block {sha}")
            record.update(status=status, target_paths=[], reason=reason, evidence_ids=evidence)
            contract = command_contract(match.group(2), record["language"], FAMILY_CONFIG[name], status, evidence)
            if contract:
                record["command_contract"] = contract

    for path in family_markdown(name):
        entry = entries[relative(path)]
        status = "adapted" if path.name == "SKILL.md" else "merged"
        reason = (
            "Canonical workflow rewritten as a product-owned decision protocol with official evidence gates and per-block classification."
            if status == "adapted"
            else "Supporting source topics merged into the reviewed family protocol; the source file is not shipped separately."
        )
        entry.update(status=status, target_paths=[target], reason=reason)

    target_path = PLUGIN / target
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(render_family(name, data), encoding="utf-8")
    staged.unlink()
    if STAGING.exists() and not any(STAGING.iterdir()):
        STAGING.rmdir()
    save(data)
    print(f"finalized {name} -> {target}")


def exclusion_reason(path: str) -> str:
    if path.startswith(".github/"):
        return f"Excluded `{path}`: upstream CI/repository automation is not dual-host runtime policy."
    if path.startswith("website/"):
        return f"Excluded `{path}`: upstream website source is presentation material, not Rust engineering guidance."
    if path in {"AGENTS.md", ".markdownlint.json"}:
        return f"Excluded `{path}`: upstream authoring or lint configuration is replaced by this repository's own instructions."
    if Path(path).name.startswith("README"):
        return f"Excluded `{path}`: upstream catalog/install documentation describes the source package, not this product interface."
    parts = Path(path).parts
    if parts and parts[0] == "skills":
        leaf = Path(path).parent.name
        domain = parts[1] if len(parts) > 1 else "unknown"
        return f"Excluded `{path}`: source profile `{leaf}` in `{domain}` is outside the selected 52 Rust low-level families or duplicates an existing owner without new requested material."
    return f"Excluded `{path}`: development metadata or non-selected source material is not required by the reviewed Rust low-level integration."


def finalize_remaining() -> None:
    data = load()
    if any(entry["status"] == "in_progress" for entry in data["entries"]):
        raise SystemExit("finish the active family before finalizing remaining entries")
    entries = entries_by_path(data)
    for name in FAMILY_ORDER:
        source = relative(skill_roots()[name] / "SKILL.md")
        if entries[source]["status"] != "adapted":
            raise SystemExit(f"family not finalized: {name}")
    notices = ["THIRD_PARTY_NOTICES.md", "provenance/THIRD_PARTY_NOTICES.md", "provenance/low-level-dev-coverage.json"]
    for entry in data["entries"]:
        if entry["status"] != "pending":
            continue
        if entry["source_path"] == "LICENSE":
            entry.update(status="merged", target_paths=notices, reason="Pinned MIT license and copyright reproduced in product notices and coverage metadata.")
        else:
            entry.update(status="excluded", target_paths=[], reason=exclusion_reason(entry["source_path"]))
    save(data)
    print("finalized non-family low-level entries")


def render_baseline(data: dict) -> str:
    lines = [
        "# Low-level tooling baseline",
        "",
        "> Product-owned command safety and evidence policy for the low-level source integration. Reviewed 2026-08-23; project state always wins.",
        "",
        "## Precedence",
        "",
        "1. Explicit user contract and repository instructions.",
        "2. Project `rust-toolchain*`, MSRV, Edition, Cargo manifests/config, lockfile, CI, target and resolved tool versions.",
        "3. Current official Rust/Cargo documentation for language, compiler, target and Cargo behavior.",
        "4. Exact tool-owner documentation for external profilers, caches, audit tools and runners.",
        "5. This product baseline: Rust 1.98, Edition 2024 and resolver 3; never an implicit upgrade request.",
        "",
        "## Command contract",
        "",
        "Before running a command, record tool/version, stable/nightly/external channel, OS/target/hardware, required components, build/network/install/privilege/config/lockfile effects, expected evidence, and stopping condition.",
        "",
        "- Automatic and read-only workflows never install tools or components, fetch the network, update resolution, use privilege, weaken host policy, or edit global Cargo/debugger configuration.",
        "- Use a project-pinned nightly when required. If unavailable, return `SKIP`; do not silently switch or install.",
        "- Use an external tool only when already installed/resolved or after explicit authorization.",
        "- Derive artifact locations from Cargo metadata and effective target/profile. Cargo's internal build-directory layout is not an API.",
        "- Keep raw profiler/timing evidence and compare the same workload before and after one change.",
        "",
        "## Corrected command semantics",
        "",
        "- Cargo timing entrypoint: `cargo build --timings`; by default the current report is under the effective target directory at `cargo-timings/cargo-timing.html`.",
        "- Resolve the effective directory with `cargo metadata --format-version 1 --locked --offline`; distinguish an offline cache miss from a project defect.",
        "- Rust sanitizer flags are nightly and target-specific. A sanitizer mode named `undefined` is not supported by rustc.",
        "- Miri executes MIR for selected tests or binaries; passing a run is not proof over all inputs, targets, FFI, optimizations or schedules.",
        "- `rustup target add` provides the Rust standard library for a target, not its linker, sysroot, native libraries, emulator, device or runtime acceptance.",
        "- perf frame-pointer, DWARF and LBR call graphs have different binary/CPU constraints; `perf_event_paranoid` is host security policy.",
        "- cargo-flamegraph, Criterion, cargo-bloat, cargo-llvm-lines, and sccache are external tools whose exact commands belong to the resolved installed version, not Cargo itself.",
        "- Flamegraphs locate sampled CPU hypotheses. Criterion or another comparable benchmark measures the change. cargo-bloat does not support WASM and crate attribution is an estimate; cargo-llvm-lines counts unoptimized LLVM IR lines, not runtime cost.",
        "- sccache is a compiler wrapper with cacheability limitations; remote credentials/backends and disabling incremental compilation are deployment decisions.",
        "- Cranelift/Cargo codegen backend, linker changes, LTO, PGO, BOLT and target CPU features require exact toolchain/target support plus measurement.",
        "",
        "## Evidence catalog",
        "",
    ]
    for key, item in sorted(data["evidence"].items()):
        lines.append(f"- [`{key}`]({item['url']}) — {item['subject']}; authority `{item['authority']}`, channel `{item['channel']}`.")
    lines.append("")
    return "\n".join(lines)


def write_indexes() -> None:
    data = load()
    refresh_command_contracts(data)
    save(data)
    for name in FAMILY_ORDER:
        target = PLUGIN / target_for_family(name)
        if target.is_file():
            target.write_text(render_family(name, data), encoding="utf-8")
    baseline = PLUGIN / "skills" / "rust-research" / "references" / "low-level-tooling-baseline.md"
    baseline.write_text(render_baseline(data), encoding="utf-8")
    owners: dict[str, list[tuple[str, str]]] = {}
    for name, config in FAMILY_CONFIG.items():
        owners.setdefault(config["owner"], []).append((name, "primary"))
        for supporting in config["supporting"]:
            owners.setdefault(supporting, []).append((name, "supporting"))
    for owner, rows in sorted(owners.items()):
        root = PLUGIN / "skills" / owner
        if not root.is_dir():
            raise SystemExit(f"missing owner skill: {owner}")
        index = root / "references" / "low-level-index.md"
        lines = [
            f"# Low-level references for `{owner}`",
            "",
            "Read the shared [tooling baseline]"
            f"({os.path.relpath(baseline, index.parent).replace(os.sep, '/')}) first when a command, artifact path, toolchain, target, profiler, sanitizer, privilege, or external tool is involved. Then load only the matching family.",
            "",
        ]
        for name, role in sorted(set(rows)):
            target = PLUGIN / target_for_family(name)
            link = os.path.relpath(target, index.parent).replace(os.sep, "/")
            lines.append(f"- [`{name}`]({link}) — {role}; {FAMILY_CONFIG[name]['focus']}")
        lines += [
            "",
            "`primary` owns the decision. `supporting` contributes one bounded constraint and then returns ownership. Source family names are references, not additional product skills.",
            "",
        ]
        index.write_text("\n".join(lines), encoding="utf-8")
        skill = root / "SKILL.md"
        content = skill.read_text(encoding="utf-8")
        marker = "[Low-level integration index](references/low-level-index.md)"
        if marker not in content:
            content = content.rstrip() + (
                "\n\n## Low-level protocols\n\n"
                "For source-derived debugging, profiling, build, sanitizer, cross-target, ABI, async-internal, security, or hardware detail relevant to this profile, read the "
                f"{marker} and load only the matching family. Apply its official-evidence and command-safety gate before execution.\n"
            )
            skill.write_text(content, encoding="utf-8")
    print(f"wrote low-level baseline and indexes for {len(owners)} owners/supporters")


def verify() -> None:
    data = load()
    assert data["schema_version"] == 1
    assert set(data["statuses"]) == STATUSES
    assert set(data["block_statuses"]) == BLOCK_STATUSES
    assert data["family_order"] == FAMILY_ORDER
    assert data["source"] == {
        "name": "mohitmishra786/low-level-dev-skills",
        "relative_path": "references/low-level-dev-skills",
        "revision": "bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608",
        "commit_date": "2026-06-27T17:34:03+05:30",
        "license": "MIT",
        "copyright": "Copyright (c) 2026 chessMan",
    }
    assert data["source_metrics"] == {
        "all_markdown_files": 205,
        "all_skill_files": 142,
        "selected_markdown_files": 84,
        "selected_markdown_lines": 16211,
        "source_blocks": 740,
        "unique_source_blocks": 738,
        "source_block_aliases": 2,
    }
    assert set(data["evidence"]) == set(EVIDENCE)
    for item in data["evidence"].values():
        assert item["url"].startswith("https://") and item["reviewed_on"] == "2026-08-23"

    entries = data["entries"]
    assert len(entries) == 213 and len({entry["source_path"] for entry in entries}) == 213
    counts = Counter(entry["status"] for entry in entries)
    assert counts == {"adapted": 52, "merged": 33, "excluded": 128}
    assert not [entry for entry in entries if entry["status"] in {"pending", "in_progress", "duplicate"}]
    indexed = entries_by_path(data)
    actual = source_files() if SOURCE.is_dir() else []
    if SOURCE.is_dir():
        assert len(actual) == 213 and {relative(path) for path in actual} == set(indexed)
    for path in actual:
        entry = indexed[relative(path)]
        assert digest(path) == entry["source_sha256"]
        assert path.stat().st_size == entry["source_bytes"]
        assert line_count(path) == entry["source_lines"]
        if entry["status"] in {"adapted", "merged"}:
            assert entry["target_paths"]
        else:
            assert not entry["target_paths"]
        for target in entry["target_paths"]:
            assert (PLUGIN / target).is_file(), f"missing target: {target}"

    blocks = data["blocks"]
    assert len(blocks) == 738 and sum(len(block["occurrences"]) for block in blocks) == 740
    assert not [block for block in blocks if block["status"] == "pending"]
    for block in blocks:
        assert block["status"] in {"fragment", "rejected"}
        assert block["reason"] and block["evidence_ids"]
        assert set(block["evidence_ids"]) <= set(EVIDENCE)
        assert not block["target_paths"]
        contract = block.get("command_contract")
        if contract:
            assert contract["tools"] and contract["applicable_version"]
            assert contract["status"] in {"stable", "nightly", "external"}
            assert contract["os_constraints"] and contract["target_constraints"]
            assert contract["side_effects"] and contract["evidence_ids"] == block["evidence_ids"]
            assert contract["decision"] == block["status"] and contract["reason"]

    assert data["summary"]["command_blocks"] == sum("command_contract" in block for block in blocks)
    assert data["summary"]["command_blocks"] >= 386
    rust_blocks = [block for block in blocks if block["language"] == "rust"]
    assert data["summary"]["rust_blocks"] == len(rust_blocks)
    for block in rust_blocks:
        assert block["rust_example"] == ("fragment" if block["status"] == "fragment" else None)

    for name, config in FAMILY_CONFIG.items():
        target = PLUGIN / target_for_family(name)
        assert target.is_file() and f"source-family: {name}" in target.read_text(encoding="utf-8")
        source_entry = indexed[relative(skill_roots()[name] / "SKILL.md")]
        assert source_entry["status"] == "adapted" and source_entry["target_paths"] == [target_for_family(name)]
        for profile in [config["owner"], *config["supporting"]]:
            index = PLUGIN / "skills" / profile / "references" / "low-level-index.md"
            assert index.is_file() and f"`{name}`" in index.read_text(encoding="utf-8")

    assert not STAGING.exists()
    low_level_files = list((PLUGIN / "skills").glob("*/references/low-level/*.md"))
    assert len(low_level_files) == 52
    combined = "\n".join(path.read_text(encoding="utf-8") for path in low_level_files)
    baseline = (PLUGIN / "skills" / "rust-research" / "references" / "low-level-tooling-baseline.md").read_text(encoding="utf-8")
    assert "-Zsanitizer=undefined" not in combined
    assert "build/cargo-timings" not in combined
    assert not re.search(r"image\s*=.*:main\b", combined, re.IGNORECASE)
    assert "mode named `undefined` is not supported" in baseline
    forbidden_skills = {"rust-security", "rust-profiling", "rust-cross", "rust-tooling", "rust-build-times", "rust-sanitizers-miri", "rust-async-internals"}
    product_skills = {path.name for path in (PLUGIN / "skills").iterdir() if path.is_dir()}
    assert not (forbidden_skills & product_skills)
    print("OK: 213 files, 52 adapted families, 84 selected Markdown files, 740/738/2 block accounting")


def main() -> None:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--force", action="store_true")
    stage = commands.add_parser("stage-family")
    stage.add_argument("family", choices=FAMILY_ORDER)
    finalize = commands.add_parser("finalize")
    finalize.add_argument("family", nargs="?", choices=FAMILY_ORDER)
    commands.add_parser("write-indexes")
    commands.add_parser("verify")
    args = parser.parse_args()
    if args.command == "init":
        initialize(args.force)
    elif args.command == "stage-family":
        stage_family(args.family)
    elif args.command == "finalize":
        finalize_family(args.family) if args.family else finalize_remaining()
    elif args.command == "write-indexes":
        write_indexes()
    else:
        verify()


if __name__ == "__main__":
    main()
