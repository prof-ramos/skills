
import os, zipfile
from pathlib import Path

BASE = "ethical-redteam-skill"

# ─────────────────────────────────────────────
# 7. scripts/reporter.py
# ─────────────────────────────────────────────
reporter_py = '''#!/usr/bin/env python3
"""
reporter.py — Gerador de Relatórios de Segurança (Markdown + PDF).

Gera relatórios profissionais de segurança com seções executiva, técnica,
recomendações e evidências, em conformidade com OWASP Testing Guide e
NIST SP 800-115. Inclui timestamp e hash de integridade como assinatura.

Uso:
    python scripts/reporter.py --analysis analysis/arquivo.json \\
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
            for linha in conteudo_md.split("\\n"):
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
'''

with open(f"{BASE}/scripts/reporter.py", "w", encoding="utf-8") as f:
    f.write(reporter_py)
print("reporter.py criado.")

# ─────────────────────────────────────────────
# 8. references/ethics-guide.md
# ─────────────────────────────────────────────
ethics_guide = """# Guia de Ética e Conformidade Legal

> **Esta SKILL é destinada exclusivamente para testes de segurança autorizados em ambientes controlados.**

## 1. Princípios Fundamentais

### 1.1 Autorização Prévia (Authorization First)

Nunca execute qualquer teste sem autorização **escrita e documentada** do proprietário legal do sistema.
A autorização deve especificar:

- **Escopo:** Quais sistemas, IPs, domínios estão autorizados
- **Janela temporal:** Datas e horários permitidos
- **Profundidade:** Quais tipos de teste são permitidos
- **Ponto de contato:** Pessoa responsável do lado do cliente
- **Procedimento de emergência:** Como agir se causar impacto inadvertido

### 1.2 Rules of Engagement (RoE)

Documente formalmente antes de iniciar:

```markdown
## Rules of Engagement — [Nome do Projeto]

**Cliente:** ___________________________
**Testador:** __________________________
**Período:** De ___ / ___ / ___ até ___ / ___ / ___
**Escopo autorizado:**
  - IPs/Ranges: ________________________
  - Domínios: _________________________
  - Aplicações: _______________________
**Escopo PROIBIDO:**
  - _________________________________
**Tipos de teste autorizados:** [ ] Passivo  [ ] Ativo  [ ] Exploração
**Contato de emergência:** _____________
**Assinatura do cliente:** _____________
```

### 1.3 Princípio do Mínimo Dano

- Prefira **reconhecimento passivo** sempre que possível
- Evite testes que possam **derrubar serviços** (DoS não autorizado)
- Documente **cada ação** para auditoria posterior
- **Pare imediatamente** se detectar impacto não previsto

---

## 2. Marco Legal Brasileiro

### Lei 12.737/2012 (Lei Carolina Dieckmann)
Tipifica crimes informáticos. Acesso não autorizado a sistemas é crime com pena de **detenção de 3 meses a 1 ano**.

### Marco Civil da Internet (Lei 12.965/2014)
Define direitos e deveres no uso da internet. Pentest sem autorização viola os artigos de proteção à privacidade.

### LGPD (Lei 13.709/2018)
Durante testes, dados pessoais encontrados devem ser protegidos e reportados, não armazenados.

### Código Penal — Art. 154-A
*"Invadir dispositivo informático alheio, conectado ou não à rede de computadores, mediante violação indevida de mecanismo de segurança..."*
Pena: **reclusão de 1 a 4 anos**, e multa.

---

## 3. Legislação Internacional Relevante

| País | Lei | Pena Máxima |
|------|-----|-------------|
| EUA | CFAA (Computer Fraud and Abuse Act) | 10-20 anos de prisão |
| Reino Unido | Computer Misuse Act 1990 | 10 anos |
| União Europeia | Directive 2013/40/EU | Harmonização entre países |
| Austrália | Criminal Code Act 1995 | 10 anos |

---

## 4. Boas Práticas Operacionais

### 4.1 Antes do Teste
- [ ] Contrato assinado com escopo detalhado
- [ ] NDA (Non-Disclosure Agreement) em vigor
- [ ] Comunicação com equipe interna de segurança do cliente
- [ ] Backup do ambiente de teste (se aplicável)

### 4.2 Durante o Teste
- [ ] Logs de todas as ações habilitados
- [ ] Janelas de teste respeitadas
- [ ] Comunicação imediata de achados críticos ao cliente
- [ ] Nenhum dado exfiltrado para fora do escopo

### 4.3 Após o Teste
- [ ] Relatório entregue apenas ao cliente autorizado
- [ ] Dados coletados descartados conforme acordo
- [ ] Sessão de debriefing com o cliente
- [ ] Acompanhamento das correções (se contratado)

---

## 5. Programas de Bug Bounty

Ao participar de programas de Bug Bounty (HackerOne, Bugcrowd, etc.):

1. **Leia o escopo completo** antes de iniciar qualquer teste
2. **Respeite os limites de taxa** (rate limiting) definidos pelo programa
3. **Reporte responsavelmente:** Nunca divulgue publicamente antes do prazo acordado
4. **Não acesse dados reais de usuários**, mesmo que encontre a vulnerabilidade
5. **Documente com evidências mínimas suficientes** — não colete mais do que o necessário

### Plataformas Reconhecidas
- [HackerOne](https://hackerone.com)
- [Bugcrowd](https://bugcrowd.com)
- [Intigriti](https://intigriti.com)
- [Open Bug Bounty](https://openbugbounty.org)
- [Programa de Bug Bounty do Governo Federal Brasileiro](https://www.gov.br/seguranca)

---

## 6. Certificações Recomendadas

| Certificação | Emissor | Foco |
|---|---|---|
| OSCP | Offensive Security | Pentest Prático |
| CEH | EC-Council | Hacking Ético |
| eJPT | eLearnSecurity | Junior Pentest |
| BSCP | PortSwigger | Web Security |
| GPEN | GIAC | Pentest Avançado |

---

*Última atualização: 2025 | Ethical Red Team Skill v1.0.0*
"""

