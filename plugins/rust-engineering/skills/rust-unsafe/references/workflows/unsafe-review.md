# Unsafe review session adapter

Use this adapter for a deeper read-only review of one unsafe boundary.

1. State the safe public contract and the exact unsafe operations beneath it.
2. Build an invariant table covering provenance, extent, alignment,
   initialization, validity, aliasing, lifetime, layout, threads, panic, and
   destruction. Mark each row `proven`, `caller obligation`, `foreign
   contract`, or `unproven`.
3. Walk all constructors, mutation paths, callbacks, error paths, and drop
   paths. Ask the user only for facts that cannot be recovered from the code or
   declared external contract.
4. Apply the retained Design protocol checklist and only the rule files relevant to
   unresolved rows.
5. Return findings first, followed by verification evidence and residual risks.

A convincing comment, an `AtomicPtr`, `NonNull`, `UnsafeCell`, `repr(C)`, or a
clean Miri run is evidence for a narrow row; none is a whole-boundary proof.

