# Huiali Macro Protocol

> Product adaptation of `skills/rust-macro/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-macros`.
- Supporting profiles when needed: `$rust-testing`, `$rust-api-design`.
- Scope retained: macro_rules!, derive, attribute and function-like procedural macros, token handling, hygiene, diagnostics, expansion, and compile-time tests.
- Baseline correction: Procedural macros have three official forms: function-like, derive, and attribute. Use absolute generated paths where appropriate, preserve spans for diagnostics, and test expansion and failure behavior on the supported toolchain.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## Macros vs Generics

| Dimension | Macros | Generics |
|-----------|--------|----------|
| Flexibility | Code transformation | Type abstraction |
| Compile cost | Incremental-friendly | Monomorphization overhead |
| Error messages | Can be cryptic | Clear |
| Debugging | Debug expanded code | Direct debugging |
| Use case | Reduce boilerplate | Generic algorithms |


## Solution Patterns

### Pattern 1: Declarative Macro (macro_rules!)

<!-- huiali-source: skills/rust-macro/SKILL.md#rust-block-1; sha256=50efb6fb14960d83fde8b29035826c0d3c6e326f9055993a747fbcfe36019adc -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Basic structure
macro_rules! my_vec {
    // Empty case
    () => {
        Vec::new()
    };
    // List of elements
    ($($elem:expr),* $(,)?) => {{
        let mut v = Vec::new();
        $(
            v.push($elem);
        )*
        v
    }};
    // Repeated element
    ($elem:expr; $n:expr) => {
        vec![$elem; $n]
    };
}

// Usage
let v1 = my_vec![];
let v2 = my_vec![1, 2, 3];
let v3 = my_vec![0; 10];
```

### Pattern 2: Derive Macro

<!-- huiali-source: skills/rust-macro/SKILL.md#rust-block-2; sha256=a9bb9eccc676e63c799fb279792d04c1573adea3687fae5c28c4749be4515595 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// In a separate proc-macro crate
use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, DeriveInput};

#[proc_macro_derive(Builder)]
pub fn derive_builder(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let name = &input.ident;
    let builder_name = format!("{}Builder", name);
    let builder_ident = syn::Ident::new(&builder_name, name.span());

    let fields = match &input.data {
        syn::Data::Struct(data) => &data.fields,
        _ => panic!("Builder only works on structs"),
    };

    let field_names: Vec<_> = fields.iter()
        .filter_map(|f| f.ident.as_ref())
        .collect();

    let field_types: Vec<_> = fields.iter()
        .map(|f| &f.ty)
        .collect();

    let expanded = quote! {
        pub struct #builder_ident {
            #(#field_names: Option<#field_types>),*
        }

        impl #builder_ident {
            pub fn new() -> Self {
                Self {
                    #(#field_names: None),*
                }
            }

            #(
                pub fn #field_names(mut self, value: #field_types) -> Self {
                    self.#field_names = Some(value);
                    self
                }
            )*

            pub fn build(self) -> Result<#name, String> {
                Ok(#name {
                    #(
                        #field_names: self.#field_names
                            .ok_or_else(|| format!("Field {} not set", stringify!(#field_names)))?
                    ),*
                })
            }
        }

        impl #name {
            pub fn builder() -> #builder_ident {
                #builder_ident::new()
            }
        }
    };

    expanded.into()
}
```

### Pattern 3: Function-like Proc Macro

<!-- huiali-source: skills/rust-macro/SKILL.md#rust-block-3; sha256=8a1c5c8e3336a8d575f08c1d56c93e9b947b2f1945ae83fc7dc802bed808e833 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
    let sql_string = input.to_string();

    // Parse and validate SQL at compile time
    validate_sql(&sql_string);

    // Generate code
    quote! {
        QueryBuilder::raw(#sql_string)
    }.into()
}

