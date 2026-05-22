#!/usr/bin/env python3
"""
reporter.py — Gerador de Relatórios de Segurança (Markdown + PDF).

Gera relatórios profissionais de segurança com seções executiva, técnica,
recomendações e evidências, em conformidade com OWASP Testing Guide e
NIST SP 800-115. Inclui timestamp e hash de integridade como assinatura.

Uso:
    python scripts/reporter.py --analysis analysis/arquivo.json \
           --target "Empresa XYZ" --tester "Pentester A" --output reports/

Autor: Ethical RedTeam Skill
Versão: 1.0.0
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from jinja2 import Environment, BaseLoader
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError as e:
    print(f"[ERRO] {e}. Execute o install.sh primeiro.")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).parent))
from utils import configurar_logger

console = Console()

TEMPLATE_EXECUTIVO = """# Relatório de Segurança — Sumário Executivo

**Data:** {{ data }}
**Alvo:** {{ alvo }}
**Responsável pelo Teste:** {{ tester }}
**Classificação:** ⚠️ CONFIDENCIAL — Uso restrito
**Hash de Integridade:** `{{ hash_integridade }}`

---

> ⚠️ **DISCLAIMER:** Este relatório foi gerado por testes de segurança autorizados
> conduzidos exclusivamente em ambiente controlado. As informações aqui contidas
> são confidenciais e destinadas apenas às partes autorizadas.

---

## Visão Geral do Risco

| Indicador | Valor |
|-----------|-------|
| Risco Geral | **{{ risco_geral }}** |
| Total de Achados | {{ total_achados }} |
| Achados Críticos | 🔴 {{ criticos }} |
| Achados Altos | 🟠 {{ altos }} |
| Achados Médios | 🟡 {{ medios }} |
| Achados Baixos | 🟢 {{ baixos }} |

## Conclusão Executiva

{{ conclusao }}

## Top 3 Achados Críticos/Altos

{% for achado in top_achados %}
### {{ loop.index }}. {{ achado.descricao }}
- **Severidade:** {{ achado.severidade }}
- **Host:** {{ achado.get('host', 'N/A') }}
- **Recomendação Principal:** {{ achado.recomendacao }}
{% endfor %}

---
*Relatório gerado automaticamente pela Ethical Red Team Skill v1.0.0*
*Conformidade: OWASP Testing Guide v4.2 | NIST SP 800-115*
"""

TEMPLATE_TECNICO = """# Relatório de Segurança — Detalhamento Técnico

**Data:** {{ data }}
**Alvo:** {{ alvo }}
**Responsável pelo Teste:** {{ tester }}
**Hash de Integridade:** `{{ hash_integridade }}`

---

## Metodologia

Este teste foi conduzido seguindo a metodologia OWASP Testing Guide v4.2,
com cobertura das categorias OWASP Top 10 (2021) e controles NIST SP 800-115.

**Fases executadas:**
1. Reconhecimento (passivo e ativo)
2. Enumeração de serviços e portas
3. Análise de vulnerabilidades
4. Correlação e classificação (CVSS v3.1)

---

## Achados Detalhados

{% for achado in achados %}
---

### {{ loop.index }}. {{ achado.descricao }}

| Campo | Valor |
|-------|-------|
| **ID** | `{{ achado.id }}` |
| **Tipo** | {{ achado.tipo }} |
| **Host** | {{ achado.get('host', 'N/A') }} |
| **Porta** | {{ achado.get('porta', 'N/A') }} |
| **Severidade** | **{{ achado.severidade }}** |
| **CVSS Score** | {{ achado.cvss_score }} |
| **Referência** | {{ achado.get('cve_ref', 'N/A') }} |
| **Frameworks** | {{ ', '.join(achado.get('frameworks', [])) }} |

**Evidência:**
```
{{ achado.evidencia }}
```

**Recomendação:**
{{ achado.recomendacao }}

{% endfor %}

---

## Resumo de Recomendações Prioritárias

{% for achado in achados_criticos_altos %}
- [ ] **[{{ achado.severidade }}]** `{{ achado.get('host', 'N/A') }}` — {{ achado.recomendacao }}
{% endfor %}

