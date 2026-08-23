# Huiali Testing Protocol

> Product adaptation of `skills/rust-testing/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-testing`.
- Supporting profiles when needed: `$rust-verify`.
- Scope retained: Unit, integration, property, compile-fail, concurrency, fuzz and regression strategy with observable failure criteria.
- Baseline correction: Choose test layers from risk and contract. Dependency-specific harnesses and exhaustive matrices are conditional; verification must distinguish compiled fixtures from illustrative fragments.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

# Rust Testing Skill

Use this skill for detailed, production-ready guidance in this Rust domain.

## Core Question

**How do we keep tests deterministic, fast, and meaningful?**

## Solution Patterns

- Use unit tests for logic, integration for contracts
- Use property tests for invariants
- Use loom/criterion for concurrency/perf confidence

## Workflow

1. Reproduce and isolate the issue with a minimal failing case.
2. Choose the smallest safe design that satisfies constraints.
3. Implement with explicit ownership, errors, and boundaries.
4. Verify with tests, linting, and scenario-specific checks.

## Review Checklist

- [ ] Correct behavior for both success and failure paths.
- [ ] Ownership and API boundaries are explicit.
- [ ] Error handling and diagnostics are actionable.
- [ ] Performance-sensitive paths are measured.
- [ ] Regression tests cover the changed behavior.

## Common Pitfalls

- Fixing flakes with sleep
- Over-mocking
- Slow tests in default CI path

## Verification Commands

```bash
cargo test
cargo test -- --nocapture
cargo bench
cargo nextest run
```

## Related Skills

- `rust-concurrency`
- `rust-performance`
- `rust-database`
