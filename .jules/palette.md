## 2026-10-13 - Tab ARIA Roles and Button Loading State Standard
**Learning:** Vanilla HTML tab components in web applications often lack proper accessibility semantics (`role="tablist"`, `role="tab"`, `role="tabpanel"`, `aria-selected`, `aria-controls`) and focus-visible indicators. In addition, asynchronous transfer buttons require explicit visual loading states and temporary disabling to prevent double submissions.
**Action:** Always verify tab accessibility markup and attach dynamic `aria-selected` attribute sync alongside button pending states in vanilla web application components.
