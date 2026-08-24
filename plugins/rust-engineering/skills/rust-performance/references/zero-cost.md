# Specialized Rust Zero Cost Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Primary owner: `$rust-performance`.
- Supporting profiles when needed: `$rust-traits`, `$rust-stable`.
- Scope retained: Static versus dynamic dispatch, monomorphization, iterators, abstraction boundaries, code size, allocation, and measured runtime cost.
- Baseline correction: Zero-cost means an abstraction should not impose avoidable runtime overhead relative to a suitable manual implementation; it does not promise zero compile time, code size, allocation, or all-purpose performance.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

## Generics vs Trait Objects

| Property | Generics (static dispatch) | Trait objects (dynamic dispatch) |
|-----|----------------------|--------------------------------|
| Performance | Zero overhead | vtable lookup |
| Code size | May grow through monomorphization | Smaller |
| Compilation time | Longer | Shorter |
| Flexibility | Types must be known | Types selected at runtime |
| Heterogeneous collections | Unsupported | `Vec<Box<dyn Trait>>` |


## When to Use Generics<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// The type is known at compile time
fn process<T: Processor>(item: T) {
    item.process();
}

// Return one concrete type
fn create_processor() -> impl Processor {
    // Return the concrete type
}

// Multiple type parameters
fn combine<A: Display, B: Display>(a: A, b: B) -> String {
    format!("{} and {}", a, b)
}
```


## When to Use Trait Objects<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Select the type at runtime
trait Plugin {
    fn run(&self);
}

struct PluginManager {
    plugins: Vec<Box<dyn Plugin>>,
}

// Heterogeneous collection
let handlers: Vec<Box<dyn Handler>> = vec![
    Box::new(HttpHandler),
    Box::new(GrpcHandler),
];
```


## Object-Safety Rules<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Not object-safe
trait Bad {
    fn create(&self) -> Self;  // Returns Self
    fn method(&self, x: Self);  // Takes Self as a parameter
}

// ✅ Object-safe
trait Good {
    fn name(&self) -> &str;
}
```


## impl Trait vs dyn Trait<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// impl Trait: return a concrete type (static dispatch)
fn create_processor() -> impl Processor {
    HttpProcessor
}

// dyn Trait: return a trait object (dynamic dispatch)
fn create_processor() -> Box<dyn Processor> {
    Box::new(HttpProcessor)
}
```


## Performance Impact<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Generics: generate a copy of the code for each type
fn process<T: Trait>(item: T) {
    item.method();
}
// After compilation:
// fn process_Http(item: Http) { ... }
// fn process_Ftp(item: Ftp) { ... }

// Trait object: one code path
fn process(item: &dyn Trait) {
    item.method();  // Call through the vtable
}
```


## Common Errors

| Error | Cause | Solution |
|-----|------|-----|
| E0277 | Missing trait bound | Add `T: Trait` |
| E0038 | Trait is not dyn-compatible | Check object-safety rules |
| E0308 | Type mismatch | Use one type or introduce generics |
| E0599 | Implementation not found | Implement the trait or check the bounds |


## Optimization Strategy

1. **Use generics in hot code** - Eliminate dynamic-dispatch overhead
2. **Use dyn in plugin systems** - Prioritize flexibility
3. **Use generics for small collections** - Avoid Box allocations
4. **Use dyn for large collections** - Reduce code-size growth
