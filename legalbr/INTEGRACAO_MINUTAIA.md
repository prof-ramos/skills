# Integração com o MinutaIA

O `legalbr` é o corpus canônico de skills. O checkout do MinutaIA é uma fonte
de comparação e de datasets opcionais; ele não deve ser copiado para dentro do
pacote distribuível de skills.

## Política de fonte

- `forma/` e `materia/` no `legalbr` são a fonte de verdade para as skills.
- O MinutaIA pode ser usado para auditoria de UUID, nome, caminho e corpo.
- Alterações semânticas no corpus exigem a política de versionamento já descrita
  no repositório; uma renomeação não cria uma segunda skill.
- Legislação e jurisprudência são snapshots de recuperação, sempre datados e
  sujeitos à conferência na fonte oficial. Não são autoridade jurídica por si.
- Os arquivos brutos não fazem parte deste pacote. O manifesto em `data/`
  registra a proveniência e as contagens observadas.

## Reconciliação observada em 2026-09-21

A auditoria por UUID encontrou **2.149 skills correspondentes**, sem UUIDs
duplicados e sem divergência de corpo. Portanto, não há uma segunda cópia a
importar. Há uma diferença de nome no frontmatter e diferenças de slug de
diretório causadas pelo empacotamento do `legalbr`; elas são mapeadas pelo
script de reconciliação e não devem gerar novas skills.

A única diferença de `name` no frontmatter é:

| MinutaIA | legalbr |
|---|---|
| `controle-constitucionalidade-estadual-reproducao-obrigatoria-tema-484` | `controle-constitucionalidade-reproducao-obrigatoria-tema-484` |

O `legalbr` pode manter seus diretórios canônicos e seus nomes de distribuição;
o UUID é a identidade estável para sincronização.

Para repetir a auditoria contra outro checkout:

```bash
uv run --no-project python scripts/reconcile_minutai.py \
  --minutai-root /caminho/para/minutai \
  --output /tmp/legalbr-reconciliation.json \
  --strict
```

## Roteamento de processos

O `legalbr` fornece o vocabulário e o índice; uma aplicação pode receber o
texto de um processo, recuperar candidatos e então usar TypeSafe AI somente
para a decisão tipada entre candidatos. O fluxo e o contrato estão em
[`docs/ROTEAMENTO_PROCESSO.md`](docs/ROTEAMENTO_PROCESSO.md).
