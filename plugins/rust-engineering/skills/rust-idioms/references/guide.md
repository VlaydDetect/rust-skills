# Rust Idioms Field Guide

This guide is the detailed policy for `rust-idioms`. It synthesizes the craft idiom patterns and anti-patterns plus full-stack style, stable, stdlib, and API guidance; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- Idiomatic Rust makes ownership, invalid states, failure, and iteration visible to the compiler and reader.
- RAII guards, enums, iterators, pattern matching, newtypes, and narrow mutability are recurring tools rather than universal mandates.
- Anti-patterns include needless collect, clone-to-appease-borrow-checker, stringly typed state, panicking library code, and abstraction copied from inheritance-heavy languages.
- Readability is contextual: a loop with early exits can be clearer than a dense iterator chain.
- Pattern selection must preserve evaluation order, short-circuit behavior, drop timing, and error context.
- Repository consistency is valuable until it conflicts with correctness or an explicit modernization goal.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Simple transformation pipeline | Iterator adapters | Ownership and laziness remain visible |
| Complex stateful early-exit loop | Explicit loop | Control flow is the primary information |
| Several exclusive states | Enum | Invalid combinations become unrepresentable |
| Many optional constructor fields | Builder | Named staged configuration improves call sites |
| One obvious constructor | Direct `new` or literal | A builder adds ceremony without choices |

## Common Failure Modes

- Replacing straightforward loops with opaque nested combinators merely to appear idiomatic.
- Adding clones during refactoring without documenting ownership or cost.
- Using `unwrap` in library or input paths because an example did so.
- Creating traits and builders modeled on another language when Rust enums or concrete types suffice.
- Accepting every lint mechanically and changing API or MSRV accidentally.

## Required Evidence

- The invariant or readability problem the chosen idiom resolves.
- Confirmation that allocation, ordering, errors, drops, and public API remain intentional.
- Compiler or test evidence for semantic rewrites and benchmarks only for performance claims.
- A stated repository convention or reason for deviating from it.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.
