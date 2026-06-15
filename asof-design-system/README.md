# ASOF Design System

A design system extracted from the **ASOF Intranet** — the internal operations
platform for the **Associação Nacional dos Oficiais de Chancelaria do Serviço
Exterior Brasileiro** (ASOF), the professional association representing the
Chancellery officers of Brazil's diplomatic service.

The product is a back-office tool for the association's executive board
(`diretoria`), secretariat (`secretaria`), and IT administrators — used to
manage members (`associados`), monthly dues, legal cases (`jurídico`), official
letters (`ofícios`), and an administrative kanban of internal activities.

The visual language blends **diplomatic restraint** with **administrative
density**: large Playfair Display serif titles set on a pale blue-gray canvas,
an almost-black navy for primary action, sky blue used sparingly as a status
accent, and small operational status markers rather than colored blocks.

---

## Sources

This system was built from the following repositories. Browse them for richer
context if you have access:

- **`prof-ramos/intranet`** — https://github.com/prof-ramos/intranet  
  Production Next.js codebase. Source of truth for tokens, components, and
  copywriting. Key files: `DESIGN.md` (canonical design spec), `CONTEXT.md`
  (domain glossary), `PAGES.md` (route catalogue), `src/lib/ui/tokens.ts`
  (color/spacing constants), `src/components/Sidebar.tsx`,
  `src/app/app/atividades/AtividadesBoard.tsx` (kanban),
  `src/app/app/_dashboard/*` (dashboard widgets), `src/app/app/globals.css`
  (DaisyUI theme).

- **`prof-ramos/logos_asof`** — https://github.com/prof-ramos/logos_asof  
  ASOF logo in production and source forms (SVG).

The intranet repo is the canonical reference — when in doubt, read the
component there before extending this system.

---

## Index

```
ASOF Design System/
├── README.md                ← you are here
├── SKILL.md                 ← agent skill entry-point
├── colors_and_type.css      ← CSS variables: tokens + semantic styles
├── fonts/
│   ├── GoogleSans-Variable.woff2
│   └── Playfair-Variable.woff2
├── assets/
│   ├── asof-logo-lockup.svg ← primary horizontal lockup (1576×475)
│   ├── asof-logo-lockup.png ← same lockup, raster (6304×1900)
│   ├── asof-logo-full.png   ← stacked lockup with full association name
│   └── asof-favicon.svg     ← favicon mark (globe only)
├── preview/                 ← Design System tab cards (small specimens)
├── ui_kits/
│   └── intranet/            ← Intranet UI kit (web) — sidebar shell,
│                              dashboard, associados table, kanban
└── slides/                  ← (not used — no deck templates provided)
```

---

## Brand Identity

**Name:** ASOF — Associação dos Oficiais de Chancelaria
**Tagline / role:** Sistema interno · Sala de operações
**Voice:** Institutional, formal-but-functional, Brazilian Portuguese.
**Domain register:** Diplomatic chancellery — letters use the *Padrão Ofício*
(Manual de Redação da Presidência da República), with vocatives, signatários,
and fechos (closures).

---

## CONTENT FUNDAMENTALS

The interface is written in **Brazilian Portuguese** (`lang="pt-BR"`). Copy is
written for a small, professional audience that knows the domain — the system
**does not over-explain**, but it **is precise**.

### Tone

- **Formal-functional, not ceremonial.** The voice respects the institutional
  setting (this is a diplomatic association) but does not slow work down with
  flourishes. Headlines feel like the title page of a briefing; supporting
  copy reads like a well-organized memo.
- **No marketing voice.** No emoji, no exclamation marks, no second-person
  cheer ("Let's get started!"). Confirmations are dry: *"Alterações no quadro
  são salvas imediatamente e entram no histórico da atividade."*
- **Voice is third-person / impersonal** by default. The system talks *about*
  records ("Nenhuma atividade cadastrada ainda"), not *to* the user, except
  when greeting them in the sidebar: *"Olá, {firstName}. Logado como
  {role}."*
- **Casing.** Titles use **sentence case** (`Painel administrativo`,
  `Quadro associativo`). Eyebrows and field labels use **UPPERCASE** with
  generous tracking (0.18em). Status badges are also uppercase, tighter
  (0.06–0.10em). Buttons are sentence-case, semibold, action-oriented
  (`Nova atividade`, `Abrir kanban`, `Ver todos`).
- **Domain vocabulary stays in Portuguese**, untranslated. Use the real terms:
  *Associados, Atividades, Ofícios, Jurídico, Financeiro, Mensalidades,
  Lotação, Posto, Padrão / Classe, SIAPE, Parecer, Consulta, Diretoria,
  Secretaria*.

