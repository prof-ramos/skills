#!/usr/bin/env bash
# Driver: edital-verticalizado
# Uso: ./driver.sh <arquivo_edital> [formato: md|csv|json] [cargo]
# Caminhos relativos ao root do projeto (edital-verticalizado/)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

EDITAL_FILE="${1:-$PROJECT_ROOT/examples/edital_exemplo.md}"
FORMATO="${2:-md}"
CARGO="${3:-}"

if [[ ! -f "$EDITAL_FILE" ]]; then
  echo "Erro: arquivo não encontrado: $EDITAL_FILE" >&2
  echo "Uso: $0 <arquivo_edital> [md|csv|json] [cargo]" >&2
  exit 1
fi

EDITAL_CONTENT="$(cat "$EDITAL_FILE")"

CARGO_INSTRUCAO=""
if [[ -n "$CARGO" ]]; then
  CARGO_INSTRUCAO="Processe apenas o cargo: $CARGO."
fi

FORMATO_INSTRUCAO=""
case "$FORMATO" in
  csv)
    FORMATO_INSTRUCAO="Entregue o resultado em CSV separado por ponto e vírgula (UTF-8). Cabeçalho: ID;Cargo;Bloco;Disciplina;Area_Eixo;Assunto;Topico;Subtopico;Texto_Original;Pagina_Fonte;Prioridade;Status;Observacoes"
    ;;
  json)
    FORMATO_INSTRUCAO='Entregue APENAS JSON válido com o schema: {"metadata":{"nome_concurso":"","banca":"","ano":"","orgao":""},"itens":[{"id":"","cargo":"","bloco":"","disciplina":"","area_eixo":"","assunto":"","topico":"","subtopico":"","texto_original":"","pagina_fonte":"","prioridade":"A verificar","status":"Não iniciado","observacoes":""}],"alertas":[]}'
    ;;
  md|markdown)
    FORMATO="md"
    FORMATO_INSTRUCAO="Entregue o resultado em tabela Markdown."
    ;;
  *)
    echo "Erro: formato não suportado: $FORMATO" >&2
    echo "Formatos aceitos: md, csv, json" >&2
    exit 2
    ;;
esac

SYSTEM_PROMPT='Você é um agente especializado em extrair e estruturar editais de concurso público em edital verticalizado.

REGRAS OBRIGATÓRIAS:
1. Localize o conteúdo programático completo.
2. Separe conhecimentos básicos, específicos e complementares no campo Bloco.
3. Identifique: Disciplina → Assunto → Tópico → Subtópico (quando houver).
4. Preserve o texto original do edital na coluna Texto_Original/Texto original.
5. Crie IDs únicos: prefixo 2 letras da disciplina + número sequencial (ex: LP-001, DC-001).
6. Inclua referência de seção/item no campo Página/Fonte.
7. Não invente tópicos. Não remova conteúdo.
8. Separe diplomas legais em linhas distintas quando estiverem numa lista com ponto e vírgula.
9. Não quebre expressões compostas consolidadas (ex: "Administração Pública direta e indireta").
10. Status padrão: "Não iniciado". Prioridade padrão: "A verificar".
11. Sinalize ambiguidades ou trechos duvidosos em Observações.

COLUNAS OBRIGATÓRIAS: ID | Cargo | Bloco | Disciplina | Área/Eixo | Assunto | Tópico | Subtópico | Texto original do edital | Página/Fonte | Prioridade | Status | Observações'

PROMPT="$CARGO_INSTRUCAO $FORMATO_INSTRUCAO

Processe o edital abaixo e gere o edital verticalizado completo:

$EDITAL_CONTENT"

echo "Processando: $EDITAL_FILE (formato: $FORMATO)" >&2
echo "---" >&2

claude -p --system-prompt "$SYSTEM_PROMPT" "$PROMPT"
