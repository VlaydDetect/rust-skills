# Specialized Rust Ffi Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Primary owner: `$rust-unsafe-ffi`.
- Supporting profiles when needed: `$rust-unsafe`, `$rust-ownership`.
- Scope retained: ABI layout, ownership transfer, allocator pairing, strings, callbacks, panic containment, handles, and foreign-thread behavior.
- Baseline correction: Validate the actual foreign ABI and target. repr(C), raw pointers, and a safety comment are inputs to a proof, not a complete proof.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

## Binding Generation

### C/C++ → Rust (bindgen)

```bash
# Auto-generate bindings
bindgen input.h \
    --output src/bindings.rs \
    --allowlist-type 'my_*' \
    --allowlist-function 'my_*'
```

### Rust → C (cbindgen)

```bash
# Generate C header
cbindgen --crate mylib --output include/mylib.h
```


## Solution Patterns

### Pattern 1: Calling C Functions<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::ffi::{CStr, CString};
use libc::c_int;

#[link(name = "curl")]
extern "C" {
    fn curl_version() -> *const libc::c_char;
    fn curl_easy_perform(curl: *mut c_int) -> c_int;
}

// ✅ Safe wrapper
fn get_version() -> String {
    unsafe {
        let ptr = curl_version();
        // SAFETY: curl_version returns valid null-terminated string
        CStr::from_ptr(ptr).to_string_lossy().into_owned()
    }
}
```

### Pattern 2: String Passing<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ Safe way to pass strings
fn process_c_string(s: &CStr) {
    // SAFETY: s is a valid CStr, ptr is valid for call duration
    unsafe {
        some_c_function(s.as_ptr());
    }
}

// Creating CString from Rust
fn get_c_string() -> Result<CString, std::ffi::NulError> {
    CString::new("hello")
}

// ❌ Dangerous: temporary CString
// let ptr = CString::new("hello").unwrap().as_ptr();  // Dangling!

// ✅ Correct: keep CString alive
let c_str = CString::new("hello")?;
let ptr = c_str.as_ptr();
// use ptr...
// c_str dropped here
```

### Pattern 3: Callback Functions<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
extern "C" fn callback(data: *mut libc::c_void) {
    // SAFETY: data must be a valid pointer to UserData
    // Caller guarantees this invariant
    unsafe {
        let user_data: &mut UserData = &mut *(data as *mut UserData);
        user_data.count += 1;
    }
}

fn register_callback(callback: extern "C" fn(*mut c_void), data: *mut c_void) {
    unsafe {
        some_c_lib_register(callback, data);
    }
}
```

### Pattern 4: C++ Interop with cxx<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Using cxx for safe C++ FFI
use cxx::CxxString;

#[cxx::bridge]
mod ffi {
    unsafe extern "C++" {
        include!("my_library.h");

        type MyClass;

        fn do_something(&self, input: i32) -> i32;
        fn get_data(&self) -> &CxxString;
    }
}

struct RustWrapper {
    inner: cxx::UniquePtr<ffi::MyClass>,
}

impl RustWrapper {
    pub fn new() -> Self {
        Self {
            inner: ffi::create_my_class(),
        }
    }

    pub fn do_something(&self, input: i32) -> i32 {
        self.inner.do_something(input)
    }
}
```


## Data Type Mapping

| Rust | C | Notes |
|------|---|-------|
| `i32` | `int` | Usually matches |
| `i64` | `long long` | Platform-dependent |
| `usize` | `uintptr_t` | Pointer-sized |
| `*const T` | `const T*` | Read-only |
| `*mut T` | `T*` | Mutable |
| `&CStr` | `const char*` | UTF-8 guaranteed |
| `CString` | `char*` | Ownership transfer |
| `NonNull<T>` | `T*` | Non-null pointer |
| `Option<NonNull<T>>` | `T*` (nullable) | Nullable pointer |


## Error Handling

