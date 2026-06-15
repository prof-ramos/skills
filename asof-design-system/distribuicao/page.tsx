// =============================================================================
// REFERENCE — production code for `src/app/app/page.tsx` in `prof-ramos/intranet`
//
// Drop the <DistribuicaoAssociadosCard /> import into the existing dashboard
// page below the kanban grid. The component is fully client-side (Recharts
// hooks) so the parent page can stay a Server Component — Recharts and its
// state live behind the `'use client'` directive in the component file.
//
// Required dependency:    pnpm add recharts
// Suggested file layout:  src/app/app/_dashboard/DistribuicaoAssociadosCard.tsx
// =============================================================================


// -----------------------------------------------------------------------------
// 1)  src/app/app/_dashboard/DistribuicaoAssociadosCard.tsx
// -----------------------------------------------------------------------------
'use client';

import { useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  Cell, PieChart, Pie, LabelList,
} from 'recharts';
import { PieChart as PieChartIcon, ArrowRight } from 'lucide-react';

// ── Data ─────────────────────────────────────────────────────────────────────
// In production, replace these consts with data fetched server-side and
// passed via props (or read from a Server Action / route handler).

type LotacaoRow   = { lotacao: string;  total: number };
type SituacaoRow  = { situacao: string; key: string; total: number; color: string };

const LOTACAO: LotacaoRow[] = [
  { lotacao: 'SERE — Brasília',           total: 412 },
  { lotacao: 'Embaixada em Washington',   total: 84  },
  { lotacao: 'Embaixada em Paris',        total: 76  },
  { lotacao: 'Embaixada em Lisboa',       total: 62  },
  { lotacao: 'Embaixada em Buenos Aires', total: 58  },
  { lotacao: 'Embaixada em Tóquio',       total: 47  },
  { lotacao: 'Embaixada em Berlim',       total: 41  },
  { lotacao: 'Embaixada em Madri',        total: 38  },
  { lotacao: 'Consulado em Nova York',    total: 35  },
  { lotacao: 'Embaixada em Pretória',     total: 28  },
  { lotacao: 'Demais postos',             total: 219 },
];

const SITUACAO: SituacaoRow[] = [
  { situacao: 'Ativo',      key: 'ativo',      total: 1284, color: '#15803d' },
  { situacao: 'Aposentado', key: 'aposentado', total: 342,  color: '#475569' },
  { situacao: 'Em licença', key: 'em_licenca', total: 42,   color: '#a16207' },
  { situacao: 'Cedido',     key: 'cedido',     total: 28,   color: '#1d4ed8' },
];

// ── Utils ────────────────────────────────────────────────────────────────────
const fmt = (n: number) => n.toLocaleString('pt-BR');
const pct = (n: number, total: number) =>
  ((n / total) * 100).toFixed(1).replace('.', ',') + '%';

// ── Component ────────────────────────────────────────────────────────────────

type View = 'lotacao' | 'situacao';

export default function DistribuicaoAssociadosCard({
  lotacaoData = LOTACAO,
  situacaoData = SITUACAO,
}: {
  lotacaoData?: LotacaoRow[];
  situacaoData?: SituacaoRow[];
}) {
  const [view, setView] = useState<View>('lotacao');

  const totalLotacao  = lotacaoData.reduce((s, d) => s + d.total, 0);
  const totalSituacao = situacaoData.reduce((s, d) => s + d.total, 0);

  return (
    <section
      aria-label="Distribuição de associados"
      className="rounded-2xl border border-base-300/60 bg-base-100 p-5 md:p-6"
    >
      {/* Header — Playfair title + segmented control */}
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <PieChartIcon className="size-5 text-secondary" aria-hidden />
            <h2 className="font-serif text-xl font-bold leading-tight text-base-content">
              Distribuição de associados
            </h2>
          </div>
          <p className="ml-7 mt-1 text-xs text-base-content/60">
            Quadro associativo segmentado por{' '}
            {view === 'lotacao' ? 'lotação atual' : 'situação funcional'}.
          </p>
        </div>

        <Segmented
          value={view}
          onChange={setView}
          options={[
            { value: 'lotacao',  label: 'Por lotação' },
            { value: 'situacao', label: 'Por situação funcional' },
          ]}
        />
      </div>

      {/* Chart */}
      <div className="mt-5">
        {view === 'lotacao'
          ? <LotacaoView data={lotacaoData} total={totalLotacao} />
          : <SituacaoView data={situacaoData} total={totalSituacao} />}
      </div>

      {/* Footer */}
      <footer className="mt-5 flex flex-wrap items-center justify-between gap-3 border-t border-base-300/60 pt-4">
        <div className="text-[11px] font-bold uppercase tracking-[0.10em] text-base-content/50">
          {view === 'lotacao'
            ? `${lotacaoData.length} lotações · ${fmt(totalLotacao)} associados`
            : `${situacaoData.length} situações · ${fmt(totalSituacao)} associados`}
        </div>
        <a
          href={view === 'lotacao' ? '/app/associados' : '#'}
          className="inline-flex items-center gap-1.5 text-sm font-semibold text-secondary hover:underline"
        >
          {view === 'lotacao' ? 'Abrir quadro associativo' : 'Exportar relatório'}
          <ArrowRight className="size-3.5" aria-hidden />
        </a>
      </footer>
    </section>
  );
}

