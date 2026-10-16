# 02 — Relatório de reaproveitamento

## Já disponível

| Capacidade | Origem | Decisão |
|---|---|---|
| Geração e edição visual | Ferramenta integrada `image_gen` / skill `$imagegen` | **Reusar; não implementar novo gerador** |
| Estrutura e descoberta de skills | `skill-creator` e convenções do repositório | Reusar diretamente e ajustar à hierarquia `skills/design/` |
| Composição de skills | `hatch-pet` | Adaptar o padrão de invocação e pós-processamento; sem copiar processamento de sprites |
| Diretrizes de prompting | OpenAI Academy | Aplicar nos briefings; referência conceitual |
| Critérios de qualidade | Cookbook Image Evals | Adaptar como rubrica; não importar runners de API |
| Produção de copy | `skills/content/social-ads-creator/` | Manter responsabilidade editorial separada |
| Diretrizes de UI | `skills/design/ui-ux-pro-max/` | Manter UI separada de ativos visuais |
| Infraestrutura de validação | `scripts/validate-skills.py` e `Makefile` do repositório | Examinar compatibilidade antes de usar |

## Construir apenas o necessário

1. `skills/design/image-production/SKILL.md` — briefing e roteamento: gerar/editar, referências, identidade visual, restrições, revisões, localização de saída e proveniência.
2. `references/briefing.md` — esquema leve, sem exigir formulário para solicitações simples: objetivo, formato, texto literal, marca, imagens e itens preservados.
3. `references/qa.md` — checklist de avaliação visual: legibilidade, hierarquia, identidade, texto, preservação e segurança.
4. `scripts/validate_asset.py` — **somente se necessário**, verificação determinística de arquivo, dimensões, formato e canal alfa. Preferir Python stdlib e dependências já instaladas, sem pipeline pesado.
5. Testes estáticos e registros locais reprodutíveis, sem imagens reais no repositório, segredos ou branding confidencial.

## Excluído por decisão explícita de produto

- `OPENAI_API_KEY`, `CODEX_API_KEY` e qualquer acesso cobrado à OpenAI API;
- SDKs e `scripts/image_gen.py` de fallback pago;
- gateways não oficiais, automação reversa de interfaces, scraping de sessões e compartilhamento de cookies/tokens;
- treinamento ou fine-tuning de modelos, GPU local, ComfyUI, Stable Diffusion;
- orquestrador de múltiplos agentes como requisito inicial;
- servidor MCP próprio para uma capacidade já disponível como ferramenta integrada.

## Riscos que devem impedir homologação

| Risco | Tratamento |
|---|---|
| `image_gen` não disponível no contexto de execução | Retornar falha verificável e orientar execução integrada; **nunca** usar API silenciosamente |
| Saída gravada apenas no cache do Codex | Copiar a escolhida ao diretório do projeto e verificar abertura |
| Texto incorporado inexato | Comparação visual contra transcrição literal; falha se houver erro em informação essencial |
| Marca, logo ou pessoa alterados indevidamente | Comparação antes/depois e aprovação quando necessário |
| Geração que destrói ativo anterior | Nomes versionados e proibição de sobrescrita sem autorização |
| Metadados privados ou segredos | Não incluir chaves, contatos privados, anexos sensíveis ou arquivos de brand kit em repositório público sem aprovação |

## Regra de decisão

Adicionar script, serviço ou agente somente quando houver caso reprodutível que a ferramenta e os utilitários existentes não resolvam, com teste objetivo e benefício mensurável.
