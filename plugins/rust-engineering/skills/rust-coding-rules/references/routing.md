# Rule Routing

Route this rulebook only after the task's owning profile and effective project state are known. Exact IDs win over inference; prefix requests select one category; task requests select the smallest evidence-backed RuleSet.

## RuleQuery

```text
selector: exact ID | prefix | task
constructs: changed types, functions, traits, macros, manifests, tests, or unsafe operations
primary_profile: the decision owner selected outside this rulebook
boundary: private | public | unsafe | FFI
toolchain: edition, MSRV, compiler, target
configuration: features, accepted dependencies, runtime
performance: measured hot path or none
phase: design | implementation | post-diff | review
```

Do not infer unknown configuration. A direct ID lookup still reads and applies that rule's `Avoid When` and prerequisites; direct invocation is not an override.

## Category Index

| Prefix | Category | Owner profile | Select when |
|---|---|---|---|
| [`own-`](categories/own.md) | Ownership and borrowing | `rust-ownership` | Moves, borrows, lifetimes, pointers, mutation, or drop control correctness. |
| [`err-`](categories/err.md) | Error handling | `rust-errors` | Failure taxonomy, propagation, context, recovery, or panic policy changes. |
| [`mem-`](categories/mem.md) | Memory optimization | `rust-performance` | Measurements identify allocation, footprint, layout, locality, or move cost. |
| [`unsafe-`](categories/unsafe.md) | Unsafe code | `rust-unsafe` | Unsafe operations or safe wrappers need a soundness proof. |
| [`api-`](categories/api.md) | API design | `rust-api-design` | A public or independently evolving caller contract changes. |
| [`async-`](categories/async.md) | Async and await | `rust-concurrency` | Suspension, task ownership, cancellation, runtime, or backpressure matters. |
| [`conc-`](categories/conc.md) | Concurrency | `rust-concurrency` | Correctness or liveness spans threads, tasks, locks, channels, or atomics. |
| [`opt-`](categories/opt.md) | Compiler optimization | `rust-performance` | A reproducible benchmark or profile supports a compiler or target hypothesis. |
| [`num-`](categories/num.md) | Numeric safety | `rust-idioms` | Range, overflow, casts, floating-point semantics, or numeric invariants matter. |
| [`type-`](categories/type.md) | Type safety | `rust-traits` | Types can enforce a demonstrated state, identity, or representation invariant. |
| [`trait-`](categories/trait.md) | Traits and generics | `rust-traits` | Real variation needs dispatch, associated types, coherence, or an extension point. |
| [`conv-`](categories/conv.md) | Conversions | `rust-api-design` | Borrowed, infallible, fallible, parsing, or lossy conversion semantics change. |
| [`const-`](categories/const.md) | Const and compile time | `rust-stable` | Const evaluation or value parameterization is useful within the actual MSRV. |
| [`serde-`](categories/serde.md) | Serde | `rust-api-design` | An accepted Serde boundary needs explicit wire and compatibility behavior. |
| [`pat-`](categories/pat.md) | Pattern matching | `rust-idioms` | Extraction, exhaustiveness, guards, or early return can be expressed more clearly. |
| [`macro-`](categories/macro.md) | Macros | `rust-macros` | Rust syntax generation is necessary after ordinary abstractions are rejected. |
| [`closure-`](categories/closure.md) | Closures | `rust-traits` | Capture, call multiplicity, storage, lifetime, or callback dispatch matters. |
| [`coll-`](categories/coll.md) | Collections | `rust-stdlib` | Operations and guarantees determine a collection choice. |
| [`name-`](categories/name.md) | Naming | `rust-api-design` or `rust-style-clippy` | Names communicate public semantics or a configured convention. |
| [`test-`](categories/test.md) | Testing | `rust-testing` | A concrete contract needs a particular test level or technique. |
| [`doc-`](categories/doc.md) | Documentation | `rust-documentation` | Rustdoc, examples, safety, failures, features, or migration guidance changes. |
| [`obs-`](categories/obs.md) | Observability | `rust-observability` | A known operational question needs a bounded, redacted signal. |
| [`perf-`](categories/perf.md) | Performance patterns | `rust-performance` | Controlled evidence identifies a semantics-preserving runtime pattern. |
| [`proj-`](categories/proj.md) | Project structure | `rust-module-layout`, `rust-workspace`, `rust-cargo-build`, or `rust-stable` | A real module, crate, Cargo, feature, MSRV, or generation boundary changes. |
| [`lint-`](categories/lint.md) | Clippy and linting | `rust-style-clippy` | Formatting, lint, warning, cfg, or CI policy controls the work. |
| [`anti-`](categories/anti.md) | Anti-patterns | Canonical owner or `rust-idioms` | A concrete smell has demonstrated impact; most duplicates route to a positive rule. |

## Common Task Routing

| Task signal | Start with | Add only if evidence requires it |
|---|---|---|
| Borrow-checker or resource-lifetime change | `own-` | `err-`, `async-`, or `unsafe-` |
| Public async API | `api-` | `async-`, `err-`, `doc-` |
| Serialization boundary | `serde-` | `api-`, `type-`, `err-` |
| Unsafe or FFI diff | `unsafe-` | `type-`, `test-`; ABI remains owned by `rust-unsafe-ffi` |
| Measured latency or memory regression | `perf-` or `mem-` | `opt-`, `coll-`, `own-` |
| Macro implementation | `macro-` | `api-`, `trait-`, `test-` |
| Review of a bounded Rust diff | Category matching the changed contract | `anti-` or `lint-` only for concrete impact |

This table names search order, not a command to load whole categories. Select individual IDs after opening the relevant index.

## RuleSet Contract

```text
selected:
  - id: rule-id
    reason: opened code and contract that establish the premise
prerequisites: accepted dependencies, MSRV, target, runtime, measurements, or none
conflicts: higher-precedence contract and resolution, or none
deferred: categories or batches intentionally not loaded
```

A normal RuleSet has one to eight IDs. If more are plausible, split by phase or category and re-query after each diff.

## Conflict and Negative Routing

- User and project contracts beat every rule. The primary profile owns semantic decisions.
- A rule that names a crate does not authorize adding it. If the crate is absent and no approval exists, defer the rule.
- Performance rules require representative evidence; source-level intuition is not a measurement.
- Public API, wire, ABI, feature, MSRV, target, panic, ordering, and safety changes require their owner-profile review.
- `rust-verify` does not automatically select rules; it runs evidence already chosen by workflow or review.
- Do not activate this rulebook for Nix-only work, verification-only requests, general Rust trivia, or architecture work with no local Rust coding decision.
- A rule ID can support a review finding only after real code establishes the trigger, caller-visible impact, and closure evidence.

## Broad Audits

Audit one category at a time and no more than eight rules per batch. Record each batch's selected IDs, confirmed findings, rejected premises, and deferred work before opening the next batch. Alias IDs resolve to canonical rules and do not create duplicate findings.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-anti-pattern`](../../rust-idioms/references/anti-pattern.md) — supporting; Symptom-to-cause diagnosis for cloning, allocation, stringly APIs, panic, locking, abstraction, collection, and async mistakes.
- [`rust-coding`](../../rust-style-clippy/references/coding.md) — supporting; Readable Rust, naming, formatting, Clippy scope, documentation, control flow, API conventions, and reviewable diffs.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
