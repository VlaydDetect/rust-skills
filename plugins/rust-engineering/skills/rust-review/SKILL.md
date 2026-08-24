---
name: rust-review
description: Perform a read-only findings-first review of a Rust or mixed Rust and Nix diff, pull request, or bounded change. Ground premises in current code, select focused domain profiles, control false positives, rank confirmed impact, and return a verdict. Do not implement fixes or use this as a whole-project architecture audit.
---

# Rust Review

Judge the change in its real call paths, not in diff isolation. Do not edit files.

## Workflow

1. Establish scope: base or diff, packages, declared intent, acceptance criteria, and repository instructions.
2. Inspect callers, implementations, tests, CI, manifests, feature gates, generated boundaries, and relevant external contracts.
3. Review one decision-unit slice at a time: its owner, changed constructs, relevant coding profiles, acceptance evidence, and callers from the workflow [ProfileStack contract](../rust-workflow/references/profile-stack.md). Use only the affected lenses from [Review lenses](references/review-lenses.md).
4. Build that unit's `RuleQuery` from the real diff and load at most nine matching IDs through `rust-coding-rules`. A rule ID may sharpen a lens but is never evidence by itself.
5. Trace each changed behavior through callers, mirror paths, errors, cleanup, tests, and configuration. Compare premises with the declared intent and actual magnitude rather than reviewing syntax in isolation.
6. For broad independent surfaces, optionally delegate at most two non-overlapping read-only lenses, each bounded to one decision unit. Use the `Finding` schema from `rust-workflow` agent contracts when available.
7. Ground every premise in opened code or command evidence. Attempt to disprove a candidate finding and apply the false-positive exclusions below. Mark unresolved claims `Suspected`; do not promote them to defects.
8. Report findings before summary, ordered by severity. Include a tight location, trigger, impact, supporting rule IDs when applicable, evidence, smallest viable fix, and verification that would close it.
9. Return `PASS`, `WARN`, `FAIL`, or `INCOMPLETE`. `FAIL` requires at least one confirmed blocking defect; `INCOMPLETE` means required evidence was unavailable.

## Finding Policy

- `Critical`: plausible memory safety, remote compromise, irreversible data loss, or equivalent release blocker.
- `High`: confirmed correctness, compatibility, security, deadlock, or major operational failure.
- `Medium`: maintainability or performance defect with concrete impact, weak tests on changed behavior, or risky API design.
- `Low`: local clarity or robustness issue worth fixing but not a merge blocker.

If no actionable findings exist, say so explicitly and list residual risks or untested surfaces. Do not invent findings to fill a report. When the user asks to fix accepted findings, hand their stable IDs and evidence to `rust-workflow`.

## False-Positive Exclusions

- Do not report a hypothetical input, target, feature, or interleaving that the current contract excludes unless the exclusion itself is missing or unsafe.
- Do not report intended behavior merely because an alternative design is preferable.
- Do not report style, naming, or speculative future flexibility as correctness findings.
- Do not report a downstream impact without locating a real caller, public contract, serialized form, ABI, or supported configuration.
- Do not duplicate the compiler or lint message unless the review adds a concrete behavioral or compatibility consequence.
- Keep tool- or environment-dependent claims `Suspected` when the decisive check cannot run.

For whole-project structural health use `rust-architecture-review`; for Nix-specific audits use `nix-review`. Accepted findings move to `addressing-findings` before implementation.

When translating the legacy Design protocol `/rust-review` command, use the
[host-neutral adapter](./references/review-adapter.md); Clippy is one evidence
source, not the definition of code review.

## Specialized Rust protocols

For additional topic detail, read the [Review adapter](./references/review-adapter.md) and load only the relevant section.