### C Error Codes<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
fn call_c_api() -> Result<(), Box<dyn std::error::Error>> {
    // SAFETY: c_function is properly initialized
    let result = unsafe { c_function_that_returns_int() };
    if result < 0 {
        return Err(format!("C API error: {}", result).into());
    }
    Ok(())
}
```

### Panic Across FFI<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Panics across FFI boundary = UB
// Must catch or prevent

#[no_mangle]
pub extern "C" fn safe_call() -> i32 {
    let result = std::panic::catch_unwind(|| {
        rust_code_that_might_panic()
    });

    match result {
        Ok(value) => value,
        Err(_) => -1,  // Error code
    }
}
```

### C++ Exceptions<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// C++ exceptions → Rust panic (with cxx)
// Must catch at FFI boundary

#[no_mangle]
pub extern "C" fn safe_cpp_call(error_code: *mut i32) -> *const c_char {
    let result = std::panic::catch_unwind(|| {
        unsafe { cpp_function() }
    });

    match result {
        Ok(Ok(value)) => value.as_ptr(),
        Ok(Err(e)) => {
            if !error_code.is_null() {
                unsafe { *error_code = e.code(); }
            }
            std::ptr::null()
        }
        Err(_) => {
            if !error_code.is_null() {
                unsafe { *error_code = -999; }
            }
            std::ptr::null()
        }
    }
}
```


## Memory Management

| Scenario | Who Frees | How |
|----------|-----------|-----|
| C allocates, Rust uses | C | Don't free from Rust |
| Rust allocates, C uses | Rust | C notifies when done |
| Shared buffer | Agreed protocol | Document clearly |<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ Rust allocates, C borrows
#[no_mangle]
pub extern "C" fn create_buffer(len: usize) -> *mut u8 {
    let mut buf = vec![0u8; len];
    let ptr = buf.as_mut_ptr();
    std::mem::forget(buf);  // Don't drop
    ptr
}

#[no_mangle]
pub extern "C" fn free_buffer(ptr: *mut u8, len: usize) {
    unsafe {
        // SAFETY: ptr was allocated by create_buffer with this len
        let _ = Vec::from_raw_parts(ptr, len, len);
    }  // Vec dropped, memory freed
}
```


## Workflow

### Step 1: Choose FFI Strategy

```
Need to call C code?
  → Simple functions? Manual extern declarations
  → Complex API? Use bindgen
  → C++? Use cxx crate

Exporting to C?
  → Use cbindgen to generate headers
  → Mark functions #[no_mangle]
  → Use extern "C"
```

### Step 2: Define Safety Invariants

```
For every FFI call:
1. Document pointer validity requirements
2. Document lifetime expectations
3. Document thread safety assumptions
4. Document panic handling
```

### Step 3: Build Safe Wrapper

```
unsafe FFI calls
  ↓
Safe private functions (validate inputs)
  ↓
Safe public API (no unsafe visible)
```

### Step 4: Test Thoroughly

```bash
# Test with Miri
cargo +nightly miri test

# Memory safety check
valgrind ./target/release/program

# Cross-compile test
cargo build --target x86_64-unknown-linux-gnu
```


## Language-Specific Tools

| Language | Tool | Use Case |
|----------|------|----------|
| Python | **PyO3** | Python extensions |
| Java | **jni** | Android/JVM |
| Node.js | **napi-rs** | Node.js addons |
| C# | **csharp-bindgen** | .NET interop |
| Go | **cgo** | Go bridge |
| C++ | **cxx** | Safe C++ FFI |


## Common Pitfalls

| Pitfall | Consequence | Avoid By |
|---------|-------------|----------|
| String encoding error | Garbled text | Use CStr/CString |
| Lifetime mismatch | Use-after-free | Clear ownership |
| Cross-thread non-Send | Data race | Arc + Mutex |
| Fat pointer to C | Memory corruption | Flatten data |
| Missing #[no_mangle] | Symbol not found | Explicit export |
| Panic across FFI | UB | catch_unwind |


