## 2026-10-10 - ARIA Tab roles and Focus States for Custom HTML Tabs
**Learning:** In simple custom HTML/JS tab widgets without framework state management, screen readers cannot convey active tab state unless explicit `role="tablist"`, `role="tab"`, and `role="tabpanel"` attributes are added, with `switchTab` handlers updating `aria-selected` dynamically.
**Action:** When working on custom tab navigation, always complement DOM class toggling with `setAttribute('aria-selected', 'true'/'false')` and explicit `:focus-visible` CSS rules.
