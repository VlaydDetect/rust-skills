# Rust Pinning Field Guide

## Contract Model

Pinning matters only when a value has an invariant that becomes invalid if the value moves after a defined point. Record the pointee, storage owner, contract start, structurally pinned fields, permitted mutation, and destruction rule. Separate address stability from lifetime validity, aliasing, thread safety, and immutability.

## Construction Algorithm

1. Prefer a representation that avoids self-reference, such as indices, handles, owned offsets, or a two-phase external graph.
2. If address sensitivity remains necessary, construct the value without exposing a pinned reference prematurely.
3. Establish all internal links while exclusive access is valid.
4. Start the pinning contract through a safe constructor when possible.
5. Expose only operations that preserve the contract; do not return an unpinned mutable reference to structurally pinned data.
6. Ensure destruction occurs before storage reuse and that deregistration or unlinking cannot race destruction.

## Projection Review

- Classify each field as structurally pinned or movable.
- Check generic `Unpin` bounds rather than assuming the outer type's behavior.
- Verify that `Drop`, assignment, `mem::replace`, enum transitions, and container movement cannot bypass the projection promise.
- Prefer a maintained projection facility when it matches the project's dependency policy; otherwise keep unsafe projection minimal and locally proved.

## Future Interaction

`Future::poll` receives `Pin<&mut Self>` because an async state machine may hold references across suspension. The Future owner controls allocation and polling; the pinning contract controls movement. Cancellation means destruction of the Future, so guards and pinned fields must remain valid and clean up without another poll.

## Required Evidence

- A written invariant and contract start.
- Safe-callers analysis for every unsafe pin operation.
- Compile-time assertions or compile-fail checks for intended `Unpin` behavior when valuable.
- Focused tests for projection, cancellation, drop order, and any registered external pointer.
- Miri only where supported; do not treat an unavailable nightly component as successful verification.

## Compiling Example

The dependency-free fixture in `../examples/golden/` demonstrates an address-sensitive value built with `PhantomPinned`, safe accessors, and a local construction proof.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-coroutine`](../../rust-concurrency/references/coroutine.md) — supporting; Stackless and stackful models, explicit state machines, suspension, scheduling, pinning, cancellation, and resource cleanup.
- [`rust-pin`](./pin.md) — primary; Address sensitivity, Pin/Unpin, structural projection, self-reference, Future polling, and the drop guarantee.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return the decision to its owner after coding constraints or helper evidence have been stated.
