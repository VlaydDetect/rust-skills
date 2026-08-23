# Huiali Const Protocol

> Product adaptation of `skills/rust-const/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-stable`.
- Supporting profiles when needed: `$rust-traits`, `$rust-performance`.
- Scope retained: Const evaluation, const fn, const generics, compile-time constraints, static data, and supported-toolchain limits.
- Baseline correction: The real project toolchain and MSRV determine available const features. Do not turn a current-stable or nightly capability into an unconditional product baseline.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## Solution Patterns

### Pattern 1: Basic Const Generics

<!-- huiali-source: skills/rust-const/SKILL.md#rust-block-1; sha256=87d429191a50f648196b2982a5e69a4d53c1e4468ca4f43ea1de0b89bb75873b -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Generic over array size
struct Buffer<T, const N: usize> {
    data: [T; N],
}

impl<T: Default + Copy, const N: usize> Buffer<T, N> {
    fn new() -> Self {
        Self {
            data: [T::default(); N],
        }
    }
}

// Usage
let buf: Buffer<u8, 1024> = Buffer::new();
```

### Pattern 2: Const Functions

<!-- huiali-source: skills/rust-const/SKILL.md#rust-block-2; sha256=6c87109d0421dd9dd526b93b8285fe27f69a78a2110d9970edf721e925ca8942 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
const fn fibonacci(n: u32) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => {
            let mut a = 0;
            let mut b = 1;
            let mut i = 2;
            while i <= n {
                let tmp = a + b;
                a = b;
                b = tmp;
                i += 1;
            }
            b
        }
    }
}

// Computed at compile time
const FIB_10: u64 = fibonacci(10);

// Also works in array sizes
const ARRAY: [u8; fibonacci(5) as usize] = [0; fibonacci(5) as usize];
```

### Pattern 3: MaybeUninit for Large Arrays

<!-- huiali-source: skills/rust-const/SKILL.md#rust-block-3; sha256=f09117cbbe29dfbd42c1074bef393d9b537935f3d788b5054f1c475a04749c56 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::mem::MaybeUninit;

// Stack overflow risk for large arrays
fn bad_large_array() -> [u8; 1024 * 1024] {
    [0; 1024 * 1024]  // Stack overflow!
}

// ✅ Good: Use heap
fn good_large_array() -> Box<[u8; 1024 * 1024]> {
    Box::new([0; 1024 * 1024])
}

// ✅ Good: MaybeUninit for uninitialized memory
fn uninit_array<const N: usize>() -> Box<[u8; N]> {
    let mut data: Box<[MaybeUninit<u8>; N]> =
        Box::new(unsafe { MaybeUninit::uninit().assume_init() });

    for elem in &mut data[..] {
        elem.write(0);
    }

    unsafe { Box::from_raw(Box::into_raw(data) as *mut [u8; N]) }
}
```

### Pattern 4: Compile-Time Validation

<!-- huiali-source: skills/rust-const/SKILL.md#rust-block-4; sha256=6403b7db3177994fc41ec33be6cd023d7598f8e9cf321f7562e91277f2e6021d -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
const fn validate_config(size: usize, alignment: usize) -> bool {
    size > 0 && alignment.is_power_of_two()
}

struct Config<const SIZE: usize, const ALIGN: usize> {
    _phantom: PhantomData<[u8; SIZE]>,
}

impl<const SIZE: usize, const ALIGN: usize> Config<SIZE, ALIGN> {
    const fn new() -> Self {
        assert!(validate_config(SIZE, ALIGN), "Invalid configuration");
        Self { _phantom: PhantomData }
    }
}

// Compile-time validation
const CONFIG: Config<1024, 8> = Config::new();
// const BAD: Config<0, 3> = Config::new();  // Compile error!
```

### Pattern 5: Type-Level State Machine

<!-- huiali-source: skills/rust-const/SKILL.md#rust-block-5; sha256=b6538281b1fb4f4bf743c4874eded6d5de4f14cdf9fe4c45442b8f672af0af35 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
struct Uninitialized;
struct Initialized;

struct StateMachine<State, const N: usize> {
    buffer: [u8; N],
    _state: PhantomData<State>,
}

impl<const N: usize> StateMachine<Uninitialized, N> {
    fn new() -> Self {
        Self {
            buffer: [0; N],
            _state: PhantomData,
        }
    }

    fn initialize(self) -> StateMachine<Initialized, N> {
        StateMachine {
            buffer: self.buffer,
            _state: PhantomData,
        }
    }
}

