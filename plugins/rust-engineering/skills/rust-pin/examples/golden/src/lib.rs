//! A dependency-free address-sensitive value with a local pinning proof.

use std::marker::PhantomPinned;
use std::pin::Pin;
use std::ptr::NonNull;

#[derive(Debug)]
pub struct PinnedLabel {
    text: String,
    text_ptr: NonNull<String>,
    _pin: PhantomPinned,
}

impl PinnedLabel {
    pub fn new(text: impl Into<String>) -> Pin<Box<Self>> {
        let mut value = Box::pin(Self {
            text: text.into(),
            text_ptr: NonNull::dangling(),
            _pin: PhantomPinned,
        });
        let text_ptr = NonNull::from(&value.text);
        // SAFETY: `value` has just been pinned in its owning Box. We only initialize
        // the pointer field and never expose an operation that moves `text`.
        unsafe { value.as_mut().get_unchecked_mut().text_ptr = text_ptr };
        value
    }

    pub fn text(self: Pin<&Self>) -> &str {
        // SAFETY: construction points at `self.text`, and the pinning API prevents
        // moving or replacing that structurally pinned field before destruction.
        unsafe { self.get_ref().text_ptr.as_ref().as_str() }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn moving_the_pin_owner_keeps_the_pointee_address() {
        let value = PinnedLabel::new("stable");
        let before = value.as_ref().text().as_ptr();
        let moved_owner = value;
        assert_eq!(moved_owner.as_ref().text(), "stable");
        assert_eq!(before, moved_owner.as_ref().text().as_ptr());
    }
}

