# 01 — Inventário de fontes e trilha de evidências

**Classificações:** D = reutilizável diretamente; A = reutilizável com adaptação; C = referência conceitual; API = dependente de API (não executar neste projeto); X = incompatível/desatualizado. Uma fonte pode ter parcelas classificadas de formas diferentes.

| Fonte | Evidência observável ou objetivo de inspeção | Aproveitamento | Teste previsto |
|---|---|---|---|
| [openai/skills](https://github.com/openai/skills) | Repositório de skills; diretórios `skills/.system` e `skills/.curated` | D/A | Checar estrutura e frontmatter da skill proposta |
| [Hatch Pet — SKILL.md](https://github.com/openai/skills/blob/main/skills/.curated/hatch-pet/SKILL.md) | Declara composição de `$imagegen` e scripts de montagem/QA determinísticos | A | Invocar geração delegada e validar artefato com script independente |
| [Skill Creator — SKILL.md](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md) | Convenções de skill, metadados, descrição e organização de recursos | D | Rodar validação de estrutura e descoberta no Codex |
| [ImageGen — skills oficiais](https://github.com/openai/skills) | Fluxo oficial de geração/edição; verificar localização exata e versão instalada | D (built-in); API (fallback) | Confirmar composição e evitar qualquer `OPENAI_API_KEY` |
| [openai/codex](https://github.com/openai/codex) | Código de referência de execução, skills, ferramentas e permissões | C/A | Confrontar versão 0.163.0 com comandos/recursos efetivamente disponíveis |
| [openai/openai-cookbook](https://github.com/openai/openai-cookbook) | Exemplos de workflows e critérios de avaliação multimodal | C; API no código de execução | Extrair rubrica sem chamar endpoints pagos |
| [Cookbook — Image Evals](https://developers.openai.com/cookbook/examples/multimodal/image_evals) | Geração: precisão e legibilidade de texto, composição, marca; edição: localidade, preservação, controle espacial | C; API para códigos de exemplo | Pontuar amostras visuais; documentar parecer e evidência |
| [OpenAI Academy — Creating images with ChatGPT](https://openai.com/academy/image-generation/) | Prompts claros, restrições explícitas e identificação de imagens de referência | C | Comparar prompt livre versus briefing com restrições |
| [OpenAI Developer Community](https://community.openai.com/) | Casos relatados por usuários, não necessariamente orientação oficial | C (baixa autoridade) | Reproduzir falhas relatadas antes de incorporá-las |
| [Agent Skills Specification](https://agentskills.io/specification) | Especificação transversal de empacotamento de skills | D/A | Validar frontmatter e recursos no sistema existente |
| [Context7 /openai/codex](https://github.com/openai/codex) | Índice auxiliar indicado na pesquisa anterior (sem versão garantida) | C | Confirmar qualquer detalhe no repositório original e Codex instalado |

## Registro por evidência

### Hatch Pet
- Fonte primária: [SKILL.md do Hatch Pet](https://github.com/openai/skills/blob/main/skills/.curated/hatch-pet/SKILL.md).
- Evidência: descrição do próprio arquivo menciona `$imagegen` e scripts determinísticos para spritesheets. O fluxo de jobs JSON pode inspirar uma etapa futura, **mas não é necessário para o MVP**.
- Adaptação: em vez de spritesheets, validar e entregar PNG/JPEG/WebP para peças de comunicação, preservando referência ao prompt e brand kit.

### Skill Creator
- Fonte primária: [SKILL.md do Skill Creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md).
- Evidência: convenções de estrutura, concisão e descoberta de skills.
- Aplicação: `SKILL.md` pequeno com frontmatter `name`/`description` e instruções que delegam à skill oficial, mantendo avaliações/referências em arquivos anexos.

### Image Evals
- Fonte: [Cookbook](https://developers.openai.com/cookbook/examples/multimodal/image_evals).
- Evidência: critérios conceituais de geração e edição podem ser usados sem API.
- **Restrição:** não afirmar equivalência entre avaliações manuais e benchmarks automatizados do Cookbook.

### Academy
- Fonte: [Creating images with ChatGPT](https://openai.com/academy/image-generation/).
- Evidência: orientar referências de imagem por papel e distinguir explicitamente o que mudar e preservar.

## Itens não verificados ou ainda pendentes

- Mapeamento exaustivo dos repositórios públicos da organização `openai` e pesquisa de código por todos os termos do briefing.
- SHA exato das versões citadas, divergências da skill oficial `imagegen` e da versão instalada no Mac.
- Comportamento de `image_gen` no modo `codex exec` do ambiente real com todas as restrições de sandbox.
- Compatibilidade de delegação a subagentes ou de execução paralela de chamadas integradas no Codex instalado.
- Eficácia quantitativa de qualquer rubrica visual — precisa de corpus e avaliações repetidas.

**Regra de evidência:** os links em `main` apontam para conteúdo variável; antes de incorporar código, registrar commit SHA, licença, versão, caso de teste e resultado.