impl<const N: usize> StateMachine<Initialized, N> {
    fn process(&mut self) {
        // Only available when initialized
    }
}
```


## Const Fn Capabilities

### What Works in Const Fn

<!-- huiali-source: skills/rust-const/SKILL.md#rust-block-6; sha256=0227c71bbf7e5e0147fbb9c531f7cce9c6ce9fb664b404b3e20f94e6cafed301 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
const fn works() {
    // ✅ Arithmetic
    let x = 1 + 2;

    // ✅ Conditionals
    if x > 0 { }

    // ✅ Loops
    let mut i = 0;
    while i < 10 { i += 1; }

    // ✅ Match
    match x {
        0 => {},
        _ => {},
    }

    // ✅ Calling other const fn
    const fn helper() -> i32 { 42 }
    let y = helper();
}
```

### Current Limitations

<!-- huiali-source: skills/rust-const/SKILL.md#rust-block-7; sha256=88fe1149c40de2a24718d2bd833c2d507036258e58afed154e996b7651ccd469 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
const fn limitations() {
    // ❌ Heap allocation (not yet stable)
    // let v = Vec::new();

    // ❌ Trait objects
    // let obj: &dyn Trait = ...;

    // ❌ Mutable references in const (limited)
    // let mut x = 5;
    // let r = &mut x;

    // ❌ Floating point (improving)
    // const F: f64 = 3.14;
}
```


## Workflow

### Step 1: Identify Const Opportunities

```
Can be const if:
  → Value known at compile time
  → No heap allocation needed
  → No dynamic dispatch
  → Pure computation (no I/O)
```

### Step 2: Choose Pattern

```
Need:
  → Fixed-size array? Const generic
  → Compile-time computation? Const fn
  → Large array? MaybeUninit + Box
  → Validation? Const assertion
  → Type-level state? PhantomData + const generic
```

### Step 3: Verify Benefits

```
Const advantages:
  ✅ Zero runtime cost
  ✅ Compile-time validation
  ✅ Better optimization
  ✅ Smaller binary (sometimes)

Drawbacks:
  ❌ Longer compile time
  ❌ Limited feature set
  ❌ Complex error messages
```


## Review Checklist

When using const:

- [ ] Computation actually benefits from compile-time execution
- [ ] No stack overflow from large arrays
- [ ] MaybeUninit used correctly for uninitialized memory
- [ ] Const fn doesn't violate limitations
- [ ] Compile-time assertions provide useful errors
- [ ] Generic const parameters reasonably bounded
- [ ] Not overusing const (readability tradeoff)


## Verification Commands

```bash
# Check const evaluation
cargo build --release
cargo asm my_module::my_const_fn

# Verify array sizes
cargo check

# Test const assertions
cargo test --lib
```


## Common Pitfalls

### 1. Stack Overflow

**Symptom**: Segmentation fault

<!-- huiali-source: skills/rust-const/SKILL.md#rust-block-8; sha256=d67d8cfd2c1e4938e9d5789fc084e9b732c537801136f1f7fad5410f07255c59 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: large array on stack
let arr = [0u8; 1024 * 1024];  // Stack overflow!

// ✅ Good: heap allocation
let arr = Box::new([0u8; 1024 * 1024]);
```

### 2. Uninitialized Memory

**Symptom**: Undefined behavior

<!-- huiali-source: skills/rust-const/SKILL.md#rust-block-9; sha256=797678514fb6c43637530ac9a0e3614731e8f1188e69ef118db0e44837f7f3f1 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: reading uninitialized
let mut arr: [u8; 100];
println!("{}", arr[0]);  // UB!

// ✅ Good: explicit initialization
let arr = [0u8; 100];
```

### 3. Const Generic Mismatch

**Symptom**: Type mismatch errors

<!-- huiali-source: skills/rust-const/SKILL.md#rust-block-10; sha256=357d7357ee4f4107145870a3facdd4db023642ddc6a460282bbd8a4b55dfb0bd -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: mismatched sizes
fn process<const N: usize>(data: [u8; N]) {
    let other: [u8; 10] = data;  // Error if N != 10
}

// ✅ Good: use generic consistently
fn process<const N: usize>(data: [u8; N]) -> [u8; N] {
    data
}
```


## Related Skills

- **rust-type-driven** - Type-level programming
- **rust-performance** - Zero-cost abstractions
- **rust-unsafe** - MaybeUninit safety
- **rust-macro** - Compile-time code generation

## Additional unique source examples

These code-only deltas appeared in the condensed English or localized source. They remain fragments, not dependency or hardware claims.

### `SKILL_EN.md` example 1

