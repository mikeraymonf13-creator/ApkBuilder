## 2026-10-14 - Accessible HTML Tabs and Dynamic Form Feedback
**Learning:** In custom HTML tab interfaces and async forms, screen readers and keyboard users need explicit ARIA roles (`role="tablist"`, `role="tab"`, `role="tabpanel"`), synced `aria-selected` attributes, `aria-live="polite"` status containers, and disabled loading states on submit buttons to prevent double submissions and provide clear operational feedback.
**Action:** When working on HTML/JS tab containers and async submission forms, always pair semantic tab attributes with synced `aria-selected` state changes, `aria-live` regions for status updates, and interactive loading states.

## 2026-10-25 - Copy-to-Clipboard Feedback Pattern in Web3 Portals
**Learning:** Displaying wallet addresses in Web3 web apps requires accessible copy controls with explicit `aria-label`, visual state changes ("Copied!"), `aria-live="polite"` feedback for screen reader users, and proper clearing of state timeouts on rapid clicks.
**Action:** When adding copy-to-clipboard functionality for crypto wallet addresses, always pair `aria-label` and `aria-live="polite"` notification toasts with debounced/cleared `setTimeout` state resets.
