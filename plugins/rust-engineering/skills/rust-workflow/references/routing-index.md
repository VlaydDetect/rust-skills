# Profile Routing Index

Select one **primary** profile that owns the decision and at most two **supporting** profiles that supply constraints. If more than three profiles are necessary, split the task into phases and re-route at each phase. Loading every relevant-looking profile weakens ownership and wastes context.

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
| `rust-coding-rules` | Addressable concrete rules selected after an owner profile | An exact rule ID or prefix is requested, or workflow/review needs a RuleSet of at most eight context-matched rules. It never occupies a primary or supporting slot. |

## Engineering Process

| Profile | Owns | Route here when |
|---|---|---|
| `addressing-findings` | Stable finding ledger, triage, ordered fixes, closure, fresh re-review | Findings already exist and must be accepted, rejected, deferred, fixed, and closed. |
| `codebase-onboarding` | First broad project map | The repository or affected subsystem is unfamiliar. |
| `debugging` | Reproduction, hypothesis, isolation, root cause | A compiler, test, runtime, timing, or integration failure is unexplained. |
| `refactoring` | Structural change under a preserved contract | Behavior should stay stable while code moves, splits, or simplifies. |
| `rust-navigation` | Bounded symbol, dispatch, cfg, macro, and call-path tracing | The project is known but the real definition, caller, impl, or effect path is not. |
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
| `rust-unsafe` | Internal unsafe invariants, raw memory, validity, aliasing, layout, Miri | Unsafe is internal to Rust and does not cross a foreign ABI. |

## Project, Cargo, and Public Contract

| Profile | Owns | Route here when |
|---|---|---|
| `rust-api-design` | Caller-visible Rust contract, visibility, ownership, extension policy | A public or independently evolving Rust API is added or changed. |
| `rust-cargo-build` | Effective Cargo state, targets, features, config, profiles, build scripts | Cargo mechanics determine behavior. |
| `rust-workspace` | Crate boundaries, workspace policy, shared metadata, release relationships | The design unit is packages and their dependency direction. |
| `rust-module-layout` | In-crate modules, files, visibility, re-exports, tests | The design unit is structure inside one crate. |
| `rust-dependencies` | Adopted dependency versions, features, sources, audit, licenses, removal | A dependency already exists or adoption has been approved. |
| `rust-crate-discovery` | Pre-adoption candidate research and build-versus-buy decision | A new external crate is being considered. |
| `rust-semver` | Released compatibility, baseline comparison, deprecation, migration | Downstream breakage or release classification is at issue. |
| `rust-documentation` | Rustdoc, doctests, examples, README, changelog, migration docs | The developer-facing contract or discoverability changes. |
| `rust-style-clippy` | rustfmt, Clippy, lint levels and exceptions | Formatting or lint tooling is the controlling issue. |
| `rust-ecosystem` | Broad project shape and solution class before candidate selection | A new project or subsystem needs high-level Rust orientation. |

## Architecture

| Profile | Owns | Route here when |
|---|---|---|
| `rust-architecture` | New system boundaries, dependency direction, ports and adapters, CQRS or events | The task designs intended architecture. |
| `rust-architecture-review` | Read-only whole-project structural health | The task audits existing architecture rather than a bounded diff. |

## Runtime, Interop, and Specialized Systems

| Profile | Owns | Route here when |
|---|---|---|
| `rust-concurrency` | Threads, async, channels, locks, atomics, cancellation, backpressure, shutdown | Correctness or liveness spans execution contexts. |
| `rust-testing` | Test design and implementation across test techniques | The primary deliverable is new or improved tests. |
| `rust-performance` | Reproducible benchmarks, profiles, optimization, regression guards | A measured metric or regression controls the work. |
| `rust-observability` | Structured logs, spans, metrics, correlation, redaction, cardinality | Runtime behavior must become operationally diagnosable. |
| `rust-unsafe-ffi` | Foreign ABI, layout, handles, buffers, strings, callbacks, unwind | Unsafe crosses a language or runtime boundary. |
| `rust-macros` | Declarative and procedural macro syntax, expansion, diagnostics, compile cost | Compile-time Rust token generation is necessary. |
| `rust-lombok-macros` | Lombok-style generated builders, accessors, constructors, validation | The request specifically concerns annotation-driven boilerplate APIs. |
| `rust-uniffi-building` | UniFFI UDL or proc-macro interfaces, scaffolding, bindings, packaging | UniFFI exposes Rust to supported foreign languages. |
| `rust-ml` | Models, tensors, preprocessing, devices, inference, batching, serving | ML pipeline semantics control the Rust system. |

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
- `rust-review` reviews a bounded diff; `rust-architecture-review` assesses whole-project structure; `nix-review` owns Nix-specific findings.
- `rust-unsafe` owns Rust-internal validity and aliasing; `rust-unsafe-ffi` adds ABI and foreign lifecycle; `rust-uniffi-building` owns the UniFFI generation workflow.
- `rust-idioms` owns semantic patterns; `rust-style-clippy` owns formatter and lint policy; `rust-api-design` owns public caller contracts.
- `rust-ecosystem` chooses a broad solution class; `rust-crate-discovery` evaluates candidates before adoption; `rust-dependencies` governs adopted crates.
- `rust-cargo-build` owns build mechanics; `rust-workspace` owns crate topology; `rust-module-layout` owns structure inside a crate.
- `rust-stable` specializes toolchain and general language stability, then hands borrowing, traits, errors, std, unsafe, and examples to their focused owners.
- `rust-performance` requires a metric and comparable baseline; an unmeasured slowdown symptom starts in `debugging`.
- `refactoring` preserves a named contract; `rust-architecture` may intentionally change boundaries or contracts after that decision is authorized.
- `rust-coding-rules` is selected after the owning profile. User and project contracts, effective toolchain and target state, and the owner profile override any rulebook recommendation.

## Routing Examples

| Request | Primary | Supporting | Reason |
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

When no profile clearly owns the request, `rust-workflow` must keep generic repository rules, state the missing decision, and avoid inventing a new profile during the task.
