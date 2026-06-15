// Small primitives shared across the kit: Icon (Lucide wrapper), Eyebrow,
// PageHeader, Button, Card, KpiCard, StatusDot, PriorityLabel, Badge.

const { useEffect, useRef } = React;

function Icon({ name, size = 20, color = 'currentColor', strokeWidth = 2, style }) {
  // Lucide rewrites <i data-lucide> into <svg> on every createIcons() pass.
  // We keep a ref so we only rebuild this single element, not the whole tree.
  const ref = useRef(null);
  useEffect(() => {
    if (!ref.current || !window.lucide) return;
    // Reset back to <i data-lucide=…> if React re-rendered (lucide replaces the node).
    ref.current.innerHTML = '';
    const i = document.createElement('i');
    i.setAttribute('data-lucide', name);
    i.style.width = size + 'px';
    i.style.height = size + 'px';
    i.style.display = 'inline-flex';
    ref.current.appendChild(i);
    window.lucide.createIcons({ attrs: { width: size, height: size, 'stroke-width': strokeWidth, color }, icons: undefined, root: ref.current });
  }, [name, size, color, strokeWidth]);
  return <span ref={ref} style={{ display: 'inline-flex', width: size, height: size, color, ...style }} aria-hidden="true" />;
}

function PageHeader({ eyebrow, title, actions }) {
  return (
    <div className="page-head">
      <div>
        <div className="eyebrow">{eyebrow}</div>
        <h1>{title}</h1>
      </div>
      {actions && <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>{actions}</div>}
    </div>
  );
}

function Button({ variant = 'primary', icon, children, onClick, ariaLabel }) {
  const cls = variant === 'outline' ? 'btn btn-outline' : 'btn btn-primary';
  return (
    <button className={cls} onClick={onClick} aria-label={ariaLabel}>
      {icon && <Icon name={icon} size={16} />}
      {children}
    </button>
  );
}

function IconButton({ name, onClick, ariaLabel, variant = 'outline' }) {
  const cls = variant === 'outline' ? 'btn btn-outline btn-icon' : 'btn btn-primary btn-icon';
  return (
    <button className={cls} onClick={onClick} aria-label={ariaLabel}>
      <Icon name={name} size={18} />
    </button>
  );
}

function KpiCard({ item }) {
  if (item.segments) {
    return (
      <div className="kpi">
        <div className="kpi-split">
          {item.segments.map((seg) => (
            <div key={seg.id} className="kpi-seg" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div className="label">{seg.label}</div>
              <div className="metric">{seg.value}</div>
            </div>
          ))}
        </div>
      </div>
    );
  }
  return (
    <div className="kpi">
      <div className="label">{item.label}</div>
      <div className="metric">{item.value}</div>
    </div>
  );
}

function StatusDot({ color }) {
  return <span className="dot" style={{ background: color }} />;
}

function PriorityLabel({ priority }) {
  const p = window.PRIORITY_STYLES[priority] || window.PRIORITY_STYLES.normal;
  return <span className="priority-label" style={{ color: p.color }}>{p.label}</span>;
}

function Badge({ kind = 'neutral', children }) {
  const cls = `badge badge-${kind}`;
  return <span className={cls}>{children}</span>;
}

function Avatar({ initials }) {
  return <div className="avatar" aria-hidden="true">{initials}</div>;
}

Object.assign(window, { Icon, PageHeader, Button, IconButton, KpiCard, StatusDot, PriorityLabel, Badge, Avatar });
