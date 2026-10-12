# Palette's Journal

## 2026-10-12 - Persistent Status Containers and Screen Reader Announcements
**Learning:** In vanilla JS SPAs with dynamic status cards that toggle visibility (e.g. display: none -> block), innerHTML changes are missed by screen readers if `aria-live="polite"` is added dynamically. The container element must possess `aria-live="polite"` and `role="status"` on initial page load.
**Action:** Always place `aria-live="polite"` and `role="status"` on persistent feedback container elements in the initial HTML markup before async JS operations mutate them.
