---
name: ready-to
description: Analisa a codebase do estado atual até o deploy, identificando erros, bloqueios, documentação faltante e decisões de design pendentes. Produz um checklist estruturado em READY-TO.md via uma sessão interativa no estilo grill-me. Use quando o usuário disser "pronto pra deploy", "pronto pra produção", "ship it", "revisão pré-deploy", ou invocar /ready-to. Sempre em português brasileiro.
---

# ready-to

**Idioma: português brasileiro.** Todas as interações, perguntas, outputs e o arquivo READY-TO.md são escritos em pt-BR. Essa skill não opera em outros idiomas.

Diagnostica o que falta entre o estado atual da codebase e um estado deplorável. Funciona como uma sessão de grill-me — a skill te entrevista sobre cada dimensão, e escreve os achados incrementalmente em `READY-TO.md`.

## Fases

### Fase 1 — Varredura automática de saúde (dispara imediatamente ao ser invocada)

Dispara agents background em paralelo para coletar:

- `git status` — changes não commitadas, estado da branch, ahead/behind do remote
- `lsp_diagnostics` nos diretórios fonte — erros de tipo, imports quebrados
- Build check — `tsc --noEmit`, `next build`, ou equivalente
- Test check — `npm test` / `pnpm test` / equivalente (se scripts existirem)
- Auditoria de config — `tsconfig.json`, `package.json`, `Dockerfile`, presença de CI
- Env check — `.env.example` existe, documenta as vars obrigatórias

Apresenta um sumário dos achados antes de prosseguir.

### Fases 2 a 5 — Grill-me interativo (sob demanda)

Após a Fase 1, pergunte ao usuário em qual área ele quer mergulhar:

- **Infraestrutura** — Docker, CI/CD, config de hospedagem (Vercel, Fly, Render, etc.)
- **Arquitetura e decisões de local** — `CONTEXT.md`, ADRs, estrutura de diretórios, arquivos órfãos
- **Documentação** — README, API docs, changelog, instruções de setup
- **Dívida técnica e issues** — issues abertas, TODO/FIXME, deps desatualizadas, cobertura de testes

Para cada achado descoberto, a skill:

1. **Pergunta** uma questão específica (estilo grill-me), fornecendo contexto da varredura da codebase
2. **Registra** a decisão ou bloqueio em `READY-TO.md`
3. **Recomenda** qual skill existente invocar para resolver, quando aplicável (ex.: `/diagnose`, `/improve-codebase-architecture`, `/write-a-skill`)

## Output: READY-TO.md

Escrito na raiz do projeto, estruturado como:

```md
# Ready-to: Checklist de Deploy

## ✅ Verificações ok

- TypeScript compila sem erros
- Testes: 142/142 passando
- CI config presente (.github/workflows/ci.yml)

## ❌ Bloqueios

### B1 — Dockerfile ausente
- **Gravidade**: Alta
- **O quê**: Nenhum Dockerfile encontrado para build de produção
- **Recomendação**: Criar um Dockerfile multi-stage
- **Skill**: manual (ou `/write-a-skill` se tiver um template)

## ❓ Precisa de decisão

### D1 — Local do novo serviço de API
- **Contexto**: A PR #42 adiciona um serviço de billing — não está claro se vai em `services/` ou `modules/`
- **Recomendação**: Discutir com o time, então registrar ADR. Tente `/grill-with-docs`
```

## Gatilhos

- Comando: `/ready-to`
- Contextual: "pronto pra deploy", "pronto pra produção", "revisão pré-deploy", "ship it", "vai pra produção", "pre-deploy check"
