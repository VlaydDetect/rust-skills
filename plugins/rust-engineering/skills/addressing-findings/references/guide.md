# Addressing Findings Field Guide

This guide is the detailed policy for `addressing-findings`. It synthesizes the craft finding-resolution workflow, Rust-specific correction guidance, and the shared review and verification contracts; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- A finding is a claim plus a premise, impact, location, and closure condition; prose without those parts is not yet actionable.
- Normalization prevents two reviewers from creating two fixes for the same root cause.
- Triage is a decision record: accept, reject, defer, needs-decision, and conflict are distinct outcomes.
- Ordering matters when safety issues, API changes, generated artifacts, and tests depend on earlier corrections.
- Fresh re-review reduces confirmation bias and catches defects introduced while addressing the original issue.
- Closure evidence should be proportionate: a targeted test, compiler error disappearance, API diff, benchmark, or documented decision.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Finding premise reproduces | Accept and define closure evidence | A confirmed path is more useful than debating wording |
| Premise is false in current code | Reject with opened-code evidence | A status without counter-evidence is not auditable |
| Correct behavior depends on product policy | Needs-decision | Engineering must not silently choose business semantics |
| Several findings share one cause | One root fix with linked IDs | Avoids inconsistent guards and duplicated work |
| Fix is valid but intentionally later | Defer with owner and trigger | Deferred is visible debt, not closure |

## Common Failure Modes

- Applying every suggestion mechanically even when findings contradict repository contracts.
- Closing an item because code changed without checking the stated failure path.
- Losing reviewer context by renumbering or paraphrasing findings beyond recognition.
- Running one broad test command and attributing unrelated failures to the fix.
- Letting the same agent both implement and provide the only re-review when independence is practical.

## Required Evidence

- A ledger containing stable ID, decision, rationale, changed locations, verification record, and residual risk.
- For rejected items, a direct counterexample from code, configuration, tests, or an authoritative contract.
- For accepted items, a smallest sufficient check tied to the original closure condition.
- A final diff review that accounts for interactions between findings and preserves unrelated user work.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.
