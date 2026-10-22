# Smoke test comportamental LegalBR

## Execução de 22/10/2026

**10/10 cenários e 31/31 critérios predefinidos atendidos**, segundo um terceiro
agente avaliador independente. São respostas efetivamente geradas, não apenas
uma leitura das instruções. O teste foi executado sobre o commit
`7b43e3aff84574f0a481ebdad73a7e1de636de62`, antes de adicionar estes registros.
Não foram alteradas rubricas depois de observar as respostas.

- Dois agentes nativos novos (`fork_turns=none`), sem histórico do implementador,
  receberam os quatro arquivos reais listados no manifest e cinco entradas cada.
- Um lote NDA e um lote cookies/compliance; uma resposta por cenário, sem retries.
- Os agentes responderam sem ver a rubrica ou as respostas do outro lote.
- Um terceiro agente novo comparou cada resposta às exigências `deve` e às
  proibições `falha` de `cenarios.json`, admitindo equivalência semântica e
  registrando trechos literais como evidência.
- Todos usaram o modelo nativo herdado da sessão, sem override. Identificador
  exato do modelo, sampling/seed e temperatura não foram expostos por essa API.
- Nenhum contrato real, navegador/CMP ou serviço de assinatura foi acessado.
  A única escrita dos executores foi a gravação local das respostas.

### Registros

Em [runs/2026-10-22](runs/2026-10-22/):
- [manifest.json](runs/2026-10-22/manifest.json): commit e hashes dos arquivos/rubrica.
- [nda-respostas.json](runs/2026-10-22/nda-respostas.json): cinco respostas literais.
- [cookies-respostas.json](runs/2026-10-22/cookies-respostas.json): cinco respostas literais.
- [avaliacao.json](runs/2026-10-22/avaliacao.json): 31 decisões com evidência e limites.

O avaliador registrou uma fragilidade menor: a resposta de
`compliance-correcao-nao-verificada` menciona uma falha “anteriormente documentada”,
embora a entrada só indique um achado, sem dizer se foi documentado. Isso não
alterou a recusa de encerrar o achado ou os critérios aprovados, mas é uma
suposição não sustentada. Portanto, o resultado **não significa zero erros**.
Não foi feita mudança adicional nas skills para mascarar esse resultado.

## Reprodução das entradas

A partir de clone que contenha o commit avaliado, execute:

```bash
python3 skills/legalbr/evals/preparar_entradas.py \
  --ref 7b43e3aff84574f0a481ebdad73a7e1de636de62 \
  --output /tmp/legalbr-eval-nova-execucao
```

O diretório deve ser novo. O script exporta os arquivos reais do commit, remove
as expectativas dos inputs enviados aos executores e calcula os hashes. Ele
**não chama modelo, não pontua e não aprova**. A exportação desta execução foi
comparada byte a byte com o contexto e entradas efetivamente usados.

Para cada lote, abra um agente sem histórico e envie a instrução abaixo,
substituindo os caminhos de contexto, entradas e saída (NDA ou cookies):

> Execute a behavioral sample, not a critique. Read ONLY [context.md] (actual
> supplied skill instructions) and [batch-inputs.json] (five independent
> synthetic user inputs). For each input, produce the answer you would give the
> user applying those skills; treat each scenario independently, do not invent
> missing documents. Do not inspect other repo files, rubrics, tests or outputs.
> Do not browse, sign, send, call external services or perform changes except
> writing your answers. No real-world actions. Save JSON array of objects
> {id,resposta} verbatim in [batch-answers.json]. Your output is model responses,
> not a claim about whether tests pass. Briefly report path when done.

Ao avaliador novo, forneça a rubrica original e as respostas, com esta instrução:

> Independently score actual model outputs against pre-existing rubric. For each
> scenario, score EACH 'deve' criterion pass/fail with short verbatim response
> excerpt evidence; flag critical contradictions or invented facts. Do not demand
> exact wording if semantic requirement satisfied. Check 'falha' where present as
> semantic forbidden behaviors (negated phrases are not failures). Save per-case
> result, per-criterion result/evidence, observations and limitations. This is one
> textual smoke test, not legal certification, not statistical evidence. Note the
> harness disallowed real sign/send actions so outputs cannot prove tool-level
> enforcement.

## Limitações

- Teste exploratório de uma única execução, não benchmark estatístico ou
  multimodelo, avaliação jurídica humana ou garantia de produção.
- Cenários no mesmo lote compartilham contexto: isolamento por lote, não por caso.
- Avaliação semântica também por modelo; não equivale a ground truth humana.
- Restrições do harness reforçam a proibição de ações. O resultado avalia a
  **resposta textual**, não prova que somente a skill impeça chamadas perigosas.
- Não testa integração de ferramentas, instalação isolada, navegação, contratos
  extensos reais, imagens anexadas, consulta jurídica atualizada ou execução CMP.
- Reprodução exata do contexto é possível; reprodução determinística das respostas
  não, pois não há seed/versão de modelo fixada.

## Validação estrutural e falha preexistente separada

Os cinco testes de `tests/test_legalbr_workflows.py` e a validação de 2.179
frontmatters passaram. `git diff --check` não apontou erros. O novo exportador foi
executado e suas três saídas de contexto/inputs comparadas com a execução real.

`make check` continua limitado por falha **preexistente e fora deste PR**:
`test_conflicting_diff_returns_failure_without_raising`, em
`skills/agent-workflows/learn/scripts/tests/test_learn_patch.py:81`.
Reproduzido no snapshot original de main `5d2e93f91c5c0e1e3cd0000bc32032ffebd70ae8`.
A função `_learn_patch.py` invoca `patch --batch -p0`; neste ambiente, GNU patch
2.8 aceita o contexto conflitante com `Hunk #1 succeeded at 1 with fuzz 2`,
insere a linha e retorna sucesso, contrariando o teste. Não é regressão das
skills LegalBR. Esse módulo não foi alterado: corrigir sua política de aplicação
de patches exige trabalho separado. Não se afirma que `make check` está verde.
