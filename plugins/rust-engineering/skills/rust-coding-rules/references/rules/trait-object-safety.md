# trait-object-safety

> Keep a trait dyn-compatible (object-safe) when you need `dyn Trait`

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-traits; supporters=`rust-api-design`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Keep a trait dyn-compatible (object-safe) when you need `dyn Trait`.

## Apply When

Apply when real implementations or callers need a behavioral abstraction, extension point, dispatch choice, or coherence solution, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when one concrete implementation or a closed enum expresses the current contract more directly. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Identify the variation axis, choose static, dynamic, associated-type, generic, enum, or newtype representation, then check coherence.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Static dispatch enables optimization but grows code; dynamic dispatch erases types but adds allocation, lifetime, and object-safety constraints.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Compile representative implementations and rejection cases; inspect object safety, blanket impls, auto traits, and downstream rights.

## Why It Matters

Only dyn-compatible traits can be used as `dyn Trait`. The Rust Reference defines dyn compatibility: every method must be dispatchable through a vtable, which means no generic type parameters on methods, no bare `Self` return or value position, and no associated constants. Violating these rules produces a hard compiler error at the `dyn` use site — often far from the trait definition. If you need both generic methods and `dyn Trait`, you can gate the non-dispatchable methods with `where Self: Sized`, which excludes them from the vtable while keeping the rest of the trait object-safe.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
trait Transformer {
    // Generic method — not dispatchable, makes the whole trait non-object-safe.
    fn transform<T: std::fmt::Debug>(&self, value: T) -> String;

    fn name(&self) -> &str;
}

struct Shout;
impl Transformer for Shout {
    fn transform<T: std::fmt::Debug>(&self, value: T) -> String {
        format!("{value:?}").to_uppercase()
    }
    fn name(&self) -> &str { "shout" }
}

// This fails to compile:
// error[E0038]: the trait `Transformer` cannot be made into an object
// fn apply(t: &dyn Transformer, x: i32) { ... }
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
trait Transformer {
    // Core dispatchable method — always in the vtable.
    fn transform_str(&self, value: &str) -> String;

    fn name(&self) -> &str;

    // Generic convenience method gated with `where Self: Sized`.
    // Callers can use it via a concrete type; it is excluded from `dyn Transformer`.
    fn transform_debug<T: std::fmt::Debug>(&self, value: T) -> String
    where
        Self: Sized,
    {
        self.transform_str(&format!("{value:?}"))
    }
}

// ----- Implementations -----

struct Shout;
impl Transformer for Shout {
    fn transform_str(&self, value: &str) -> String { value.to_uppercase() }
    fn name(&self) -> &str { "shout" }
}

struct Whisper;
impl Transformer for Whisper {
    fn transform_str(&self, value: &str) -> String { value.to_lowercase() }
    fn name(&self) -> &str { "whisper" }
}

// ----- Object-safe usage -----

fn apply_all(transformers: &[Box<dyn Transformer>], input: &str) {
    for t in transformers {
        println!("[{}] {}", t.name(), t.transform_str(input));
    }
}

// ----- Generic (static) usage — can call the `where Self: Sized` method -----

fn apply_generic<T: Transformer>(t: &T, value: i32) -> String {
    t.transform_debug(value)  // available because T: Sized
}

fn demo() {
    let ts: Vec<Box<dyn Transformer>> = vec![
        Box::new(Shout),
        Box::new(Whisper),
    ];
    apply_all(&ts, "Hello World");

    // Static dispatch path can use the generic helper.
    let result = apply_generic(&Shout, 42);
    println!("{result}");
}
```

## Dyn-Compatibility Rules (Quick Reference)

| Feature | Allowed in `dyn Trait`? |
|---|---|
| `&self` / `&mut self` methods | Yes |
| Methods returning `Self` by value | No — use `Box<Self>` or gate with `where Self: Sized` |
| Generic method parameters (`fn f<T>`) | No — gate with `where Self: Sized` |
| Associated constants | No |
| Associated types | Yes (type is erased but fixed per impl) |
| `where Self: Sized` methods | Excluded from vtable, safe to have |

See the Rust Reference — "Object Safety" — at doc.rust-lang.org/reference/items/traits.html#object-safety for the full rules.

## Related Rules
- [trait-dyn-vs-generic](trait-dyn-vs-generic.md) - choose between static and dynamic dispatch deliberately
- [anti-type-erasure](anti-type-erasure.md) - don't use `Box<dyn Trait>` when `impl Trait` works
- [api-sealed-trait](api-sealed-trait.md) - prevent external implementations of a trait