with open(f"{BASE}/references/ethics-guide.md", "w", encoding="utf-8") as f:
    f.write(ethics_guide)

# ─────────────────────────────────────────────
# 9. references/owasp-checklist.md
# ─────────────────────────────────────────────
owasp_checklist = """# Checklist OWASP Testing Guide v4.2 + NIST SP 800-115

> Referência para cobertura metodológica dos testes de segurança.

## OWASP Top 10 (2021) — Verificações por Módulo

| ID | Categoria | Módulo da Skill | Verificações |
|----|-----------|-----------------|--------------|
| A01 | Broken Access Control | scanner + analyzer | Exposição de endpoints autenticados, IDOR |
| A02 | Cryptographic Failures | recon + scanner | HTTP sem TLS, cifras fracas, FTP/Telnet aberto |
| A03 | Injection | scanner (NSE scripts) | SQLi via nmap NSE, cabeçalhos de erro |
| A04 | Insecure Design | analyzer | Análise de arquitetura baseada nos achados |
| A05 | Security Misconfiguration | scanner + analyzer | Cabeçalhos HTTP, portas desnecessárias, banners |
| A06 | Vulnerable Components | scanner (versões) | Versões detectadas vs CVEs conhecidos |
| A07 | Auth Failures | scanner | Serviços sem auth (Redis, MongoDB, FTP anon) |
| A08 | Software Integrity Failures | recon | Subdomínios não autorizados, takeover |
| A09 | Logging Failures | (manual) | Verificar se sistema loga adequadamente |
| A10 | SSRF | recon (HTTP) | Cabeçalhos de resposta, redirecionamentos |

---

## NIST SP 800-115 — Fases de Teste

### Fase 1: Planejamento
- [ ] Definir escopo e objetivos
- [ ] Obter autorização formal
- [ ] Identificar restrições operacionais

### Fase 2: Descoberta (recon.py)
- [ ] Reconhecimento de rede passivo
- [ ] Identificação de hosts ativos
- [ ] Enumeração de serviços
- [ ] Identificação de vulnerabilidades

### Fase 3: Ataque (scanner.py)
- [ ] Exploração controlada de vulnerabilidades
- [ ] Escalação de privilégios (se autorizado)
- [ ] Pivotamento (se autorizado no escopo)

### Fase 4: Relatório (reporter.py)
- [ ] Documentar todas as vulnerabilidades
- [ ] Classificar por severidade (CVSS)
- [ ] Fornecer recomendações acionáveis
- [ ] Revisão de qualidade

---

## CVSS v3.1 — Escala de Severidade

| Score | Severidade | Cor | SLA Recomendado |
|-------|-----------|-----|-----------------|
| 9.0–10.0 | Crítica | 🔴 | 24-48 horas |
| 7.0–8.9 | Alta | 🟠 | 7 dias |
| 4.0–6.9 | Média | 🟡 | 30 dias |
| 0.1–3.9 | Baixa | 🟢 | 90 dias |
| 0.0 | Informativa | ⚪ | Próximo ciclo |

---

## Referências

- [OWASP Testing Guide v4.2](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST SP 800-115](https://csrc.nist.gov/publications/detail/sp/800/115/final)
- [CVSS v3.1 Specification](https://www.first.org/cvss/specification-document)
- [OWASP Top 10 2021](https://owasp.org/Top10/)
"""

