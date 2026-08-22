# lint-workspace-lints

> Configure lints at workspace level for consistent enforcement

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-style-clippy; supporters=`rust-stable`, `rust-cargo-build`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Configure lints at workspace level for consistent enforcement.

## Apply When

Apply when the repository needs a scoped formatting, lint, warning-level, cfg, or CI policy under its actual toolchain, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when a broad lint group or automatic fix would change API, MSRV, semantics, generated code, or unrelated dirty files. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Reproduce the exact lint, classify it, fix semantic causes individually, and use the narrowest documented allow for intentional exceptions.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Stricter lint policy catches defects earlier but increases toolchain churn, exception maintenance, and migration work.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.

## Verification

Run the configured format and Clippy gate with exact packages, targets, features, and toolchain; separate baseline failures.

## Why It Matters

Without centralized lint configuration, each crate develops its own standards (or none). Workspace-level lints (Rust 1.74+) ensure consistent code quality across all crates. Denied lints catch issues in CI before they reach production.

## Bad

```toml
# crate-a/Cargo.toml - strict
[lints.clippy]
unwrap_used = "deny"

# crate-b/Cargo.toml - lenient
# No lint config

# crate-c/Cargo.toml - different
[lints.clippy]
unwrap_used = "warn"

# Inconsistent enforcement, some issues slip through
```

## Good

```toml
# Root Cargo.toml
[workspace.lints.rust]
unsafe_code = "deny"
missing_docs = "warn"

[workspace.lints.clippy]
# Correctness
unwrap_used = "deny"
expect_used = "warn"
panic = "deny"

# Style
needless_pass_by_value = "warn"
redundant_clone = "warn"

# Complexity
cognitive_complexity = "warn"

[workspace.lints.rustdoc]
broken_intra_doc_links = "deny"

# crate-a/Cargo.toml
[lints]
workspace = true

# crate-b/Cargo.toml
[lints]
workspace = true
```

## Recommended Lint Configuration

```toml
# Root Cargo.toml
[workspace.lints.rust]
# Safety
unsafe_code = "deny"
missing_debug_implementations = "warn"

# Quality
unused_results = "warn"
unused_qualifications = "warn"

[workspace.lints.clippy]
# === Correctness (deny) ===
correctness = { level = "deny", priority = -1 }

# === Suspicious (deny) ===
suspicious = { level = "deny", priority = -1 }

# === Style (warn) ===
style = { level = "warn", priority = -1 }

# === Complexity (warn) ===
complexity = { level = "warn", priority = -1 }

# === Perf (warn) ===
perf = { level = "warn", priority = -1 }

# === Pedantic (selective) ===
# Not all pedantic lints are useful
doc_markdown = "warn"
needless_pass_by_value = "warn"
redundant_closure_for_method_calls = "warn"
semicolon_if_nothing_returned = "warn"

# === Nursery (selective) ===
cognitive_complexity = "warn"
useless_let_if_seq = "warn"

# === Restriction (selective) ===
unwrap_used = "deny"
expect_used = "warn"
dbg_macro = "warn"
print_stdout = "warn"  # Use logging instead
todo = "warn"

[workspace.lints.rustdoc]
broken_intra_doc_links = "deny"
private_intra_doc_links = "warn"
```

## Per-Crate Overrides

```toml
# crate-with-binary/Cargo.toml
[lints]
workspace = true

# Binary entry point can use unwrap
[lints.clippy]
unwrap_used = "allow"

# test-utils/Cargo.toml
[lints]
workspace = true

# Test utilities can print
[lints.clippy]
print_stdout = "allow"
```

## CI Integration

```yaml
# .github/workflows/ci.yml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy
      
      - name: Clippy
        run: cargo clippy --workspace --all-targets -- -D warnings
      
      - name: Rustdoc
        run: RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps
```

## Lint Categories

```toml
# Category-level configuration
[workspace.lints.clippy]
# All lints in category at once
correctness = { level = "deny", priority = -1 }
suspicious = { level = "deny", priority = -1 }
style = { level = "warn", priority = -1 }
complexity = { level = "warn", priority = -1 }
perf = { level = "warn", priority = -1 }
pedantic = { level = "warn", priority = -1 }

# Then override specific lints (higher priority)
missing_errors_doc = "allow"  # Override pedantic
```

## Related Rules
- [lint-deny-correctness](./lint-deny-correctness.md) - Critical lints
- [proj-workspace-deps](./proj-workspace-deps.md) - Workspace configuration
- [anti-unwrap-abuse](./anti-unwrap-abuse.md) - unwrap lints
