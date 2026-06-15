// Associados — sticky search + table with navy header and pill statuses.

const { useState } = React;

function Associados({ user }) {
  const [q, setQ] = React.useState('');
  const rows = window.ASSOCIATES.filter((a) => a.name.toLowerCase().includes(q.toLowerCase()));
  const total = window.ASSOCIATES.length;
  const eyebrow = `Quadro associativo · ${window.TODAY_LABEL}`;

  return (
    <div>
      <div className="sticky-bar">
        <div className="inner">
          <label className="search">
            <Icon name="search" size={18} color="var(--fg-4)" />
            <input
              type="search"
              placeholder="Buscar por nome..."
              value={q}
              onChange={(e) => setQ(e.target.value)}
              aria-label="Buscar associado por nome"
            />
          </label>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <Avatar initials={user.initials} />
            <div style={{ lineHeight: 1.2 }}>
              <div style={{ fontSize: 13, fontWeight: 600 }}>{user.name}</div>
              <div style={{ fontSize: 11, color: 'var(--fg-4)', textTransform: 'capitalize' }}>{user.role}</div>
            </div>
          </div>
        </div>
      </div>

      <main className="page">
        <PageHeader eyebrow={eyebrow} title="Associados" />

        <section className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <div className="toolbar">
            <p className="muted">{rows.length === 0 ? 'Nenhum resultado' : `1–${rows.length} de ${total}`}</p>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <a className="link-action" href="#" style={{ color: 'var(--on-surface)' }}>Ver todos ({total})</a>
              <IconButton name="download" ariaLabel="Exportar para CSV" />
              <nav className="pager" aria-label="Paginação">
                <button className="pager-btn" disabled aria-label="Página anterior"><Icon name="chevron-left" size={16} /></button>
                <span className="pager-page">1/1</span>
                <button className="pager-btn" disabled aria-label="Próxima página"><Icon name="chevron-right" size={16} /></button>
              </nav>
            </div>
          </div>

          <div style={{ overflowX: 'auto', borderTop: '1px solid var(--border-hairline)' }}>
            <table className="table" aria-label="Lista de associados">
              <thead>
                <tr>
                  <th>Nome</th><th>Lotação</th><th>Padrão</th><th>Email</th><th>Situação</th><th aria-label="Ações" style={{ width: 56 }}></th>
                </tr>
              </thead>
              <tbody>
                {rows.length === 0 ? (
                  <tr><td colSpan={6} style={{ textAlign: 'center', padding: '48px 0', color: 'var(--fg-4)' }}>Nenhum associado encontrado.</td></tr>
                ) : rows.map((row) => {
                  const st = window.STATUS_LABEL[row.status];
                  return (
                    <tr key={row.id}>
                      <td><strong>{row.name}</strong></td>
                      <td>{row.assignment}</td>
                      <td>{row.classPattern}</td>
                      <td style={{ color: 'var(--fg-3)' }}>{row.email}</td>
                      <td><Badge kind={st.badge.replace('badge-', '')}>{st.label}</Badge></td>
                      <td style={{ textAlign: 'right' }}>
                        <button className="row-edit" aria-label={`Editar ${row.name}`}><Icon name="pencil" size={14} /></button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  );
}

Object.assign(window, { Associados });
