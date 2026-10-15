# Stellar Influences Static Wiki Design System

## 1. Atmosphere & Identity

The static wiki is a quiet research instrument: dense, legible, and built for repeated lookup rather than promotion. The signature is an indexed reading desk, with compact navigation, restrained contrast, and clear separation between canonical factors, axes, and oriented planetary pictures.

## 2. Color

### Palette

| Role | Token | Light | Dark | Usage |
|------|-------|-------|------|-------|
| Surface/primary | --surface-primary | #F7F4EC | #1D1B18 | Page background |
| Surface/secondary | --surface-secondary | #FFFDF7 | #28251F | Navigation bands and panels |
| Surface/elevated | --surface-elevated | #FFFFFF | #312D25 | Search results and repeated entries |
| Text/primary | --text-primary | #23211D | #F8F2E6 | Headings and body |
| Text/secondary | --text-secondary | #676055 | #C9BEAA | Metadata and secondary copy |
| Text/tertiary | --text-tertiary | #8B8172 | #948A79 | Disabled and subdued labels |
| Border/default | --border-default | #D8D0BF | #4A4338 | Panels, dividers, controls |
| Border/subtle | --border-subtle | #E9E2D2 | #3A352E | Soft separation |
| Accent/primary | --accent-primary | #27645D | #69B8AA | Links, focus, selected states |
| Accent/hover | --accent-hover | #194E49 | #8BD0C4 | Hover states |
| Accent/warm | --accent-warm | #9C6A1B | #D8A347 | Counts and highlighted metadata |
| Status/error | --status-error | #A34035 | #E1897E | Broken or unavailable links |

### Rules
- Accent is used for navigation, links, focus, and search affordances only.
- Warm accent is reserved for counts and page metadata.
- No colors outside this table in generated static assets.

## 3. Typography

### Scale

| Level | Size | Weight | Line Height | Tracking | Usage |
|-------|------|--------|-------------|----------|-------|
| Display | 40px | 700 | 1.12 | 0 | Main index title |
| H1 | 32px | 700 | 1.2 | 0 | Page titles |
| H2 | 24px | 650 | 1.3 | 0 | Section headers |
| H3 | 18px | 650 | 1.35 | 0 | Source subheads and cards |
| Body | 16px | 400 | 1.65 | 0 | Reading text |
| Body/sm | 14px | 400 | 1.55 | 0 | Metadata and secondary text |
| Caption | 12px | 650 | 1.4 | 0.04em | Labels |

### Font Stack
- Primary: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
- Mono: ui-monospace, "SFMono-Regular", Consolas, "Liberation Mono", monospace

### Rules
- Body text never below 14px.
- Formula and token fragments use the mono stack.
- Letter spacing is 0 except caption labels.

## 4. Spacing & Layout

### Base Unit

All spacing derives from 4px.

| Token | Value | Usage |
|-------|-------|-------|
| --space-1 | 4px | Tight inline gaps |
| --space-2 | 8px | Compact controls |
| --space-3 | 12px | Badge and list spacing |
| --space-4 | 16px | Standard panel padding |
| --space-5 | 20px | Reading rhythm |
| --space-6 | 24px | Section spacing |
| --space-8 | 32px | Major groups |
| --space-10 | 40px | Page breaks |

### Grid
- Max content width: 1320px.
- Directory lists use responsive grids with minimum 220px cells.
- Reading pages use a two-column shell on desktop and a single column on mobile.
- Breakpoints: sm 640px, md 768px, lg 1024px, xl 1280px.

### Rules
- No page section is styled as a floating card.
- Cards are allowed only for repeated entries, search results, and compact statistic items.
- Fixed-format controls keep stable dimensions across hover and focus states.

## 5. Components

### Top Navigation
- Structure: skip link, site title, primary nav links, search field.
- Spacing: --space-3 to --space-5.
- States: hover, focus-visible, current page.
- Accessibility: semantic links, visible focus outline.

### Directory Entry
- Structure: link title, optional metadata line.
- Spacing: --space-3.
- States: default, hover, focus-visible.
- Accessibility: full title text remains visible without truncation.

### Search Results
- Structure: result count, ordered result list, title, type badge, excerpt.
- Spacing: --space-3 to --space-4.
- States: empty query, no results, populated results.
- Accessibility: `aria-live` result status.

## 6. Motion & Interaction

### Timing

| Type | Duration | Easing | Usage |
|------|----------|--------|-------|
| Micro | 120ms | ease-out | Link and control hover |
| Standard | 180ms | ease-in-out | Search result reveal |

### Rules
- Only color, background-color, border-color, opacity, and transform are animated.
- `prefers-reduced-motion` removes transitions.
- Every interactive control has hover and focus-visible states.

## 7. Depth & Surface

### Strategy

Borders-only with light tonal shifts. Shadows are not used in the generated wiki.

| Type | Value | Usage |
|------|-------|-------|
| Default | 1px solid var(--border-default) | Controls and repeated entries |
| Subtle | 1px solid var(--border-subtle) | Section dividers |
