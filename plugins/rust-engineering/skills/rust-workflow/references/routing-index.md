# Profile Routing Index

Use this index to find candidate profiles after the current `TaskBrief` is known. Build roles and enforce circuit breakers with the canonical [ProfileStack contract](./profile-stack.md): one owner per decision unit, coding profiles for actual Rust constructs, and helpers only after an observed trigger. Loading every relevant-looking profile weakens ownership and wastes context.

All profiles may be invoked manually. In an implementation task `rust-workflow` remains the writer and uses the selected profiles as engineering policy. A focused user question may invoke a profile directly.

## Host Invocation

Profile names in these files are host-neutral. For an explicit manual invocation use `$profile-name` in Codex and `/rust-engineering:profile-name` in Claude Code. During automatic routing, use the host's native skill mechanism rather than emitting the other host's command syntax. `agents/openai.yaml` contains the Codex manual prompt metadata; Claude Code discovers the same `SKILL.md` files from the plugin namespace.

## Entrypoints

| Profile | Owns | Route here when |
|---|---|---|
| `rust-workflow` | Discovery, routing, implementation, integration, final diff | The request changes code, manifests, tests, docs, or Nix files. |
| `rust-review` | Read-only diff or pull-request findings and verdict | The user asks to review, audit a change, or identify defects without editing. |
| `rust-verify` | Read-only command evidence and failure classification | The user asks to run checks or prove an existing state without fixing it. |

## Reference Overlay

| Skill | Owns | Route here when |
|---|---|---|
| `rust-coding-rules` | Addressable concrete rules selected after an owner profile | An exact rule ID or prefix is requested, or workflow/review needs a RuleSet of at most nine context-matched rules per decision unit. It never occupies a `ProfileStack` role. |

## Reviewed Cargo-tool overlays

These are progressive references under existing owners, not standalone profiles. Load one only when the named tool or its specific capability controls the task; a generic Rust request or the mere presence of `Cargo.toml` is not enough.

| Trigger | Decision owner | Additional profiles to classify from current evidence | Reference |
|---|---|---|---|
| Project generation from a local/remote template; Liquid, placeholders, conditionals, Rhai hooks | `rust-cargo-build` | `rust-workspace`, `rust-research` | `cargo-generate` |
| Nextest filters, profiles, groups, retries, timeouts, JUnit, or process-per-test behavior | `rust-testing` | `rust-verify`, `debugging` | `cargo-nextest` |
| LLVM source coverage, reports, thresholds, nextest integration, branch/doctest coverage | `rust-testing` | `rust-verify`, `rust-research` | `cargo-llvm-cov` |
| cargo-machete unused-dependency findings, false positives, exit codes, or metadata-assisted scan | `rust-dependencies` | `rust-cargo-build`, `rust-verify` | `cargo-machete` |
| Cargo target/build state across Git linked worktrees, cache contention, or artifact identity | `rust-cargo-build` | `rust-performance`, `rust-verify` | `cargo-worktree-builds` |
| Clippy groups/priorities, workspace inheritance, typed config, disallowed items, or lint-policy migration | `rust-style-clippy` | `rust-stable`, `rust-verify` | `clippy-advanced` |

`mockito-http-mocking` is intentionally absent: it has no profile, reference, trigger, agent, hook, or positive route.

## Engineering Process

| Profile | Owns | Route here when |
|---|---|---|
| `addressing-findings` | Stable finding ledger, triage, ordered fixes, closure, fresh re-review | Findings already exist and must be accepted, rejected, deferred, fixed, and closed. |
| `codebase-onboarding` | First broad project map | The repository or affected subsystem is unfamiliar. |
| `debugging` | Reproduction, hypothesis, isolation, debugger/core/trace evidence, root cause | A compiler, test, runtime, timing, symbol, crash, hang, or integration failure is unexplained. |
| `refactoring` | Structural change under a preserved contract | Behavior should stay stable while code moves, splits, or simplifies. |
| `rust-navigation` | Bounded symbol, dispatch, cfg, macro, and call-path tracing | The project is known but the real definition, caller, impl, or effect path is not. |
| `rust-design-protocol` | Cross-layer mechanics/design/domain trace and evidence-backed `DesignBrief` | Repeated local failures, comparisons, or consequential ambiguity require adjacent-layer constraints. |
| `rust-research` | Dated Rust, Cargo, Clippy, std, crate, target, external-tool, docs, or news evidence | Correctness depends on current upstream or resolved-tool facts not fixed by the repository. |
| `specs` | Normative rules, examples, acceptance scenarios, non-goals | Product behavior is ambiguous or needs an executable contract. |

