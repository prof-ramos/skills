# Contribuindo com Novas Skills

Guia para contribuir com novas skills para este repositório.

## Estrutura de uma Skill

Cada skill deve seguir a [especificação oficial](https://agentskills.io/specification):

```text
skill-name/
├── SKILL.md          # Obrigatório
├── scripts/          # Scripts auxiliares (opcional)
├── references/       # Documentação técnica (opcional)
└── assets/           # Templates e imagens (opcional)
```

## Formato do SKILL.md

### Frontmatter (Obrigatório)

```yaml
---
name: nome-da-skill          # Lowercase, hífens, 1-64 chars
description: >-              # O que faz e quando usar, 1-1024 chars
  Descrição detalhada da skill com keywords
  para ajudar agentes a identificar tarefas relevantes.
license: MIT                 # Opcional
compatibility: >-            # Opcional: requisitos de ambiente
  Designed for Claude Code. Requires Python 3.8+.
metadata:                    # Opcional
  author: seu-nome
  version: "1.0.0"
---
```

### Corpo (Markdown)

Instruções detalhadas para o agente executar a skill.

## Convenções de Nome

- ✅ `pdf-processing`
- ✅ `data-analysis`
- ❌ `PDF-Processing` (maiúsculas)
- ❌ `-pdf` (inicia com hífen)
- ❌ `pdf--processing` (hífens consecutivos)

## Categorias Disponíveis

Organize sua skill na categoria apropriada:

| Categoria | Caminho | Uso |
|-----------|---------|-----|
| Automação | `skills/automation/` | Scripts, integrações, bots |
| Conteúdo | `skills/content/` | Documentação, copywriting |
| Design | `skills/design/` | UI/UX, visual |

## Checklist de Validação

- [ ] `name` corresponde ao nome do diretório
- [ ] `description` tem 1-1024 caracteres
- [ ] Frontmatter segue formato YAML válido
- [ ] Scripts são auto-contidos ou documentam dependências
- [ ] Inclui instruções claras de uso

## Exemplo Mínimo

```yaml
---
name: minha-skill
description: Faz X quando usuário pede Y ou menciona Z.
---

# Minha Skill

Instruções para o agente...
```