## Review Checklist

When reviewing FFI code:

- [ ] All extern functions have SAFETY comments
- [ ] String conversion uses CStr/CString properly
- [ ] Memory ownership is clearly documented
- [ ] No panics across FFI boundary (use catch_unwind)
- [ ] FFI types use #[repr(C)]
- [ ] Raw pointers validated before dereferencing
- [ ] Functions exported with #[no_mangle]
- [ ] Callbacks have correct ABI (extern "C")
- [ ] Tested with Miri for UB detection
- [ ] Documentation explains ownership protocol


## Verification Commands

```bash
# Check safety
cargo +nightly miri test

# Memory leaks
valgrind --leak-check=full ./target/release/program

# Generate bindings
bindgen wrapper.h --output src/ffi.rs

# Generate C header
cbindgen --lang c --output target/mylib.h

# Check exports
nm target/release/libmylib.so | grep my_function
```


## Safety Guidelines

1. **Minimize unsafe**: Only wrap necessary C calls
2. **Defensive programming**: Check null pointers, validate ranges
3. **Clear documentation**: Who owns memory, who frees it
4. **Test coverage**: FFI bugs are extremely hard to debug
5. **Use Miri**: Detect undefined behavior early


## Related Skills

- **rust-unsafe** - Unsafe code fundamentals
- **rust-ownership** - Memory and lifetime management
- **rust-coding** - Export conventions
- **rust-performance** - FFI overhead optimization
- **rust-web** - Using FFI in web services

## Additional unique source examples

These code-only deltas appeared in the condensed English or localized source. They remain fragments, not dependency or hardware claims.

### `SKILL_ZH.md` example 1<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::ffi::{CStr, CString};
use libc::c_int;

#[link(name = "curl")]
extern "C" {
    fn curl_version() -> *const libc::c_char;
    fn curl_easy_perform(curl: *mut c_int) -> c_int;
}

fn get_version() -> String {
    unsafe {
        let ptr = curl_version();
        CStr::from_ptr(ptr).to_string_lossy().into_owned()
    }
}
```

### `SKILL_ZH.md` example 2<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ Safe approach
fn process_c_string(s: &CStr) {
    unsafe {
        some_c_function(s.as_ptr());
    }
}

// When a String is required
fn get_c_string() -> CString {
    CString::new("hello").unwrap()
}
```

### `SKILL_ZH.md` example 3<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
extern "C" fn callback(data: *mut libc::c_void) {
    unsafe {
        let user_data: &mut UserData = &mut *(data as *mut UserData);
        user_data.count += 1;
    }
}

fn register_callback(callback: extern "C" fn(*mut c_void), data: *mut c_void) {
    unsafe {
        some_c_lib_register(callback, data);
    }
}
```

### `SKILL_ZH.md` example 4<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
fn call_c_api() -> Result<(), Box<dyn std::error::Error>> {
    let result = unsafe { c_function_that_returns_int() };
    if result < 0 {
        return Err(format!("C API error: {}", result).into());
    }
    Ok(())
}
```

### `SKILL_ZH.md` example 5<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Panics at an FFI boundary must be caught or prohibited
#[no_mangle]
pub extern "C" fn safe_call() {
    std::panic::catch_unwind(|| {
        rust_code_that_might_panic()
    }).ok();  // Ignore the panic
}
```

### `SKILL_ZH.md` example 6<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Use cxx for safe C++ FFI
use cxx::CxxString;
use cxx::CxxVector;

#[cxx::bridge]
mod ffi {
    unsafe extern "C++" {
        include!("my_library.h");

        type MyClass;

        fn do_something(&self, input: i32) -> i32;
        fn get_data(&self) -> &CxxString;
        fn process_vector(&self, vec: &CxxVector<i32>) -> i32;
    }

    #[namespace = "mylib"]
    unsafe extern "C++" {
        fn free_resource(ptr: *mut c_void);
    }
}

struct RustWrapper {
    ptr: *mut c_void,
}

impl RustWrapper {
    pub fn new() -> Self {
        unsafe {
            Self {
                ptr: mylib::create_object(),
            }
        }
    }

    pub fn do_something(&self, input: i32) -> i32 {
        unsafe {
            (*self.ptr).do_something(input)
        }
    }
}

impl Drop for RustWrapper {
    fn drop(&mut self) {
        unsafe {
            mylib::free_resource(self.ptr);
        }
    }
}
```

