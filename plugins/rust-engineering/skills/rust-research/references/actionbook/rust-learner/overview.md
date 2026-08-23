# Rust and crate research protocol

> Adapted from Actionbook `rust-learner`. Current facts use primary sources and dated evidence. Actionbook MCP selectors, agent-browser, and background agents are optional host capabilities, not dependencies or mandatory tool order.

## Route the question

| Question | Research branch | Primary evidence |
|---|---|---|
| Current Rust/Cargo/Edition or a release change | Rust release | Rust Blog and official release notes |
| Standard-library item | Std | `doc.rust-lang.org` for the applicable toolchain |
| Clippy lint | Clippy | Stable Clippy lint documentation and project lint config |
| Resolved dependency in this project | Crate | locked offline Cargo metadata plus exact-version docs/source |
| New crate candidate | Crate discovery | current registry/docs/repository facts, then `rust-crate-discovery` |

Do not browse for facts already fixed by a local toolchain or lockfile unless the user asks for current upstream information.

## Rust release research

1. Read `rust-toolchain*`, `rust-version`, edition, CI, and installed `rustc`/Cargo first.
2. If current upstream facts matter, consult the official Rust release list and release notes.
3. Separate language, compiler, standard library, Cargo, Clippy, target, compatibility, and migration changes.
4. Record stabilization version for every API recommended beyond the project's MSRV.
5. Prefer a compatible fallback when the project cannot raise MSRV.

Output: requested/current version, release date, relevant changes, MSRV impact, migration/lint impact, primary links, retrieved date, confidence, and gaps.

## Exact crate research

1. Resolve the package through `cargo metadata --format-version 1 --locked --offline`.
2. Distinguish dependency alias from package name and require exact package ID when versions repeat.
3. Read version-specific docs.rs, declared repository/source, and crates.io metadata as needed.
4. Record resolved features, target conditions, dependency kind, source, edition, and MSRV.
5. Confirm APIs against the selected version; mark `/latest/` or main-branch material as non-authoritative for the lockfile package.

Output:

```text
package_id; alias; version; source; resolved_features; target_conditions;
edition; MSRV; important APIs; safety/migration notes; evidence; confidence; gaps
```

Crate popularity, download count, or recommendation sites may help discovery but do not prove correctness, maintenance, license compatibility, or suitability.

## Standard library and Clippy

- Match docs to the target toolchain where possible.
- Include the exact item or lint path and availability.
- For a lint, report default level, lint group, MSRV/toolchain relevance, false-positive or intentional-exception context, and the project's current configuration.
- Do not turn a Clippy suggestion into policy without checking semantics and repository conventions.

## Agent use

The optional `rust-researcher` agent can gather one bounded set of current facts while the main agent continues local work. Supply a specific question, source scope, time horizon, target package/toolchain, and expected evidence record. The agent is read-only and cannot install tools, update lockfiles, generate dossiers, or edit documentation.

Retry one alternative authoritative source on a fetch failure, then report the gap. Do not loop, guess versions, or hide a documentation/version mismatch.
