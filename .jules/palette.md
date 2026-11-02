## 2026-10-14 - Accessible HTML Tabs and Dynamic Form Feedback
**Learning:** In custom HTML tab interfaces and async forms, screen readers and keyboard users need explicit ARIA roles (`role="tablist"`, `role="tab"`, `role="tabpanel"`), synced `aria-selected` attributes, `aria-live="polite"` status containers, and disabled loading states on submit buttons to prevent double submissions and provide clear operational feedback.
**Action:** When working on HTML/JS tab containers and async submission forms, always pair semantic tab attributes with synced `aria-selected` state changes, `aria-live` regions for status updates, and interactive loading states.

## 2026-11-02 - Web3 Transfer Form Accessibility and Input Sanitation
**Learning:** In Web3 and crypto transfer interfaces, address fields suffer from unwanted mobile auto-capitalization and spellcheck red squiggles, while numeric token amounts risk zero/negative submissions if min constraints are missing. Pairing `spellcheck="false"` and `autocomplete="off"` with `aria-required="true"` and visible indicators provides clear validation boundaries and seamless copy-pasting for crypto address strings.
**Action:** Always disable spellcheck/autocomplete on cryptographic address/hash inputs, set `min` boundaries on token/currency transfer amounts, and reset form inputs after successful broadcast.
