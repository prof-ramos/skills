// Dashboard with the new "Distribuição de associados" chart card inserted
// below the kanban + sidebar section. Identical to the base Dashboard.jsx
// in ui_kits/intranet/ except for the appended <DistributionChart /> block.

function Dashboard({ user }) {
  const eyebrow = `Sala de operações · ${window.TODAY_LABEL}`;
  return (
    <main className="page">
      <PageHeader
        eyebrow={eyebrow}
        title="Painel administrativo"
        actions={
          <>
            <Button variant="outline" icon="calendar">Esta semana</Button>
            <Button variant="primary" icon="plus">Nova atividade</Button>
          </>
        }
      />

      <section className="kpi-strip" aria-label="Indicadores">
        {window.KPI_STRIPE.map((item) => <KpiCard key={item.id} item={item} />)}
      </section>

      <section className="section-grid">
        <div className="card">
          <div className="h-card" style={{ justifyContent: 'space-between' }}>
            <h2>Atividades em curso</h2>
            <a className="link-action">Abrir kanban <Icon name="arrow-right" size={14} /></a>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 16 }}>
            {window.STATUS_COLUMNS.slice(0, 4).map((col) => (
              <article key={col.status} className="kanban-col" style={{ background: 'var(--surface-container-low)' }}>
                <header>
                  <StatusDot color={col.accent} />
                  <span className="title" style={{ fontSize: 11 }}>{col.label}</span>
                  <span style={{ marginLeft: 'auto', fontSize: 12, fontWeight: 600, color: 'var(--fg-4)' }}>{col.total}</span>
                </header>
                {col.cards.length === 0 ? (
                  <div className="quick-add" style={{ textAlign: 'center' }}>Sem cards</div>
                ) : col.cards.slice(0, 2).map((card) => (
                  <div key={card.id} className="kanban-card">
                    <p className="title">{card.title}</p>
                    <div className="meta">
                      <PriorityLabel priority={card.priority} />
                      {card.dueDate && <span className="due-text">· vence {formatDueDate(card.dueDate)}</span>}
                    </div>
                    <span className="associate-chip">{card.associateLabel || 'Sem associado'}</span>
                  </div>
                ))}
              </article>
            ))}
          </div>
        </div>

        <aside style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          <div className="card">
            <div className="h-card"><span className="ico"><Icon name="megaphone" size={20} color="#76aeea" /></span><h2 style={{ fontSize: 18 }}>Pendências</h2></div>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
              {window.URGENT_ACTIVITIES.map((act) => (
                <li key={act.id} className="pend-item">
                  <Icon name="alert-triangle" size={20} color="#b91c1c" />
                  <div>
                    <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--on-surface)', lineHeight: 1.35 }}>{act.title}</div>
                    <div style={{ fontSize: 12, color: 'var(--fg-3)', marginTop: 4 }}>
                      {window.PRIORITY_STYLES[act.priority]?.label || act.priority} · vencimento {formatDueDate(act.dueDate)}
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>

          <div className="card">
            <div className="h-card"><span className="ico"><Icon name="globe" size={20} color="#76aeea" /></span><h2 style={{ fontSize: 18 }}>Associados por país</h2></div>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: 12 }}>
              {window.TOP_REGIONS.map((r) => (
                <li key={r.country}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 6 }}>
                    <span style={{ fontSize: 13, fontWeight: 500 }}>{r.country}</span>
                    <span style={{ fontSize: 13, fontWeight: 700, fontVariantNumeric: 'tabular-nums' }}>{r.total}<span style={{ marginLeft: 6, fontSize: 11, color: 'var(--fg-4)', fontWeight: 400 }}>{r.pct}%</span></span>
                  </div>
                  <div className="bar-track"><div className="bar-fill" style={{ width: `${r.pct}%` }} /></div>
                </li>
              ))}
            </ul>
          </div>

          <p style={{ fontSize: 11, color: 'var(--fg-4)', lineHeight: 1.6, margin: 0 }}>
            Olá, {user.name.split(' ')[0]}. Logado como <span style={{ textTransform: 'capitalize' }}>{user.role}</span>.
          </p>
        </aside>
      </section>

      {/* New: distribution chart card — full-width below the section-grid */}
      <section style={{ marginTop: 28 }} aria-label="Distribuição de associados">
        <DistributionChart />
      </section>
    </main>
  );
}

function formatDueDate(iso) {
  if (!iso) return '';
  const d = new Date(iso + 'T00:00:00');
  return d.toLocaleDateString('pt-BR', { day: 'numeric', month: 'short' }).replace('.', '');
}

Object.assign(window, { Dashboard, formatDueDate });