with open(f"{BASE}/references/owasp-checklist.md", "w", encoding="utf-8") as f:
    f.write(owasp_checklist)

# ─────────────────────────────────────────────
# 10. references/examples/sample-report.md
# ─────────────────────────────────────────────
sample_report = """# Relatório de Segurança — EXEMPLO FICTÍCIO

> ⚠️ **DADOS FICTÍCIOS PARA FINS DIDÁTICOS — NÃO REPRESENTA NENHUM SISTEMA REAL**

**Data:** 10/03/2025 às 14:30:00
**Alvo:** Lab Teste Interno (192.168.100.0/24 — ambiente fictício)
**Responsável:** Pentester Exemplo
**Hash de Integridade:** `a1b2c3d4e5f6g7h8`

---

## Visão Geral do Risco

| Indicador | Valor |
|-----------|-------|
| Risco Geral | **Alto** |
| Total de Achados | 5 |
| Achados Críticos | 🔴 1 |
| Achados Altos | 🟠 2 |
| Achados Médios | 🟡 2 |

## Achados

### 1. Redis sem autenticação exposto (CRÍTICO — CVSS 9.8)
- **Host:** 192.168.100.15
- **Porta:** 6379/tcp
- **Evidência:** `redis-cli -h 192.168.100.15 ping` retornou `PONG` sem senha
- **Recomendação:** Habilitar AUTH no redis.conf, bind apenas localhost, implementar TLS

### 2. Telnet habilitado (CRÍTICO — CVSS 9.8)
- **Host:** 192.168.100.20
- **Porta:** 23/tcp
- **Evidência:** Banner: `Ubuntu 20.04 LTS telnetd`
- **Recomendação:** Desabilitar Telnet imediatamente, migrar para SSH com chaves

### 3. HTTP sem HTTPS (MÉDIO — CVSS 5.3)
- **Host:** 192.168.100.10
- **Porta:** 80/tcp
- **Evidência:** Acesso à porta 80 sem redirecionamento para 443
- **Recomendação:** Implementar certificado TLS, configurar redirecionamento 301

---

*Relatório gerado pela Ethical Red Team Skill v1.0.0 — Dados fictícios para fins educacionais*
"""

with open(f"{BASE}/references/examples/sample-report.md", "w", encoding="utf-8") as f:
    f.write(sample_report)

