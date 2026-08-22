# Executable Specifications Field Guide

This guide is the detailed policy for `specs`. It synthesizes the craft specifications workflow and its scenario-writing guidance, adapted to Rust API and test contracts; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- A robust artifact triple is normative rules, concrete examples, and executable acceptance scenarios.
- Given names relevant state, When names one event or action, Then names externally observable outcomes.
- Examples expose ambiguities in equality, ordering, defaults, limits, and error handling that abstract prose hides.
- Implementation plans may change without changing the specification; mixing them makes both unstable.
- A rule-to-evidence matrix prevents attractive scenarios from leaving core obligations untested.
- Specifications should define trust boundaries and authorization decisions when inputs cross process, network, storage, or FFI boundaries.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Behavior is already stable and public | Normative contract plus compatibility examples | Downstream callers need durable semantics |
| Behavior is exploratory | Decision record and examples first | Premature MUST language freezes uncertain choices |
| Complex business rule | Rule table plus independent scenarios | Tables expose combinations; scenarios expose observations |
| Algorithmic implementation detail | Implementation plan unless externally observable | Private tactics should remain replaceable |
| Environment-dependent outcome | Contract the classification and evidence limits | Tests cannot promise unavailable infrastructure |

## Common Failure Modes

- Writing scenarios that call internal functions instead of describing user or system behavior.
- Using vague terms such as fast, valid, recent, or secure without measurable or decision-owned meaning.
- Making every current quirk normative because the code happens to behave that way.
- Omitting negative cases, limits, ordering, retries, and concurrency from an otherwise detailed happy path.
- Combining several actions in one When step so a failure cannot be localized.

## Required Evidence

- A glossary and boundary statement for overloaded domain terms.
- Normative rules with success, boundary, and failure examples.
- Independent acceptance scenarios mapped to rule IDs or headings.
- An explicit list of product decisions, non-goals, and environment-dependent evidence gaps.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.
