---
name: Gerador de Simulados
version: 1.1.0
description: Gera simulados personalizados para concursos públicos com base no edital fornecido, utilizando questões reais de provas anteriores da mesma banca examinadora.
tags:
  - concursos
  - simulados
  - questões
  - PDF
  - educação
---

# Gerador de Simulados para Concursos Públicos

## Visão Geral

Esta skill analisa editais de concursos públicos e gera simulados completos utilizando **exclusivamente questões reais** aplicadas pela mesma banca examinadora. O resultado final é um documento PDF pronto para impressão e prática.

---

## ⚠️ Passo Inicial Obrigatório

> [!IMPORTANT]
> **Antes de iniciar, solicite ao usuário que anexe o arquivo do edital do concurso.**
>
> Exemplo de pergunta inicial:
>
> ```text
> Para gerar o simulado, por favor anexe o arquivo do edital do concurso
> (pode ser PDF, Markdown ou texto). Se preferir, cole o conteúdo diretamente.
> ```

---

## Entradas Obrigatórias

| Entrada  | Descrição                               | Como Obter                     |
| -------- | --------------------------------------- | ------------------------------ |
| `edital` | Conteúdo integral do edital do concurso | **Solicitar anexo ao usuário** |

## Entradas Opcionais

| Entrada         | Descrição                                                        | Padrão             |
| --------------- | ---------------------------------------------------------------- | ------------------ |
| `banca`         | Nome da banca examinadora (se não estiver explícito no edital)   | Extraído do edital |
| `cargo`         | Cargo específico para filtrar questões                           | Todos relacionados |
| `anos_recentes` | Quantidade de anos para filtrar questões de conhecimentos gerais | 5                  |

---

## Fluxo de Execução

### 1. Solicitar o Edital

Inicie a interação solicitando que o usuário anexe ou forneça o edital:

```text
Olá! Vou gerar um simulado personalizado para seu concurso.

📎 Por favor, **anexe o arquivo do edital** (PDF, Markdown ou texto)
   ou cole o conteúdo diretamente aqui.

Após receber o edital, irei:
1. Analisar a estrutura da prova
2. Identificar a banca examinadora
3. Pesquisar questões reais da mesma banca
4. Montar o simulado no formato oficial
```

### 2. Análise do Edital

Após receber o edital, realize uma leitura completa e extraia:

- [ ] **Banca examinadora** responsável pelo concurso
- [ ] **Total de questões** da prova objetiva
- [ ] **Distribuição** entre conhecimentos gerais e específicos
- [ ] **Peso de cada área** (se aplicável)
- [ ] **Conteúdos programáticos** detalhados de cada matéria
- [ ] **Existência de questões dissertativas** e seu formato
- [ ] **Critérios de avaliação** e pontuação

### 3. Pesquisa de Questões

Busque questões reais seguindo estas regras **obrigatórias**:

#### Para Conhecimentos Gerais

- Utilize apenas questões dos **últimos {anos_recentes} anos**
- Priorize questões de concursos com **nível de escolaridade similar**

#### Para Conhecimentos Específicos

- Selecione provas aplicadas para cargos que abordem **exatamente** os conteúdos listados no edital
- Não há restrição de anos para questões específicas

#### Regras Gerais

> [!IMPORTANT]
>
> - **SOMENTE** questões da **MESMA BANCA EXAMINADORA**
> - **NUNCA** utilize questões de outras bancas
> - **MANTENHA** rigorosamente a proporção de questões definida no edital

### 4. Montagem do Simulado

Estruture o simulado com:

1. **Capa** com nome do concurso, cargo e banca
2. **Instruções** no mesmo formato da banca
3. **Questões objetivas** organizadas por disciplina
4. **Questões dissertativas** (se aplicável), seguindo o estilo da banca

#### Metadados de cada questão

Para cada questão incluída, informe:

- Concurso de origem
- Ano de aplicação
- Órgão contratante
- Número original da questão

### 5. Geração do Documento Final

Produza um arquivo **PDF** contendo:

- [ ] Simulado completo formatado
- [ ] Folha de respostas destacável
- [ ] **Gabarito oficial** ao final
- [ ] Lista de fontes utilizadas

#### Especificações do PDF

| Propriedade      | Valor                   |
| ---------------- | ----------------------- |
| Formato          | A4 (210 × 297 mm)       |
| Margens          | 25 mm em todos os lados |
| Fonte corpo      | Serif, 12pt             |
| Fonte títulos    | Sans-serif, 14-16pt     |
| Espaçamento      | 1.15 entrelinhas        |
| Numeração        | Rodapé, centralizado    |
| Idioma documento | pt-BR                   |

#### Requisitos de Acessibilidade

- [ ] PDF estruturado com tags semânticas (headings, listas, tabelas)
- [ ] Ordem de leitura lógica definida
- [ ] Metadados de idioma e título configurados
- [ ] Fontes legíveis embutidas no documento
- [ ] Contraste de cores adequado (WCAG 2.1 AA)
- [ ] Bookmarks/TOC para navegação
- [ ] Cabeçalhos de tabela marcados corretamente

---

## Formato de Saída

```text
📄 simulado_{concurso}_{cargo}.pdf
├── Capa
├── Instruções
├── Questões Objetivas (organizadas por disciplina)
├── Questões Dissertativas (se houver)
├── Folha de Respostas
├── Gabarito Oficial
└── Referências (concursos utilizados)
```

