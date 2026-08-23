# macro-proc-error-spans

> Report proc-macro errors as spanned compile errors, never by panicking## Decision

Consider this rule only after its prerequisites are satisfied: Report proc-macro errors as spanned compile errors, never by panicking.

## Apply When

Apply when ordinary functions, traits, generics, derives, or build-time generation cannot express required Rust syntax or repetition cleanly, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when a normal language abstraction is sufficient or the proposed DSL adds more grammar and diagnostics than value. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Specify valid and invalid invocations, expansion, hygiene, evaluation count, visibility, and diagnostics before implementation.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Macros remove repetition but add expansion, hygiene, diagnostics, navigation, public surface, and compile-time costs.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`thiserror`, `syn`, `quote`, `proc-macro2`) must already be accepted by the project or be approved before addition.

## Verification

Use compile-pass and compile-fail cases, expansion inspection, crate-renaming and cross-crate tests, and compile-time measurement when broad.

## Why It Matters

A `panic!`, `.unwrap()`, or `.expect()` inside a proc-macro produces an opaque compiler message — "proc macro panicked" — with no source location. The user sees no indication of which part of their code triggered the error. Returning a `syn::Error` converted to a token stream instead gives a diagnostic that points directly at the offending span, exactly like an ordinary compiler error.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use proc_macro::TokenStream;
use syn::{parse_macro_input, Data, DeriveInput};

#[proc_macro_derive(MyTrait)]
pub fn derive_my_trait(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);

    let fields = match input.data {
        Data::Struct(ref s) => &s.fields,
        _ => panic!("MyTrait can only be derived on structs"), // WRONG
    };

    // `.unwrap()` here gives "called `Option::unwrap()` on a `None` value"
    // with no location info in user code.
    let first = fields.iter().next().unwrap();
    let name = first.ident.as_ref().unwrap();

    quote::quote! {
        impl MyTrait for #name {}
    }
    .into()
}
```

```text
error: proc macro panicked
  --> src/main.rs:3:10
   |
 3 | #[derive(MyTrait)]
   |          ^^^^^^^
   |
   = help: message: MyTrait can only be derived on structs
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use proc_macro::TokenStream;
use proc_macro2::TokenStream as TokenStream2;
use quote::quote;
use syn::{parse_macro_input, spanned::Spanned, Data, DeriveInput, Error};

#[proc_macro_derive(MyTrait)]
pub fn derive_my_trait(input: TokenStream) -> TokenStream {
    derive_my_trait_inner(input).unwrap_or_else(|e| e.to_compile_error().into())
}

fn derive_my_trait_inner(input: TokenStream) -> Result<TokenStream, Error> {
    let input = parse_macro_input!(input as DeriveInput);

    let fields = match &input.data {
        Data::Struct(s) => &s.fields,
        Data::Enum(e) => {
            return Err(Error::new_spanned(
                &input.ident,
                "MyTrait can only be derived on structs, not enums",
            ));
        }
        Data::Union(u) => {
            return Err(Error::new_spanned(
                &input.ident,
                "MyTrait can only be derived on structs, not unions",
            ));
        }
    };

    let first = fields.iter().next().ok_or_else(|| {
        Error::new_spanned(&input.ident, "MyTrait requires at least one field")
    })?;

    let field_name = first.ident.as_ref().ok_or_else(|| {
        // Attach the error to the field's span, not the struct name.
        Error::new_spanned(first, "MyTrait requires named fields")
    })?;

    let struct_name = &input.ident;
    Ok(quote! {
        impl MyTrait for #struct_name {
            fn first_field_name() -> &'static str {
                stringify!(#field_name)
            }
        }
    }
    .into())
}
```

```text
error: MyTrait requires named fields
  --> src/main.rs:7:5
   |
 7 |     u8,   // tuple struct field
   |     ^^
```

## Key Points

- Wrap proc-macro logic in a `fn(...) -> Result<TokenStream2, syn::Error>` helper and convert at the entry point with `.unwrap_or_else(|e| e.to_compile_error().into())`.
- Use `Error::new_spanned(tokens, "message")` to attach the error to a specific part of the input AST.
- Use `Error::new(span, "message")` when you only have a `Span`, not a token.
- Combine multiple errors with `Error::combine` rather than returning early, so the user sees all problems at once.
- Error messages: lowercase, no trailing punctuation (consistent with Rust compiler style).

## Related Rules
- [macro-proc-syn-quote](macro-proc-syn-quote.md) - parsing with syn, quoting with quote
- [err-thiserror-lib](err-thiserror-lib.md) - idiomatic library error types
