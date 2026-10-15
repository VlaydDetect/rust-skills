//! Semantically equivalent implementations for a controlled benchmark fixture.

pub fn sum_squares_iterator(values: &[u64]) -> u64 {
    values.iter().copied().map(|value| value * value).sum()
}

pub fn sum_squares_loop(values: &[u64]) -> u64 {
    let mut total = 0;
    for &value in values {
        total += value * value;
    }
    total
}

/// Sums a validated prefix with defined overflow behavior.
pub fn sum_prefix_safe(values: &[u64], count: usize) -> Option<u64> {
    Some(
        values
            .get(..count)?
            .iter()
            .fold(0u64, |sum, value| sum.wrapping_add(*value)),
    )
}

/// Demonstrates the proof for unchecked access; no speedup is claimed.
pub fn sum_prefix_unchecked(values: &[u64], count: usize) -> Option<u64> {
    let prefix = values.get(..count)?;
    let mut total = 0u64;
    for index in 0..prefix.len() {
        // SAFETY: index is in this borrowed slice; its bounds cannot change in the loop.
        total = total.wrapping_add(unsafe { *prefix.get_unchecked(index) });
    }
    Some(total)
}

#[cfg(test)]
mod tests {
    #[test]
    fn the_correctness_oracle_precedes_measurement() {
        let values = [1, 2, 3, 5, 8];
        assert_eq!(
            super::sum_squares_iterator(&values),
            super::sum_squares_loop(&values)
        );
    }

    #[test]
    fn all_valid_prefixes_match_with_wrapping_arithmetic() {
        let values = [u64::MAX, 1, 2, u64::MAX, 7];
        for count in 0..=values.len() {
            assert_eq!(
                super::sum_prefix_safe(&values, count),
                super::sum_prefix_unchecked(&values, count),
            );
        }
        assert_eq!(super::sum_prefix_unchecked(&values, 2), Some(0));
    }

    #[test]
    fn empty_and_invalid_lengths_are_checked_before_unsafe_access() {
        for values in [&[][..], &[1, 2, 3][..]] {
            assert_eq!(super::sum_prefix_safe(values, 0), Some(0));
            assert_eq!(super::sum_prefix_unchecked(values, 0), Some(0));
            for count in [values.len() + 1, usize::MAX] {
                assert_eq!(super::sum_prefix_safe(values, count), None);
                assert_eq!(super::sum_prefix_unchecked(values, count), None);
            }
        }
    }

    #[test]
    fn fixed_length_storage_keeps_elements_mutable() {
        let mut growing = Vec::with_capacity(32);
        growing.extend([1, 2, 3]);
        let mut fixed = growing.into_boxed_slice();
        fixed[1] = 9;
        assert_eq!(&*fixed, &[1, 9, 3]);
        assert!(Vec::<u8>::new().into_boxed_slice().is_empty());
    }
}
