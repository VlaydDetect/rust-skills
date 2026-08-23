# Huiali Lifetime Complex Protocol

> Product adaptation of `skills/rust-lifetime-complex/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-ownership`.
- Supporting profiles when needed: `$rust-traits`, `$rust-api-design`.
- Scope retained: Lifetime diagnosis, variance, HRTBs, GATs, reborrowing, returned borrows, trait objects, and async lifetime boundaries.
- Baseline correction: Start from who owns the data and how long the API must expose it. Add explicit lifetimes, HRTBs, or GATs only after the concrete relationship is identified.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## Solution Patterns

### Pattern 1: HRTB (Higher-Ranked Trait Bounds)

<!-- huiali-source: skills/rust-lifetime-complex/SKILL.md#rust-block-1; sha256=2aa0eeac86e66e699dc50262357c3761d8efa1a59c62f7b7e523440d04e68338 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Problem: Concrete lifetime vs generic lifetime

// ❌ This doesn't work with dyn
type ClosureFn<T> = dyn for<'a> FnOnce(&'a mut Connection) -> BoxFuture<'a, T>;

// ✅ Solution: Keep HRTB in generic bounds
async fn with_connection<F, T, Fut>(f: F) -> Result<T, Error>
where
    F: for<'c> FnOnce(&'c mut Connection) -> Fut,
    Fut: Future<Output = Result<T, Error>>,
{
    let mut conn = get_connection().await?;
    f(&mut conn).await
}

// Usage
with_connection(|conn| async move {
    query("SELECT * FROM users").fetch_all(conn).await
}).await?;
```

### Pattern 2: GAT + Object Safety

<!-- huiali-source: skills/rust-lifetime-complex/SKILL.md#rust-block-2; sha256=52d64796aa7728820354af054a34da93a05adaf77e6a798d6ad80e1b028f5b6c -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Problem: GAT makes trait non-object-safe

// ❌ Can't use dyn with GAT
trait Repository {
    type Row<'a>: RowView<'a>;  // GAT
    fn query<'a>(&'a self) -> Vec<Self::Row<'a>>;
}
// let repo: Box<dyn Repository> = ...;  // Error!

// ✅ Solution: Layered architecture
trait InternalRepo {
    type Row<'a>: RowView<'a>;  // GAT for internal use
    fn query_borrowed<'a>(&'a self) -> Vec<Self::Row<'a>>;
}

trait PublicRepo: Send + Sync {
    fn query(&self) -> Vec<RowDto>;  // Owned data
}

// Adapter converts borrowed -> owned
impl<T: InternalRepo> PublicRepo for T {
    fn query(&self) -> Vec<RowDto> {
        self.query_borrowed()
            .into_iter()
            .map(|row| row.to_dto())
            .collect()
    }
}
```

### Pattern 3: Static Bound Conflicts

<!-- huiali-source: skills/rust-lifetime-complex/SKILL.md#rust-block-3; sha256=e5059effdb56660d0b7662bed9c33eadfd9d01276498e31f2375fe66fee7a30e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Problem: 'static requirement conflicts with borrowing

// ❌ Can't borrow when 'static required
async fn bad_resolver(&self, ctx: &Context) -> Result<&Data> {
    // Error: lifetime 'a not 'static
}

// ✅ Solution: Return owned data
async fn good_resolver(&self, ctx: &Context) -> Result<DataDto> {
    let borrowed = self.repo.query().await?;
    Ok(borrowed.to_owned_dto())
}

// Alternative: Use Arc for shared ownership
async fn shared_resolver(&self) -> Result<Arc<Data>> {
    Ok(Arc::clone(&self.cached_data))
}
```

### Pattern 4: Lifetime Elision Edge Cases

<!-- huiali-source: skills/rust-lifetime-complex/SKILL.md#rust-block-4; sha256=13a7d86611ad3e738adb042ebfc674f1cfde2bcc0fa6c3d5ba49aad243f75bc3 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Problem: Compiler can't infer lifetime

// ❌ Ambiguous lifetime
struct Parser<'a> {
    input: &'a str,
}

impl<'a> Parser<'a> {
    fn parse(&self) -> Result<&str, Error> {
        // Which lifetime? 'a or 'self?
        // Compiler can't tell
    }
}

// ✅ Explicit lifetime annotation
impl<'a> Parser<'a> {
    fn parse<'b>(&'b self) -> Result<&'a str, Error> {
        // Returns data from input, not self
        Ok(&self.input[..10])
    }
}
```

### Pattern 5: Async + Lifetime Conflicts

<!-- huiali-source: skills/rust-lifetime-complex/SKILL.md#rust-block-5; sha256=d9b2e3275719000c88fec9f20845522d4883962870413f4854870a916561d9d6 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Problem: Holding references across await

