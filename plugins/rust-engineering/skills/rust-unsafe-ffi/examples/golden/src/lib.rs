//! A tiny C ABI with explicit null policy and no unwinding.

#[no_mangle]
pub unsafe extern "C" fn sum_u32(values: *const u32, len: usize, out: *mut u64) -> bool {
    if out.is_null() || (values.is_null() && len != 0) { return false; }
    // SAFETY: `values` is either non-null for `len` initialized elements or len is zero;
    // `out` was checked non-null and the C contract requires it to be writable.
    let slice = if len == 0 { &[] } else { unsafe { std::slice::from_raw_parts(values, len) } };
    unsafe { out.write(slice.iter().map(|&value| u64::from(value)).sum()) };
    true
}

#[cfg(test)]
mod tests {
    #[test]
    fn validates_null_and_empty_inputs() {
        let mut out = 99;
        assert!(unsafe { super::sum_u32(std::ptr::null(), 0, &mut out) });
        assert_eq!(out, 0);
        assert!(!unsafe { super::sum_u32(std::ptr::null(), 1, &mut out) });
    }
}