<!-- huiali-source: skills/rust-const/SKILL_EN.md#rust-block-1; sha256=d15c1ec0d69e491af25c1dccf8f71c284fa7369bf08b74608e0f68414a782765 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
pub struct RingBuf<T, const N: usize> {
    data: [Option<T>; N],
    head: usize,
    tail: usize,
}
```

### `SKILL_EN.md` example 2

<!-- huiali-source: skills/rust-const/SKILL_EN.md#rust-block-2; sha256=f0ef2d7f7123f2568e4ec3e2aaa811806bfeeb4acf4ab6a6b5b6616ca2d2eedc -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
pub struct Block<const SIZE: usize>;

impl<const SIZE: usize> Block<SIZE> {
    pub const fn validate() {
        assert!(SIZE.is_power_of_two());
    }
}
```

### `SKILL_ZH.md` example 1

<!-- huiali-source: skills/rust-const/SKILL_ZH.md#rust-block-1; sha256=590fa9befbcf57aabe087caf71d968eb69d651d3d0c9f69e1e4b9da8463ceb89 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
struct Array<T, const N: usize> {
    data: [T; N],
}

let arr: Array<i32, 5> = Array { data: [0; 5] };
```

### `SKILL_ZH.md` example 2

<!-- huiali-source: skills/rust-const/SKILL_ZH.md#rust-block-2; sha256=da9789694487552fd28de9b92a0cb9d34e87ca37e46a40ce685ea3d9971f9a99 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 栈上固定大小数组
let arr: [i32; 100] = [0; 100];

// MaybeUninit 用于未初始化内存
use std::mem::MaybeUninit;
let mut arr: [MaybeUninit<i32>; 100] = [MaybeUninit::uninit(); 100];

// 初始化后使用
unsafe {
    let arr: [i32; 100] = arr.map(|x| x.assume_init());
}
```

### `SKILL_ZH.md` example 3

<!-- huiali-source: skills/rust-const/SKILL_ZH.md#rust-block-3; sha256=8c93621cd81fd94fdee6749640c1717848f6adbc48510d411e649f9575c6385b -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
const fn double(x: i32) -> i32 {
    x * 2
}

const VAL: i32 = double(5);  // 编译时计算

// 编译时检查
const fn checked_div(a: i32, b: i32) -> i32 {
    assert!(b != 0, "division by zero");
    a / b
}
```

### `SKILL_ZH.md` example 4

<!-- huiali-source: skills/rust-const/SKILL_ZH.md#rust-block-4; sha256=d94c71eea837863b17d5bc461b379c7446b4d2adc9680375480cf112bc508e79 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 有些操作 const fn 还不能做
const fn heap_alloc() -> Vec<i32> {
    Vec::new()  // ❌ 还不支持
}

const fn dynamic_size(n: usize) -> [i32; n] {
    // ❌ 数组大小必须是 const
    [0; n]
}
```

### `SKILL_ZH.md` example 5

<!-- huiali-source: skills/rust-const/SKILL_ZH.md#rust-block-5; sha256=023b211dc54b3d920a54e7dbf0b4986d40c3f529ae7477a7c3edbf1a1b5d2e72 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 数组长度检查
const fn assert_len<T>(slice: &[T], len: usize) {
    assert!(slice.len() == len);
}

// 使用
const _: () = assert_len(&[1, 2, 3], 3);  // 编译时断言

// 类型级状态机
struct StateMachine<S: State> {
    data: Vec<u8>,
    _phantom: std::marker::PhantomData<S>,
}

trait State {}
struct Initial;
struct Processing;
struct Done;

impl StateMachine<Initial> {
    fn start(self) -> StateMachine<Processing> {
        StateMachine {
            data: vec![],
            _phantom: std::marker::PhantomData,
        }
    }
}
```

### `SKILL_ZH.md` example 6

<!-- huiali-source: skills/rust-const/SKILL_ZH.md#rust-block-6; sha256=7f77fb864ee48f37c050aad7a62e5e16095f697afad9f1a4c2b6502fdd4323bc -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 安全初始化模式
fn init_array<T: Default + Copy>(len: usize) -> Vec<T> {
    let mut vec = Vec::with_capacity(len);
    for _ in 0..len {
        unsafe {
            vec.as_mut_ptr().write(T::default());
        }
    }
    unsafe {
        vec.set_len(len);
    }
    vec
}

// 大数组：栈可能溢出
fn big_array_on_heap() -> Box<[u8; 1024 * 1024]> {
    Box::new([0; 1024 * 1024])
}
```
