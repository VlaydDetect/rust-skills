# Actionbook abstraction protocol

Use these references after the API and ownership constraints are known. They preserve Actionbook's mechanical questions without treating every compile-time encoding as desirable.

## Zero-cost abstractions

- [Generics, dispatch, and monomorphization](actionbook/m04-zero-cost/overview.md)

Use when choosing generics, `impl Trait`, trait objects, or manual specialization. Include code-size, compile-time, object-safety, and dynamic-dispatch costs in the decision.

## Type-driven design

- [Newtypes, typestate, markers, and sealed traits](actionbook/m05-type-driven/overview.md)

Use when invalid states can be excluded at a stable boundary. Reject typestate or marker machinery when runtime validation is clearer or when state growth makes the API harder to use.
