# Huiali Resource Protocol

> Product adaptation of `skills/rust-resource/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-ownership`.
- Supporting profiles when needed: `$rust-errors`, `$rust-concurrency`.
- Scope retained: RAII, smart-pointer selection, pools, guards, acquisition ordering, partial construction, cleanup, and cancellation-safe release.
- Baseline correction: Make ownership and cleanup paths explicit, including partial failure and cancellation. Pools and shared ownership are optimizations or coordination tools, not defaults.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## 选择决策树

```
需要共享数据吗？
    │
    ├─ 否 → 单 owner
    │   ├─ 需要堆分配？ → Box<T>
    │   └─ 栈上即可？ → 直接值类型
    │
    └─ 是 → 需要共享
          │
          ├─ 单线程？
          │   ├─ 可变？ → Rc<RefCell<T>>
          │   └─ 只读？ → Rc<T>
          │
          └─ 多线程？
                ├─ 可变？ → Arc<Mutex<T>> 或 Arc<RwLock<T>>
                └─ 只读？ → Arc<T>
```


## 智能指针对比

| 类型 | 所有权 | 线程安全 | 适用场景 |
|-----|-------|---------|---------|
| `Box<T>` | 单 owner | Yes | 堆分配、递归类型、trait object |
| `Rc<T>` | 共享 | No | 单线程共享、避免 clone |
| `Arc<T>` | 共享 | Yes | 多线程共享、只读数据 |
| `Weak<T>` | 弱引用 | - | 打破循环引用 |
| `RefCell<T>` | 单 owner | No | 运行时借用检查 |
| `Cell<T>` | 单 owner | No | Copy 类型的内部可变性 |


## 常见错误与解决方案

### Rc 循环引用泄漏

<!-- huiali-source: skills/rust-resource/SKILL.md#rust-block-1; sha256=97bb582449414770d220f498231497a9822f5419e152f5b960f0b0a1fda94c35 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ 内存泄漏：两个 Rc 互相引用
struct Node {
    value: i32,
    next: Option<Rc<Node>>,
}

// ✅ 解决方案：使用 Weak 打破循环
struct Node {
    value: i32,
    next: Option<Weak<Node>>,
}
```

### RefCell panic

<!-- huiali-source: skills/rust-resource/SKILL.md#rust-block-2; sha256=6ce8f2727d07c39303c8c770649172cb0b39070521cd75fe9b52e37b3de65ff1 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ 运行时 panic：双重可变借用
let cell = RefCell::new(vec![1, 2, 3]);
let mut_borrow = cell.borrow_mut();
let another_borrow = cell.borrow(); // panic!

// ✅ 解决方案：使用 try_borrow
if let Ok(mut_borrow) = cell.try_borrow_mut() {
    // 安全使用
}
```

### Arc 开销投诉

<!-- huiali-source: skills/rust-resource/SKILL.md#rust-block-3; sha256=6148f7de6c8b505b059944801f2446f4612ac5718d8fc6459205398c5d1f4279 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ 不必要的 Arc：单线程环境
let shared = Arc::new(data);

// ✅ 单线程用 Rc
let shared = Rc::new(data);

// ❌ 多线程不必要的原子操作
// 如果确定不需要跨线程共享，就不要用 Arc
```


## 内部可变性选择

<!-- huiali-source: skills/rust-resource/SKILL.md#rust-block-4; sha256=e604b6ed88979c53991e01ecad5a4844be2e06f5bc3c55d4d1e901e2b8bc05f7 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// T 是 Copy 类型 → Cell
struct Counter {
    count: Cell<u32>,
}

// T 不是 Copy → RefCell
struct Container {
    items: RefCell<Vec<Item>>,
}

// 多线程 → Mutex 或 RwLock
struct SharedContainer {
    items: Mutex<Vec<Item>>,
}
```


## RAII 与 Drop

<!-- huiali-source: skills/rust-resource/SKILL.md#rust-block-5; sha256=00d817975c6f3a67d17b32a96d5d99a7f386f9fccbc0422b4521cf8c215cde4a -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
struct File {
    handle: std::fs::File,
}

impl Drop for File {
    fn drop(&mut self) {
        // 自动释放资源
        println!("File closed");
    }
}

// 使用 guard pattern 确保清理
struct Guard<'a> {
    resource: &'a Resource,
}

impl Drop for Guard<'_> {
    fn drop(&mut self) {
        self.resource.release();
    }
}
```


## 性能提示

| 场景 | 建议 |
|-----|------|
| 大量小对象 | `Rc::make_mut()` 避免 clone |
| 频繁读取 | `RwLock` 比 `Mutex` 更好 |
| 计数器 | 用 `AtomicU64` 而非 `Mutex<u64>` |
| 缓存 | 考虑 `moka` 或 `cached` crate |


## 何时不用智能指针

- 栈上数据足够 → 用值类型
- 借用即可满足 → 用引用 `&T`
- 生命周期简单 → 不要过度抽象
