# Design tokens and sidebar spec

Defaults for the `saas-sidebar-redesign` skill. If the project defines its own palette or scale (for example in `CLAUDE.md`), use that and keep the token names.

## Tokens

Put these in the global style block.

```css
:root {
  /* Spacing: 4px grid */
  --space-1: 0.25rem;  /* 4  */
  --space-2: 0.5rem;   /* 8  */
  --space-3: 0.75rem;  /* 12 */
  --space-4: 1rem;     /* 16 */
  --space-6: 1.5rem;   /* 24 */
  --space-8: 2rem;     /* 32 */
  --space-12: 3rem;    /* 48 */

  /* Radius */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* Type */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --font-medium: 500;
  --font-semibold: 600;
  --leading-tight: 1.25;
  --leading-normal: 1.5;

  /* Color roles (slate defaults) */
  --color-bg: #f8fafc;
  --color-surface: #ffffff;
  --color-surface-muted: #f1f5f9;
  --color-border: #e2e8f0;
  --color-text: #0f172a;
  --color-text-muted: #64748b;
  --color-primary: #2563eb;
  --color-primary-soft: #eff6ff;
  --color-success: #059669;
  --color-warning: #d97706;
  --color-danger: #dc2626;
  --color-info: #2563eb;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.06);
  --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.08);
  --shadow-lg: 0 20px 50px rgba(15, 23, 42, 0.15); /* modals */

  /* Layout */
  --sidebar-width: 240px;
  --sidebar-width-collapsed: 64px;
  --content-max-width: 1600px;
  --page-padding: var(--space-6);

  /* Stacking */
  --z-sidebar: 100;
  --z-overlay: 200;
  --z-dropdown: 300;
  --z-modal: 400;
}

@media (max-width: 768px) {
  :root { --page-padding: var(--space-4); }
}
```

Merge near-duplicate values when migrating. Typical cases: `#3b82f6` and `#2563eb` both mean primary, so use `--color-primary`. Radii of 10px and 12px become `--radius-lg`. Font sizes like 0.813rem and 0.938rem snap to the nearest step.

## Sidebar spec

| Property | Value |
|---|---|
| Width | `--sidebar-width` (240px) on desktop |
| Position | Sticky, `top: 0`, height `100vh` |
| Background | `--color-surface` with a 1px right border in `--color-border` |
| Padding | `--space-4` |
| Brand block | App name at `--text-lg`, `--font-semibold`; optional subtitle at `--text-xs` in muted text; `--space-6` below |
| Nav item | Height 40px, padding `--space-2` `--space-3`, gap `--space-3` between icon and label, radius `--radius-md`, text `--text-sm`, `--font-medium` |
| Nav item hover | Background `--color-surface-muted` |
| Nav item active | Background `--color-primary-soft`, text `--color-primary`, optional 3px left accent |
| Nav item focus | 2px outline in `--color-primary`, 2px offset |
| Bottom area | Pinned with `margin-top: auto`; profile and language controls; a 1px top border; `--space-4` padding above |
| Icons | Inline SVG, 20px, `currentColor`. No emoji and no icon library unless the project already has one |
| Mobile (up to 768px) | Off-canvas, `position: fixed`, `transform: translateX(-100%)`, slides in with a 200ms transition; backdrop at `--z-overlay` |

## Content area

- `main` fills the remaining grid column and scrolls on its own.
- Inner container: `max-width: var(--content-max-width)`, centered, padding `--page-padding`.
- Page headers use `--text-2xl` for the title and `--color-text-muted` for the subtitle, with `--space-6` below.
- Cards: `--color-surface` background, 1px `--color-border`, `--radius-lg`, `--shadow-sm`, padding `--space-6`.
- Vertical rhythm between sections: `--space-6`. Gap inside grids: `--space-4`.
- Tables: header row in `--color-surface-muted` with `--text-xs` uppercase muted labels; row padding `--space-3` `--space-4`; row dividers in `--color-border`.

## Dropdowns and modals

- Dropdowns anchored in the sidebar bottom area open upward (`bottom: calc(100% + var(--space-2))`) and use `--z-dropdown`, `--shadow-md`, `--radius-md`.
- Modals use `--z-modal` and `--shadow-lg`, and they cover the sidebar.
