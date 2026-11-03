---
name: saas-sidebar-redesign
description: Redesign a Vue 3 app's UI into a modern SaaS layout with a left vertical sidebar replacing the top nav, tokenized spacing and a polished look. Use when asked to modernize, restyle or add a sidebar to a Vue app.
---

# SaaS Sidebar Redesign

Turn a Vue 3 app with a top navigation bar into a SaaS-style shell: fixed left sidebar, scrolling content area, consistent design tokens. Token values and the sidebar spec are in `references/design-tokens.md`. Read it before step 3.

## Guardrails

- Keep route paths, component logic, API and data code unchanged. This is a presentation change.
- Add no dependencies. Use plain CSS (variables, Grid, flexbox).
- Use no emojis in the UI.
- Do not commit unless the user asks.
- Do not mix Options API and Composition API inside one file. Follow the style the file already uses.

## Workflow

### 1. Discover

Report these findings to the user before editing:

- Router file and the list of routes.
- The shell component that holds the top nav (usually `App.vue`), and where the global styles live.
- Elements positioned relative to the top bar: `position: sticky` or `fixed` with a hardcoded `top` value, and dropdowns anchored with `top: calc(100% + ...)`.
- Repeated `max-width` values and any existing CSS variables.
- Nav labels that are hardcoded instead of using the app's i18n.
- Whether any `@media` rules exist.

### 2. Respect project rules

Read `CLAUDE.md` (root and client). Apply what it says about:

- Which subagent must edit `.vue` files. If one is required, delegate every `.vue` edit to it and pass it this workflow.
- Palette, status colors, chart style and the no-emoji rule. A project palette overrides the defaults in the tokens reference.
- Browser testing tools and ports.

### 3. Tokens first

Add the `:root` variables from `references/design-tokens.md` to the global style block. Then replace values in the shell and in shared global classes (cards, tables, badges, buttons, page headers). Migrate per-component styles only where the component touches the layout or looks off. Do not rewrite every stylesheet in one pass.

### 4. Shell layout

- Use a two-column CSS Grid: sidebar and content.
- The sidebar is full height and sticky, with a fixed width.
- Sidebar order: brand, primary nav, then profile and language controls pinned to the bottom.
- Reuse the existing `router-link` entries and i18n keys. Show the active route with a background and an accent. Set `aria-current="page"` on it.
- The content area scrolls on its own. Wrap routed views in a container with a max width and the page padding token.
- Move any global filter bar into the content area. Do not leave it in the sidebar.

### 5. Fix dependents

- Replace sticky offsets that assumed the top bar with `top: 0` or a variable.
- Re-anchor dropdowns (profile, language) so they open upward or sideways from the sidebar, and stay inside the viewport.
- Collapse repeated `max-width` values into one variable.
- Check modals. Their z-index must sit above the sidebar and the mobile backdrop.

### 6. Responsive

Add one breakpoint at about 768px. Below it, the sidebar becomes an off-canvas drawer:

- A menu button in a slim top bar opens it. A backdrop closes it.
- It also closes on route change and on Escape.
- The button has an `aria-label` and `aria-expanded`. Focus moves into the drawer when it opens and returns to the button when it closes.
- The content area uses the mobile padding token. There is no horizontal page scroll.

### 7. Polish

- Cards, tables, badges and buttons use tokens only: no raw hex, no ad hoc radius or font size.
- Use subtle borders and shadows, visible focus rings, and hover and active states on interactive elements.
- Keep one primary blue. Remove stray off-palette colors.

### 8. Verify

Run the dev servers using the project's start command. Then use the browser tool named in `CLAUDE.md` (Playwright MCP here):

1. For every route, take a screenshot at 1440px and at 390px wide.
2. Check that the active link matches each route.
3. At 390px, open and close the drawer with the button, the backdrop, Escape and a nav click.
4. Open each dropdown and modal and confirm placement and stacking.
5. Check that the console has no errors and the page has no horizontal scroll.

Fix problems and repeat. Finish with a short report: what changed, what you left alone on purpose, and any pre-existing problems you noticed but did not fix (for example an unrouted view or a hardcoded label).
