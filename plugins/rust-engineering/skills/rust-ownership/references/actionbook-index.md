# Actionbook ownership protocol

Load only the branch that matches the controlling decision. These references preserve the source algorithms and examples; `rust-ownership` remains the owner and current project state overrides generic examples.

## Ownership and lifetimes

- [Core ownership questions](actionbook/m01-ownership/overview.md)
- [Cross-language ownership comparison](actionbook/m01-ownership/comparison.md)
- [Ownership best practices](actionbook/m01-ownership/examples/best-practices.md)
- [Compiler-error patterns](actionbook/m01-ownership/patterns/common-errors.md)
- [Lifetime patterns](actionbook/m01-ownership/patterns/lifetime-patterns.md)

Start here for moves, borrows, escaping references, lifetime relationships, or repeated clone-based fixes. Trace upward only when the local ownership graph exposes a design or domain mismatch.

## Resource topology

- [Resource-management protocol](actionbook/m02-resource/overview.md)

Use this for `Box`, `Rc`, `Arc`, `Weak`, RAII, cycles, and drop ownership. Select from the actual single-thread, cross-thread, uniqueness, and lifecycle requirements.

## Mutability

- [Mutability protocol](actionbook/m03-mutability/overview.md)

Use this for exclusive borrows, interior mutability, lock-backed mutation, and the question of whether mutation belongs at the current layer. No lock or cell type is a default independent of topology.

## Resource lifecycle

- [Lifecycle, guards, cleanup, and initialization](actionbook/m12-lifecycle/overview.md)

Use this when acquisition, error, cancellation, shutdown, and drop paths must form one coherent resource protocol.
