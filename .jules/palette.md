## 2026-10-14 - Accessible HTML Tabs and Dynamic Form Feedback
**Learning:** In custom HTML tab interfaces and async forms, screen readers and keyboard users need explicit ARIA roles (`role="tablist"`, `role="tab"`, `role="tabpanel"`), synced `aria-selected` attributes, `aria-live="polite"` status containers, and disabled loading states on submit buttons to prevent double submissions and provide clear operational feedback.
**Action:** When working on HTML/JS tab containers and async submission forms, always pair semantic tab attributes with synced `aria-selected` state changes, `aria-live` regions for status updates, and interactive loading states.

## 2026-10-23 - Mobile Input Attributes & Persistent Live Regions
**Learning:** For crypto/wallet address inputs, mobile browsers default to auto-capitalizing and spellchecking addresses which frustrates users. Additionally, hiding `aria-live` containers with `display: none` can remove them from screen reader trees; using `:empty { display: none; }` keeps the live region active in the accessibility tree while hiding empty containers visually.
**Action:** Always add `autocomplete="off" spellcheck="false" autocapitalize="none"` to address inputs, `inputmode="decimal"` to numeric inputs, and maintain `aria-live` containers in the DOM tree using CSS `:empty`.