# ─────────────────────────────────────────────
# 11. assets/report-template.md
# ─────────────────────────────────────────────
report_template = """# Relatório de Segurança — [NOME DO ALVO]

> ⚠️ CONFIDENCIAL — Uso restrito às partes autorizadas

**Data:** [DATA]
**Alvo:** [NOME/IP DO ALVO]
**Responsável:** [NOME DO TESTADOR]
**Número do Relatório:** [REF-YYYY-NNN]
**Hash de Integridade:** `[HASH SHA-256]`

---

## 1. Sumário Executivo

[Descrição em linguagem não técnica do estado geral de segurança do alvo,
destacando os riscos mais críticos e o impacto potencial ao negócio.]

### Distribuição de Achados

| Severidade | Quantidade | SLA Recomendado |
|-----------|-----------|-----------------|
| 🔴 Crítica | X | 24-48 horas |
| 🟠 Alta | X | 7 dias |
| 🟡 Média | X | 30 dias |
| 🟢 Baixa | X | 90 dias |
| ⚪ Informativa | X | Próximo ciclo |

---

## 2. Metodologia

- **Framework:** OWASP Testing Guide v4.2 + NIST SP 800-115
- **Período:** [DATA INÍCIO] a [DATA FIM]
- **Tipo de teste:** [Black Box / Grey Box / White Box]
- **Ferramentas:** nmap, subfinder, theHarvester, nuclei

---

## 3. Achados Detalhados

### 3.1 [TÍTULO DO ACHADO] — [SEVERIDADE]

| Campo | Valor |
|-------|-------|
| **ID** | FIND-001 |
| **CVSS Score** | X.X |
| **CWE/CVE** | CWE-XXX |
| **Host/Serviço** | [HOST:PORTA] |
| **Framework** | OWASP AXX:2021 |

**Descrição:**
[Descrição técnica clara da vulnerabilidade.]

**Evidência:**
```
[Saída de comando / screenshot / log que comprova a vulnerabilidade]
```

**Impacto:**
[Impacto potencial ao negócio se explorada.]

**Recomendação:**
[Passos concretos e acionáveis para correção.]

**Referências:**
- [Link para documentação OWASP/NIST relevante]

---

## 4. Recomendações Consolidadas

### Ações Imediatas (24-48h)
- [ ] [Ação crítica 1]

### Curto Prazo (7 dias)
- [ ] [Ação alta 1]

### Médio Prazo (30 dias)
- [ ] [Ação média 1]

---

## 5. Conclusão

[Conclusão geral com avaliação do nível de maturidade de segurança e
próximos passos recomendados.]

---

*Gerado pela Ethical Red Team Skill v1.0.0*
*Conformidade: OWASP Testing Guide v4.2 | NIST SP 800-115 | CVSS v3.1*
"""

with open(f"{BASE}/assets/report-template.md", "w", encoding="utf-8") as f:
    f.write(report_template)

