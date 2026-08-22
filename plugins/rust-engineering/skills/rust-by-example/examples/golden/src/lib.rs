//! One concept, one complete observable result: parse and sum valid integers.

pub fn sum_lines(input: &str) -> Result<i64, std::num::ParseIntError> {
    input.lines().map(str::trim).filter(|line| !line.is_empty()).map(str::parse::<i64>).sum()
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn example_is_runnable_and_covers_the_contrast() {
        assert_eq!(sum_lines("1\n 2\n\n3"), Ok(6));
        assert!(sum_lines("1\nnope").is_err());
    }
}
