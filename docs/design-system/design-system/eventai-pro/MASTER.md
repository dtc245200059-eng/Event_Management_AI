# EventAI Pro — Design System Master

> **Purpose:** Authoritative design guidance for the existing EventAI Pro application.
> **Priority:** Existing application CSS, Bootstrap 5.3.3, working interactions, and accessibility requirements take precedence over generic generated examples.
> **Scope:** Flask + Jinja2, HTML, CSS, JavaScript, Bootstrap 5.3.3.
> **Important:** This file documents the current design direction. Do not treat it as permission to rewrite application source files or replace established design tokens.

---

## 1. Project Design Principles

- **Design direction:** Apple-inspired minimalism with restrained Liquid Glass effects.
- **Product type:** Event management SaaS dashboard with integrated AI assistance.
- **Primary goal:** Help users discover, create, manage, and attend events efficiently.
- **Visual character:** Clean, precise, spacious, restrained, accessible, and responsive.
- **Implementation:** Reuse the existing Flask/Jinja2 structure, Bootstrap components, CSS variables, and JavaScript behavior.
- **Consistency:** Prefer established design tokens over hard-coded colors, spacing, shadows, or radii.
- **Performance:** Favor CSS-based effects and short transitions. Avoid unnecessary animation loops, large blur regions, layout thrashing, and excessive DOM updates.

Do not apply a generic landing-page template to authenticated dashboard screens. Use a landing-page pattern only when the page is genuinely intended to introduce the product or convert visitors.

---

## 2. Source of Truth

Before implementing or redesigning a page, inspect:

1. `app/templates/base.html`
2. `app/static/css/style.css`
3. The specific page template and its related JavaScript.
4. Existing responsive navigation, AI Assistant, notification, theme, and print behaviors relevant to that page.

The existing application source is authoritative for exact values and behavior.

Do not invent CSS variables, assume a component exists, or duplicate an existing component without checking the source first.

Do not remove compatibility aliases or rename tokens without auditing all references.

### Technology constraints

- Backend and rendering: Flask + Jinja2.
- CSS framework: Bootstrap 5.3.3.
- Styling: Existing custom CSS in `app/static/css/style.css`.
- Interactions: Existing JavaScript and Bootstrap behavior.
- Icons: Reuse the icon library already loaded by the application. Do not add another icon library without justification.
- Typography: Use the existing native Apple/system font stack.
- Do not introduce Tailwind, React, or another framework unless explicitly requested.

---

## 3. Color System

### Light Mode

Use the existing CSS variables rather than redefining them.

| Role | Existing token | Current value |
|---|---|---|
| Page background | `--background` | `#F5F5F7` |
| Main surface | `--surface` | `#FFFFFF` |
| Secondary surface | `--surface-secondary` | `#FAFAFA` |
| Tertiary surface | `--surface-tertiary` | `#F0F0F2` |
| Elevated surface | `--surface-elevated` | `#FFFFFF` |
| Primary text | `--text-primary` | `#1D1D1F` |
| Secondary text | `--text-secondary` | `#6E6E73` |
| Tertiary text | `--text-tertiary` | `#86868B` |
| Primary accent | `--accent-primary` | `#007AFF` |
| Accent hover | `--accent-primary-hover` | `#0062CC` |
| Main border | `--border` | `rgba(0, 0, 0, 0.08)` |
| Input focus | `--input-focus-border` | `#007AFF` |

### Dark Mode

| Role | Existing token | Current value |
|---|---|---|
| Page background | `--background` | `#000000` |
| Main surface | `--surface` | `#1C1C1E` |
| Secondary surface | `--surface-secondary` | `#2C2C2E` |
| Tertiary surface | `--surface-tertiary` | `#3A3A3C` |
| Elevated surface | `--surface-elevated` | `#2C2C2E` |
| Primary text | `--text-primary` | `#F5F5F7` |
| Secondary text | `--text-secondary` | `#A1A1A6` |
| Tertiary text | `--text-tertiary` | `#86868B` |
| Primary accent | `--accent-primary` | `#0A84FF` |
| Accent hover | `--accent-primary-hover` | `#007AFF` |
| Main border | `--border` | `rgba(255, 255, 255, 0.10)` |
| Input focus | `--input-focus-border` | Verify the actual dark-mode override before changing it |