## Rust Language and Safety

| Profile | Owns | Route here when |
|---|---|---|
| `rust-stable` | Edition, compiler availability, MSRV, stable versus nightly | Toolchain or language-stability policy controls the answer. |
| `rust-stdlib` | Collections, iterators, I/O, paths, time, process, synchronization primitives | The decision is which standard-library facility expresses the contract. |
| `rust-by-example` | Minimal compiling or compile-fail demonstration | A concrete example is the requested output or best explanatory tool. |
| `rust-ownership` | Moves, borrowing, lifetimes, pointers, RAII, interior mutability, drop | Data or resource ownership is the main constraint. |
| `rust-traits` | Traits, bounds, associated types, dispatch, coherence, newtypes, typestate | Polymorphism or type-driven design is the main constraint. |
| `rust-errors` | Error taxonomy, propagation, context, recovery, panic policy | Caller-visible failure semantics are the main constraint. |
| `rust-idioms` | Semantic Rust patterns and anti-patterns | Correct code needs a Rust-native expression or pattern assessment. |
| `rust-unsafe` | Internal unsafe invariants, raw memory, validity, aliasing, layout, Miri and Rust sanitizers | Unsafe is internal to Rust and does not cross a foreign ABI. |
| `rust-pin` | Address sensitivity, Pin/Unpin, structural projection, self-reference, pinned destruction | Moving a value after a defined point could invalidate an internal address-dependent invariant. |

## Project, Cargo, and Public Contract

| Profile | Owns | Route here when |
|---|---|---|
| `rust-api-design` | Caller-visible Rust contract, visibility, ownership, extension policy | A public or independently evolving Rust API is added or changed. |
| `rust-cargo-build` | Effective Cargo state, targets, features, config, profiles, build scripts, linker/cache mechanics, explicit template generation, and worktree build layout | Cargo, cross-build, scaffolding, or linked-worktree build mechanics determine behavior. |
| `rust-workspace` | Crate boundaries, workspace policy, shared metadata, release relationships | The design unit is packages and their dependency direction. |
| `rust-module-layout` | In-crate modules, files, visibility, re-exports, tests | The design unit is structure inside one crate. |
| `rust-dependencies` | Adopted dependency versions, features, sources, advisories, licenses, supply policy, unused-dependency evidence, and removal | A dependency already exists or adoption has been approved. |
| `rust-crate-discovery` | Pre-adoption candidate research and build-versus-buy decision | A new external crate is being considered. |
| `rust-semver` | Released compatibility, baseline comparison, deprecation, migration | Downstream breakage or release classification is at issue. |
| `rust-documentation` | Rustdoc, doctests, examples, README, changelog, migration docs | The developer-facing contract or discoverability changes. |
| `rust-style-clippy` | rustfmt, Clippy, lint levels/priorities, typed config, and exceptions | Formatting or lint tooling is the controlling issue. |
| `rust-ecosystem` | Broad project shape and solution class before candidate selection | A new project or subsystem needs high-level Rust orientation. |

## Architecture

| Profile | Owns | Route here when |
|---|---|---|
| `rust-architecture` | New system boundaries, dependency direction, ports and adapters, CQRS or events | The task designs intended architecture. |
| `rust-architecture-review` | Read-only whole-project structural health | The task audits existing architecture rather than a bounded diff. |

## Runtime, Interop, and Specialized Systems

