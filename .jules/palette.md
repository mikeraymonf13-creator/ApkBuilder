## 2026-10-14 - Async Form Feedback & Live Region Accessibility
**Learning:** Async transfer forms lack visual feedback during network requests, leading to potential accidental double submissions. Additionally, dynamic result containers inserted into the DOM post-submit are ignored by screen readers without ARIA live attributes.
**Action:** Always disable submit buttons, show loading text ("Sending..."), and add `role="status" aria-live="polite"` to output message containers during async form submissions.
