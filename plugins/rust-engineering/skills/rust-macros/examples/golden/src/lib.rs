//! A hygienic declarative macro that evaluates each argument once.

#[macro_export]
macro_rules! checked_ratio {
    ($numerator:expr, $denominator:expr) => {{
        let numerator = $numerator;
        let denominator = $denominator;
        (denominator != 0).then(|| numerator / denominator)
    }};
}

#[cfg(test)]
mod tests {
    #[test]
    fn arguments_are_evaluated_once() {
        let mut calls = 0;
        let ratio = crate::checked_ratio!({ calls += 1; 8 }, { calls += 1; 2 });
        assert_eq!(ratio, Some(4));
        assert_eq!(calls, 2);
    }
}
