// Seed data for the ASOF Intranet UI kit.
// All examples in Brazilian Portuguese to match the production register.

const TODAY_LABEL = (() => {
  const d = new Date();
  const fmt = new Intl.DateTimeFormat('pt-BR', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
  });
  const s = fmt.format(d);
  return s.charAt(0).toUpperCase() + s.slice(1);
})();

const CURRENT_USER = {
  name: 'Helena Vasconcelos',
  role: 'diretoria',
  initials: 'HV',
};

const KPI_STRIPE = [
  { id: 'ativos', label: 'Associados ativos', value: '1.284' },
  { id: 'pendentes', label: 'Pendentes migração', value: '37' },
  {
    id: 'atividades',
    segments: [
      { id: 'aberto', label: 'Atividades em aberto', value: '47' },
      { id: 'atraso', label: 'Em atraso', value: '6' },
    ],
  },
  { id: 'contrib', label: 'Adimplência', value: '92%' },
  { id: 'consultas', label: 'Consultas jurídicas', value: '12' },
];

const STATUS_COLUMNS = [
  {
    status: 'a_fazer', label: 'A fazer', accent: '#94a3b8', total: 4,
    cards: [
      { id: 1, title: 'Conferir vagas para o Posto em Tóquio', priority: 'normal', dueDate: '2026-05-26', associateLabel: 'Sem associado' },
      { id: 2, title: 'Atualizar lotações pós-remoções', priority: 'alta', dueDate: '2026-05-23', associateLabel: 'Sem associado' },
    ],
  },
  {
    status: 'em_andamento', label: 'Em andamento', accent: '#76aeea', total: 3,
    cards: [
      { id: 3, title: 'Revisar parecer 014/2026', priority: 'alta', dueDate: '2026-05-22', associateLabel: 'Maria L. Carvalho' },
      { id: 4, title: 'Editar ofício à SERE — DAJ', priority: 'normal', dueDate: '2026-05-25', associateLabel: 'João P. Andrade' },
    ],
  },
  {
    status: 'aguardando_terceiros', label: 'Aguardando terceiros', accent: '#e7c16b', total: 2,
    cards: [
      { id: 5, title: 'Resposta da Embaixada em Lisboa', priority: 'urgente', dueDate: '2026-05-15', associateLabel: 'João P. Andrade' },
    ],
  },
  {
    status: 'concluido', label: 'Concluído', accent: '#86efac', total: 24,
    cards: [
      { id: 6, title: 'Inicialização das mensalidades · maio/2026', priority: 'normal', dueDate: '2026-05-10', associateLabel: 'Diretoria' },
    ],
  },
];

const URGENT_ACTIVITIES = [
  { id: 5, title: 'Resposta da Embaixada em Lisboa', priority: 'urgente', dueDate: '2026-05-15' },
  { id: 11, title: 'Renovação de credenciais consulares · Madrid', priority: 'alta', dueDate: '2026-05-18' },
];

const TOP_REGIONS = [
  { country: 'Brasília — SERE', total: 412, pct: 32 },
  { country: 'Estados Unidos', total: 168, pct: 13 },
  { country: 'França', total: 121, pct: 9 },
  { country: 'Portugal', total: 98, pct: 8 },
  { country: 'Argentina', total: 84, pct: 7 },
];

const ASSOCIATES = [
  { id: 1, name: 'Ana C. Pereira',       assignment: 'Embaixada em Paris',      classPattern: 'Classe B · Padrão 3', email: 'ana.pereira@itamaraty.gov.br', status: 'ativo' },
  { id: 2, name: 'Bruno R. Almeida',     assignment: 'SERE — Brasília',          classPattern: 'Classe A · Padrão 5', email: 'bruno.almeida@itamaraty.gov.br', status: 'ativo' },
  { id: 3, name: 'Cláudia M. Souza',     assignment: 'Consulado em Boston',     classPattern: 'Classe Especial',      email: 'claudia.souza@itamaraty.gov.br', status: 'aposentado' },
  { id: 4, name: 'Diego L. Ferreira',    assignment: 'Embaixada em Tóquio',     classPattern: 'Classe B · Padrão 2', email: 'diego.ferreira@itamaraty.gov.br', status: 'ativo' },
  { id: 5, name: 'Eduarda S. Bianchi',   assignment: 'Embaixada em Berlim',     classPattern: 'Classe C · Padrão 1', email: 'eduarda.bianchi@itamaraty.gov.br', status: 'em_licenca' },
  { id: 6, name: 'Felipe A. Castro',     assignment: 'Consulado em Buenos Aires', classPattern: 'Classe B · Padrão 4', email: 'felipe.castro@itamaraty.gov.br', status: 'ativo' },
  { id: 7, name: 'Gabriela O. Tavares',  assignment: 'SERE — Brasília',          classPattern: 'Classe A · Padrão 3', email: 'gabriela.tavares@itamaraty.gov.br', status: 'ativo' },
  { id: 8, name: 'Heitor M. Lima',       assignment: 'Embaixada em Pretória',   classPattern: 'Classe B · Padrão 5', email: 'heitor.lima@itamaraty.gov.br', status: 'cedido' },
];

const STATUS_LABEL = {
  ativo:        { label: 'Ativo',        badge: 'badge-success' },
  aposentado:   { label: 'Aposentado',   badge: 'badge-neutral' },
  em_licenca:   { label: 'Em licença',   badge: 'badge-warning' },
  cedido:       { label: 'Cedido',       badge: 'badge-neutral' },
};

const PRIORITY_STYLES = {
  baixa:   { label: 'Baixa',   color: 'rgba(13,31,60,0.50)' },
  normal:  { label: 'Normal',  color: 'rgba(13,31,60,0.70)' },
  alta:    { label: 'Alta',    color: '#a16207' },
  urgente: { label: 'Urgente', color: '#b91c1c' },
};

Object.assign(window, {
  TODAY_LABEL, CURRENT_USER, KPI_STRIPE, STATUS_COLUMNS, URGENT_ACTIVITIES,
  TOP_REGIONS, ASSOCIATES, STATUS_LABEL, PRIORITY_STYLES,
});