// ── Subcomponents ───────────────────────────────────────────────────────────

function Segmented<T extends string>({
  value, onChange, options,
}: {
  value: T;
  onChange: (v: T) => void;
  options: { value: T; label: string }[];
}) {
  return (
    <div role="tablist" className="inline-flex rounded-full border border-base-300/60 bg-base-200/60 p-[3px]">
      {options.map((opt) => {
        const active = opt.value === value;
        return (
          <button
            key={opt.value}
            role="tab"
            type="button"
            aria-selected={active}
            onClick={() => onChange(opt.value)}
            className={[
              'rounded-full px-3.5 py-1.5 text-xs font-semibold transition-colors',
              'focus-visible:outline focus-visible:outline-2 focus-visible:outline-secondary focus-visible:outline-offset-2',
              active
                ? 'bg-base-100 text-primary shadow-[0_1px_2px_rgba(4,9,32,0.08)]'
                : 'text-base-content/60 hover:text-base-content',
            ].join(' ')}
          >
            {opt.label}
          </button>
        );
      })}
    </div>
  );
}

function LotacaoView({ data, total }: { data: LotacaoRow[]; total: number }) {
  return (
    <div style={{ width: '100%', height: data.length * 34 + 16 }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 4, right: 72, bottom: 4, left: 0 }}
          barCategoryGap={8}
        >
          <CartesianGrid horizontal={false} stroke="rgba(4,9,32,0.05)" />
          <XAxis type="number" hide />
          <YAxis
            type="category"
            dataKey="lotacao"
            width={220}
            tick={{ fill: 'rgba(13,31,60,0.70)', fontSize: 12 }}
            tickLine={false}
            axisLine={false}
          />
          <Tooltip
            cursor={{ fill: 'rgba(4,9,32,0.04)' }}
            content={(props) => <LotacaoTooltip {...props} total={total} />}
          />
          <Bar dataKey="total" fill="#040920" radius={[0, 3, 3, 0]} barSize={18}>
            <LabelList
              dataKey="total"
              position="right"
              formatter={fmt}
              style={{ fill: '#040920', fontSize: 12, fontWeight: 700, fontVariantNumeric: 'tabular-nums' }}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function SituacaoView({ data, total }: { data: SituacaoRow[]; total: number }) {
  return (
    <div className="grid items-center gap-8 md:grid-cols-[280px_1fr]">
      <div className="relative size-[280px]">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="total"
              nameKey="situacao"
              cx="50%"
              cy="50%"
              innerRadius={78}
              outerRadius={116}
              stroke="#fff"
              strokeWidth={3}
              startAngle={90}
              endAngle={-270}
            >
              {data.map((d) => <Cell key={d.key} fill={d.color} />)}
            </Pie>
            <Tooltip content={(props) => <SituacaoTooltip {...props} total={total} />} />
          </PieChart>
        </ResponsiveContainer>
        <div className="pointer-events-none absolute inset-0 grid place-content-center text-center">
          <div className="font-sans text-3xl font-bold leading-none text-primary tabular-nums">
            {fmt(total)}
          </div>
          <div className="mt-2 text-[10px] font-bold uppercase tracking-[0.18em] text-base-content/50">
            Associados
          </div>
        </div>
      </div>

      <ul className="m-0 flex list-none flex-col gap-3.5 p-0">
        {data.map((d) => {
          const percentage = (d.total / total) * 100;
          return (
            <li key={d.key} className="grid grid-cols-[auto_1fr] items-center gap-3">
              <span
                className="inline-block size-2.5 rounded-[2px]"
                style={{ background: d.color }}
              />
              <div className="min-w-0">
                <div className="mb-1.5 flex items-baseline justify-between">
                  <span className="text-sm font-medium">{d.situacao}</span>
                  <span className="text-sm font-bold text-primary tabular-nums">
                    {fmt(d.total)}
                    <span className="ml-2 text-[11px] font-normal text-base-content/50">
                      {pct(d.total, total)}
                    </span>
                  </span>
                </div>
                <div className="h-1.5 overflow-hidden rounded-full bg-base-200">
                  <div className="h-full rounded-full" style={{ width: `${percentage}%`, background: d.color }} />
                </div>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

// ── Tooltips ─────────────────────────────────────────────────────────────────

type TooltipProps = {
  active?: boolean;
  payload?: Array<{ payload: any }>;
  total: number;
};

function LotacaoTooltip({ active, payload, total }: TooltipProps) {
  if (!active || !payload || !payload.length) return null;
  const d = payload[0].payload as LotacaoRow;
  return (
    <div className="rounded-[10px] border border-base-300/60 bg-base-100 px-3.5 py-2.5 shadow-[0_8px_20px_rgba(4,9,32,0.08)]">
      <div className="text-[11px] font-bold uppercase tracking-[0.06em] text-base-content/50">Lotação</div>
      <div className="mt-0.5 text-sm font-semibold">{d.lotacao}</div>
      <div className="mt-1.5 text-[13px] text-base-content/70 tabular-nums">
        <span className="font-bold text-primary">{fmt(d.total)}</span> associados · {pct(d.total, total)}
      </div>
    </div>
  );
}

function SituacaoTooltip({ active, payload, total }: TooltipProps) {
  if (!active || !payload || !payload.length) return null;
  const d = payload[0].payload as SituacaoRow;
  return (
    <div className="rounded-[10px] border border-base-300/60 bg-base-100 px-3.5 py-2.5 shadow-[0_8px_20px_rgba(4,9,32,0.08)]">
      <div className="flex items-center gap-2">
        <span className="inline-block size-2.5 rounded-[2px]" style={{ background: d.color }} />
        <span className="text-[11px] font-bold uppercase tracking-[0.06em] text-base-content/50">Situação</span>
      </div>
      <div className="mt-1 text-sm font-semibold">{d.situacao}</div>
      <div className="mt-1.5 text-[13px] text-base-content/70 tabular-nums">
        <span className="font-bold text-primary">{fmt(d.total)}</span> associados · {pct(d.total, total)}
      </div>
    </div>
  );
}


// -----------------------------------------------------------------------------
// 2)  Wiring it into src/app/app/page.tsx
// -----------------------------------------------------------------------------
//
// import DistribuicaoAssociadosCard from './_dashboard/DistribuicaoAssociadosCard';
//
// export default function PainelAdministrativoPage() {
//   return (
//     <main className="page mx-auto w-full max-w-[1180px] px-10 py-7">
//       <PageHeader eyebrow={…} title="Painel administrativo" actions={…} />
//
//       <KpiStrip … />
//
//       <section className="grid grid-cols-1 lg:grid-cols-[1fr_280px] gap-7 items-start">
//         {/* existing atividades-em-curso + aside */}
//       </section>
//
//       {/* NEW: distribution chart, full-width below */}
//       <section className="mt-7" aria-label="Distribuição de associados">
//         <DistribuicaoAssociadosCard
//           lotacaoData={await getLotacaoDistribution()}
//           situacaoData={await getSituacaoDistribution()}
//         />
//       </section>
//     </main>
//   );
// }
//
// Server-side aggregation suggestion (in a `getDistribuicao()` helper):
//
//   SELECT lotacao AS lotacao, COUNT(*)::int AS total
//   FROM associados
//   GROUP BY lotacao
//   ORDER BY total DESC
//   LIMIT 10;
//
//   SELECT situacao AS situacao, COUNT(*)::int AS total
//   FROM associados
//   GROUP BY situacao;
//