# ─────────────────────────────────────────────
# 12. README.md (nível de repositório — FORA da pasta da skill)
# ─────────────────────────────────────────────
readme_md = """# Ethical Red Team & Bug Bounty Skill para Claude

> ⚠️ **Esta SKILL é destinada exclusivamente para testes de segurança autorizados em ambientes controlados.**

[![Licença: MIT](https://img.shields.io/badge/Licença-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![macOS 13+](https://img.shields.io/badge/macOS-13%2B%20Apple%20Silicon-lightgrey.svg)](https://apple.com)
[![OWASP](https://img.shields.io/badge/Conformidade-OWASP%20%7C%20NIST-green.svg)](https://owasp.org)

## O que é?

Uma **Claude Skill** profissional que transforma o Claude em um assistente de Red Team/Bug Bounty,
conduzindo testes de segurança éticos com reconhecimento, scanning, análise e geração de relatórios
OWASP/NIST — otimizado para **Apple Silicon M3** com 8GB RAM.

## Instalação

### Requisitos
- macOS 13+ (Ventura ou superior)
- Apple Silicon M1/M2/M3 (ARM64)
- 8GB RAM (consome máx. 4GB)
- Homebrew instalado

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/ethical-redteam-skill.git
cd ethical-redteam-skill
```

### 2. Executar o instalador automático
```bash
chmod +x ethical-redteam-skill/scripts/install.sh
./ethical-redteam-skill/scripts/install.sh
```

O instalador detecta automaticamente a arquitetura M3 e instala binários ARM64 nativos.

### 3. Instalar a Skill no Claude

1. Comprima a pasta: `zip -r ethical-redteam-skill.zip ethical-redteam-skill/`
2. Acesse Claude.ai → Settings → Capabilities → Skills
3. Clique em "Upload skill" e selecione o arquivo `.zip`
4. Ative a skill nas configurações

## Uso Rápido

```bash
# Ativar ambiente virtual
source ethical-redteam-skill/.venv-redteam/bin/activate

# 1. Reconhecimento passivo
python ethical-redteam-skill/scripts/recon.py --target alvo-autorizado.com --mode passive

# 2. Scan padrão
python ethical-redteam-skill/scripts/scanner.py --target 192.168.1.1 --profile standard

# 3. Análise consolidada
python ethical-redteam-skill/scripts/analyzer.py --scan scan_output/ARQUIVO.json

# 4. Gerar relatório
python ethical-redteam-skill/scripts/reporter.py \\
       --analysis analysis/ARQUIVO.json \\
       --target "Meu Alvo" --tester "Meu Nome"
```

## Estrutura do Repositório

```
ethical-redteam-skill/          ← Pasta da Skill (fazer upload desta)
├── SKILL.md                    ← Arquivo principal da Skill (obrigatório)
├── scripts/
│   ├── install.sh              ← Instalador inteligente (M3-aware)
│   ├── utils.py                ← Utilitários compartilhados
│   ├── recon.py                ← Módulo de reconhecimento OSINT/DNS
│   ├── scanner.py              ← Módulo de scanning nmap
│   ├── analyzer.py             ← Análise e correlação CVSS
│   └── reporter.py             ← Gerador de relatórios MD+PDF
├── references/
│   ├── ethics-guide.md         ← Guia de ética e conformidade legal
│   ├── owasp-checklist.md      ← Checklist OWASP/NIST
│   └── examples/
│       └── sample-report.md    ← Exemplo de relatório (dados fictícios)
└── assets/
    └── report-template.md      ← Template padrão de relatório
```

## Módulos

| Módulo | Função | RAM Estimada |
|--------|--------|--------------|
| `recon.py` | OSINT, DNS, subdomínios, WHOIS | ~200MB |
| `scanner.py` | Nmap portas/serviços (3 perfis) | 200MB–2GB |
| `analyzer.py` | Correlação CVSS, achados OWASP | ~150MB |
| `reporter.py` | Relatórios MD + PDF | ~100MB |

## Aviso Legal

O uso não autorizado desta ferramenta contra sistemas de terceiros é **ilegal** conforme:
- Lei 12.737/2012 (Lei Carolina Dieckmann)
- Marco Civil da Internet (Lei 12.965/2014)  
- Código Penal Brasileiro — Art. 154-A
- CFAA (para alvos nos EUA)

Consulte `ethical-redteam-skill/references/ethics-guide.md` para orientação completa.

## Licença

MIT License — Veja [LICENSE](LICENSE) para detalhes.
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_md)
print("README.md criado (nível de repositório).")

# ─────────────────────────────────────────────
# 13. Criar ZIP final
# ─────────────────────────────────────────────
zip_path = "ethical-redteam-skill.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(BASE):
        for file in files:
            filepath = os.path.join(root, file)
            arcname = os.path.relpath(filepath, ".")
            zf.write(filepath, arcname)

print(f"\n✅ ZIP criado: {zip_path}")
print(f"   Tamanho: {os.path.getsize(zip_path)/1024:.1f} KB")

# Listar conteúdo
print("\n📁 Estrutura do ZIP:")
with zipfile.ZipFile(zip_path, "r") as zf:
    for name in sorted(zf.namelist()):
        print(f"   {name}")
