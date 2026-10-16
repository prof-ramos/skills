# 04 — Plano de implementação e homologação no Mac

**Ambiente-alvo informado:** MacBook Air M3 (ARM64, 8 GB), macOS, Codex CLI `0.163.0`, sessão ChatGPT autenticada. **Não testado por esta alteração no GitHub.**

## Estágios e portas de qualidade

| Estágio | Ação | Evidência exigida | Aceite |
|---|---|---|---|
| P0 — baseline | Registrar `codex --version`, `codex --help`, modo de login e disponibilidade de `$imagegen`; não imprimir tokens | comandos redigidos e outputs saneados | Versão e contexto registrados |
| P1 — esqueleto | Criar skill com YAML correto em `skills/design/image-production/` | lint e descoberta pelo Codex | Sem warnings estruturais |
| P2 — integração | Invocar `$imagegen` integrada em geração simples sem key | logs saneados + PNG real | Arquivo legível e caminho conhecido |
| P3 — edição | Editar imagem local preservando região não solicitada | antes/depois + checklist | Mudança correta sem perda essencial |
| P4 — marca | Aplicar kit de marca de teste não confidencial e texto literal | prompt final + visual + checklist | Sem nome/logo incorreto; texto legível |
| P5 — entrega | Copiar final ao workspace com nome versionado | hash antes/depois + listagem de arquivos | Sem sobrescrita nem asset órfão |
| P6 — falhas | Simular indisponibilidade da ferramenta, arquivo inválido, input ausente e path sem permissão | log de erro e saída não-zero quando pertinente | Falha explícita; sem fallback API |
| P7 — revisão | Executar teste de regressão e revisão de segurança | relatório com evidências | Aprovação para merge e catálogo |

## Conjunto mínimo de casos de teste

| ID | Situação | Verificação | Resultado atual |
|---|---|---|---|
| IP-01 | Gerar uma imagem simples 1:1 com especificação objetiva | Tool integrada utilizada e PNG válido | PENDENTE |
| IP-02 | Produzir peça vertical com texto exato em pt-BR | Texto, hierarquia e leitura em tela móvel | PENDENTE |
| IP-03 | Editar imagem removendo apenas um elemento | Preservar regiões não afetadas | PENDENTE |
| IP-04 | Usar duas referências com funções explícitas | Correspondência de estilo/recurso; sem confusão | PENDENTE |
| IP-05 | Criar peça com brand kit de teste | Cor, identidade e logo preservado | PENDENTE |
| IP-06 | Salvar em diretório definido com nome versionado | Arquivo existe e abre; original intacto | PENDENTE |
| IP-07 | Forçar `image_gen` indisponível | Interromper com diagnóstico, sem API | PENDENTE |
| IP-08 | Ausência de credenciais API (sem expor valores) | Gerar usando login ChatGPT, sem chamadas API | PENDENTE |
| IP-09 | Executar com `codex exec` se ferramenta estiver exposta | Resultado, arquivos e status auditáveis | PENDENTE; COMPATIBILIDADE A VERIFICAR |
| IP-10 | Criar 2 variantes sem duplicação de outputs | Manter somente finais escolhidos | PENDENTE |

## Rubrica visual (referência conceitual do Cookbook)

Escala 0–2 por critério, pontuado com evidência observável:
- **Conformidade:** pedidos explícitos e restrições atendidos;
- **Texto:** ortografia, acentuação, caracteres, números e leitura correta;
- **Hierarquia e composição:** foco, contraste, alinhamento e legibilidade em celular;
- **Marca:** identidade, proporção e integridade de logotipos;
- **Preservação em edição:** áreas fora do escopo não alteradas indevidamente.

Regra inicial sugerida: **nenhuma falha crítica** (texto oficial errado, identidade adulterada, output ausente ou uso não autorizado de API). Pontuação agregada pode ser exploratória, mas não substitui verificação de condições eliminatórias.

## Protocolo operacional

1. Usar um workspace isolado de teste; impedir publicação automática.
2. Verificar previamente comportamento real do Codex e skills instaladas; não fazer upgrade nem trocar modo de autenticação sem necessidade.
3. Executar casos IP-01 a IP-10. Documentar comandos, ferramentas efetivamente invocadas, caminhos, formatos, tamanhos, checksums, observações e conclusão.
4. Para cada erro, ajustar apenas o ponto afetado e repetir o teste que falhou.
5. Não copiar arquivos privados de marca, imagens pessoais ou dados de produção ao repositório.
6. Registrar `PASS`, `FAIL`, `SKIP` (com motivo). É proibido converter `SKIP` em aprovação.
7. Validar `make check` somente depois de inspecionar seu escopo e dependências; qualquer erro existente deve ser distinguido de regressão da nova skill.
8. Criar PR e verificar CI; solicitar autorização antes de qualquer atualização em ambientes de produção ou publicação pública de brand kits.

## Tarefas da fase seguinte

- [ ] Fixar revisão de `openai/skills` e `openai/codex` e revisar direitos de reutilização.
- [ ] Criar `SKILL.md` e referências em `skills/design/image-production/`.
- [ ] Validar sintaxe e descoberta, sem API.
- [ ] Executar e documentar teste end-to-end no Mac.
- [ ] Incorporar somente validadores determinísticos justificados por falhas reproduzidas.
- [ ] Validar cenários de marca e edição com revisão visual.
- [ ] Revisar PR e só então registrar no catálogo `skills.sh`.

## Critério final de homologação

A skill será considerada pronta apenas com todos os cenários essenciais aprovados e evidências reproduzíveis no Mac informado, utilizando a ferramenta integrada sem API, preservando arquivos existentes, respeitando brand kits autorizados e sem desviar de aprovações do Codex.
