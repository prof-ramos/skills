// App root — login → app shell with sidebar routing.

const { useState, useEffect } = React;

function App() {
  const [authed, setAuthed] = React.useState(true); // start logged in for the kit demo
  const [route, setRoute]   = React.useState('dashboard');

  if (!authed) return <Login onSubmit={() => setAuthed(true)} />;

  let page;
  switch (route) {
    case 'associados':  page = <Associados user={window.CURRENT_USER} />; break;
    case 'atividades':  page = <Atividades user={window.CURRENT_USER} />; break;
    case 'juridico':
    case 'oficios':
    case 'financeiro':
    case 'config':
      page = <PlaceholderPage route={route} />; break;
    default:
      page = <Dashboard user={window.CURRENT_USER} />;
  }

  return (
    <div className="app">
      <Sidebar
        route={route}
        setRoute={setRoute}
        user={window.CURRENT_USER}
        onLogout={() => setAuthed(false)}
      />
      <div className="main">{page}</div>
    </div>
  );
}

const ROUTE_LABEL = {
  juridico:   { eyebrow: 'Operação · Assessoria jurídica', title: 'Jurídico' },
  oficios:    { eyebrow: 'Secretaria · Padrão Ofício',     title: 'Ofícios' },
  financeiro: { eyebrow: 'Operação · Contribuições',       title: 'Financeiro' },
  config:     { eyebrow: 'Sistema · Administração',        title: 'Configurações' },
};

function PlaceholderPage({ route }) {
  const meta = ROUTE_LABEL[route] || { eyebrow: 'Operação', title: route };
  return (
    <main className="page">
      <PageHeader eyebrow={meta.eyebrow} title={meta.title} />
      <div className="card" style={{ textAlign: 'center', padding: 48, color: 'var(--fg-3)', background: 'var(--surface-container-low)', border: '1px dashed var(--border-subtle)' }}>
        <Icon name="construction" size={28} color="var(--fg-4)" />
        <p style={{ margin: '12px 0 4px', fontSize: 14, fontWeight: 600, color: 'var(--on-surface)' }}>Tela em construção</p>
        <p style={{ margin: 0, fontSize: 13, color: 'var(--fg-3)' }}>
          Esta tela existe na intranet em produção, mas não é recriada neste UI kit.
        </p>
      </div>
    </main>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
