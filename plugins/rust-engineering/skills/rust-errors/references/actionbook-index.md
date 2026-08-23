# Actionbook error protocol

- [Error-handling decision model](actionbook/m06-error-handling/overview.md)
- [Application versus library examples](actionbook/m06-error-handling/examples/library-vs-app.md)
- [Detailed error patterns](actionbook/m06-error-handling/patterns/error-patterns.md)

Use these references to trace from a local `Result`, `Option`, panic, or propagation question to caller-visible recovery and domain semantics. Preserve source chains and context at boundaries. Do not turn `expect`, `unwrap`, `anyhow`, or `thiserror` into a universal preference.

## Domain recovery

- [Domain-error classification and recovery](actionbook/m13-domain-error/overview.md)

Load this branch only when transient/permanent classification, retries, fallbacks, degradation, or user-visible codes are part of a confirmed product contract.
