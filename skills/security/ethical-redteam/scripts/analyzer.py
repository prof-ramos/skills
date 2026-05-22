#!/usr/bin/env python3
"""
analyzer.py — Módulo de Análise e Correlação de Resultados.

Consolida os resultados de reconhecimento e scanning, classifica
vulnerabilidades por severidade CVSS v3.1, e gera recomendações
baseadas nas diretrizes OWASP e NIST SP 800-115.

Uso:
    python scripts/analyzer.py --scan scan_output/arquivo.json
    python scripts/analyzer.py --recon recon_output/arquivo.json --scan scan_output/arquivo.json

Autor: Ethical RedTeam Skill
Versão: 1.0.0
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
except ImportError as e:
    print(f"[ERRO] {e}. Execute o install.sh primeiro.")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).parent))
from utils import configurar_logger, salvar_json, calcular_severidade_cvss

console = Console()

# Mapeamento de portas/serviços para achados comuns (base de conhecimento interna)
BASE_CONHECIMENTO = {
    21: {"servico": "FTP", "descricao": "FTP sem criptografia", "cvss": 7.5,
         "cve_ref": "CWE-319", "recomendacao": "Migrar para SFTP ou FTPS"},
    22: {"servico": "SSH", "descricao": "SSH exposto publicamente", "cvss": 3.7,
         "cve_ref": "CWE-284", "recomendacao": "Restringir acesso por IP, usar chaves SSH, desabilitar senha"},
    23: {"servico": "Telnet", "descricao": "Telnet sem criptografia", "cvss": 9.8,
         "cve_ref": "CWE-319", "recomendacao": "Desabilitar Telnet imediatamente, usar SSH"},
    25: {"servico": "SMTP", "descricao": "SMTP sem autenticação/TLS", "cvss": 6.5,
         "cve_ref": "CWE-306", "recomendacao": "Configurar STARTTLS e autenticação obrigatória"},
    80: {"servico": "HTTP", "descricao": "HTTP não criptografado", "cvss": 5.3,
         "cve_ref": "CWE-319", "recomendacao": "Redirecionar para HTTPS, implementar HSTS"},
    443: {"servico": "HTTPS", "descricao": "HTTPS — verificar certificado e versão TLS", "cvss": 0.0,
          "cve_ref": None, "recomendacao": "Verificar TLS 1.2+, certificado válido, HSTS habilitado"},
    3306: {"servico": "MySQL", "descricao": "Banco de dados MySQL exposto na rede", "cvss": 8.8,
           "cve_ref": "CWE-284", "recomendacao": "Restringir acesso ao banco por firewall, nunca expor publicamente"},
    3389: {"servico": "RDP", "descricao": "Remote Desktop Protocol exposto", "cvss": 9.8,
           "cve_ref": "CVE-2019-0708", "recomendacao": "Usar VPN, habilitar NLA, aplicar patches BlueKeep"},
    5432: {"servico": "PostgreSQL", "descricao": "PostgreSQL exposto na rede", "cvss": 8.8,
           "cve_ref": "CWE-284", "recomendacao": "Restringir acesso, usar pg_hba.conf corretamente"},
    6379: {"servico": "Redis", "descricao": "Redis sem autenticação exposto", "cvss": 9.8,
           "cve_ref": "CWE-306", "recomendacao": "Habilitar AUTH, bind apenas localhost, usar TLS"},
    27017: {"servico": "MongoDB", "descricao": "MongoDB sem autenticação", "cvss": 9.8,
            "cve_ref": "CWE-306", "recomendacao": "Habilitar autenticação, bind localhost, usar TLS"},
    8080: {"servico": "HTTP-Alt", "descricao": "Servidor HTTP alternativo", "cvss": 5.3,
           "cve_ref": "CWE-319", "recomendacao": "Verificar se é necessário, adicionar autenticação"},
}

RECOMENDACOES_CABECALHOS = {
    "Server": "Remover/ofuscar cabeçalho Server para não revelar tecnologia",
    "X-Powered-By": "Remover cabeçalho X-Powered-By (revela tecnologia)",
    "X-Frame-Options": "Adicionar X-Frame-Options: DENY para prevenir Clickjacking",
    "X-Content-Type-Options": "Adicionar X-Content-Type-Options: nosniff",
    "Strict-Transport-Security": "Implementar HSTS: max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "Implementar Content-Security-Policy restritiva",
}


class ModuloAnalyzer:
    """
    Módulo de análise e correlação de vulnerabilidades.

    Processa resultados de reconhecimento e scanning para gerar
    achados classificados por severidade com recomendações OWASP/NIST.
    """

    def __init__(self, arquivo_recon: Optional[str], arquivo_scan: Optional[str], diretorio_saida: str):
        """
        Inicializa o módulo de análise.

        Parâmetros:
            arquivo_recon: Caminho para o JSON de reconhecimento (opcional).
            arquivo_scan: Caminho para o JSON de scanning (opcional).
            diretorio_saida: Diretório para salvar a análise consolidada.
        """
        self.arquivo_recon = arquivo_recon
        self.arquivo_scan = arquivo_scan
        self.diretorio_saida = diretorio_saida
        self.logger, self.log_file = configurar_logger("analyzer")
        self.dados_recon = self._carregar_json(arquivo_recon) if arquivo_recon else {}
        self.dados_scan = self._carregar_json(arquivo_scan) if arquivo_scan else {}
        self.achados: list = []

    def _carregar_json(self, caminho: str) -> dict:
        """
        Carrega e valida um arquivo JSON de entrada.

        Parâmetros:
            caminho: Caminho para o arquivo JSON.

        Retorna:
            dict: Dados carregados do arquivo.
        """
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"Arquivo não encontrado: {caminho}")
            console.print(f"[bold red]❌ Arquivo não encontrado: {caminho}[/bold red]")
            sys.exit(1)
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON inválido em {caminho}: {e}")
            console.print(f"[bold red]❌ JSON inválido: {e}[/bold red]")
            sys.exit(1)

    def analisar_portas(self):
        """
        Analisa portas abertas do scan e gera achados baseados na base de conhecimento.

        Correlaciona cada porta aberta com a base de conhecimento interna
        para identificar configurações potencialmente inseguras.
        """
        if not self.dados_scan:
            return

        for host in self.dados_scan.get("hosts", []):
            for porta in host.get("portas", []):
                if porta["estado"] != "open":
                    continue

                num_porta = porta["porta"]
                info_bk = BASE_CONHECIMENTO.get(num_porta)

                if info_bk:
                    achado = {
                        "id": f"SCAN-{num_porta:05d}",
                        "tipo": "Porta/Serviço",
                        "host": host["ip"],
                        "porta": num_porta,
                        "servico": porta.get("servico", info_bk["servico"]),
                        "produto": porta.get("produto", ""),
                        "versao": porta.get("versao", ""),
                        "descricao": info_bk["descricao"],
                        "cvss_score": info_bk["cvss"],
                        "severidade": calcular_severidade_cvss(info_bk["cvss"]),
                        "cve_ref": info_bk.get("cve_ref"),
                        "recomendacao": info_bk["recomendacao"],
                        "evidencia": f"Porta {num_porta}/tcp aberta em {host['ip']}",
                        "frameworks": ["OWASP A05:2021", "NIST SP 800-115 §6.1"],
                    }
                    self.achados.append(achado)
                    self.logger.info(f"Achado: {achado['id']} | {achado['severidade']} | {achado['descricao']}")

    def analisar_cabecalhos_http(self):
        """
        Analisa cabeçalhos HTTP do reconhecimento para identificar ausências de segurança.

        Verifica a presença de cabeçalhos de segurança recomendados pela
        OWASP Secure Headers Project.
        """
        if not self.dados_recon:
            return

        headers = self.dados_recon.get("osint", {}).get("http_headers", {}).get("headers", {})
        headers_lower = {k.lower(): v for k, v in headers.items()}

        cabecalhos_seguranca = {
            "strict-transport-security": ("HSTS ausente", 6.1, "OWASP A05:2021"),
            "x-frame-options": ("X-Frame-Options ausente (Clickjacking)", 4.3, "OWASP A05:2021"),
            "x-content-type-options": ("X-Content-Type-Options ausente", 3.7, "OWASP A05:2021"),
            "content-security-policy": ("Content-Security-Policy ausente", 5.4, "OWASP A03:2021"),
        }

        for cabecalho, (descricao, cvss, framework) in cabecalhos_seguranca.items():
            if cabecalho not in headers_lower:
                achado = {
                    "id": f"HTTP-{cabecalho.upper()[:10]}",
                    "tipo": "Cabeçalho HTTP",
                    "host": self.dados_recon.get("alvo", "N/A"),
                    "descricao": descricao,
                    "cvss_score": cvss,
                    "severidade": calcular_severidade_cvss(cvss),
                    "recomendacao": RECOMENDACOES_CABECALHOS.get(
                        cabecalho, f"Implementar cabeçalho {cabecalho}"
                    ),
                    "evidencia": f"Cabeçalho '{cabecalho}' não encontrado na resposta HTTP",
                    "frameworks": [framework, "NIST CSF PR.PT-4"],
                }
                self.achados.append(achado)

    def _calcular_risco_geral(self) -> str:
        """
        Calcula o nível de risco geral baseado nos achados identificados.

        Retorna:
            str: Classificação de risco geral (Crítico/Alto/Médio/Baixo/Mínimo).
        """
        if any(a["severidade"] == "Crítica" for a in self.achados):
            return "Crítico"
        elif any(a["severidade"] == "Alta" for a in self.achados):
            return "Alto"
        elif any(a["severidade"] == "Média" for a in self.achados):
            return "Médio"
        elif any(a["severidade"] == "Baixa" for a in self.achados):
            return "Baixo"
        return "Mínimo"

    def executar(self) -> str:
        """
        Executa a análise completa e salva o relatório consolidado.

        Retorna:
            str: Caminho do arquivo JSON com a análise consolidada.
        """
        console.print(Panel("[bold green]🔎 Análise iniciada[/bold green]", border_style="green"))

        self.analisar_portas()
        self.analisar_cabecalhos_http()

        # Ordenar por severidade
        ordem_severidade = {"Crítica": 0, "Alta": 1, "Média": 2, "Baixa": 3, "Informativa": 4}
        self.achados.sort(key=lambda x: ordem_severidade.get(x["severidade"], 5))

        alvo = (self.dados_scan or self.dados_recon).get("alvo", "desconhecido")
        analise = {
            "alvo": alvo,
            "timestamp": datetime.now().isoformat(),
            "risco_geral": self._calcular_risco_geral(),
            "total_achados": len(self.achados),
            "distribuicao_severidade": {
                sev: len([a for a in self.achados if a["severidade"] == sev])
                for sev in ["Crítica", "Alta", "Média", "Baixa", "Informativa"]
            },
            "achados": self.achados,
            "log_auditoria": self.log_file,
        }

        # Exibir resumo
        tabela = Table(title="📊 Resumo da Análise", border_style="cyan")
        tabela.add_column("Severidade", style="bold")
        tabela.add_column("Quantidade", style="green")
        cores = {"Crítica": "red", "Alta": "orange1", "Média": "yellow", "Baixa": "cyan", "Informativa": "white"}
        for sev, qtd in analise["distribuicao_severidade"].items():
            cor = cores.get(sev, "white")
            tabela.add_row(f"[{cor}]{sev}[/{cor}]", str(qtd))
        tabela.add_row("[bold]Risco Geral[/bold]", f"[bold]{analise['risco_geral']}[/bold]")
        console.print(tabela)

        caminho = salvar_json(analise, f"{alvo.replace('.', '_')}_analysis", self.diretorio_saida)
        console.print(f"[bold green]✅ Análise salva em: {caminho}[/bold green]")
        return caminho


def main():
    """Ponto de entrada principal do módulo de análise."""
    parser = argparse.ArgumentParser(description="Módulo de Análise — Ethical Red Team Skill")
    parser.add_argument("--recon", help="Arquivo JSON do reconhecimento")
    parser.add_argument("--scan", help="Arquivo JSON do scanning")
    parser.add_argument("--output", default="analysis", help="Diretório de saída")
    args = parser.parse_args()

    if not args.recon and not args.scan:
        parser.error("Forneça pelo menos --recon ou --scan")

    modulo = ModuloAnalyzer(args.recon, args.scan, args.output)
    modulo.executar()


if __name__ == "__main__":
    main()
