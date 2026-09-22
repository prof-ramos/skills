# Camada opcional de dados

Este diretório contém apenas metadados versionados. Os textos brutos do
MinutaIA não são incorporados ao `legalbr`, porque são snapshots grandes,
regeneráveis e sujeitos a atualização.

O manifesto em [`manifest.json`](manifest.json) registra a coleta usada para a
integração. O checkout externo deve ser passado explicitamente aos scripts.

## Validar um checkout de dados

```bash
uv run --no-project python scripts/validate_minutai_data.py \
  --data-root /Users/gabrielramos/Developer/playground/redground/minutai/data \
  --manifest data/manifest.json
```

Depois de uma nova coleta, atualize as contagens e o hash observado com:

```bash
uv run --no-project python scripts/validate_minutai_data.py \
  --data-root /caminho/para/minutai/data \
  --manifest data/manifest.json \
  --write-manifest
```

O validador confere também o `data_tree_sha256` registrado no manifesto, de modo
que uma alteração de conteúdo sem mudança de contagem é detectada. Códigos de
saída:

- `0` — checkout íntegro e consistente com o manifesto, ou manifesto atualizado
  com sucesso em `--write-manifest`.
- `1` — problema estrutural (par `.json`/`.txt` incompleto, JSON inválido, texto
  vazio) ou divergência em relação ao manifesto.

Em caso de problema estrutural o manifesto **não** é reescrito, para que um
checkout inválido nunca substitua o baseline confiável.

## Construir índice local opcional

O índice SQLite não é fonte canônica e não deve ser commitado:

```bash
uv run --no-project python scripts/build_minutai_index.py \
  --data-root /Users/gabrielramos/Developer/playground/redground/minutai/data \
  --output /tmp/legalbr-minutai.sqlite3 \
  --overwrite
```

O índice contém texto e metadados para recuperação lexical. A aplicação deve
combinar seus resultados com as skills do `legalbr` e registrar a data do
snapshot ao apresentar qualquer fundamento jurídico.
