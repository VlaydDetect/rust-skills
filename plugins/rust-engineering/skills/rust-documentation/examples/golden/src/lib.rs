//! A documented value with a compiling caller example.

/// A non-negative count.
///
/// # Examples
///
/// ```
/// use golden_rust_documentation::Count;
/// let mut count = Count::new(2);
/// count.increment();
/// assert_eq!(count.get(), 3);
/// ```
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Count(u64);

impl Count {
    /// Constructs a count from an existing value.
    pub const fn new(value: u64) -> Self { Self(value) }
    /// Returns the current value.
    pub const fn get(self) -> u64 { self.0 }
    /// Increments unless the value is already `u64::MAX`.
    pub fn increment(&mut self) { self.0 = self.0.saturating_add(1); }
}
