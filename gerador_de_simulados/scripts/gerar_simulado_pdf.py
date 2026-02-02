#!/usr/bin/env python3
"""
Gerador de PDF para Simulados de Concursos

Converte um simulado em formato Markdown para PDF formatado,
pronto para impressão. Suporta PDF/UA para acessibilidade.

Uso:
    python gerar_simulado_pdf.py entrada.md saida.pdf
    python gerar_simulado_pdf.py entrada.md saida.html --html
    python gerar_simulado_pdf.py entrada.md saida.pdf --verbose

Dependências:
    pip install weasyprint
"""

from __future__ import annotations

import argparse
import html
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import TypedDict

logger = logging.getLogger(__name__)


def escape_html(text: str | None) -> str:
    """Escapa caracteres especiais HTML para prevenir XSS."""
    if text is None:
        return ""
    return html.escape(str(text))


# Type definitions
class Questao(TypedDict):
    numero: str
    texto: str
    alternativas: list[tuple[str, str]]
    origem: str


class Disciplina(TypedDict):
    nome: str
    questoes: list[Questao]


class Secao(TypedDict):
    nome: str
    disciplinas: list[Disciplina]


class DadosSimulado(TypedDict):
    titulo: str
    cargo: str
    banca: str
    data: str
    secoes: list[Secao]
    gabarito: list[tuple[str, str]]


# Template HTML para o simulado (PDF/UA compatível)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <meta name="author" content="Gerador de Simulados">
    <meta name="description" content="Simulado para concurso - {cargo}">
    <meta name="keywords" content="simulado, concurso, {banca}, questões">
    <meta name="dcterms.created" content="{data_iso}">
    <meta name="generator" content="gerar_simulado_pdf.py">
    <style>
        @page {{
            size: A4;
            margin: 25mm;
            @bottom-center {{
                content: "Página " counter(page) " de " counter(pages);
                font-size: 10pt;
                color: #666;
            }}
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Times New Roman', Times, serif;
            font-size: 12pt;
            line-height: 1.5;
            color: #333;
            max-width: 100%;
        }}

        header {{
            text-align: center;
            border-bottom: 2px solid #333;
            padding-bottom: 15px;
            margin-bottom: 25px;
        }}

        header h1 {{
            font-size: 18pt;
            margin: 0 0 10px 0;
            text-transform: uppercase;
        }}

        header .info {{
            font-size: 11pt;
            color: #555;
        }}

        h2 {{
            background-color: #f0f0f0;
            padding: 10px 15px;
            margin: 25px 0 15px 0;
            border-left: 4px solid #333;
            font-weight: bold;
            font-size: 14pt;
            page-break-after: avoid;
        }}

        h3 {{
            font-weight: bold;
            font-size: 12pt;
            color: #444;
            margin: 20px 0 10px 0;
            padding-bottom: 5px;
            border-bottom: 1px solid #ddd;
            page-break-after: avoid;
        }}

        article.questao {{
            margin: 15px 0;
            padding: 10px;
            background-color: #fafafa;
            border-radius: 4px;
            page-break-inside: avoid;
        }}

        .questao-numero {{
            font-weight: bold;
            color: #333;
        }}

        .questao-texto {{
            margin: 10px 0;
            text-align: justify;
        }}

        .alternativas {{
            margin: 10px 0 10px 20px;
            list-style: none;
            padding: 0;
        }}

        .alternativas li {{
            margin: 5px 0;
            padding: 3px 0;
        }}

        .alternativa-letra {{
            font-weight: bold;
            margin-right: 8px;
        }}

        .origem {{
            font-size: 9pt;
            color: #777;
            font-style: italic;
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px dashed #ddd;
        }}

        section.gabarito {{
            margin-top: 30px;
            padding: 20px;
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            page-break-before: always;
        }}

        section.gabarito h2 {{
            text-align: center;
            margin-bottom: 20px;
            font-size: 16pt;
            background: none;
            border: none;
            padding: 0;
        }}

        .gabarito-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .gabarito-item {{
            width: 80px;
            padding: 4px 8px;
            background-color: #fff;
            border: 1px solid #ccc;
            text-align: center;
            font-family: monospace;
            font-size: 11pt;
        }}

        footer {{
            margin-top: 30px;
            padding-top: 15px;
            border-top: 1px solid #ccc;
            font-size: 9pt;
            color: #777;
            text-align: center;
        }}

        @media print {{
            article.questao {{
                page-break-inside: avoid;
            }}
            h2, h3 {{
                page-break-after: avoid;
            }}
        }}
    </style>
