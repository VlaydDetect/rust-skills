pub(super) fn one_token(input: &str) -> Option<&str> {
    let token = input.trim();
    (!token.is_empty()).then_some(token)
}
