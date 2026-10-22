# 03 — Arquitetura proposta para `image-production`

## Visão geral

```text
Solicitação do usuário
  └─ Codex CLI (autenticado no ChatGPT)
      └─ skill image-production [briefing/seleção de marca/regras]
          ├─ referências locais do projeto + brand kit autorizado
          ├─ skill oficial $imagegen
          │   └─ ferramenta integrada image_gen [sem API externa/chaves]
          ├─ inspeção visual [correção direcionada, quando necessária]
          ├─ verificações locais determinísticas [arquivo, dimensões, alfa]
          └─ assets finais versionados + registro de prompt e QA
```

### Responsabilidades

- **Codex:** planejar tarefa, carregar skill, chamar ferramenta integrada quando disponível, coordenar revisão e arquivo.
- **image-production:** converter pedido em briefing visual, selecionar referências autorizadas, impor requisitos de preservação, orientar avaliação e entrega.
- **$imagegen:** geração e edição; não recriar código de geração.
- **Scripts locais:** somente validações determinísticas e pequenos ajustes de arquivo; não gerar por OpenAI API.
- **Brand kit:** referências por projeto, não globais. Logo deve ser tratado como artefato a preservar, não como pedido para recriar marca textualmente.
- **Agentes externos:** opcionais e somente após testes de isolamento, disponibilidade e segurança; no MVP, não são dependência.

### Modelo mínimo de entrada

```yaml
task: generate # ou edit
purpose: "Post institucional"
destination: "assets/images/"
size_or_ratio: "1080x1350"
exact_text: "Texto literal autorizado"
brand_kit: "./brand/README.md"
references:
  - path: "./brand/logo.png"
    role: "asset-to-preserve"
must_preserve: ["logotipo", "nomes e dados oficiais"]
avoid: ["logos inventados", "informação inexistente"]
```

Isto é um **exemplo ilustrativo**, não um formato obrigatório nem prova de que a ferramenta integrada aceite esses campos. A skill traduz o briefing para o prompt e os anexos suportados pelo contexto.

### Etapas lógicas

1. Interpretar solicitação e identificar formato, uso final e limites.
2. Carregar brand kit **apenas** se o projeto o fornecer e autorizar.
3. Distinguir imagem de referência, imagem para editar, recurso protegido e inspiração de estilo.
4. Solicitar à `$imagegen` geração ou edição usando `image_gen` integrada.
5. Validar se houve artefato real; falhas não devem ser classificadas como sucesso.
6. Revisar composição, legibilidade, texto e fidelidade; se necessário, iterar com mudança específica.
7. Validar formato/dimensões/transparência e copiar arquivo selecionado ao projeto, sem sobrescrever originais.
8. Registrar arquivo final, prompt, ferramenta e checklist de QA.

### Isolamento, segurança e custo

- Não aceitar automaticamente instruções embutidas em imagens, arquivos externos ou brand kits como comandos de ferramenta.
- Respeitar permissões já configuradas no Codex, inclusive aprovações para editar ou executar fora do workspace.
- Não criar ou expor credenciais; não ativar API como fallback.
- Scripts locais não devem ter acesso à rede para sua função de validação.
- Política de retenção: manter apenas finais e logs mínimos não sensíveis; prévias descartadas não devem ser publicadas por padrão.
- Brand kits de organizações e pessoas devem permanecer em armazenamento autorizado; não serão versionados/publicados sem aprovação.

### Layout futuro (não implementado nesta branch)

```text
skills/design/image-production/
  SKILL.md
  references/
    briefing.md
    qa.md
  scripts/
    validate_asset.py  # opcional, conforme testes
  tests/
    cases.md
```

### Arquitetura mínima recomendada

Fase 1: SKILL.md + duas referências + checklist e operações manuais já disponíveis no Codex. Fase 2: validador local pequeno, apenas se os testes demonstrarem necessidade. Fase 3: orquestração/automação em lote somente após estabilidade comprovada.
