//! Semantically equivalent implementations for a controlled benchmark fixture.

pub fn sum_squares_iterator(values: &[u64]) -> u64 {
    values.iter().copied().map(|value| value * value).sum()
}

pub fn sum_squares_loop(values: &[u64]) -> u64 {
    let mut total = 0;
    for &value in values { total += value * value; }
    total
}

#[cfg(test)]
mod tests {
    #[test]
    fn the_correctness_oracle_precedes_measurement() {
        let values = [1, 2, 3, 5, 8];
        assert_eq!(super::sum_squares_iterator(&values), super::sum_squares_loop(&values));
    }
}