### Eyebrow → Title pattern

Every page header opens with a short uppercase **eyebrow** that anchors the
context, followed by a large serif **title** in sentence case. The eyebrow
often includes the current date or the operational area:

> `SALA DE OPERAÇÕES · TERÇA-FEIRA, 19 DE MAIO DE 2026`  
> **Painel administrativo**

> `QUADRO ASSOCIATIVO · TERÇA-FEIRA, 19 DE MAIO DE 2026`  
> **Associados**

> `OPERAÇÃO · QUADRO DE ATIVIDADES`  
> **Atividades**

### Empty / waiting / error states

Empty states are short, declarative, and never apologetic:
- *"Nenhum associado encontrado."*
- *"Nenhuma atividade atrasada."*
- *"Em desenvolvimento — Métricas de e-mail e SLA em breve."*

Error states say what failed and what to do, no exclamation marks:
- *"Não foi possível salvar a atividade. Tente novamente."*
- *"Email ou senha inválidos."*

### Status & priority labels

- **Status** (kanban): `A fazer`, `Em andamento`, `Aguardando terceiros`,
  `Concluído`.
- **Priority**: `Baixa`, `Normal`, `Alta`, `Urgente`.
- **Membership status (situação funcional)**: `Ativo`, `Aposentado`, `Cedido`,
  `Em licença`.
- **Contribution**: `Em dia`, `Inadimplente`, `Pendente migração`, `Isento`.

### Emoji

**Never.** The product does not use emoji. Status is communicated through
small color dots and uppercase text badges.

---

## VISUAL FOUNDATIONS

### Color

The palette is **light and cool**. The page canvas is a very pale blue-gray
(`--background: #f8fafc`); content sits on **white panels**. The primary
interaction color is an **almost-black navy** (`--primary: #040920`) and the
sidebar uses a slightly lighter institutional navy (`--primary-container:
#06284f`). High contrast without ever feeling consumer-y or loud.

- **Sky blue (`#76aeea`)** is used *sparingly*, only as: active-nav
  left-border, focus-ring, KPI top-stripe, progress bars, and as the text
  color for inline "Open kanban →" style links inside cards.
- **Amber (`#e7c16b / #a16207`)** signals *waiting / cautionary / legal*
  context and medium-risk priority. Soft amber for backgrounds
  (`--warning-container: #f4ddb1`), darker amber for text.
- **Green (`#15803d / #86efac`)** signals *completion, contribution health,
  successful confirmation*.
- **Red (`#b91c1c`)** is reserved for *overdue, urgent, destructive, or
  blocked* states.

Status is **never** communicated by a large saturated block. The pattern is
white card → 8px status dot (small, slightly rounded `2px` square) → small
uppercase text badge.

### Typography

Two typefaces, one rule:

- **Playfair Display** (serif) — every page title, section heading, and
  card title. Tight line-height (`1` to `1.08`), bold (700), navy color, never
  uppercase, never tracked open.
- **Google Sans** (sans) — every other text on screen: body, labels, table
  cells, buttons, metrics. Body sizes stay in the **12–16px** band; only page
  titles and headline metrics break that density.

Eyebrows, badges, and field labels use Google Sans uppercase with wide
tracking (`0.06em → 0.18em`) — these give pages the rhythm of a formal
dossier.

Metrics in dashboards are 30px, 700, Google Sans, tabular-nums, navy — *not*
Playfair. The serif is reserved for headings only.

### Spacing & rhythm

- **4px base unit.** Operational clusters use 12 / 16 / 20 / 28 / 40px gaps.
- **Page max-width:** 1180px, centered. Outer padding 20 / 32 / 40 px across
  mobile / tablet / desktop.
- **Sidebar width:** 288px (fixed) on `md+`, drawer-overlay on smaller.
- **Section-to-section gap:** 28px is the default rhythm between major page
  sections.

### Backgrounds

- **No imagery, no gradients, no decorative blobs, no glass.** The canvas is
  flat `#f8fafc`. Section dividers come from white panels sitting on the
  canvas with a 1px hairline border.
- The **only gradient** in production is a vertical navy gradient inside the
  sidebar logo cap (`linear-gradient(180deg, #031a35 0%, #06284f 100%)`) —
  used to seat the logo, never elsewhere.
- Kanban columns have a subtle pale fill (`#eef1f6`) to set them apart from
  the canvas; cards inside are white.

### Shape language (radii)

Moderately soft, administrative. **Never playful, never pill-heavy.**

