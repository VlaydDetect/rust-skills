# Actionbook research-agent lenses

The product exposes one read-only `rust-researcher` role. Load only the source lens matching its bounded question:

- [Exact crate metadata](actionbook/agents/crate-researcher.md)
- [Version-specific third-party docs](actionbook/agents/docs-researcher.md)
- [Standard-library docs](actionbook/agents/std-docs-researcher.md)
- [Clippy lint docs](actionbook/agents/clippy-researcher.md)
- [Rust release changes](actionbook/agents/rust-changelog.md)
- [Rust news aggregation](actionbook/agents/rust-daily-reporter.md)
- [Host-neutral fetch strategy](actionbook/agents/_shared/fetch-strategy.md)
- [Evidence freshness record](actionbook/agents/docs-cache.md)

These are lenses, not separately registered agents. The main agent supplies one question, exact toolchain/package/time range, source scope, and expected evidence record. The researcher never edits, installs, changes lockfiles, or writes dossiers.