### Color rules

- Preserve the current blue accent as the primary interactive color.
- Existing green, orange, red, purple, and teal tokens may be used for semantic statuses when appropriate.
- Do not replace the palette with the generated purple/orange theme.
- Do not introduce decorative gradients or saturated colors without a clear functional purpose.
- Maintain readable text and control boundaries in both themes.
- Never assume a translucent surface has sufficient contrast over every background.
- Validate actual foreground/background combinations, including text displayed over glass surfaces.
- Use semantic status colors consistently; never communicate status by color alone.

---

## 4. Typography

The current system font stack is defined by `--apple-font`:

`-apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", "Segoe UI", Roboto, sans-serif`

The monospace stack is defined by `--apple-font-mono`.

### Typography rules

- Preserve the existing font variables.
- Prefer native system typography and a clear hierarchy.
- Use concise page titles, readable body text, and restrained metadata.
- Keep dashboard labels and data tables legible at typical desktop and laptop widths.
- Avoid introducing Playfair Display, decorative display fonts, or external Google Fonts solely because they appear in generated recommendations.
- Reuse existing heading sizes and responsive typography rules.
- Avoid excessive font weights, uppercase text, and oversized headings in information-dense interfaces.

---

## 5. Spacing, Radius, and Motion Tokens

### Existing radius tokens

| Token | Current value |
|---|---|
| `--radius-xs` | `6px` |
| `--radius-sm` | `8px` |
| `--radius-md` | `12px` |
| `--radius-lg` | `16px` |
| `--radius-xl` | `20px` |
| `--radius-2xl` | `24px` |
| `--radius-3xl` | `28px` |
| `--radius-pill` | `980px` |
| `--radius-btn` | `980px` |
| `--radius-card` | `20px` |
| `--radius-modal` | `24px` |
| `--radius-input` | `12px` |
| `--radius-badge` | `980px` |

### Existing transitions

| Token | Current value |
|---|---|
| `--transition-fast` | `all 0.18s cubic-bezier(0.25, 0.1, 0.25, 1)` |
| `--transition-smooth` | `all 0.24s cubic-bezier(0.16, 1, 0.3, 1)` |
| `--transition-bounce` | `all 0.36s cubic-bezier(0.34, 1.56, 0.64, 1)` |

### Rules

- Reuse the existing radius and transition tokens.
- Check the complete stylesheet before assuming a spacing or shadow token is available.
- Prefer consistent spacing and alignment over arbitrary one-off values.
- Use fast, subtle feedback for hover, focus, and active states.
- Avoid hover effects that move surrounding content or cause layout shifts.
- Reserve bounce effects for suitable non-critical interactions.
- Do not animate every element merely to make the interface appear more dynamic.

---

## 6. Liquid Glass and Surfaces

Existing surface-related tokens include:

- `--surface-translucent`
- `--surface-translucent-heavy`
- `--surface-glass`
- `--glass-bg`
- `--glass-border`
- `--glass-shadow`

Use these tokens and inspect their definitions before implementing a new glass component.

### Glass guidelines

- Use glass selectively for suitable navigation, floating controls, overlays, and AI Assistant surfaces.
- Keep the main content area stable, readable, and visually distinct from overlays.
- Use a sufficiently opaque fallback when backdrop blur is unsupported.
- Do not place long passages of small text over busy or highly translucent backgrounds.
- Keep borders and shadows subtle; use them to establish hierarchy rather than decorate every container.
- Avoid excessive nested glass layers, large blurred regions, and continuously animated blur effects.
- Ensure dialogs and menus remain visually distinguishable from the page behind them in both themes.

---

## 7. Component Guidelines

### Buttons

- Reuse Bootstrap button variants and existing project-specific button styles.
- Preserve the current primary blue accent.
- Give primary actions a clear visual priority.
- Use secondary, outline, and quiet actions where appropriate.
- Provide visible hover, active, focus, disabled, and loading states where applicable.
- Ensure the entire intended clickable area is interactive.
- Do not apply generic button CSS from this document over existing Bootstrap or project rules.

