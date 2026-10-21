# LegalBR — acervo LegalSkillsBR

Protocolo de pesquisa e acervo de modelos e matérias de direito brasileiro. O conteúdo é referência secundária e exige verificação em fontes oficiais no caso concreto.

## Estrutura real

```text
legalbr/
├── SKILL.md                   # protocolo central
├── indice.tsv                 # índice gerado; caminhos relativos a legalbr/
├── forma/<slug>/SKILL.md      # modelos documentais
├── materia/<area>/<slug>/SKILL.md
├── references/               # verificação e consistência temática
└── scripts/catalogo.py       # validação e geração do índice
```

O inventário desta revisão contém **2.156 SKILL.md**: 1 protocolo raiz, **304 formas** e **1.851 matérias** em 25 áreas. O acervo anterior tinha 299 formas e 1.850 matérias. Contagens devem ser regeneradas ao adicionar ou remover itens; integridade estrutural não significa correção jurídica.

## Consultar

1. Ler `SKILL.md`, identificar objetivo e data relevante e buscar nomes/assuntos no índice.
2. Para documento, escolher uma forma e as matérias pertinentes; para pesquisa, escolher matérias. Ler os arquivos inteiros.
3. Verificar os fundamentos materiais nas fontes oficiais e registrar a aderência aos fatos. Não tomar título, trigger ou data de commit como validação.

```bash
rg -i 'assédio|jornada|registro de ponto' legalbr/indice.tsv
rg -i 'compensação|precatório' legalbr/materia/ legalbr/forma/
```

Os comandos partem da raiz do repositório. Todos os caminhos `sourcePath` passam a apontar para o arquivo real no repositório. O histórico anterior permanece no Git.

## Metadados e limites

Os arquivos legados preservam identificadores, categorias e gatilhos técnicos. Suas descrições de ativação foram encurtadas para indicar uso; isso não revalida o conteúdo.

- `version`: revisão do arquivo, inclusive migração de metadados; não é prova de vigência.
- `verifiedAt: null`, `status: a conferir`, `sources: []`: conteúdo sem revisão jurídica integral registrada.
- `reviewedAt`, `reviewScope` e `sources`: conferência parcial, com escopo explícito. Não promovem o arquivo inteiro a validado.
- `verifiedAt` preenchido exige revisão integral efetiva e fontes oficiais. Revisão periódica sugerida: trimestral para os itens mais usados, além de revisão imediata após alteração relevante.

O índice desta revisão mantém **zero arquivos com validação jurídica integral declarada**. As correções pontuais estão identificadas no escopo de cada arquivo. Não se fez auditoria jurídica integral das 2.149 habilidades herdadas.

## Fluxos adicionados

- `forma/pedido-lai` e `forma/recurso-lai`: acesso e recursos, com rito específico de omissão.
- `forma/denuncia-tcu`: competência, legitimidade, identificação e proteção de dados.
- `forma/manifestacao-falabr`: classificação, anonimato e limite operacional de relato.
- `forma/parecer-risco-publicacao`: prioridades, evidência e correções textuais.
- `materia/administrativo/fatos-agentes-publicos`: confronto entre bases e minimização de dados.

## Manter e validar

Requer Python 3.10+ e PyYAML no ambiente de manutenção. O validador não consulta a internet nem verifica o direito: confere YAML, chaves duplicadas, caminhos, URLs oficiais, datas, escopo de revisão e índice.

```bash
python3 legalbr/scripts/catalogo.py --write
python3 legalbr/scripts/catalogo.py --check
python3 scripts/validate-skills.py
```

Não atribuir validade jurídica ao resultado desses comandos. O `indice.tsv` gerado aqui é interno ao acervo e não presume a existência ou atualização de `/home/box/juridico/indice.tsv` em outro computador.

## Descoberta por instaladores

A árvore contém um protocolo raiz e habilidades filhas. Instaladores podem interromper a descoberta na primeira pasta com SKILL.md; para explorar as filhas, usar os subdiretórios ou opção de descoberta profunda suportada pelo instalador. Ao instalar uma filha isoladamente, manter acesso ao protocolo e às referências relativos à raiz; não presumir que um instalador copia arquivos ancestrais. A validação executada nesta revisão é local; não se declara teste real em todos os agentes.
