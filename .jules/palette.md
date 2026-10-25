## 2026-10-14 - Accessible HTML Tabs and Dynamic Form Feedback
**Learning:** In custom HTML tab interfaces and async forms, screen readers and keyboard users need explicit ARIA roles (`role="tablist"`, `role="tab"`, `role="tabpanel"`), synced `aria-selected` attributes, `aria-live="polite"` status containers, and disabled loading states on submit buttons to prevent double submissions and provide clear operational feedback.
**Action:** When working on HTML/JS tab containers and async submission forms, always pair semantic tab attributes with synced `aria-selected` state changes, `aria-live` regions for status updates, and interactive loading states.

## 2026-10-25 - Accessible Clipboard Copy Feedback in Web3 Portals
**Learning:** One-click copy buttons for wallet addresses or hashes require explicit visual feedback ('Copy' -> 'Copied!') alongside an `aria-live="polite"` notification region so screen readers receive immediate audible confirmation of clipboard actions without layout shifts.
**Action:** When adding copy-to-clipboard buttons, always include `aria-label`, visual state transitions, and a live region to announce completion to assistive tech.
