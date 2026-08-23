---
name: rust-stable
description: Select editions, MSRV, stable versus nightly features, language semantics, and compatibility tactics for production Rust. Use for general Rust questions whose controlling issue is toolchain or language stability; delegate focused ownership, trait, error, standard-library, or example work.
---

# Stable Rust

Own toolchain-aware language guidance, edition behavior, MSRV, and stable or nightly boundaries. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A language feature, edition change, compiler version, unstable feature gate, or MSRV policy controls the solution.
- Code must work across supported Rust versions or avoid nightly-only APIs.
- A general Rust design question needs routing to a more specific language profile.

## Workflow

1. Inspect `rust-toolchain*`, Cargo manifests, CI matrices, `rust-version`, and repository instructions before recommending syntax or APIs.
2. Identify whether the issue is edition semantics, compiler availability, library stabilization, platform support, or a separate ownership or trait problem.
3. Choose the oldest supported toolchain as the compatibility floor and the effective CI toolchain as evidence, noting mismatches.
4. Prefer stable language and standard-library capabilities; justify nightly by an explicit product or build requirement.
5. For edition or MSRV changes, inventory packages, dependencies, generated code, docs, examples, and release compatibility.
6. Specify the minimal compile and test matrix that proves the selected toolchain policy.

## Decision Rules

- Do not assume the current global `rustc` is the repository's toolchain.
- Edition and compiler version are related but different: edition opt-in changes parsing and migration rules, while APIs stabilize by release.
- `rust-version` is a consumer contract; raising it can be breaking even when source API is unchanged.
- Nightly features require a reason, a pinning policy, and a failure plan for compiler churn.
- Avoid suggesting APIs stabilized after the declared MSRV without a fallback or policy change.
- Use edition migration tooling as assistance, then review semantic and macro changes.
- Route detailed borrowing, trait dispatch, error design, unsafe, or standard-library selection to their owner profiles.
- Do not claim cross-target support from host-only compilation.

## Rulebook Overlay

After establishing edition and MSRV, use relevant [`const-`](../rust-coding-rules/references/categories/const.md) rules and toolchain-sensitive entries in [`proj-`](../rust-coding-rules/references/categories/proj.md) or [`lint-`](../rust-coding-rules/references/categories/lint.md). Source-version claims never override the repository's compiler floor.

## Boundaries and Hand-offs

- `rust-ownership`, `rust-traits`, `rust-errors`, `rust-unsafe`, and `rust-stdlib` own their detailed language domains.
- `rust-cargo-build` owns Cargo mechanics and `rust-semver` owns release compatibility beyond the MSRV facet.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Stable Rust field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.

## Huiali protocols

For source-derived detail relevant to this profile, read the [Huiali integration index](references/huiali-index.md) and load only the matching family reference.
