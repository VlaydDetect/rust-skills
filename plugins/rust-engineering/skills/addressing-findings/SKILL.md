---
name: addressing-findings
description: Resolve review, audit, CI, and user findings through explicit triage, ordered fixes, targeted verification, and fresh re-review. Use when findings already exist and must be accepted, rejected, deferred, clarified, or implemented. Do not use to perform the initial review.
---

# Addressing Findings

Own the lifecycle from an existing finding to a defensible closure decision. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A review, audit, CI report, issue list, or user feedback contains actionable findings.
- Several findings overlap, conflict, depend on one another, or need severity triage.
- The task is to fix accepted findings and prove that the review loop is closed.

## Workflow

1. Collect every finding with its source, location, severity, claimed impact, and available evidence; assign a stable ID.
2. Normalize duplicates and split compound findings so each ID has one testable claim.
3. Classify each item as accept, reject, defer, needs-decision, or conflict; record a reason instead of silently dropping it.
4. Order accepted work by safety, prerequisite, shared root cause, and blast radius; fix the common cause once when multiple findings share it.
5. Verify each accepted item against its closure condition, then request a fresh read-only review of the resulting diff rather than relying on the original reviewer state.
6. Publish a closure ledger containing status, evidence, residual risk, and any owner or deadline for deferred work.

## Decision Rules

- Never treat severity as proof; confirm the premise in the current code and configuration.
- Reject a finding only with counter-evidence that addresses its exact failure path.
- Do not mix a product decision with an implementation defect; route unresolved policy to the user or owner.
- Preserve the finding ID across commits and re-reviews so discussion remains traceable.
- If a fix invalidates another finding, update both records and explain the dependency.
- A compile pass does not close a behavioral finding unless compilation was the stated contract.
- Mark environmental and pre-existing failures separately; neither automatically excuses a regression.
- Do not close deferred items as fixed, and do not invent a deadline the repository has not committed to.

## Boundaries and Hand-offs

- Initial diff or architecture assessment belongs to `rust-review`; this profile begins with a supplied finding set.
- Domain-specific implementation decisions belong to the relevant Rust or Nix profile selected by `rust-workflow`.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Addressing Findings field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