// ❌ Can't hold borrow across await
async fn bad_async() {
    let data = get_data();
    let borrowed = &data.field;

    some_async_call().await;  // Error: data might move

    use_borrowed(borrowed);
}

// ✅ Solution 1: Clone before await
async fn good_async_clone() {
    let data = get_data();
    let owned = data.field.clone();

    some_async_call().await;  // OK

    use_owned(&owned);
}

// ✅ Solution 2: Drop borrow before await
async fn good_async_scope() {
    let data = get_data();
    let value = {
        let borrowed = &data.field;
        extract_value(borrowed)
    };  // borrow dropped

    some_async_call().await;  // OK
}
```


## Common Conflict Patterns

| Pattern | Cause | Solution |
|---------|-------|----------|
| HRTB → dyn | Concrete vs universal lifetime | Use generic functions |
| GAT → dyn | Variable-sized associated types | Layered design with owned DTOs |
| 'static + borrow | Lifetime contradiction | Return owned data |
| Async + borrow | Future holds state across await | Clone or drop before await |
| Closure capture + Send | Lifetime issues | Use 'static or Arc |


## When to Give Up Borrowing

### Performance vs Maintainability

<!-- huiali-source: skills/rust-lifetime-complex/SKILL.md#rust-block-6; sha256=cc9b37bc100435652c353958d741083376a20239aa96a702157f0198765f812d -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Decision factors:
fn should_use_owned() -> bool {
    // ✅ Use owned if:
    // - Complex lifetime interactions
    // - API boundaries
    // - Async contexts
    // - Multi-threaded sharing

    // ✅ Keep borrowing if:
    // - Large data structures
    // - Hot path performance
    // - Simple lifetime relationships
    // - Internal implementation only

    true
}
```

### Rule of Thumb

1. **API layer**: Default to owned data
2. **Internal impl**: Borrow when beneficial
3. **Performance hotspot**: Profile first, then optimize
4. **High complexity**: Fall back to owned


## Workflow

### Step 1: Diagnose Error

```
Common errors:
  "one type is more general" → HRTB + dyn conflict
  "lifetime may not live long enough" → Borrow exceeds scope
  "cannot be made into object" → GAT or HRTB in trait
  "does not live long enough" → Early drop
```

### Step 2: Choose Strategy

```
Options:
  → Simplify: Remove abstraction
  → Split: Separate borrowed/owned layers
  → Clone: Accept allocation cost
  → Arc: Shared ownership
  → Redesign: Change data flow
```

### Step 3: Validate Solution

```
Check:
  → Compiles without hacky workarounds
  → Reasonable complexity
  → Performance acceptable
  → Maintainable long-term
```


## Debugging Techniques

### Minimize

<!-- huiali-source: skills/rust-lifetime-complex/SKILL.md#rust-block-7; sha256=e0493b55c1f8bf3414f57ca8f915d89b087f0a3f5454a6fdd4c68f83853670f3 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Reduce to minimal reproduction
// Remove generics, traits, async one by one
// Find the core conflict
```

### Explicit Lifetimes

<!-- huiali-source: skills/rust-lifetime-complex/SKILL.md#rust-block-8; sha256=9c2eadc963116e5cebc436a46d97cfdc5bc33e574ee1e777a184cc7d8689f17f -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Write out all lifetime parameters
// Makes relationships visible
fn explicit<'a, 'b>(x: &'a str, y: &'b str) -> &'a str {
    x
}
```

### Accept Reality

<!-- huiali-source: skills/rust-lifetime-complex/SKILL.md#rust-block-9; sha256=cee43fed08edae12b235ce4e74a8dd307a79efd788e7513d883279ed7dae6fb2 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Not all designs can compile
// Sometimes owned data is the answer
// Complexity has limits
```


## Review Checklist

When dealing with complex lifetimes:

- [ ] HRTB not used with dyn trait objects
- [ ] GAT traits have owned alternative for object safety
- [ ] 'static bounds justified and documented
- [ ] Async functions don't hold borrows across await
- [ ] Lifetime elision not hiding ambiguity
- [ ] Complex lifetimes have explicit annotations
- [ ] Considered owned data alternative
- [ ] Design simplification explored first


## Verification Commands

```bash
# Check for lifetime errors
cargo check

# Expand to see generated code
cargo expand

