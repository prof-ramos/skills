# LegalBR Council

Uma skill de workflow e um seletor local, sem servidor, embeddings ou contratação de modelos. Reutiliza o acervo LegalBR: a recuperação não verifica direito e a orquestração não cria agentes automaticamente.

## Instalar e ativar

```bash
npx skills add prof-ramos/skills --skill legalbr-council
```

No checkout local, validar descoberta antes da instalação:

```bash
npx skills add ./skills/agent-workflows/legalbr-council --list
```

A instalação da skill pode copiar apenas seu diretório. O catálogo e o protocolo LegalBR são dependências de **conteúdo**, localizados fora dele. Manter um checkout autorizado do repositório e apontar `--catalog` para seu diretório `legalbr`; ler `legalbr/SKILL.md` e as referências indicadas. Não alegar instalação autossuficiente sem esse acervo. O helper requer Python 3.10+ e biblioteca padrão; a validação do repositório já usa PyYAML, fora do helper.

Ativação: “Use legalbr-council para avaliar a questão abaixo, com melhor tese contrária, fontes verificadas e lacunas explícitas.” Para consulta simples, a skill escolhe modo direto. Para autonomia multiagente, o usuário precisa autorizar e o runtime precisa fornecer isolamento real; o fallback sequencial funciona com um agente e não declara independência.

## Exemplo completo fictício e offline

**Entrada:** “Uma servidora federal pede remoção por saúde e apresentou somente relato de tratamento; não recebemos laudo nem decisão. Quero parecer preliminar. Não consulte a internet e use um único contexto.”

**Execução:** modo compacto/sequencial; premissas são fictícias, não prova. Selecionar `remocao-redistribuicao-servidor` e `parecer-juridico-consultivo`; ler ambas. Usar distinção entre atuação vinculada/discricionária para organizar os pressupostos e a prova faltante, sem atribuir essa formulação a uma obra não lida. Construir a objeção de insuficiência probatória e conferir as limitações do próprio acervo. Fontes externas não foram consultadas.

**Resultado ilustrativo:** “Não é possível concluir que há direito à remoção com os elementos fornecidos. O enquadramento depende do regime aplicável e da demonstração dos pressupostos da hipótese invocada. A tese favorável considera atuação vinculada quando esses pressupostos estão satisfeitos; a objeção é que não recebemos documento que os comprove. A falta de prova não equivale a prova de ausência da condição de saúde. Solicitar decisão, assentamentos e documentação pertinente, com minimização dos dados. A norma e a jurisprudência mencionadas no acervo permanecem não verificadas nesta execução offline; não há prazo calculado nem recurso protocolado.”

**Registro:** fatos alegados A1…, lacunas L1…; origem das duas skills e hash obtido pelo helper; S1 norma “não verificado”; S2 precedente “não verificado”; conceito doutrinário usado como análise, sem citação atribuída. Revisão necessária antes de decisão concreta. Este exemplo é didático, não saída registrada de avaliação independente.

Com rede autorizada, o auditor abre a fonte primária e registra a afirmação exata, URL, data, trecho, aplicação temporal e limite; somente então o resultado daquela proposição pode mudar para verificado. Uma fonte que confirma existência do artigo pode continuar insuficiente para confirmar a conclusão jurídica ou o fato.

## Arquitetura e limitações

- `SKILL.md`: entrada, seleção, modos, deliberação e entrega.
- `scripts/select_skills.py`: shortlist lexical determinística, limites de 1–12 arquivos, identidade e hash. Sem rede nem gravação de consultas.
- `references/`: instruções efetivamente usadas para recuperação, deliberação, fontes, orçamento/dados.
- `templates/parecer-conselho.md`: resposta executiva, fatos, argumentos, objeções, fontes e diligências.
- `evals/scenarios.md`: entradas e critérios para avaliação comportamental real, separada dos testes de código.

O catálogo atual contém 2.156 entradas (304 formas, 1.851 matérias e hub), após PRs anteriores; os 2.149 itens históricos não são reestruturados pelo Council. A busca considera 2.155 arquivos de Forma/Matéria, excluindo o hub. A nova skill vive fora de `legalbr/`.

Ranking lexical perde sinônimos e pode trazer falsos positivos. Ler e avaliar a shortlist, pesquisar tese oposta e registrar lacunas. Orçamento e privacidade são instruções para o executor, não sandbox adicional. Não afirmar auditoria automática de vigência, jurisprudência ou mérito. Consenso não prova correção. Ações externas e uso de dados continuam dependentes das permissões da sessão.

## Verificar

Na raiz do checkout:

```bash
python3 tests/test_legalbr_council.py -v
python3 legalbr/scripts/catalogo.py --check
python3 scripts/validate-skills.py
python3 scripts/validate_skills_sh.py --strict
python3 tests/test_cli_discovery_oracle.py -v
make check
```

Testes unitários executam recuperação em arquivos reais e CLI local, incluindo índice ausente/defasado, ausência de resultado, filtro de área, limite e hash. Eles **não** demonstram preservação de divergência em respostas de modelo, sigilo de um runtime, vigência ou qualidade de parecer. Cenários comportamentais precisam de entradas/saídas registradas e revisão; não transformar a mera existência das rubricas em teste passado.