- `--r-md: 8px` — buttons, inputs, kanban cards, segmented controls (default)
- `--r-lg: 10px` — compact cards, alerts, login surface
- `--r-box: 16px` — full-width content panels, dashboard cards, kanban
  columns
- `--r-full` — pills used **only** for badges, avatars, tags, and segmented
  controls
- Status dots are 8×8px with a 2px corner radius — squared, not circular —
  reinforcing the operational dashboard feel.

### Elevation

**Hairlines do the work, not shadows.** Most cards use a 1px
`rgba(4, 9, 32, 0.05)` border with no shadow. Stronger shadows appear only on:

- Popovers — `0 8px 20px rgba(4, 9, 32, 0.08)`
- Drawers — `-12px 0 30px rgba(4, 9, 32, 0.12)` (right-side, navy-tinted)
- Modals — `0 24px 60px rgba(4, 9, 32, 0.25)`
- KPI cards may carry a **top stripe** of `3px var(--secondary)` instead of a
  shadow — institutional and quiet.

### Hover / press / focus

- **Sidebar items:** hover → fill with `#0d3260` (one shade up from sidebar
  navy); active → `#123d73` + 6px sky-blue left border. Inactive text is
  `rgba(255,255,255,0.70)`; hover/active is full white.
- **Buttons (primary navy):** hover → `#0d3260`. No scale, no shadow flash.
- **Buttons (secondary outline):** hover → `rgba(4,9,32,0.04)` background, no
  border change.
- **Cards / table rows:** hover background fades to `#f8fafc` (canvas color)
  to reinforce that rows are interactive. Inline edit/action icons
  fade in via `opacity-0 → opacity-100` only on row hover.
- **Focus ring:** `2px solid #76aeea` with a 2px offset — the *only* place
  sky blue is required, applied consistently to every interactive element
  via the shared `focusRingClass` token.
- **Press states** are intentionally restrained — no scale-down, no color
  flash. Transitions run for 120–150ms with the default `ease` curve.

### Borders

- **Hairline** `rgba(4, 9, 32, 0.05)` — card edges, table row separators,
  most internal dividers. The dominant border.
- **Soft** `#dde3ec` — outline-variant for grouping panels.
- **Muted** `#c9d2df` — outline for input fields and stronger separators.
- **Subtle** `rgba(4, 9, 32, 0.15)` — secondary-button outline, pagination
  buttons.
- Dashed borders are used **only for empty-state placeholders** and the
  "Em desenvolvimento" tiles.

### Transparency & blur

- **No backdrop blur anywhere.** No frosted glass.
- Transparency is used only in `rgba(13, 31, 60, …)` foreground steps for
  text (`0.70 → 0.55 → 0.40`), in the dark-mode side rail
  (`rgba(255,255,255,0.10–0.70)`), and for overlay scrims behind drawers
  (`rgba(4, 9, 32, 0.35)`).

### Imagery

Production currently uses **no photography or illustration** inside the
product. The brand mark (logo) is the only graphic. When imagery is needed in
external comms, prefer a **cool, formal register** — neutral whites and
navies, never warm filters, never grain.

### Motion

- **Durations:** 120ms (fast), 150ms (base, the most common), 220ms (slow,
  used for drawers and modals).
- **Easings:** default `ease` for most interactions; `cubic-bezier(0.2, 0, 0, 1)`
  for emphasized transitions (drawer entry).
- **No bounces, no springs, no parallax.** Color and opacity transitions
  only. The system respects `prefers-reduced-motion` and clamps
  durations to `0.01ms` when set.

### Layout rules

- Fixed shell: 288px navy sidebar on the left, 14px-min topbar on mobile
  (with hamburger), content area scrolls on the canvas.
- Pages are centered on a `max-width: 1180px` column.
- Dashboard pages open with: **eyebrow + title** (left), **secondary actions
  + primary action** (right) — primary is the only navy button on the row.
- KPI strips run in a 1 / 2 / 5 column grid (mobile / tablet / desktop).
- Kanban columns scroll horizontally on mobile (`snap-x snap-mandatory`),
  switch to a 2-up grid on tablet, and 4-up on desktop. Each column has a
  squared status dot, an uppercase status label, and a numeric count.

### Cards

The default card is:

```
background: #ffffff
border:     1px solid rgba(4, 9, 32, 0.05)
radius:     16px
padding:    20px
shadow:     none
```

Form cards bump padding to 28px. Kanban cards drop to `r-md: 8px` and
`padding: 12px`. KPI cards add a `3px solid #76aeea` top border to mark them
as institutional indicators.