### Cards and dashboard panels

- Use existing surface, radius, border, and shadow tokens.
- Keep cards visually restrained and content-focused.
- Use hover elevation only when a card is genuinely interactive.
- Do not assign `cursor: pointer` to a static informational card.
- Preserve meaningful grouping and readable spacing.
- Avoid adding shadows and borders redundantly to every nested element.

### Forms and inputs

- Use Bootstrap-compatible form markup and current project input styles.
- Preserve clear labels, validation messages, and error states.
- Keep focus indicators visible.
- Associate labels with their controls and provide useful accessible names.
- Do not remove browser outlines without providing a clear replacement.
- Avoid placeholder text as the only label.

### Navigation

- Preserve the existing Apple-inspired navigation and responsive mobile drawer.
- Keep active, hover, focus, and expanded states distinguishable.
- Ensure menus and overlays do not obscure essential controls without a way to dismiss them.
- Avoid arbitrary high z-index values; establish and reuse a coherent layering scale after auditing existing components.

### AI Assistant

- Preserve the existing chat dialog, backdrop, message list, and input behavior.
- Maintain readable user and assistant messages in Light and Dark Mode.
- Keep loading, empty, error, and no-results states explicit and understandable.
- Render structured data safely; never expose raw values such as `[object Object]undefined` to users.
- Keep keyboard interaction and dialog focus behavior accessible.
- Ensure the assistant and its backdrop do not cause unintended mobile overflow.

### Notifications and status indicators

- Make unread counts understandable without relying on color alone.
- Use consistent semantic colors and concise status labels.
- Prevent badges from clipping at common viewport sizes.
- Avoid unnecessary animation or pulsing for persistent notifications.

### Tables and event lists

- Prioritize scanability, alignment, clear headers, and useful empty states.
- Keep action controls reachable on smaller screens.
- Use responsive table behavior appropriate to the data; do not introduce page-wide horizontal scrolling.
- Preserve filtering, pagination, sorting, and other existing behaviors.

---

## 8. Page Layout Strategy

### Dashboard-first design

For authenticated application pages, prioritize:

1. Existing application navigation and page context.
2. Page title and concise supporting information.
3. The most relevant primary action.
4. Important event data, metrics, lists, or workflows.
5. Secondary details, filters, and contextual assistance.

The order must follow the page's real purpose; do not force every screen into an identical layout.

### Event discovery and event details

- Make event title, date, venue, status, and primary action easy to find.
- Use consistent information hierarchy and clear event status labels.
- Keep registration and ticket-related actions obvious without making the page visually noisy.
- Preserve existing business rules and data behavior.

### AI-oriented pages

- Distinguish AI-generated suggestions from confirmed application data.
- Provide clear loading, failure, empty, and success states.
- Make consequential actions explicit and reviewable.
- Do not let decorative effects interfere with the actual workflow.

### Landing pages

Use a hero-led layout only for pages intended to introduce the product or communicate a focused value proposition. Do not replace operational dashboard layouts with oversized hero sections.

---

## 9. Responsive Design

Validate at these viewport widths:

- `375px` — small mobile.
- `768px` — tablet.
- `1024px` — small desktop or landscape tablet.
- `1440px` — desktop.

### Responsive requirements

- Preserve the existing viewport configuration and safe-area support.
- Avoid horizontal overflow at all tested widths.
- Keep navigation, forms, dialogs, tables, and chat usable on mobile.
- Allow buttons and form controls to fit or wrap without clipping.
- Ensure fixed and sticky elements do not hide headings, focused controls, or important content.
- Use responsive layout changes instead of simply shrinking desktop content.
- Test long event titles, long labels, empty states, validation messages, and large datasets.
- Verify touch targets and spacing on touch devices.

---

## 10. Accessibility

