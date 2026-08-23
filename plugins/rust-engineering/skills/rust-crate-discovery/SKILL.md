---
name: rust-crate-discovery
description: Evaluate candidate Rust crates before adoption using explicit requirements, maintenance, API fit, MSRV, features, dependencies, security, licensing, platform support, and local proof. Use for crate choice or build-versus-buy decisions.
---

# Rust Crate Discovery

Own evidence-based pre-adoption selection of an external crate or a std or local alternative. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A new external capability may require a crate and candidates need comparison.
- The user asks which crate, library, framework, parser, runtime, database, or tool to use.
- An existing home-grown component might be replaced, but adoption costs and fit are unknown.

## Workflow

1. Write hard requirements and weighted preferences covering API, MSRV, targets, no-std, async runtime, safety, licenses, maintenance, and dependency budget.
2. Check std and already-adopted dependencies first; only then form a short candidate list.
3. Inspect primary evidence: crate metadata, repository, docs, changelog, release cadence, issue posture, features, dependency tree, unsafe and native code, advisories, and license.
4. Score candidates against the same rubric and mark evidence date, uncertainty, and disqualifying constraints.
5. Prototype the top candidate in a minimal local example or narrow repository spike under actual toolchain, features, and target constraints.
6. Recommend adopt, adopt with conditions, defer, or build locally; hand an accepted crate to `rust-dependencies` for ongoing governance.

## Decision Rules

- Do not infer quality from download counts, GitHub stars, or a polished README alone.
- Use current web evidence only when network access is authorized; otherwise state that maintenance and advisory facts are unverified.
- Evaluate the exact feature set and version range the project would use, not the maximal crate showcase.
- Check whether public types would leak the crate and constrain future replacement.
- Account for proc macros, build scripts, C or C++ toolchains, system libraries, code generation, and cross-target support.
- Prefer a small local implementation when requirements are narrow, stable, and cheaper than the dependency lifecycle.
- A proof-of-concept must exercise the risky integration path, not merely compile an import.
- Record rejected candidates and decisive reasons so the search is not repeated without new evidence.

## Boundaries and Hand-offs

- `rust-dependencies` owns version and feature policy after adoption.
- `rust-ecosystem` owns broad solution-class and project bootstrap guidance when no bounded crate decision exists yet.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Crate Discovery field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.

## Specialized Rust protocols

For additional topic detail, read the [Profile reference index](./references/guide.md) and load only the matching family reference.
