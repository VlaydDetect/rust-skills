//! Stable, MSRV-friendly data transformation without nightly features.

pub fn first_nonempty<'a, I>(values: I) -> Option<&'a str>
where
    I: IntoIterator<Item = &'a str>,
{
    values.into_iter().find(|value| !value.is_empty())
}

#[cfg(test)]
mod tests {
    #[test]
    fn generic_input_keeps_the_contract_small() {
        let values = ["", "stable", "rust"];
        assert_eq!(super::first_nonempty(values), Some("stable"));
    }
}
