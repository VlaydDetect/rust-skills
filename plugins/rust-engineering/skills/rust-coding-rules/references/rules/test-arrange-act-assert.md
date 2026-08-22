# test-arrange-act-assert

> Structure tests with clear Arrange, Act, Assert sections

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-testing; supporters=`rust-verify`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Structure tests with clear Arrange, Act, Assert sections.

## Apply When

Apply when a concrete contract or risk needs the cheapest deterministic test that would fail for the defect, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the technique duplicates lower-cost coverage or adds a framework, snapshot, mock, sleep, or fuzz harness without unique risk coverage. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Map the contract to one test level and technique, isolate uncontrolled resources, and prove the assertion fails for the intended regression when practical.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Specialized test tools broaden state-space coverage but add dependencies, execution cost, maintenance, and false-stability risk.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`tokio`) must already be accepted by the project or be approved before addition.

## Verification

Run the exact new test and its owning package or target, then record required features, runtime, seed, environment, and residual matrix.

## Why It Matters

The AAA pattern makes tests readable and maintainable. Each section has a clear purpose: set up test data, execute the code under test, verify the results. This structure helps identify what's being tested and makes tests easier to debug when they fail.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
#[test]
fn test_user() {
    assert_eq!(User::new("alice", "alice@example.com").unwrap().name(), "alice");
    assert!(User::new("", "email@example.com").is_err());
    let u = User::new("bob", "bob@example.com").unwrap();
    assert!(u.validate());
    assert_eq!(u.email(), "bob@example.com");
}
// Multiple concerns, hard to understand, hard to debug
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
#[test]
fn new_user_has_correct_name() {
    // Arrange
    let name = "alice";
    let email = "alice@example.com";
    
    // Act
    let user = User::new(name, email).unwrap();
    
    // Assert
    assert_eq!(user.name(), "alice");
}

#[test]
fn user_creation_fails_with_empty_name() {
    // Arrange
    let name = "";
    let email = "email@example.com";
    
    // Act
    let result = User::new(name, email);
    
    // Assert
    assert!(result.is_err());
    assert!(matches!(result, Err(UserError::EmptyName)));
}
```

## With Comments

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the With Comments illustration -->
```rust
#[test]
fn order_total_includes_tax() {
    // Arrange
    let mut order = Order::new();
    order.add_item(Item::new("Widget", 100.00));
    order.add_item(Item::new("Gadget", 50.00));
    let tax_rate = 0.10;
    
    // Act
    let total = order.calculate_total(tax_rate);
    
    // Assert
    let expected = (100.00 + 50.00) * 1.10;
    assert_eq!(total, expected);
}
```

## Complex Arrange

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Complex Arrange illustration -->
```rust
#[test]
fn search_returns_matching_documents() {
    // Arrange
    let mut index = SearchIndex::new();
    index.add_document(Document::new(1, "rust programming"));
    index.add_document(Document::new(2, "python programming"));
    index.add_document(Document::new(3, "rust web development"));
    
    let query = Query::new("rust");
    
    // Act
    let results = index.search(&query);
    
    // Assert
    assert_eq!(results.len(), 2);
    assert!(results.iter().any(|d| d.id == 1));
    assert!(results.iter().any(|d| d.id == 3));
}
```

## Async Tests

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Async Tests illustration -->
```rust
#[tokio::test]
async fn fetch_user_returns_user_data() {
    // Arrange
    let client = TestClient::new();
    let user_id = 42;
    
    // Act
    let result = client.fetch_user(user_id).await;
    
    // Assert
    assert!(result.is_ok());
    let user = result.unwrap();
    assert_eq!(user.id, user_id);
}
```

## Helper Functions

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Helper Functions illustration -->
```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    // Arrange helpers
    fn create_test_user() -> User {
        User::new("test", "test@example.com").unwrap()
    }
    
    fn create_order_with_items(items: &[(&str, f64)]) -> Order {
        let mut order = Order::new();
        for (name, price) in items {
            order.add_item(Item::new(name, *price));
        }
        order
    }
    
    // Assert helpers
    fn assert_order_total(order: &Order, expected: f64) {
        let total = order.calculate_total(0.0);
        assert!((total - expected).abs() < 0.01);
    }
    
    #[test]
    fn order_total_sums_items() {
        // Arrange
        let order = create_order_with_items(&[
            ("A", 10.0),
            ("B", 20.0),
        ]);
        
        // Act & Assert
        assert_order_total(&order, 30.0);
    }
}
```

## Related Rules
- [test-descriptive-names](./test-descriptive-names.md) - Test naming
- [test-fixture-raii](./test-fixture-raii.md) - Test setup/teardown
- [test-mock-traits](./test-mock-traits.md) - Mocking dependencies