// Usage:
let query = sql!("SELECT * FROM users WHERE id = ?");
```

### Pattern 4: Attribute Macro

<!-- huiali-source: skills/rust-macro/SKILL.md#rust-block-4; sha256=61af748192935c1c35c596a457f8b6c6acf678c81aec16f66238e36db5106f7b -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
#[proc_macro_attribute]
pub fn cached(_attr: TokenStream, item: TokenStream) -> TokenStream {
    let input = parse_macro_input!(item as ItemFn);
    let fn_name = &input.sig.ident;
    let fn_body = &input.block;

    let expanded = quote! {
        fn #fn_name() -> Result {
            use std::sync::OnceLock;
            static CACHE: OnceLock<Result> = OnceLock::new();

            CACHE.get_or_init(|| {
                #fn_body
            }).clone()
        }
    };

    expanded.into()
}

// Usage:
#[cached]
fn expensive_computation() -> String {
    // ...
}
```


## Repetition Patterns

| Syntax | Meaning |
|--------|---------|
| `$()` | Match zero or more |
| `$($x),*` | Comma-separated |
| `$($x),+` | At least one |
| `$x:ty` | Type matcher |
| `$x:expr` | Expression matcher |
| `$x:pat` | Pattern matcher |
| `$x:ident` | Identifier matcher |
| `$x:path` | Path matcher |
| `$x:tt` | Token tree matcher |

<!-- huiali-source: skills/rust-macro/SKILL.md#rust-block-5; sha256=b745b652fbbe19faf99692d2c99fdaa9eb8ec1fc448ba8d31c31f856b20698cf -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Example: multiple matchers
macro_rules! create_struct {
    ($name:ident { $($field:ident: $type:ty),* }) => {
        struct $name {
            $($field: $type),*
        }
    };
}

create_struct!(User {
    id: u64,
    name: String,
    email: String
});
```


## Workflow

### Step 1: Consider Alternatives

```
Need to reduce duplication?
  → Can generics solve it? Prefer generics
  → Need syntax transformation? Use macros
  → Need to inspect types? Derive macro
  → Need attribute? Attribute macro
```

### Step 2: Choose Macro Type

```
Declarative (macro_rules!)?
  ✅ Simple pattern matching
  ✅ Quick to write
  ❌ Limited power

Procedural (proc-macro)?
  ✅ Full AST access
  ✅ Complex transformations
  ❌ Separate crate needed
  ❌ Longer compile times
```

### Step 3: Debug Expansion

```bash
# Expand macros
cargo expand

# Expand specific function
cargo expand my_module::my_function

# Expand tests
cargo expand --test test_name
```

### Step 4: Test Thoroughly

<!-- huiali-source: skills/rust-macro/SKILL.md#rust-block-6; sha256=c169e4132cffe9d683ae0b7fd16ae89526e5d0dd651411da90f0d9504a3f49cc -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_macro_expansion() {
        // Test generated code
        let result = my_macro!(input);
        assert_eq!(result, expected);
    }
}
```


## Common Crates

| Crate | Purpose |
|-------|---------|
| **syn** | Parse Rust syntax |
| **quote** | Generate Rust code |
| **proc-macro2** | Token manipulation |
| **derive-more** | Common derive macros |
| **darling** | Parse macro attributes |


## Best Practices

| Practice | Reason |
|----------|--------|
| Try generics first | Safer, easier to debug |
| Keep macros simple | Complex macros hard to maintain |
| Document macros | Users need to understand expansion |
| Test expansion | Ensure correctness |
| Use cargo expand | Visualize macro output |


## Review Checklist

When reviewing macro code:

- [ ] Could this be solved with generics instead?
- [ ] Macro expansion documented with examples
- [ ] Error messages are helpful
- [ ] Edge cases tested
- [ ] Hygiene respected (no accidental captures)
- [ ] Used cargo expand to verify output
- [ ] Compile-time overhead acceptable
- [ ] No unnecessary proc-macro dependency


## Verification Commands

```bash
# Expand macros
cargo expand

# Expand specific module
cargo expand path::to::module

# Check proc-macro crate
cargo check -p my-proc-macro

# Test expansion
cargo test --all-features
```


## Common Pitfalls

### 1. Hygiene Violations

