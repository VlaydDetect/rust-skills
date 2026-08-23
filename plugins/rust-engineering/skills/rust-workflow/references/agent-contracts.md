# Agent contracts

Delegation is optional. The main agent remains the sole writer and sends only the context needed for one bounded question.

## RoleBrief

```text
role: rust-scout | rust-researcher | rust-reviewer | rust-verifier
question: one concrete question
scope: packages, files, symbols, or commands allowed
constraints: toolchain, features, target, time or command limits
known_context: facts already established by the main agent
profiles: one primary and up to two supporting profile names
expected_output: ContextBrief | ResearchRecord | Finding[] | VerificationRecord
```

## ContextBrief

```text
scope; relevant files and symbols; callers and tests; effective Cargo state;
repository-native commands; constraints; unknowns; evidence locations
```

## Finding

```text
id; status=Confirmed|Suspected; severity=Critical|High|Medium|Low;
file:line; claim; evidence; impact; smallest viable fix; verification
```

Reject a finding when its premise is contradicted by opened code. Keep it `Suspected` when decisive evidence is unavailable. Never manufacture a location.

## ResearchRecord

```text
subject; exact version or Cargo package ID; repository baseline; claim;
canonical source; retrieval date; confidence; gaps; adoption implications
```

Prefer primary, version-matched sources. Community material is discovery
evidence and must be labelled. One useful fallback is enough before returning
an explicit gap.

## VerificationRecord

```text
command; scope; expected evidence; result=PASS|FAIL|SKIP;
cause=change|pre-existing|environmental|unknown; evidence; residual risk
```

Subagents must read the assigned profiles before applying their rules. They must not edit files, install tools, update dependencies, publish, or widen scope. If a command may mutate source, lockfiles, generated assets, or external state, return it as a recommendation instead of running it.

The main agent remains the only writer, owns cross-profile trade-offs, and decides whether evidence is sufficient. A scout maps current state, a researcher establishes one current external fact, a reviewer attempts to falsify a change, and a verifier executes an agreed evidence command; do not assign two roles the same question. For a post-fix re-review, prefer a fresh reviewer context and provide the original finding IDs without the implementer's conclusion.
