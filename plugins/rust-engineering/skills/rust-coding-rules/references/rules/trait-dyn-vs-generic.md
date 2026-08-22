# trait-dyn-vs-generic

> Choose static dispatch (generics / `impl Trait`) vs dynamic dispatch (`dyn Trait`) deliberately

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-traits; supporters=`rust-api-design`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Choose static dispatch (generics / `impl Trait`) vs dynamic dispatch (`dyn Trait`) deliberately.

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

Generic bounds and `impl Trait` monomorphize at compile time: each concrete type gets its own specialised copy that the compiler can inline and optimise, but every distinct type adds to binary size. `dyn Trait` stores a fat pointer (data + vtable) and dispatches at runtime, producing a single code path — necessary when you must store heterogeneous values or return erased types, at the cost of one pointer indirection per call. Choosing the wrong option either leaves performance on the table or prevents heterogeneous collections entirely. Default to generics for hot, simple code; reach for `dyn` when you need flexibility, heap storage, or cross-crate plug-ins.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Using `dyn` everywhere "to be flexible" — blocks inlining and
// forces heap allocation even for single, known types.
trait Shape {
    fn area(&self) -> f64;
}

struct Circle { radius: f64 }
impl Shape for Circle {
    fn area(&self) -> f64 { std::f64::consts::PI * self.radius * self.radius }
}

// Unnecessary boxing when only one concrete type is used.
fn total_area(shapes: &[Box<dyn Shape>]) -> f64 {
    shapes.iter().map(|s| s.area()).sum()
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::fmt;

trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> &str;
}

#[derive(Clone)]
struct Circle { radius: f64 }
#[derive(Clone)]
struct Rect { w: f64, h: f64 }

impl Shape for Circle {
    fn area(&self) -> f64 { std::f64::consts::PI * self.radius * self.radius }
    fn name(&self) -> &str { "circle" }
}
impl Shape for Rect {
    fn area(&self) -> f64 { self.w * self.h }
    fn name(&self) -> &str { "rect" }
}

// --- Static dispatch: use when the type is known and performance matters ---
// Monomorphized; the compiler can inline `area()`.
fn total_area_generic<S: Shape>(shapes: &[S]) -> f64 {
    shapes.iter().map(|s| s.area()).sum()
}

// Also fine with `impl Trait` in argument position (same monomorphization).
fn print_area(shape: &impl Shape) {
    println!("{}: {:.2}", shape.name(), shape.area());
}

// --- Dynamic dispatch: use for heterogeneous collections or plugin-like APIs ---
fn total_area_dyn(shapes: &[Box<dyn Shape>]) -> f64 {
    shapes.iter().map(|s| s.area()).sum()
}

fn demo() {
    // Homogeneous slice — zero boxing, static dispatch.
    let circles = [Circle { radius: 1.0 }, Circle { radius: 2.0 }];
    println!("{:.2}", total_area_generic(&circles));

    // Heterogeneous collection — `dyn` is the right tool.
    let shapes: Vec<Box<dyn Shape>> = vec![
        Box::new(Circle { radius: 1.0 }),
        Box::new(Rect { w: 3.0, h: 4.0 }),
    ];
    println!("{:.2}", total_area_dyn(&shapes));
}
```

## Decision Table

| Situation | Prefer |
|---|---|
| Single known concrete type | `impl Trait` / generic |
| Hot path, inlining critical | Generic bound |
| Heterogeneous collection (`Vec<Box<dyn …>>`) | `dyn Trait` |
| Storing trait objects across calls | `dyn Trait` |
| Returning erased type from `fn` | `Box<dyn Trait>` or `impl Trait` (static) |
| Binary size matters, many monomorphisations | `dyn Trait` |
| Plug-in / callback registered at runtime | `dyn Trait` |

## Related Rules
- [anti-type-erasure](anti-type-erasure.md) - don't use `Box<dyn Trait>` when `impl Trait` works
- [type-generic-bounds](type-generic-bounds.md) - add trait bounds only where needed
- [trait-object-safety](trait-object-safety.md) - keep traits dyn-compatible when you need `dyn Trait`