### `SKILL_ZH.md` example 7<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// An exception thrown by C++ becomes a Rust panic
// Catch it with catch_unwind

#[no_mangle]
pub extern "C" fn safe_cpp_call() -> i32 {
    let result = std::panic::catch_unwind(|| {
        unsafe {
            cpp_function_that_might_throw()
        }
    });

    match result {
        Ok(value) => value,
        Err(_) => {
            // The C++ exception was caught; return an error code
            -1
        }
    }
}

// Better approach: custom error conversion
#[no_mangle]
pub extern "C" fn checked_cpp_call(error_code: *mut i32) -> *const c_char {
    let result = std::panic::catch_unwind(|| {
        unsafe {
            cpp_function()
        }
    });

    match result {
        Ok(Ok(value)) => {
            // Success
            value.as_ptr()
        }
        Ok(Err(e)) => {
            // C++ error
            if !error_code.is_null() {
                unsafe { *error_code = e.code(); }
            }
            std::ptr::null()
        }
        Err(_) => {
            // C++ exception
            if !error_code.is_null() {
                unsafe { *error_code = -999; }
            }
            std::ptr::null()
        }
    }
}
```

### `SKILL_ZH.md` example 8<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Interaction between C++ stack unwinding and Rust is complex

// 1. Prevent panics from crossing the FFI boundary
#[no_mangle]
pub extern "C" fn rust_function() {
    // Rust code may panic,
    // but this can make C++ stack unwinding invoke Rust drop code,
    // potentially causing undefined behavior

    // Solution: catch_unwind
    let _ = std::panic::catch_unwind(|| {
        risky_rust_code()
    });
}

// 2. C++ destructors and Rust Drop
// C++ destructors run during stack unwinding
// Rust Drop implementations also run during a panic
// Combining the two can cause problems

// Solution: use ManuallyDrop
struct Wrapper {
    inner: ManuallyDrop<InnerType>,
}

impl Drop for Wrapper {
    fn drop(&mut self) {
        // Prevent double cleanup
        // The C++ destructor may still run, however
    }
}
```

### `SKILL_ZH.md` example 9<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Bridge std::unique_ptr with cxx
#[cxx::bridge]
mod ffi {
    unsafe extern "C++" {
        include!("memory");

        type UniquePtr<T>;

        // Transfer ownership: Rust → C++
        fn take_unique_ptr(ptr: Box<UniquePtr<T>>) -> *mut T;

        // Transfer ownership: C++ → Rust
        fn create_unique_ptr() -> Box<UniquePtr<T>>;
        fn release_unique_ptr(ptr: Box<UniquePtr<T>>) -> *mut T;
    }
}

// Bridge std::shared_ptr manually
struct SharedPtr<T> {
    ptr: *mut T,
    ref_count: usize,
}

impl<T> SharedPtr<T> {
    pub fn new(ptr: *mut T) -> Self {
        Self {
            ptr,
            ref_count: 1,
        }
    }

    pub fn clone(&mut self) {
        self.ref_count += 1;
    }

    pub fn drop(&mut self) {
        self.ref_count -= 1;
        if self.ref_count == 0 {
            unsafe {
                // Call C++ delete
                cpp_delete(self.ptr);
            }
        }
    }
}

unsafe impl<T> Send for SharedPtr<T> {}
unsafe impl<T> Sync for SharedPtr<T> {}
```
