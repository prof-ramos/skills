// Aggregated distribution data for the dashboard chart.
// Numbers add up to ~1.694 (1.284 ativos + outros) — coherent with the
// KPI strip on the painel administrativo.

const LOTACAO_DISTRIBUTION = [
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

const SITUACAO_DISTRIBUTION = [
  { situacao: 'Ativo',      key: 'ativo',      total: 1284, color: '#15803d', soft: '#86efac' },
  { situacao: 'Aposentado', key: 'aposentado', total: 342,  color: '#475569', soft: '#cbd5e1' },
  { situacao: 'Em licença', key: 'em_licenca', total: 42,   color: '#a16207', soft: '#f4ddb1' },
  { situacao: 'Cedido',     key: 'cedido',     total: 28,   color: '#1d4ed8', soft: '#bfdbfe' },
];

Object.assign(window, { LOTACAO_DISTRIBUTION, SITUACAO_DISTRIBUTION });
