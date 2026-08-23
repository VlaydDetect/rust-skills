# Host-neutral fetch strategy

Use the simplest available tool that can read the authoritative source. The plugin has no browser, crawler, MCP, Docker, or login dependency.

## Source before transport

1. Prefer project-local toolchain, lockfile, source, and generated rustdoc for fixed facts.
2. For current Rust facts, use official Rust documentation and release sources.
3. For an exact crate, use Cargo metadata, exact-version docs.rs, the declared repository, and crates.io metadata.
4. Use community aggregation only for discovery and follow important claims to their primary source.

## Transport

- Use the host's normal web access when current external evidence is required.
- Use an already available signed-in browser only when a page genuinely requires it.
- Do not install or require agent-browser, crawl4ai, Chrome automation, or an MCP server.
- Retry one alternate access method, then record the failure and continue with available evidence.

## Validation

Check the canonical URL, requested version/date, non-error content, source authority, retrieval time, and any mismatch with the target toolchain or lockfile. Never turn a search snippet, selector output, or stale cached page into an API fact.
