// Sidebar — institutional navy rail with active sky-blue indicator.

function SidebarItem({ icon, label, active, badge, onClick }) {
  return (
    <a className={`sb-item ${active ? 'active' : ''}`} onClick={onClick}>
      <span className="ico"><Icon name={icon} size={20} /></span>
      <span style={{ flex: 1, minWidth: 0 }}>{label}</span>
      {badge != null && (
        <span style={{ marginLeft: 'auto', background: 'rgba(255,255,255,0.10)', color: '#fff', fontSize: 11, fontWeight: 700, letterSpacing: '0.06em', textTransform: 'uppercase', padding: '2px 8px', borderRadius: 9999 }}>
          {badge}
        </span>
      )}
    </a>
  );
}

function Sidebar({ route, setRoute, user, onLogout }) {
  const items = [
    { key: 'dashboard',   icon: 'layout-dashboard', label: 'Dashboard' },
    { key: 'associados',  icon: 'users',            label: 'Associados' },
    { key: 'atividades',  icon: 'kanban',           label: 'Atividades', badge: 6 },
    { key: 'juridico',    icon: 'scale',            label: 'Jurídico' },
    { key: 'oficios',     icon: 'file-spreadsheet', label: 'Secretaria' },
    { key: 'financeiro',  icon: 'dollar-sign',      label: 'Financeiro' },
    { key: 'config',      icon: 'settings',         label: 'Configurações' },
  ];
  return (
    <aside className="sidebar">
      <div className="logo-cap">
        <img src="../../assets/asof-logo-lockup.svg" alt="ASOF — Associação Nacional dos Oficiais de Chancelaria do Serviço Exterior Brasileiro" />
        <span className="tag">Intranet</span>
      </div>
      <nav aria-label="Navegação principal">
        {items.map((it) => (
          <SidebarItem
            key={it.key}
            icon={it.icon}
            label={it.label}
            badge={it.badge}
            active={route === it.key}
            onClick={() => setRoute(it.key)}
          />
        ))}
      </nav>
      <div className="sb-foot">
        <div className="name">{user.name}</div>
        <div className="role">{user.role}</div>
        <button className="logout-btn" onClick={onLogout}>
          <Icon name="log-out" size={14} />
          Sair
        </button>
      </div>
    </aside>
  );
}

Object.assign(window, { Sidebar });
