---
name: rust-coding-rules
description: Select and apply concrete, addressable Rust coding rules from a 265-rule, 26-category rulebook after a workflow or domain profile establishes the real decision context. Use for direct rule ID or prefix lookup, focused implementation guidance, post-diff checks, and evidence-backed Rust review. Do not use as a second orchestrator, a primary profile, a verification-only workflow, or a blanket checklist.
---

# Rust Coding Rules

Use this skill as a progressive-disclosure reference overlay. It supplies detailed decisions, algorithms, exceptions, examples, and verification prompts; `rust-workflow`, `rust-review`, or a focused domain profile still owns scope and engineering judgment.

## Precedence and Scope

Apply rules in this order:

1. Explicit user requirements and path-scoped repository instructions.
2. Actual project contracts, callers, edition, MSRV, toolchain, target, features, dependencies, runtime, and measured workload.
3. The selected primary profile and its supporting constraints.
4. This rulebook.

The rulebook does not consume a primary or supporting profile slot and never grants permission to add a dependency, change a public contract, enable nightly, weaken safety, or perform an optimization. `rust-workflow` remains the only writer in an implementation workflow. `rust-review` remains read-only. `rust-verify` executes an already selected evidence matrix and does not load this rulebook automatically.

## Build a RuleQuery

Record only facts that affect selection:

- explicit selector: exact rule ID, prefix, or task description;
- changed constructs, symbols, callers, and boundary;
- selected primary profile;
- public, private, unsafe, or foreign-ABI surface;
- edition, MSRV, toolchain, target, and portability requirements;
- accepted features, dependencies, and runtime;
- measured hot path or resource constraint, if any;
- phase: design, implementation, post-diff, or review.

Unknown facts stay unknown. A crate name, keyword, or hypothetical future use is not enough to activate a rule.

## Select and Apply Rules

1. For an exact ID, open `references/rules/<id>.md`. Alias files remain addressable and route to their canonical rule.
2. For a prefix or task, read [Rule routing](references/routing.md), then only the matching [category index](references/categories/).
3. Select at most eight rules for a normal phase. Give one concrete reason for every selected ID and omit rules whose premise is not established.
4. Read each selected rule fully, including `Apply When`, `Avoid When`, prerequisites, source guidance, trade-offs, and verification.
5. Resolve conflicts using the precedence above. Conditional rules require their stated dependency, measurement, target, runtime, or compatibility premise.
6. Return a compact `RuleSet`: selected IDs and reasons, prerequisites or conflicts, and deferred categories or batches.
7. During implementation, re-run selection against the actual diff. During review, cite a rule ID only after opened code proves the trigger and impact.

For a broad audit, batch one category at a time in groups of no more than eight rules. Do not load all 265 rules into one context.

## Dependency and Optimization Guardrails

Tokio, Serde, anyhow, thiserror, tracing, rayon, SmallVec, loom, test frameworks, and every other external crate in examples are options only when already accepted or separately approved. Prefer project-native and standard-library facilities when they satisfy the contract.

LTO, codegen-unit changes, `target-cpu=native`, `panic=abort`, RwLock, boxing, arenas, compact integers, custom hashers, SIMD, PGO, and similar choices require representative evidence plus portability and correctness review. They are never global defaults from this skill.

## Direct Invocation

- Codex: `$rust-coding-rules <id|prefix|task>`
- Claude Code: `/rust-engineering:rust-coding-rules <id|prefix|task>`

Use [Rule routing](references/routing.md) for task and prefix selection. Category indexes link every one of the 265 source IDs to a full or alias rule file. For Actionbook's summarized coding guidance and legacy `/guideline` command, consult the [one-to-one crosswalk](references/actionbook/coding-guidelines/crosswalk.md) rather than creating duplicate rules.