| Profile | Owns | Route here when |
|---|---|---|
| `rust-concurrency` | Threads, async/Future/Waker internals, channels, locks, atomics, cancellation, backpressure, shutdown | Correctness or liveness spans execution contexts. |
| `rust-testing` | Test and coverage strategy/implementation, including nextest execution policy, bounded fuzz targets, and crash regressions | Tests, their runner policy, or coverage contract is the deliverable. |
| `rust-performance` | Reproducible benchmarks, perf/flamegraphs/counters, allocation/size/build-time profiles, optimization, regression guards | A measured metric or regression controls the work. |
| `rust-observability` | Structured logs, spans, metrics, correlation, redaction, cardinality | Runtime behavior must become operationally diagnosable. |
| `rust-unsafe-ffi` | Foreign ABI, layout, handles, buffers, strings, callbacks, unwind | Unsafe crosses a language or runtime boundary. |
| `rust-platforms` | Unix and Windows APIs, OS-specific resource lifecycle, runtime capabilities, global allocator selection | Rust program behavior depends on POSIX/Linux/BSD/macOS/Windows APIs or a measured allocator decision; Nix environment and packaging work stays with Nix profiles. |
| `rust-serialization` | Binary byte formats, schema evolution, canonicality, validation, framing, decode limits | The durable or transported byte representation itself controls correctness. |
| `rust-data` | Data-oriented layout, ECS, arrays, columnar memory, query execution | Access patterns, shape, traversal, or analytical execution determine the representation. |
| `rust-database` | Transactions, client/pool lifecycle, schema migrations, retries, backup/restore, SurrealDB | Persistence semantics or database lifecycle owns the change, whether or not a desktop UI calls it. |
| `rust-tauri` | Tauri 2 IPC, capabilities, CSP, plugins, updater security, Specta TypeScript bindings | A Tauri window/webview trust boundary, plugin, packaging/update path, or generated frontend contract controls the work. |
| `rust-macros` | Declarative and procedural macro syntax, expansion, diagnostics, compile cost | Compile-time Rust token generation is necessary. |
| `rust-lombok-macros` | Lombok-style generated builders, accessors, constructors, validation | The request specifically concerns annotation-driven boilerplate APIs. |
| `rust-uniffi-building` | UniFFI UDL or proc-macro interfaces, scaffolding, bindings, packaging | UniFFI exposes Rust to supported foreign languages. |
| `rust-ml` | Models, tensors, preprocessing, devices, inference, batching, serving | ML pipeline semantics control the Rust system. |
| `rust-gpu` | Device capabilities, memory hierarchy, transfer, layout, dispatch, synchronization | GPU execution and host-device memory behavior control correctness or measured performance. |
| `rust-systems-networking` | eBPF verifier/map/ABI, AF_XDP UMEM/rings, and DPDK mempool/mbuf/queue/NUMA execution | Kernel probes or userspace packet pipelines impose environment-specific resource rules. |
| `rust-distributed-systems` | Cross-node failure, consistency, idempotency, retries, leases, versioned contracts, coordination | An operation crosses a process or node boundary and partial failure changes its meaning. |

For a compound request, route by decision phase instead of loading every domain at once. For example, a Tauri application with SurrealDB and a binary export first uses `rust-tauri` for the IPC/capability phase, then `rust-database` for transaction and migration work, then `rust-serialization` for the export contract. A NixOS deployment uses the relevant Nix owner for environment or service configuration and starts a separate `rust-platforms` phase only for Rust program behavior on that OS.

IoT, embedded, and cloud-native prompts start in `rust-architecture` with its
Design protocol domain constraint maps, then route mechanics to the existing owners
such as concurrency, performance, observability, errors, dependencies, unsafe,
or FFI. They do not require standalone framework profiles.

## Nix

