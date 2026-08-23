# Design protocol research-agent lenses

The product exposes one read-only `rust-researcher` role. Load only the source lens matching its bounded question:

- [Exact crate metadata](./lenses/crate-researcher.md)
- [Version-specific third-party docs](./lenses/docs-researcher.md)
- [Standard-library docs](./lenses/std-docs-researcher.md)
- [Clippy lint docs](./lenses/clippy-researcher.md)
- [Rust release changes](./news/rust-changelog.md)
- [Rust news aggregation](./news/rust-daily-reporter.md)
- [Host-neutral fetch strategy](./lenses/fetch-strategy.md)
- [Evidence freshness record](./dossiers/docs-cache.md)

These are lenses, not separately registered agents. The main agent supplies one question, exact toolchain/package/time range, source scope, and expected evidence record. The researcher never edits, installs, changes lockfiles, or writes dossiers.
