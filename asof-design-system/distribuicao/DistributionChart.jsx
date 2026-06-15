// DistributionChart — Recharts visualization of associate distribution.
// Two views toggled by a segmented control inside the card header:
//   1. "Por lotação"        — horizontal bar chart, sorted descending
//   2. "Por situação funcional" — donut + legend
//
// Card chrome and typography follow ASOF tokens (Playfair title, Google Sans
// body, hairline border, 16px radius, no shadow). Recharts components are
// pulled off the global `Recharts` UMD bundle.

function DistributionChart() {
  const {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    Cell, PieChart, Pie, LabelList,
  } = window.Recharts;

  const [view, setView] = React.useState('lotacao');

  const lotacao = window.LOTACAO_DISTRIBUTION;
  const situacao = window.SITUACAO_DISTRIBUTION;
  const totalLotacao = lotacao.reduce((s, d) => s + d.total, 0);
  const totalSituacao = situacao.reduce((s, d) => s + d.total, 0);

  const fmt = (n) => n.toLocaleString('pt-BR');
  const pct = (n, total) => ((n / total) * 100).toFixed(1).replace('.', ',') + '%';

  // ── tooltip ──────────────────────────────────────────────────────────────
  const tooltipStyle = {
    background: '#fff',
    border: '1px solid rgba(4,9,32,0.05)',
    borderRadius: 10,
    boxShadow: '0 8px 20px rgba(4,9,32,0.08)',
    padding: '10px 14px',
    fontFamily: 'var(--font-sans)',
  };

  const LotacaoTooltip = ({ active, payload }) => {
    if (!active || !payload || !payload.length) return null;
    const d = payload[0].payload;
    return (
      <div style={tooltipStyle}>
        <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.06em', textTransform: 'uppercase', color: 'var(--fg-4)' }}>Lotação</div>
        <div style={{ fontSize: 14, fontWeight: 600, color: 'var(--on-surface)', marginTop: 2 }}>{d.lotacao}</div>
        <div style={{ marginTop: 6, fontSize: 13, color: 'var(--fg-3)', fontVariantNumeric: 'tabular-nums' }}>
          <span style={{ color: 'var(--primary)', fontWeight: 700 }}>{fmt(d.total)}</span> associados · {pct(d.total, totalLotacao)}
        </div>
      </div>
    );
  };

  const SituacaoTooltip = ({ active, payload }) => {
    if (!active || !payload || !payload.length) return null;
    const d = payload[0].payload;
    return (
      <div style={tooltipStyle}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ display: 'inline-block', width: 10, height: 10, borderRadius: 2, background: d.color }} />
          <span style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.06em', textTransform: 'uppercase', color: 'var(--fg-4)' }}>Situação</span>
        </div>
        <div style={{ fontSize: 14, fontWeight: 600, color: 'var(--on-surface)', marginTop: 4 }}>{d.situacao}</div>
        <div style={{ marginTop: 6, fontSize: 13, color: 'var(--fg-3)', fontVariantNumeric: 'tabular-nums' }}>
          <span style={{ color: 'var(--primary)', fontWeight: 700 }}>{fmt(d.total)}</span> associados · {pct(d.total, totalSituacao)}
        </div>
      </div>
    );
  };

  // ── views ────────────────────────────────────────────────────────────────
  const LotacaoView = () => (
    <div style={{ width: '100%', height: lotacao.length * 34 + 16 }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={lotacao}
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
            tick={{ fill: 'rgba(13,31,60,0.70)', fontSize: 12, fontFamily: 'var(--font-sans)' }}
            tickLine={false}
            axisLine={false}
          />
          <Tooltip cursor={{ fill: 'rgba(4,9,32,0.04)' }} content={<LotacaoTooltip />} />
          <Bar dataKey="total" fill="var(--primary)" radius={[0, 3, 3, 0]} barSize={18} isAnimationActive={false}>
            <LabelList
              dataKey="total"
              position="right"
              formatter={fmt}
              style={{ fill: 'var(--primary)', fontSize: 12, fontWeight: 700, fontFamily: 'var(--font-sans)', fontVariantNumeric: 'tabular-nums' }}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );

  const SituacaoView = () => (
    <div style={{ display: 'grid', gridTemplateColumns: '280px 1fr', gap: 32, alignItems: 'center' }}>
      <div style={{ position: 'relative', width: 280, height: 280 }}>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={situacao}
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
              isAnimationActive={false}
            >
              {situacao.map((d) => <Cell key={d.key} fill={d.color} />)}
            </Pie>
            <Tooltip content={<SituacaoTooltip />} />
          </PieChart>
        </ResponsiveContainer>
        <div style={{
          position: 'absolute', inset: 0, display: 'grid', placeContent: 'center',
          textAlign: 'center', pointerEvents: 'none',
        }}>
          <div style={{ fontSize: 30, fontWeight: 700, color: 'var(--primary)', lineHeight: 1, fontVariantNumeric: 'tabular-nums' }}>
            {fmt(totalSituacao)}
          </div>
          <div style={{ fontSize: 10, letterSpacing: '0.18em', textTransform: 'uppercase', color: 'var(--fg-4)', marginTop: 8, fontWeight: 700 }}>
            Associados
          </div>
        </div>
      </div>

      <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: 14 }}>
        {situacao.map((d) => {
          const percentage = (d.total / totalSituacao) * 100;
          return (
            <li key={d.key} style={{ display: 'grid', gridTemplateColumns: 'auto 1fr auto', gap: 12, alignItems: 'center' }}>
              <span style={{ display: 'inline-block', width: 10, height: 10, borderRadius: 2, background: d.color }} />
              <div style={{ minWidth: 0 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 6 }}>
                  <span style={{ fontSize: 13, fontWeight: 500, color: 'var(--on-surface)' }}>{d.situacao}</span>
                  <span style={{ fontSize: 13, fontWeight: 700, color: 'var(--primary)', fontVariantNumeric: 'tabular-nums' }}>
                    {fmt(d.total)}
                    <span style={{ marginLeft: 8, fontSize: 11, color: 'var(--fg-4)', fontWeight: 400 }}>
                      {pct(d.total, totalSituacao)}
                    </span>
                  </span>
                </div>
                <div style={{ height: 6, background: 'var(--surface-container-low)', borderRadius: 9999, overflow: 'hidden' }}>
                  <div style={{ width: `${percentage}%`, height: '100%', background: d.color, borderRadius: 9999 }} />
                </div>
              </div>
              <span />
            </li>
          );
        })}
      </ul>
    </div>
  );

  // ── render ───────────────────────────────────────────────────────────────
  return (
    <div className="card">
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 16, marginBottom: 8, flexWrap: 'wrap' }}>
        <div>
          <div className="h-card" style={{ marginBottom: 4 }}>
            <span className="ico"><Icon name="pie-chart" size={20} color="#76aeea" /></span>
            <h2>Distribuição de associados</h2>
          </div>
          <div style={{ fontSize: 12, color: 'var(--fg-3)', marginLeft: 28 }}>
            Quadro associativo segmentado por {view === 'lotacao' ? 'lotação atual' : 'situação funcional'}.
          </div>
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

      <div style={{ marginTop: 20 }}>
        {view === 'lotacao' ? <LotacaoView /> : <SituacaoView />}
      </div>

      <footer style={{
        marginTop: 20, paddingTop: 16, borderTop: '1px solid var(--border-hairline)',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16, flexWrap: 'wrap',
      }}>
        <div style={{ fontSize: 11, color: 'var(--fg-4)', letterSpacing: '0.10em', textTransform: 'uppercase', fontWeight: 700 }}>
          {view === 'lotacao'
            ? `${lotacao.length} lotações · ${fmt(totalLotacao)} associados`
            : `${situacao.length} situações · ${fmt(totalSituacao)} associados`}
        </div>
        <a className="link-action">
          {view === 'lotacao' ? 'Abrir quadro associativo' : 'Exportar relatório'}
          <Icon name="arrow-right" size={14} />
        </a>
      </footer>
    </div>
  );
}

// Local segmented control — matches the ASOF inline toggle used elsewhere.
function Segmented({ value, onChange, options }) {
  return (
    <div role="tablist" style={{
      display: 'inline-flex',
      padding: 3,
      background: 'var(--surface-container-low)',
      border: '1px solid var(--border-hairline)',
      borderRadius: 9999,
    }}>
      {options.map((opt) => {
        const active = opt.value === value;
        return (
          <button
            key={opt.value}
            role="tab"
            aria-selected={active}
            onClick={() => onChange(opt.value)}
            style={{
              border: 0,
              background: active ? '#fff' : 'transparent',
              color: active ? 'var(--primary)' : 'var(--fg-3)',
              padding: '7px 14px',
              fontSize: 12,
              fontWeight: 600,
              borderRadius: 9999,
              transition: 'background-color 120ms ease, color 120ms',
              boxShadow: active ? '0 1px 2px rgba(4,9,32,0.08)' : 'none',
              cursor: 'pointer',
              fontFamily: 'var(--font-sans)',
            }}
          >
            {opt.label}
          </button>
        );
      })}
    </div>
  );
}

Object.assign(window, { DistributionChart, Segmented });