---

## Restrições

> [!CAUTION]
>
> - ❌ **NÃO** utilize questões de outras bancas
> - ❌ **NÃO** altere a estrutura da prova prevista no edital
> - ❌ **NÃO** crie questões fictícias ou adaptadas
> - ✅ **SOMENTE** questões reais da mesma banca

---

## Considerações Legais e de Privacidade

> [!WARNING]
> **Atenção aos aspectos legais e de proteção de dados:**
>
> **Direitos Autorais:**
>
> - Verifique o status de copyright das questões reutilizadas
> - Busque autorização quando necessário
> - Documente e credite todas as fontes utilizadas
>
> **Proteção de Dados (LGPD):**
>
> - Não armazene ou processe dados pessoais desnecessários dos editais
> - Implemente anonimização quando aplicável
> - Garanta conformidade com a Lei Geral de Proteção de Dados
>
> Mantenha registro/log de permissões e fontes para fins de auditoria.

---

## Tratamento de Erros

| Situação                                  | Ação                                                         |
| ----------------------------------------- | ------------------------------------------------------------ |
| Edital não anexado                        | Solicitar ao usuário que anexe o arquivo                     |
| Banca não identificada no edital          | Perguntar ao usuário                                         |
| Questões insuficientes da banca           | Informar e sugerir alternativas (ver Regras de Fallback)     |
| Formato de edital não reconhecido         | Pedir esclarecimentos                                        |
| Dúvidas sobre estrutura da prova          | Confirmar com o usuário antes de prosseguir                  |
| Falha na geração do PDF                   | Registrar erro, tentar novamente, informar fallback ao user  |
| Problemas de acesso ao banco de questões  | Retry com backoff, notificar usuário sobre indisponibilidade |
| Erros de rede durante pesquisa            | Retry/backoff, mostrar resultados parciais ou mensagem       |
| Memória insuficiente para editais grandes | Processar em chunks, sugerir arquivo menor                   |
| Timeout em operações longas               | Exibir progresso, oferecer job assíncrono                    |

---

## Exemplo de Uso

### Arquivo de Edital de Exemplo

O seguinte arquivo pode ser usado como referência para testes:

```text
./examples/edital_policial_legislativo.md
```

### Interação Esperada

O usuário anexa o edital acima.

#### Resposta da Skill

```markdown
## 📋 Análise do Edital - Policial Legislativo Federal

| Informação           | Detalhe                                                 |
| -------------------- | ------------------------------------------------------- |
| **Concurso**         | Câmara dos Deputados - Policial Legislativo Federal     |
| **Banca**            | Cebraspe                                                |
| **Prova Objetiva**   | 180 questões (90 conhecimentos gerais + 90 específicos) |
| **Prova Discursiva** | Sim (2 questões + 1 peça técnica)                       |
| **Data da Prova**    | 26/04/2026                                              |

### Estrutura do Simulado a ser gerado:

**Conhecimentos Gerais (90 questões)**

- Língua Portuguesa
- Raciocínio Lógico
- Noções de Informática
- Atualidades
- Ética no Serviço Público

**Conhecimentos Específicos (90 questões)**

- Direito Constitucional
- Direito Penal e Processual Penal
- Direito Administrativo
- Criminologia e Criminalística
- Atividade de Inteligência
- Legislação específica

Confirma a geração do simulado com questões do Cebraspe?
```

#### Saída Final

Simulado em PDF com questões reais do Cebraspe dos últimos 5 anos para conhecimentos gerais, e questões específicas para cargos de segurança pública de qualquer ano.

---

## Recursos da Skill

| Recurso                   | Caminho                                                                                | Descrição                                                                                   |
| ------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Guia de Análise de Edital | [`references/analise-edital.md`](./references/analise-edital.md)                       | Metodologia detalhada para extração de informações de editais, checklist e casos especiais  |
| Base de Bancas            | [`references/bancas-concursos.md`](./references/bancas-concursos.md)                   | Características de cada banca, URLs oficiais, estratégias de busca e mapeamento cargo→banca |
| Padrão de Discursivas     | [`references/provas-discursivas.md`](./references/provas-discursivas.md)               | Estrutura e formato de questões discursivas (dissertativas e peças técnicas)                |
| Template do Simulado      | [`assets/template_simulado.md`](./assets/template_simulado.md)                         | Estrutura padronizada do simulado em Markdown                                               |
| Gerador de PDF            | [`scripts/gerar_simulado_pdf.py`](./scripts/gerar_simulado_pdf.py)                     | Script Python para conversão Markdown→PDF formatado                                         |
| Exemplo de Edital         | [`examples/edital_policial_legislativo.md`](./examples/edital_policial_legislativo.md) | Edital de referência para testes                                                            |
| Exemplo de Discursivas    | [`examples/discursivas.pdf`](./examples/discursivas.pdf)                               | Prova discursiva real do CEBRASPE (TCE/MS 2025)                                             |

### Uso do Script de Geração de PDF

```bash
# Gerar PDF (requer weasyprint)
python scripts/gerar_simulado_pdf.py simulado.md simulado.pdf

# Gerar apenas HTML (fallback)
python scripts/gerar_simulado_pdf.py simulado.md saida.html --html
```

> [!TIP]
> Para instalar as dependências do script:
>
> ```bash
> pip install markdown weasyprint
> ```
