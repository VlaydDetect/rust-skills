# Actionbook cognitive protocol index

Load one branch at a time.

## Layer routing and comparisons

- [Adapted three-layer router](actionbook/rust-router/overview.md)
- [Worked routing examples](actionbook/rust-router/examples/workflow.md)
- [Comparison and ambiguity protocol](actionbook/rust-router/patterns/negotiation.md)
- [Optional safety-tool integration](actionbook/rust-router/integrations/os-checker.md)

The adapted router does not replace `rust-workflow`, install a prompt hook, or force negotiation for keywords.

## Mental models

- [Mental-model selection](actionbook/m14-mental-model/overview.md)
- [Thinking in Rust patterns](actionbook/m14-mental-model/patterns/thinking-in-rust.md)

Use these for explanation and misconception repair. Confirm every analogy against the actual language invariant.

## Multi-lens analysis

- [Experimental parallel source protocol](actionbook/meta-cognition-parallel/overview.md)
- [Layer 1 mechanics lens](actionbook/agents/layer1-analyzer.md)
- [Layer 2 design lens](actionbook/agents/layer2-analyzer.md)
- [Layer 3 domain lens](actionbook/agents/layer3-analyzer.md)
- [Evidence confidence rubric](actionbook/agents/_negotiation/confidence-rubric.md)
- [Source response format](actionbook/agents/_negotiation/response-format.md)

Reuse its layer lenses and synthesis checks. Do not launch three agents by default; sequential analysis is the normal path.

## Full cognitive protocol

Load one retained document only when its trigger applies:

- [Layer definitions](actionbook/cognitive-protocol/layer-definitions.md) for L1 mechanics, L2 design, and L3 domain routing.
- [Reasoning framework](actionbook/cognitive-protocol/reasoning-framework.md) for upward, downward, or bidirectional constraint tracing.
- [Negotiation protocol](actionbook/cognitive-protocol/negotiation-protocol.md) and [response templates](actionbook/cognitive-protocol/negotiation-templates.md) only when work was actually delegated and evidence must be synthesized.
- [Error escalation](actionbook/cognitive-protocol/error-protocol.md) after repeated evidence shows the current layer or approach is wrong; three attempts are not mandatory.
- [Externalized cognition](actionbook/cognitive-protocol/externalization.md) for long tasks that need inspectable decision and evidence artifacts, never private chain-of-thought logs.
- [Hook patterns](actionbook/cognitive-protocol/hooks-patterns.md) as a workflow-checkpoint catalog only. It does not authorize additional automatic host hooks.

## Worked and operational references

- [Context optimization](actionbook/context-optimization.md) preserves source
  guidance on progressive disclosure and isolated work with product limits on
  forced forks and parallelism.
- [E0382 trading-system example](actionbook/examples/e0382-trading-system.md) is
  a worked upward/downward trace. Its domain assumptions and `Arc` choice must
  be re-established before reuse.