---

## ICONOGRAPHY

The intranet uses **[Lucide](https://lucide.dev)** icons exclusively, imported
as `lucide-react`. Lucide is a clean, single-weight, stroke-based set that
matches the system's restrained, administrative tone.

- **Style:** stroke-based outline icons, `1.5` to `2` stroke width (Lucide
  default).
- **Default sizes:** `20px` in primary nav and section headers, `18px` in
  sub-nav items, `16px` inline with buttons / link labels, `14px` for
  decorative chevrons.
- **Color:** `currentColor` — they inherit the text color of their context.
  Inside cards: `var(--secondary)` (sky blue) when used as a section-heading
  marker (e.g., the *Megaphone* / *Mail* / *Globe* icons in the dashboard
  sidebar). Status icons (`AlertTriangle`) use the semantic color directly
  (`var(--error)` / `#b91c1c`).
- **Common icons in use:** `LayoutDashboard`, `Users`, `Kanban`, `Scale`,
  `FileSpreadsheet`, `DollarSign`, `Receipt`, `Settings`, `Shield`,
  `ShieldCheck`, `MapPin`, `Webhook`, `Calendar`, `Plus`, `Search`,
  `ChevronLeft`, `ChevronRight`, `ChevronDown`, `Pencil`, `Download`,
  `Menu`, `ArrowRight`, `AlertTriangle`, `Clock`, `Megaphone`, `Mail`,
  `Globe`.

This design system links Lucide from CDN (`https://unpkg.com/lucide@latest`)
in the UI kit demos. Use `<i data-lucide="name"></i>` or the React package in
production.

- **Emoji:** never used. The visual system rejects emoji as inconsistent with
  the institutional register.
- **Unicode symbols:** `·` (middle dot) is used as a separator inside eyebrows
  (e.g., *"Sala de operações · 19 de maio de 2026"*); `→` and `←` appear only
  through Lucide arrow icons.

### Logo

Three files cover every usage:

- **`assets/asof-logo-lockup.svg`** — the canonical **horizontal lockup**:
  black `AS` + `F` wordmark wrapping a blue globe-with-arrow ideogram. This
  is the primary mark — use it in app chrome, headers, and any context that
  has its own caption or sub-title. 1576×475 (≈3.3:1).
- **`assets/asof-logo-lockup.png`** — same lockup at 6304×1900 for raster
  contexts (slides, social, situations where SVG isn't accepted).
- **`assets/asof-logo-full.png`** — the **stacked full lockup** with the
  association's complete name (*Associação Nacional dos Oficiais de
  Chancelaria do Serviço Exterior Brasileiro*) typeset beneath. Use this on
  the institutional homepage, on the login surface, on cover slides, and
  anywhere the brand needs to identify itself in full.
- **`assets/asof-favicon.svg`** — just the globe-with-arrow ideogram,
  isolated for favicons / app icons.

**On dark surfaces** (navy `#040920` / `#06284f`), apply
`filter: brightness(0) invert(1)` to the lockup SVG — this flattens both the
black wordmark and the colored globe to a single white silhouette, matching
the institutional dark-theme variant used on asof.org.br. The kit's sidebar
demonstrates this treatment.

---

## Font substitutions

Both fonts are the **production binaries** copied from the intranet repo
(`src/app/fonts/`) — no substitutions are needed.

- **Playfair Display** (Variable, weights 600–800) →
  `fonts/Playfair-Variable.woff2`
- **Google Sans** (Variable, weights 400–700) → `fonts/GoogleSans-Variable.woff2`

> ⚠️ **Google Sans** is Google's proprietary corporate typeface and is not
> publicly licensed. The intranet ships a variable WOFF2 of it. If you need a
> licensed substitute for external work, the closest match on Google Fonts is
> **Google Sans Text** (where available), or **Inter** / **DM Sans** as a
> fallback with similar x-height and humanist proportions. Flag this to the
> user before publishing public assets that re-host the font.

---

## UI Kits

- `ui_kits/intranet/` — the ASOF Intranet (web). Includes the sidebar shell,
  dashboard, associados (members) table, and atividades (kanban) board.

---

## Caveats

- The intranet UI uses the **Lucide React** package, plus **DaisyUI** on top
  of Tailwind 4. The UI kit here uses CDN Lucide and plain CSS so the
  prototypes render standalone — visuals are pixel-faithful, but markup is
  flatter than production.
- The Google Sans font ships in the repo but is not openly licensed; see the
  *Font substitutions* note above.
- No slide deck templates were attached for ASOF, so this system does not
  contain a `slides/` directory.