- Aim for WCAG AA contrast: at least `4.5:1` for normal text and `3:1` for qualifying large text.
- Measure contrast for actual rendered color combinations, including translucent surfaces.
- Preserve visible keyboard focus.
- Ensure all interactive controls can be operated using a keyboard.
- Use semantic HTML, appropriate labels, and accessible names.
- Use appropriate dialog semantics and manage focus for modal interactions.
- Respect `prefers-reduced-motion`.
- Never rely on color alone to communicate errors, statuses, or selection.
- Use meaningful SVG or existing icon-library icons instead of emoji as interface icons.
- Give icon-only buttons accessible names.
- Verify focus order and prevent keyboard focus from becoming trapped behind overlays.

---

## 11. Performance

- Prefer transforms and opacity for lightweight visual transitions.
- Avoid animating layout-heavy properties when a cheaper alternative is available.
- Limit large-area `backdrop-filter` effects and excessive layered shadows.
- Avoid unnecessary dependencies and duplicate icon libraries.
- Do not add continuously running animation loops without a functional purpose.
- Pause or disable nonessential animation when appropriate.
- Check mobile responsiveness and interaction latency after visual changes.
- Keep existing JavaScript behavior intact unless a change is explicitly required.

---

## 12. Print and Ticket Safety

The application contains ticket-printing behavior with strict physical page and QR-code requirements.

- Inspect the existing print-specific CSS before modifying ticket layouts or shared styles.
- Do not make broad CSS changes that unintentionally affect print output.
- Preserve one physical ticket per intended printed page and existing QR-code sizing and visibility requirements.
- Validate print preview separately from normal browser rendering.
- Keep print-only and screen-only behavior scoped appropriately.

---

## 13. Anti-Patterns

Do not:

- Replace the existing Apple-inspired palette with generated purple/orange colors.
- Introduce Playfair Display or external font imports without a specific requirement.
- Apply generic component CSS that conflicts with Bootstrap or current project styles.
- Replace the dashboard with a hero-centric marketing layout without justification.
- Remove existing CSS variables or compatibility aliases without auditing their consumers.
- Use emoji as interface icons.
- Remove focus indicators.
- use arbitrary z-index values without checking existing overlays.
- Use layout-shifting hover animations.
- Add glass, blur, gradients, or shadows to every component.
- sacrifice contrast for translucency.
- create horizontal page overflow on mobile.
- change print styles without testing ticket output.
- claim accessibility or responsive compliance without testing it.

---

## 14. Pre-Delivery Checklist

### Design consistency
- [ ] Existing Apple-inspired visual direction is preserved.
- [ ] Existing color, typography, radius, and transition tokens are reused.
- [ ] Both Light and Dark Mode have been checked.
- [ ] Bootstrap and project-specific component styles do not conflict.

### Functionality
- [ ] Existing interactions remain functional.
- [ ] Loading, empty, error, and success states are clear where applicable.
- [ ] Navigation, AI Assistant, forms, and dialogs behave correctly.

### Accessibility
- [ ] Contrast is checked for actual foreground/background pairs.
- [ ] Keyboard focus is visible.
- [ ] Labels, accessible names, and dialog semantics are appropriate.
- [ ] Reduced-motion preferences are respected.

### Responsive behavior
- [ ] Layout checked at 375px, 768px, 1024px, and 1440px.
- [ ] No unintended horizontal overflow.
- [ ] Sticky navigation, mobile drawer, dialogs, and AI chat remain usable.

### Performance and regression
- [ ] No unnecessary animation loops or heavy visual effects.
- [ ] No new console errors or broken assets.
- [ ] Ticket printing and QR-code output are unaffected when relevant.
- [ ] Relevant existing tests and build checks pass.

---

## 15. Change Policy

This document is a design reference, not authorization for a wholesale redesign.

Before changing application code:

1. Inspect the relevant template, CSS selectors, JavaScript, and existing tokens.
2. Identify the specific problem and intended outcome.
3. Prefer the smallest coherent change that solves it.
4. Check both themes and affected responsive layouts.
5. Test existing functionality, especially navigation, AI chat, and ticket printing when relevant.
6. Report changed files and verification results accurately.

If a generated UI/UX Pro Max recommendation conflicts with the existing application design or architecture, adapt or reject the recommendation rather than applying it blindly.
