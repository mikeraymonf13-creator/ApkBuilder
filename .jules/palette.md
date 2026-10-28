## 2026-10-14 - Accessible HTML Tabs and Dynamic Form Feedback
**Learning:** In custom HTML tab interfaces and async forms, screen readers and keyboard users need explicit ARIA roles (`role="tablist"`, `role="tab"`, `role="tabpanel"`), synced `aria-selected` attributes, `aria-live="polite"` status containers, and disabled loading states on submit buttons to prevent double submissions and provide clear operational feedback.
**Action:** When working on HTML/JS tab containers and async submission forms, always pair semantic tab attributes with synced `aria-selected` state changes, `aria-live` regions for status updates, and interactive loading states.

## 2026-10-28 - Transaction Hash Copy Buttons and ARIA List Semantics
**Learning:** Displaying raw full-length transaction hashes in activity feeds clutters UI layout. Truncating hash strings while embedding copy buttons with descriptive `aria-label` attributes, instant visual status ("Copied!"), and list semantics (`role="list"`, `role="listitem"`) creates a clean, screen-reader accessible history.
**Action:** When displaying cryptographic hashes or wallet addresses in feeds or status banners, pair truncated visual labels with accessible copy buttons and `role="list"`/`role="listitem"` container semantics.
