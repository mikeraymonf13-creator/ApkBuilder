## 2026-10-14 - Accessible HTML Tabs and Dynamic Form Feedback
**Learning:** In custom HTML tab interfaces and async forms, screen readers and keyboard users need explicit ARIA roles (`role="tablist"`, `role="tab"`, `role="tabpanel"`), synced `aria-selected` attributes, `aria-live="polite"` status containers, and disabled loading states on submit buttons to prevent double submissions and provide clear operational feedback.
**Action:** When working on HTML/JS tab containers and async submission forms, always pair semantic tab attributes with synced `aria-selected` state changes, `aria-live` regions for status updates, and interactive loading states.

## 2026-10-24 - Cryptographic Address Input Usability and Form Guidance
**Learning:** Cryptographic wallet address and token amount inputs require explicit mobile input modes (`inputmode="decimal"`), disabled spellcheck (`spellcheck="false"`), disabled auto-complete (`autocomplete="off"`), and explicit `aria-describedby` helper texts. Without these, mobile keyboards default to text auto-capitalization, browsers auto-fill home addresses into crypto fields, and spellcheckers highlight base64 addresses in red.
**Action:** Always include `inputmode="decimal"`, `min="0"`, `spellcheck="false"`, `autocomplete="off"`, and `aria-describedby` hint text on crypto transfer address and numeric token amount fields.
