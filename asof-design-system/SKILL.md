---
name: asof-design
description: Use this skill to generate well-branded interfaces and assets for ASOF (Associação Nacional dos Oficiais de Chancelaria do Serviço Exterior Brasileiro), either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Where things live

- `README.md` — full design system reference (content fundamentals, visual foundations, iconography)
- `colors_and_type.css` — CSS variables for tokens + semantic element styles. Load this first when prototyping.
- `fonts/` — production variable WOFF2 fonts (Google Sans + Playfair Display)
- `assets/` — ASOF logo and favicon SVGs
- `ui_kits/intranet/` — high-fidelity recreations of the ASOF Intranet (sidebar shell, dashboard, associados table, atividades kanban). Read `index.html` first; component JSX files are loadable as Babel scripts.
- `preview/` — small specimen cards used in the Design System tab; useful as a quick token reference.

## Quick rules

- **Language:** copy is **Brazilian Portuguese** unless instructed otherwise.
- **Fonts:** Playfair Display (serif) for titles only; Google Sans for everything else.
- **Color:** navy `#040920` for primary; pale blue-gray canvas `#f8fafc`; white surfaces. Use sky blue `#76aeea` only as an accent (focus / progress / KPI top-stripe). Never large saturated blocks.
- **Shape:** 16px for cards, 8px for controls, 8×8 squared status dots. Avoid playful rounding.
- **Elevation:** hairlines do the work — `1px solid rgba(4, 9, 32, 0.05)`. Shadows only on overlays.
- **No emoji, no gradients, no glass/blur, no marketing voice.**
- **Iconography:** Lucide, stroke-based, 16–20px, `currentColor`.