| Profile | Owns | Route here when |
|---|---|---|
| `nix-flakes` | Flake inputs, lock, systems, outputs, follows, overlays | Flake composition or reproducibility is the issue. |
| `nix-dev-env` | Development shells, toolchain, native tools, direnv, hooks | Developer environment availability is the issue. |
| `nix-packaging` | Derivations, hashes, builders, native inputs, install artifacts | Reproducible build and package outputs are the issue. |
| `nixos` | NixOS or Home Manager options, services, users, files, secrets | Declarative deployment or user configuration is the issue. |
| `nix-review` | Read-only findings for Nix expressions and artifacts | The user requests Nix-specific review or audit. |

## Conflict Rules

Use these ownership splits when descriptions overlap:

- `rust-testing` decides which tests to create; `rust-verify` runs the evidence matrix and never edits tests.
- `rust-testing` defines nextest and coverage strategy; `rust-verify` only executes an already selected tool/profile/threshold contract.
- `rust-dependencies` decides whether a dependency can be removed; cargo-machete contributes heuristic evidence and never owns the edit.
- `rust-cargo-build` owns Git-worktree build layout; `rust-workspace` joins only when Cargo package topology changes.
- `rust-style-clippy` owns lint policy and tool configuration; `rust-review` judges the semantic correctness of a proposed lint fix.
- Coverage remains under `rust-testing` unless the request concerns a measured runtime or build-time metric; then `rust-performance` may support it.
- A general Rust task does not activate cargo-generate, nextest, LLVM coverage, machete, worktree-build, or advanced-Clippy references solely because a manifest exists.
- `rust-review` reviews a bounded diff; `rust-architecture-review` assesses whole-project structure; `nix-review` owns Nix-specific findings.
- `rust-unsafe` owns Rust-internal validity and aliasing; `rust-unsafe-ffi` adds ABI and foreign lifecycle; `rust-uniffi-building` owns the UniFFI generation workflow.
- `rust-idioms` owns semantic patterns; `rust-style-clippy` owns formatter and lint policy; `rust-api-design` owns public caller contracts.
- `rust-ecosystem` chooses a broad solution class; `rust-crate-discovery` evaluates candidates before adoption; `rust-dependencies` governs adopted crates.
- `rust-cargo-build` owns build mechanics; `rust-workspace` owns crate topology; `rust-module-layout` owns structure inside a crate.
- `rust-stable` specializes toolchain and general language stability, then hands borrowing, traits, errors, std, unsafe, and examples to their focused owners.
- `rust-performance` requires a metric and comparable baseline; an unmeasured slowdown symptom starts in `debugging`.
- `rust-performance` owns build-time diagnosis and comparable measurements; `rust-cargo-build` owns Cargo profiles, linker, target, wrapper and cache configuration.
- `rust-unsafe` owns Miri/sanitizer interpretation and residual soundness proof; `rust-verify` runs the selected evidence; `debugging` localizes a particular failure.
- `refactoring` preserves a named contract; `rust-architecture` may intentionally change boundaries or contracts after that decision is authorized.
- `rust-coding-rules` is selected after the owning profile. User and project contracts, effective toolchain and target state, and the owner profile override any rulebook recommendation.
- `rust-pin` owns the pinning contract; `rust-unsafe` proves unsafe projection; `rust-concurrency` owns Future cancellation and task lifecycle.
- `rust-concurrency` owns Future/Waker/executor lifecycle; `rust-pin` owns address stability; `debugging` owns hangs, lost wakes and debugger evidence.
- `rust-cargo-build` owns cross-build mechanics; `rust-stable` and `rust-research` establish target/toolchain support; `rust-unsafe-ffi` owns ABI and native-library contracts.
- Security work is split by decision: `rust-architecture` owns threats/trust boundaries, `rust-dependencies` owns advisories and supply policy, `rust-unsafe`/`rust-unsafe-ffi` own soundness and ABI, and `rust-testing` owns fuzz targets.
- Nix profiles own flakes, development environments, packages, and NixOS configuration; `rust-platforms` owns Unix/Windows behavior inside the Rust program.
- `rust-platforms` owns the OS API and native resource lifecycle; `rust-unsafe-ffi` supports raw ABI proofs, and `rust-cargo-build` supports target/linker mechanics.
- `rust-serialization` owns byte format and evolution; `rust-distributed-systems` owns delivery, retries, and cross-node failure after the message contract exists.
- `rust-data` owns access-pattern-driven representation and query execution; `rust-performance` requires comparable measurement rather than activating for every layout change.
- `rust-database` owns generic transactions, migrations, and SurrealDB; `rust-tauri` owns desktop IPC and capabilities, not persistence merely because it is called from a command.
- `rust-tauri` owns Specta-generated command contracts; `rust-serialization` owns a separate actual byte-format decision but does not activate for ordinary typed IPC.
- `rust-gpu` owns device and memory execution; `rust-ml` owns model semantics; `rust-data` owns host data layout; `rust-performance` owns bottleneck measurement.
- `rust-systems-networking` owns the eBPF or DPDK execution environment; `rust-observability`, `rust-unsafe`, and `rust-performance` add telemetry, soundness, and measurement constraints.
- `rust-distributed-systems` owns cross-node failure and consistency; `rust-architecture` owns system boundaries; `rust-concurrency` owns in-process execution.

