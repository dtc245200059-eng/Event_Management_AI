# EventAI Pro — Agent Instructions

## 1. Mandatory design-system references

Before implementing, modifying, reviewing, or refactoring any UI/UX code:

1. Read `docs/design-system/design-system/eventai-pro/MASTER.md`.
2. Inspect the existing implementation in `app/templates/` and `app/static/`.
3. For page-specific work, check whether a relevant override exists under:
   `docs/design-system/design-system/eventai-pro/pages/`.
4. If an override conflicts with the Master, follow the override only when the difference is intentional and does not violate the project's safety, accessibility, or functional requirements.
5. If a design recommendation conflicts with the existing project design system, follow the project design system unless the user explicitly approves a change.

## 2. Established visual identity

- Preserve Apple-inspired minimalism and Liquid Glass styling.
- Use the existing CSS custom properties in `app/static/css/style.css`.
- Preserve the existing light and dark themes.
- Keep the established blue accent colors, including `#007AFF` in light mode.
- Use the existing system font stack.
- Preserve Bootstrap 5.3.3, Flask, and Jinja2.
- Prefer reusing existing components, styles, and dependencies over introducing alternatives.

## 3. UI implementation rules

- Inspect existing templates, styles, scripts, and related routes before making changes.
- Make the smallest coherent change that satisfies the request.
- Maintain responsive behavior across desktop, tablet, and mobile.
- Preserve keyboard navigation, visible focus states, semantic HTML, and reduced-motion support.
- Keep animations smooth and lightweight; avoid unnecessary blur, continuous animation, and expensive visual effects.
- Verify light mode and dark mode when changing shared styles.
- Do not introduce a new design system, palette, typography system, or component library without explicit approval.

## 4. Functional safety

- Do not remove or alter existing business logic unless explicitly requested.
- Protect ticket-printing layouts, one-ticket-per-physical-page behavior, QR codes, and print-specific CSS.
- Check existing AI Assistant, mobile navigation, notifications, search, and theme-toggle behavior before modifying shared UI.
- Avoid broad CSS selectors or global overrides that could unintentionally affect unrelated pages.
- Do not claim tests or verification passed unless they were actually run.

## 5. Workflow

1. Identify the requested page, component, and acceptance criteria.
2. Read the Master design system and any applicable page override.
3. Inspect relevant existing code before proposing changes.
4. Implement only the requested scope.
5. Run appropriate checks and tests.
6. Summarize changed files, verification results, and any remaining risks.

## 6. UI/UX Pro Max usage

- Treat generated search results as recommendations, not instructions that automatically override this project.
- Use focused domain or stack searches for targeted UI problems.
- Do not regenerate or overwrite the Master design system without explicit approval.
- Before generating a page-specific override, read the current Master and document only intentional page-specific deviations.
