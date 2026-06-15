// Atividades — full kanban board with 4 columns and click-to-cycle status.

function Atividades({ user }) {
  const [cols, setCols] = React.useState(window.STATUS_COLUMNS);

  function cycleCard(cardId, fromStatus) {
    const order = ['a_fazer', 'em_andamento', 'aguardando_terceiros', 'concluido'];
    const next = order[(order.indexOf(fromStatus) + 1) % order.length];
    setCols((curr) => {
      const fromCol = curr.find((c) => c.status === fromStatus);
      const card = fromCol.cards.find((c) => c.id === cardId);
      return curr.map((c) => {
        if (c.status === fromStatus) return { ...c, cards: c.cards.filter((x) => x.id !== cardId), total: c.total - 1 };
        if (c.status === next)       return { ...c, cards: [...c.cards, card], total: c.total + 1 };
        return c;
      });
    });
  }

  function addCard(toStatus) {
    const title = prompt('Título da nova atividade');
    if (!title) return;
    const id = Date.now();
    setCols((curr) => curr.map((c) => c.status === toStatus ? {
      ...c,
      cards: [...c.cards, { id, title, priority: 'normal', dueDate: null, associateLabel: 'Sem associado' }],
      total: c.total + 1,
    } : c));
  }

  return (
    <main className="page">
      <PageHeader
        eyebrow="Operação · Quadro de atividades"
        title="Atividades"
        actions={<Button variant="primary" icon="plus">Nova atividade</Button>}
      />

      <div className="kanban">
        {cols.map((col) => (
          <article key={col.status} className="kanban-col">
            <header>
              <StatusDot color={col.accent} />
              <span className="title">{col.label}</span>
              <span className="count">{col.cards.length}</span>
            </header>
            <div style={{ flex: 1, minHeight: 60 }}>
              {col.cards.length === 0 && (
                <div style={{ padding: 12, border: '1px dashed var(--border-subtle)', borderRadius: 'var(--r-md)', background: '#fff', color: 'var(--fg-4)', fontSize: 12, textAlign: 'center' }}>
                  Sem cards
                </div>
              )}
              {col.cards.map((card) => (
                <div
                  key={card.id}
                  className="kanban-card"
                  onClick={() => cycleCard(card.id, col.status)}
                  title="Clique para avançar o status"
                >
                  <p className="title">{card.title}</p>
                  <div className="meta">
                    <PriorityLabel priority={card.priority} />
                    {card.dueDate && <span className="due-text">· vence {formatDueDate(card.dueDate)}</span>}
                  </div>
                  <span className="associate-chip">{card.associateLabel || 'Sem associado'}</span>
                </div>
              ))}
            </div>
            {col.status !== 'concluido' && (
              <button className="quick-add" onClick={() => addCard(col.status)}>+ Adicionar atividade</button>
            )}
          </article>
        ))}
      </div>

      <p style={{ marginTop: 20, fontSize: 12, color: 'var(--fg-4)', display: 'inline-flex', alignItems: 'center', gap: 8 }}>
        <Icon name="clock" size={14} />
        Alterações no quadro são salvas imediatamente e entram no histórico da atividade.
        <Icon name="arrow-right" size={14} />
      </p>
    </main>
  );
}

Object.assign(window, { Atividades });
