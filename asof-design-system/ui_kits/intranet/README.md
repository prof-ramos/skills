# ASOF Intranet — UI Kit

High-fidelity recreation of the ASOF Intranet (web). The kit boots into the
authenticated `/app` shell with the navy sidebar and the diretoria dashboard;
nav items in the sidebar switch between three live screens.

## Files

- `index.html` — entry point. Loads `colors_and_type.css` from the root +
  `kit.css`, React 18.3.1 + Babel standalone, Lucide UMD for icons, then the
  JSX modules below.
- `kit.css` — layout & utility styles supplementing the root token sheet.
- `data.jsx` — seed data (Brazilian Portuguese): KPI stripe, kanban columns,
  associates table, top countries.
- `primitives.jsx` — `Icon`, `PageHeader`, `Button`, `IconButton`, `KpiCard`,
  `StatusDot`, `PriorityLabel`, `Badge`, `Avatar`.
- `Sidebar.jsx` — navy institutional rail with logo cap, nav items, footer.
- `Dashboard.jsx` — KPI strip, 2×2 "Atividades em curso" grid, side panel
  with Pendências / Comunicação / Países.
- `Associados.jsx` — sticky search header, navy-headed table, pill
  statuses, paginator.
- `Atividades.jsx` — full 4-column kanban; click a card to cycle its
  status; quick-add per column.
- `Login.jsx` — navy backdrop, white card, focus-ring on input.
- `app.jsx` — root + route switcher (dashboard / associados / atividades /
  placeholder for jurídico / ofícios / financeiro / config).

## Try it

Open `index.html`. The demo logs you in as `Helena Vasconcelos · diretoria`.
- Click the **sidebar** to switch screens.
- On **Atividades**, click any kanban card to advance its status (a_fazer →
  em_andamento → aguardando_terceiros → concluido → a_fazer).
- On **Associados**, type in the search box to filter.
- Click **Sair** (sidebar footer) to land on the login screen, then submit
  to return.

## Fidelity notes

- The production app uses **Lucide React + Tailwind 4 + DaisyUI**. The kit
  uses **Lucide UMD + plain CSS** so it renders standalone. Markup is
  intentionally flatter than production — the goal is *visual* fidelity,
  not a re-implementation.
- Drag-and-drop on the kanban (`@hello-pangea/dnd` in production) is
  replaced with click-to-cycle for the kit.
- Drawer + reassign modal are not recreated; status cycling is the visible
  state change.
- All screens beyond the three above show a "Tela em construção" empty
  state — recreating them would duplicate code without adding kit value.
