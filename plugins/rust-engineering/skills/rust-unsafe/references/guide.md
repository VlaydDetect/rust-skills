# Unsafe Rust Field Guide

This guide is the detailed policy for `rust-unsafe`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Unsafe permits a small set of operations; it does not disable Rust's validity, aliasing, lifetime, and data-race rules.
- Soundness is a universal claim over every safe call pattern, feature, target, panic path, and concurrency interaction in scope.
- Raw-pointer dereference requires a valid, aligned, appropriately initialized allocation for the accessed type and duration.
- References carry stronger aliasing and validity guarantees than raw pointers, so creating a reference is itself consequential.
- Partial initialization needs an explicit count or state and a drop strategy for both success and unwind paths.
- Layout promises require `repr` attributes or a documented compiler contract; ordinary Rust layout is not a stable ABI.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Safe std or established crate covers need | Use the safe abstraction | It concentrates proof and platform testing |
| Local bounds-checked hot path | Measure before targeted unsafe | Unsafe complexity needs demonstrated value |
| Partial array initialization | MaybeUninit with initialization guard | Success and unwind must drop exactly initialized values |
| Interior mutation | Cell, RefCell, lock, or atomic first | UnsafeCell alone does not enforce access rules |
| Foreign ABI operation | Route to rust-unsafe-ffi | ABI and foreign lifecycle add separate obligations |

## Common Failure Modes

- Writing `SAFETY: caller guarantees` inside a safe function that exposes no such obligation.
- Creating slices or references from raw parts before validating null, alignment, length, allocation, and lifetime.
- Assuming `repr(Rust)` field order or enum layout across versions or languages.
- Leaking or double-dropping partially initialized elements on panic.
- Using Miri or one architecture's tests as a substitute for an invariant proof.

## Required Evidence

- An operation-by-operation safety argument tied to checks, types, and ownership in opened code.
- Tests for empty, boundary, invalid, panic, drop, concurrency, and target-specific cases that apply.
- Miri or sanitizer records with the exact configuration and acknowledged coverage limits.
- A safe API review showing callers cannot construct invalid states or violate hidden obligations.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-dpdk`](../../rust-systems-networking/references/dpdk.md) — supporting; Mempools, mbuf ownership, queues, burst processing, RSS, NUMA placement, affinity, and bounded packet-resource lifecycles.
- [`rust-ebpf`](../../rust-systems-networking/references/ebpf.md) — supporting; Verifier constraints, bounded control flow, maps, XDP and probe attachment, no_std code, kernel/user ABI, and observability boundaries.
- [`rust-embedded`](../../rust-architecture/references/domains/embedded-runtime.md) — supporting; no_std constraints, HAL ownership, interrupts, bounded memory, timing, peripherals, power, and deterministic cleanup.
- [`rust-ffi`](../../rust-unsafe-ffi/references/ffi-boundaries.md) — supporting; ABI layout, ownership transfer, allocator pairing, strings, callbacks, panic containment, handles, and foreign-thread behavior.
- [`rust-pin`](../../rust-pin/references/pin.md) — supporting; Address sensitivity, Pin/Unpin, structural projection, self-reference, Future polling, and the drop guarantee.
- [`rust-unsafe`](./unsafe-invariants.md) — primary; Unsafe preconditions, aliasing, initialization, layout, provenance, Send/Sync, panic safety, and safe-abstraction review.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return the decision to its owner after coding constraints or helper evidence have been stated.
