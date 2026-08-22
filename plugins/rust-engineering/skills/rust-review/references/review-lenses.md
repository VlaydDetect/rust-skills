# Review lenses

Use only lenses intersecting the change.

| Lens | Inspect |
|---|---|
| Correctness | Inputs, invariants, state transitions, boundary values, error paths, resource cleanup, serialization, and regression tests. |
| Ownership and errors | Semantic ownership, accidental clones, borrow duration, panic reachability, error classification, context, and sensitive detail. |
| Public API and SemVer | Public types, bounds, auto traits, errors, features, MSRV, wire formats, macros, docs, and downstream callers. |
| Concurrency | Cancellation, deadlocks, lock scope, blocking in async, queue bounds, ordering, shutdown, atomics, and race-oriented tests. |
| Unsafe and FFI | Safety preconditions, aliasing, lifetime, layout, provenance, ABI, unwinding, allocation ownership, callbacks, and safe wrappers. |
| Cargo and supply chain | Workspace inheritance, target and feature graph, build scripts, new dependencies, license, advisories, lockfile, and mutually exclusive features. |
| Cross-platform and Nix | `cfg` coverage, target linker/runtime assumptions, packaging inputs, reproducibility, option merge behavior, and secret handling. |
| Performance and ML | Measurement comparability, dominant cost, allocations and copies, algorithmic complexity, shapes, dtype, device, determinism, and tolerance. |
| Observability | Event semantics, cardinality, redaction, propagation, sampling, failure visibility, and flush on shutdown. |
| Tests and documentation | Changed behavior coverage, deterministic assertions, realistic boundary tests, doctests, safety docs, examples, and CI parity. |
| Architecture | Dependency direction, cycles, layer leaks, invariant ownership, cohesion, needless indirection, and migration blast radius. |

For each proposed finding, ask: which exact input or interleaving triggers it, which opened code establishes that premise, what observable impact follows, and which check would disprove it?

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-review/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.
