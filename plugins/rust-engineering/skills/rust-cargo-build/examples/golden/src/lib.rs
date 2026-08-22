//! The feature changes capability, while both configurations remain valid.

pub fn transport_name() -> &'static str {
    #[cfg(feature = "fast")]
    { "fast" }
    #[cfg(not(feature = "fast"))]
    { "portable" }
}

#[cfg(test)]
mod tests {
    #[test]
    fn selected_configuration_is_explicit() {
        let expected = if cfg!(feature = "fast") { "fast" } else { "portable" };
        assert_eq!(super::transport_name(), expected);
    }
}