## Routing Examples

| Request | Decision owner | Additional current profiles | Reason |
|---|---|---|---|
| Fix an E0502 compiler error in a parser | `rust-ownership` | `debugging`, `rust-testing` | Borrow relationship owns the decision; reproduce and guard it. |
| Add a public async client method | `rust-api-design` | `rust-concurrency`, `rust-errors` | Public caller contract owns cancellation and error shape. |
| Upgrade Tokio and remove default features | `rust-dependencies` | `rust-cargo-build`, `rust-concurrency` | Adopted dependency policy owns the graph change. |
| Choose a parser crate | `rust-crate-discovery` | `rust-api-design` | Evaluate current candidates against public coupling. |
| Extract a package from a large module | `rust-workspace` | `refactoring`, `rust-semver` | Crate boundary owns the migration and compatibility cost. |
| Review a lock-free queue diff | `rust-review` | `rust-concurrency`, `rust-unsafe` | Review owns findings; focused profiles supply protocol and soundness rules. |
| Add Swift bindings with UniFFI | `rust-uniffi-building` | `rust-api-design`, `rust-unsafe-ffi` | UniFFI owns generation; API and ABI constrain it. |
| Package a cross-compiled CLI with a flake | `nix-packaging` | `nix-flakes`, `rust-cargo-build` | Derivation owns artifact construction; flake and Cargo supply context. |
| Address twelve mixed review comments | `addressing-findings` | Profiles selected per remediation phase | First normalize and triage; do not load twelve domains at once. |
| Compare async runtimes for a constrained service | `rust-design-protocol` | `rust-concurrency`, `rust-research` | Criteria and domain constraints own the comparison; research supplies dated facts. |
| Build an exact dossier for a resolved crate | `rust-research` | `rust-dependencies` | Cargo package identity and dated docs own the evidence; dependency policy owns later adoption changes. |
| Review unsafe projection in a custom Future | `rust-pin` | `rust-unsafe`, `rust-concurrency` | Pinning owns structural stability; unsafe proves the operation and concurrency owns cancellation. |
| Plan GPU batching for a tensor pipeline | `rust-gpu` | `rust-ml`, `rust-performance` | Device memory and transfer own execution; model semantics and measurement constrain it. |
| Wrap Linux descriptors and Windows handles safely | `rust-platforms` | `rust-unsafe-ffi`, `rust-testing` | OS lifecycle and capability behavior own the API; ABI and regression evidence support it. |
| Configure a NixOS service for an existing Rust daemon | `nixos` | `nix-packaging`, `rust-cargo-build` | Declarative service configuration owns the task; no Rust OS-API behavior is changing. |
| Version a bounded Protobuf message over a stream | `rust-serialization` | `rust-distributed-systems`, `rust-testing` | Field evolution and framing own the byte contract; delivery and malformed-input evidence constrain it. |
| Choose ECS storage for frequently changing components | `rust-data` | `rust-performance`, `rust-architecture` | Access patterns and structural changes own representation; measurement and system boundaries support it. |
| Add a SurrealDB migration to a Tauri application | `rust-database` | `rust-tauri`, `rust-testing` | Transaction and schema lifecycle own the phase; desktop lifecycle and migration evidence constrain it. |
| Expose typed Tauri 2 commands with Specta | `rust-tauri` | `rust-api-design`, `rust-testing` | IPC trust boundary and generated TypeScript contract own the change. |
| Diagnose an XDP verifier rejection | `rust-systems-networking` | `rust-observability`, `rust-unsafe` | eBPF program type and verifier own acceptance; telemetry and layout proofs support it. |
| Add retries to an at-least-once consumer | `rust-distributed-systems` | `rust-errors`, `rust-observability` | Cross-node uncertainty owns idempotency and aggregate retry budget. |
| Investigate a slow incremental Rust build | `rust-performance` | `rust-cargo-build`, `rust-research` | Timings and invalidation own diagnosis; Cargo owns effective config and research verifies version-sensitive backend/cache facts. |
| Run Miri after changing a raw-buffer wrapper | `rust-unsafe` | `rust-verify`, `debugging` | The unsafe proof owns meaning; verification runs supported paths and debugging localizes a finding. |
| Cross-compile a C-linked CLI for ARM Linux | `rust-cargo-build` | `rust-unsafe-ffi`, `rust-research` | Cargo owns target/linker mechanics, FFI owns native ABI and research confirms current target/tool support. |
| Profile an AF_XDP packet loop | `rust-systems-networking` | `rust-performance`, `rust-unsafe` | UMEM/ring ownership controls execution; measurement and buffer soundness constrain it. |
| Generate a service from a reviewed local template | `rust-cargo-build` | `rust-workspace`, `rust-research` | Generator effects and Cargo integration own the operation; template version and topology constrain it. |
| Configure nextest groups for database tests | `rust-testing` | `rust-verify`, `debugging` | Test-resource policy owns grouping; verification runs it and debugging handles unexplained flakes. |
| Establish an LLVM line-coverage regression gate | `rust-testing` | `rust-verify`, `rust-research` | Test adequacy and threshold scope own the gate; execution and version facts support it. |
| Review a cargo-machete candidate used by generated code | `rust-dependencies` | `rust-cargo-build`, `rust-verify` | Dependency ownership decides removal; build/generated paths explain the heuristic false positive. |
| Stop duplicate builds across three Git worktrees | `rust-cargo-build` | `rust-performance`, `rust-verify` | Isolated directory/cache mechanics own the design; measurements decide whether optimization helps. |
| Add workspace Clippy priorities and one disallowed API | `rust-style-clippy` | `rust-stable`, `rust-review` | Lint policy owns configuration; toolchain support and semantic boundary review constrain it. |

These examples show search candidates, not a fixed stack size. Classify every additional profile as coding, triggered helper, deferred, or a separate decision owner under the canonical contract. When no profile clearly owns the request, `rust-workflow` must keep generic repository rules, state the missing decision, and avoid inventing a new profile during the task.

For compiler diagnostics, the retained [Design protocol error-code index](./compiler-error-routing.md)
is a quick entry-signal map. Confirm the full diagnostic and affected construct
before routing; its source "common fixes" are hypotheses, not defaults.

## Specialized topic map

Read only the family reference that matches the current decision. `owner` means the profile owns one decision unit; `helper` means it contributes bounded evidence after a trigger.

- [`rust-skill`](./skill-authoring.md) — owner; Problem-first classification, uncertainty reduction, owner selection, coding constraints, and verification handoff.
- [`rust-skill-index`](./skill-routing.md) — owner; Precise symptom-to-profile lookup, negative routing, manual invocation, and escalation from mechanics to design or domain reasoning.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return each decision to its owner after coding constraints or helper evidence have been stated.
