## 2026-10-14 - Accessible HTML Tabs and Dynamic Form Feedback
**Learning:** In custom HTML tab interfaces and async forms, screen readers and keyboard users need explicit ARIA roles (`role="tablist"`, `role="tab"`, `role="tabpanel"`), synced `aria-selected` attributes, `aria-live="polite"` status containers, and disabled loading states on submit buttons to prevent double submissions and provide clear operational feedback.
**Action:** When working on HTML/JS tab containers and async submission forms, always pair semantic tab attributes with synced `aria-selected` state changes, `aria-live` regions for status updates, and interactive loading states.

## 2026-10-31 - Accessible Input Length Limits and Real-Time Character Counters
**Learning:** Hard input limits without live feedback lead to user frustration when pasted or typed text is silently truncated or rejected. Pairing a visible live counter with `aria-describedby` and `aria-live="polite"` ensures that both visual users and assistive tech users receive prompt, non-intrusive awareness of remaining capacity before submitting a transaction memo or payload.
**Action:** When adding maximum character constraints to form fields, always link the counter to the input using `aria-describedby`, mark the counter with `aria-live="polite"`, and update counts on the `input` event.
