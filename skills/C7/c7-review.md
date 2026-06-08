# C7 Review Workflow

Revisão de conformidade de bibliotecas e APIs usando o Context7.

## Descrição

Este workflow guia o agente na análise de documentos de planejamento, arquitetura ou implementação (como `implementation_plan.md`, PRDs, saídas do `repomix`, etc.) para extrair as bibliotecas, frameworks e APIs utilizadas. Ele realiza uma validação ativa dessas tecnologias contra o Context7 (via API ou MCP) para garantir que a utilização está correta, moderna e livre de padrões obsoletos.

## Passos

### Passo 1: Identificar e Extrair a Stack Tecnológica

- Analise o documento de entrada fornecido (por exemplo, `implementation_plan.md`, PRD, `repomix-output.xml`, etc.).
- Liste todas as bibliotecas de terceiros, APIs, SDKs, frameworks e ferramentas que serão (ou estão sendo) utilizadas no projeto ou alteração.

### Passo 2: Consultar o Context7 para cada Componente da Stack

- Para cada biblioteca ou API identificada, utilize a ferramenta ou MCP do Context7 para buscar sua documentação oficial atualizada e melhores práticas.
- Se houver dúvidas sobre a versão, sintaxe específica ou assinaturas de métodos de uma biblioteca no código atual, faça queries direcionadas no Context7.

### Passo 3: Comparar e Validar a Implementação

- Compare a implementação proposta (ou código existente) com a documentação recuperada do Context7.
- Verifique especificamente se:
  - As assinaturas de funções e métodos estão corretas.
  - Há padrões ou métodos obsoletos (deprecated) sendo sugeridos ou utilizados.
  - As configurações recomendadas pelo Context7 estão sendo seguidas.
  - Os tratamentos de erros ou inicializações estão em conformidade com as diretrizes oficiais.

### Passo 4: Reportar Descobertas e Sugerir Correções

- Se encontrar divergências ou oportunidades de melhoria, liste-as claramente para o usuário.
- Para cada divergência apontada, forneça:
  - O trecho incorreto ou obsoleto.
  - A recomendação correta baseada no Context7 (incluindo exemplos de código se apropriado).
  - A justificativa ou referência encontrada no Context7.
- Se tudo estiver em conformidade, informe que a validação via Context7 foi concluída com sucesso.
