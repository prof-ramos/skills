# GERADOR DE SIMULADOS

> **Versão:** 1.0.0
> **Última atualização:** 2026-02-02

## Sobre Esta Skill

Esta skill é um **conjunto de instruções para assistentes de IA** (como Claude, GPT ou Gemini) gerarem simulados personalizados para concursos públicos. Ela analisa editais fornecidos pelo usuário e monta provas completas utilizando exclusivamente questões reais de provas anteriores da mesma banca examinadora.

### Objetivo

Analisar o edital fornecido e montar um simulado conforme especificações.

### Entrada Esperada

| Campo    | Tipo  | Obrigatório | Descrição                                                 |
| -------- | ----- | ----------- | --------------------------------------------------------- |
| `edital` | Texto | Sim         | Conteúdo integral do edital (ver formatos aceitos abaixo) |
| `banca`  | Texto | Não         | Se omitido, será extraído automaticamente do edital       |

#### Formatos de Edital Aceitos

- **Markdown** (.md) - Recomendado
- **Texto plano** (.txt)
- **PDF** - Requer extração prévia de texto
- **JSON** - Com campos `conteudo` ou `texto`

#### Validações

- **Tamanho máximo:** ~50 páginas (editais maiores devem ser divididos)
- **Codificação:** UTF-8
- **Campos obrigatórios:** Conteúdo programático, número de questões

---

## Instruções de Execução

Siga as etapas abaixo com precisão:

### 1. Estudo do Edital

Identifique e extraia as seguintes informações:

- Número total de questões previstas
- Distribuição entre conhecimentos gerais e específicos
- Conteúdos programáticos de ambas as partes
- Existência e formato de questões dissertativas
- Critérios de avaliação e pontuação

### 2. Pesquisa de Questões Reais

Utilize **apenas questões reais** aplicadas anteriormente pela **mesma banca examinadora**.

#### Regras de Seleção

| Tipo de Conhecimento | Critério de Tempo | Critério de Cargo                                      |
| -------------------- | ----------------- | ------------------------------------------------------ |
| **Gerais**           | Últimos 5 anos    | Mesmo nível de escolaridade                            |
| **Específicos**      | Sem restrição     | Arquitetos, engenheiros ou conteúdos exatamente iguais |

#### Regras de Fallback (Questões Insuficientes)

Quando os filtros estritos retornarem questões insuficientes, aplique relaxamento progressivo **nesta ordem de prioridade**:

1. **Prioridade máxima:** Manter a mesma banca examinadora
2. **Segunda prioridade:** Estender período de 5 para 10 anos (conhecimentos gerais)
3. **Terceira prioridade:** Permitir cargos correlatos (mesma área de atuação)
4. **Última opção:** Permitir tópicos adjacentes ao conteúdo programático

> [!WARNING]
> **Regras de Auditoria:**
>
> - Documente qualquer relaxamento aplicado
> - Informe ao usuário quais critérios foram flexibilizados
> - Se mesmo com todos os relaxamentos não houver questões suficientes, **aborte a geração** e notifique o usuário
> - Nunca utilize questões de outras bancas, mesmo como fallback

#### Proporção

Mantenha **rigorosamente a proporção de questões** definida no edital.

### 3. Montagem do Simulado

Estruture o simulado seguindo estas regras:

#### Organização

| Aspecto              | Regra                                                       |
| -------------------- | ----------------------------------------------------------- |
| **Ordenação padrão** | Conhecimentos gerais primeiro, depois específicos           |
| **Agrupamento**      | Por disciplina, na ordem do edital                          |
| **Embaralhamento**   | Questões embaralhadas dentro de cada disciplina (seed fixo) |
| **Quebra de página** | Nenhuma questão dividida entre páginas                      |

#### Estrutura do Simulado

1. **Capa:** Nome do concurso, cargo e banca
2. **Instruções:** Mesmo formato da banca
3. **Questões objetivas:** Organizadas por disciplina
4. **Questões dissertativas:** (se houver) Seguindo o estilo da banca

#### Metadados Obrigatórios por Questão

Para cada questão incluída, informe:

```text
[Ano] - [Órgão Contratante] - [Cargo Original]
Questão nº [número original]
```

### 4. Entrega

Monte o documento final em **PDF** seguindo estas especificações:

#### Layout do Documento

| Propriedade       | Valor                                  |
| ----------------- | -------------------------------------- |
| **Formato papel** | A4 (210 × 297 mm)                      |
| **Margens**       | 25 mm em todos os lados                |
| **Fonte corpo**   | Serif (ex: Times New Roman), 12pt      |
| **Fonte títulos** | Sans-serif (ex: Arial), 14-16pt        |
| **Espaçamento**   | 1.15 entrelinhas, 6pt entre parágrafos |
| **Numeração**     | Rodapé, centralizado                   |
| **Cabeçalho**     | Nome do concurso + "SIMULADO"          |

#### Estrutura Final

1. Capa
2. Instruções
3. Questões objetivas (organizadas por disciplina)
4. Questões dissertativas (se houver)
5. Folha de respostas (página nova)
6. **Gabarito oficial** (página nova, label: "GABARITO")
7. Referências (concursos utilizados)

#### Conformidade

- PDF/A recomendado para arquivamento
- Pronto para impressão frente e verso

---

## Considerações Legais

> [!CAUTION]
> **Direitos Autorais e Uso de Questões**
>
> - Verifique o status de copyright das questões antes de usá-las
> - Busque autorização quando necessário para reprodução
> - Documente e credite as fontes de todas as questões utilizadas
> - Este projeto não se responsabiliza por uso indevido de questões protegidas

> [!IMPORTANT]
> **Proteção de Dados (LGPD)**
>
> - Não armazene dados pessoais desnecessários extraídos dos editais
> - Implemente anonimização quando aplicável
> - Garanta conformidade com a LGPD no tratamento de dados

---

## Restrições

> [!CAUTION]
>
> - ❌ Utilize **apenas** questões da mesma banca examinadora
> - ❌ Não altere a estrutura da prova prevista no edital
> - ❌ Não crie questões fictícias ou adaptadas

Se surgir qualquer dúvida durante o processo, solicite esclarecimentos antes de prosseguir.

---

## Perguntas Frequentes (FAQ)

### Por que usar apenas questões da mesma banca?

Cada banca examinadora tem estilo próprio de elaboração de questões, nível de dificuldade característico e padrões de formatação. Usar questões da mesma banca garante uma simulação mais realista da prova.

### O que fazer se a banca for nova ou tiver poucas provas?

Aplique as regras de fallback: estenda o período de pesquisa, amplie para cargos correlatos, ou informe ao usuário sobre a limitação e pergunte se deseja prosseguir com menos questões.

### Posso usar questões de outras bancas como complemento?

**Não.** A restrição de usar apenas a mesma banca é absoluta. Se não houver questões suficientes mesmo após os fallbacks, aborte a geração e informe o usuário.

### Como garantir que o simulado tenha a mesma dificuldade da prova real?

Além de usar questões da mesma banca, priorize questões de concursos com mesmo nível de escolaridade e cargos semelhantes.

---

## Histórico de Alterações

| Versão | Data       | Alteração                                           |
| ------ | ---------- | --------------------------------------------------- |
| 1.0.0  | 2026-02-02 | Versão inicial com todas as instruções estruturadas |