</head>
<body>
    {conteudo}
</body>
</html>
"""


def parse_markdown_simulado(md_content: str) -> DadosSimulado:
    """
    Analisa o conteúdo Markdown do simulado e extrai estrutura.

    Args:
        md_content: Conteúdo do arquivo Markdown

    Returns:
        Dicionário com dados estruturados do simulado
    """
    resultado: DadosSimulado = {
        "titulo": "",
        "cargo": "",
        "banca": "",
        "data": datetime.now().strftime("%d/%m/%Y"),
        "secoes": [],
        "gabarito": [],
    }

    linhas = md_content.split("\n")
    secao_atual: Secao | None = None
    disciplina_atual: Disciplina | None = None
    questao_atual: Questao | None = None

    i = 0
    while i < len(linhas):
        linha = linhas[i].strip()

        # Detectar título principal
        if linha.startswith("# SIMULADO") or linha.startswith("SIMULADO"):
            resultado["titulo"] = linha.replace("#", "").strip()
            logger.debug(f"Título encontrado: {resultado['titulo']}")

        # Detectar informações do cabeçalho
        elif linha.lower().startswith("cargo:"):
            resultado["cargo"] = linha.split(":", 1)[1].strip()
        elif linha.lower().startswith("banca:"):
            resultado["banca"] = linha.split(":", 1)[1].strip()

        # Detectar seções (PARTE I, PARTE II, etc.)
        elif "PARTE I" in linha.upper() or "CONHECIMENTOS GERAIS" in linha.upper():
            secao_atual = {"nome": "CONHECIMENTOS GERAIS", "disciplinas": []}
            resultado["secoes"].append(secao_atual)
            logger.debug("Seção: Conhecimentos Gerais")
        elif "PARTE II" in linha.upper() or "CONHECIMENTOS ESPECÍFICOS" in linha.upper():
            secao_atual = {"nome": "CONHECIMENTOS ESPECÍFICOS", "disciplinas": []}
            resultado["secoes"].append(secao_atual)
            logger.debug("Seção: Conhecimentos Específicos")
        elif "DISSERTATIVA" in linha.upper():
            secao_atual = {"nome": "QUESTÕES DISSERTATIVAS", "disciplinas": []}
            resultado["secoes"].append(secao_atual)
        elif "GABARITO" in linha.upper():
            # Coletar gabarito
            i += 1
            while i < len(linhas):
                linha_gab = linhas[i].strip()
                if linha_gab:
                    # Formato: 01-A  02-C  03-B
                    matches = re.findall(r"(\d+)[.-]([A-Ea-e])", linha_gab)
                    for num, letra in matches:
                        resultado["gabarito"].append((num, letra.upper()))
                i += 1
            break

        # Detectar disciplina (linha em colchetes ou negrito)
        elif linha.startswith("[") and linha.endswith("]"):
            disciplina_atual = {"nome": linha[1:-1], "questoes": []}
            if secao_atual:
                secao_atual["disciplinas"].append(disciplina_atual)
        elif linha.startswith("**") and linha.endswith("**"):
            disciplina_atual = {"nome": linha[2:-2], "questoes": []}
            if secao_atual:
                secao_atual["disciplinas"].append(disciplina_atual)

        # Detectar questão
        elif re.match(r"^[Qq]uest[aã]o\s*(\d+)", linha) or re.match(r"^(\d+)[.)]\s", linha):
            match = re.match(r"^[Qq]uest[aã]o\s*(\d+)[.)]?\s*(.*)", linha)
            if not match:
                match = re.match(r"^(\d+)[.)]\s*(.*)", linha)

            if match:
                num = match.group(1)
                texto = match.group(2) if match.lastindex >= 2 else ""

                # Coletar texto completo da questão
                i += 1
                while i < len(linhas) and not re.match(r"^\([A-Ea-e]\)", linhas[i].strip()):
                    if linhas[i].strip():
                        texto += " " + linhas[i].strip()
                    i += 1
                i -= 1  # Voltar uma linha para processar alternativas

                questao_atual = {
                    "numero": num,
                    "texto": texto.strip(),
                    "alternativas": [],
                    "origem": "",
                }

                if disciplina_atual:
                    disciplina_atual["questoes"].append(questao_atual)
                elif secao_atual and secao_atual["disciplinas"]:
                    secao_atual["disciplinas"][-1]["questoes"].append(questao_atual)

        # Detectar alternativas
        elif re.match(r"^\([A-Ea-e]\)", linha):
            if questao_atual:
                letra = linha[1]
                texto_alt = linha[3:].strip()
                questao_atual["alternativas"].append((letra, texto_alt))

        # Detectar origem
        elif linha.lower().startswith("origem:"):
            if questao_atual:
                questao_atual["origem"] = linha.split(":", 1)[1].strip()

        i += 1

    logger.info(f"Parsed: {len(resultado['secoes'])} seções, {len(resultado['gabarito'])} respostas no gabarito")
    return resultado


def gerar_html(dados: DadosSimulado) -> str:
    """
    Gera HTML formatado a partir dos dados do simulado.

    Usa tags semânticas (header, section, article) para PDF/UA.

    Args:
        dados: Dados estruturados do simulado

    Returns:
        String HTML completa
    """
    html_parts: list[str] = []

    # Cabeçalho semântico
    html_parts.append(f"""
    <header>
        <h1>{escape_html(dados['titulo']) or 'SIMULADO'}</h1>
        <div class="info">
            <p><strong>Cargo:</strong> {escape_html(dados['cargo']) or 'N/A'}</p>
            <p><strong>Banca:</strong> {escape_html(dados['banca']) or 'N/A'}</p>
            <p><strong>Data de geração:</strong> {escape_html(dados['data'])}</p>
        </div>
    </header>
    <main>
    """)

    # Seções e questões
    for secao in dados["secoes"]:
        if secao["nome"] == "GABARITO":
            continue

        html_parts.append(f"<section><h2>{escape_html(secao['nome'])}</h2>")

        for disciplina in secao["disciplinas"]:
            if disciplina["nome"]:
                html_parts.append(f"<h3>{escape_html(disciplina['nome'])}</h3>")

            for questao in disciplina["questoes"]:
                html_parts.append('<article class="questao">')
                html_parts.append(f'<span class="questao-numero">Questão {escape_html(questao["numero"])}.</span>')
                html_parts.append(f'<p class="questao-texto">{escape_html(questao["texto"])}</p>')

                if questao["alternativas"]:
                    html_parts.append('<ul class="alternativas" role="list">')
                    for letra, texto in questao["alternativas"]:
                        html_parts.append(
                            f'<li><span class="alternativa-letra">({escape_html(letra)})</span>{escape_html(texto)}</li>'
                        )
                    html_parts.append("</ul>")

                if questao["origem"]:
                    html_parts.append(f'<p class="origem">Origem: {escape_html(questao["origem"])}</p>')

                html_parts.append("</article>")

        html_parts.append("</section>")

    html_parts.append("</main>")

    # Gabarito
    if dados["gabarito"]:
        html_parts.append("""
        <section class="gabarito">
            <h2>GABARITO OFICIAL</h2>
            <div class="gabarito-grid" role="list">
        """)

        for num, letra in sorted(dados["gabarito"], key=lambda x: int(x[0]) if x[0].isdigit() else 0):
            html_parts.append(f'<div class="gabarito-item" role="listitem">{escape_html(num)}-{escape_html(letra)}</div>')

        html_parts.append("</div></section>")

    # Footer
    html_parts.append(f"""
    <footer>
        <p>Simulado gerado automaticamente em {dados['data']}</p>
        <p>Este material é exclusivamente para fins de estudo.</p>
    </footer>
    """)

    conteudo = "\n".join(html_parts)
    data_iso = datetime.now().isoformat()

    return HTML_TEMPLATE.format(
        titulo=dados["titulo"] or "Simulado",
        cargo=dados["cargo"] or "N/A",
        banca=dados["banca"] or "N/A",
        data_iso=data_iso,
        conteudo=conteudo,
    )


def gerar_pdf(html_content: str, output_path: Path) -> bool:
    """
    Converte HTML para PDF usando WeasyPrint.

    Args:
        html_content: String HTML completa
        output_path: Caminho para salvar o PDF

    Returns:
        True se gerado com sucesso, False se WeasyPrint não disponível
    """
    try:
        from weasyprint import HTML

        HTML(string=html_content).write_pdf(str(output_path))
        return True
    except ImportError:
        logger.warning("WeasyPrint não instalado. Use: pip install weasyprint")
        return False
    except Exception as e:
        logger.error(f"Erro ao gerar PDF: {e}")
        return False


def create_parser() -> argparse.ArgumentParser:
    """Cria e configura o parser de argumentos."""
    parser = argparse.ArgumentParser(
        prog="gerar_simulado_pdf",
        description="Converte simulado Markdown para PDF formatado, pronto para impressão.",
        epilog="Exemplo: python gerar_simulado_pdf.py simulado.md output.pdf --verbose",
    )

    parser.add_argument(
        "entrada",
        type=Path,
        help="Arquivo Markdown de entrada",
    )
    parser.add_argument(
        "saida",
        type=Path,
        help="Arquivo de saída (PDF ou HTML)",
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Gerar apenas HTML (sem converter para PDF)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Exibir informações detalhadas de processamento",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Modo debug (exibe todas as mensagens de log)",
    )

    return parser


def main() -> int:
    """
    Função principal do script.

    Returns:
        Código de saída (0 = sucesso, 1 = erro)
    """
    parser = create_parser()
    args = parser.parse_args()

    # Configurar logging baseado nos argumentos
    log_level = logging.WARNING
    if args.debug:
        log_level = logging.DEBUG
    elif args.verbose:
        log_level = logging.INFO

    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=log_level,
    )
    logger.setLevel(log_level)

    entrada: Path = args.entrada
    saida: Path = args.saida
    apenas_html: bool = args.html

    # Verificar arquivo de entrada
    if not entrada.exists():
        logger.error(f"Arquivo não encontrado: {entrada}")
        return 1

    if not entrada.is_file():
        logger.error(f"Caminho não é um arquivo: {entrada}")
        return 1

    # Ler conteúdo
    logger.info(f"📖 Lendo arquivo: {entrada}")
    try:
        md_content = entrada.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        logger.error(f"Erro de codificação no arquivo: {e}")
        return 1

    # Analisar conteúdo
    logger.info("🔍 Analisando estrutura do simulado...")
    dados = parse_markdown_simulado(md_content)

    # Estatísticas
    total_questoes = sum(
        len(d["questoes"])
        for s in dados["secoes"]
        for d in s["disciplinas"]
    )

    print(f"📊 Encontradas {total_questoes} questões")
    print(f"📋 Gabarito com {len(dados['gabarito'])} respostas")

    # Gerar HTML
    logger.info("🎨 Gerando HTML formatado...")
    html_content = gerar_html(dados)

    # Salvar
    if apenas_html or saida.suffix == ".html":
        saida_html = saida.with_suffix(".html") if saida.suffix != ".html" else saida
        saida_html.write_text(html_content, encoding="utf-8")
        print(f"✅ HTML gerado: {saida_html}")
    else:
        logger.info("📄 Convertendo para PDF...")
        if gerar_pdf(html_content, saida):
            print(f"✅ PDF gerado: {saida}")
        else:
            # Fallback para HTML
            saida_html = saida.with_suffix(".html")
            saida_html.write_text(html_content, encoding="utf-8")
            print(f"⚠️  PDF não disponível. HTML gerado: {saida_html}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
