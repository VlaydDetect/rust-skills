# Unsafe Rust Field Guide

This guide is the detailed policy for `rust-unsafe`. It synthesizes the craft unsafe raw-pointer and invariant guides plus full-stack stable Rust and unsafe-FFI distinctions; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

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
