# Repositório de Habilidades Jurídicas - LegalSkillsBR

Este diretório contém o acervo integral das **2.149 habilidades** do ecossistema LegalSkillsBR, organizadas de maneira estruturada, padronizada e enriquecida com metadados em frontmatter YAML.

---

## 📊 Estatísticas Gerais

- **Total de Habilidades:** 2.149 arquivos `.md`
- **Tamanho Total em Disco:** ~16.8 MB
- **Média por Habilidade:** ~8.200 caracteres (mínimo 2.454 bytes, máximo 27.354 bytes)
- **Status de Integridade:** 100% íntegro (0 arquivos vazios, 0 arquivos faltantes)

### Divisão por Categoria

1. **Formas (`skills/forma/` - 299 itens):**
   - Estruturas completas para minutas de petições iniciais, recursos, contestações, pareceres, contratos, termos de acordo e decisões judiciais.
2. **Matérias (`skills/materia/` - 1.850 itens):**
   - Teses jurídicas, enquadramentos legais, súmulas vinculantes, temas de repercussão geral (STF), recursos repetitivos (STJ) e jurisprudência consolidada, subdivididos em **25 ramos jurídicos**.

---

## 📁 Estrutura de Diretórios

A estrutura espelha a taxonomia canônica do repositório oficial:

```text
skills/
├── README.md
├── forma/                                     # 299 minutas e peças processuais
│   ├── acao-anulatoria-debito-fiscal.md
│   ├── apelacao-civel.md
│   ├── contestacao-civel.md
│   ├── habeas-corpus.md
│   ├── peticao-inicial-civel.md
│   └── ...
└── materia/                                   # 1.850 teses de mérito por área
    ├── administrativo/                        # 213 teses
    │   ├── acoes-coletivas-controle-social/
    │   ├── concursos-publicos/
    │   ├── improbidade/
    │   ├── licitacoes-contratos/
    │   └── ...
    ├── ambiental/                             # 32 teses
    ├── bancario/                              # 47 teses
    ├── civil/                                 # 66 teses
    ├── constitucional/                        # 60 teses
    ├── consultoria/                           # 59 teses
    ├── consumidor/                            # 106 teses
    ├── contratos/                             # 59 teses
    ├── digital-dados/                         # 27 teses
    ├── diversidade-dh/                        # 26 teses
    ├── eleitoral/                             # 27 teses
    ├── empresarial/                           # 43 teses
    ├── familia-sucessoes/                     # 39 teses
    ├── imobiliario/                           # 47 teses
    ├── internacional/                         # 18 teses
    ├── militar/                               # 5 teses
    ├── penal/                                 # 166 teses
    │   ├── parte-geral/
    │   └── parte-especial/
    ├── previdenciario/                        # 74 teses
    ├── processo-civil/                        # 165 teses
    ├── processo-penal/                        # 120 teses
    ├── regulatorio/                           # 14 teses
    ├── saude/                                 # 37 teses
    ├── societario/                            # 26 teses
    ├── trabalho/                              # 128 teses
    └── tributario/                            # 246 teses
```

> **Nota Taxonômica:** A disposição das pastas segue estritamente os caminhos oficiais `sourcePath` da plataforma. Na taxonomia original, a tese `coisa-julgada-fiscalizacao-tema-339-sv4` possui a tag `materia: "administrativo"`, mas seu caminho canônico de arquivo é `materia/processo-civil/coisa-julgada-fiscalizacao-tema-339-sv4.md`. Ambos os dados são preservados com total fidelidade (metadado no frontmatter e caminho físico no disco).

---

## 📄 Estrutura de Cada Arquivo `.md`

Cada arquivo é composto por duas partes:
1. **Frontmatter YAML padronizado**: Metadados indexáveis (UUID, nome, título, categoria, matéria, triggers de ativação semântica e descrição resumida).
2. **Corpo Markdown**: Conteúdo completo da habilidade (tabelas conceituais, artigos de lei, teses jurisprudenciais, checklists e modelos).

### Exemplo de Cabeçalho:
```yaml
---
id: "9857a06c-7ccc-42cc-a2a2-aeb8c9dff2a0"
name: "abandono-funcao-cp-323"
title: "Abandono de Função (CP 323) + Tipos Funcionais Próximos"
category: "materia"
materia: "penal"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/penal/parte-especial/abandono-funcao-cp-323.md"
triggers:
  - "CP 323"
  - "abandono função"
  - "art. 323"
description: "Crime de abandono de função pública (CP, art. 323)..."
---

# Abandono de Função e Tipos Funcionais Próximos
...
```

---

## 🔍 Como Consultar e Usar

### 0. Instalação via Skills CLI (`skills.sh`)

O acervo LegalSkillsBR pode ser explorado e instalado diretamente no Claude Code, Cursor, OpenCode ou outros agentes compatíveis:

```bash
# Listar todas as 2.149 habilidades jurídicas via subpath
npx skills add prof-ramos/skills/legalbr --list

# Instalar habilidade jurídica específica via subpath
npx skills add prof-ramos/skills/legalbr@acao-alimentos -a claude-code -y

# Instalar navegando toda a árvore do repositório via flag --full-depth
npx skills add prof-ramos/skills@acao-alimentos --full-depth -a claude-code -y

# Listar por matéria jurídica específica (ex: Tributário, 246 skills)
npx skills add prof-ramos/skills/legalbr/materia/tributario --list
```

### 1. Busca por Texto ou Tese (ripgrep)
```bash
# Buscar teses sobre ICMS-ST
rg -i "icms-st" skills/materia/tributario/

# Buscar modelos de Agravo de Instrumento
rg -i "efeito suspensivo" skills/forma/
```

### 2. Busca Programática (Python)
```python
import json

# Usando o arquivo consolidado de consulta rápida
with open("habilidades_conteudo_completo.json") as f:
    skills = json.load(f)

# Filtrar habilidades com determinado gatilho
matches = [s for s in skills if any("dano moral" in t.lower() for t in s.get("triggers", []))]
print(f"Encontradas {len(matches)} habilidades sobre dano moral.")
```

### 3. Integração com Agentes e LLMs
Os arquivos `.md` podem ser lidos diretamente por ferramentas de retrieval (RAG), injetados em prompts de sistema de agentes jurídicos ou consultados sob demanda pelo Claude Code, Cursor Composer, OpenCode ou LangChain.

---

## 🛠️ Scripts Auxiliares no Projeto

- `download_skills.py`: Script autônomo com concorrência, retries exponenciais e validação automática.
- `verify_download.py`: Suite de testes de integridade que checa arquivos ausentes, tamanhos, sintaxe frontmatter e consistência de dados.
- `generate_index.py`: Gerador dos índices consolidados (`INDICE_HABILIDADES.md`, `indice_habilidades.csv`, `indice_habilidades.json`).
