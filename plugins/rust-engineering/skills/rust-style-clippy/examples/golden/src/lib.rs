//! Readable, lint-friendly code without changing the public contract for style.

pub fn normalized_words(input: &str) -> Vec<String> {
    input
        .split_whitespace()
        .filter(|word| !word.is_empty())
        .map(str::to_lowercase)
        .collect()
}

#[cfg(test)]
mod tests {
    #[test]
    fn formatting_and_lints_do_not_replace_behavior() {
        assert_eq!(super::normalized_words(" Rust  STYLE "), ["rust", "style"]);
    }
}