# Verify no borrow checker issues
cargo clippy
```


## Related Skills

- **rust-ownership** - Basic lifetime fundamentals
- **rust-async** - Async lifetime patterns
- **rust-type-driven** - Type-level design
- **rust-trait** - Trait object constraints
- **rust-performance** - When to optimize with borrowing

## Additional unique source examples

These code-only deltas appeared in the condensed English or localized source. They remain fragments, not dependency or hardware claims.

### `SKILL_ZH.md` example 1

<!-- huiali-source: skills/rust-lifetime-complex/SKILL_ZH.md#rust-block-1; sha256=7d2e94573ecc935aa02379b891b1b9db41ecfd11b937e0477b5634acca024f02 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ HRTB 不能装进 dyn trait object
pub type ConnFn<T> =
    dyn for<'c> FnOnce(&'c mut PgConnection) -> BoxFuture<'c, T> + Send;

let f = Box::new(move |conn: &mut PgConnection| -> BoxFuture<'_, i64> {
    Box::pin(async { Ok(42) })
}) as Box<ConnFn<i64>>;  // ❌ "one type is more general than the other"
```

### `SKILL_ZH.md` example 2

<!-- huiali-source: skills/rust-lifetime-complex/SKILL_ZH.md#rust-block-2; sha256=2ee0250054c72829d8d330caaf93b4e57e58d13d60e43c1a8ca8338403174de3 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ HRTB 只在调用点使用泛型
impl Db {
    pub async fn with_conn<F, T, Fut>(&self, f: F) -> Result<T, DbError>
    where
        F: for<'c> FnOnce(&'c mut PgConnection) -> Fut + Send,
        Fut: Future<Output = Result<T, DbError>> + Send,
    {
        let mut conn = self.pool.acquire().await?;
        f(&mut conn).await
    }
}
```

### `SKILL_ZH.md` example 3

<!-- huiali-source: skills/rust-lifetime-complex/SKILL_ZH.md#rust-block-3; sha256=a7b5daa41d0bafa42f5c96e74ceeb80ed2e686a242a6720a35c856d7a52322b7 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
db.with_conn(|conn| async move {
    // 这里 'c 由调用时确定，不需要 dyn
    sqlx::query("...").fetch_all(conn).await
}).await
```

### `SKILL_ZH.md` example 4

<!-- huiali-source: skills/rust-lifetime-complex/SKILL_ZH.md#rust-block-4; sha256=f056e37a813846ba6a43138c93d0abfad2136004b003de2790528294082cbf82 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ GAT 不能和 dyn Trait 一起用
trait ReportRepo: Send + Sync {
    type Row<'r>: RowView<'r>;  // ❌ GAT
}

let repo: Arc<dyn ReportRepo> = ...;  // ❌ 编译错误
```

### `SKILL_ZH.md` example 5

<!-- huiali-source: skills/rust-lifetime-complex/SKILL_ZH.md#rust-block-5; sha256=2e28a2e90eb4d22065f598622287c3e9c5d9940242cc4592a32d7f50395dca12 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 内部：GAT + 借用（高性能）
trait InternalRepo {
    type Row<'r>: RowView<'r>;
    async fn query<'c>(&'c self) -> Vec<Self::Row<'c>>;
}

// 外部：owned DTO（兼容 GraphQL）
pub trait PublicRepo: Send + Sync {
    async fn query(&self) -> Vec<ReportDto>;  // owned
}

// 适配层
impl PublicRepo for PgRepo {
    async fn query(&self) -> Vec<ReportDto> {
        let rows = self.internal.query().await;  // 借用内部
        rows.into_iter().map(|r| r.to_dto()).collect()
    }
}
```

### `SKILL_ZH.md` example 6

<!-- huiali-source: skills/rust-lifetime-complex/SKILL_ZH.md#rust-block-6; sha256=4727049492fd74ea1d9f08ee0d5308451cc1c51415bc00aac73a52a7dab2767b -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// async-graphql 要求 schema 是 'static
// 但 repo 方法返回借用数据
async fn resolve(&self) -> Result<&'r Row<'r>> {
    // ❌ 'r 不能 outlive 'static
}
```

### `SKILL_ZH.md` example 7

<!-- huiali-source: skills/rust-lifetime-complex/SKILL_ZH.md#rust-block-7; sha256=636fee7b382257da2b5d7ce7e0e2ab29aa4bc3ea6d9b2f64f0bcdcfb046eee16 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 不要在 API 层暴露借用
async fn resolve(&self) -> Result<ReportDto> {
    let row = self.repo.query().await?;  // owned
    Ok(row.to_dto())
}
```

### `SKILL_ZH.md` example 8

<!-- huiali-source: skills/rust-lifetime-complex/SKILL_ZH.md#rust-block-8; sha256=912e96f1b2a9691c39acfd7505d0512869c076efd6c9e041b182912f8043495f -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 性能收益 vs 复杂性
fn should_borrow() -> bool {
    // 大数据结构 → 借用
    // 高频访问 → 借用
    // 生命周期简单 → 借用

    // 复杂生命周期 → owned
    // API 边界 → owned
    // 异步上下文 → owned
}
```
