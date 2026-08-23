# Huiali Zero Cost Protocol

> Product adaptation of `skills/rust-zero-cost/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-performance`.
- Supporting profiles when needed: `$rust-traits`, `$rust-stable`.
- Scope retained: Static versus dynamic dispatch, monomorphization, iterators, abstraction boundaries, code size, allocation, and measured runtime cost.
- Baseline correction: Zero-cost means an abstraction should not impose avoidable runtime overhead relative to a suitable manual implementation; it does not promise zero compile time, code size, allocation, or all-purpose performance.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## 泛型 vs Trait Object

| 特性 | 泛型 (static dispatch) | trait object (dynamic dispatch) |
|-----|----------------------|--------------------------------|
| 性能 | 零开销 | vtable 查找 |
| 代码大小 | 可能膨胀 | 更小 |
| 编译时间 | 更长 | 更短 |
| 灵活性 | 类型必须已知 | 运行时决定 |
| 异构集合 | 不支持 | `Vec<Box<dyn Trait>>` |


## 何时用泛型

<!-- huiali-source: skills/rust-zero-cost/SKILL.md#rust-block-1; sha256=25cac31b55740fe6b063c3ddea5e30fdf6326e9e784384bfe68fd1c094fbde4b -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 类型在编译时已知
fn process<T: Processor>(item: T) {
    item.process();
}

// 返回同一类型
fn create_processor() -> impl Processor {
    // 返回具体类型
}

// 多个类型参数
fn combine<A: Display, B: Display>(a: A, b: B) -> String {
    format!("{} and {}", a, b)
}
```


## 何时用 trait object

<!-- huiali-source: skills/rust-zero-cost/SKILL.md#rust-block-2; sha256=e1986e926f6ef9bd2cc3bbe7258a0650ccfec7927af8d0355ff7659c26967154 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 运行时决定类型
trait Plugin {
    fn run(&self);
}

struct PluginManager {
    plugins: Vec<Box<dyn Plugin>>,
}

// 异构集合
let handlers: Vec<Box<dyn Handler>> = vec![
    Box::new(HttpHandler),
    Box::new(GrpcHandler),
];
```


## 对象安全规则

<!-- huiali-source: skills/rust-zero-cost/SKILL.md#rust-block-3; sha256=13d90fbcb77919227f1279bc1fca395f908c62bf495eb6b31bb56795911157f3 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ 不是对象安全的
trait Bad {
    fn create(&self) -> Self;  // 返回 Self
    fn method(&self, x: Self);  // 参数有 Self
}

// ✅ 对象安全
trait Good {
    fn name(&self) -> &str;
}
```


## impl Trait vs dyn Trait

<!-- huiali-source: skills/rust-zero-cost/SKILL.md#rust-block-4; sha256=bff0fb94e7fcaac46cb8a43379c20a8654c4c4ee18d832155ebc6f3378546dd8 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// impl Trait：返回具体类型（静态分发）
fn create_processor() -> impl Processor {
    HttpProcessor
}

// dyn Trait：返回 trait object（动态分发）
fn create_processor() -> Box<dyn Processor> {
    Box::new(HttpProcessor)
}
```


## 性能影响

<!-- huiali-source: skills/rust-zero-cost/SKILL.md#rust-block-5; sha256=4d53b303e278d1dd9b8e9f00a14fb29e2d54a493032ad28515fdfa6d3338b182 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 泛型：每个类型生成一份代码
fn process<T: Trait>(item: T) {
    item.method();
}
// 编译后：
// fn process_Http(item: Http) { ... }
// fn process_Ftp(item: Ftp) { ... }

// trait object：单一路径
fn process(item: &dyn Trait) {
    item.method();  // 通过 vtable 调用
}
```


## 常见错误

| 错误 | 原因 | 解决 |
|-----|------|-----|
| E0277 | 缺少 trait bound | 添加 `T: Trait` |
| E0038 | trait object 不安全 | 检查对象安全规则 |
| E0308 | 类型不匹配 | 统一类型或用泛型 |
| E0599 | 未找到实现 | 实现 trait 或检查约束 |


## 优化策略

1. **热点代码用泛型** - 消除动态分发开销
2. **插件系统用 dyn** - 灵活性优先
3. **小集合用泛型** - 避免 Box 分配
4. **大集合用 dyn** - 减少代码膨胀