---
*Hash de Integridade: `{{ hash_integridade }}`*
*Gerado em: {{ data }} | Ethical Red Team Skill v1.0.0*
"""


class GeradorRelatorio:
    """
    Gerador de relatórios de segurança em Markdown e PDF.

    Produz relatórios executivo e técnico com assinatura de integridade
    (hash SHA-256), timestamp e conformidade OWASP/NIST.
    """

    def __init__(self, arquivo_analise: str, nome_alvo: str, nome_tester: str, diretorio_saida: str):
        """
        Inicializa o gerador de relatório.

        Parâmetros:
            arquivo_analise: Caminho para o JSON de análise consolidada.
            nome_alvo: Nome descritivo do alvo (para o relatório).
            nome_tester: Nome do responsável pelo teste.
            diretorio_saida: Diretório para salvar os relatórios gerados.
        """
        self.nome_alvo = nome_alvo
        self.nome_tester = nome_tester
        self.diretorio_saida = diretorio_saida
        self.logger, self.log_file = configurar_logger("reporter")
        self.analise = self._carregar_analise(arquivo_analise)
        self.data_relatorio = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        self.env = Environment(loader=BaseLoader())

    def _carregar_analise(self, caminho: str) -> dict:
        """
        Carrega o arquivo JSON de análise consolidada.

        Parâmetros:
            caminho: Caminho para o arquivo JSON.

        Retorna:
            dict: Dados da análise carregados.
        """
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Erro ao carregar análise: {e}")
            console.print(f"[bold red]❌ Erro ao carregar análise: {e}[/bold red]")
            sys.exit(1)

    def _calcular_hash(self, conteudo: str) -> str:
        """
        Calcula hash SHA-256 do conteúdo para assinatura de integridade.

        Parâmetros:
            conteudo: String com o conteúdo a ser assinado.

        Retorna:
            str: Hash SHA-256 em hexadecimal (primeiros 16 caracteres).
        """
        return hashlib.sha256(conteudo.encode("utf-8")).hexdigest()[:16]

    def _preparar_contexto(self) -> dict:
        """
        Prepara o contexto de dados para os templates de relatório.

        Retorna:
            dict: Dicionário com todos os dados necessários para renderização.
        """
        achados = self.analise.get("achados", [])
        dist = self.analise.get("distribuicao_severidade", {})
        top_achados = [a for a in achados if a["severidade"] in ("Crítica", "Alta")][:3]
        achados_ca = [a for a in achados if a["severidade"] in ("Crítica", "Alta")]

        risco = self.analise.get("risco_geral", "N/A")
        criticos = dist.get("Crítica", 0)
        altos = dist.get("Alta", 0)

        if risco == "Crítico":
            conclusao = (
                f"O sistema apresenta **{criticos} achado(s) crítico(s)** que requerem "
                "ação imediata. Recomenda-se suspender operações públicas do sistema até "
                "que as correções sejam implementadas e validadas."
            )
        elif risco == "Alto":
            conclusao = (
                f"O sistema apresenta **{altos} achado(s) de alta severidade**. "
                "Correções devem ser priorizadas no próximo ciclo de desenvolvimento "
                "ou no prazo máximo de 30 dias."
            )
        else:
            conclusao = (
                "O sistema apresenta achados de severidade moderada a baixa. "
                "Recomenda-se implementar as correções no próximo ciclo planejado."
            )

        hash_base = f"{self.nome_alvo}{self.data_relatorio}{len(achados)}"
        return {
            "data": self.data_relatorio,
            "alvo": self.nome_alvo,
            "tester": self.nome_tester,
            "risco_geral": risco,
            "total_achados": len(achados),
            "criticos": criticos,
            "altos": altos,
            "medios": dist.get("Média", 0),
            "baixos": dist.get("Baixa", 0),
            "conclusao": conclusao,
            "top_achados": top_achados,
            "achados": achados,
            "achados_criticos_altos": achados_ca,
            "hash_integridade": self._calcular_hash(hash_base),
        }

    def gerar_markdown(self, ctx: dict) -> tuple[str, str]:
        """
        Gera os relatórios executivo e técnico em formato Markdown.

        Parâmetros:
            ctx: Contexto de dados para renderização dos templates.

        Retorna:
            tuple: (caminho_executivo, caminho_tecnico) com os caminhos dos arquivos.
        """
        Path(self.diretorio_saida).mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        alvo_slug = self.nome_alvo.replace(" ", "_").lower()[:30]

        # Executivo
        tmpl_exec = self.env.from_string(TEMPLATE_EXECUTIVO)
        conteudo_exec = tmpl_exec.render(**ctx)
        caminho_exec = Path(self.diretorio_saida) / f"{alvo_slug}_executive_{ts}.md"
        caminho_exec.write_text(conteudo_exec, encoding="utf-8")

        # Técnico
        tmpl_tec = self.env.from_string(TEMPLATE_TECNICO)
        conteudo_tec = tmpl_tec.render(**ctx)
        caminho_tec = Path(self.diretorio_saida) / f"{alvo_slug}_technical_{ts}.md"
        caminho_tec.write_text(conteudo_tec, encoding="utf-8")

        self.logger.info(f"Relatórios Markdown gerados: {caminho_exec}, {caminho_tec}")
        return str(caminho_exec), str(caminho_tec)

    def gerar_pdf(self, caminho_md: str) -> Optional[str]:
        """
        Converte relatório Markdown para PDF usando reportlab.

        Parâmetros:
            caminho_md: Caminho do arquivo Markdown a converter.

        Retorna:
            str: Caminho do PDF gerado, ou None em caso de falha.
        """
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import cm
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
            from reportlab.lib import colors

            caminho_pdf = caminho_md.replace(".md", ".pdf")
            doc = SimpleDocTemplate(
                caminho_pdf, pagesize=A4,
                leftMargin=2*cm, rightMargin=2*cm,
                topMargin=2*cm, bottomMargin=2*cm
            )
            estilos = getSampleStyleSheet()

            # Estilo personalizado
            titulo_estilo = ParagraphStyle(
                "Titulo", parent=estilos["Title"],
                fontSize=16, spaceAfter=12, textColor=colors.HexColor("#1a1a2e")
            )
            aviso_estilo = ParagraphStyle(
                "Aviso", parent=estilos["Normal"],
                backColor=colors.HexColor("#fff3cd"),
                borderColor=colors.HexColor("#ffc107"),
                borderWidth=1, borderPadding=8,
                textColor=colors.HexColor("#856404"), fontSize=9
            )

            conteudo_md = Path(caminho_md).read_text(encoding="utf-8")
            elementos = []

            # Disclaimer no topo do PDF
            elementos.append(Paragraph(
                "⚠️ CONFIDENCIAL — Uso exclusivo para testes de segurança autorizados",
                aviso_estilo
            ))
            elementos.append(Spacer(1, 0.3*cm))

            # Processar linhas do markdown para elementos básicos
            for linha in conteudo_md.split("\n"):
                linha = linha.strip()
                if not linha:
                    elementos.append(Spacer(1, 0.2*cm))
                elif linha.startswith("# "):
                    elementos.append(Paragraph(linha[2:], titulo_estilo))
                elif linha.startswith("## "):
                    elementos.append(Paragraph(linha[3:], estilos["Heading2"]))
                elif linha.startswith("### "):
                    elementos.append(Paragraph(linha[4:], estilos["Heading3"]))
                elif linha.startswith("---"):
                    elementos.append(HRFlowable(width="100%", color=colors.grey))
                else:
                    # Formatar negrito básico
                    linha_fmt = linha.replace("**", "<b>", 1).replace("**", "</b>", 1)
                    try:
                        elementos.append(Paragraph(linha_fmt, estilos["Normal"]))
                    except Exception:
                        elementos.append(Paragraph(linha.replace("<", "&lt;").replace(">", "&gt;"), estilos["Normal"]))

            doc.build(elementos)
            self.logger.info(f"PDF gerado: {caminho_pdf}")
            return caminho_pdf
        except Exception as e:
            self.logger.warning(f"Falha ao gerar PDF: {e}")
            console.print(f"[yellow]⚠️ PDF não gerado (reportlab): {e}[/yellow]")
            return None

    def executar(self):
        """
        Orquestra a geração completa de todos os relatórios.

        Gera relatórios executivo e técnico em Markdown e tenta
        exportar o relatório executivo em PDF.
        """
        console.print(Panel("[bold green]📄 Gerador de Relatórios iniciado[/bold green]", border_style="green"))
        ctx = self._preparar_contexto()

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as p:
            t = p.add_task("Gerando relatórios Markdown...")
            exec_md, tec_md = self.gerar_markdown(ctx)
            p.remove_task(t)

            t = p.add_task("Exportando PDF...")
            pdf = self.gerar_pdf(exec_md)
            p.remove_task(t)

        console.print(f"[bold green]✅ Relatório Executivo: {exec_md}[/bold green]")
        console.print(f"[bold green]✅ Relatório Técnico:   {tec_md}[/bold green]")
        if pdf:
            console.print(f"[bold green]✅ PDF Exportado:       {pdf}[/bold green]")
        console.print(f"[cyan]   Log de Auditoria:   {self.log_file}[/cyan]")


def main():
    """Ponto de entrada principal do gerador de relatórios."""
    parser = argparse.ArgumentParser(description="Gerador de Relatórios — Ethical Red Team Skill")
    parser.add_argument("--analysis", required=True, help="Arquivo JSON da análise consolidada")
    parser.add_argument("--target", required=True, help="Nome descritivo do alvo")
    parser.add_argument("--tester", default="Pentester Anônimo", help="Nome do responsável pelo teste")
    parser.add_argument("--output", default="reports", help="Diretório de saída")
    args = parser.parse_args()

    gerador = GeradorRelatorio(args.analysis, args.target, args.tester, args.output)
    gerador.executar()


if __name__ == "__main__":
    main()
