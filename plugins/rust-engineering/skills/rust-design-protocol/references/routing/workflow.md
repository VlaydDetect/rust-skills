# Workflow Examples

> Example rust-router workflow

## Example 1: Error Code with Domain Context

```
User: "Why am I getting E0382 in my trading system?"

Analysis:
1. Entry: Layer 1 (E0382 = ownership/move error)
2. Load: m01-ownership skill
3. Context: inspect repository trading and audit specifications

Trace UP ↑:
- E0382 in trading context
- Check whether the project actually requires immutable audit records
- Finding: Trading data should be shared, not moved

Response:
"E0382 indicates a value was moved when still needed.
If this trading system's specification requires immutable shared audit
records, the ownership graph must preserve that contract.

Instead of cloning, consider:
- Arc<TradeRecord> for shared immutable access
- This aligns with financial audit requirements

See: rust-ownership and the repository's audit requirements."
```

## Example 2: Design Question

```
User: "How should I handle user authentication?"

1. Entry: Layer 2 (design question)
2. Trace UP only to documented security and deployment constraints
3. Load: rust-architecture when the authentication boundary is undecided
4. Trace DOWN: rust-errors and rust-concurrency when relevant
5. Do not choose JWT until session, revocation, trust, and client constraints support it
```

## Example 3: Comparative Query

```
User: "Compare tokio and async-std"

1. Detect: "compare" → Enable negotiation
2. Load both runtime knowledge sources
3. Assess confidence for each
4. Synthesize with disclosed gaps
5. Answer: Structured comparison table
```

## Example 4: Multi-Layer Trace

```
User: "My web API reports Rc cannot be sent between threads"

1. Entry: Layer 1 (Send/Sync error)
2. Load: m07-concurrency
3. Inspect the framework's executor and state contract
4. Load rust-concurrency; add rust-architecture only if state placement is undecided
5. Choose `Arc`, thread-local state, or message passing from the actual topology
```

## Example 5: Intent Analysis Request

```
User: "Analyze this question: How do I share state in actix-web?"

Analysis Steps:
1. Extract Keywords: share, state, actix-web
2. Identify Entry Layer: Layer 1 (sharing = concurrency)
3. Map to Skills: rust-concurrency; use rust-architecture only for state-boundary design
4. Report:
   - Layer 1: Concurrency (state sharing mechanisms)
   - Framework constraints: confirm executor and application-state APIs from current docs
   - Suggested trace: mechanics → framework facts → architecture only if required
5. Invoke: rust-concurrency first; use rust-research for current Actix facts
```
