# Protocolo de verificação

## Fonte e escopo

1. Legislação: abrir texto compilado do Planalto ou do órgão legislativo competente; conferir dispositivo, alterações, revogações, eficácia temporal e eventual controle de constitucionalidade.
2. STF: conferir tese, processo, decisão, embargos e modulação no portal oficial. Se indisponível, recorrer a acórdão/ata, Informativo ou notícia oficial, declarando o alcance e a hierarquia da evidência. Não tratar notícia como substituta automática do inteiro teor.
3. STJ: conferir repetitivos, súmulas e inteiro teor no portal oficial; diferenciar julgamento isolado, orientação dominante e precedente qualificado.
4. TSE: usar resolução compilada e ato modificador; conferir também o calendário, turno, circunscrição, legitimidade e rito da demanda. Não confundir resolução modificadora com o diploma que contém o artigo.
5. Atos e fatos administrativos: confrontar DOU, Portal da Transparência e publicação do órgão. Nome homônimo, situação atual e evento passado são questões distintas.
6. Bloqueio de site, LexML ou conector não comprova inexistência. Tentar outra fonte oficial e declarar o que faltou.

Registrar separadamente julgamento, publicação, trânsito e eficácia. Não usar a data do commit como data de verificação jurídica. Não atribuir força vinculante universal a todo precedente do STF, STJ ou TSE.

## Metadados de revisão

Preservar os identificadores e a taxonomia existentes. `sourcePath` deve ser caminho real a partir da raiz do repositório. Fontes históricas podem permanecer no Git, sem caminhos órfãos no campo operacional.

| Campo | Regra |
| --- | --- |
| `version` | Incrementar ao alterar conteúdo ou metadados; não é data nem prova de vigência. |
| `verifiedAt` | Data ISO de revisão integral do conteúdo jurídico; `null` se inexistente. |
| `status` | `a conferir`, `vigente`, `alterada` ou `superada`; não confundir com força da argumentação. |
| `sources` | URLs oficiais efetivamente acessadas para a revisão registrada; lista vazia não valida nada. |
| `reviewedAt` | Data de revisão pontual, sem substituir `verifiedAt`. |
| `reviewScope` | Dispositivos ou tópicos efetivamente conferidos e pendências. |

Arquivos migrados mecanicamente permanecem com `verifiedAt: null`, `status: a conferir` e `sources: []`. Uma checagem de YAML não permite promover esses campos. Revisão parcial deve manter o status global pendente e indicar seu alcance, mesmo que tenha fontes válidas.

Avaliar cada argumento no caso concreto:
- Forte: base atual bem estabelecida, fatos comprovados e aderência suficiente, sem distinção material não enfrentada.
- Média: orientação consistente, mas prova incompleta, distinção relevante ou ausência de consolidação aplicável.
- Fraca: analogia distante, entendimento isolado ou divergência material não superada.

Não preencher `forca` em lote: a avaliação depende do argumento e do caso, não apenas do arquivo.

## Prazos e dados

Não calcular vencimento sem termo inicial, meio de ciência, regra de contagem e calendário/suspensões aplicáveis. No Executivo federal, distinguir recurso LAI de reclamação por omissão e de manifestação geral de ouvidoria. Não aplicar Decreto 7.724/2012 automaticamente a estados, municípios ou outros Poderes.

Na análise de risco, examinar a incidência da LGPD e suas exceções, em especial finalidade jornalística; não aplicar os arts. 7º e 23 como autorização genérica para qualquer particular publicar dados funcionais. Qualificações exigidas por um órgão podem constar de anexo restrito, quando admitido, em vez de versão pública.

Saída mínima por fundamento: proposição, fonte oficial, consulta em DD/MM/AAAA, alcance verificado, aplicação aos fatos e eventual ponto “a conferir”.
