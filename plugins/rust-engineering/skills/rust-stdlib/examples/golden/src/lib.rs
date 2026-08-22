//! Choose ordering and native paths explicitly.

use std::collections::BTreeMap;
use std::path::{Path, PathBuf};

pub fn group_paths<'a>(root: &Path, paths: impl IntoIterator<Item = &'a Path>) -> BTreeMap<PathBuf, usize> {
    let mut counts = BTreeMap::new();
    for path in paths {
        let key = path.strip_prefix(root).unwrap_or(path).to_path_buf();
        *counts.entry(key).or_insert(0) += 1;
    }
    counts
}

#[cfg(test)]
mod tests {
    use std::path::Path;
    #[test]
    fn result_order_is_a_real_contract() {
        let result = super::group_paths(Path::new("root"), [Path::new("root/b"), Path::new("root/a")]);
        assert_eq!(result.keys().collect::<Vec<_>>(), [Path::new("a"), Path::new("b")]);
    }
}