**Symptom**: Unexpected variable captures

<!-- huiali-source: skills/rust-macro/SKILL.md#rust-block-7; sha256=00246709509f3f6f060df97908bdd8721feb8148a039098a6a5d48eec8c6e8a8 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: name clash risk
macro_rules! bad_macro {
    ($x:expr) => {{
        let result = $x;  // 'result' might clash
        result
    }};
}

// ✅ Good: use unique names
macro_rules! good_macro {
    ($x:expr) => {{
        let __macro_result = $x;
        __macro_result
    }};
}
```

### 2. Complex Error Messages

**Symptom**: Users don't understand macro errors

<!-- huiali-source: skills/rust-macro/SKILL.md#rust-block-8; sha256=f48e84bda1a0fc58ed0238cab4c9a4ca15d4946ce9ecca64c5d5ebff18a9b28c -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ Good: helpful error messages
macro_rules! require_trait {
    ($t:ty) => {
        const _: fn() = || {
            fn assert_impl<T: MyTrait>() {}
            assert_impl::<$t>();
        };
    };
}
```

### 3. Proc Macro Compile Time

**Symptom**: Slow incremental builds

<!-- huiali-source: skills/rust-macro/SKILL.md#rust-block-9; sha256=58270e0eb56a50ad03b280ea094a4197967a3cb26292de18280bb4d70aa8aabf -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Avoid: heavy proc macros for simple tasks
#[derive(HeavyProcMacro)]
struct Simple {
    field: String,
}

// ✅ Better: manual impl or simpler derive
impl Simple {
    // Manual implementation
}
```


## Related Skills

- **rust-coding** - Naming macro conventions
- **rust-performance** - Macro compile-time cost
- **rust-type-driven** - When generics suffice
- **rust-error** - Error handling in macros
- **rust-testing** - Testing macro expansion

## Additional unique source examples

These code-only deltas appeared in the condensed English or localized source. They remain fragments, not dependency or hardware claims.

### `SKILL_ZH.md` example 1

<!-- huiali-source: skills/rust-macro/SKILL_ZH.md#rust-block-1; sha256=5e1fa46dce4044740514250d20e9ba431c040689b43a18319f7d0de25f7d9bce -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
macro_rules! my_vec {
    () => {
        Vec::new()
    };
    ($($elem:expr),*) => {
        vec![$($elem),*]
    };
    ($elem:expr; $n:expr) => {
        vec![$elem; $n]
    };
}
```

### `SKILL_ZH.md` example 2

<!-- huiali-source: skills/rust-macro/SKILL_ZH.md#rust-block-2; sha256=d7d52666e99dd0de5eac0694645dce4d4716aa9f0b9caf71bedd6d7f8046d063 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use proc_macro::TokenStream;
#[proc_macro_derive(MyDerive)]
pub fn my_derive(input: TokenStream) -> TokenStream {
    let input = syn::parse_macro_input!(input as syn::DeriveInput);
    let name = &input.ident;

    let expanded = quote::quote! {
        impl MyDerive for #name {
            fn my_method(&self) -> String {
                format!("Hello from {}", stringify!(#name))
            }
        }
    };

    expanded.into()
}
```

### `SKILL_ZH.md` example 3

<!-- huiali-source: skills/rust-macro/SKILL_ZH.md#rust-block-3; sha256=c9e687fd193b8457742ff76913f4c796a4bf725a5649bb1bf0ea993a8e373842 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
#[derive(MyDerive)]
struct MyStruct {
    field: i32,
}
```

### `SKILL_ZH.md` example 4

<!-- huiali-source: skills/rust-macro/SKILL_ZH.md#rust-block-4; sha256=4854cd5fd866bbec218abb25f01b106bc9494dea7a46fbb504ef5d52c42a7860 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
#[proc_macro]
pub fn my_func_macro(input: TokenStream) -> TokenStream {
    // 转换输入
    let tokens = input.into_iter().collect::<Vec<_>>();
    // 生成代码
    quote::quote! { /* ... */ }.into()
}
```
