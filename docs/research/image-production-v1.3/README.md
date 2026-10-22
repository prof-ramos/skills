# Image Production v1.3 — pesquisa e decisão arquitetural

**Data de corte:** 2026-10-16 · **Estado:** pesquisa preliminar consolidada; implementação e homologação local pendentes.

## Objetivo

Construir a menor Agent Skill `image-production` capaz de planejar, gerar, editar, validar e entregar ativos visuais para projetos no Codex CLI, **sem consumir a API OpenAI nem exigir `OPENAI_API_KEY`**. Usar preferencialmente a ferramenta `image_gen` integrada à sessão autenticada do ChatGPT/Codex. A disponibilidade da ferramenta não deve ser confundida com garantia de funcionamento em qualquer versão, ambiente ou execução não interativa.

## Premissas verificadas e limites

- Histórico de teste fornecido pelo usuário: Codex CLI `0.163.0`, macOS Apple Silicon M3, 8 GB RAM, autenticação ChatGPT; geração de PNG válido 1312×1199 pixels por `image_gen`, sem chaves da API no ambiente. Esse é um relato do ambiente local, **não um teste realizado por esta atualização GitHub**.
- A pesquisa identificou `openai/skills` (`hatch-pet`, `skill-creator`, `imagegen`), `openai/codex`, `openai/openai-cookbook`, OpenAI Academy e Cookbook de avaliações.
- `hatch-pet` compõe a skill `$imagegen` e usa scripts determinísticos para validar e montar artefatos — padrão de arquitetura recomendado.
- `imagegen` privilegia a ferramenta integrada; qualquer fallback via `scripts/image_gen.py` pressupõe API key e fica **excluído** deste projeto.
- Não houve inspeção do Mac, instalação, execução de testes, mudanças de credenciais ou incorporação de bibliotecas nesta atualização.
- Parte das fontes externas tem conteúdo que pode mudar; fixar SHAs/tags quando a implementação começar. Declarações de comportamento não documentado devem ser tratadas como hipóteses até validação.

## Entregáveis

1. [Inventário de fontes](./01-inventario-fontes.md)
2. [Relatório de reaproveitamento](./02-reaproveitamento.md)
3. [Arquitetura recomendada](./03-arquitetura.md)
4. [Plano operacional de implementação e homologação](./04-implementacao-homologacao.md)

## Decisão

**Criar uma skill de orquestração, não um novo gerador.** A `image-production` deve invocar `$imagegen` para geração/edição por ferramenta integrada, carregar o brand kit especificado e executar verificações determinísticas locais de dimensões, arquivo, transparência (quando necessária), nomeação e entrega. Julgamentos visuais e textuais exigem revisão humana ou validação adicional; não devem ser declarados automaticamente aprovados sem evidência.

## Escopo desta branch

Publicação de pesquisa/planejamento para revisão. A futura skill operacional deverá ficar em `skills/design/image-production/` após execução e aprovação dos testes definidos. Não registrar automaticamente no catálogo `skills.sh` antes de haver implementação funcional.

## Relação com skills existentes

- `skills/content/social-ads-creator/`: estratégia editorial/copy, que poderá gerar o briefing de imagem.
- `skills/design/ui-ux-pro-max/`: UI e design de aplicações; não substitui a geração de imagens.
- A nova skill não deve copiar indevidamente o motor, fluxo de API ou responsabilidades dessas skills.

## Critério para marcar conclusão

Marcar como **implementado** somente depois de criar os arquivos da skill, executar validações estáticas, invocar a skill a partir do Codex no Mac, gerar/editar imagem via ferramenta integrada **sem chave API**, verificar artefatos e registrar relatório de testes reproduzível.
