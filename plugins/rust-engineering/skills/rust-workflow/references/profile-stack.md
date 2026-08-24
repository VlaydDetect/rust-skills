# ProfileStack Contract

Use this contract for mutating Rust work. Build the stack from the current change slice, not from a broad project plan or a later phase.

## Evidence order

Route in this order:

1. The user's current instruction and path-scoped repository constraints.
2. Symbols, contracts, callers, tests, and configuration actually changed in this phase.
3. Confirmed risks of the current diff.
4. Background plans and future implementations as context only.

A keyword, platform mentioned only in a plan, hypothetical caller, or deferred feature does not activate a profile.

## TaskBrief

Record the following before routing:

```text
requested_now: the deliverable requested in this turn
background_context: relevant existing plan or architecture that does not expand scope
deferred_work: explicitly later work
change_slice: packages, files, symbols, callers, tests, and configuration in this phase
decision_units: independent contracts that need an engineering decision
changed_constructs: Rust types, traits, errors, lifecycles, unsafe blocks, formats, or other mechanics
acceptance: observable behavior plus the test or check that will prove it
risks: confirmed current risks and unresolved evidence
```

`requested_now` and `change_slice` control routing. Put future Direct I/O, async, platform ports, migrations, and similar later work in `deferred_work`; they cannot select an active profile by themselves.

## ProfileStack

```text
decision_units:
  - id: stable phase-local identifier
    owner_profile: exactly one profile
coding_profiles: [profile]
helper_profiles: [profile]
deferred_profiles: [profile]
forbidden_profiles: [profile]
same_phase_reason: optional explanation for multiple owners
coverage:
  decisions: [decision_unit ids]
  constructs:
    - construct: changed Rust construct or invariant
      profile: coding profile, or the owner when it covers the mechanic directly
      reason: why that profile is needed
  acceptance:
    - criterion: acceptance item
      evidence: test, check, inspection, or explicitly unavailable evidence
  gaps: []
```

The stack records one active phase. `rust-workflow`, `rust-review`, `rust-verify`, `rust-architecture-review`, and `nix-review` form the control plane and never appear in profile roles. `rust-coding-rules` is an overlay and never appears in a role.

## Role rules

- **Owner:** one profile owns each decision unit. Co-ownership of one decision is invalid.
- **Coding:** a profile supplies concrete Rust mechanics for a named construct or invariant. From the third coding profile onward, record why the owner plus focused rule IDs are insufficient.
- **Helper:** activate only after an observable trigger, obtain the bounded result, then unload it. `helper_profiles` records helpers activated during the task; it is not a resident context list. A helper may own a task whose deliverable is its normal output, such as a test-only change or root-cause diagnosis.
- **Deferred:** relevant to a later phase but inactive now.
- **Forbidden:** contradicted by the current scope or a negative route.

Default role is only search order. A profile may be promoted or demoted when the current decision requires it.

## Role matrix

| Default class | Profiles |
|---|---|
| Control plane | `rust-workflow`, `rust-review`, `rust-verify`, `rust-architecture-review`, `nix-review` |
| Owner-first | `nix-dev-env`, `nix-flakes`, `nix-packaging`, `nixos`, `rust-api-design`, `rust-architecture`, `rust-cargo-build`, `rust-crate-discovery`, `rust-data`, `rust-database`, `rust-dependencies`, `rust-distributed-systems`, `rust-ecosystem`, `rust-gpu`, `rust-ml`, `rust-module-layout`, `rust-platforms`, `rust-semver`, `rust-serialization`, `rust-systems-networking`, `rust-tauri`, `rust-uniffi-building`, `rust-workspace` |
| Coding-first | `rust-concurrency`, `rust-errors`, `rust-idioms`, `rust-lombok-macros`, `rust-macros`, `rust-ownership`, `rust-pin`, `rust-stable`, `rust-stdlib`, `rust-style-clippy`, `rust-traits`, `rust-unsafe`, `rust-unsafe-ffi` |
| Helper-first | `addressing-findings`, `codebase-onboarding`, `debugging`, `refactoring`, `rust-by-example`, `rust-design-protocol`, `rust-documentation`, `rust-navigation`, `rust-observability`, `rust-performance`, `rust-research`, `rust-testing`, `specs` |
| Overlay | `rust-coding-rules` |

## Circuit breakers

- At most three owners in one phase. A second owner requires a distinct changed contract. A third also requires `same_phase_reason` to explain why splitting would break atomicity.
- At most six coding profiles. Every one must appear in `coverage.constructs`.
- At most ten helper activations per task. Do not pre-load helpers as a quota.
- A fourth owner, seventh coding profile, or eleventh helper requires a phase split and a fresh TaskBrief. Never truncate the needed list to fit a cap.

The `3/6/10` limits are circuit breakers, not targets and not outputs of a complexity score.

## Evidence escalation

Activate a helper only from current evidence:

| Observed trigger | Helper result |
|---|---|
| Unexplained compile, test, runtime, timing, or integration failure | `debugging` returns a reproduction and root cause |
| Current version, crate, tool, target, or upstream behavior controls correctness | `rust-research` returns dated primary evidence |
| A concrete acceptance contract needs test design or implementation | `rust-testing` returns the required test strategy or test change |
| The real definition, caller, dispatch, cfg, or macro path is unknown | `rust-navigation` returns the bounded path |
| A measured metric controls the decision | `rust-performance` returns the baseline and comparison |
| Product behavior is ambiguous | `specs` returns a bounded contract and scenarios |

Do not activate `rust-research` for stable repository facts or `debugging` before a failure exists. Record a helper's result in the TaskBrief or evidence log and remove it from the active working set.

## Pre-edit gate and re-routing

Before editing, require `coverage.gaps` to be empty:

- every decision unit has exactly one owner;
- every significant Rust construct is covered by a coding profile or explicitly by its owner;
- every acceptance criterion names a test or check;
- deferred and forbidden profiles are absent from active roles.

Re-route after discovery changes `change_slice`, after a helper reveals a new decision, when an owner changes, when a circuit breaker is crossed, or when the current phase finishes. Reviewers, verifiers, scouts, and researchers receive only one decision-unit slice; the main agent remains the sole writer and integrates all results.
